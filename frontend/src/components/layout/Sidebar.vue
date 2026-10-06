<template>
    <div class="sidebar" :class="{ collapsed: isCollapsed }">
        <!-- Glass effect overlay -->
        <div class="sidebar-glass"></div>
        
        <!-- Header -->
        <div class="sidebar-header">
            <div class="logo">
                <div class="logo-gem">◆</div>
                <div class="logo-text-group" v-if="!isCollapsed">
                    <span class="logo-title">A.R.C</span>
                    <span class="logo-sub">Archive Registry by Korchagin</span>
                </div>
            </div>
            <button class="toggle-btn" @click="toggleSidebar">
                <svg v-if="!isCollapsed" width="18" height="18" viewBox="0 0 24 24" fill="none">
                    <path d="M15 18L9 12L15 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none">
                    <path d="M9 18L15 12L9 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </button>
        </div>

        <!-- Search -->
        <div class="sidebar-search" v-if="!isCollapsed">
            <div class="search-wrapper">
                <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none">
                    <circle cx="11" cy="11" r="8" stroke="currentColor" stroke-width="2"/>
                    <path d="M21 21L17 17" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
                <input
                    type="text"
                    :value="searchQuery"
                    @input="onSearch"
                    placeholder="Поиск контактов..."
                    class="search-input"
                />
                <span class="search-hint">⌘K</span>
            </div>
        </div>

        <!-- Stats -->
        <div class="sidebar-stats" v-if="!isCollapsed">
            <div class="stat-item">
                <span class="stat-number">{{ persons.length }}</span>
                <span class="stat-label">контактов</span>
            </div>
            <div class="stat-divider"></div>
            <div class="stat-item">
                <span class="stat-number">{{ getImportantCount() }}</span>
                <span class="stat-label">важных</span>
            </div>
            <!-- <div class="stat-divider"></div>
            <div class="stat-item">
                <span class="stat-number">{{ getRelationsCount() }}</span>
                <span class="stat-label">связей</span>
            </div> -->
        </div>

        <!-- List -->
        <div class="sidebar-list">
            <div v-if="isLoading" class="loading-state">
                <div class="loading-ring"></div>
            </div>

            <div
                v-for="person in filteredPersons"
                :key="person.id"
                class="sidebar-item"
                :class="{ 
                    active: selectedPersonId === person.id,
                    important: person.importance >= 7
                }"
                @click="selectPerson(person.id)"
                @contextmenu.prevent="editPerson(person.id)"
            >
                <div class="item-avatar" :style="{ background: getAvatarColor(person.short_name) }">
                    {{ getInitials(person.full_name) }}
                    <div class="avatar-ring" v-if="person.importance >= 8"></div>
                </div>
                <div class="item-info" v-if="!isCollapsed">
                    <div class="item-name">{{ person.full_name }}</div>
                    <div class="item-meta">
                        <span class="item-short">@{{ person.short_name }}</span>
                        <span class="item-dot" v-if="person.phone"></span>
                        <span class="item-phone" v-if="person.phone">{{ person.phone }}</span>
                    </div>
                </div>
                <div class="item-rank" v-if="!isCollapsed" :style="{ background: getRankColor(person.importance) }">
                    {{ person.importance || 0 }}
                </div>
                <div class="item-rank-small" v-else :style="{ background: getRankColor(person.importance) }">
                    {{ person.importance || 0 }}
                </div>
            </div>

            <div v-if="!isLoading && filteredPersons.length === 0" class="empty-state">
                <svg width="40" height="40" viewBox="0 0 24 24" fill="none">
                    <circle cx="11" cy="11" r="8" stroke="#2a4a3e" stroke-width="1.5"/>
                    <path d="M21 21L17 17" stroke="#2a4a3e" stroke-width="1.5" stroke-linecap="round"/>
                </svg>
                <span>Ничего не найдено</span>
            </div>
        </div>

        <!-- Footer -->
        <div class="sidebar-footer" v-if="!isCollapsed">
            <button class="footer-btn" @click="refreshData">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                    <path d="M23 4V10H17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M1 20V14H7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M3.51 9.00001C4.01717 7.56678 4.87913 6.28541 6.01547 5.27542C7.1518 4.26543 8.52547 3.55976 10.0083 3.22426C11.4911 2.88875 13.0348 2.93434 14.4952 3.35677C15.9556 3.77921 17.2853 4.56472 18.36 5.64001L23 10.0001M1 14.0001L5.64 18.3601C6.71475 19.4353 8.04437 20.2209 9.50481 20.6433C10.9652 21.0657 12.5089 21.1113 13.9917 20.7758C15.4745 20.4403 16.8482 19.7346 17.9845 18.7246C19.1209 17.7146 19.9828 16.4333 20.49 15.0001" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span>Обновить</span>
            </button>
            <button class="footer-btn primary" @click="addPerson">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                    <path d="M12 5V19" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                    <path d="M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
                <span>Добавить</span>
            </button>
        </div>
        <div class="sidebar-footer collapsed" v-else>
            <button class="footer-btn" @click="refreshData">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                    <path d="M23 4V10H17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M1 20V14H7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M3.51 9.00001C4.01717 7.56678 4.87913 6.28541 6.01547 5.27542C7.1518 4.26543 8.52547 3.55976 10.0083 3.22426C11.4911 2.88875 13.0348 2.93434 14.4952 3.35677C15.9556 3.77921 17.2853 4.56472 18.36 5.64001L23 10.0001M1 14.0001L5.64 18.3601C6.71475 19.4353 8.04437 20.2209 9.50481 20.6433C10.9652 21.0657 12.5089 21.1113 13.9917 20.7758C15.4745 20.4403 16.8482 19.7346 17.9845 18.7246C19.1209 17.7146 19.9828 16.4333 20.49 15.0001" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </button>
            <button class="footer-btn primary" @click="addPerson">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                    <path d="M12 5V19" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                    <path d="M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
            </button>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Sidebar',
    props: {
        persons: {
            type: Array,
            default: () => []
        },
        selectedPersonId: {
            type: Number,
            default: null
        },
        isLoading: {
            type: Boolean,
            default: false
        },
        searchQuery: {
            type: String,
            default: ''
        }
    },
    data() {
        return {
            isCollapsed: false
        }
    },
    computed: {
        filteredPersons() {
            if (!this.searchQuery) return this.persons || []
            const q = this.searchQuery.toLowerCase()
            return this.persons.filter(p =>
                p.full_name?.toLowerCase().includes(q) ||
                p.short_name?.toLowerCase().includes(q)
            )
        }
    },
    methods: {
        toggleSidebar() {
            this.isCollapsed = !this.isCollapsed
        },
        getImportantCount() {
            return this.persons?.filter(p => p.importance >= 7).length || 0
        },
        getRelationsCount() {
            return this.persons?.reduce((sum, p) => sum + (p.relations?.length || 0), 0) || 0
        },
        refreshData() {
            this.$emit('refresh')
        },
        addPerson() {
            this.$emit('add-person')
        },
        onSearch(event) {
            this.$emit('search', event.target.value)
        },
        selectPerson(id) {
            this.$emit('select-contact', id)
        },
        editPerson(id) {
            this.$emit('edit-person', id)
        },
        getInitials(name) {
            if (!name) return '?'
            return name.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase()
        },
        getAvatarColor(name) {
            const colors = ['#00c49a', '#4ecdc4', '#ffd93d', '#ff6b6b', '#6c5ce7', '#74b9ff', '#fd79a8', '#a29bfe']
            let hash = 0
            for (let i = 0; i < name.length; i++) {
                hash = name.charCodeAt(i) + ((hash << 5) - hash)
            }
            return colors[Math.abs(hash) % colors.length]
        },
        getRankColor(importance) {
            if (!importance || importance === 0) return '#2a4a3e'
            if (importance >= 8) return '#ff6b6b'
            if (importance >= 6) return '#ffd93d'
            if (importance >= 4) return '#74b9ff'
            return '#2a4a3e'
        }
    }
}
</script>

