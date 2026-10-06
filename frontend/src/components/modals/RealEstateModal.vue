<template>
  <BaseModal ref="modalRef" :title="isEdit ? '✏️ Редактирование недвижимости' : '🏢 Новая недвижимость'" size="lg">
    <template #body>
      <form @submit.prevent="handleSubmit" id="realEstateForm" class="real-estate-form">
        <div class="form-section">
          <h4>🏠 Основная информация</h4>
          <div class="form-row">
            <div class="form-group">
              <label>Тип недвижимости *</label>
              <select v-model="form.property_type" required class="form-input">
                <option value="">Выберите тип</option>
                <option value="apartment">🏢 Квартира</option>
                <option value="house">🏠 Дом</option>
                <option value="land">🌾 Земельный участок</option>
                <option value="commercial">🏭 Коммерческая</option>
                <option value="garage">🚗 Гараж</option>
                <option value="office">💼 Офис</option>
                <option value="warehouse">📦 Склад</option>
                <option value="retail">🛍️ Торговая площадь</option>
              </select>
            </div>
            <div class="form-group">
              <label>Название</label>
              <input type="text" v-model="form.property_name" class="form-input" placeholder="Например: Квартира на Ленина">
            </div>
          </div>
          <div class="form-group">
            <label>Адрес *</label>
            <textarea v-model="form.address" rows="2" required class="form-input" placeholder="Полный адрес объекта"></textarea>
          </div>
        </div>

        <div class="form-section">
          <h4>📐 Параметры</h4>
          <div class="form-row">
            <div class="form-group">
              <label>Общая площадь (м²)</label>
              <input type="number" v-model.number="form.total_area" step="0.1" class="form-input" placeholder="м²">
            </div>
            <div class="form-group">
              <label>Жилая площадь (м²)</label>
              <input type="number" v-model.number="form.living_area" step="0.1" class="form-input" placeholder="м²">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Площадь участка (м²)</label>
              <input type="number" v-model.number="form.land_area" step="0.1" class="form-input" placeholder="м²">
            </div>
            <div class="form-group">
              <label>Количество комнат</label>
              <input type="number" v-model.number="form.rooms_count" class="form-input" placeholder="шт">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Этаж</label>
              <input type="number" v-model.number="form.floor" class="form-input" placeholder="Этаж">
            </div>
            <div class="form-group">
              <label>Всего этажей</label>
              <input type="number" v-model.number="form.total_floors" class="form-input" placeholder="всего">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Количество санузлов</label>
              <input type="number" v-model.number="form.bathroom_count" class="form-input" placeholder="шт">
            </div>
            <div class="form-group">
              <label>Количество балконов/лоджий</label>
              <input type="number" v-model.number="form.balcony_count" class="form-input" placeholder="шт">
            </div>
          </div>
        </div>

        <div class="form-section">
          <h4>📄 Право собственности</h4>
          <div class="form-row">
            <div class="form-group">
              <label>Тип собственности</label>
              <select v-model="form.ownership_type" class="form-input">
                <option value="">Выберите тип</option>
                <option value="sole">Единоличная</option>
                <option value="shared">Долевая</option>
                <option value="joint">Совместная</option>
                <option value="municipal">Муниципальная</option>
                <option value="rent">Аренда</option>
              </select>
            </div>
            <div class="form-group">
              <label>Доля владения (%)</label>
              <input type="number" v-model.number="form.ownership_percent" step="0.1" min="0" max="100" class="form-input">
            </div>
          </div>
          <div class="form-group">
            <label>Кадастровый номер</label>
            <input type="text" v-model="form.cadastral_number" class="form-input" placeholder="Номер в кадастре">
          </div>
          <div class="form-group">
            <label>Дата регистрации права</label>
            <input type="date" v-model="form.registration_date" class="form-input">
          </div>
        </div>

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
              <label>Банк ипотеки</label>
              <input type="text" v-model="form.mortgage_bank" class="form-input" placeholder="Название банка">
            </div>
            <div class="form-group">
              <label>Сумма ипотеки (₽)</label>
              <input type="number" v-model.number="form.mortgage_amount" step="0.01" class="form-input" placeholder="₽">
            </div>
          </div>
          <div class="form-group">
            <label>Остаток по ипотеке (₽)</label>
            <input type="number" v-model.number="form.mortgage_left" step="0.01" class="form-input" placeholder="₽">
          </div>
        </div>

        <div class="form-section">
          <h4>🔧 Состояние</h4>
          <div class="form-row">
            <div class="form-group">
              <label>Состояние</label>
              <select v-model="form.condition" class="form-input">
                <option value="">Выберите состояние</option>
                <option value="excellent">Отличное</option>
                <option value="good">Хорошее</option>
                <option value="normal">Нормальное</option>
                <option value="needs_repair">Требует ремонта</option>
                <option value="emergency">Аварийное</option>
              </select>
            </div>
            <div class="form-group">
              <label>Год постройки</label>
              <input type="number" v-model.number="form.year_built" class="form-input" placeholder="Год">
            </div>
          </div>
          <div class="form-group">
            <label>Год последнего ремонта</label>
            <input type="number" v-model.number="form.renovation_year" class="form-input" placeholder="Год">
          </div>
        </div>

        <div class="form-section">
          <h4>📝 Заметки</h4>
          <div class="form-group">
            <label>Дополнительная информация</label>
            <textarea v-model="form.notes" rows="3" class="form-input" placeholder="Особенности, обременения, планировка и т.д."></textarea>
          </div>
          <div class="form-group checkbox-group">
            <label class="checkbox-label">
              <input type="checkbox" v-model="form.is_active" class="checkbox-input">
              <span>Объект активен</span>
            </label>
          </div>
        </div>
      </form>
    </template>
    <template #footer>
      <button class="btn-secondary" @click="close">Отмена</button>
      <button type="submit" form="realEstateForm" class="btn-primary" :disabled="loading">
        {{ loading ? 'Сохранение...' : 'Сохранить' }}
      </button>
    </template>
  </BaseModal>
