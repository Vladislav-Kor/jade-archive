<template>
  <div class="social-tab">
    <div class="tab-header">
      <h3>
        <span class="header-icon">🌐</span>
        Социальные сети
      </h3>
      <button class="add-btn" @click="$emit('add')">
        <span class="btn-icon">+</span>
        Добавить соцсеть
      </button>
    </div>

    <div v-if="!items?.length" class="empty-state">
      <div class="empty-animation">📱</div>
      <h4>Нет социальных сетей</h4>
      <p>Добавьте ссылки на профили в Telegram, VK, Instagram и других платформах</p>
      <button class="empty-add-btn" @click="$emit('add')">
        <span>+</span> Добавить соцсеть
      </button>
    </div>

    <div v-else class="social-grid">
      <div v-for="social in items" :key="social.id" class="social-card" :data-platform="getPlatformType(social.platform)">
        <div class="social-card-header">
          <div class="social-icon" :style="{ background: getPlatformColor(social.platform) }">
            <span class="platform-icon">{{ getPlatformIcon(social.platform) }}</span>
          </div>
          <div class="social-info">
            <div class="platform-name">{{ getPlatformDisplayName(social.platform) }}</div>
            <div class="social-handle">{{ getHandleFromUrl(social.link) }}</div>
          </div>
          <div class="social-actions">
            <button class="action-btn copy-btn" @click="copyLink(social.link)" title="Копировать ссылку">
              📋
            </button>
            <button class="action-btn delete-btn" @click="$emit('delete', social.id)" title="Удалить">
              🗑️
            </button>
          </div>
        </div>
        <div class="social-card-footer">
          <a :href="social.link" target="_blank" class="social-link" rel="noopener noreferrer">
            <span class="link-text">{{ truncateUrl(social.link, 40) }}</span>
            <span class="open-icon">🔗</span>
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useToast } from '@/composables/useToast';

const props = defineProps({
  items: { type: Array, default: () => [] }
});

const emit = defineEmits(['add', 'delete']);

const { success } = useToast();

// Определение платформы по названию
const getPlatformType = (platform) => {
  const p = platform?.toLowerCase() || '';
  if (p.includes('telegram')) return 'telegram';
  if (p.includes('vk') || p.includes('вк')) return 'vk';
  if (p.includes('instagram') || p.includes('inst')) return 'instagram';
  if (p.includes('youtube')) return 'youtube';
  if (p.includes('twitch')) return 'twitch';
  if (p.includes('twitter') || p.includes('x')) return 'twitter';
  if (p.includes('tiktok')) return 'tiktok';
  if (p.includes('github')) return 'github';
  if (p.includes('steam')) return 'steam';
  if (p.includes('discord')) return 'discord';
  if (p.includes('whatsapp')) return 'whatsapp';
  if (p.includes('facebook') || p.includes('fb')) return 'facebook';
  if (p.includes('linkedin')) return 'linkedin';
  if (p.includes('pinterest')) return 'pinterest';
  if (p.includes('reddit')) return 'reddit';
  if (p.includes('snapchat')) return 'snapchat';
  return 'default';
};

// Цвета для разных платформ
const getPlatformColor = (platform) => {
  const colors = {
    telegram: 'linear-gradient(135deg, #0088cc, #00a3e0)',
    vk: 'linear-gradient(135deg, #4c75a3, #2a4a7a)',
    instagram: 'linear-gradient(135deg, #feda77, #d62976, #962fbf, #4f5bd5)',
    youtube: 'linear-gradient(135deg, #ff0000, #cc0000)',
    twitch: 'linear-gradient(135deg, #9146ff, #772ce8)',
    twitter: 'linear-gradient(135deg, #1da1f2, #0d8de1)',
    tiktok: 'linear-gradient(135deg, #010101, #20d5ec, #fe2c55)',
    github: 'linear-gradient(135deg, #333, #24292e)',
    steam: 'linear-gradient(135deg, #171a21, #2a475e)',
    discord: 'linear-gradient(135deg, #5865f2, #4752c4)',
    whatsapp: 'linear-gradient(135deg, #25d366, #128c7e)',
    facebook: 'linear-gradient(135deg, #1877f2, #0d65d4)',
    linkedin: 'linear-gradient(135deg, #0077b5, #005e8c)',
    pinterest: 'linear-gradient(135deg, #bd081c, #9a0616)',
    reddit: 'linear-gradient(135deg, #ff4500, #cc3700)',
    snapchat: 'linear-gradient(135deg, #fffc00, #e6e200)',
    default: 'linear-gradient(135deg, #2a3a35, #1a2420)'
  };
  return colors[getPlatformType(platform)] || colors.default;
};

// Иконки для разных платформ
const getPlatformIcon = (platform) => {
  const icons = {
    telegram: '📱',
    vk: '💙',
    instagram: '📸',
    youtube: '📺',
    twitch: '🎬',
    twitter: '🐦',
    tiktok: '🎵',
    github: '🐙',
    steam: '🎮',
    discord: '💬',
    whatsapp: '💚',
    facebook: '👍',
    linkedin: '🔗',
    pinterest: '📌',
    reddit: '🤖',
    snapchat: '👻',
    default: '🌐'
  };
  return icons[getPlatformType(platform)] || icons.default;
};

