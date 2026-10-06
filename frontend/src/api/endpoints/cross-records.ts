import { apiClient } from '../client'
import { personResource } from '../resource'

// Создание — POST /cross-records с person_id в теле, остальное как у других ресурсов.
export const crossRecordsApi = {
    ...personResource('cross-records'),
    create: (personId: number, data: object) => apiClient.post('/cross-records', { ...data, person_id: personId }),
}