</template>

<script setup>
import { ref, reactive } from 'vue';
import BaseModal from '../common/BaseModal.vue';
import { realEstateApi } from '@/api/endpoints/real-estate';
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
  property_type: '',
  property_name: '',
  address: '',
  total_area: null,
  living_area: null,
  land_area: null,
  floor: null,
  total_floors: null,
  rooms_count: null,
  bathroom_count: null,
  balcony_count: null,
  ownership_type: '',
  ownership_percent: 100,
  cadastral_number: '',
  registration_date: '',
  purchase_price: null,
  current_value: null,
  mortgage_bank: '',
  mortgage_amount: null,
  mortgage_left: null,
  condition: '',
  year_built: null,
  renovation_year: null,
  notes: '',
  is_active: true
});


const resetForm = () => {
  Object.keys(form).forEach(key => {
    if (key === 'is_active') form[key] = true;
    else if (key === 'ownership_percent') form[key] = 100;
    else if (typeof form[key] === 'number') form[key] = null;
    else form[key] = '';
  });
  isEdit.value = false;
  currentId.value = null;
};

const open = async (id = null) => {
  console.log('📂 Открытие RealEstateModal, id:', id);
  resetForm();
  
  if (id) {
    isEdit.value = true;
    currentId.value = id;
    try {
      const item = await realEstateApi.getById(id);
      if (item) {
        fillForm(form, item);
        if (form.registration_date) {
          form.registration_date = form.registration_date.split('T')[0];
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
  if (!form.property_type || !form.address) {
    toastError('Заполните тип недвижимости и адрес');
    return;
  }
  
  loading.value = true;
  try {
    const data = toPayload({ ...form }, isEdit.value);
    if (isEdit.value && currentId.value) {
      await personStore.updateItem('real_estate', currentId.value, data);
      success('Недвижимость обновлена');
    } else {
      await personStore.createItem('real_estate', data);
      success('Недвижимость добавлена');
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
.real-estate-form { max-height: 70vh; overflow-y: auto; padding-right: 8px; }
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