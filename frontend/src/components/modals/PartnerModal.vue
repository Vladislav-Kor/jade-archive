<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="close">
    <div class="modal-content">
      <div class="modal-header">
        <h2>{{ isEdit ? '✏️ Редактирование партнера' : '➕ Новый партнер' }}</h2>
        <button class="modal-close" @click="close">✕</button>
      </div>
      
      <div class="modal-body">
        <div v-if="loading" class="loading-spinner"></div>
        
        <form v-else @submit.prevent="save">
          <div class="form-grid">
            <!-- Партнер -->
            <div class="form-group full-width">
              <label>Выберите партнера *</label>
              <select v-model="form.partner_id" required>
                <option value="">-- Выберите контакт --</option>
                <option 
                  v-for="p in availablePersons" 
                  :key="p.id" 
                  :value="p.id"
                  :disabled="p.id === personId"
                >
                  {{ p.full_name }} (@{{ p.short_name }})
                </option>
              </select>
            </div>

            <div class="form-group">
              <label>Тип отношений</label>
              <input v-model="form.relationship_type" placeholder="романтический, деловой..." />
            </div>

            <div class="form-group">
              <label>Статус</label>
              <select v-model="form.relationship_status">
                <option value="">Не указан</option>
                <option value="active">Активные</option>
                <option value="ended">Завершены</option>
                <option value="pending">Ожидают</option>
              </select>
            </div>

            <div class="form-group">
              <label>Метка</label>
              <input v-model="form.relationship_label" placeholder="Любимый, Партнер..." />
            </div>

            <div class="form-group">
              <label>Дата начала</label>
              <input v-model="form.start_date" type="date" />
            </div>

            <div class="form-group">
              <label>Дата окончания</label>
              <input v-model="form.end_date" type="date" />
            </div>

            <div class="form-group full-width">
              <label>Заметки</label>
              <textarea v-model="form.relationship_notes" rows="3"></textarea>
            </div>
          </div>

          <div class="modal-actions">
            <button type="button" class="btn-cancel" @click="close">Отмена</button>
            <button type="submit" class="btn-save" :disabled="!canSave || loading">
              {{ isEdit ? 'Сохранить' : 'Создать' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { partnersApi } from '@/api/endpoints/partners'
import { usePersonStore } from '@/stores/usePersonStore'
import { useTreeStore } from '@/stores/useTreeStore'
import { useToast } from '@/composables/useToast'
import { toPayload } from '@/utils/payload'

const personStore = usePersonStore()
const treeStore = useTreeStore()

const isOpen = ref(false)
const loading = ref(false)
const isEdit = ref(false)
const personId = ref(null)
const partnerId = ref(null)
// Список людей уже есть в сторе боковой панели и обновляется сам.
const availablePersons = computed(() => treeStore.persons)

const { success, error: toastError } = useToast()

const defaultForm = {
  partner_id: '',
  relationship_type: '',
  relationship_status: '',
  relationship_label: '',
  start_date: '',
  end_date: '',
  breakup_reason: '',
  emotional_connection: '',
  physical_connection: '',
  relationship_rating: null,
  relationship_notes: '',
}

const form = ref({ ...defaultForm })

const canSave = computed(() => {
  return form.value.partner_id && form.value.partner_id !== personId.value
})

const open = async (id = null, pid = null) => {
  console.log('📂 PartnerModal.open()', { id, pid })
  
  personId.value = pid || null
  isEdit.value = !!id
  partnerId.value = id || null
  
  if (id) {
    await loadPartner(id)
  } else {
    form.value = { ...defaultForm }
  }
  
  isOpen.value = true
}

const loadPartner = async (id) => {
  try {
    loading.value = true
    const data = await partnersApi.getById(id)
    form.value = {
      partner_id: data.partner_id || '',
      relationship_type: data.relationship_type || '',
      relationship_status: data.relationship_status || '',
      relationship_label: data.relationship_label || '',
      start_date: data.start_date || '',
      end_date: data.end_date || '',
      breakup_reason: data.breakup_reason || '',
      emotional_connection: data.emotional_connection || '',
      physical_connection: data.physical_connection || '',
      relationship_rating: data.relationship_rating || null,
      relationship_notes: data.relationship_notes || '',
    }
  } catch (err) {
    console.error('❌ Ошибка загрузки партнера:', err)
    toastError('Ошибка загрузки')
    close()
  } finally {
    loading.value = false
  }
}

const save = async () => {
  if (!canSave.value) return
  
  loading.value = true
  try {
    const data = toPayload({ ...form.value }, isEdit.value)

    if (isEdit.value) {
      await personStore.updateItem('partners', partnerId.value, data)
      success('Партнер обновлен')
    } else {
      await personStore.createItem('partners', data)
      success('Партнер добавлен')
    }

    close()
  } catch (err) {
    console.error('❌ Ошибка сохранения:', err)
    toastError(err.message || 'Ошибка сохранения')
  } finally {
    loading.value = false
  }
}

const close = () => {
  isOpen.value = false
  form.value = { ...defaultForm }
  isEdit.value = false
  partnerId.value = null
}

defineExpose({ open, close })
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(8px);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.modal-content {
  background: #0d1210;
  border: 1px solid #1a2420;
  border-radius: 20px;
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid #1a2420;
}

.modal-header h2 {
  font-size: 18px;
  font-weight: 600;
  color: #fff;
  margin: 0;
}

.modal-close {
  background: none;
  border: none;
  color: #5a6e68;
  font-size: 24px;
  cursor: pointer;
  padding: 0 8px;
}

.modal-close:hover {
  color: #fff;
}

.modal-body {
  padding: 24px;
  overflow-y: auto;
  flex: 1;
  position: relative;
  min-height: 200px;
}

.loading-spinner {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.loading-spinner::after {
  content: '';
  width: 40px;
  height: 40px;
  border: 4px solid #1a2420;
  border-top-color: #00c49a;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.full-width {
  grid-column: 1 / -1;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.form-group label {
  font-size: 12px;
  color: #5a6e68;
  font-weight: 500;
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: 8px 12px;
  background: #0a0e0c;
  border: 1px solid #1a2420;
  border-radius: 8px;
  color: #e0e8e5;
  font-size: 14px;
  transition: border-color 0.2s;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #00c49a;
}

.form-group textarea {
  resize: vertical;
  min-height: 60px;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding-top: 16px;
  border-top: 1px solid #1a2420;
  margin-top: 8px;
}

.btn-cancel {
  padding: 8px 20px;
  background: #1a2420;
  border: none;
  border-radius: 8px;
  color: #5a6e68;
  cursor: pointer;
}

.btn-cancel:hover {
  background: #2a3a35;
}

.btn-save {
  padding: 8px 24px;
  background: #00c49a;
  border: none;
  border-radius: 8px;
  color: #0a0e0c;
  font-weight: 600;
  cursor: pointer;
}

.btn-save:hover:not(:disabled) {
  background: #00d6a8;
}

.btn-save:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
</style>
