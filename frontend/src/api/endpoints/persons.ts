import { apiClient } from '../client'

export const personsApi = {
    getAll: () => apiClient.get('/persons'),
    getById: (id: number) => apiClient.get(`/persons/${id}`),
    create: (data: object) => apiClient.post('/persons', data),
    update: (id: number, data: object) => apiClient.put(`/persons/${id}`, data),
    delete: (id: number) => apiClient.delete(`/persons/${id}`),
    search: (query: string) => apiClient.get('/search', { params: { q: query } }),
}
