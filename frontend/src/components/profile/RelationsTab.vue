<template>
  <div class="relations-tab">
    <div class="tab-header">
      <h3>Связи</h3>
      <button class="add-btn" @click="handleAdd">+ Добавить связь</button>
    </div>

    <div v-if="outgoingRelations.length === 0 && incomingRelations.length === 0" class="empty-block">
      <div class="empty-icon">🔗</div>
      <p>Нет связей</p>
      <button class="secondary-btn" @click="handleAdd">Создать связь</button>
    </div>

    <div v-if="outgoingRelations.length" class="relations-group">
      <div class="group-title">📤 Исходящие</div>
      <RelationItem
        v-for="rel in outgoingRelations"
        :key="rel.id"
        :relation="rel"
        direction="outgoing"
        @delete="handleDelete(rel.id)"
        @click="handleSelectPerson(rel.person_id)"
      />
    </div>

    <div v-if="incomingRelations.length" class="relations-group">
      <div class="group-title">📥 Входящие</div>
      <RelationItem
        v-for="rel in incomingRelations"
        :key="rel.id"
        :relation="rel"
        direction="incoming"
        @delete="handleDelete(rel.id)"
        @click="handleSelectPerson(rel.person_id)"
      />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import RelationItem from './RelationItem.vue'

const props = defineProps({
  person: { type: Object, required: true }
})

const emit = defineEmits(['add', 'delete', 'selectPerson'])

const outgoingRelations = computed(() =>
  (props.person.relations || []).filter(r => r.direction === 'outgoing')
)

const incomingRelations = computed(() =>
  (props.person.relations || []).filter(r => r.direction === 'incoming')
)

const handleAdd = () => {
  emit('add')
}

const handleDelete = (id) => {
  emit('delete', id)
}

const handleSelectPerson = (id) => {
  emit('selectPerson', id)
}
</script>

<style scoped>
.relations-tab {
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
.relations-group { margin-bottom: 24px; }
.group-title {
  font-size: 11px;
  font-weight: 600;
  color: #00c49a;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 12px;
}
</style>
