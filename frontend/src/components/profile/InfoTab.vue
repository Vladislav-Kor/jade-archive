<template>
  <div class="info-tab">
    <div class="info-row">
      <InfoCard 
        v-for="field in infoFields" 
        :key="field.label" 
        :field="field" 
        :value="getFieldValue(field.key)" 
      />
    </div>
    <NotesCard v-if="person?.notes" :notes="person.notes" />
  </div>
</template>

<script setup>
import InfoCard from './InfoCard.vue'
import NotesCard from './NotesCard.vue'

const props = defineProps({
  person: { type: Object, required: true }
})

const infoFields = [
  { key: 'phone', label: 'Телефон', icon: '📞' },
  { key: 'email', label: 'Email', icon: '✉️' },
  { key: 'address', label: 'Адрес', icon: '📍', fullWidth: true },
  { key: 'birth_date', label: 'Дата рождения', icon: '🎂' },
  { key: 'gender', label: 'Пол', icon: '🚻' },
  { key: 'marital_status', label: 'Семейное положение', icon: '💑' },
  { key: 'children_count', label: 'Детей', icon: '👶' },
  { key: 'height', label: 'Рост', icon: '📏' },
  { key: 'weight', label: 'Вес', icon: '⚖️' },
  { key: 'clothing_size', label: 'Размер одежды', icon: '👕' },
  { key: 'shoe_size', label: 'Размер обуви', icon: '👟' },
  { key: 'blood_type', label: 'Группа крови', icon: '🩸' },
  { key: 'allergies', label: 'Аллергии', icon: '🤧', fullWidth: true },
  { key: 'chronic_diseases', label: 'Хронические заболевания', icon: '🏥', fullWidth: true },
  { key: 'profession', label: 'Профессия', icon: '💼', fullWidth: true },
  { key: 'workplace', label: 'Место работы', icon: '🏢', fullWidth: true },
  { key: 'favorite_color', label: 'Любимый цвет', icon: '🎨' },
  { key: 'favorite_food', label: 'Любимая еда', icon: '🍕' },
  { key: 'favorite_music', label: 'Любимая музыка', icon: '🎵' },
  { key: 'hobbies', label: 'Хобби', icon: '🎯', fullWidth: true }
]

const getFieldValue = (key) => {
  const value = props.person[key]
  if (key === 'birth_date') {
    return value ? new Date(value).toLocaleDateString('ru-RU') : '—'
  }
  if (key === 'gender') {
    return value === 'male' ? 'Мужской' : value === 'female' ? 'Женский' : '—'
  }
  if (key === 'marital_status') {
    const labels = {
      single: 'Холост/Не замужем',
      married: 'Женат/Замужем',
      divorced: 'Разведен(а)',
      widowed: 'Вдовец/Вдова'
    }
    return labels[value] || '—'
  }
  return value || '—'
}
</script>

<style scoped>
.info-tab {
  background: #0d1210;
  border-radius: 20px;
  padding: 20px;
  border: 1px solid #1a2420;
}
.info-row {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 16px;
  margin-bottom: 16px;
}
</style>
