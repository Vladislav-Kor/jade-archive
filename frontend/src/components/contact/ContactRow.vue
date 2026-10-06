<template>
  <div class="contact-row" :class="{ active: isActive }" @click="$emit('select')">
    <div class="contact-avatar">
      <span class="avatar-text">{{ getInitials(person.full_name) }}</span>
      <span class="contact-rank" :style="{ background: getRankColor(person.importance) }}">
        {{ person.importance || 0 }}
      </span>
    </div>
    <div class="contact-details">
      <div class="contact-name">{{ person.full_name }}</div>
      <div class="contact-nick">@{{ person.short_name }}</div>
    </div>
    <div class="contact-actions">
      <button class="contact-action" @click.stop="$emit('addRelation')" title="Добавить связь">🔗</button>
      <button class="contact-action" @click.stop="$emit('edit')" title="Редактировать">✏️</button>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  person: { type: Object, required: true },
  isActive: { type: Boolean, default: false }
})

const emit = defineEmits(['select', 'edit', 'addRelation'])

const getInitials = (name) => {
  if (!name) return '?'
  return name.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase()
}

const getRankColor = (importance) => {
  if (!importance || importance === 0) return '#2e7d64'
  if (importance >= 8) return '#e55c5c'
  if (importance >= 6) return '#e5a03c'
  if (importance >= 4) return '#e5c53c'
  return '#2e7d64'
}
</script>

<style scoped src="@/styles/components/ContactRow.css"></style>
