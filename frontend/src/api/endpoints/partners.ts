import { apiClient } from '../client'

export const partnersApi = {
  getForPerson: (personId: number) => apiClient.get(`/persons/${personId}/partners`),
  getById: (id: number) => apiClient.get(`/partners/${id}`),
  create: (data: any) => apiClient.post(`/persons/${data.person_id}/partners`, data),
  update: (id: number, data: any) => apiClient.put(`/partners/${id}`, data),
  delete: (id: number) => apiClient.delete(`/partners/${id}`),
}
