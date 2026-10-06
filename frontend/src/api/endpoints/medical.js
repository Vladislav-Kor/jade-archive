import { apiClient } from '../client'

export const medicalApi = {
    getForPerson: (personId) => 
        apiClient.get('/persons/' + personId + '/medical'),
    
    get: (id) => 
        apiClient.get('/medical/' + id),
    
    create: (personId, data) => 
        apiClient.post('/persons/' + personId + '/medical', data),
    
    update: (id, data) => 
        apiClient.put('/medical/' + id, data),
    
    delete: (id) => 
        apiClient.delete('/medical/' + id)
}