<style scoped>
.sidebar {
    width: 280px;
    min-width: 280px;
    height: 100vh;
    background: #080e0c;
    border-right: 1px solid rgba(0, 196, 154, 0.06);
    display: flex;
    flex-direction: column;
    position: fixed;
    left: 0;
    top: 0;
    z-index: 100;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.sidebar-glass {
    position: absolute;
    inset: 0;
    background: linear-gradient(180deg, rgba(0, 196, 154, 0.02) 0%, transparent 50%, rgba(0, 196, 154, 0.01) 100%);
    pointer-events: none;
}

.sidebar.collapsed {
    width: 68px;
    min-width: 68px;
}

.sidebar-header {
    padding: 18px 20px;
    border-bottom: 1px solid rgba(0, 196, 154, 0.05);
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    z-index: 1;
}

.logo {
    display: flex;
    align-items: center;
    gap: 10px;
    text-decoration: none;
}

.logo-gem {
    font-size: 26px;
    background: linear-gradient(135deg, #00c49a, #008b6e, #00c49a);
    background-size: 200% 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gemShine 4s ease-in-out infinite;
}

@keyframes gemShine {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

.logo-text-group {
    display: flex;
    flex-direction: column;
    line-height: 1.1;
}

.logo-title {
    font-size: 18px;
    font-weight: 600;
    color: #e8f0ee;
    letter-spacing: 2px;
}

.logo-sub {
    font-size: 10px;
    color: #4a7a6a;
    letter-spacing: 4px;
    text-transform: uppercase;
}

.toggle-btn {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.04);
    color: #4a6a62;
    cursor: pointer;
    padding: 6px 8px;
    border-radius: 8px;
    transition: all 0.3s;
    display: flex;
    align-items: center;
    justify-content: center;
}

.toggle-btn:hover {
    background: rgba(0, 196, 154, 0.1);
    color: #00c49a;
    border-color: rgba(0, 196, 154, 0.15);
}

.sidebar-search {
    padding: 14px 16px;
    position: relative;
    z-index: 1;
}

.search-wrapper {
    position: relative;
    display: flex;
    align-items: center;
}

.search-icon {
    position: absolute;
    left: 12px;
    color: #3a5a52;
}

.search-input {
    width: 100%;
    padding: 8px 36px 8px 38px;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(0, 196, 154, 0.06);
    border-radius: 10px;
    color: #e8f0ee;
    font-size: 13px;
    outline: none;
    transition: all 0.3s;
}

.search-input:focus {
    border-color: rgba(0, 196, 154, 0.25);
    background: rgba(255, 255, 255, 0.04);
    box-shadow: 0 0 30px rgba(0, 196, 154, 0.04);
}

.search-hint {
    position: absolute;
    right: 12px;
    font-size: 10px;
    color: #3a5a52;
    background: rgba(255, 255, 255, 0.04);
    padding: 2px 8px;
    border-radius: 4px;
    border: 1px solid rgba(255, 255, 255, 0.04);
}

.sidebar-stats {
    padding: 10px 20px 14px;
    display: flex;
    gap: 14px;
    border-bottom: 1px solid rgba(0, 196, 154, 0.04);
    z-index: 1;
    position: relative;
}

.stat-item {
    display: flex;
    align-items: baseline;
    gap: 4px;
    flex: 1;
}

.stat-number {
    font-size: 16px;
    font-weight: 600;
    color: #e8f0ee;
}

.stat-label {
    font-size: 11px;
    color: #4a6a62;
}

.stat-divider {
    width: 1px;
    background: rgba(255, 255, 255, 0.04);
}

.sidebar-list {
    flex: 1;
    overflow-y: auto;
    padding: 6px 8px;
    position: relative;
    z-index: 1;
}

.sidebar-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 12px;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.25s ease;
    position: relative;
}

.sidebar-item:hover {
    background: rgba(0, 196, 154, 0.04);
}

.sidebar-item.active {
    background: rgba(0, 196, 154, 0.07);
}

.sidebar-item.active::before {
    content: '';
    position: absolute;
    left: 0;
    top: 6px;
    bottom: 6px;
    width: 3px;
    background: linear-gradient(180deg, #00c49a, #008b6e);
    border-radius: 0 4px 4px 0;
}

.sidebar-item.important .item-name {
    color: #ffd93d;
}

.item-avatar {
    position: relative;
    width: 34px;
    height: 34px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 700;
    color: #060a08;
    flex-shrink: 0;
    transition: transform 0.2s;
}

.sidebar-item:hover .item-avatar {
    transform: scale(1.05);
}

.avatar-ring {
    position: absolute;
    inset: -2px;
    border-radius: 12px;
    border: 2px solid rgba(255, 215, 0, 0.5);
    animation: ringPulse 2s ease-in-out infinite;
}

@keyframes ringPulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(1.05); }
}

