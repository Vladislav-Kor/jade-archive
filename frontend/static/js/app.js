// API Configuration
const API = '/api';

// State
let currentPersonId = null;
let currentParentId = null;
let confirmCallback = null;
let expandedFolders = new Set();
let currentSortMode = 'importance';
let currentHierarchyView = false;
let currentDigitalAccountId = null;
// let currentCasePersonId = null;
// let currentMedicalPersonId = null;

// Utility Functions
function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/[&<>]/g, function (m) {
        if (m === '&') return '&amp;';
        if (m === '<') return '&lt;';
        if (m === '>') return '&gt;';
        return m;
    });
}

function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    if (!container) return;
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    let icon = type === 'success' ? 'fa-check-circle' : (type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle');
    toast.innerHTML = `<i class="fas ${icon}"></i><span class="toast-message">${escapeHtml(message)}</span>`;
    container.appendChild(toast);
    setTimeout(() => { toast.style.opacity = '0'; toast.style.transform = 'translateX(100px)'; setTimeout(() => toast.remove(), 300); }, 3000);
}

function showConfirm(message, callback) {
    confirmCallback = callback;
    document.getElementById('confirmMessage').textContent = message;
    openModal('confirmModal');
}

// API Functions
async function fetchAPI(endpoint, options = {}) {
    try {
        const res = await fetch(`${API}${endpoint}`, {
            headers: { 'Content-Type': 'application/json' },
            ...options
        });
        if (!res.ok) throw new Error(await res.text());
        return res.json();
    } catch (error) {
        showToast(error.message, 'error');
        throw error;
    }
}

// Modal Functions
function openModal(modalId) { const modal = document.getElementById(modalId); if (modal) { modal.style.display = 'flex'; modal.classList.add('active'); } }
function closeModal(modalId) { const modal = document.getElementById(modalId); if (modal) { modal.style.display = 'none'; modal.classList.remove('active'); } }

