import axios from 'axios';

export const apiClient = axios.create({
    baseURL: '/api',
    headers: { 'Content-Type': 'application/json' },
    timeout: 10000,
});

// »нтерцептор дл€ обработки ошибок и ретраев
apiClient.interceptors.response.use(
    (response) => response.data,
    async (error) => {
        const originalRequest = error.config;
        if (error.response?.status === 401) {
            // ѕеренаправление на страницу логина (реализовать позже)
            console.warn('401 Unauthorized Ц redirect to login');
        }
        if (error.code === 'ECONNABORTED' && !originalRequest._retry) {
            originalRequest._retry = true;
            try {
                return await apiClient(originalRequest);
            } catch (retryError) {
                console.error('Retry failed:', retryError);
            }
        }
        const message = error.response?.data?.detail || error.message || 'ќшибка запроса';
        console.error('API Error:', message);
        return Promise.reject(new Error(message));
    }
);