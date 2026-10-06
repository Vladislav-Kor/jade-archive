<template>
  <div class="tab-container">
    <div class="tab-header">
      <h3>📱 Устройства</h3>
      <button class="add-btn" @click="handleAdd">➕ Добавить</button>
    </div>
    
    <div v-if="!devices || devices.length === 0" class="empty-state">
      <p>Нет устройств</p>
    </div>
    
    <div v-else class="items-grid">
      <div v-for="item in devices" :key="item.id" class="item-card">
        <div class="item-icon">{{ getDeviceIcon(item.device_type) }}</div>
        <div class="item-info">
          <div class="item-title">{{ item.brand }} {{ item.model }}</div>
          <div class="item-subtitle">{{ item.device_type }}</div>
          <div class="item-meta">
            <span v-if="item.color">{{ item.color }}</span>
            <span v-if="item.imei">IMEI: {{ item.imei }}</span>
          </div>
        </div>
        <div class="item-actions">
          <button class="edit-btn" @click="handleEdit(item.id)">✏️</button>
          <button class="delete-btn" @click="handleDelete(item.id)">🗑️</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  devices: Array,
  person: Object
})

const emit = defineEmits(['add', 'edit', 'delete'])

// Явные обработчики с логами
const handleAdd = () => {
  console.log('🖱️ DevicesTab: Клик по кнопке ДОБАВИТЬ')
  emit('add')
}

const handleEdit = (id) => {
  console.log('🖱️ DevicesTab: Клик по EDIT, id:', id)
  emit('edit', id)
}

const handleDelete = (id) => {
  console.log('🖱️ DevicesTab: Клик по DELETE, id:', id)
  emit('delete', id)
}

const getDeviceIcon = (type) => {
  const icons = {
    phone: '📱',
    tablet: '📱',
    laptop: '💻',
    desktop: '🖥️',
    headphones: '🎧',
    smartwatch: '⌚',
    camera: '📷',
    console: '🎮',
    other: '📟'
  }
  return icons[type] || '📟'
}
</script>

<style scoped>
.tab-container {
  padding: 16px 0;
}
.tab-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
.tab-header h3 {
  color: #fff;
  font-size: 16px;
  margin: 0;
}
.add-btn {
  padding: 6px 16px;
  background: #00c49a;
  border: none;
  border-radius: 8px;
  color: #0a0e0c;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
}
.add-btn:hover {
  background: #00d6a8;
  transform: scale(1.02);
}
.add-btn:active {
  transform: scale(0.98);
}
.empty-state {
  padding: 40px;
  text-align: center;
  color: #5a6e68;
}
.items-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 12px;
}
.item-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: #0d1210;
  border: 1px solid #1a2420;
  border-radius: 12px;
  transition: border-color 0.2s;
}
.item-card:hover {
  border-color: #2a3a35;
}
.item-icon {
  font-size: 28px;
}
.item-info {
  flex: 1;
}
.item-title {
  color: #fff;
  font-weight: 500;
}
.item-subtitle {
  color: #5a6e68;
  font-size: 13px;
}
.item-meta {
  color: #3a4e48;
  font-size: 12px;
  margin-top: 4px;
}
.item-actions {
  display: flex;
  gap: 8px;
}
.edit-btn, .delete-btn {
  padding: 4px 10px;
  background: #1a2420;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}
.edit-btn:hover { 
  background: #2a3a35; 
  color: #00c49a;
}
.delete-btn:hover { 
  background: #2a1a1a; 
  color: #e55c5c;
}
</style>
