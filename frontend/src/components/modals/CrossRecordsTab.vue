<template>
    <div class="cross-records-tab">
        <div class="tab-header">
            <h3>📝 Записи</h3>
            <button class="add-btn" @click="emit('add')">➕ Добавить</button>
        </div>

        <div v-if="!records || records.length === 0" class="empty-state">
            <p>Нет записей</p>
        </div>

        <div v-else class="records-grid">
            <div 
                v-for="record in records" 
                :key="record.id" 
                class="record-card"
                :style="{ borderLeftColor: getCategoryColor(record.primary_category_id) }"
            >
                <div class="record-header">
                    <span class="record-title">{{ record.title }}</span>
                    <div class="record-actions">
                        <button class="edit-btn" @click="emit('edit', record.id)">✏️</button>
                        <button class="delete-btn" @click="emit('delete', record.id)">🗑️</button>
                    </div>
                </div>
                <div class="record-body">
                    <div class="record-type">
                        <span class="badge" :style="{ backgroundColor: getCategoryColor(record.primary_category_id) }">
                            {{ getCategoryName(record.primary_category_id) }}
                        </span>
                        <span class="record-status" :class="record.status">
                            {{ record.status }}
                        </span>
                        <span class="record-type-label">{{ getRecordTypeLabel(record.record_type) }}</span>
                    </div>
                    <p class="record-description" v-if="record.description">
                        {{ truncateText(record.description, 150) }}
                    </p>
                    <div class="record-meta">
                        <span v-if="record.record_date">📅 {{ formatDate(record.record_date) }}</span>
                        <span v-if="record.importance" class="importance">
                            ⭐ {{ record.importance }}
                        </span>
                    </div>
                    <div class="record-tags" v-if="record.tags && record.tags.length">
                        <span 
                            v-for="tag in record.tags" 
                            :key="tag.id" 
                            class="tag"
                            :style="{ backgroundColor: tag.color + '33', color: tag.color }"
                        >
                            #{{ tag.name }}
                        </span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
    person: { type: Object, default: null },
    personId: { type: Number, default: null },
    records: { type: Array, default: () => [] },
    categories: { type: Array, default: () => [] },
    partners: { type: Array, default: () => [] },
    devices: { type: Array, default: () => [] }
})

const emit = defineEmits(['add', 'edit', 'delete', 'selectPerson'])

const categoryMap = computed(() => {
    const map = {}
    if (props.categories) {
        props.categories.forEach(cat => {
            map[cat.id] = cat
        })
    }
    return map
})

const getCategoryName = (categoryId) => {
    const cat = categoryMap.value[categoryId]
    return cat ? cat.name : 'Без категории'
}

const getCategoryColor = (categoryId) => {
    const cat = categoryMap.value[categoryId]
    return cat ? cat.color || '#00c49a' : '#00c49a'
}

const getRecordTypeLabel = (type) => {
    const labels = {
        intimate: '💕 Интим',
        partner: '🤝 Партнер',
        device: '📱 Устройство',
        medicine: '💊 Медицина',
        gift: '🎁 Подарок',
        skill: '🎯 Навык',
        travel: '✈️ Путешествие',
        work: '💼 Работа',
        character: '🎭 Характер',
        date: '📅 Дата',
        other: '📌 Другое'
    }
    return labels[type] || type
}

const formatDate = (date) => {
    if (!date) return ''
    const d = new Date(date)
    return d.toLocaleDateString('ru-RU')
}

const truncateText = (text, maxLength) => {
    if (!text) return ''
    return text.length > maxLength ? text.slice(0, maxLength) + '...' : text
}
</script>

<style scoped>
.cross-records-tab {
    padding: 16px 0;
}
.tab-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
}
.tab-header h3 {
    color: #fff;
    font-size: 16px;
    margin: 0;
}
.add-btn {
    padding: 6px 16px;
    background: #00c49a;
    border: none;
    border-radius: 8px;
    color: #0a0e0c;
    font-weight: 600;
    cursor: pointer;
}
.add-btn:hover {
    background: #00d4a8;
}
.empty-state {
    padding: 40px 20px;
    text-align: center;
    color: #5a6e68;
}
.records-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 12px;
}
.record-card {
    background: #0d1210;
    border: 1px solid #1a2420;
    border-left: 4px solid #00c49a;
    border-radius: 12px;
    padding: 16px;
    transition: all 0.2s;
}
.record-card:hover {
    background: #111a17;
}
.record-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}
.record-title {
    font-size: 15px;
    font-weight: 600;
    color: #fff;
}
.record-actions {
    display: flex;
    gap: 6px;
}
.record-actions button {
    background: none;
    border: none;
    color: #5a6e68;
    cursor: pointer;
    padding: 4px 6px;
    border-radius: 4px;
    transition: all 0.2s;
}
.record-actions button:hover {
    background: #1a2420;
}
.edit-btn:hover {
    color: #00c49a;
}
.delete-btn:hover {
    color: #e55c5c;
}
.record-body {
    display: flex;
    flex-direction: column;
    gap: 8px;
}
.record-type {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
}
.badge {
    padding: 2px 10px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 600;
    color: #fff;
}
.record-status {
    font-size: 11px;
    padding: 2px 8px;
    border-radius: 10px;
    text-transform: uppercase;
}
.record-status.active {
    background: #00c49a20;
    color: #00c49a;
}
.record-status.completed {
    background: #2e7d6420;
    color: #2e7d64;
}
.record-status.archived {
    background: #5a6e6820;
    color: #5a6e68;
}
.record-type-label {
    font-size: 12px;
    color: #5a6e68;
}
.record-description {
    color: #8a9e98;
    font-size: 13px;
    margin: 0;
    line-height: 1.5;
    white-space: pre-wrap;
}
.record-meta {
    display: flex;
    gap: 16px;
    font-size: 12px;
    color: #5a6e68;
}
.record-meta .importance {
    color: #e5c53c;
}
.record-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    margin-top: 4px;
}
.record-tags .tag {
    padding: 2px 8px;
    border-radius: 10px;
    font-size: 11px;
}
@media (max-width: 768px) {
    .record-header {
        flex-wrap: wrap;
        gap: 8px;
    }
    .record-title {
        font-size: 14px;
    }
}
</style>