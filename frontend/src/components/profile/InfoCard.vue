<template>
  <div class="info-card" :class="{ 'full-width': field.fullWidth }">
    <div class="info-card-icon">{{ field.icon }}</div>
    <div class="info-card-content">
      <div class="info-card-label">{{ field.label }}</div>
      <div class="info-card-value">{{ value }}</div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  field: { type: Object, required: true },
  value: { required: true }
})
</script>

<style scoped>
.info-card {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 16px;
  background: #0d1210;
  border-radius: 16px;
  border: 1px solid #1a2420;
}
.info-card.full-width { grid-column: span 2; }
.info-card-icon { font-size: 24px; }
.info-card-content { flex: 1; }
.info-card-label {
  font-size: 11px;
  color: #5a6e68;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 4px;
}
.info-card-value {
  font-size: 14px;
  color: #fff;
  word-break: break-word;
}
</style>
