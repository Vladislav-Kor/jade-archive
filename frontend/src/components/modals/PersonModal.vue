<template>
  <BaseModal ref="modalRef" :title="isEdit ? '✏️ Редактирование контакта' : '➕ Новый контакт'" size="lg">
    <template #body>
      <form @submit.prevent="handleSubmit" id="personForm" class="person-form">
        <!-- Основная информация -->
        <div class="form-section">
          <h4>📋 Основная информация</h4>
          <div class="form-row">
            <div class="form-group">
              <label>Полное имя *</label>
              <input type="text" v-model="form.full_name" required class="form-input">
            </div>
            <div class="form-group">
              <label>Короткое имя *</label>
              <input type="text" v-model="form.short_name" required class="form-input">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Телефон</label>
              <input type="tel" v-model="form.phone" class="form-input" placeholder="+7 XXX XXX-XX-XX">
            </div>
            <div class="form-group">
              <label>Email</label>
              <input type="email" v-model="form.email" class="form-input" placeholder="example@mail.com">
            </div>
          </div>
          <div class="form-group">
            <label>Адрес</label>
            <textarea v-model="form.address" rows="2" class="form-input" placeholder="Полный адрес проживания"></textarea>
          </div>
        </div>

        <!-- Личная информация -->
        <div class="form-section">
          <h4>👤 Личная информация</h4>
          <div class="form-row">
            <div class="form-group">
              <label>Дата рождения</label>
              <input type="date" v-model="form.birth_date" class="form-input">
            </div>
            <div class="form-group">
              <label>Пол</label>
              <select v-model="form.gender" class="form-input">
                <option value="">Не указан</option>
                <option value="male">Мужской</option>
                <option value="female">Женский</option>
              </select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Семейное положение</label>
              <select v-model="form.marital_status" class="form-input">
                <option value="">Не указано</option>
                <option value="single">Холост/Не замужем</option>
                <option value="married">Женат/Замужем</option>
                <option value="divorced">Разведен(а)</option>
                <option value="widowed">Вдовец/Вдова</option>
              </select>
            </div>
            <div class="form-group">
              <label>Количество детей</label>
              <input type="number" v-model.number="form.children_count" min="0" class="form-input">
            </div>
          </div>
        </div>

        <!-- Физические параметры -->
        <div class="form-section">
          <h4>📏 Физические параметры</h4>
          <div class="form-row">
            <div class="form-group">
              <label>Рост (см)</label>
              <input type="number" v-model.number="form.height" min="50" max="250" class="form-input">
            </div>
            <div class="form-group">
              <label>Вес (кг)</label>
              <input type="number" v-model.number="form.weight" min="10" max="300" class="form-input">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Размер одежды</label>
              <input type="text" v-model="form.clothing_size" class="form-input" placeholder="S, M, L, XL, XXL">
            </div>
            <div class="form-group">
              <label>Размер обуви</label>
              <input type="number" v-model.number="form.shoe_size" class="form-input">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Грудь (см)</label>
              <input type="number" v-model.number="form.chest_size" class="form-input">
            </div>
            <div class="form-group">
              <label>Талия (см)</label>
              <input type="number" v-model.number="form.waist_size" class="form-input">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Бедра (см)</label>
              <input type="number" v-model.number="form.hip_size" class="form-input">
            </div>
          </div>
        </div>

        <!-- Медицинская информация -->
        <div class="form-section">
          <h4>🏥 Медицинская информация</h4>
          <div class="form-row">
            <div class="form-group">
              <label>Группа крови</label>
              <select v-model="form.blood_type" class="form-input">
                <option value="">Не указана</option>
                <option value="A">A (II)</option>
                <option value="B">B (III)</option>
                <option value="AB">AB (IV)</option>
                <option value="O">O (I)</option>
              </select>
            </div>
            <div class="form-group">
              <label>Резус-фактор</label>
              <select v-model="form.rh_factor" class="form-input">
                <option value="">Не указан</option>
                <option value="positive">Положительный (+)</option>
                <option value="negative">Отрицательный (-)</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label>Аллергии</label>
            <textarea v-model="form.allergies" rows="2" class="form-input" placeholder="Какие аллергены, реакция"></textarea>
          </div>
          <div class="form-group">
            <label>Хронические заболевания</label>
            <textarea v-model="form.chronic_diseases" rows="2" class="form-input"></textarea>
          </div>
          <div class="form-group">
            <label>Принимаемые лекарства</label>
            <textarea v-model="form.medications" rows="2" class="form-input"></textarea>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Артериальное давление</label>
              <input type="text" v-model="form.blood_pressure" class="form-input" placeholder="120/80">
            </div>
            <div class="form-group">
              <label>Пульс (уд/мин)</label>
              <input type="number" v-model.number="form.heart_rate" class="form-input">
            </div>
          </div>
        </div>

        <!-- Документы -->
        <div class="form-section">
          <h4>🪪 Документы</h4>
          <div class="form-group">
            <label>Паспорт (серия номер)</label>
            <input type="text" v-model="form.passport_number" class="form-input" placeholder="XXXX XXXXXX">
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>ИНН</label>
              <input type="text" v-model="form.inn" class="form-input">
            </div>
            <div class="form-group">
              <label>СНИЛС</label>
              <input type="text" v-model="form.snils" class="form-input">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Водительские права (категории)</label>
              <input type="text" v-model="form.driver_license_category" class="form-input" placeholder="A, B, C, D">
            </div>
            <div class="form-group">
              <label>Номер прав</label>
              <input type="text" v-model="form.driver_license_number" class="form-input">
            </div>
          </div>
        </div>

        <!-- Работа и образование -->
        <div class="form-section">
          <h4>💼 Работа и образование</h4>
          <div class="form-group">
            <label>Образование</label>
            <input type="text" v-model="form.education" class="form-input" placeholder="Высшее, Среднее и т.д.">
          </div>
          <div class="form-group">
            <label>Профессия</label>
            <input type="text" v-model="form.profession" class="form-input">
          </div>
          <div class="form-group">
            <label>Место работы</label>
            <input type="text" v-model="form.workplace" class="form-input">
          </div>
        </div>

        <!-- Предпочтения -->
        <div class="form-section">
          <h4>❤️ Предпочтения и интересы</h4>
          <div class="form-row">
            <div class="form-group">
              <label>Любимый цвет</label>
              <input type="text" v-model="form.favorite_color" class="form-input">
            </div>
            <div class="form-group">
              <label>Любимые цветы</label>
              <input type="text" v-model="form.favorite_flowers" class="form-input">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Любимая еда</label>
              <input type="text" v-model="form.favorite_food" class="form-input">
            </div>
            <div class="form-group">
              <label>Любимая музыка</label>
              <input type="text" v-model="form.favorite_music" class="form-input">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Любимые фильмы</label>
              <input type="text" v-model="form.favorite_movies" class="form-input">
            </div>
            <div class="form-group">
              <label>Хобби</label>
              <input type="text" v-model="form.hobbies" class="form-input">
            </div>
          </div>
        </div>

        <!-- Важность и заметки -->
        <div class="form-section">
          <h4>⭐ Важность и заметки</h4>
          <div class="form-row">
            <div class="form-group">
              <label>Уровень важности</label>
              <select v-model="form.importance_level" class="form-input">
                <option value="low">Низкая</option>
                <option value="medium">Средняя</option>
                <option value="high">Высокая</option>
                <option value="critical">Критическая</option>
              </select>
            </div>
            <div class="form-group">
              <label>Числовое значение (0-10)</label>
              <input type="number" v-model.number="form.importance" step="0.1" min="0" max="10" class="form-input">
            </div>
          </div>
          <div class="form-group">
            <label>Заметки</label>
            <textarea v-model="form.notes" rows="3" class="form-input" placeholder="Дополнительная информация"></textarea>
          </div>
        </div>
      </form>
    </template>
    <template #footer>
      <button class="btn-secondary" @click="close">Отмена</button>
      <button type="submit" form="personForm" class="btn-primary" :disabled="loading">
        {{ loading ? 'Сохранение...' : 'Сохранить' }}
      </button>
    </template>
  </BaseModal>
