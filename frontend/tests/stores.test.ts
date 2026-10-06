import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'

// Сеть — граница: API-модули подменены, сторы — настоящие.
const api = vi.hoisted(() => {
    const resource = () => ({
        getForPerson: vi.fn(async () => []),
        getById: vi.fn(),
        create: vi.fn(),
        update: vi.fn(),
        delete: vi.fn(async () => ({})),
    })
    return {
        persons: { getAll: vi.fn(async () => []), getById: vi.fn(), create: vi.fn(), update: vi.fn(), delete: vi.fn() },
        relations: { getAll: vi.fn(async () => []), getForPerson: vi.fn(async () => []), create: vi.fn(), delete: vi.fn() },
        cases: resource(), medical: resource(), realEstate: resource(), vehicles: resource(), digital: resource(),
        social: resource(), partners: resource(), devices: resource(), cross: resource(),
    }
})
vi.mock('@/api/endpoints/persons', () => ({ personsApi: api.persons }))
vi.mock('@/api/endpoints/relations', () => ({ relationsApi: api.relations }))
vi.mock('@/api/endpoints/cases', () => ({ casesApi: api.cases }))
vi.mock('@/api/endpoints/medical', () => ({ medicalApi: api.medical }))
vi.mock('@/api/endpoints/real-estate', () => ({ realEstateApi: api.realEstate }))
vi.mock('@/api/endpoints/vehicles', () => ({ vehiclesApi: api.vehicles }))
vi.mock('@/api/endpoints/digital-accounts', () => ({ digitalAccountsApi: api.digital }))
vi.mock('@/api/endpoints/social', () => ({ socialApi: api.social }))
vi.mock('@/api/endpoints/partners', () => ({ partnersApi: api.partners }))
vi.mock('@/api/endpoints/devices', () => ({ devicesApi: api.devices }))
vi.mock('@/api/endpoints/cross-records', () => ({ crossRecordsApi: api.cross }))

import { usePersonStore } from '@/stores/usePersonStore'
import { useTreeStore } from '@/stores/useTreeStore'

const ivan = { id: 1, full_name: 'Иван', short_name: 'ivan', importance: 5 }
const petr = { id: 2, full_name: 'Пётр', short_name: 'petr', importance: 3 }

function deferred<T>() {
    let resolve!: (v: T) => void
    const promise = new Promise<T>((r) => { resolve = r })
    return { promise, resolve }
}

beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
    for (const r of Object.values(api)) {
        if ('getForPerson' in r) (r.getForPerson as any).mockResolvedValue([])
    }
    api.persons.getById.mockImplementation(async (id: number) => (id === 1 ? { ...ivan } : { ...petr }))
})

describe('usePersonStore.loadPerson', () => {
    it('loads the person with every collection the tabs show', async () => {
        api.realEstate.getForPerson.mockResolvedValue([{ id: 7, address: 'ул. 1' }])
        api.social.getForPerson.mockResolvedValue([{ id: 3, platform: 'tg' }])
        const store = usePersonStore()

        await store.loadPerson(1)

        expect(store.currentPerson?.full_name).toBe('Иван')
        expect(store.currentPerson?.real_estate).toEqual([{ id: 7, address: 'ул. 1' }])
        expect(store.currentPerson?.social_media).toEqual([{ id: 3, platform: 'tg' }])
        for (const key of ['relations', 'digital_accounts', 'vehicles', 'cases', 'medical_records',
            'partners', 'devices', 'cross_records']) {
            expect(store.currentPerson?.[key]).toEqual([])
        }
    })

    it('keeps the last selected person when an older response arrives late', async () => {
        const slowIvan = deferred<any>()
        api.persons.getById.mockImplementation((id: number) => (id === 1 ? slowIvan.promise : Promise.resolve({ ...petr })))
        const store = usePersonStore()

        const first = store.loadPerson(1)
        await store.loadPerson(2)
        slowIvan.resolve({ ...ivan })
        await first

        expect(store.currentPerson?.id).toBe(2)
    })

    it('shows the spinner only when switching people, not on a background refresh', async () => {
        const store = usePersonStore()
        await store.loadPerson(1)

        const refresh = store.refreshCurrent()
        expect(store.isLoading).toBe(false)
        await refresh

        const switching = store.loadPerson(2)
        expect(store.isLoading).toBe(true)
        await switching
        expect(store.isLoading).toBe(false)
    })
})

