<template>
    <div class="app">
        <Sidebar
            :persons="treeStore.persons"
            :selected-person-id="treeStore.selectedPersonId"
            :is-loading="treeStore.isLoading"
            :search-query="treeStore.searchQuery"
            :relations-count="treeStore.relations.length"
            @toggle="handleSidebarToggle"
            @search="handleSearch"
            @refresh="refreshData"
            @add-person="openPersonModal"
            @select-contact="selectContact"
            @edit-person="openPersonModal"
            @add-relation="openRelationModal"
        />

        <main class="main-content">
            <div v-if="personStore.isLoading" class="loading-container" role="status">
                <div class="loading-spinner"></div>
                <p>Загрузка данных...</p>
            </div>

            <div v-else-if="!currentPerson" class="welcome-container">
                <div class="welcome-card">
                    <div class="welcome-icon">◆</div>
                    <h1>ARC Agent</h1>
                    <p>Управление контактами и связями</p>
                    <button class="welcome-btn" @click="openPersonModal()">➕ Добавить контакт</button>
                </div>
            </div>

            <ProfileView
                ref="profileViewRef"
                v-else
                :person="currentPerson"
                @edit="() => openPersonModal(currentPerson.id)"
                @delete="confirmDeletePerson"
                @editItem="handleEditItem"
                @deleteItem="handleDeleteItem"
                @addItem="handleAddItem"
                @selectPerson="selectContact"
            />
        </main>

        <!-- Модальные окна -->
        <PersonModal ref="personModalRef" />
        <RelationModal ref="relationModalRef" />
        <SocialModal ref="socialModalRef" />
        <DigitalAccountModal ref="digitalAccountModalRef" />
        <RealEstateModal ref="realEstateModalRef" />
        <VehicleModal ref="vehicleModalRef" />
        <CaseModal ref="caseModalRef" />
        <MedicalModal ref="medicalModalRef" />
        <CrossRecordModal ref="crossRecordModalRef" />
        <PartnerModal ref="partnerModalRef" />
        <DeviceModal ref="deviceModalRef" />
        <ConfirmModal ref="confirmModalRef" />
        <ToastHost />
    </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useTreeStore } from './stores/useTreeStore'
import { usePersonStore } from './stores/usePersonStore'
import { useToast } from './composables/useToast'

import Sidebar from './components/layout/Sidebar.vue'
import ProfileView from './views/ProfileView.vue'
import PersonModal from './components/modals/PersonModal.vue'
import RelationModal from './components/modals/RelationModal.vue'
import SocialModal from './components/modals/SocialModal.vue'
import DigitalAccountModal from './components/modals/DigitalAccountModal.vue'
import RealEstateModal from './components/modals/RealEstateModal.vue'
import VehicleModal from './components/modals/VehicleModal.vue'
import CaseModal from './components/modals/CaseModal.vue'
import MedicalModal from './components/modals/MedicalModal.vue'
import CrossRecordModal from './components/modals/CrossRecordModal.vue'
import PartnerModal from './components/modals/PartnerModal.vue'
import DeviceModal from './components/modals/DeviceModal.vue'
import ConfirmModal from './components/common/ConfirmModal.vue'
import ToastHost from './components/common/ToastHost.vue'

const treeStore = useTreeStore()
const personStore = usePersonStore()
const { success, error: toastError } = useToast()

const profileViewRef = ref(null)
const personModalRef = ref(null)
const relationModalRef = ref(null)
const socialModalRef = ref(null)
const digitalAccountModalRef = ref(null)
const realEstateModalRef = ref(null)
const vehicleModalRef = ref(null)
const caseModalRef = ref(null)
const medicalModalRef = ref(null)
const crossRecordModalRef = ref(null)
const partnerModalRef = ref(null)
const deviceModalRef = ref(null)

const confirmModalRef = ref(null)

const currentPerson = computed(() => personStore.currentPerson)

const handleSidebarToggle = () => {}

const handleSearch = (query) => {
    treeStore.setSearchQuery(query)
}