// Sorting
function initSorting() {
    document.querySelectorAll('.sort-btn').forEach(btn => {
        btn.addEventListener('click', async () => {
            const sortMode = btn.getAttribute('data-sort');
            document.querySelectorAll('.sort-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentSortMode = sortMode;
            currentHierarchyView = (sortMode === 'hierarchy');
            await loadTree();
        });
    });
}

// Load Tree
async function loadTree() {
    const treeContainer = document.getElementById('tree');
    if (!treeContainer) return;
    try {
        let tree;
        if (currentHierarchyView) {
            tree = await fetchAPI('/tree');
        } else {
            const persons = await fetchAPI('/persons');
            let sortedPersons = [...persons];
            if (currentSortMode === 'importance') sortedPersons.sort((a, b) => (b.importance || 0) - (a.importance || 0));
            else if (currentSortMode === 'date') sortedPersons.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
            else if (currentSortMode === 'name') sortedPersons.sort((a, b) => a.full_name.localeCompare(b.full_name));
            tree = { id: 0, name: 'Все контакты', short_name: 'all', importance: 0, importance_level: 'medium', children: sortedPersons.map(p => ({ id: p.id, name: p.full_name, short_name: p.short_name, importance: p.importance || 0, importance_level: p.importance_level || 'medium', children: [] })) };
        }
        renderTree(tree);
        await updateStats();
    } catch (e) { treeContainer.innerHTML = '<div class="text-center text-error p-4"><i class="fas fa-exclamation-triangle"></i> Ошибка загрузки</div>'; }
}

function renderTree(node, level = 0, container = null) {
    const mainContainer = document.getElementById('tree');
    if (!mainContainer) return;
    if (level === 0) {
        mainContainer.innerHTML = '';
        const totalCount = document.getElementById('totalCount')?.textContent || '0';
        const rootDiv = document.createElement('div');
        rootDiv.className = 'tree-node root-folder mb-2';
        rootDiv.innerHTML = `<div class="folder-tab" onclick="loadAllContacts()"><div class="folder-icon"><span class="folder-badge">${totalCount}</span></div><span class="folder-name">Все контакты</span><div class="folder-actions"><button class="action-btn" onclick="event.stopPropagation(); openPersonModal()"><i class="fas fa-plus"></i></button></div></div>`;
        mainContainer.appendChild(rootDiv);
        const divider = document.createElement('div');
        divider.className = 'h-px bg-gradient-to-r from-transparent via-[#00a884]/20 to-transparent my-3';
        mainContainer.appendChild(divider);
        container = mainContainer;
    }
    const hasChildren = node.children && node.children.length > 0;
    const isExpanded = expandedFolders.has(node.id);
    let importanceIcon = '';
    if (node.importance >= 8) importanceIcon = '<i class="fas fa-fire" style="color:#ff6b6b"></i>';
    else if (node.importance >= 6) importanceIcon = '<i class="fas fa-chart-line" style="color:#ffd93d"></i>';
    else if (node.importance >= 3) importanceIcon = '<i class="fas fa-star" style="color:#00a884"></i>';
    else if (node.importance > 0) importanceIcon = '<i class="fas fa-arrow-down" style="color:#b0b0b0"></i>';
    const nodeDiv = document.createElement('div');
    nodeDiv.className = `tree-node ${level > 0 ? 'subfolder' : ''}`;
    nodeDiv.style.marginLeft = level > 0 ? '16px' : '0';
    nodeDiv.innerHTML = `<div class="folder-tab ${hasChildren ? 'has-children' : ''}" onclick="loadPerson(${node.id})">${hasChildren ? `<div class="expand-icon ${isExpanded ? 'expanded' : ''}" onclick="event.stopPropagation(); toggleFolder(${node.id})"><i class="fas fa-chevron-right"></i></div>` : '<div style="width:20px"></div>'}<div class="folder-icon">${hasChildren ? `<span class="folder-badge">${node.children.length}</span>` : ''}</div><span class="folder-name">${escapeHtml(node.name)}</span>${importanceIcon ? `<span style="margin-left:auto; margin-right:8px">${importanceIcon}</span>` : ''}<div class="folder-actions"><button class="action-btn" onclick="event.stopPropagation(); openRelationModal(${node.id})"><i class="fas fa-link"></i></button><button class="action-btn" onclick="event.stopPropagation(); openPersonModal(${node.id})"><i class="fas fa-edit"></i></button></div></div>`;
    container.appendChild(nodeDiv);
    if (hasChildren && isExpanded) {
        const childrenContainer = document.createElement('div');
        childrenContainer.className = 'tree-children';
        container.appendChild(childrenContainer);
        node.children.forEach(child => renderTree(child, level + 1, childrenContainer));
    }
}

function toggleFolder(nodeId) {
    if (expandedFolders.has(nodeId)) expandedFolders.delete(nodeId);
    else expandedFolders.add(nodeId);
    loadTree();
}

// Load All Contacts
async function loadAllContacts() {
    try {
        const persons = await fetchAPI('/persons');
        document.getElementById('mainContent').innerHTML = `<div class="animate-in"><div class="dossier-card"><h2 style="font-size:20px; margin-bottom:20px"><i class="fas fa-address-book text-jade"></i> Все контакты (${persons.length})</h2><div style="display:grid; grid-template-columns:repeat(auto-fill, minmax(280px,1fr)); gap:12px">${persons.map(p => `<div class="folder-tab" onclick="loadPerson(${p.id})" style="cursor:pointer"><div class="folder-icon"></div><span class="folder-name">${escapeHtml(p.full_name)}</span><span style="font-size:11px; color:var(--text-muted)">@${escapeHtml(p.short_name)}</span></div>`).join('')}</div></div></div>`;
        document.querySelectorAll('.tree-node').forEach(n => n.classList.remove('selected'));
    } catch (e) { showToast('Ошибка загрузки контактов', 'error'); }
}

// Load Person
async function loadPerson(id) {
    currentPersonId = id;
    document.querySelectorAll('.tree-node').forEach(node => node.classList.remove('selected'));
    document.getElementById('mainContent').innerHTML = `<div class="skeleton" style="height:200px; margin-bottom:20px"></div><div class="skeleton" style="height:300px"></div>`;
    try {
        const person = await fetchAPI(`/persons/${id}`);
        displayPerson(person);
    } catch (e) { showToast('Ошибка загрузки контакта', 'error'); }
}

function formatGender(gender) {
    const genders = { male: 'Мужской', female: 'Женский', other: 'Другой' };
    return genders[gender] || 'Не указан';
}

function formatBloodType(type) {
    const types = { 'A+': 'A+ (II+)', 'A-': 'A- (II-)', 'B+': 'B+ (III+)', 'B-': 'B- (III-)', 'AB+': 'AB+ (IV+)', 'AB-': 'AB- (IV-)', 'O+': 'O+ (I+)', 'O-': 'O- (I-)' };
    return types[type] || type || 'Не указана';
}

function formatDate(date) {
    if (!date) return 'Не указана';
    return new Date(date).toLocaleDateString('ru-RU');
}

// ========================================
// DIGITAL ACCOUNTS FUNCTIONS
// ========================================

function getPlatformIcon(platform) {
    const icons = {
        steam: 'steam',
        discord: 'discord',
        epic: 'fort-awesome',
        genshin: 'genshin',
        ea: 'futbol',
        blizzard: 'snowflake',
        riot: 'bolt',
        microsoft: 'windows',
        sony: 'playstation',
        nintendo: 'nintendo-switch',
        ubisoft: 'ubi',
        rockstar: 'star',
        mobile: 'android',
        other: 'gamepad'
    };
    return icons[platform] || 'gamepad';
}

function getPlatformName(platform) {
    const names = {
        steam: 'Steam',
        discord: 'Discord',
        epic: 'Epic Games',
        genshin: 'Genshin Impact',
        ea: 'EA / Origin',
        blizzard: 'Blizzard (Battle.net)',
        riot: 'Riot Games',
        microsoft: 'Microsoft / Xbox',
        sony: 'Sony / PlayStation',
        nintendo: 'Nintendo',
        ubisoft: 'Ubisoft',
        rockstar: 'Rockstar',
        mobile: 'Мобильная игра',
        other: 'Другое'
    };
    return names[platform] || platform;
}

function openDigitalAccountModal(accountId = null) {
    currentDigitalAccountId = accountId;
    const form = document.getElementById('digitalAccountForm');
    const title = document.getElementById('digitalAccountModalTitle');
    
    if (form) form.reset();
    
    if (accountId) {
        if (title) title.innerHTML = '<i class="fas fa-edit"></i> Редактирование аккаунта';
        loadDigitalAccountForEdit(accountId);
    } else {
        if (title) title.innerHTML = '<i class="fas fa-gamepad"></i> Новый цифровой аккаунт';
        document.getElementById('digitalAccountId').value = '';
    }
    
    openModal('digitalAccountModal');
}

async function loadDigitalAccountForEdit(accountId) {
    try {
        const account = await fetchAPI(`/digital-accounts/${accountId}`);
        
        document.getElementById('digitalAccountId').value = account.id;
        document.getElementById('accountPlatformType').value = account.platform_type || '';
        document.getElementById('accountPlatformName').value = account.platform_name || '';
        document.getElementById('accountUsername').value = account.username || '';
        document.getElementById('accountEmail').value = account.email || '';
        document.getElementById('accountPhone').value = account.phone || '';
        document.getElementById('accountPassword').value = account.password || '';
        document.getElementById('accountBackupCodes').value = account.backup_codes || '';
        document.getElementById('accountSecurityQuestions').value = account.security_questions || '';
        
        // Новые поля для ID
        document.getElementById('accountAccountId').value = account.account_id || '';
        document.getElementById('accountUid').value = account.uid || '';
        document.getElementById('accountUserId').value = account.user_id || '';
        document.getElementById('accountFriendCode').value = account.friend_code || '';
        document.getElementById('accountServerId').value = account.server_id || '';
        document.getElementById('accountServerName').value = account.server_name || '';
        document.getElementById('accountRegion').value = account.region || '';
        
        document.getElementById('accountNickname').value = account.nickname || '';
        document.getElementById('accountServer').value = account.server || '';
        document.getElementById('accountLevel').value = account.level || '';
        document.getElementById('accountRank').value = account.rank || '';
        document.getElementById('accountGuild').value = account.guild || '';
        document.getElementById('accountCharacters').value = account.characters || '';
        document.getElementById('accountNotes').value = account.notes || '';
        document.getElementById('accountIsActive').value = account.is_active ? 'true' : 'false';
        
    } catch (error) {
        showToast('Ошибка загрузки аккаунта', 'error');
    }
}

async function saveDigitalAccount() {
    const accountData = {
        platform_type: document.getElementById('accountPlatformType').value,
        platform_name: document.getElementById('accountPlatformName').value,
        username: document.getElementById('accountUsername').value,
        email: document.getElementById('accountEmail').value,
        phone: document.getElementById('accountPhone').value,
        password: document.getElementById('accountPassword').value,
        backup_codes: document.getElementById('accountBackupCodes').value,
        security_questions: document.getElementById('accountSecurityQuestions').value,
        
        // Новые поля для ID
        account_id: document.getElementById('accountAccountId').value,
        uid: document.getElementById('accountUid').value,
        user_id: document.getElementById('accountUserId').value,
        friend_code: document.getElementById('accountFriendCode').value,
        server_id: document.getElementById('accountServerId').value,
        server_name: document.getElementById('accountServerName').value,
        region: document.getElementById('accountRegion').value,
        
        nickname: document.getElementById('accountNickname').value,
        server: document.getElementById('accountServer').value,
        level: parseInt(document.getElementById('accountLevel').value) || null,
        rank: document.getElementById('accountRank').value,
        guild: document.getElementById('accountGuild').value,
        characters: document.getElementById('accountCharacters').value,
        notes: document.getElementById('accountNotes').value,
        is_active: document.getElementById('accountIsActive').value === 'true'
    };
    
    // Валидация
    if (!accountData.platform_type) {
        showToast('Выберите платформу', 'error');
        return;
    }
    if (!accountData.platform_name) {
        accountData.platform_name = accountData.platform_type;
    }
    
    try {
        let url, method;
        
        if (currentDigitalAccountId) {
            url = `${API}/digital-accounts/${currentDigitalAccountId}`;
            method = 'PUT';
        } else {
            url = `${API}/persons/${currentPersonId}/digital-accounts`;
            method = 'POST';
        }
        
        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(accountData)
        });
        
        if (!response.ok) throw new Error(await response.text());
        
        closeModal('digitalAccountModal');
        await loadPerson(currentPersonId);
        showToast(currentDigitalAccountId ? 'Аккаунт обновлен' : 'Аккаунт добавлен', 'success');
        
    } catch (error) {
        showToast('Ошибка при сохранении: ' + error.message, 'error');
    }
}

