<template>
    <div class="toast-host">
        <!-- Ошибки озвучиваются сразу (alert), остальное — вежливо (status) -->
        <TransitionGroup name="toast">
            <div
                v-for="t in toasts"
                :key="t.id"
                class="toast"
                :class="t.type"
                :role="t.type === 'error' ? 'alert' : 'status'"
            >
                <span class="toast-icon" aria-hidden="true">{{ ICONS[t.type] }}</span>
                <span class="toast-text">{{ t.message }}</span>
                <button class="toast-close" type="button" aria-label="Закрыть уведомление" @click="dismiss(t.id)">×</button>
            </div>
        </TransitionGroup>
    </div>
</template>

<script setup>
import { useToast } from '@/composables/useToast'

const ICONS = { success: '✓', error: '!', warning: '⚠', info: 'i' }
const { toasts, dismiss } = useToast()
</script>

<style scoped>
.toast-host {
    position: fixed;
    right: 20px;
    bottom: 20px;
    z-index: 2000;
    display: flex;
    flex-direction: column;
    gap: 8px;
    max-width: min(380px, calc(100vw - 40px));
}
.toast {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 12px;
    background: #0d1210;
    border: 1px solid #2a3a35;
    border-left-width: 3px;
    border-radius: 10px;
    color: #e6efec;
    font-size: 13px;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35);
}
.toast.success { border-left-color: #00c49a; }
.toast.error { border-left-color: #e55c5c; }
.toast.warning { border-left-color: #e5a03c; }
.toast.info { border-left-color: #5a8dee; }
.toast-icon {
    width: 20px;
    height: 20px;
    flex-shrink: 0;
    border-radius: 10px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 12px;
    background: #1a2420;
}
.toast-text { flex: 1; line-height: 1.4; }
.toast-close {
    background: none;
    border: none;
    color: #8aa29b;
    font-size: 18px;
    line-height: 1;
    cursor: pointer;
    padding: 2px 4px;
    border-radius: 6px;
}
.toast-close:hover, .toast-close:focus-visible { color: #fff; background: #1a2420; }
.toast-enter-active, .toast-leave-active { transition: all 0.2s ease; }
.toast-enter-from, .toast-leave-to { opacity: 0; transform: translateY(8px); }
@media (prefers-reduced-motion: reduce) {
    .toast-enter-active, .toast-leave-active { transition: none; }
}
</style>