.item-info {
    flex: 1;
    min-width: 0;
}

.item-name {
    font-size: 13px;
    color: #e8f0ee;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    font-weight: 500;
}

.item-meta {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 11px;
    color: #4a6a62;
}

.item-dot {
    width: 3px;
    height: 3px;
    border-radius: 50%;
    background: #3a5a52;
}

.item-rank {
    padding: 1px 10px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 700;
    color: #060a08;
}

.item-rank-small {
    padding: 1px 6px;
    border-radius: 8px;
    font-size: 10px;
    font-weight: 700;
    color: #060a08;
}

.loading-state {
    padding: 60px 0;
    display: flex;
    justify-content: center;
}

.loading-ring {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    border: 2px solid rgba(0, 196, 154, 0.08);
    border-top-color: #00c49a;
    animation: spin 0.8s cubic-bezier(0.6, 0, 0.4, 1) infinite;
}

.empty-state {
    padding: 60px 20px;
    text-align: center;
    color: #3a5a52;
    font-size: 13px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
}

.empty-state svg {
    opacity: 0.4;
}

.sidebar-footer {
    padding: 12px 16px;
    border-top: 1px solid rgba(0, 196, 154, 0.04);
    display: flex;
    gap: 8px;
    position: relative;
    z-index: 1;
}

