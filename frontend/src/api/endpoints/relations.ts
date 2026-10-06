import { apiClient } from '../client';

export const relationsApi = {
    getAll: () => apiClient.get('/relations'),
    getForPerson: (personId: number) => apiClient.get(`/persons/${personId}/relations`),
    create: (data: { parent_id: number; child_id: number; relation_type: string }) => 
        apiClient.post('/relations', data),
    delete: (id: number) => apiClient.delete(`/relations/${id}`),
};
