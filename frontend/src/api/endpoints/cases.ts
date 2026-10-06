import { apiClient } from '../client'

export const casesApi = {
    getForPerson: (personId) => 
        apiClient.get('/persons/' + personId + '/cases'),
    
    get: (id) => 
        apiClient.get('/cases/' + id),
    
    create: (personId, data) => 
        apiClient.post('/persons/' + personId + '/cases', data),
    
    update: (id, data) => 
        apiClient.put('/cases/' + id, data),
    
    delete: (id) => 
        apiClient.delete('/cases/' + id)
}
