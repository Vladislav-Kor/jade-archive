import { defineStore } from 'pinia'
import { ref } from 'vue'
import { personsApi } from '@/api/endpoints/persons'
import { relationsApi } from '@/api/endpoints/relations'
import { digitalAccountsApi } from '@/api/endpoints/digital-accounts'
import { partnersApi } from '@/api/endpoints/partners'
import { devicesApi } from '@/api/endpoints/devices'
import { crossRecordsApi } from '@/api/endpoints/cross-records'
import { realEstateApi } from '@/api/endpoints/real-estate'
import { vehiclesApi } from '@/api/endpoints/vehicles'
import { casesApi } from '@/api/endpoints/cases'
import { medicalApi } from '@/api/endpoints/medical'
import { socialApi } from '@/api/endpoints/social'
import type { PersonResource } from '@/api/resource'
import { useTreeStore } from './useTreeStore'
import { useToast } from '@/composables/useToast'

/** Коллекции профиля: ключ — поле человека, значение — API ресурса. */
const RESOURCES = {
    social_media: socialApi,
    digital_accounts: digitalAccountsApi,
    real_estate: realEstateApi,
    vehicles: vehiclesApi,
    cases: casesApi,
    medical_records: medicalApi,
    partners: partnersApi,
    devices: devicesApi,
    cross_records: crossRecordsApi,
} satisfies Record<string, PersonResource>

export type ResourceKey = keyof typeof RESOURCES
export type CollectionKey = ResourceKey | 'relations'

const COLLECTION_KEYS = ['relations', ...Object.keys(RESOURCES), 'tags_prefs']

/** Названия вкладок для сообщений пользователю. */
const LABELS: Record<string, string> = {
    relations: 'связи', social_media: 'соцсети', digital_accounts: 'аккаунты', real_estate: 'недвижимость',
    vehicles: 'транспорт', cases: 'дела', medical_records: 'медицина', partners: 'партнёры',
    devices: 'устройства', cross_records: 'записи',
}

/** Только поля самого человека: коллекции в ответах /persons не отфильтрованы (там и удалённые). */
function personFields(person: any) {
    const out = { ...person }
    for (const key of COLLECTION_KEYS) delete out[key]
    return out
}

export const usePersonStore = defineStore('person', () => {
    const currentPerson = ref<any | null>(null)
    const isLoading = ref(false)
    const tree = useTreeStore()
    const { error: toastError } = useToast()
    let loadToken = 0

    const fetchList = (key: string, load: () => Promise<any[]>, failed: string[]) =>
        load().catch(() => { failed.push(key); return [] })

    /**
     * Загружает человека со всеми вкладками. Спиннер — только при переходе к другому человеку;
     * ответ на устаревший запрос (уже выбран другой) отбрасывается.
     */
    const loadPerson = async (id: number) => {
        const token = ++loadToken
        if (currentPerson.value?.id !== id) isLoading.value = true
        const failed: string[] = []
        try {
            const [person, relations, ...lists] = await Promise.all([
                personsApi.getById(id),
                fetchList('relations', () => relationsApi.getForPerson(id), failed),
                ...Object.entries(RESOURCES).map(([key, api]) => fetchList(key, () => api.getForPerson(id), failed)),
            ])
            if (token !== loadToken) return
            const collections = Object.fromEntries(Object.keys(RESOURCES).map((key, i) => [key, lists[i]]))
            currentPerson.value = { ...personFields(person), relations, ...collections }
            if (failed.length) toastError(`Не удалось загрузить: ${failed.map((k) => LABELS[k] ?? k).join(', ')}`)
        } catch (err: any) {
            if (token === loadToken) toastError(err.message || 'Ошибка загрузки контакта')
        } finally {
            if (token === loadToken) isLoading.value = false
        }
    }

    /** Тихая перезагрузка открытого профиля (кнопка «Обновить»), без спиннера. */
    const refreshCurrent = async () => {
        if (currentPerson.value) await loadPerson(currentPerson.value.id)
    }

    const clearCurrent = () => {
        loadToken++
        currentPerson.value = null
        isLoading.value = false
    }

    const requirePerson = () => {
        if (!currentPerson.value) throw new Error('Контакт не выбран')
        return currentPerson.value
    }

    const setCollection = (personId: number, key: CollectionKey, items: any[]) => {
        if (currentPerson.value?.id === personId) currentPerson.value[key] = items
    }

    // ---- связи: в профиле — производный вид (direction, person_name), поэтому перечитываем список ----
    const reloadRelations = async (personId: number) => {
        setCollection(personId, 'relations', await relationsApi.getForPerson(personId))
    }

    const createRelation = async (data: { parent_id: number; child_id: number; relation_type: string }) => {
        const relation = await relationsApi.create(data)
        tree.upsertRelation(relation)
        const openId = currentPerson.value?.id
        if (openId === data.parent_id || openId === data.child_id) await reloadRelations(openId)
        return relation
    }

    const deleteRelation = async (id: number) => {
        await relationsApi.delete(id)
        tree.removeRelation(id)
    }

    // ---- остальные коллекции: стор правится ответом сервера, без перезагрузки ----
    const createItem = async (key: CollectionKey, data: any) => {
        if (key === 'relations') return createRelation(data)
        const person = requirePerson()
        const item = await RESOURCES[key].create(person.id, data)
        setCollection(person.id, key, [...(currentPerson.value?.[key] ?? []), item])
        return item
    }

    const updateItem = async (key: ResourceKey, id: number, data: any) => {
        const person = requirePerson()
        const item = await RESOURCES[key].update(id, data)
        const list = (currentPerson.value?.[key] ?? []) as any[]
        // Снятый флаг «активно» прячет запись так же, как это делает сервер в списках.
        const next = item?.is_active === false
            ? list.filter((x) => x.id !== id)
            : list.map((x) => (x.id === id ? item : x))
        setCollection(person.id, key, next)
        return item
    }

    /** Удаление сразу убирает запись; если сервер отказал — возвращает её на место. */
    const deleteItem = async (key: CollectionKey, id: number) => {
        const person = requirePerson()
        const list = (person[key] ?? []) as any[]
        const index = list.findIndex((x) => x.id === id)
        const removed = list[index]
        setCollection(person.id, key, list.filter((x) => x.id !== id))
        try {
            if (key === 'relations') await deleteRelation(id)
            else await RESOURCES[key].delete(id)
        } catch (err) {
            if (removed && currentPerson.value?.id === person.id) {
                const restored = [...(currentPerson.value[key] ?? [])]
                restored.splice(index, 0, removed)
                currentPerson.value[key] = restored
            }
            throw err
        }
    }

    // ---- сам человек: профиль и строка в боковой панели обновляются вместе ----
    const createPerson = async (data: any) => {
        const person = await personsApi.create(data)
        tree.upsertPerson(personFields(person))
        return person
    }

    const updatePerson = async (id: number, data: any) => {
        const person = personFields(await personsApi.update(id, data))
        tree.upsertPerson(person)
        if (currentPerson.value?.id === id) currentPerson.value = { ...currentPerson.value, ...person }
        return person
    }

    const deletePerson = async (id: number) => {
        await personsApi.delete(id)
        tree.removePerson(id)
        if (currentPerson.value?.id === id) clearCurrent()
    }

    return {
        currentPerson, isLoading,
        loadPerson, refreshCurrent, clearCurrent,
        createItem, updateItem, deleteItem, createRelation, deleteRelation,
        createPerson, updatePerson, deletePerson,
    }
})
