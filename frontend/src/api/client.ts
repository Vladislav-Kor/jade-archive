import axios from 'axios'

export const apiClient = axios.create({
    baseURL: '/api',
    headers: { 'Content-Type': 'application/json' },
    timeout: 10000,
})

export class ApiError extends Error {
    status?: number

    constructor(message: string, status?: number) {
        super(message)
        this.status = status
    }
}

/** Понятный текст ошибки: detail FastAPI (строка или список ошибок валидации 422) или сеть. */
export function errorMessage(error: any): string {
    const detail = error.response?.data?.detail
    if (typeof detail === 'string') return detail
    if (Array.isArray(detail)) return detail.map((d) => d.msg).join('; ')
    if (error.code === 'ECONNABORTED') return 'Сервер не ответил вовремя'
    if (error.response) return `Ошибка сервера (${error.response.status})`
    return 'Нет связи с сервером'
}

apiClient.interceptors.response.use(
    (response) => response.data,
    async (error) => {
        const request = error.config
        // Повторяем только чтение: повтор POST/PUT после таймаута мог бы создать дубликат.
        if (error.code === 'ECONNABORTED' && request?.method === 'get' && !request._retried) {
            request._retried = true
            return apiClient(request)
        }
        return Promise.reject(new ApiError(errorMessage(error), error.response?.status))
    },
)
