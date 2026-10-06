import { ref, readonly } from 'vue';

export interface Toast {
    id: number;
    message: string;
    type: 'success' | 'error' | 'info';
}

const toasts = ref<Toast[]>([]);
let nextId = 0;

export function useToast() {
    const show = (message: string, type: Toast['type'] = 'info') => {
        const id = nextId++;
        toasts.value.push({ id, message, type });
        setTimeout(() => {
            toasts.value = toasts.value.filter(t => t.id !== id);
        }, 3000);
    };
    
    const success = (msg: string) => show(msg, 'success');
    const error = (msg: string) => show(msg, 'error');
    const info = (msg: string) => show(msg, 'info');
    
    return { toasts: readonly(toasts), show, success, error, info };
}
