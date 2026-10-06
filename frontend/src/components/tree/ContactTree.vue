<template>
  <div class="tree-container">
    <div class="tree-header">
      <Icon name="menu" size="sm" color="#6eafa2" />
      <span>Структура контактов</span>
      <button class="tree-refresh" @click="$emit('refresh')" title="Обновить">
        <Icon name="refresh" size="sm" :spin="isLoading" />
      </button>
    </div>
    
    <div class="tree-wrapper">
      <div v-if="isLoading" class="loading">
        <div class="skeleton" v-for="i in 5" :key="i"></div>
      </div>
      
      <div v-else-if="error" class="error-state">
        <Icon name="alert" size="lg" color="#ff6b6b" />
        <p>{{ error }}</p>
        <button class="btn-sm" @click="$emit('refresh')">Повторить</button>
      </div>
      
      <div v-else-if="!persons || persons.length === 0" class="empty-state">
        <Icon name="users" size="lg" color="#6eafa2" />
        <p>Нет контактов</p>
        <button class="btn-sm" @click="$emit('addPerson')">
          <Icon name="plus" size="sm" /> Добавить
        </button>
      </div>
      
      <div v-else class="tree-list">
        <div 
          v-for="person in persons" 
          :key="person.id"
          class="tree-node"
          :class="{ selected: selectedId === person.id }"
        >
          <div class="folder-tab" @click="$emit('select', person.id)">
            <div class="folder-icon">
              <Icon name="person" size="sm" :color="selectedId === person.id ? '#ffd54f' : '#00d4a8'" />
            </div>
            <div class="folder-badge" :style="{ background: getImportanceColor(person.importance) }">
              {{ person.importance || 0 }}
            </div>
            <div class="folder-name">
              {{ person.full_name }}
              <span class="text-xs">@{{ person.short_name }}</span>
            </div>
            <div class="folder-actions">
              <button class="action-btn" @click.stop="$emit('addRelation', person.id)" title="Связь">
                <Icon name="link" size="sm" />
              </button>
              <button class="action-btn" @click.stop="$emit('editPerson', person.id)" title="Редактировать">
                <Icon name="edit" size="sm" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import Icon from '@/components/common/Icon.vue';

const props = defineProps({
  persons: { type: Array, default: () => [] },
  isLoading: { type: Boolean, default: false },
  error: { type: String, default: null },
  selectedId: { type: Number, default: null }
});

const emit = defineEmits([
  'select', 'refresh', 'addRelation', 'editPerson', 'addPerson'
]);

const getImportanceColor = (importance) => {
  if (!importance) return '#00a884';
  if (importance >= 8) return '#ff6b6b';
  if (importance >= 6) return '#ff9f43';
  if (importance >= 4) return '#ffd93d';
  return '#00a884';
};
</script>

<style scoped>
.tree-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.tree-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: rgba(0, 200, 155, 0.05);
  border-bottom: 1px solid rgba(0, 200, 155, 0.1);
  font-size: 11px;
  font-weight: 600;
  color: #6eafa2;
}

.tree-header span {
  flex: 1;
  margin-left: 8px;
}

.tree-refresh {
  background: rgba(0, 200, 155, 0.1);
  border: none;
  width: 28px;
  height: 28px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tree-refresh:hover {
  background: rgba(0, 212, 168, 0.2);
  transform: rotate(180deg);
}

.tree-wrapper {
  flex: 1;
  overflow-y: auto;
  padding: 12px;
}

.tree-node {
  margin-bottom: 6px;
}

.folder-tab {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  background: linear-gradient(135deg, rgba(0, 50, 45, 0.4), rgba(0, 30, 27, 0.4));
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid rgba(0, 200, 155, 0.08);
}

.folder-tab:hover {
  background: rgba(0, 212, 168, 0.12);
  transform: translateX(4px);
}

.tree-node.selected .folder-tab {
  background: rgba(0, 212, 168, 0.18);
  border-left: 3px solid #ffd54f;
}

.folder-icon {
  flex-shrink: 0;
}

.folder-badge {
  padding: 2px 6px;
  border-radius: 20px;
  font-size: 10px;
  font-weight: 700;
  color: #1a1a1a;
  min-width: 24px;
  text-align: center;
}

.folder-name {
  flex: 1;
  font-size: 13px;
  font-weight: 600;
  color: #d4ede8;
}

.text-xs {
  font-size: 10px;
  color: #6eafa2;
  margin-left: 6px;
}

.folder-actions {
  display: flex;
  gap: 4px;
  opacity: 0;
  transition: opacity 0.2s;
}

.folder-tab:hover .folder-actions {
  opacity: 1;
}

.action-btn {
  background: rgba(0, 200, 155, 0.12);
  border: none;
  width: 28px;
  height: 28px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.action-btn:hover {
  background: rgba(0, 212, 168, 0.25);
  transform: scale(1.05);
}

.skeleton {
  height: 48px;
  background: linear-gradient(90deg, rgba(0,212,168,0.05) 25%, rgba(0,212,168,0.1) 50%, rgba(0,212,168,0.05) 75%);
  background-size: 1000px 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 12px;
  margin-bottom: 8px;
}

@keyframes shimmer {
  0% { background-position: -1000px 0; }
  100% { background-position: 1000px 0; }
}

.loading, .error-state, .empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #6eafa2;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.btn-sm {
  padding: 6px 16px;
  font-size: 12px;
  background: linear-gradient(135deg, #00d4a8, #00a884);
  border: none;
  border-radius: 8px;
  color: #0a0f0e;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}
</style>