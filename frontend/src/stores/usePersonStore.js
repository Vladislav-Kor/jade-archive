import { defineStore } from 'pinia'
import { ref } from 'vue'
import { personsApi } from '@/api/endpoints/persons'
import { relationsApi } from '@/api/endpoints/relations'
import { digitalAccountsApi } from '@/api/endpoints/digital-accounts'
import { partnersApi } from '@/api/endpoints/partners'
import { devicesApi } from '@/api/endpoints/devices'
import { crossRecordsApi } from '@/api/endpoints/cross-records'
import { useToast } from '@/composables/useToast'

export const usePersonStore = defineStore('person', () => {
    const currentPerson = ref(null)
    const isLoading = ref(false)
    const { error: toastError } = useToast()

    const loadPerson = async (id) => {
        isLoading.value = true
        try {
            const [person, relations, digitalAccounts, partners, devices, crossRecords] = await Promise.all([
                personsApi.getById(id),
                relationsApi.getForPerson(id).catch(() => []),
                digitalAccountsApi.getForPerson(id).catch(() => []),
                partnersApi.getForPerson(id).catch(() => []),
                devicesApi.getForPerson(id).catch(() => []),
                crossRecordsApi.getForPerson(id).catch(() => [])
            ])
            
            currentPerson.value = { 
                ...person, 
                relations, 
                digital_accounts: digitalAccounts,
                partners: partners,
                devices: devices,
                cross_records: crossRecords
            }
            
            console.log('✅ Загружен person:', currentPerson.value)
            
        } catch (err) {
            console.error('❌ Ошибка загрузки:', err)
            toastError('Ошибка загрузки контакта')
        } finally {
            isLoading.value = false
        }
    }

    const clearCurrent = () => { 
        currentPerson.value = null 
    }

    return { currentPerson, isLoading, loadPerson, clearCurrent }
})