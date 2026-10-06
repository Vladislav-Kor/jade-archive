import { apiClient } from '../client'

export const personsApi = {
    getAll: () => {
        return apiClient.get('/persons')
    },

    getById: (id) => {
        return apiClient.get('/persons/' + id)
    },

    create: (data) => {
        return apiClient.post('/persons', data)
    },

    update: (id, data) => {
        return apiClient.put('/persons/' + id, data)
    },

    delete: (id) => {
        return apiClient.delete('/persons/' + id)
    },

    search: (query) => {
        return apiClient.get('/search?q=' + query)
    }
}
