import { apiClient } from '../client';

export const crossRecordsApi = {
    // Получить все записи для человека
    getForPerson: (personId) => apiClient.get(`/persons/${personId}/cross-records`),
    
    // Получить запись по ID
    getById: (id) => apiClient.get(`/cross-records/${id}`),
    
    // Создать запись
    create: (data) => apiClient.post('/cross-records', data),
    
    // Обновить запись
    update: (id, data) => apiClient.put(`/cross-records/${id}`, data),
    
    // Удалить запись
    delete: (id) => apiClient.delete(`/cross-records/${id}`)
};
