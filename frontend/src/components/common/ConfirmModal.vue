<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="isOpen" class="modal-overlay" @click.self="close">
        <div class="modal-container modal-sm">
          <div class="modal-header">
            <h3>
              <Icon name="alert" size="md" color="#ff6b6b" />
              Подтверждение
            </h3>
            <button class="modal-close" @click="close">
              <Icon name="close" size="sm" />
            </button>
          </div>
          <div class="modal-body text-center">
            <p class="confirm-message">{{ message }}</p>
          </div>
          <div class="modal-footer justify-center">
            <button class="btn-secondary" @click="close">Отмена</button>
            <button class="btn-danger" @click="confirm">
              <Icon name="trash" size="sm" /> Удалить
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref } from 'vue';
import Icon from './Icon.vue';

const isOpen = ref(false);
let resolvePromise = null;
const message = ref('Вы уверены?');

const confirm = () => {
  if (resolvePromise) resolvePromise(true);
  close();
};

const close = () => {
  isOpen.value = false;
  document.body.style.overflow = '';
  if (resolvePromise) resolvePromise(false);
  resolvePromise = null;
};

const open = (msg) => {
  message.value = msg || 'Вы уверены?';
  isOpen.value = true;
  document.body.style.overflow = 'hidden';
  return new Promise((resolve) => {
    resolvePromise = resolve;
  });
};

defineExpose({ open });
</script>

<style scoped>
.modal-enter-active, .modal-leave-active { transition: opacity 0.3s ease; }
.modal-enter-active .modal-container, .modal-leave-active .modal-container { transition: transform 0.3s cubic-bezier(0.2, 0.9, 0.4, 1.1); }
.modal-enter-from, .modal-leave-to { opacity: 0; }
.modal-enter-from .modal-container, .modal-leave-to .modal-container { transform: translateY(40px) scale(0.96); }
.modal-overlay { 
  position: fixed; 
  top: 0; 
  left: 0; 
  width: 100%; 
  height: 100%; 
  background: rgba(0, 0, 0, 0.88); 
  backdrop-filter: blur(12px); 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  z-index: 1000; 
}
.modal-container { 
  background: linear-gradient(135deg, rgba(13, 35, 30, 0.98), rgba(7, 22, 19, 0.98)); 
  backdrop-filter: blur(20px); 
  border-radius: 28px; 
  width: 90%; 
  max-width: 450px; 
  overflow: hidden; 
  border: 1px solid rgba(0, 212, 168, 0.2); 
}
.modal-header { 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  padding: 20px 24px; 
  border-bottom: 1px solid rgba(0, 212, 168, 0.12); 
}
.modal-header h3 { 
  font-size: 18px; 
  font-weight: 700; 
  margin: 0; 
  display: flex; 
  align-items: center; 
  gap: 8px; 
}
.modal-close { 
  width: 32px; 
  height: 32px; 
  background: rgba(255, 255, 255, 0.04); 
  border: 1px solid rgba(255, 255, 255, 0.08); 
  border-radius: 10px; 
  color: #8ecfc4; 
  cursor: pointer; 
  display: inline-flex; 
  align-items: center; 
  justify-content: center; 
}
.modal-close:hover { 
  background: rgba(255, 90, 90, 0.15); 
  border-color: #ff5a5a; 
  color: #ff8a7a; 
}
.modal-body { padding: 24px; }
.modal-footer { 
  display: flex; 
  justify-content: center; 
  gap: 12px; 
  padding: 16px 24px; 
  border-top: 1px solid rgba(0, 212, 168, 0.1); 
}
.text-center { text-align: center; }
.confirm-message { margin: 0; font-size: 14px; color: #e8f0ef; }
.btn-secondary { 
  padding: 8px 20px; 
  background: rgba(0, 212, 168, 0.08); 
  border: 1px solid rgba(0, 212, 168, 0.25); 
  border-radius: 10px; 
  color: #d4ede8; 
  cursor: pointer; 
}
.btn-danger { 
  padding: 8px 20px; 
  background: rgba(255, 90, 90, 0.15); 
  border: 1px solid rgba(255, 90, 90, 0.3); 
  border-radius: 10px; 
  color: #ff8a7a; 
  cursor: pointer; 
  display: inline-flex; 
  align-items: center; 
  gap: 6px; 
}
.btn-danger:hover { background: rgba(255, 90, 90, 0.25); }
</style>
