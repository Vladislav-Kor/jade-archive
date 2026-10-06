<template>
  <ItemsTab 
    title="Транспорт" 
    :items="items" 
    empty-icon="🚗" 
    empty-text="Нет транспортных средств"
    @add="handleAdd"
    @edit="handleEdit"
    @delete="handleDelete"
  />
</template>

<script setup>
import { computed } from 'vue'
import ItemsTab from './ItemsTab.vue'

const props = defineProps({ person: { type: Object, required: true } })
const emit = defineEmits(['add', 'edit', 'delete'])

const items = computed(() => props.person.vehicles || [])

const handleAdd = () => emit('add')
const handleEdit = (id) => emit('edit', id)
const handleDelete = (id) => emit('delete', id)
</script>