async function deleteDigitalAccount(accountId) {
    showConfirm('Удалить этот аккаунт?', async () => {
        try {
            const response = await fetch(`${API}/digital-accounts/${accountId}`, {
                method: 'DELETE'
            });
            
            if (!response.ok) throw new Error(await response.text());
            
            await loadPerson(currentPersonId);
            showToast('Аккаунт удален', 'success');
            closeModal('confirmModal');
            
        } catch (error) {
            showToast('Ошибка при удалении', 'error');
        }
    });
}

function togglePasswordVisibility(fieldId) {
    const field = document.getElementById(fieldId);
    if (!field) return;
    
    const type = field.type === 'password' ? 'text' : 'password';
    field.type = type;
    
    const button = field.nextElementSibling;
    if (button) {
        const icon = button.querySelector('i');
        if (icon) {
            icon.classList.toggle('fa-eye');
            icon.classList.toggle('fa-eye-slash');
        }
    }
}

// ========================================
// DISPLAY PERSON WITH DIGITAL ACCOUNTS
// ========================================

function displayPerson(p) {
    const age = p.birth_date ? new Date().getFullYear() - new Date(p.birth_date).getFullYear() : null;
    
    // Digital Accounts HTML
    const digitalAccountsHtml = p.digital_accounts?.length ? 
        p.digital_accounts.map(acc => `
            <div class="digital-account-item p-3 rounded-xl mb-2" style="background: rgba(0, 59, 49, 0.3); border: 1px solid rgba(0, 168, 132, 0.15);">
                <div class="flex justify-between items-start">
                    <div class="flex-1">
                        <div class="flex items-center gap-2 mb-2 flex-wrap">
                            <i class="fab fa-${getPlatformIcon(acc.platform_type)} text-xl text-[#00a884]"></i>
                            <strong class="text-[#00a884]">${escapeHtml(acc.platform_name || getPlatformName(acc.platform_type))}</strong>
                            ${acc.is_active ? '<span class="badge" style="background: rgba(0,168,132,0.2); color: #00a884;">Активен</span>' : '<span class="badge" style="background: rgba(255,107,107,0.2); color: #ff6b6b;">Неактивен</span>'}
                        </div>
                        ${acc.username ? `<div class="text-sm"><i class="fas fa-user w-5 text-[#00a884]"></i> ${escapeHtml(acc.username)}</div>` : ''}
                        ${acc.email ? `<div class="text-sm"><i class="fas fa-envelope w-5 text-[#00a884]"></i> ${escapeHtml(acc.email)}</div>` : ''}
                        ${acc.account_id ? `<div class="text-sm"><i class="fas fa-id-badge w-5 text-[#00a884]"></i> Account ID: <code class="bg-[#001a15] px-2 py-1 rounded">${escapeHtml(acc.account_id)}</code></div>` : ''}
                        ${acc.uid ? `<div class="text-sm"><i class="fas fa-qrcode w-5 text-[#00a884]"></i> UID: <code class="bg-[#001a15] px-2 py-1 rounded">${escapeHtml(acc.uid)}</code></div>` : ''}
                        ${acc.user_id ? `<div class="text-sm"><i class="fas fa-user-circle w-5 text-[#00a884]"></i> User ID: ${escapeHtml(acc.user_id)}</div>` : ''}
                        ${acc.friend_code ? `<div class="text-sm"><i class="fas fa-user-plus w-5 text-[#00a884]"></i> Friend Code: <code class="bg-[#001a15] px-2 py-1 rounded">${escapeHtml(acc.friend_code)}</code></div>` : ''}
                        ${acc.server_id ? `<div class="text-sm"><i class="fas fa-server w-5 text-[#00a884]"></i> Server ID: ${escapeHtml(acc.server_id)}</div>` : ''}
                        ${acc.server_name ? `<div class="text-sm"><i class="fas fa-globe w-5 text-[#00a884]"></i> Server: ${escapeHtml(acc.server_name)}</div>` : ''}
                        ${acc.region ? `<div class="text-sm"><i class="fas fa-map-marker-alt w-5 text-[#00a884]"></i> Регион: ${escapeHtml(acc.region)}</div>` : ''}
                        ${acc.nickname ? `<div class="text-sm"><i class="fas fa-gamepad w-5 text-[#00a884]"></i> Ник: ${escapeHtml(acc.nickname)}</div>` : ''}
                        ${acc.level ? `<div class="text-sm"><i class="fas fa-chart-line w-5 text-[#00a884]"></i> Уровень: ${acc.level}</div>` : ''}
                        ${acc.rank ? `<div class="text-sm"><i class="fas fa-medal w-5 text-[#00a884]"></i> Ранг: ${escapeHtml(acc.rank)}</div>` : ''}
                        ${acc.guild ? `<div class="text-sm"><i class="fas fa-users w-5 text-[#00a884]"></i> Гильдия: ${escapeHtml(acc.guild)}</div>` : ''}
                        ${acc.server ? `<div class="text-sm"><i class="fas fa-server w-5 text-[#00a884]"></i> Сервер: ${escapeHtml(acc.server)}</div>` : ''}
                        ${acc.characters ? `<div class="text-sm"><i class="fas fa-user-friends w-5 text-[#00a884]"></i> Персонажи: ${escapeHtml(acc.characters)}</div>` : ''}
                        ${acc.notes ? `<div class="text-xs text-[#e0f2f1]/50 mt-1"><i class="fas fa-sticky-note"></i> ${escapeHtml(acc.notes)}</div>` : ''}
                    </div>
                    <div class="flex gap-1">
                        <button class="action-btn" onclick="openDigitalAccountModal(${acc.id})" title="Редактировать">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="action-btn text-red-400" onclick="deleteDigitalAccount(${acc.id})" title="Удалить">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
                ${acc.password || acc.backup_codes || acc.security_questions || acc.characters ? `
                <details class="mt-2">
                    <summary class="text-xs text-[#e0f2f1]/40 cursor-pointer hover:text-[#00a884]">
                        🔒 Показать чувствительные данные
                    </summary>
                    <div class="mt-2 space-y-1 text-sm border-t border-[#00a884]/20 pt-2">
                        ${acc.password ? `<div><i class="fas fa-key text-[#00a884] w-5"></i> Пароль: <code class="bg-[#001a15] px-2 py-1 rounded text-xs">${escapeHtml(acc.password)}</code></div>` : ''}
                        ${acc.backup_codes ? `<div><i class="fas fa-ticket-alt text-[#00a884] w-5"></i> Резервные коды:<br><code class="bg-[#001a15] px-2 py-1 rounded text-xs block mt-1 whitespace-pre-wrap">${escapeHtml(acc.backup_codes)}</code></div>` : ''}
                        ${acc.security_questions ? `<div><i class="fas fa-question-circle text-[#00a884] w-5"></i> Секретные вопросы:<br><code class="bg-[#001a15] px-2 py-1 rounded text-xs block mt-1">${escapeHtml(acc.security_questions)}</code></div>` : ''}
                        ${acc.characters ? `<div><i class="fas fa-user-friends text-[#00a884] w-5"></i> Персонажи:<br><code class="bg-[#001a15] px-2 py-1 rounded text-xs block mt-1">${escapeHtml(acc.characters)}</code></div>` : ''}
                    </div>
                </details>
                ` : ''}
            </div>
        `).join('') : 
        '<div class="text-center text-[#e0f2f1]/40 py-4"><i class="fas fa-gamepad mr-2"></i>Нет добавленных аккаунтов</div>';
    
    document.getElementById('mainContent').innerHTML = `
    <div class="animate-in">
        <!-- Header -->
        <div class="dossier-card"><div class="dossier-header"><div style="display:flex; gap:20px; align-items:center"><div class="avatar">👤</div><div><h2>${escapeHtml(p.full_name)}</h2><div class="dossier-badges"><span class="badge">@${escapeHtml(p.short_name)}</span>${age ? `<span class="badge"><i class="fas fa-birthday-cake"></i> ${age} лет</span>` : ''}</div></div></div><div class="dossier-actions"><button class="btn-secondary" onclick="openPersonModal(${p.id})"><i class="fas fa-edit"></i> Редактировать</button><button class="btn-danger" onclick="deletePerson(${p.id})"><i class="fas fa-trash"></i> Удалить</button></div></div></div>
        
        <!-- Основная информация -->
        <div class="dossier-card"><h3><i class="fas fa-info-circle"></i> Основная информация</h3><div class="info-grid"><div class="info-item"><div class="info-icon"><i class="fas fa-calendar"></i></div><div><div class="info-label">Дата рождения</div><div class="info-value">${formatDate(p.birth_date)}</div></div></div><div class="info-item"><div class="info-icon"><i class="fas fa-venus-mars"></i></div><div><div class="info-label">Пол</div><div class="info-value">${formatGender(p.gender)}</div></div></div><div class="info-item"><div class="info-icon"><i class="fas fa-phone"></i></div><div><div class="info-label">Телефон</div><div class="info-value">${p.phone || 'Не указан'}</div></div></div><div class="info-item"><div class="info-icon"><i class="fas fa-envelope"></i></div><div><div class="info-label">Email</div><div class="info-value">${p.email || 'Не указан'}</div></div></div><div class="info-item full-width"><div class="info-icon"><i class="fas fa-map-marker-alt"></i></div><div><div class="info-label">Адрес</div><div class="info-value">${p.address || 'Не указан'}</div></div></div></div></div>
        
        <!-- Параметры тела -->
        <div class="dossier-card"><h3><i class="fas fa-ruler"></i> Параметры тела</h3><div class="info-grid"><div class="info-item"><div class="info-icon"><i class="fas fa-arrow-up"></i></div><div><div class="info-label">Рост</div><div class="info-value">${p.height ? p.height + ' см' : 'Не указан'}</div></div></div><div class="info-item"><div class="info-icon"><i class="fas fa-weight-hanging"></i></div><div><div class="info-label">Вес</div><div class="info-value">${p.weight ? p.weight + ' кг' : 'Не указан'}</div></div></div><div class="info-item"><div class="info-icon"><i class="fas fa-tshirt"></i></div><div><div class="info-label">Размер одежды</div><div class="info-value">${p.clothing_size || 'Не указан'}</div></div></div><div class="info-item"><div class="info-icon"><i class="fas fa-shoe-prints"></i></div><div><div class="info-label">Размер обуви</div><div class="info-value">${p.shoe_size || 'Не указан'}</div></div></div><div class="info-item"><div class="info-icon"><i class="fas fa-arrows-alt-h"></i></div><div><div class="info-label">Грудь/Талия/Бедра</div><div class="info-value">${p.chest_size || '?'}/${p.waist_size || '?'}/${p.hip_size || '?'}</div></div></div></div></div>
        
        <!-- Медицинские данные -->
        <div class="dossier-card"><h3><i class="fas fa-heartbeat"></i> Медицинские данные</h3><div class="info-grid"><div class="info-item"><div class="info-icon"><i class="fas fa-tint"></i></div><div><div class="info-label">Группа крови</div><div class="info-value">${formatBloodType(p.blood_type)}${p.rh_factor === 'positive' ? ' +' : (p.rh_factor === 'negative' ? ' -' : '')}</div></div></div><div class="info-item"><div class="info-icon"><i class="fas fa-tachometer-alt"></i></div><div><div class="info-label">Давление / Пульс</div><div class="info-value">${p.blood_pressure || '?'} / ${p.heart_rate || '?'}</div></div></div><div class="info-item full-width"><div class="info-icon"><i class="fas fa-allergies"></i></div><div><div class="info-label">Аллергии</div><div class="info-value">${p.allergies || 'Нет'}</div></div></div><div class="info-item full-width"><div class="info-icon"><i class="fas fa-disease"></i></div><div><div class="info-label">Хронические заболевания</div><div class="info-value">${p.chronic_diseases || 'Нет'}</div></div></div><div class="info-item full-width"><div class="info-icon"><i class="fas fa-capsules"></i></div><div><div class="info-label">Принимаемые лекарства</div><div class="info-value">${p.medications || 'Нет'}</div></div></div></div><div style="margin-top:16px"><button class="btn-secondary" onclick="openMedicalModal(${p.id})"><i class="fas fa-plus"></i> Добавить мед. запись</button></div></div>
        
        <!-- Документы -->
        <div class="dossier-card"><h3><i class="fas fa-id-card"></i> Документы</h3><div class="info-grid"><div class="info-item"><div class="info-icon"><i class="fas fa-passport"></i></div><div><div class="info-label">Паспорт</div><div class="info-value">${p.passport_number || 'Не указан'}</div></div></div><div class="info-item"><div class="info-icon"><i class="fas fa-file-invoice"></i></div><div><div class="info-label">ИНН</div><div class="info-value">${p.inn || 'Не указан'}</div></div></div><div class="info-item"><div class="info-icon"><i class="fas fa-file-contract"></i></div><div><div class="info-label">СНИЛС</div><div class="info-value">${p.snils || 'Не указан'}</div></div></div><div class="info-item"><div class="info-icon"><i class="fas fa-car"></i></div><div><div class="info-label">Водительские права</div><div class="info-value">${p.driver_license_category || '?'} ${p.driver_license_number || ''}</div></div></div></div></div>
        
        <!-- Социальные параметры -->
        <div class="dossier-card"><h3><i class="fas fa-users"></i> Социальные параметры</h3><div class="info-grid"><div class="info-item"><div class="info-icon"><i class="fas fa-ring"></i></div><div><div class="info-label">Семейное положение</div><div class="info-value">${p.marital_status === 'single' ? 'Холост/Не замужем' : (p.marital_status === 'married' ? 'Женат/Замужем' : (p.marital_status === 'divorced' ? 'Разведен(а)' : (p.marital_status === 'widowed' ? 'Вдовец/Вдова' : 'Не указано')))}</div></div></div><div class="info-item"><div class="info-icon"><i class="fas fa-child"></i></div><div><div class="info-label">Дети</div><div class="info-value">${p.children_count || '0'}</div></div></div><div class="info-item"><div class="info-icon"><i class="fas fa-graduation-cap"></i></div><div><div class="info-label">Образование</div><div class="info-value">${p.education || 'Не указано'}</div></div></div><div class="info-item"><div class="info-icon"><i class="fas fa-briefcase"></i></div><div><div class="info-label">Профессия</div><div class="info-value">${p.profession || 'Не указана'}</div></div></div><div class="info-item full-width"><div class="info-icon"><i class="fas fa-building"></i></div><div><div class="info-label">Место работы</div><div class="info-value">${p.workplace || 'Не указано'}</div></div></div></div></div>
        
        <!-- Предпочтения -->
        <div class="dossier-card"><h3><i class="fas fa-heart"></i> Предпочтения</h3><div class="info-grid"><div class="info-item"><div class="info-icon"><i class="fas fa-palette"></i></div><div><div class="info-label">Любимый цвет</div><div class="info-value">${p.favorite_color || 'Не указан'}</div></div></div><div class="info-item"><div class="info-icon"><i class="fas fa-seedling"></i></div><div><div class="info-label">Любимые цветы</div><div class="info-value">${p.favorite_flowers || 'Не указаны'}</div></div></div><div class="info-item"><div class="info-icon"><i class="fas fa-utensils"></i></div><div><div class="info-label">Любимая еда</div><div class="info-value">${p.favorite_food || 'Не указана'}</div></div></div><div class="info-item"><div class="info-icon"><i class="fas fa-music"></i></div><div><div class="info-label">Любимая музыка</div><div class="info-value">${p.favorite_music || 'Не указана'}</div></div></div><div class="info-item"><div class="info-icon"><i class="fas fa-film"></i></div><div><div class="info-label">Любимые фильмы</div><div class="info-value">${p.favorite_movies || 'Не указаны'}</div></div></div><div class="info-item"><div class="info-icon"><i class="fas fa-gamepad"></i></div><div><div class="info-label">Хобби</div><div class="info-value">${p.hobbies || 'Не указаны'}</div></div></div></div></div>
        
        <!-- Социальные сети -->
        <div class="dossier-card"><h3><i class="fas fa-share-alt"></i> Социальные сети</h3>${p.social_media?.length ? p.social_media.map(sm => `<div class="social-item"><div><i class="fab fa-${sm.platform.toLowerCase()}"></i> <strong>${escapeHtml(sm.platform)}</strong></div><div><a href="${escapeHtml(sm.link)}" target="_blank" class="social-link">${escapeHtml(sm.link)}</a></div><button class="action-btn" onclick="deleteSocialMedia(${sm.id})"><i class="fas fa-trash"></i></button></div>`).join('') : '<div style="text-align:center; padding:20px">Нет добавленных соцсетей</div>'}<div style="margin-top:16px"><button class="btn-secondary" onclick="openSocialModal(${p.id})"><i class="fas fa-plus"></i> Добавить соцсеть</button></div></div>
        
        <!-- Цифровые аккаунты (игры, Discord, Steam и др.) -->
        <div class="dossier-card">
            <div class="flex justify-between items-center mb-4">
                <h3><i class="fas fa-gamepad"></i> Цифровые аккаунты</h3>
                <button class="btn-secondary text-sm" onclick="openDigitalAccountModal()">
                    <i class="fas fa-plus"></i> Добавить аккаунт
                </button>
            </div>
            <div id="digitalAccountsList" class="space-y-3">
                ${digitalAccountsHtml}
            </div>
        </div>
        
        <!-- Заметки -->
        <div class="dossier-card"><h3><i class="fas fa-sticky-note"></i> Заметки</h3><p>${p.notes || 'Нет заметок'}</p></div>
    </div>`;
    
    document.querySelectorAll('.tree-node').forEach(node => { 
        node.classList.remove('selected'); 
        if (node.querySelector(`[onclick="loadPerson(${p.id})"]`)) node.classList.add('selected'); 
    });
}

