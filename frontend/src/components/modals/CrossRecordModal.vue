<template>
    <div v-if="isOpen" class="modal-overlay" @click.self="close">
        <div class="modal-content">
            <div class="modal-header">
                <h2>{{ isEdit ? '✏️ Редактирование записи' : '➕ Новая запись' }}</h2>
                <button class="modal-close" @click="close">✕</button>
            </div>
            
            <div class="modal-body">
                <div v-if="isLoading" class="loading-state">
                    <div class="loading-spinner"></div>
                    <p>Загрузка данных...</p>
                </div>
                
                <form v-else @submit.prevent="save">
                    <div class="form-group">
                        <label>Название записи *</label>
                        <input v-model="form.title" type="text" required placeholder="Введите название" />
                    </div>

                    <div class="form-group">
                        <label>Тип записи *</label>
                        <select v-model="form.record_type" required>
                            <option value="partner">🤝 Партнер</option>
                            <option value="device">📱 Устройство</option>
                            <option value="sex">❤️ Секс</option>
                            <option value="medicine">💊 Медицина</option>
                            <option value="gifts">🎁 Подарки</option>
                            <option value="skills">🧠 Навыки</option>
                            <option value="travel">✈️ Путешествия</option>
                            <option value="work">💼 Работа</option>
                            <option value="character">👤 Характер</option>
                            <option value="dates">📅 Даты</option>
                            <option value="other">📌 Другое</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label>Категория *</label>
                        <select v-model="form.primary_category_id" required>
                            <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                                {{ cat.name }}
                            </option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label>Описание</label>
                        <textarea v-model="form.description" rows="4" placeholder="Введите описание..."></textarea>
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label>Дата</label>
                            <input v-model="form.record_date" type="date" />
                        </div>
                        <div class="form-group">
                            <label>Важность</label>
                            <select v-model="form.importance">
                                <option :value="0">Низкая</option>
                                <option :value="1">Средняя</option>
                                <option :value="2">Высокая</option>
                            </select>
                        </div>
                    </div>

                    <div class="form-group">
                        <label>Статус</label>
                        <select v-model="form.status">
                            <option value="active">🟢 Активно</option>
                            <option value="completed">✅ Завершено</option>
                            <option value="archived">📦 В архиве</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label>
                            <input v-model="form.is_private" type="checkbox" />
                            🔒 Приватная запись
                        </label>
                    </div>
                </form>
            </div>

            <div class="modal-footer">
                <button class="btn-secondary" @click="close">Отмена</button>
                <button class="btn-primary" @click="save" :disabled="isLoading">
                    {{ isLoading ? '💾 Сохранение...' : '💾 Сохранить' }}
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { crossRecordsApi } from '@/api/endpoints/cross-records'
import { categoriesApi } from '@/api/endpoints/categories'
import { useToast } from '@/composables/useToast'

const isOpen = ref(false)
const isEdit = ref(false)
const isLoading = ref(false)
const recordId = ref(null)
const personId = ref(null)
const categories = ref([])

const { success, error: toastError } = useToast()

const form = reactive({
    title: '',
    description: '',
    record_type: 'other',
    primary_category_id: null,
    data: {},
    record_date: null,
    start_date: null,
    end_date: null,
    status: 'active',
    importance: 0,
    is_private: false
})

// Очистка формы
const resetForm = () => {
    Object.assign(form, {
        title: '',
        description: '',
        record_type: 'other',
        primary_category_id: categories.value.length > 0 ? categories.value[0].id : null,
        data: {},
        record_date: null,
        start_date: null,
        end_date: null,
        status: 'active',
        importance: 0,
        is_private: false
    })
}

// Загрузка категорий
const loadCategories = async () => {
    try {
        const data = await categoriesApi.getAll()
        categories.value = data
        if (data.length > 0 && !form.primary_category_id) {
            form.primary_category_id = data[0].id
        }
        console.log('✅ Загружено категорий:', categories.value.length)
    } catch (error) {
        console.error('❌ Ошибка загрузки категорий:', error)
        toastError('Ошибка загрузки категорий')
    }
}

// Загрузка записи для редактирования
const loadRecord = async (id) => {
    try {
        isLoading.value = true
        console.log('📥 Загрузка записи ID:', id)
        
        const record = await crossRecordsApi.getById(id)
        console.log('📝 Получена запись:', record)
        
        if (!record) {
            toastError('Запись не найдена')
            return
        }
        
        // Заполняем форму данными
        form.title = record.title || ''
        form.description = record.description || ''
        form.record_type = record.record_type || 'other'
        form.primary_category_id = record.primary_category_id || (categories.value.length > 0 ? categories.value[0].id : null)
        form.data = record.data || {}
        form.record_date = record.record_date || null
        form.start_date = record.start_date || null
        form.end_date = record.end_date || null
        form.status = record.status || 'active'
        form.importance = record.importance || 0
        form.is_private = record.is_private || false
        
        console.log('✅ Форма заполнена:', form)
        isEdit.value = true
        
    } catch (error) {
        console.error('❌ Ошибка загрузки записи:', error)
        toastError('Ошибка загрузки записи: ' + (error.message || 'Unknown error'))
    } finally {
        isLoading.value = false
    }
}

