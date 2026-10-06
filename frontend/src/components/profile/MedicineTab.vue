<template>
  <div class="tab-container">
    <div class="tab-header">
      <h2>🏥 Медицина</h2>
      <button class="add-btn" @click="handleAdd">➕ Добавить</button>
    </div>
    
    <div v-if="!records || records.length === 0" class="empty-state">
      <p>Нет медицинских записей</p>
      <p class="empty-hint">Добавьте записи о болезнях, лекарствах или осмотрах</p>
    </div>
    
    <div v-else class="records-grid">
      <div v-for="record in records" :key="record.id" class="record-card">
        <div class="record-header">
          <span class="record-title">{{ record.title }}</span>
          <span class="record-type">{{ record.record_type }}</span>
          <span v-if="record.status" class="record-status" :class="record.status">
            {{ record.status }}
          </span>
          <div class="record-actions">
            <button class="edit-btn" @click="handleEdit(record.id)">✏️</button>
            <button class="delete-btn" @click="handleDelete(record.id)">🗑️</button>
          </div>
        </div>
        <div class="record-body">
          <p v-if="record.description" class="record-description">{{ record.description }}</p>
          <div v-if="record.data" class="record-data">
            <div v-for="(value, key) in record.data" :key="key" class="data-item">
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

const records = computed(() => {
  return props.person?.cross_records?.filter(r => 
    r.primary_category_id === 1 || 
    r.secondary_categories?.includes(1)
  ) || []
})

const handleAdd = () => emit('add')
const handleEdit = (id) => emit('edit', id)
const handleDelete = (id) => emit('delete', id)
</script>

<style scoped>
.tab-container { padding: 20px; }
.tab-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.tab-header h2 { margin: 0; color: #00c49a; }
.add-btn { padding: 8px 16px; background: #00c49a; border: none; border-radius: 8px; color: #0a0e0c; cursor: pointer; font-weight: 600; }
.add-btn:hover { background: #00d4a8; }
.empty-state { text-align: center; padding: 40px; color: #5a6e68; }
.empty-hint { font-size: 14px; margin-top: 8px; opacity: 0.7; }
.records-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 16px; }
.record-card { background: #0d1210; border: 1px solid #1a2420; border-radius: 12px; padding: 16px; }
.record-header { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-bottom: 12px; }
.record-title { font-weight: 600; color: #fff; flex: 1; }
.record-type { font-size: 11px; color: #00c49a; background: #00c49a15; padding: 2px 8px; border-radius: 12px; }
.record-status { font-size: 11px; padding: 2px 8px; border-radius: 12px; }
.record-status.active { background: #00c49a20; color: #00c49a; }
.record-status.completed { background: #3498db20; color: #3498db; }
.record-status.archived { background: #5a6e6820; color: #5a6e68; }
.record-actions { display: flex; gap: 8px; }
.edit-btn, .delete-btn { background: none; border: none; cursor: pointer; font-size: 16px; padding: 4px 8px; border-radius: 4px; }
.edit-btn:hover { background: #1a2420; }
.delete-btn:hover { background: #2a1a1a; }
.record-description { color: #5a6e68; margin: 0 0 8px 0; }
.record-data { display: grid; grid-template-columns: 1fr 1fr; gap: 4px 16px; font-size: 13px; }
.data-key { color: #3a4e48; }
.data-value { color: #7a8e88; }
</style>