// CRUD Operations
async function deletePerson(id) {
    showConfirm('Удалить контакт?', async () => {
        await fetchAPI(`/persons/${id}`, { method: 'DELETE' });
        await loadTree();
        if (currentPersonId === id) document.getElementById('mainContent').innerHTML = '<div class="welcome-screen"><div class="welcome-icon"><i class="fas fa-trash"></i><div class="welcome-pulse"></div></div><h2>Контакт удален</h2><p>Выберите другой контакт</p></div>';
        showToast('Контакт удален', 'success');
        closeModal('confirmModal');
    });
}

async function deleteSocialMedia(socialId) {
    showConfirm('Удалить соцсеть?', async () => {
        await fetchAPI(`/social/${socialId}`, { method: 'DELETE' });
        if (currentPersonId) await loadPerson(currentPersonId);
        showToast('Удалено', 'success');
        closeModal('confirmModal');
    });
}

// Показать существующие связи при добавлении новой
async function openRelationModal(parentId) {
    currentParentId = parentId;
    
    try {
        // Загружаем список всех контактов
        const persons = await fetchAPI('/persons');
        // Загружаем существующие связи
        const existingRelations = await fetchAPI(`/persons/${parentId}/relations`);
        
        // Фильтруем контакты, исключая уже связанных
        const linkedPersonIds = existingRelations.map(r => r.person_id);
        const otherPersons = persons.filter(p => p.id !== parentId && !linkedPersonIds.includes(p.id));
        
        if (otherPersons.length === 0) {
            showToast('Нет доступных контактов для связи (все уже связаны)', 'error');
            return;
        }
        
        const select = document.getElementById('relationChildId');
        if (!select) return;
        
        select.innerHTML = '<option value="">-- Выберите контакт --</option>';
        otherPersons.forEach(person => {
            const option = document.createElement('option');
            option.value = person.id;
            option.textContent = `${person.full_name} (@${person.short_name})`;
            select.appendChild(option);
        });
        
        // Показываем существующие связи
        if (existingRelations.length > 0) {
            const relationInfo = document.createElement('div');
            relationInfo.className = 'mt-4 p-3 bg-[#001a15]/50 rounded-xl text-sm';
            relationInfo.innerHTML = '<div class="text-[#00a884] mb-2"><i class="fas fa-link"></i> Существующие связи:</div>';
            existingRelations.forEach(rel => {
                const directionIcon = rel.direction === 'outgoing' ? '→' : '←';
                relationInfo.innerHTML += `<div class="text-[#e0f2f1]/70 text-xs">${directionIcon} ${rel.person_name} (${rel.relation_type})</div>`;
            });
            
            // Добавляем информацию в модальное окно, если её там нет
            const modalBody = document.querySelector('#relationModal .modal-body');
            const existingInfo = modalBody.querySelector('.existing-relations-info');
            if (!existingInfo) {
                relationInfo.className += ' existing-relations-info';
                modalBody.appendChild(relationInfo);
            }
        }
        
        document.getElementById('relationType').value = '';
        openModal('relationModal');
    } catch (error) {
        showToast('Ошибка загрузки списка', 'error');
    }
}

