import { apiClient } from '../client';

export const digitalAccountsApi = {
    getForPerson: (personId: number) => {
        if (!personId) throw new Error('personId обязателен');
        return apiClient.get(`/persons/${personId}/digital-accounts`);
    },
    getById: (id: number) => {
        if (!id) throw new Error('id обязателен');
        return apiClient.get(`/digital-accounts/${id}`);
    },
    create: (personId: number, data: any) => {
        if (!personId) throw new Error('personId обязателен');
        if (!data) throw new Error('data обязателен');
        return apiClient.post(`/persons/${personId}/digital-accounts`, data);
    },
    update: (id: number, data: any) => {
        if (!id) throw new Error('id обязателен');
        if (!data) throw new Error('data обязателен');
        return apiClient.put(`/digital-accounts/${id}`, data);
    },
    delete: (id: number) => {
        if (!id) throw new Error('id обязателен');
        return apiClient.delete(`/digital-accounts/${id}`);
    },
};