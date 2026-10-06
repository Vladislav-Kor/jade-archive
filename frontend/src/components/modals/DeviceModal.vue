<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="close">
    <div class="modal-content">
      <div class="modal-header">
        <h2>{{ isEdit ? '✏️ Редактирование устройства' : '➕ Новое устройство' }}</h2>
        <button class="modal-close" @click="close">✕</button>
      </div>
      
      <div class="modal-body">
        <div v-if="loading" class="loading-spinner"></div>
        
        <form v-else @submit.prevent="save">
          <div class="form-grid">
            <div class="form-group">
              <label>Тип *</label>
              <select v-model="form.device_type" required>
                <option value="">Выберите</option>
                <option value="phone">📱 Смартфон</option>
                <option value="tablet">📱 Планшет</option>
                <option value="laptop">💻 Ноутбук</option>
                <option value="desktop">🖥️ Компьютер</option>
                <option value="headphones">🎧 Наушники</option>
                <option value="smartwatch">⌚ Умные часы</option>
                <option value="watch">⌚ Часы</option>
                <option value="power-bank">🔋 Power Bank</option>
                <option value="camera">📷 Камера</option>
                <option value="console">🎮 Консоль</option>
              </select>
            </div>

            <div class="form-group">
              <label>Бренд *</label>
              <input v-model="form.brand" placeholder="Apple, Samsung..." required />
            </div>

            <div class="form-group">
              <label>Модель *</label>
              <input v-model="form.model" placeholder="iPhone 15..." required />
            </div>

            <div class="form-group">
              <label>Цвет</label>
              <input v-model="form.color" placeholder="Черный" />
            </div>

            <div class="form-group full-width">
              <label>Характеристики</label>
              <textarea v-model="form.specs" rows="2" placeholder="Процессор, память..."></textarea>
            </div>

            <div class="form-group">
              <label>IMEI</label>
              <input v-model="form.imei" placeholder="15 цифр" />
            </div>

            <div class="form-group">
              <label>Серийный номер</label>
              <input v-model="form.serial_number" placeholder="SN..." />
            </div>

            <div class="form-group">
              <label>Дата покупки</label>
              <input v-model="form.purchase_date" type="date" />
            </div>

            <div class="form-group">
              <label>Цена</label>
              <input v-model.number="form.purchase_price" type="number" step="0.01" placeholder="0.00" />
            </div>

            <div class="form-group full-width">
              <label>Место покупки</label>
              <input v-model="form.purchase_place" placeholder="Где куплено" />
            </div>

            <div class="form-group">
              <label>Гарантия до</label>
              <input v-model="form.warranty_until" type="date" />
            </div>

            <div class="form-group">
              <label>Состояние</label>
              <select v-model="form.condition">
                <option value="">Не указано</option>
                <option value="new">Новое</option>
                <option value="excellent">Отличное</option>
                <option value="good">Хорошее</option>
                <option value="used">Б/У</option>
              </select>
            </div>

            <div class="form-group full-width">
              <label>
                <input v-model="form.is_active" type="checkbox" />
                Устройство активно
              </label>
            </div>

            <div class="form-group full-width">
              <label>Заметки</label>
              <textarea v-model="form.notes" rows="2"></textarea>
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
import { ref, computed } from 'vue'
import { devicesApi } from '@/api/endpoints/devices'
import { usePersonStore } from '@/stores/usePersonStore'
import { useToast } from '@/composables/useToast'
import { toPayload } from '@/utils/payload'

const personStore = usePersonStore()

const isOpen = ref(false)
const loading = ref(false)
const isEdit = ref(false)
const deviceId = ref(null)
const personId = ref(null)

const { success, error: toastError } = useToast()

const defaultForm = {
  device_type: '',
  brand: '',
  model: '',
  color: '',
  specs: '',
  imei: '',
  serial_number: '',
  purchase_date: '',
  purchase_price: null,
  purchase_place: '',
  warranty_until: '',
  accessories: '',
  condition: '',
  notes: '',
  is_active: true,
}

const form = ref({ ...defaultForm })

const canSave = computed(() => {
  return form.value.device_type && form.value.brand && form.value.model
})

const open = async (id = null, pid = null) => {
  console.log('📱 DeviceModal.open()', { id, pid })
  
  personId.value = pid || null
  isEdit.value = !!id
  deviceId.value = id || null
  
  if (id) {
    await loadDevice(id)
  } else {
    form.value = { ...defaultForm }
  }
  
  isOpen.value = true
}

const loadDevice = async (id) => {
  try {
    loading.value = true
    const data = await devicesApi.getById(id)
    form.value = {
      device_type: data.device_type || '',
      brand: data.brand || '',
      model: data.model || '',
      color: data.color || '',
      specs: data.specs || '',
      imei: data.imei || '',
      serial_number: data.serial_number || '',
      purchase_date: data.purchase_date || '',
      purchase_price: data.purchase_price || null,
      purchase_place: data.purchase_place || '',
      warranty_until: data.warranty_until || '',
      accessories: data.accessories || '',
      condition: data.condition || '',
      notes: data.notes || '',
      is_active: data.is_active !== undefined ? data.is_active : true,
    }
  } catch (err) {
    console.error('❌ Ошибка загрузки устройства:', err)
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
      await personStore.updateItem('devices', deviceId.value, data)
      success('Устройство обновлено')
    } else {
      await personStore.createItem('devices', data)
      success('Устройство добавлено')
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
  deviceId.value = null
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
  min-height: 40px;
}

.form-group input[type="checkbox"] {
  accent-color: #00c49a;
  margin-right: 8px;
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