// Person Modal
async function openPersonModal(personId = null) {
    const modal = document.getElementById('personModal');
    const form = document.getElementById('personForm');
    const title = document.getElementById('personModalTitle');
    const importanceSlider = document.getElementById('importanceSlider');
    const importanceValue = document.getElementById('importanceValue');
    const importanceLevelSelect = document.getElementById('importanceLevelSelect');
    
    if (!modal || !form) {
        console.error('Modal elements not found');
        return;
    }
    
    // Reset form
    form.reset();
    
    // Set default values
    if (importanceSlider) importanceSlider.value = 5;
    if (importanceValue) importanceValue.textContent = '5';
    if (importanceLevelSelect) importanceLevelSelect.value = 'medium';
    
    if (personId) {
        // Edit mode
        title.innerHTML = '<i class="fas fa-edit"></i> Редактирование контакта';
        
        try {
            const person = await fetchAPI(`/persons/${personId}`);
            
            // Fill form fields
            form.full_name.value = person.full_name || '';
            form.short_name.value = person.short_name || '';
            form.birth_date.value = person.birth_date || '';
            form.gender.value = person.gender || '';
            form.address.value = person.address || '';
            form.phone.value = person.phone || '';
            form.email.value = person.email || '';
            form.height.value = person.height || '';
            form.weight.value = person.weight || '';
            form.clothing_size.value = person.clothing_size || '';
            form.shoe_size.value = person.shoe_size || '';
            form.chest_size.value = person.chest_size || '';
            form.waist_size.value = person.waist_size || '';
            form.hip_size.value = person.hip_size || '';
            form.blood_type.value = person.blood_type || '';
            form.rh_factor.value = person.rh_factor || '';
            form.allergies.value = person.allergies || '';
            form.chronic_diseases.value = person.chronic_diseases || '';
            form.medications.value = person.medications || '';
            form.blood_pressure.value = person.blood_pressure || '';
            form.heart_rate.value = person.heart_rate || '';
            form.passport_number.value = person.passport_number || '';
            form.inn.value = person.inn || '';
            form.snils.value = person.snils || '';
            form.driver_license_category.value = person.driver_license_category || '';
            form.driver_license_number.value = person.driver_license_number || '';
            form.marital_status.value = person.marital_status || '';
            form.children_count.value = person.children_count || 0;
            form.education.value = person.education || '';
            form.profession.value = person.profession || '';
            form.workplace.value = person.workplace || '';
            form.favorite_color.value = person.favorite_color || '';
            form.favorite_flowers.value = person.favorite_flowers || '';
            form.favorite_food.value = person.favorite_food || '';
            form.favorite_music.value = person.favorite_music || '';
            form.favorite_movies.value = person.favorite_movies || '';
            form.hobbies.value = person.hobbies || '';
            form.notes.value = person.notes || '';
            
            // Importance
            const importance = person.importance || 5;
            if (importanceSlider) importanceSlider.value = importance;
            if (importanceValue) importanceValue.textContent = importance;
            if (importanceLevelSelect) {
                if (importance <= 2) importanceLevelSelect.value = 'low';
                else if (importance <= 5) importanceLevelSelect.value = 'medium';
                else if (importance <= 8) importanceLevelSelect.value = 'high';
                else importanceLevelSelect.value = 'critical';
            }
            
        } catch (error) {
            showToast('Ошибка загрузки контакта', 'error');
            return;
        }
        
        // Submit handler for edit
        form.onsubmit = async (e) => {
            e.preventDefault();
            
            // Collect form data
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            
            // Fix children_count
            if (data.children_count === '' || data.children_count === null || data.children_count === undefined) {
                data.children_count = 0;
            } else {
                data.children_count = parseInt(data.children_count);
            }
            
            // Fix other numeric fields
            const numberFields = ['height', 'weight', 'shoe_size', 'chest_size', 'waist_size', 'hip_size', 'heart_rate'];
            numberFields.forEach(field => {
                if (data[field] === '' || data[field] === null || data[field] === undefined) {
                    data[field] = null;
                } else {
                    const num = parseInt(data[field]);
                    data[field] = isNaN(num) ? null : num;
                }
            });
            
            // Fix importance
            let importance = 5;
            if (importanceSlider) {
                importance = parseInt(importanceSlider.value);
            } else if (data.importance) {
                importance = parseFloat(data.importance);
            }
            data.importance = isNaN(importance) ? 5 : importance;
            
            // Fix importance_level
            if (importanceLevelSelect) {
                data.importance_level = importanceLevelSelect.value;
            }
            
            try {
                await fetchAPI(`/persons/${personId}`, {
                    method: 'PUT',
                    body: JSON.stringify(data)
                });
                closeModal('personModal');
                await loadTree();
                await loadPerson(personId);
                showToast('Контакт обновлен', 'success');
            } catch (error) {
                showToast('Ошибка при обновлении: ' + error.message, 'error');
            }
        };
        
    } else {
        // Create mode
        title.innerHTML = '<i class="fas fa-user-plus"></i> Новый контакт';
        
        // Submit handler for create
        form.onsubmit = async (e) => {
            e.preventDefault();
            
            // Collect form data
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            
            // Validate required fields
            if (!data.full_name || !data.short_name) {
                showToast('Заполните обязательные поля (Полное имя и Короткое имя)', 'error');
                return;
            }
            
            // Fix children_count
            if (data.children_count === '' || data.children_count === null || data.children_count === undefined) {
                data.children_count = 0;
            } else {
                data.children_count = parseInt(data.children_count);
            }
            
            // Fix other numeric fields
            const numberFields = ['height', 'weight', 'shoe_size', 'chest_size', 'waist_size', 'hip_size', 'heart_rate'];
            numberFields.forEach(field => {
                if (data[field] === '' || data[field] === null || data[field] === undefined) {
                    data[field] = null;
                } else {
                    const num = parseInt(data[field]);
                    data[field] = isNaN(num) ? null : num;
                }
            });
            
            // Fix importance
            let importance = 5;
            if (importanceSlider) {
                importance = parseInt(importanceSlider.value);
            } else if (data.importance) {
                importance = parseFloat(data.importance);
            }
            data.importance = isNaN(importance) ? 5 : importance;
            
            // Fix importance_level
            if (importanceLevelSelect) {
                data.importance_level = importanceLevelSelect.value;
            }
            
            try {
                await fetchAPI('/persons', {
                    method: 'POST',
                    body: JSON.stringify(data)
                });
                closeModal('personModal');
                await loadTree();
                showToast('Контакт добавлен', 'success');
            } catch (error) {
                showToast('Ошибка при добавлении: ' + error.message, 'error');
            }
        };
    }
    
    // Show modal
    openModal('personModal');
}