const selectContact = async (id) => {
    if (!id) return
    treeStore.selectPerson(id)
    await personStore.loadPerson(id)  // ошибки показывает стор
}

// Полная перезагрузка — только при старте и по кнопке «Обновить». После CRUD сторы обновляются сами.
const refreshData = async () => {
    await Promise.all([treeStore.refresh(), personStore.refreshCurrent()])
    if (treeStore.error) toastError(treeStore.error)
}

// ===== УНИВЕРСАЛЬНЫЙ МЕТОД ОТКРЫТИЯ МОДАЛЬНЫХ ОКОН =====
const openModal = (modalRef, id = null, personId = null) => { console.log('📥 App.openModal() вызван, modalRef:', modalRef, 'id:', id, 'personId:', personId);
    if (!modalRef) {
        console.error('❌ Модальное окно не инициализировано')
        return false
    }
    try {
        if (personId !== null) {
            modalRef.open(id, personId)
        } else {
            modalRef.open(id)
        }
        return true
    } catch (error) {
        console.error('❌ Ошибка открытия модального окна:', error)
        return false
    }
}

const openPersonModal = (id = null) => {
    console.log('📋 Открытие PersonModal, id:', id)
    return openModal(personModalRef.value, id)
}

const openRelationModal = (parentId) => {
    console.log('🔗 Открытие RelationModal, parentId:', parentId)
    return openModal(relationModalRef.value, parentId)
}

const openSocialModal = (id = null) => {
    console.log('🌐 Открытие SocialModal, id:', id)
    return openModal(socialModalRef.value, id)
}

const openDigitalAccountModal = (id = null) => {
    console.log('🎮 Открытие DigitalAccountModal, id:', id)
    return openModal(digitalAccountModalRef.value, id)
}

const openRealEstateModal = (id = null) => {
    console.log('🏢 Открытие RealEstateModal, id:', id)
    return openModal(realEstateModalRef.value, id)
}

const openVehicleModal = (id = null) => {
    console.log('🚗 Открытие VehicleModal, id:', id)
    return openModal(vehicleModalRef.value, id)
}

const openCaseModal = (id = null) => {
    console.log('📋 Открытие CaseModal, id:', id)
    return openModal(caseModalRef.value, id)
}

const openMedicalModal = (id = null) => {
    console.log('🏥 Открытие MedicalModal, id:', id)
    return openModal(medicalModalRef.value, id)
}

const openCrossRecordModal = (id = null, personId = null) => {
    console.log('📝 Открытие CrossRecordModal, id:', id, 'personId:', personId || currentPerson.value?.id)
    const result = openModal(crossRecordModalRef.value, id, personId || currentPerson.value?.id)
    if (result) {
        console.log('✅ CrossRecordModal открыт успешно')
    } else {
        console.error('❌ Не удалось открыть CrossRecordModal')
    }
    return result
}

const openPartnerModal = (id = null, personId = null) => { console.log('📥 App.openPartnerModal() вызван, id:', id, 'personId:', personId);
    console.log('🤝 Открытие PartnerModal, id:', id, 'personId:', personId || currentPerson.value?.id)
    console.log('📥 Проверка partnerModalRef:', partnerModalRef.value); return openModal(partnerModalRef.value, id, personId || currentPerson.value?.id)
}

const openDeviceModal = (id = null, personId = null) => {
    console.log('📱 Открытие DeviceModal, id:', id, 'personId:', personId || currentPerson.value?.id)
    return openModal(deviceModalRef.value, id, personId || currentPerson.value?.id)
}

