<template>
  <BaseModal ref="modalRef" title="Добавление связи" icon="link" size="sm">
    <template #body>
      <form @submit.prevent="handleSubmit" id="relationForm">
        <div class="form-group">
          <label>Выберите контакт *</label>
          <select v-model="form.child_id" required class="form-input">
            <option value="">-- Выберите контакт --</option>
            <option v-for="p in availablePersons" :key="p.id" :value="p.id">
              {{ p.full_name }} (@{{ p.short_name }})
            </option>
          </select>
        </div>
        <div class="form-group">
          <label>Тип связи *</label>
          <input type="text" v-model="form.relation_type" required placeholder="Друг, Коллега, Родственник..." class="form-input">
        </div>
      </form>
    </template>
    <template #footer>
      <button class="btn-secondary" @click="close">Отмена</button>
      <button type="submit" form="relationForm" class="btn-primary" :disabled="loading">
        <Icon name="plus" size="sm" /> Добавить
      </button>
    </template>
  </BaseModal>
</template>

<script setup>
import { ref, reactive, computed } from 'vue';
import Icon from '../common/Icon.vue';
import BaseModal from '../common/BaseModal.vue';
import { useTreeStore } from '@/stores/useTreeStore';
import { usePersonStore } from '@/stores/usePersonStore';
import { useToast } from '@/composables/useToast';

const modalRef = ref(null);
const treeStore = useTreeStore();
const personStore = usePersonStore();
const { success, error: toastError } = useToast();

const parentId = ref(null);
const loading = ref(false);

const form = reactive({
  child_id: '',
  relation_type: ''
});

const availablePersons = computed(() => {
  if (!parentId.value) return [];
  return treeStore.persons.filter(p => p.id !== parentId.value);
});

const resetForm = () => {
  form.child_id = '';
  form.relation_type = '';
};

const open = async (id) => {
  parentId.value = id;
  resetForm();
  
  if (availablePersons.value.length === 0) {
    toastError('Нет доступных контактов для связи');
    return;
  }
  
  modalRef.value?.open();
};

const close = () => {
  modalRef.value?.close();
};

const handleSubmit = async () => {
  if (!form.child_id || !form.relation_type) {
    toastError('Заполните все поля');
    return;
  }
  
  loading.value = true;
  try {
    const data = {
      parent_id: parentId.value,
      child_id: parseInt(form.child_id),
      relation_type: form.relation_type
    };
    
    // Связь сразу появляется и в дереве, и во вкладке «Связи» открытого контакта.
    await personStore.createRelation(data);
    success('Связь добавлена');
    close();
  } catch (err) {
    toastError(err.message || 'Ошибка добавления связи');
  } finally {
    loading.value = false;
  }
};

defineExpose({ open, close });
</script>

<style scoped>
.form-group { margin-bottom: 20px; }
.form-group label { display: block; font-size: 11px; font-weight: 600; margin-bottom: 6px; color: #a8d5ce; text-transform: uppercase; letter-spacing: 0.5px; }
.form-input { width: 100%; padding: 10px 12px; background: rgba(0, 25, 22, 0.7); border: 1px solid rgba(0, 212, 168, 0.2); border-radius: 10px; color: #e8f0ef; font-size: 13px; transition: all 0.2s; }
.form-input:focus { outline: none; border-color: #ffd54f; background: rgba(0, 25, 22, 0.9); }
select.form-input { cursor: pointer; }
</style>