import { apiClient } from '../client'

export const categoriesApi = {
    getAll: () => apiClient.get('/categories'),
    getById: (id: number) => apiClient.get(`/categories/${id}`),
    create: (data: object) => apiClient.post('/categories', data),
    update: (id: number, data: object) => apiClient.put(`/categories/${id}`, data),
    delete: (id: number) => apiClient.delete(`/categories/${id}`),
}