// Открытие модального окна
const open = async (id = null, pId = null) => {
    console.log('📂 ОТКРЫТИЕ CrossRecordModal:', { id, pId })
    
    // Сбрасываем форму
    resetForm()
    
    recordId.value = id
    personId.value = pId
    isEdit.value = false
    isLoading.value = false
    isOpen.value = true
    
    // Загружаем категории если нужно
    if (categories.value.length === 0) {
        await loadCategories()
    }
    
    // Если есть ID - загружаем запись для редактирования
    if (id) {
        console.log('📝 Режим редактирования, загрузка записи ID:', id)
        await loadRecord(id)
    } else {
        console.log('📝 Режим создания новой записи')
        // Устанавливаем категорию по умолчанию
        if (categories.value.length > 0 && !form.primary_category_id) {
            form.primary_category_id = categories.value[0].id
        }
    }
    
    console.log('✅ CrossRecordModal ОТКРЫТ, isEdit:', isEdit.value, 'recordId:', recordId.value)
}

// Закрытие модального окна
const close = () => {
    isOpen.value = false
    recordId.value = null
    personId.value = null
    isEdit.value = false
    isLoading.value = false
    resetForm()
}

// Сохранение
const save = async () => {
    // Валидация
    if (!form.title || !form.record_type || !form.primary_category_id) {
        toastError('Заполните обязательные поля')
        return
    }
    
    try {
        isLoading.value = true
        
        const data = {
            person_id: personId.value,
            title: form.title,
            description: form.description,
            record_type: form.record_type,
            primary_category_id: form.primary_category_id,
            data: form.data || {},
            record_date: form.record_date || null,
            start_date: form.start_date || null,
            end_date: form.end_date || null,
            status: form.status || 'active',
            importance: form.importance || 0,
            is_private: form.is_private || false
        }
        
        console.log('💾 Сохранение записи:', data)
        
        let result
        if (isEdit.value && recordId.value) {
            console.log('🔄 Обновление записи ID:', recordId.value)
            result = await crossRecordsApi.update(recordId.value, data)
            success('Запись обновлена')
        } else {
            console.log('➕ Создание новой записи')
            result = await crossRecordsApi.create(data)
            success('Запись создана')
        }
        
        console.log('✅ Результат сохранения:', result)
        
        emit('saved')
        close()
    } catch (error) {
        console.error('❌ Ошибка сохранения:', error)
        toastError('Ошибка сохранения записи: ' + (error.message || 'Unknown error'))
    } finally {
        isLoading.value = false
    }
}

const emit = defineEmits(['saved'])

// Загружаем категории при монтировании
onMounted(() => {
    loadCategories()
})

// Экспортируем методы
defineExpose({ open, close })
</script>

<style scoped>
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.7);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
    backdrop-filter: blur(4px);
}
.modal-content {
    background: #0d1210;
    border-radius: 20px;
    border: 1px solid #1a2420;
    padding: 30px;
    max-width: 600px;
    width: 90%;
    max-height: 90vh;
    overflow-y: auto;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.8);
}
.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}
.modal-header h2 {
    color: #fff;
    font-size: 20px;
    margin: 0;
}
.modal-close {
    background: none;
    border: none;
    color: #5a6e68;
    font-size: 24px;
    cursor: pointer;
    padding: 0;
}
.modal-close:hover {
    color: #e55c5c;
}
.modal-body {
    margin-bottom: 20px;
}
.modal-footer {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    padding-top: 16px;
    border-top: 1px solid #1a2420;
}
.btn-primary {
    padding: 8px 24px;
    background: #00c49a;
    border: none;
    border-radius: 10px;
    color: #0a0e0c;
    font-weight: 600;
    cursor: pointer;
}
.btn-primary:hover:not(:disabled) {
    background: #00dbaa;
}
.btn-primary:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}
.btn-secondary {
    padding: 8px 24px;
    background: #1a2420;
    border: 1px solid #2a3a35;
    border-radius: 10px;
    color: #5a6e68;
    cursor: pointer;
}
.btn-secondary:hover {
    background: #2a3a35;
}
.form-group {
    margin-bottom: 16px;
}
.form-group label {
    display: block;
    color: #5a6e68;
    font-size: 13px;
    margin-bottom: 6px;
}
.form-group input,
.form-group select,
.form-group textarea {
    width: 100%;
    padding: 10px 14px;
    background: #1a2420;
    border: 1px solid #2a3a35;
    border-radius: 10px;
    color: #fff;
    font-size: 14px;
}
.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
    border-color: #00c49a;
    outline: none;
}
.form-group input[type="checkbox"] {
    width: auto;
    margin-top: 8px;
}
.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
}
.form-row .form-group {
    margin-bottom: 0;
}
.loading-state {
    text-align: center;
    padding: 40px 20px;
    color: #5a6e68;
}
.loading-spinner {
    width: 40px;
    height: 40px;
    border: 3px solid #1a2420;
    border-top-color: #00c49a;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto 16px;
}
@keyframes spin {
    to { transform: rotate(360deg); }
}
</style>
