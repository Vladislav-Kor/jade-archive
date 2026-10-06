<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="isOpen" class="modal-overlay" @click.self="close">
        <div class="modal-container" :class="sizeClass">
          <div class="modal-header">
            <h3>
              <Icon v-if="icon" :name="icon" size="md" color="#ffd54f" />
              {{ title }}
            </h3>
            <button class="modal-close" @click="close">
              <Icon name="close" size="sm" />
            </button>
          </div>
          
          <div class="modal-body">
            <slot name="body"></slot>
          </div>
          
          <div class="modal-footer">
            <slot name="footer">
              <button class="btn-secondary" @click="close">Отмена</button>
              <button class="btn-primary" @click="handleSubmit" :disabled="loading">
                <Icon v-if="loading" name="refresh" size="sm" spin />
                {{ loading ? 'Сохранение...' : 'Сохранить' }}
              </button>
            </slot>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, computed } from 'vue';
import Icon from './Icon.vue';

const props = defineProps({
  title: { type: String, default: 'Модальное окно' },
  icon: { type: String, default: '' },
  size: { type: String, default: 'md', validator: (v) => ['sm', 'md', 'lg'].includes(v) },
  // Сохранение идёт в окне-владельце: пока true, кнопка заблокирована (нет двойных записей).
  loading: { type: Boolean, default: false }
});

const emit = defineEmits(['submit', 'close']);

const isOpen = ref(false);

const sizeClass = computed(() => {
  const sizes = { sm: 'modal-sm', md: 'modal-md', lg: 'modal-lg' };
  return sizes[props.size] || 'modal-md';
});

const open = () => {
  isOpen.value = true;
  document.body.style.overflow = 'hidden';
};

const close = () => {
  isOpen.value = false;
  document.body.style.overflow = '';
  emit('close');
};

const handleSubmit = () => {
  if (!props.loading) emit('submit');
};

defineExpose({ open, close });
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
  max-height: 88vh; 
  overflow: hidden; 
  border: 1px solid rgba(0, 212, 168, 0.2); 
  box-shadow: 0 32px 64px rgba(0, 0, 0, 0.4); 
}
.modal-container.modal-sm { max-width: 500px; }
.modal-container.modal-md { max-width: 600px; }
.modal-container.modal-lg { max-width: 800px; }
.modal-header { 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  padding: 20px 24px; 
  border-bottom: 1px solid rgba(0, 212, 168, 0.12); 
  background: linear-gradient(135deg, rgba(0, 212, 168, 0.05), transparent); 
}
.modal-header h3 { 
  font-size: 18px; 
  font-weight: 700; 
  background: linear-gradient(135deg, #fff, #ffd54f); 
  -webkit-background-clip: text; 
  background-clip: text; 
  color: transparent; 
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
  transition: all 0.2s; 
  display: inline-flex; 
  align-items: center; 
  justify-content: center; 
}
.modal-close:hover { 
  background: rgba(255, 90, 90, 0.15); 
  border-color: #ff5a5a; 
  color: #ff8a7a; 
  transform: rotate(90deg); 
}
.modal-body { 
  padding: 24px; 
  overflow-y: auto; 
  max-height: calc(88vh - 140px); 
}
.modal-footer { 
  display: flex; 
  justify-content: flex-end; 
  gap: 12px; 
  padding: 16px 24px; 
  border-top: 1px solid rgba(0, 212, 168, 0.1); 
  background: rgba(0, 0, 0, 0.2); 
}
.btn-secondary { 
  padding: 8px 16px; 
  background: rgba(0, 212, 168, 0.08); 
  border: 1px solid rgba(0, 212, 168, 0.25); 
  border-radius: 10px; 
  color: #d4ede8; 
  cursor: pointer; 
}

</style>