// Social Modal
let currentSocialPersonId = null;
function openSocialModal(personId) { currentSocialPersonId = personId; openModal('socialModal'); }
document.getElementById('socialForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const platform = document.getElementById('socialPlatform').value.trim();
    const link = document.getElementById('socialLink').value.trim();
    if (!platform || !link) { showToast('Заполните поля', 'error'); return; }
    await fetchAPI(`/persons/${currentSocialPersonId}/social`, { method: 'POST', body: JSON.stringify({ platform, link }) });
    closeModal('socialModal');
    await loadPerson(currentSocialPersonId);
    showToast('Соцсеть добавлена', 'success');
});

// Digital Account Form Submit
document.getElementById('digitalAccountForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    await saveDigitalAccount();
});

// Case Modal
let currentCasePersonId = null;
function openCaseModal(personId) { currentCasePersonId = personId; openModal('caseModal'); }
document.getElementById('caseForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = { case_type: document.getElementById('caseType').value, title: document.getElementById('caseTitle').value, description: document.getElementById('caseDescription').value, priority: document.getElementById('casePriority').value, due_date: document.getElementById('caseDueDate').value };
    await fetchAPI(`/persons/${currentCasePersonId}/cases`, { method: 'POST', body: JSON.stringify(data) });
    closeModal('caseModal');
    await loadPerson(currentCasePersonId);
    showToast('Дело добавлено', 'success');
});

