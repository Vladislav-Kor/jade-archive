<template>
  <BaseModal ref="modalRef" :title="isEdit ? '✏️ Редактирование соцсети' : '🌐 Новая социальная сеть'" size="sm">
    <template #body>
      <form @submit.prevent="handleSubmit" id="socialForm">
        <div class="form-group">
          <label>Платформа *</label>
          <input 
            type="text" 
            v-model="form.platform" 
            required 
            placeholder="Telegram, VK, Instagram..." 
            class="form-input"
            list="platforms"
          />
          <datalist id="platforms">
            <option value="Telegram"></option>
            <option value="VK"></option>
            <option value="Instagram"></option>
            <option value="YouTube"></option>
            <option value="Twitter"></option>
            <option value="TikTok"></option>
            <option value="Steam"></option>
            <option value="Discord"></option>
            <option value="GitHub"></option>
            <option value="Twitch"></option>
            <option value="WhatsApp"></option>
            <option value="Facebook"></option>
            <option value="LinkedIn"></option>
            <option value="Pinterest"></option>
            <option value="Reddit"></option>
            <option value="Snapchat"></option>
          </datalist>
        </div>
        <div class="form-group">
          <label>Ссылка *</label>
          <input 
            type="url" 
            v-model="form.link" 
            required 
            placeholder="https://t.me/username" 
            class="form-input"
          />
        </div>
      </form>
    </template>
    <template #footer>
      <button class="btn-secondary" @click="close">Отмена</button>
      <button type="submit" form="socialForm" class="btn-primary" :disabled="loading">
        {{ loading ? 'Сохранение...' : 'Сохранить' }}
      </button>
    </template>
  </BaseModal>
</template>

<script setup>
import { ref, reactive } from 'vue';
import BaseModal from '../common/BaseModal.vue';
import { usePersonStore } from '@/stores/usePersonStore';
import { useToast } from '@/composables/useToast';

const modalRef = ref(null);
const personStore = usePersonStore();
const { success, error: toastError } = useToast();

const isEdit = ref(false);
const currentId = ref(null);
const loading = ref(false);

const form = reactive({
  platform: '',
  link: ''
});

const resetForm = () => {
  form.platform = '';
  form.link = '';
  isEdit.value = false;
  currentId.value = null;
};

const open = async (id = null) => {
  console.log('📂 Открытие SocialModal, id:', id);
  resetForm();
  
  if (id) {
    isEdit.value = true;
    currentId.value = id;
    // Для социальных сетей данные хранятся в person.social_media
    // Поэтому мы не можем получить их напрямую по ID
    // Вместо этого ищем в текущем контакте
    const person = personStore.currentPerson;
    if (person && person.social_media) {
      const item = person.social_media.find(s => s.id === id);
      if (item) {
        form.platform = item.platform;
        form.link = item.link;
        console.log('✅ Данные загружены:', item);
      } else {
        console.error('❌ Данные не найдены для ID:', id);
        toastError('Данные не найдены');
        return;
      }
    } else {
      toastError('Нет данных о контакте');
      return;
    }
  }
  
  modalRef.value?.open();
};

const close = () => {
  modalRef.value?.close();
};

const handleSubmit = async () => {
  if (!form.platform || !form.link) {
    toastError('Заполните все поля');
    return;
  }
  
  loading.value = true;
  try {
    const data = { platform: form.platform.trim(), link: form.link.trim() };

    if (isEdit.value && currentId.value) {
      // Одно обновление (PUT) вместо «удалить и создать»: при сбое ссылка не теряется.
      await personStore.updateItem('social_media', currentId.value, data);
      success('Соцсеть обновлена');
    } else {
      await personStore.createItem('social_media', data);
      success('Соцсеть добавлена');
    }
    close();
  } catch (err) {
    toastError(err.message || 'Ошибка сохранения');
  } finally {
    loading.value = false;
  }
};

defineExpose({ open, close });
</script>

<style scoped>
.form-group { margin-bottom: 20px; }
.form-group label { 
  display: block; 
  font-size: 11px; 
  font-weight: 600; 
  margin-bottom: 6px; 
  color: #a8d5ce; 
  text-transform: uppercase; 
  letter-spacing: 0.5px; 
}
.form-input { 
  width: 100%; 
  padding: 10px 12px; 
  background: rgba(0, 25, 22, 0.7); 
  border: 1px solid rgba(0, 212, 168, 0.2); 
  border-radius: 10px; 
  color: #e8f0ef; 
  font-size: 13px; 
  transition: all 0.2s; 
}
.form-input:focus { 
  outline: none; 
  border-color: #ffd54f; 
  background: rgba(0, 25, 22, 0.9); 
}
</style>