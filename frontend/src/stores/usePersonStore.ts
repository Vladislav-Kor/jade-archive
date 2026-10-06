import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
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
import type { Person } from '@/types/person'
import { useToast } from '@/composables/useToast'

export const usePersonStore = defineStore('person', () => {
    const currentPerson = ref<Person | null>(null)
    const isLoading = ref(false)
    const { error: toastError } = useToast()

    // Загружаем только базовую информацию
    const loadPerson = async (id: number) => {
        isLoading.value = true
        try {
            const person = await personsApi.getById(id)
            currentPerson.value = { ...person } // базовая информация
            console.log('? Загружен person:', person.full_name)
        } catch (err) {
            console.error('? Ошибка загрузки:', err)
            toastError('Ошибка загрузки контакта')
        } finally {
            isLoading.value = false
        }
    }

    // Ленивая загрузка для каждого таба
    const loadRelations = async () => {
        if (!currentPerson.value) return
        try {
            const relations = await relationsApi.getForPerson(currentPerson.value.id)
            currentPerson.value.relations = relations
        } catch { /* ignore */ }
    }
    const loadDigitalAccounts = async () => {
        if (!currentPerson.value) return
        try {
            const accounts = await digitalAccountsApi.getForPerson(currentPerson.value.id)
            currentPerson.value.digital_accounts = accounts
        } catch { /* ignore */ }
    }
    // ... аналогично для остальных

    const clearCurrent = () => { currentPerson.value = null }

    return { currentPerson, isLoading, loadPerson, loadRelations, loadDigitalAccounts, clearCurrent }
})