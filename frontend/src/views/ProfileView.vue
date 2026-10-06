<template>
    <div class="profile-container">
        <div class="profile-header">
            <div class="profile-avatar">
                <span class="profile-initials">{{ getInitials(person.full_name) }}</span>
                <div class="profile-rank" :style="{ background: getRankColor(person.importance) }">
                    {{ person.importance || 0 }}
                </div>
            </div>
            <div class="profile-details">
                <h1 class="profile-name">{{ person.full_name }}</h1>
                <div class="profile-tags">
                    <span class="tag">@{{ person.short_name }}</span>
                    <span class="tag" v-if="person.phone">📞 {{ person.phone }}</span>
                    <span class="tag" v-if="person.email">✉️ {{ person.email }}</span>
                    <span class="tag" v-if="personAge">🎂 {{ personAge }} лет</span>
                </div>
                <div class="profile-address" v-if="person.address">
                    📍 {{ person.address }}
                </div>
            </div>
            <div class="profile-actions">
                <button class="action-edit" @click="handleEdit">✏️ Редактировать</button>
                <button class="action-delete" @click="handleDelete">🗑️ Удалить</button>
            </div>
        </div>

        <div class="profile-tabs">
            <button 
                v-for="tab in tabs" 
                :key="tab.id" 
                class="tab" 
                :class="{ active: activeTab === tab.id }"
                @click="activeTab = tab.id"
            >
                <span class="tab-icon">{{ tab.icon }}</span>
                <span>{{ tab.label }}</span>
                <span class="tab-count" v-if="getTabCount(tab.id)">{{ getTabCount(tab.id) }}</span>
            </button>
        </div>

        <component 
            :is="getTabComponent(activeTab)" 
            :person="person"
            :partners="person.partners"
            :devices="person.devices"
            :records="person.cross_records"
            :categories="categories"
            @add="handleAddItem"
            @edit="handleEditItem"
            @delete="handleDeleteItem"
            @selectPerson="handleSelectPerson"
        />
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import InfoTab from '@/components/profile/InfoTab.vue'
import RelationsTab from '@/components/profile/RelationsTab.vue'
import RealEstateTab from '@/components/profile/RealEstateTab.vue'
import VehiclesTab from '@/components/profile/VehiclesTab.vue'
import DigitalAccountsTab from '@/components/profile/DigitalAccountsTab.vue'
import SocialMediaTab from '@/components/profile/SocialMediaTab.vue'
import CasesTab from '@/components/profile/CasesTab.vue'
import MedicalTab from '@/components/profile/MedicalTab.vue'
import PartnersTab from '@/components/profile/PartnersTab.vue'
import DevicesTab from '@/components/profile/DevicesTab.vue'
import CrossRecordsTab from '@/components/profile/CrossRecordsTab.vue'
import { categoriesApi } from '@/api/endpoints/categories'

const props = defineProps({
    person: { type: Object, required: true }
})

const emit = defineEmits(['edit', 'delete', 'editItem', 'deleteItem', 'addItem', 'selectPerson'])

const activeTab = ref('info')
const categories = ref([])

const tabs = [
    { id: 'info', label: 'Информация', icon: '📋' },
    { id: 'relations', label: 'Связи', icon: '🔗' },
    { id: 'realestate', label: 'Недвижимость', icon: '🏢' },
    { id: 'vehicles', label: 'Транспорт', icon: '🚗' },
    { id: 'digital', label: 'Аккаунты', icon: '🎮' },
    { id: 'social', label: 'Соцсети', icon: '🌐' },
    { id: 'cases', label: 'Дела', icon: '📋' },
    { id: 'medical', label: 'Медицина', icon: '🏥' },
    { id: 'partners', label: 'Партнеры', icon: '🤝' },
    { id: 'devices', label: 'Устройства', icon: '📱' },
    { id: 'cross', label: 'Записи', icon: '📝' },
]

const tabComponents = {
    info: InfoTab,
    relations: RelationsTab,
    realestate: RealEstateTab,
    vehicles: VehiclesTab,
    digital: DigitalAccountsTab,
    social: SocialMediaTab,
    cases: CasesTab,
    medical: MedicalTab,
    partners: PartnersTab,
    devices: DevicesTab,
    cross: CrossRecordsTab,
}

const personAge = computed(() => {
    if (!props.person?.birth_date) return null
    const today = new Date()
    const birth = new Date(props.person.birth_date)
    let age = today.getFullYear() - birth.getFullYear()
    const m = today.getMonth() - birth.getMonth()
    if (m < 0 || (m === 0 && today.getDate() < birth.getDate())) age--
    return age
})

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