// Отображаемое имя платформы
const getPlatformDisplayName = (platform) => {
  if (!platform) return 'Соцсеть';
  const p = platform.toLowerCase();
  if (p.includes('telegram')) return 'Telegram';
  if (p.includes('vk') || p.includes('вк')) return 'VKontakte';
  if (p.includes('instagram')) return 'Instagram';
  if (p.includes('youtube')) return 'YouTube';
  if (p.includes('twitch')) return 'Twitch';
  if (p.includes('twitter')) return 'Twitter/X';
  if (p.includes('tiktok')) return 'TikTok';
  if (p.includes('github')) return 'GitHub';
  if (p.includes('steam')) return 'Steam';
  if (p.includes('discord')) return 'Discord';
  if (p.includes('whatsapp')) return 'WhatsApp';
  if (p.includes('facebook')) return 'Facebook';
  if (p.includes('linkedin')) return 'LinkedIn';
  if (p.includes('pinterest')) return 'Pinterest';
  if (p.includes('reddit')) return 'Reddit';
  if (p.includes('snapchat')) return 'Snapchat';
  return platform.charAt(0).toUpperCase() + platform.slice(1);
};

// Извлечение имени пользователя из ссылки
const getHandleFromUrl = (url) => {
  if (!url) return '';
  try {
    // Убираем https:// и trailing slash
    let clean = url.replace(/^https?:\/\//, '').replace(/\/$/, '');
    // Разбиваем на части
    const parts = clean.split('/');
    // Берем последнюю часть или домен
    let handle = parts[parts.length - 1] || parts[0];
    // Для Telegram из t.me/username
    if (clean.includes('t.me/')) {
      handle = '@' + handle;
    }
    // Для VK
    if (clean.includes('vk.com/')) {
      handle = handle;
    }
    // Ограничиваем длину
    if (handle.length > 25) {
      handle = handle.substring(0, 22) + '...';
    }
    return handle;
  } catch {
    return url;
  }
};

// Сокращение URL для отображения
const truncateUrl = (url, length) => {
  if (!url) return '';
  if (url.length <= length) return url;
  return url.substring(0, length) + '...';
};

// Копирование ссылки в буфер обмена
const copyLink = async (link) => {
  try {
    await navigator.clipboard.writeText(link);
    success('Ссылка скопирована!');
  } catch (err) {
    console.error('Failed to copy:', err);
  }
};
</script>

<style scoped>
.social-tab {
  background: #0d1210;
  border-radius: 20px;
  padding: 24px;
  border: 1px solid #1a2420;
}

.tab-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #1a2420;
}

.tab-header h3 {
  font-size: 18px;
  font-weight: 600;
  color: #ffd54f;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 10px;
}

.header-icon {
  font-size: 24px;
}

.add-btn {
  padding: 8px 20px;
  background: linear-gradient(135deg, #00d4a8, #00a884);
  border: none;
  border-radius: 12px;
  color: #0a0e0c;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
  font-size: 14px;
}

.add-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 212, 168, 0.3);
}

.btn-icon {
  font-size: 18px;
}

/* Grid Layout */
.social-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 16px;
}

/* Social Card */
.social-card {
  background: linear-gradient(135deg, rgba(26, 36, 32, 0.8), rgba(13, 18, 16, 0.9));
  border-radius: 16px;
  border: 1px solid rgba(0, 212, 168, 0.1);
  overflow: hidden;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.social-card:hover {
  transform: translateY(-4px);
  border-color: rgba(0, 212, 168, 0.3);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

.social-card-header {
  display: flex;
  align-items: center;
  padding: 16px;
  gap: 14px;
  position: relative;
}

.social-icon {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.platform-icon {
  font-size: 26px;
}

.social-info {
  flex: 1;
  min-width: 0;
}

.platform-name {
  font-size: 15px;
  font-weight: 600;
  color: #fff;
  margin-bottom: 4px;
}

.social-handle {
  font-size: 12px;
  color: #5a6e68;
  font-family: monospace;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.social-actions {
  display: flex;
  gap: 8px;
  opacity: 0.6;
  transition: opacity 0.2s;
}

.social-card:hover .social-actions {
  opacity: 1;
}

.action-btn {
  width: 32px;
  height: 32px;
  background: rgba(0, 212, 168, 0.1);
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-btn:hover {
  transform: scale(1.05);
  background: rgba(0, 212, 168, 0.2);
}

.copy-btn:hover {
  background: rgba(255, 213, 79, 0.2);
}

.delete-btn:hover {
  background: rgba(229, 92, 92, 0.2);
}

.social-card-footer {
  padding: 12px 16px;
  border-top: 1px solid rgba(0, 212, 168, 0.08);
  background: rgba(0, 0, 0, 0.2);
}

.social-link {
  display: flex;
  align-items: center;
  justify-content: space-between;
  text-decoration: none;
  color: #00c49a;
  font-size: 12px;
  transition: all 0.2s;
}

.social-link:hover {
  color: #ffd54f;
}

.link-text {
  font-family: monospace;
  word-break: break-all;
}

.open-icon {
  font-size: 12px;
  opacity: 0.6;
  transition: all 0.2s;
}

.social-link:hover .open-icon {
  opacity: 1;
  transform: translateX(3px);
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.empty-animation {
  font-size: 64px;
  margin-bottom: 20px;
  opacity: 0.6;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.empty-state h4 {
  font-size: 18px;
  color: #fff;
  margin-bottom: 8px;
}

.empty-state p {
  font-size: 13px;
  color: #5a6e68;
  margin-bottom: 24px;
}

.empty-add-btn {
  padding: 10px 24px;
  background: linear-gradient(135deg, #00d4a8, #00a884);
  border: none;
  border-radius: 12px;
  color: #0a0e0c;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
}

.empty-add-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 212, 168, 0.3);
}

/* Responsive */
@media (max-width: 768px) {
  .social-tab {
    padding: 16px;
  }
  
  .social-grid {
    grid-template-columns: 1fr;
  }
  
  .social-card-header {
    flex-wrap: wrap;
  }
  
  .social-actions {
    opacity: 1;
  }
}
</style>
