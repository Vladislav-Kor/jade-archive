import { apiClient } from '../client'

export const socialApi = {
    getForPerson: (personId) => 
        apiClient.get('/persons/' + personId + '/social'),
    
    create: (personId, data) => 
        apiClient.post('/persons/' + personId + '/social', data),
    
    delete: (id) => 
        apiClient.delete('/social/' + id)
}