const getTabCount = (tabId) => {
    if (!props.person) return 0
    const counts = {
        relations: props.person.relations?.length || 0,
        realestate: props.person.real_estate?.length || 0,
        vehicles: props.person.vehicles?.length || 0,
        digital: props.person.digital_accounts?.length || 0,
        social: props.person.social_media?.length || 0,
        cases: props.person.cases?.length || 0,
        medical: props.person.medical_records?.length || 0,
        partners: props.person.partners?.length || 0,
        devices: props.person.devices?.length || 0,
        cross: props.person.cross_records?.length || 0,
    }
    return counts[tabId] || 0
}

const getTabComponent = (tabId) => {
    return tabComponents[tabId] || InfoTab
}

const handleEdit = () => {
    emit('edit')
}

const handleDelete = () => {
    emit('delete')
}

const handleAddItem = () => { console.log('📤 ProfileView.handleAddItem() вызван, активный таб:', activeTab.value);
    console.log('📤 ProfileView отправляет addItem с табом:', activeTab.value); emit('addItem', activeTab.value)
}

const handleEditItem = (id) => { console.log('📤 ProfileView.handleEditItem() вызван, id:', id, 'таб:', activeTab.value);
    emit('editItem', id)
}

const handleDeleteItem = (id) => { console.log('📤 ProfileView.handleDeleteItem() вызван, id:', id, 'таб:', activeTab.value);
    emit('deleteItem', { id, type: activeTab.value })
}

const handleSelectPerson = (id) => {
    emit('selectPerson', id)
}

onMounted(async () => {
    try {
        const data = await categoriesApi.getAll()
        categories.value = data
    } catch (error) {
        console.error('Error loading categories:', error)
    }
})

defineExpose({
    activeTab
})
</script>

<style scoped>
.profile-container {
    max-width: 1200px;
    margin: 0 auto;
}
.profile-header {
    display: flex;
    align-items: center;
    gap: 24px;
    padding: 24px;
    background: #0d1210;
    border-radius: 20px;
    border: 1px solid #1a2420;
    margin-bottom: 24px;
}
.profile-avatar {
    position: relative;
    width: 80px;
    height: 80px;
    background: linear-gradient(135deg, #00c49a, #008b6e);
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}
.profile-initials {
    font-size: 32px;
    font-weight: 700;
    color: #fff;
}
.profile-rank {
    position: absolute;
    bottom: -6px;
    right: -6px;
    width: 28px;
    height: 28px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 700;
    color: #0a0e0c;
    border: 2px solid #0d1210;
}
.profile-details {
    flex: 1;
}
.profile-name {
    font-size: 24px;
    font-weight: 600;
    color: #fff;
    margin-bottom: 8px;
}
.profile-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 12px;
}
.tag {
    padding: 4px 12px;
    background: #1a2420;
    border-radius: 20px;
    font-size: 12px;
    color: #5a6e68;
}
.profile-address {
    font-size: 13px;
    color: #5a6e68;
    padding: 6px 12px;
    background: #1a2420;
    border-radius: 10px;
    display: inline-block;
}
.profile-actions {
    display: flex;
    gap: 12px;
}
.action-edit {
    padding: 8px 20px;
    background: #1a2420;
    border: 1px solid #2a3a35;
    border-radius: 10px;
    color: #00c49a;
    cursor: pointer;
}
.action-edit:hover {
    background: #00c49a20;
}
.action-delete {
    padding: 8px 20px;
    background: #1a2420;
    border: 1px solid #e55c5c;
    border-radius: 10px;
    color: #e55c5c;
    cursor: pointer;
}
.action-delete:hover {
    background: #e55c5c20;
}
.profile-tabs {
    display: flex;
    gap: 8px;
    margin-bottom: 24px;
    padding-bottom: 12px;
    border-bottom: 1px solid #1a2420;
    overflow-x: auto;
    flex-wrap: wrap;
}
.tab {
    padding: 8px 16px;
    background: none;
    border: none;
    border-radius: 20px;
    color: #5a6e68;
    cursor: pointer;
    font-size: 13px;
    display: flex;
    align-items: center;
    gap: 6px;
    white-space: nowrap;
    transition: all 0.2s;
}
.tab:hover {
    color: #00c49a;
    background: #00c49a10;
}
.tab.active {
    background: #00c49a15;
    color: #00c49a;
}
.tab-count {
    background: #00c49a20;
    padding: 1px 6px;
    border-radius: 10px;
    font-size: 10px;
    font-weight: 600;
}
@media (max-width: 768px) {
    .profile-header {
        flex-direction: column;
        text-align: center;
    }
    .profile-tags {
        justify-content: center;
    }
    .profile-actions {
        width: 100%;
        justify-content: center;
    }
    .profile-tabs {
        flex-wrap: wrap;
        justify-content: center;
    }
}
</style>

