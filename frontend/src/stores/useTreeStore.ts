import { defineStore } from 'pinia'
import { ref } from 'vue'
import { personsApi } from '@/api/endpoints/persons'
import { relationsApi } from '@/api/endpoints/relations'

export const useTreeStore = defineStore('tree', () => {
    const persons = ref([])
    const selectedPersonId = ref(null)
    const isLoading = ref(false)
    const searchQuery = ref('')

    const loadPersons = async () => {
        isLoading.value = true
        try {
            const data = await personsApi.getAll()
            persons.value = data
            console.log('✅ Загружены люди:', persons.value.length)
        } catch (error) {
            console.error('❌ Ошибка загрузки людей:', error)
        } finally {
            isLoading.value = false
        }
    }

    const refresh = async () => {
        await loadPersons()
    }

    const selectPerson = (id) => {
        selectedPersonId.value = id
        console.log('✅ Выбран человек:', id)
    }

    const setSearchQuery = (query) => {
        searchQuery.value = query
    }

    return {
        persons,
        selectedPersonId,
        isLoading,
        searchQuery,
        loadPersons,
        refresh,
        selectPerson,
        setSearchQuery
    }
})
