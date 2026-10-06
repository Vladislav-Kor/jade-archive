<template>
  <ItemsTab 
    title="Социальные сети" 
    :items="items" 
    empty-icon="🌐" 
    empty-text="Нет социальных сетей"
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

// Убеждаемся что social_media - это массив
const items = computed(() => {
  const social = props.person?.social_media || []
  console.log('📱 SocialMediaTab items:', social)
  return social
})

const handleAdd = () => emit('add')
const handleEdit = (id) => emit('edit', id)
const handleDelete = (id) => emit('delete', id)
</script>