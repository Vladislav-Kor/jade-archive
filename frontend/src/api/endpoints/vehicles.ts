import { apiClient } from '../client'

export const vehiclesApi = {
    getForPerson: (personId: number) => 
        apiClient.get(/persons/\/vehicles),
    
    get: (id: number) => 
        apiClient.get(/vehicles/\),
    
    create: (personId: number, data: any) => 
        apiClient.post(/persons/\/vehicles, data),
    
    update: (id: number, data: any) => 
        apiClient.put(/vehicles/\, data),
    
    delete: (id: number) => 
        apiClient.delete(/vehicles/\)
}
