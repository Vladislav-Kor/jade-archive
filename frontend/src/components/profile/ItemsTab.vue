<template>
  <div class="items-tab">
    <div class="tab-header">
      <h3>{{ title }}</h3>
      <button class="add-btn" @click="handleAdd">+ Добавить</button>
    </div>

    <div v-if="!items?.length" class="empty-block">
      <div class="empty-icon">{{ emptyIcon }}</div>
      <p>{{ emptyText }}</p>
      <button class="secondary-btn" @click="handleAdd">Добавить</button>
    </div>

    <div v-else class="items-list">
      <div v-for="item in items" :key="item.id" class="item-block">
        <div class="item-icon">{{ getItemIcon(item) }}</div>
        <div class="item-info">
          <div class="item-title">{{ getItemTitle(item) }}</div>
          <div class="item-meta">
            <span v-for="(value, key) in getItemMeta(item)" :key="key">{{ value }}</span>
          </div>
        </div>
        <div class="item-controls">
          <button class="edit-btn" @click="handleEdit(item.id)">✏️</button>
          <button class="delete-btn" @click="handleDelete(item.id)">🗑️</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  title: { type: String, required: true },
  items: { type: Array, default: () => [] },
  emptyIcon: { type: String, default: '📦' },
  emptyText: { type: String, default: 'Нет элементов' }
})

const emit = defineEmits(['add', 'edit', 'delete'])

const handleAdd = () => {
  emit('add')
}

const handleEdit = (id) => {
  emit('edit', id)
}

const handleDelete = (id) => {
  emit('delete', id)
}

const getItemIcon = (item) => {
  // Социальные сети
  if (item.platform) {
    const platform = item.platform.toLowerCase()
    const icons = {
      'telegram': '📱',
      'vk': '💙',
      'instagram': '📸',
      'youtube': '📺',
      'twitch': '🎬',
      'twitter': '🐦',
      'tiktok': '🎵',
      'github': '🐙',
      'steam': '🎮',
      'discord': '💬',
      'whatsapp': '💚',
      'facebook': '👍',
      'linkedin': '🔗',
      'pinterest': '📌',
      'reddit': '🤖',
      'snapchat': '👻'
    }
    return icons[platform] || '🌐'
  }
  
  // Недвижимость
  if (item.property_type) return '🏢'
  
  // Транспорт
  if (item.brand) return '🚗'
  
  // Цифровые аккаунты
  if (item.platform_type) return '🎮'
  
  // Дела
  if (item.case_type) return '📋'
  
  // Медицина
  if (item.record_type) return '🏥'
  
  return '📦'
}

const getItemTitle = (item) => {
  // Социальные сети - показываем платформу
  if (item.platform) {
    return item.platform
  }
  
  // Дела
  if (item.title) return item.title
  
  // Имя
  if (item.name) return item.name
  
  // Цифровые аккаунты
  if (item.platform_name) return item.platform_name
  
  // Недвижимость
  if (item.property_name) return item.property_name
  
  // Транспорт
  if (item.brand && item.model) return item.brand + ' ' + item.model
  if (item.brand) return item.brand
  
  return 'Элемент'
}

const getItemMeta = (item) => {
  const meta = []
  
  // Социальные сети - показываем ссылку
  if (item.platform && item.link) {
    // Укорачиваем ссылку для отображения
    let link = item.link
    if (link.length > 40) {
      link = link.substring(0, 40) + '...'
    }
    meta.push('🔗 ' + link)
  }
  
  // Недвижимость
  if (item.address) meta.push('📍 ' + item.address)
  if (item.total_area) meta.push('📐 ' + item.total_area + ' м²')
  if (item.rooms_count) meta.push('🚪 ' + item.rooms_count + ' комн')
  
  // Транспорт
  if (item.license_plate) meta.push('🔢 ' + item.license_plate)
  if (item.year) meta.push('📅 ' + item.year)
  if (item.color) meta.push('🎨 ' + item.color)
  if (item.horsepower) meta.push('⚡ ' + item.horsepower + ' л.с.')
  
  // Цифровые аккаунты
  if (item.username) meta.push('👤 ' + item.username)
  if (item.email) meta.push('✉️ ' + item.email)
  if (item.nickname) meta.push('🎮 ' + item.nickname)
  
  // Дела
  if (item.case_type) {
    const types = {
      'legal': '⚖️ Судебное',
      'work': '💼 Рабочее',
      'personal': '👤 Личное',
      'family': '👨‍👩‍👧 Семейное',
      'financial': '💰 Финансовое',
      'medical': '🏥 Медицинское',
      'education': '📚 Образовательное',
      'real_estate': '🏠 Недвижимость'
    }
    meta.push(types[item.case_type] || item.case_type)
  }
  if (item.status) meta.push('📌 ' + item.status)
  if (item.priority) meta.push('⭐ ' + item.priority)
  
  // Медицина
  if (item.record_type) {
    const types = {
      'diagnosis': '🩺 Диагноз',
      'examination': '🔬 Осмотр',
      'vaccination': '💉 Вакцинация',
      'analysis': '🧪 Анализ',
      'operation': '🏥 Операция',
      'hospitalization': '🏨 Госпитализация',
      'prescription': '💊 Рецепт',
      'allergy': '🤧 Аллергия',
      'chronic': '📋 Хроническое',
      'checkup': '📅 Осмотр'
    }
    meta.push(types[item.record_type] || item.record_type)
  }
  if (item.doctor_name) meta.push('👨‍⚕️ ' + item.doctor_name)
  if (item.record_date) {
    const date = new Date(item.record_date)
    meta.push('📅 ' + date.toLocaleDateString('ru-RU'))
  }
  
  return meta
}
</script>

<style scoped>
.items-tab {
  background: #0d1210;
  border-radius: 20px;
  padding: 20px;
  border: 1px solid #1a2420;
}
.tab-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid #1a2420;
}
.tab-header h3 { font-size: 16px; font-weight: 600; color: #ffd54f; }
.add-btn {
  padding: 6px 14px;
  background: #1a2420;
  border: 1px solid #2a3a35;
  border-radius: 20px;
  color: #00c49a;
  cursor: pointer;
  font-size: 12px;
}
.add-btn:hover { background: #00c49a20; }
.items-list { display: flex; flex-direction: column; gap: 12px; }
.item-block {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 16px;
  background: #1a2420;
  border-radius: 16px;
}
.item-icon { font-size: 32px; flex-shrink: 0; }
.item-info { flex: 1; }
.item-title { font-size: 15px; font-weight: 600; color: #fff; margin-bottom: 6px; }
.item-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  font-size: 11px;
  color: #5a6e68;
}
.item-controls { display: flex; gap: 8px; }
.edit-btn, .delete-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
}
.edit-btn { color: #5a6e68; }
.edit-btn:hover { color: #00c49a; }
.delete-btn { color: #5a6e68; }
.delete-btn:hover { color: #e55c5c; }
.empty-block {
  text-align: center;
  padding: 60px 20px;
  color: #5a6e68;
}
.empty-icon { font-size: 48px; margin-bottom: 16px; opacity: 0.5; }
.secondary-btn {
  margin-top: 16px;
  padding: 8px 20px;
  background: #1a2420;
  border: 1px solid #2a3a35;
  border-radius: 20px;
  color: #00c49a;
  cursor: pointer;
}
</style>