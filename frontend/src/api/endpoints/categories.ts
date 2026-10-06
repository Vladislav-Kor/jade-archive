import { apiClient } from '../client'

export const categoriesApi = {
    getAll: () => 
        apiClient.get('/categories'),
    
    get: (id: number) => 
        apiClient.get(/categories/),
    
    create: (data: any) => 
        apiClient.post('/categories', data),
    
    update: (id: number, data: any) => 
        apiClient.put(/categories/, data),
    
    delete: (id: number) => 
        apiClient.delete(/categories/)
}
