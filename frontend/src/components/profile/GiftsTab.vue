<template>
  <div class="tab-container">
    <div class="tab-header">
      <h2>🎁 Подарки</h2>
      <button class="add-btn" @click="handleAdd">➕ Добавить</button>
    </div>
    
    <div v-if="!items || items.length === 0" class="empty-state">
      <p>Нет записей в разделе "Подарки"</p>
      <p class="empty-hint">Нажмите "Добавить" чтобы создать первую запись</p>
    </div>
    
    <div v-else class="items-grid">
      <div v-for="item in items" :key="item.id" class="item-card">
        <div class="item-header">
          <span class="item-title">{{ item.title || 'Без названия' }}</span>
          <span v-if="item.record_type" class="item-type">{{ item.record_type }}</span>
          <span v-if="item.status" class="item-status" :class="item.status">
            {{ item.status }}
          </span>
          <div class="item-actions">
            <button class="edit-btn" @click="handleEdit(item.id)">✏️</button>
            <button class="delete-btn" @click="handleDelete(item.id)">🗑️</button>
          </div>
        </div>
        <div class="item-body">
          <p v-if="item.description" class="item-description">{{ item.description }}</p>
          <div v-if="item.data" class="item-data">
            <div v-for="(value, key) in item.data" :key="key" class="data-item">
              <span class="data-key">{{ key }}:</span>
              <span class="data-value">{{ value }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  person: { type: Object, required: true }
})

const emit = defineEmits(['add', 'edit', 'delete'])

const items = computed(() => {
  return props.person?.cross_records?.filter(r => 
    r.primary_category_id === 4 || 
    r.secondary_categories?.includes(4)
  ) || []
})

const handleAdd = () => emit('add')
const handleEdit = (id) => emit('edit', id)
const handleDelete = (id) => emit('delete', id)
</script>

<style scoped>
.tab-container { padding: 20px; }
.tab-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.tab-header h2 { margin: 0; color: #00c49a; font-size: 20px; }
.add-btn { padding: 8px 16px; background: #00c49a; border: none; border-radius: 8px; color: #0a0e0c; cursor: pointer; font-weight: 600; transition: all 0.2s; }
.add-btn:hover { background: #00d4a8; transform: scale(1.02); }
.empty-state { text-align: center; padding: 60px 20px; color: #5a6e68; }
.empty-hint { font-size: 14px; margin-top: 8px; opacity: 0.7; }
.items-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 16px; }
.item-card { background: #0d1210; border: 1px solid #1a2420; border-radius: 12px; padding: 16px; transition: all 0.2s; }
.item-card:hover { border-color: #2a3a35; }
.item-header { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-bottom: 12px; }
.item-title { font-weight: 600; color: #fff; flex: 1; font-size: 15px; }
.item-type { font-size: 11px; color: #00c49a; background: #00c49a15; padding: 2px 10px; border-radius: 12px; }
.item-status { font-size: 11px; padding: 2px 10px; border-radius: 12px; font-weight: 500; }
.item-status.active { background: #00c49a20; color: #00c49a; }
.item-status.completed { background: #3498db20; color: #3498db; }
.item-status.archived { background: #5a6e6820; color: #5a6e68; }
.item-status.planned { background: #f39c1220; color: #f39c12; }
.item-actions { display: flex; gap: 4px; }
.edit-btn, .delete-btn { background: none; border: none; cursor: pointer; font-size: 16px; padding: 4px 8px; border-radius: 4px; transition: all 0.2s; }
.edit-btn:hover { background: #1a2420; }
.delete-btn:hover { background: #2a1a1a; }
.item-description { color: #5a6e68; margin: 0 0 8px 0; font-size: 14px; }
.item-data { display: grid; grid-template-columns: 1fr 1fr; gap: 4px 16px; font-size: 13px; margin-top: 8px; padding-top: 8px; border-top: 1px solid #1a2420; }
.data-key { color: #3a4e48; }
.data-value { color: #7a8e88; }
</style>