describe('usePersonStore collections', () => {
    beforeEach(async () => {
        api.cases.getForPerson.mockResolvedValue([{ id: 10, title: 'Старое' }])
        await usePersonStore().loadPerson(1)
        vi.clearAllMocks()
    })

    it('adds a created item from the server response without reloading', async () => {
        api.cases.create.mockResolvedValue({ id: 11, title: 'Новое' })
        const store = usePersonStore()

        await store.createItem('cases', { title: 'Новое' })

        expect(api.cases.create).toHaveBeenCalledWith(1, { title: 'Новое' })
        expect(store.currentPerson?.cases.map((c: any) => c.id)).toEqual([10, 11])
        expect(api.cases.getForPerson).not.toHaveBeenCalled()
        expect(api.persons.getById).not.toHaveBeenCalled()
    })

    it('replaces an updated item in place', async () => {
        api.cases.update.mockResolvedValue({ id: 10, title: 'Обновлено' })
        const store = usePersonStore()

        await store.updateItem('cases', 10, { title: 'Обновлено' })

        expect(store.currentPerson?.cases).toEqual([{ id: 10, title: 'Обновлено' }])
    })

    it('removes a deleted item immediately', async () => {
        const store = usePersonStore()
        const pending = deferred<any>()
        api.cases.delete.mockReturnValue(pending.promise)

        const removal = store.deleteItem('cases', 10)
        expect(store.currentPerson?.cases).toEqual([])
        pending.resolve({})
        await removal
    })

    it('puts the item back if the server refuses to delete it', async () => {
        api.cases.delete.mockRejectedValue(new Error('Нет связи с сервером'))
        const store = usePersonStore()

        await expect(store.deleteItem('cases', 10)).rejects.toThrow('Нет связи с сервером')

        expect(store.currentPerson?.cases).toEqual([{ id: 10, title: 'Старое' }])
    })

    it('reloads only the relations list after a relation change and updates the tree', async () => {
        api.relations.create.mockResolvedValue({ id: 5, parent_id: 1, child_id: 2, relation_type: 'friend' })
        api.relations.getForPerson.mockResolvedValue([{ id: 5, person_id: 2, person_name: 'Пётр', direction: 'outgoing' }])
        const store = usePersonStore()
        const tree = useTreeStore()

        await store.createItem('relations', { parent_id: 1, child_id: 2, relation_type: 'friend' })

        expect(store.currentPerson?.relations).toEqual([{ id: 5, person_id: 2, person_name: 'Пётр', direction: 'outgoing' }])
        expect(tree.relations.map((r: any) => r.id)).toEqual([5])
        expect(api.persons.getById).not.toHaveBeenCalled()
    })
})

describe('person create / update / delete keep the sidebar in sync', () => {
    it('updatePerson patches the profile and the sidebar row but keeps loaded tabs', async () => {
        api.cases.getForPerson.mockResolvedValue([{ id: 10 }])
        api.persons.update.mockResolvedValue({ ...ivan, full_name: 'Иван Иванов' })
        const store = usePersonStore()
        const tree = useTreeStore()
        tree.upsertPerson({ ...ivan })
        await store.loadPerson(1)

        await store.updatePerson(1, { full_name: 'Иван Иванов' })

        expect(store.currentPerson?.full_name).toBe('Иван Иванов')
        expect(store.currentPerson?.cases).toEqual([{ id: 10 }])
        expect(tree.persons.find((p: any) => p.id === 1)?.full_name).toBe('Иван Иванов')
    })

    it('createPerson adds the new person to the sidebar', async () => {
        api.persons.create.mockResolvedValue({ ...petr })
        const store = usePersonStore()
        const tree = useTreeStore()

        const created = await store.createPerson({ full_name: 'Пётр', short_name: 'petr' })

        expect(created.id).toBe(2)
        expect(tree.persons.map((p: any) => p.id)).toEqual([2])
    })

    it('deletePerson removes the person, their relations and clears the open profile', async () => {
        api.persons.delete.mockResolvedValue({})
        const store = usePersonStore()
        const tree = useTreeStore()
        tree.upsertPerson({ ...ivan })
        tree.upsertPerson({ ...petr })
        tree.upsertRelation({ id: 5, parent_id: 1, child_id: 2, relation_type: 'friend' })
        await store.loadPerson(1)

        await store.deletePerson(1)

        expect(tree.persons.map((p: any) => p.id)).toEqual([2])
        expect(tree.relations).toEqual([])
        expect(store.currentPerson).toBeNull()
    })
})

describe('useTreeStore', () => {
    it('search results react to a person added without reloading', () => {
        const tree = useTreeStore()
        tree.setSortMode('name')
        tree.setSearchQuery('пётр')
        expect(tree.filteredPersons).toEqual([])

        tree.upsertPerson({ ...petr })

        expect(tree.filteredPersons.map((p: any) => p.id)).toEqual([2])
    })

    it('upsertPerson replaces an existing row instead of duplicating it', () => {
        const tree = useTreeStore()
        tree.upsertPerson({ ...ivan })
        tree.upsertPerson({ ...ivan, importance: 9 })

        expect(tree.persons).toEqual([{ ...ivan, importance: 9 }])
    })
})