// ===== ОБРАБОТЧИКИ ИЗ ПРОФИЛЯ =====
const handleAddItem = (tabId) => { console.log('📥 App.handleAddItem() вызван, tabId:', tabId);
    console.log('➕ Добавление элемента в таб:', tabId)
    
    const modalMap = {
        info: () => openPersonModal(null),
        relations: () => openRelationModal(currentPerson.value?.id),
        realestate: () => openRealEstateModal(null),
        vehicles: () => openVehicleModal(null),
        digital: () => openDigitalAccountModal(null),
        social: () => openSocialModal(null),
        cases: () => openCaseModal(null),
        medical: () => openMedicalModal(null),
        partners: () => openPartnerModal(null, currentPerson.value?.id),
        devices: () => openDeviceModal(null, currentPerson.value?.id),
        sex: () => openCrossRecordModal(null, currentPerson.value?.id),
        medicine: () => openCrossRecordModal(null, currentPerson.value?.id),
        gifts: () => openCrossRecordModal(null, currentPerson.value?.id),
        skills: () => openCrossRecordModal(null, currentPerson.value?.id),
        travel: () => openCrossRecordModal(null, currentPerson.value?.id),
        work: () => openCrossRecordModal(null, currentPerson.value?.id),
        character: () => openCrossRecordModal(null, currentPerson.value?.id),
        dates: () => openCrossRecordModal(null, currentPerson.value?.id),
        cross: () => openCrossRecordModal(null, currentPerson.value?.id)
    }
    
    const handler = modalMap[tabId]
    if (handler) {
        handler()
    } else {
        console.error('❌ Неизвестный таб для добавления:', tabId)
    }
}

const handleEditItem = (id) => {
    console.log('✏️ Редактирование элемента:', id)
    
    if (!profileViewRef.value) {
        console.error('❌ ProfileView не найден')
        return
    }
    
    const actualTab = profileViewRef.value.activeTab
    console.log('📍 Активный таб:', actualTab)
    
    const modalMap = {
        info: () => openPersonModal(id),
        relations: () => openRelationModal(id),
        realestate: () => openRealEstateModal(id),
        vehicles: () => openVehicleModal(id),
        digital: () => openDigitalAccountModal(id),
        social: () => openSocialModal(id),
        cases: () => openCaseModal(id),
        medical: () => openMedicalModal(id),
        partners: () => openPartnerModal(id, currentPerson.value?.id),
        devices: () => openDeviceModal(id, currentPerson.value?.id),
        sex: () => openCrossRecordModal(id, currentPerson.value?.id),
        medicine: () => openCrossRecordModal(id, currentPerson.value?.id),
        gifts: () => openCrossRecordModal(id, currentPerson.value?.id),
        skills: () => openCrossRecordModal(id, currentPerson.value?.id),
        travel: () => openCrossRecordModal(id, currentPerson.value?.id),
        work: () => openCrossRecordModal(id, currentPerson.value?.id),
        character: () => openCrossRecordModal(id, currentPerson.value?.id),
        dates: () => openCrossRecordModal(id, currentPerson.value?.id),
        cross: () => openCrossRecordModal(id, currentPerson.value?.id)
    }
    
    const handler = modalMap[actualTab]
    if (handler) {
        handler()
    } else {
        console.error('❌ Неизвестный таб для редактирования:', actualTab)
    }
}

// Вкладка профиля → коллекция в сторе
const TAB_COLLECTION = {
    relations: 'relations',
    realestate: 'real_estate',
    vehicles: 'vehicles',
    digital: 'digital_accounts',
    social: 'social_media',
    cases: 'cases',
    medical: 'medical_records',
    partners: 'partners',
    devices: 'devices',
    cross: 'cross_records',
    cross_records: 'cross_records',
}

const handleDeleteItem = async ({ id, type }) => {
    const key = TAB_COLLECTION[type]
    if (!key || !confirmModalRef.value) return
    if (!(await confirmModalRef.value.open('Удалить элемент?'))) return
    try {
        await personStore.deleteItem(key, id)  // запись исчезает сразу, при ошибке возвращается
        success('Удалено')
    } catch (err) {
        toastError(`Не удалось удалить: ${err.message}`)
    }
}

const confirmDeletePerson = async () => {
    const person = currentPerson.value
    if (!person || !confirmModalRef.value) return
    if (!(await confirmModalRef.value.open('Удалить контакт? Это действие необратимо!'))) return
    try {
        await personStore.deletePerson(person.id)
        success('Контакт удален')
    } catch (err) {
        toastError(`Не удалось удалить контакт: ${err.message}`)
    }
}

onMounted(() => {
    refreshData()
})
</script>

<style src="./styles/app.css"></style>


