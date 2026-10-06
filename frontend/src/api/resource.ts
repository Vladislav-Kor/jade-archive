import { apiClient } from './client'

/**
 * Ресурс, который принадлежит человеку: /persons/{id}/<name> и /<name>/{itemId}.
 * Все модули отдают одинаковые методы — стор работает с ними одинаково.
 */
export interface PersonResource<T = any> {
    getForPerson: (personId: number) => Promise<T[]>
    getById: (id: number) => Promise<T>
    create: (personId: number, data: Partial<T>) => Promise<T>
    update: (id: number, data: Partial<T>) => Promise<T>
    delete: (id: number) => Promise<unknown>
}

export function personResource<T = any>(
    name: string,
    { personIdInBody = false }: { personIdInBody?: boolean } = {},
): PersonResource<T> {
    return {
        getForPerson: (personId) => apiClient.get(`/persons/${personId}/${name}`),
        getById: (id) => apiClient.get(`/${name}/${id}`),
        create: (personId, data) =>
            apiClient.post(`/persons/${personId}/${name}`, personIdInBody ? { ...data, person_id: personId } : data),
        update: (id, data) => apiClient.put(`/${name}/${id}`, data),
        delete: (id) => apiClient.delete(`/${name}/${id}`),
    }
}