</template>

<script setup>
import { ref, reactive } from 'vue';
import BaseModal from '../common/BaseModal.vue';
import { personsApi } from '@/api/endpoints/persons';
import { useTreeStore } from '@/stores/useTreeStore';
import { usePersonStore } from '@/stores/usePersonStore';
import { useToast } from '@/composables/useToast';
import { toPayload, fillForm } from '@/utils/payload';

const modalRef = ref(null);
const treeStore = useTreeStore();
const personStore = usePersonStore();
const { success, error: toastError } = useToast();

const isEdit = ref(false);
const currentId = ref(null);
const loading = ref(false);

const form = reactive({
  full_name: '',
  short_name: '',
  phone: '',
  email: '',
  address: '',
  birth_date: '',
  gender: '',
  marital_status: '',
  children_count: 0,
  height: null,
  weight: null,
  clothing_size: '',
  shoe_size: null,
  chest_size: null,
  waist_size: null,
  hip_size: null,
  blood_type: '',
  rh_factor: '',
  allergies: '',
  chronic_diseases: '',
  medications: '',
  blood_pressure: '',
  heart_rate: null,
  passport_number: '',
  inn: '',
  snils: '',
  driver_license_category: '',
  driver_license_number: '',
  education: '',
  profession: '',
  workplace: '',
  favorite_color: '',
  favorite_flowers: '',
  favorite_food: '',
  favorite_music: '',
  favorite_movies: '',
  hobbies: '',
  importance_level: 'medium',
  importance: 0,
  notes: ''
});

const resetForm = () => {
  Object.keys(form).forEach(key => {
    if (key === 'children_count') form[key] = 0;
    else if (key === 'importance') form[key] = 0;
    else if (key === 'importance_level') form[key] = 'medium';
    else if (typeof form[key] === 'number') form[key] = null;
    else form[key] = '';
  });
  isEdit.value = false;
  currentId.value = null;
};

const open = async (id = null) => {
  resetForm();
  if (id) {
    isEdit.value = true;
    currentId.value = id;
    try {
      const person = await personsApi.getById(id);
      fillForm(form, person);
      if (person.birth_date) {
        form.birth_date = person.birth_date.split('T')[0];
      }
    } catch (err) {
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
  if (!form.full_name || !form.short_name) {
    toastError('Заполните обязательные поля (ФИО и короткое имя)');
    return;
  }
  
  loading.value = true;
  try {
    const data = toPayload({ ...form }, isEdit.value);
    if (isEdit.value && currentId.value) {
      // Профиль и строка в боковой панели обновляются ответом сервера, вкладки не перезагружаются.
      await personStore.updatePerson(currentId.value, data);
      success('Контакт обновлен');
    } else {
      const created = await personStore.createPerson(data);
      success('Контакт добавлен');
      treeStore.selectPerson(created.id);
      personStore.loadPerson(created.id);  // сразу открываем новый контакт
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
.person-form { max-height: 70vh; overflow-y: auto; padding-right: 8px; }
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