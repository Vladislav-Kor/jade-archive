import { apiClient } from '../client';

export const realEstateApi = {
    getForPerson: (personId) => {
        if (!personId) throw new Error('personId обязателен');
        return apiClient.get(`/persons/${personId}/real-estate`);
    },
    getById: (id) => {
        if (!id) throw new Error('id обязателен');
        return apiClient.get(`/real-estate/${id}`);
    },
    create: (personId, data) => {
        if (!personId) throw new Error('personId обязателен');
        if (!data) throw new Error('data обязателен');
        return apiClient.post(`/persons/${personId}/real-estate`, data);
    },
    update: (id, data) => {
        if (!id) throw new Error('id обязателен');
        if (!data) throw new Error('data обязателен');
        return apiClient.put(`/real-estate/${id}`, data);
    },
    delete: (id) => {
        if (!id) throw new Error('id обязателен');
        return apiClient.delete(`/real-estate/${id}`);
    },
};