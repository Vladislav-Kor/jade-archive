import { apiClient } from '../client'

export const realEstateApi = {
    getForPerson: (personId: number) => 
        apiClient.get(/persons/\/real-estate),
    
    get: (id: number) => 
        apiClient.get(/real-estate/\),
    
    create: (personId: number, data: any) => 
        apiClient.post(/persons/\/real-estate, data),
    
    update: (id: number, data: any) => 
        apiClient.put(/real-estate/\, data),
    
    delete: (id: number) => 
        apiClient.delete(/real-estate/\)
}
