<template>
  <div class="items-tab">
    <div class="tab-header">
      <h3>{{ title }}</h3>
      <button class="add-btn" @click="$emit('add')">+ Добавить</button>
    </div>

    <div v-if="!items?.length" class="empty-block">
      <div class="empty-icon">{{ emptyIcon }}</div>
      <p>{{ emptyText }}</p>
      <button class="secondary-btn" @click="$emit('add')">Добавить</button>
    </div>

    <div v-else class="items-list">
      <slot :items="items"></slot>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, required: true },
  items: { type: Array, default: () => [] },
  emptyIcon: { type: String, default: '📦' },
  emptyText: { type: String, default: 'Нет элементов' }
})

defineEmits(['add'])
</script>

<style scoped src="@/styles/components/ItemsList.css"></style>
