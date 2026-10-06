<template>
  <BaseModal ref="modalRef" :title="isEdit ? '✏️ Редактирование дела' : '📋 Новое дело'" size="md">
    <template #body>
      <form @submit.prevent="handleSubmit" id="caseForm" class="case-form">
        
        <div class="form-section">
          <h4>📋 Основная информация</h4>
          <div class="form-group">
            <label>Тип дела *</label>
            <select v-model="form.case_type" required class="form-input">
              <option value="">Выберите тип</option>
              <option value="legal">⚖️ Судебное дело</option>
              <option value="work">💼 Рабочее дело</option>
              <option value="personal">👤 Личное дело</option>
              <option value="family">👨‍👩‍👧 Семейное дело</option>
              <option value="financial">💰 Финансовое дело</option>
              <option value="medical">🏥 Медицинское дело</option>
              <option value="education">📚 Образовательное дело</option>
              <option value="real_estate">🏠 Недвижимость</option>
              <option value="other">📌 Другое</option>
            </select>
          </div>
          <div class="form-group">
            <label>Название *</label>
            <input type="text" v-model="form.title" required class="form-input" placeholder="Краткое название дела">
          </div>
          <div class="form-group">
            <label>Описание</label>
            <textarea v-model="form.description" rows="4" class="form-input" placeholder="Подробное описание дела, обстоятельства, участники..."></textarea>
          </div>
        </div>

        <div class="form-section">
          <h4>⚙️ Параметры</h4>
          <div class="form-row">
            <div class="form-group">
              <label>Приоритет</label>
              <select v-model="form.priority" class="form-input">
                <option value="low">🟢 Низкий</option>
                <option value="medium">🟡 Средний</option>
                <option value="high">🟠 Высокий</option>
                <option value="critical">🔴 Критический</option>
              </select>
            </div>
            <div class="form-group">
              <label>Статус</label>
              <select v-model="form.status" class="form-input">
                <option value="active">🟢 Активно</option>
                <option value="pending">🟡 Ожидает</option>
                <option value="completed">✅ Завершено</option>
                <option value="cancelled">❌ Отменено</option>
                <option value="deferred">⏸️ Отложено</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label>Срок выполнения</label>
            <input type="datetime-local" v-model="form.due_date" class="form-input">
          </div>
        </div>

      </form>
    </template>
    <template #footer>
      <button class="btn-secondary" @click="close">Отмена</button>
      <button type="submit" form="caseForm" class="btn-primary" :disabled="loading">
        {{ loading ? 'Сохранение...' : 'Сохранить' }}
      </button>
    </template>
  </BaseModal>
</template>

<script setup>
import { ref, reactive } from 'vue';
import BaseModal from '../common/BaseModal.vue';
import { casesApi } from '@/api/endpoints/cases';
import { usePersonStore } from '@/stores/usePersonStore';
import { useToast } from '@/composables/useToast';

const modalRef = ref(null);
const personStore = usePersonStore();
const { success, error: toastError } = useToast();

const isEdit = ref(false);
const currentId = ref(null);
const loading = ref(false);

const form = reactive({
  case_type: '',
  title: '',
  description: '',
  priority: 'medium',
  status: 'active',
  due_date: ''
});

function cleanData(data) {
  const cleaned = {};
  for (const [key, value] of Object.entries(data)) {
    if (value === '' || value === null || value === undefined) {
      continue;
    }
    cleaned[key] = value;
  }
  return cleaned;
}

const resetForm = () => {
  form.case_type = '';
  form.title = '';
  form.description = '';
  form.priority = 'medium';
  form.status = 'active';
  form.due_date = '';
  isEdit.value = false;
  currentId.value = null;
};

const open = async (id = null) => {
  console.log('📂 Открытие CaseModal, id:', id);
  resetForm();
  
  if (id) {
    isEdit.value = true;
    currentId.value = id;
    try {
      const item = await casesApi.getById(id);
      if (item) {
        Object.assign(form, item);
        if (form.due_date) {
          form.due_date = form.due_date.split('T')[0];
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
  if (!form.case_type || !form.title) {
    toastError('Заполните тип и название дела');
    return;
  }
  
  loading.value = true;
  try {
    const data = cleanData({ ...form });
    if (isEdit.value && currentId.value) {
      await casesApi.update(currentId.value, data);
      success('Дело обновлено');
    } else {
      await casesApi.create(personStore.currentPerson?.id, data);
      success('Дело добавлено');
    }
    await personStore.refreshCurrent();
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
.case-form { max-height: 70vh; overflow-y: auto; padding-right: 8px; }
.form-section { margin-bottom: 28px; padding-bottom: 20px; border-bottom: 1px solid rgba(0, 212, 168, 0.1); }
.form-section h4 { font-size: 14px; font-weight: 700; color: #ffd54f; margin: 0 0 16px 0; display: flex; align-items: center; gap: 8px; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; }
.form-group { margin-bottom: 16px; }
.form-group label { display: block; font-size: 11px; font-weight: 600; margin-bottom: 6px; color: #a8d5ce; text-transform: uppercase; letter-spacing: 0.5px; }
.form-input { width: 100%; padding: 10px 12px; background: rgba(0, 25, 22, 0.7); border: 1px solid rgba(0, 212, 168, 0.2); border-radius: 10px; color: #e8f0ef; font-size: 13px; transition: all 0.2s; }
.form-input:focus { outline: none; border-color: #ffd54f; box-shadow: 0 0 0 3px rgba(255, 213, 79, 0.1); background: rgba(0, 25, 22, 0.9); }
textarea.form-input { resize: vertical; font-family: inherit; }
@media (max-width: 768px) { .form-row { grid-template-columns: 1fr; gap: 0; } }
</style>