// Medical Modal
let currentMedicalPersonId = null;
function openMedicalModal(personId) { currentMedicalPersonId = personId; openModal('medicalModal'); }
document.getElementById('medicalForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = { record_type: document.getElementById('medicalType').value, title: document.getElementById('medicalTitle').value, description: document.getElementById('medicalDescription').value, record_date: document.getElementById('medicalDate').value, doctor_name: document.getElementById('medicalDoctor').value };
    await fetchAPI(`/persons/${currentMedicalPersonId}/medical`, { method: 'POST', body: JSON.stringify(data) });
    closeModal('medicalModal');
    await loadPerson(currentMedicalPersonId);
    showToast('Мед. запись добавлена', 'success');
});

// Stats
async function updateStats() {
    try {
        const persons = await fetchAPI('/persons');
        const relations = await fetchAPI('/relations');
        document.getElementById('totalCount').textContent = persons.length;
        document.getElementById('relationsCount').textContent = relations?.length || 0;
        
        let accountsCount = 0;
        for (const p of persons.slice(0, 10)) { 
            const full = await fetchAPI(`/persons/${p.id}`); 
            accountsCount += full.digital_accounts?.length || 0;
        }
        document.getElementById('accountsCount').textContent = accountsCount;
    } catch (e) { console.error(e); }
}

