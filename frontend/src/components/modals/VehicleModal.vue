<template>
  <BaseModal ref="modalRef" :title="isEdit ? '✏️ Редактирование ТС' : '🚗 Новое транспортное средство'" size="lg">
    <template #body>
      <form @submit.prevent="handleSubmit" id="vehicleForm" class="vehicle-form">
        
        <!-- Основная информация -->
        <div class="form-section">
          <h4>🚗 Основная информация</h4>
          <div class="form-row">
            <div class="form-group">
              <label>Тип ТС *</label>
              <select v-model="form.vehicle_type" required class="form-input">
                <option value="">Выберите тип</option>
                <option value="car">🚗 Легковой автомобиль</option>
                <option value="motorcycle">🏍️ Мотоцикл</option>
                <option value="scooter">🛵 Скутер</option>
                <option value="truck">🚚 Грузовик</option>
                <option value="bus">🚌 Автобус</option>
                <option value="suv">🚙 Внедорожник/SUV</option>
                <option value="sports">🏎️ Спортивный автомобиль</option>
                <option value="electric">🔋 Электромобиль</option>
              </select>
            </div>
            <div class="form-group">
              <label>Марка *</label>
              <input type="text" v-model="form.brand" required class="form-input" placeholder="Марка автомобиля">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Модель *</label>
              <input type="text" v-model="form.model" required class="form-input" placeholder="Модель">
            </div>
            <div class="form-group">
              <label>Год выпуска</label>
              <input type="number" v-model.number="form.year" class="form-input" placeholder="Год">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Цвет</label>
              <input type="text" v-model="form.color" class="form-input" placeholder="Цвет">
            </div>
            <div class="form-group">
              <label>Государственный номер</label>
              <input type="text" v-model="form.license_plate" class="form-input" placeholder="А123ВС 777">
            </div>
          </div>
        </div>

        <!-- Технические характеристики -->
        <div class="form-section">
          <h4>🔧 Технические характеристики</h4>
          <div class="form-group">
            <label>VIN номер</label>
            <input type="text" v-model="form.vin" class="form-input" placeholder="VIN код">
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Номер двигателя</label>
              <input type="text" v-model="form.engine_number" class="form-input">
            </div>
            <div class="form-group">
              <label>Номер шасси</label>
              <input type="text" v-model="form.chassis_number" class="form-input">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Объем двигателя (л)</label>
              <input type="number" v-model.number="form.engine_capacity" step="0.1" class="form-input" placeholder="л">
            </div>
            <div class="form-group">
              <label>Мощность (л.с.)</label>
              <input type="number" v-model.number="form.horsepower" class="form-input" placeholder="л.с.">
            </div>
          </div>
          <div class="form-group">
            <label>Пробег (км)</label>
            <input type="number" v-model.number="form.mileage" class="form-input" placeholder="км">
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Коробка передач</label>
              <select v-model="form.transmission" class="form-input">
                <option value="">Выберите КПП</option>
                <option value="manual">Механическая</option>
                <option value="automatic">Автоматическая</option>
                <option value="cvt">Вариатор</option>
                <option value="robot">Роботизированная</option>
              </select>
            </div>
            <div class="form-group">
              <label>Привод</label>
              <select v-model="form.drive_type" class="form-input">
                <option value="">Выберите привод</option>
                <option value="front">Передний</option>
                <option value="rear">Задний</option>
                <option value="full">Полный</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label>Топливо</label>
            <select v-model="form.fuel_type" class="form-input">
              <option value="">Выберите тип топлива</option>
              <option value="petrol">Бензин</option>
              <option value="diesel">Дизель</option>
              <option value="electric">Электро</option>
              <option value="hybrid">Гибрид</option>
              <option value="lpg">Газ</option>
            </select>
          </div>
        </div>

        <!-- Документы -->
        <div class="form-section">
          <h4>📄 Документы</h4>
          <div class="form-row">
            <div class="form-group">
              <label>Тип собственности</label>
              <select v-model="form.ownership_type" class="form-input">
                <option value="">Выберите тип</option>
                <option value="own">Собственность</option>
                <option value="leasing">Лизинг</option>
                <option value="credit">Кредит</option>
              </select>
            </div>
            <div class="form-group">
              <label>Дата регистрации</label>
              <input type="date" v-model="form.registration_date" class="form-input">
            </div>
          </div>
          <div class="form-group">
            <label>Регистрационный номер</label>
            <input type="text" v-model="form.registration_number" class="form-input" placeholder="Свидетельство о регистрации">
          </div>
        </div>

        <!-- Финансы -->
        <div class="form-section">
          <h4>💰 Финансовая информация</h4>
          <div class="form-row">
            <div class="form-group">
              <label>Цена покупки (₽)</label>
              <input type="number" v-model.number="form.purchase_price" step="0.01" class="form-input" placeholder="₽">
            </div>
            <div class="form-group">
              <label>Текущая стоимость (₽)</label>
              <input type="number" v-model.number="form.current_value" step="0.01" class="form-input" placeholder="₽">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Банк кредита</label>
              <input type="text" v-model="form.loan_bank" class="form-input" placeholder="Название банка">
            </div>
            <div class="form-group">
              <label>Сумма кредита (₽)</label>
              <input type="number" v-model.number="form.loan_amount" step="0.01" class="form-input" placeholder="₽">
            </div>
          </div>
          <div class="form-group">
            <label>Остаток по кредиту (₽)</label>
            <input type="number" v-model.number="form.loan_left" step="0.01" class="form-input" placeholder="₽">
          </div>
        </div>

        <!-- Страховка -->
        <div class="form-section">
          <h4>🛡️ Страховка</h4>
          <div class="form-row">
            <div class="form-group">
              <label>Страховая компания</label>
              <input type="text" v-model="form.insurance_company" class="form-input">
            </div>
            <div class="form-group">
              <label>Номер полиса</label>
              <input type="text" v-model="form.insurance_policy" class="form-input">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Страховка КАСКО до</label>
              <input type="date" v-model="form.insurance_until" class="form-input">
            </div>
            <div class="form-group">
              <label>ОСАГО до</label>
              <input type="date" v-model="form.osago_until" class="form-input">
            </div>
          </div>
        </div>

        <!-- Обслуживание -->
        <div class="form-section">
          <h4>🔧 Обслуживание</h4>
          <div class="form-row">
            <div class="form-group">
              <label>Последнее ТО</label>
              <input type="date" v-model="form.last_maintenance" class="form-input">
            </div>
            <div class="form-group">
              <label>Следующее ТО</label>
              <input type="date" v-model="form.next_maintenance" class="form-input">
            </div>
          </div>
          <div class="form-group">
            <label>Заметки по обслуживанию</label>
            <textarea v-model="form.maintenance_notes" rows="2" class="form-input" placeholder="Что делали, что планируется"></textarea>
          </div>
        </div>

        <!-- Состояние и заметки -->
        <div class="form-section">
          <h4>📝 Состояние и заметки</h4>
          <div class="form-row">
            <div class="form-group">
              <label>Состояние ТС</label>
              <select v-model="form.condition" class="form-input">
                <option value="">Выберите состояние</option>
                <option value="excellent">Отличное</option>
                <option value="good">Хорошее</option>
                <option value="normal">Нормальное</option>
                <option value="bad">Плохое</option>
                <option value="broken">Не на ходу</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label>Общие заметки</label>
            <textarea v-model="form.notes" rows="3" class="form-input" placeholder="Дополнительная информация"></textarea>
          </div>
          <div class="form-group checkbox-group">
            <label class="checkbox-label">
              <input type="checkbox" v-model="form.is_active" class="checkbox-input">
              <span>ТС в эксплуатации</span>
            </label>
          </div>
        </div>

      </form>
    </template>
    <template #footer>
      <button class="btn-secondary" @click="close">Отмена</button>
      <button type="submit" form="vehicleForm" class="btn-primary" :disabled="loading">
        {{ loading ? 'Сохранение...' : 'Сохранить' }}
      </button>
    </template>
  </BaseModal>
