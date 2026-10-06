<template>
    <div class="cross-records-tab">
        <div class="tab-header">
            <h3>📝 Записи</h3>
            <button class="btn-add" @click="emit('add')">➕ Добавить запись</button>
        </div>
        
        <div v-if="!records || records.length === 0" class="empty-state">
            <div class="empty-icon">📝</div>
            <p>Нет записей</p>
            <button class="btn-primary" @click="emit('add')">Создать первую запись</button>
        </div>
        
        <div v-else class="records-grid">
            <div v-for="record in sortedRecords" :key="record.id" class="record-card">
                <div class="record-header">
                    <span class="record-type">{{ getRecordTypeLabel(record.record_type) }}</span>
                    <span class="record-status" :class="record.status">{{ record.status }}</span>
                </div>
                
                <h4 class="record-title">{{ record.title }}</h4>
                
                <p v-if="record.description" class="record-description">
                    {{ truncateText(record.description, 100) }}
                </p>
                
                <div class="record-meta">
                    <span class="record-date" v-if="record.record_date">
                        📅 {{ formatDate(record.record_date) }}
                    </span>
                    <span class="record-importance" :class="getImportanceClass(record.importance)">
                        ⭐ {{ record.importance || 0 }}
                    </span>
                </div>
                
                <div class="record-actions">
                    <button class="btn-edit" @click="emit('edit', record.id)">✏️</button>
                    <button class="btn-delete" @click="emit('delete', record.id)">🗑️</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
    person: { type: Object, required: true },
    records: { type: Array, default: () => [] }
})

const emit = defineEmits(['add', 'edit', 'delete', 'selectPerson'])

const sortedRecords = computed(() => {
    if (!props.records) return []
    return [...props.records].sort((a, b) => {
        return new Date(b.created_at) - new Date(a.created_at)
    })
})

const getRecordTypeLabel = (type) => {
    const labels = {
        partner: '🤝 Партнер',
        device: '📱 Устройство',
        sex: '❤️ Секс',
        medicine: '💊 Медицина',
        gifts: '🎁 Подарки',
        skills: '🧠 Навыки',
        travel: '✈️ Путешествия',
        work: '💼 Работа',
        character: '👤 Характер',
        dates: '📅 Даты',
        other: '📌 Другое'
    }
    return labels[type] || type
}

const getImportanceClass = (importance) => {
    if (importance >= 2) return 'high'
    if (importance >= 1) return 'medium'
    return 'low'
}

const formatDate = (date) => {
    if (!date) return ''
    return new Date(date).toLocaleDateString('ru-RU')
}

const truncateText = (text, maxLength) => {
    if (!text) return ''
    if (text.length <= maxLength) return text
    return text.slice(0, maxLength) + '...'
}
</script>

<style scoped>
.cross-records-tab {
    padding: 20px 0;
}
.tab-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}
.tab-header h3 {
    color: #fff;
    font-size: 18px;
    margin: 0;
}
.btn-add {
    padding: 8px 16px;
    background: #00c49a;
    border: none;
    border-radius: 10px;
    color: #0a0e0c;
    font-weight: 600;
    cursor: pointer;
}
.btn-add:hover {
    background: #00dbaa;
}
.empty-state {
    text-align: center;
    padding: 60px 20px;
    color: #5a6e68;
}
.empty-icon {
    font-size: 48px;
    margin-bottom: 16px;
}
.records-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 16px;
}
.record-card {
    background: #0d1210;
    border: 1px solid #1a2420;
    border-radius: 16px;
    padding: 16px;
    position: relative;
}
.record-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}
.record-type {
    font-size: 12px;
    color: #5a6e68;
    background: #1a2420;
    padding: 2px 10px;
    border-radius: 20px;
}
.record-status {
    font-size: 11px;
    padding: 2px 10px;
    border-radius: 20px;
    text-transform: capitalize;
}
.record-status.active {
    background: #00c49a20;
    color: #00c49a;
}
.record-status.completed {
    background: #008b6e20;
    color: #008b6e;
}
.record-status.archived {
    background: #5a6e6820;
    color: #5a6e68;
}
.record-title {
    color: #fff;
    font-size: 16px;
    margin: 8px 0;
}
.record-description {
    color: #5a6e68;
    font-size: 13px;
    line-height: 1.5;
    margin: 8px 0;
}
.record-meta {
    display: flex;
    gap: 12px;
    font-size: 12px;
    color: #5a6e68;
    margin: 8px 0;
}
.record-importance {
    padding: 2px 8px;
    border-radius: 12px;
}
.record-importance.high {
    background: #e55c5c20;
    color: #e55c5c;
}
.record-importance.medium {
    background: #e5a03c20;
    color: #e5a03c;
}
.record-importance.low {
    background: #008b6e20;
    color: #008b6e;
}
.record-actions {
    display: flex;
    gap: 8px;
    margin-top: 12px;
    padding-top: 12px;
    border-top: 1px solid #1a2420;
}
.record-actions button {
    padding: 4px 12px;
    background: none;
    border: 1px solid #2a3a35;
    border-radius: 8px;
    color: #5a6e68;
    cursor: pointer;
}
.record-actions button:hover {
    background: #1a2420;
}
.btn-edit:hover {
    border-color: #00c49a;
    color: #00c49a;
}
.btn-delete:hover {
    border-color: #e55c5c;
    color: #e55c5c;
}
</style>
