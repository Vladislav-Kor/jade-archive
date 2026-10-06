<template>
  <BaseModal ref="modalRef" :title="isEdit ? '✏️ Редактирование аккаунта' : '🎮 Новый цифровой аккаунт'" size="lg">
    <template #body>
      <form @submit.prevent="handleSubmit" id="digitalAccountForm" class="digital-form">
        
        <!-- Основная информация -->
        <div class="form-section">
          <h4>📱 Основная информация</h4>
          <div class="form-row">
            <div class="form-group">
              <label>Тип платформы *</label>
              <select v-model="form.platform_type" required class="form-input">
                <option value="">Выберите платформу</option>
                <option value="steam">🎮 Steam</option>
                <option value="discord">💬 Discord</option>
                <option value="telegram">📱 Telegram</option>
                <option value="whatsapp">💚 WhatsApp</option>
                <option value="instagram">📸 Instagram</option>
                <option value="vk">🔵 VK</option>
                <option value="facebook">🔵 Facebook</option>
                <option value="twitter">🐦 Twitter/X</option>
                <option value="tiktok">🎵 TikTok</option>
                <option value="youtube">📺 YouTube</option>
                <option value="twitch">🎬 Twitch</option>
                <option value="genshin">⚔️ Genshin Impact</option>
                <option value="mobile">📱 Mobile Legends</option>
                <option value="wow">⚔️ World of Warcraft</option>
                <option value="league">🏆 League of Legends</option>
                <option value="dota">🎯 Dota 2</option>
                <option value="csgo">🔫 CS:GO/CS2</option>
                <option value="valorant">🎯 Valorant</option>
                <option value="fortnite">🔫 Fortnite</option>
                <option value="minecraft">⛏️ Minecraft</option>
                <option value="other">📌 Другое</option>
              </select>
            </div>
            <div class="form-group">
              <label>Название платформы</label>
              <input type="text" v-model="form.platform_name" class="form-input" placeholder="Например: Мой Steam аккаунт">
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label>Логин / Username</label>
              <input type="text" v-model="form.username" class="form-input" placeholder="Имя пользователя">
            </div>
            <div class="form-group">
              <label>Email</label>
              <input type="email" v-model="form.email" class="form-input" placeholder="email@example.com">
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label>Телефон</label>
              <input type="tel" v-model="form.phone" class="form-input" placeholder="+7 XXX XXX-XX-XX">
            </div>
            <div class="form-group">
              <label>Пароль</label>
              <input type="еуче" v-model="form.password" class="form-input" placeholder="Пароль от аккаунта">
            </div>
          </div>
        </div>

        <!-- ID и идентификаторы -->
        <div class="form-section">
          <h4>🆔 ID и идентификаторы</h4>
          <div class="form-row">
            <div class="form-group">
              <label>Account ID</label>
              <input type="text" v-model="form.account_id" class="form-input" placeholder="ID аккаунта">
            </div>
            <div class="form-group">
              <label>UID</label>
              <input type="text" v-model="form.uid" class="form-input" placeholder="User ID">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>User ID</label>
              <input type="text" v-model="form.user_id" class="form-input" placeholder="ID пользователя">
            </div>
            <div class="form-group">
              <label>Friend Code</label>
              <input type="text" v-model="form.friend_code" class="form-input" placeholder="Код друга">
            </div>
          </div>
        </div>

        <!-- Сервер и регион -->
        <div class="form-section">
          <h4>🌍 Сервер и регион</h4>
          <div class="form-row">
            <div class="form-group">
              <label>Server ID</label>
              <input type="text" v-model="form.server_id" class="form-input" placeholder="ID сервера">
            </div>
            <div class="form-group">
              <label>Server Name</label>
              <input type="text" v-model="form.server_name" class="form-input" placeholder="Название сервера">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Регион</label>
              <select v-model="form.region" class="form-input">
                <option value="">Выберите регион</option>
                <option value="EU">Европа (EU)</option>
                <option value="NA">Северная Америка (NA)</option>
                <option value="AS">Азия (AS)</option>
                <option value="RU">Россия (RU)</option>
                <option value="SA">Южная Америка (SA)</option>
                <option value="AU">Австралия (AU)</option>
                <option value="AF">Африка (AF)</option>
              </select>
            </div>
            <div class="form-group">
              <label>Сервер</label>
              <input type="text" v-model="form.server" class="form-input" placeholder="Название сервера">
            </div>
          </div>
        </div>

        <!-- Игровые данные -->
        <div class="form-section">
          <h4>🎮 Игровые данные</h4>
          <div class="form-row">
            <div class="form-group">
              <label>Никнейм</label>
              <input type="text" v-model="form.nickname" class="form-input" placeholder="Игровой ник">
            </div>
            <div class="form-group">
              <label>Уровень</label>
              <input type="number" v-model.number="form.level" class="form-input" placeholder="Уровень в игре">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Ранг</label>
              <input type="text" v-model="form.rank" class="form-input" placeholder="Ранг/звание">
            </div>
            <div class="form-group">
              <label>Гильдия / Клан</label>
              <input type="text" v-model="form.guild" class="form-input" placeholder="Название гильдии">
            </div>
          </div>
          <div class="form-group">
            <label>Персонажи</label>
            <textarea v-model="form.characters" rows="2" class="form-input" placeholder="Список персонажей через запятую"></textarea>
          </div>
        </div>

        <!-- Безопасность -->
        <div class="form-section">
          <h4>🔒 Безопасность</h4>
          <div class="form-group">
            <label>Резервные коды</label>
            <textarea v-model="form.backup_codes" rows="2" class="form-input" placeholder="Резервные коды для восстановления доступа"></textarea>
          </div>
          <div class="form-group">
            <label>Контрольные вопросы</label>
            <textarea v-model="form.security_questions" rows="2" class="form-input" placeholder="Вопросы и ответы для восстановления"></textarea>
          </div>
        </div>

        <!-- Заметки и статус -->
        <div class="form-section">
          <h4>📝 Заметки</h4>
          <div class="form-group">
            <label>Заметки</label>
            <textarea v-model="form.notes" rows="3" class="form-input" placeholder="Дополнительная информация об аккаунте"></textarea>
          </div>
          <div class="form-group checkbox-group">
            <label class="checkbox-label">
              <input type="checkbox" v-model="form.is_active" class="checkbox-input">
              <span>Аккаунт активен</span>
            </label>
          </div>
        </div>

      </form>
    </template>
    <template #footer>
      <button class="btn-secondary" @click="close">Отмена</button>
      <button type="submit" form="digitalAccountForm" class="btn-primary" :disabled="loading">
        {{ loading ? 'Сохранение...' : 'Сохранить' }}
      </button>
    </template>
  </BaseModal>