.sidebar-footer.collapsed {
    flex-direction: column;
    align-items: center;
    gap: 8px;
    padding: 12px 8px;
}

.footer-btn {
    flex: 1;
    padding: 8px 12px;
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.04);
    border-radius: 10px;
    color: #5a7a72;
    cursor: pointer;
    font-size: 13px;
    transition: all 0.25s;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

.footer-btn:hover {
    border-color: rgba(0, 196, 154, 0.15);
    color: #e8f0ee;
}

.footer-btn.primary {
    background: linear-gradient(135deg, #00c49a, #008b6e);
    border: none;
    color: #060a08;
    font-weight: 600;
}

.footer-btn.primary:hover {
    box-shadow: 0 4px 24px rgba(0, 196, 154, 0.3);
    transform: translateY(-1px);
}

.sidebar-footer.collapsed .footer-btn {
    flex: none;
    width: 38px;
    height: 38px;
    padding: 0;
    border-radius: 10px;
}

/* Scrollbar */
.sidebar-list::-webkit-scrollbar {
    width: 2px;
}
.sidebar-list::-webkit-scrollbar-track {
    background: transparent;
}
.sidebar-list::-webkit-scrollbar-thumb {
    background: rgba(0, 196, 154, 0.2);
    border-radius: 4px;
}
.sidebar-list::-webkit-scrollbar-thumb:hover {
    background: rgba(0, 196, 154, 0.4);
}
</style>