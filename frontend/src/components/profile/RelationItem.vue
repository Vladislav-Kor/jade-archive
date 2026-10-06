<template>
  <div class="relation-item">
    <div class="relation-info">
      <span class="relation-arrow">{{ direction === 'outgoing' ? '→' : '←' }}</span>
      <span class="relation-name" @click="handleClick">{{ relation.person_name }}</span>
      <span class="relation-type">{{ relation.relation_type }}</span>
    </div>
    <button class="delete-btn" @click="handleDelete">🗑️</button>
  </div>
</template>

<script setup>
const props = defineProps({
  relation: { type: Object, required: true },
  direction: { type: String, required: true }
})

const emit = defineEmits(['delete', 'click'])

const handleClick = () => {
  emit('click')
}

const handleDelete = () => {
  emit('delete')
}
</script>

<style scoped>
.relation-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: #1a2420;
  border-radius: 12px;
  margin-bottom: 8px;
}
.relation-info { display: flex; align-items: center; gap: 12px; }
.relation-arrow { color: #00c49a; font-size: 14px; }
.relation-name {
  cursor: pointer;
  color: #00c49a;
  font-size: 14px;
  font-weight: 500;
}
.relation-name:hover { text-decoration: underline; }
.relation-type {
  font-size: 11px;
  padding: 2px 8px;
  background: #00c49a20;
  border-radius: 12px;
  color: #00c49a;
}
.delete-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  color: #5a6e68;
}
.delete-btn:hover { color: #e55c5c; }
</style>