</template>

<script setup>
import { ref, reactive } from 'vue';
import BaseModal from '../common/BaseModal.vue';
import { vehiclesApi } from '@/api/endpoints/vehicles';
import { usePersonStore } from '@/stores/usePersonStore';
import { useToast } from '@/composables/useToast';

const modalRef = ref(null);
const personStore = usePersonStore();
const { success, error: toastError } = useToast();

const isEdit = ref(false);
const currentId = ref(null);
const loading = ref(false);

const form = reactive({
  vehicle_type: '',
  brand: '',
  model: '',
  year: null,
  color: '',
  license_plate: '',
  vin: '',
  engine_number: '',
  chassis_number: '',
  engine_capacity: null,
  horsepower: null,
  mileage: null,
  transmission: '',
  drive_type: '',
  fuel_type: '',
  ownership_type: '',
  registration_date: '',
  registration_number: '',
  purchase_price: null,
  current_value: null,
  loan_bank: '',
  loan_amount: null,
  loan_left: null,
  insurance_company: '',
  insurance_policy: '',
  insurance_until: '',
  osago_until: '',
  last_maintenance: '',
  next_maintenance: '',
  maintenance_notes: '',
  condition: '',
  notes: '',
  is_active: true
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
  Object.keys(form).forEach(key => {
    if (key === 'is_active') form[key] = true;
    else if (typeof form[key] === 'number') form[key] = null;
    else form[key] = '';
  });
  isEdit.value = false;
  currentId.value = null;
};

const open = async (id = null) => {
  console.log('📂 Открытие VehicleModal, id:', id);
  resetForm();
  
  if (id) {
    isEdit.value = true;
    currentId.value = id;
    try {
      const item = await vehiclesApi.getById(id);
      if (item) {
        Object.assign(form, item);
        if (form.registration_date) {
          form.registration_date = form.registration_date.split('T')[0];
        }
        if (form.insurance_until) {
          form.insurance_until = form.insurance_until.split('T')[0];
        }
        if (form.osago_until) {
          form.osago_until = form.osago_until.split('T')[0];
        }
        if (form.last_maintenance) {
          form.last_maintenance = form.last_maintenance.split('T')[0];
        }
        if (form.next_maintenance) {
          form.next_maintenance = form.next_maintenance.split('T')[0];
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
  if (!form.vehicle_type || !form.brand || !form.model) {
    toastError('Заполните тип, марку и модель ТС');
    return;
  }
  
  loading.value = true;
  try {
    const data = cleanData({ ...form });
    if (isEdit.value && currentId.value) {
      await vehiclesApi.update(currentId.value, data);
      success('ТС обновлено');
    } else {
      await vehiclesApi.create(personStore.currentPerson?.id, data);
      success('ТС добавлено');
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
.vehicle-form { max-height: 70vh; overflow-y: auto; padding-right: 8px; }
.form-section { margin-bottom: 28px; padding-bottom: 20px; border-bottom: 1px solid rgba(0, 212, 168, 0.1); }
.form-section h4 { font-size: 14px; font-weight: 700; color: #ffd54f; margin: 0 0 16px 0; display: flex; align-items: center; gap: 8px; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; }
.form-group { margin-bottom: 16px; }
.form-group label { display: block; font-size: 11px; font-weight: 600; margin-bottom: 6px; color: #a8d5ce; text-transform: uppercase; letter-spacing: 0.5px; }
.form-input { width: 100%; padding: 10px 12px; background: rgba(0, 25, 22, 0.7); border: 1px solid rgba(0, 212, 168, 0.2); border-radius: 10px; color: #e8f0ef; font-size: 13px; transition: all 0.2s; }
.form-input:focus { outline: none; border-color: #ffd54f; box-shadow: 0 0 0 3px rgba(255, 213, 79, 0.1); background: rgba(0, 25, 22, 0.9); }
textarea.form-input { resize: vertical; font-family: inherit; }
.checkbox-group { margin-top: 16px; }
.checkbox-label { display: flex; align-items: center; gap: 10px; cursor: pointer; text-transform: none; font-size: 13px; color: #e8f0ef; }
.checkbox-input { width: 18px; height: 18px; cursor: pointer; accent-color: #00d4a8; }
@media (max-width: 768px) { .form-row { grid-template-columns: 1fr; gap: 0; } }
</style>