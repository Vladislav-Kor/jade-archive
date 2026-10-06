import { ref, readonly } from 'vue'

export type ToastType = 'success' | 'error' | 'info' | 'warning'

export interface Toast {
    id: number
    message: string
    type: ToastType
}

const DURATION: Record<ToastType, number> = { success: 3000, info: 3000, warning: 4000, error: 6000 }

const toasts = ref<Toast[]>([])
let nextId = 0

export function useToast() {
    const dismiss = (id: number) => {
        toasts.value = toasts.value.filter((t) => t.id !== id)
    }

    const show = (message: string, type: ToastType = 'info', duration = DURATION[type]) => {
        const id = nextId++
        toasts.value.push({ id, message, type })
        setTimeout(() => dismiss(id), duration)
    }

    return {
        toasts: readonly(toasts),
        show,
        dismiss,
        success: (msg: string) => show(msg, 'success'),
        error: (msg: string) => show(msg, 'error'),
        info: (msg: string) => show(msg, 'info'),
        warning: (msg: string) => show(msg, 'warning'),
        clear: () => { toasts.value = [] },
    }
}
