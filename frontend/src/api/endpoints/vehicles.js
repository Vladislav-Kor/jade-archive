import { apiClient } from '../client';

export const vehiclesApi = {
    getForPerson: (personId) => {
        if (!personId) throw new Error('personId обязателен');
        return apiClient.get(`/persons/${personId}/vehicles`);
    },
    getById: (id) => {
        if (!id) throw new Error('id обязателен');
        return apiClient.get(`/vehicles/${id}`);
    },
    create: (personId, data) => {
        if (!personId) throw new Error('personId обязателен');
        if (!data) throw new Error('data обязателен');
        return apiClient.post(`/persons/${personId}/vehicles`, data);
    },
    update: (id, data) => {
        if (!id) throw new Error('id обязателен');
        if (!data) throw new Error('data обязателен');
        return apiClient.put(`/vehicles/${id}`, data);
    },
    delete: (id) => {
        if (!id) throw new Error('id обязателен');
        return apiClient.delete(`/vehicles/${id}`);
    },
};