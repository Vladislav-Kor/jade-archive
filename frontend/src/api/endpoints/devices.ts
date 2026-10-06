import { apiClient } from '../client'

export const devicesApi = {
  getForPerson: (personId: number) => apiClient.get(`/persons/${personId}/devices`),
  getById: (id: number) => apiClient.get(`/devices/${id}`),
  create: (data: any) => apiClient.post(`/persons/${data.person_id}/devices`, data),
  update: (id: number, data: any) => apiClient.put(`/devices/${id}`, data),
  delete: (id: number) => apiClient.delete(`/devices/${id}`),
}