</template>

<script setup>
import { ref, reactive } from 'vue';
import BaseModal from '../common/BaseModal.vue';
import { digitalAccountsApi } from '@/api/endpoints/digital-accounts';
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
  platform_type: '',
  platform_name: '',
  username: '',
  email: '',
  phone: '',
  password: '',
  account_id: '',
  uid: '',
  user_id: '',
  friend_code: '',
  server_id: '',
  server_name: '',
  region: '',
  server: '',
  nickname: '',
  level: null,
  rank: '',
  guild: '',
  characters: '',
  backup_codes: '',
  security_questions: '',
  notes: '',
  is_active: true
});

// Функция очистки данных перед отправкой

const resetForm = () => {
  Object.keys(form).forEach(key => {
    if (key === 'is_active') form[key] = true;
    else if (key === 'level') form[key] = null;
    else form[key] = '';
  });
  isEdit.value = false;
  currentId.value = null;
};

const open = async (id = null) => {
  console.log('📂 Открытие DigitalAccountModal, id:', id);
  resetForm();
  
  if (id) {
    isEdit.value = true;
    currentId.value = id;
    try {
      const account = await digitalAccountsApi.getById(id);
      if (account) {
        fillForm(form, account);
        console.log('✅ Данные загружены:', account);
      } else {
        console.error('❌ Данные не найдены для ID:', id);
        toastError('Данные не найдены');
        return;
      }
    } catch (err) {
      console.error('❌ Ошибка загрузки:', err);
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
  if (!form.platform_type) {
    toastError('Выберите тип платформы');
    return;
  }
  
  loading.value = true;
  try {
    const data = toPayload({ ...form }, isEdit.value);
    if (isEdit.value && currentId.value) {
      await personStore.updateItem('digital_accounts', currentId.value, data);
      success('Аккаунт обновлен');
    } else {
      await personStore.createItem('digital_accounts', data);
      success('Аккаунт добавлен');
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
.digital-form { max-height: 70vh; overflow-y: auto; padding-right: 8px; }
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