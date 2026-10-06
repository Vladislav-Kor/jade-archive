import { ref, readonly } from 'vue';

const toasts = ref([]);
let nextId = 0;

export function useToast() {
    const show = (message, type = 'info', duration = 3000) => {
        const id = nextId++;
        toasts.value.push({ id, message, type });
        
        setTimeout(() => {
            toasts.value = toasts.value.filter(t => t.id !== id);
        }, duration);
    };
    
    const success = (msg, duration = 3000) => show(msg, 'success', duration);
    const error = (msg, duration = 5000) => show(msg, 'error', duration);
    const info = (msg, duration = 3000) => show(msg, 'info', duration);
    const warning = (msg, duration = 4000) => show(msg, 'warning', duration);
    
    const clear = () => { toasts.value = []; };
    
    return {
        toasts: readonly(toasts),
        show,
        success,
        error,
        info,
        warning,
        clear
    };
}