// Search
let searchTimeout;
document.getElementById('searchInput')?.addEventListener('input', async (e) => {
    clearTimeout(searchTimeout);
    const query = e.target.value;
    if (query.length < 2) { loadTree(); return; }
    searchTimeout = setTimeout(async () => {
        const results = await fetchAPI(`/search?q=${encodeURIComponent(query)}`);
        document.getElementById('tree').innerHTML = `<div class="p-2 text-jade text-xs">Найдено: ${results.length}</div>${results.map(p => `<div class="tree-node mb-1"><div class="folder-tab" onclick="loadPerson(${p.id})"><div class="folder-icon"></div><span class="folder-name">${escapeHtml(p.full_name)}</span><span class="text-muted text-xs">@${escapeHtml(p.short_name)}</span></div></div>`).join('')}`;
    }, 300);
});

// Mobile Menu
document.getElementById('mobileMenuToggle')?.addEventListener('click', () => document.getElementById('sidebar')?.classList.toggle('open'));

// Relation Form Submit
document.getElementById('relationForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const childId = document.getElementById('relationChildId').value;
    const relationType = document.getElementById('relationType').value.trim();
    if (!childId || !relationType) { showToast('Заполните поля', 'error'); return; }
    await fetchAPI('/relations', { method: 'POST', body: JSON.stringify({ parent_id: currentParentId, child_id: parseInt(childId), relation_type: relationType }) });
    closeModal('relationModal');
    await loadTree();
    showToast('Связь добавлена', 'success');
});

// Confirm Action
document.getElementById('confirmActionBtn')?.addEventListener('click', () => { if (confirmCallback) { confirmCallback(); confirmCallback = null; } });

// Platform buttons
document.querySelectorAll('.platform-btn').forEach(btn => btn.addEventListener('click', () => document.getElementById('socialPlatform').value = btn.getAttribute('data-platform')));

// Importance slider
const impSlider = document.getElementById('importanceSlider');
const impValue = document.getElementById('importanceValue');
if (impSlider && impValue) impSlider.addEventListener('input', (e) => impValue.innerText = e.target.value);

// Initialize
document.addEventListener('DOMContentLoaded', () => { initSorting(); loadTree(); });