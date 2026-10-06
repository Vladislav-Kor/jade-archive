<template>
  <BaseModal ref="modalRef" :title="isEdit ? '✏️ Редактирование записи' : '🏥 Новая медицинская запись'" size="md">
    <template #body>
      <form @submit.prevent="handleSubmit" id="medicalForm" class="medical-form">
        
        <div class="form-section">
          <h4>📋 Информация о записи</h4>
          <div class="form-group">
            <label>Тип записи *</label>
            <select v-model="form.record_type" required class="form-input">
              <option value="">Выберите тип</option>
              <option value="diagnosis">🩺 Диагноз</option>
              <option value="examination">🔬 Осмотр</option>
              <option value="vaccination">💉 Вакцинация</option>
              <option value="analysis">🧪 Анализ</option>
              <option value="operation">🏥 Операция</option>
              <option value="hospitalization">🏨 Госпитализация</option>
              <option value="prescription">💊 Рецепт/Назначение</option>
              <option value="allergy">🤧 Аллергия</option>
              <option value="chronic">📋 Хроническое заболевание</option>
              <option value="checkup">📅 Профилактический осмотр</option>
            </select>
          </div>
          <div class="form-group">
            <label>Название *</label>
            <input type="text" v-model="form.title" required class="form-input" placeholder="Название записи">
          </div>
          <div class="form-group">
            <label>Описание</label>
            <textarea v-model="form.description" rows="4" class="form-input" placeholder="Подробное описание, симптомы, заключение..."></textarea>
          </div>
        </div>

        <div class="form-section">
          <h4>👨‍⚕️ Врач и дата</h4>
          <div class="form-row">
            <div class="form-group">
              <label>Дата записи</label>
              <input type="date" v-model="form.record_date" class="form-input">
            </div>
            <div class="form-group">
              <label>Врач</label>
              <input type="text" v-model="form.doctor_name" class="form-input" placeholder="ФИО врача">
            </div>
          </div>
        </div>

        <div class="form-section">
          <h4>📎 Вложения</h4>
          <div class="form-group">
            <label>Ссылки на файлы</label>
            <textarea v-model="form.attachments" rows="2" class="form-input" placeholder="Ссылки на снимки, анализы, документы (каждая с новой строки)"></textarea>
          </div>
          <div class="form-hint">
            <small>📎 Можно указать ссылки на Google Drive, Dropbox или другие облачные хранилища</small>
          </div>
        </div>

      </form>
    </template>
    <template #footer>
      <button class="btn-secondary" @click="close">Отмена</button>
      <button type="submit" form="medicalForm" class="btn-primary" :disabled="loading">
        {{ loading ? 'Сохранение...' : 'Сохранить' }}
      </button>
    </template>
  </BaseModal>
</template>

<script setup>
import { ref, reactive } from 'vue';
import BaseModal from '../common/BaseModal.vue';
import { medicalApi } from '@/api/endpoints/medical';
import { usePersonStore } from '@/stores/usePersonStore';
import { toPayload, fillForm } from '@/utils/payload';
import { useToast } from '@/composables/useToast';

const modalRef = ref(null);
const personStore = usePersonStore();
const { success, error: toastError } = useToast();

const isEdit = ref(false);
const currentId = ref(null);
const loading = ref(false);

const form = reactive({
  record_type: '',
  title: '',
  description: '',
  record_date: '',
  doctor_name: '',
  attachments: ''
});


const resetForm = () => {
  Object.keys(form).forEach(key => form[key] = '');
  isEdit.value = false;
  currentId.value = null;
};

const open = async (id = null) => {
  console.log('📂 Открытие MedicalModal, id:', id);
  resetForm();
  
  if (id) {
    isEdit.value = true;
    currentId.value = id;
    try {
      const item = await medicalApi.getById(id);
      if (item) {
        fillForm(form, item);
        if (form.record_date) {
          form.record_date = form.record_date.split('T')[0];
        }
        console.log('✅ Данные загружены:', item);
      } else {
        console.error('❌ Данные не найдены для ID:', id);
        toastError('Данные не найдены');
        return;
      }
    } catch (err) {
      console.error('❌ Ошибка загрузки данных:', err);
      toastError('Ошибка загрузки данных');
      return;
    }
  }
  
  modalRef.value?.open();
};

const close = () => {
  modalRef.value?.close();
};

const handleSubmit = async () => {
  if (!form.record_type || !form.title) {
    toastError('Заполните тип и название записи');
    return;
  }
  
  loading.value = true;
  try {
    const data = toPayload({ ...form }, isEdit.value);
    if (isEdit.value && currentId.value) {
      await personStore.updateItem('medical_records', currentId.value, data);
      success('Запись обновлена');
    } else {
      await personStore.createItem('medical_records', data);
      success('Запись добавлена');
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
.medical-form { max-height: 70vh; overflow-y: auto; padding-right: 8px; }
.form-section { margin-bottom: 28px; padding-bottom: 20px; border-bottom: 1px solid rgba(0, 212, 168, 0.1); }
.form-section h4 { font-size: 14px; font-weight: 700; color: #ffd54f; margin: 0 0 16px 0; display: flex; align-items: center; gap: 8px; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; }
.form-group { margin-bottom: 16px; }
.form-group label { display: block; font-size: 11px; font-weight: 600; margin-bottom: 6px; color: #a8d5ce; text-transform: uppercase; letter-spacing: 0.5px; }
.form-input { width: 100%; padding: 10px 12px; background: rgba(0, 25, 22, 0.7); border: 1px solid rgba(0, 212, 168, 0.2); border-radius: 10px; color: #e8f0ef; font-size: 13px; transition: all 0.2s; }
.form-input:focus { outline: none; border-color: #ffd54f; box-shadow: 0 0 0 3px rgba(255, 213, 79, 0.1); background: rgba(0, 25, 22, 0.9); }
textarea.form-input { resize: vertical; font-family: inherit; }
.form-hint { margin-top: 8px; font-size: 11px; color: #6eafa2; }
@media (max-width: 768px) { .form-row { grid-template-columns: 1fr; gap: 0; } }
</style>