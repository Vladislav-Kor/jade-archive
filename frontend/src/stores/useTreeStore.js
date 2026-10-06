import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { personsApi } from '@/api/endpoints/persons';
import { relationsApi } from '@/api/endpoints/relations';

export const useTreeStore = defineStore('tree', () => {
    const persons = ref([]);
    const relations = ref([]);
    const isLoading = ref(false);
    const error = ref(null);
    const selectedPersonId = ref(null);
    const searchQuery = ref('');
    const sortMode = ref('importance'); // 'importance', 'name', 'hierarchy'
    const expandedNodes = ref(new Set());

    const loadPersons = async () => {
        isLoading.value = true;
        try {
            persons.value = await personsApi.getAll();
        } catch (err) {
            error.value = err.message || 'Ошибка загрузки';
        } finally {
            isLoading.value = false;
        }
    };

    const loadRelations = async () => {
        try {
            relations.value = await relationsApi.getAll();
        } catch (err) {
            console.error('Failed to load relations', err);
        }
    };

    // Построение дерева контактов
    const buildTree = () => {
        const personMap = new Map();
        const childrenMap = new Map();
        
        persons.value.forEach(person => {
            personMap.set(person.id, {
                ...person,
                children: []
            });
        });
        
        relations.value.forEach(rel => {
            const parent = personMap.get(rel.parent_id);
            const child = personMap.get(rel.child_id);
            if (parent && child) {
                parent.children.push(child);
            }
        });
        
        const roots = [];
        const hasParent = new Set();
        
        relations.value.forEach(rel => {
            hasParent.add(rel.child_id);
        });
        
        personMap.forEach(person => {
            if (!hasParent.has(person.id)) {
                roots.push(person);
            }
        });
        
        const sortChildren = (node) => {
            if (sortMode.value === 'importance') {
                node.children.sort((a, b) => (b.importance || 0) - (a.importance || 0));
            } else if (sortMode.value === 'name') {
                node.children.sort((a, b) => a.full_name.localeCompare(b.full_name, 'ru'));
            }
            node.children.forEach(child => sortChildren(child));
        };
        
        roots.forEach(root => sortChildren(root));
        
        if (sortMode.value === 'importance') {
            roots.sort((a, b) => (b.importance || 0) - (a.importance || 0));
        } else if (sortMode.value === 'name') {
            roots.sort((a, b) => a.full_name.localeCompare(b.full_name, 'ru'));
        }
        
        return roots;
    };
    
    const flattenTree = (nodes, level = 0) => {
        let result = [];
        for (const node of nodes) {
            result.push({
                ...node,
                _level: level,
                _hasChildren: node.children && node.children.length > 0,
                _expanded: expandedNodes.value.has(node.id)
            });
            
            if (expandedNodes.value.has(node.id) && node.children && node.children.length > 0) {
                result = result.concat(flattenTree(node.children, level + 1));
            }
        }
        return result;
    };
    
    const hierarchicalPersons = computed(() => {
        if (sortMode.value !== 'hierarchy') {
            return [];
        }
        const tree = buildTree();
        return flattenTree(tree);
    });
    
    const filteredPersons = computed(() => {
        let filtered = [];
        
        if (sortMode.value === 'hierarchy') {
            filtered = hierarchicalPersons.value;
        } else {
            filtered = [...persons.value];
            
            if (searchQuery.value.length >= 2) {
                const query = searchQuery.value.toLowerCase();
                filtered = filtered.filter(p => 
                    p.full_name?.toLowerCase().includes(query) || 
                    p.short_name?.toLowerCase().includes(query)
                );
            }
            
            if (sortMode.value === 'importance') {
                filtered.sort((a, b) => (b.importance || 0) - (a.importance || 0));
            } else if (sortMode.value === 'name') {
                filtered.sort((a, b) => (a.full_name || '').localeCompare(b.full_name || '', 'ru'));
            }
        }
        
        return filtered;
    });
    
    const toggleNode = (nodeId) => {
        if (expandedNodes.value.has(nodeId)) {
            expandedNodes.value.delete(nodeId);
        } else {
            expandedNodes.value.add(nodeId);
        }
        expandedNodes.value = new Set(expandedNodes.value);
    };
    
    const expandAll = () => {
        const addAllChildren = (nodes) => {
            for (const node of nodes) {
                expandedNodes.value.add(node.id);
                if (node.children && node.children.length) {
                    addAllChildren(node.children);
                }
            }
        };
        const tree = buildTree();
        addAllChildren(tree);
        expandedNodes.value = new Set(expandedNodes.value);
    };
    
    const collapseAll = () => {
        expandedNodes.value.clear();
        expandedNodes.value = new Set();
    };
    
    const selectPerson = (id) => { selectedPersonId.value = id; };
    const setSearchQuery = (query) => { searchQuery.value = query; };
    const setSortMode = (mode) => { 
        sortMode.value = mode;
        if (mode !== 'hierarchy') {
            expandedNodes.value.clear();
        }
    };
    const refresh = async () => { 
        await Promise.all([loadPersons(), loadRelations()]);
        if (sortMode.value === 'hierarchy') {
            expandAll();
        }
    };

    return { 
        persons, 
        relations, 
        isLoading, 
        error, 
        selectedPersonId, 
        searchQuery, 
        sortMode,
        expandedNodes,
        filteredPersons,
        hierarchicalPersons,
        loadPersons, 
        loadRelations,
        selectPerson, 
        setSearchQuery, 
        setSortMode,
        toggleNode,
        expandAll,
        collapseAll,
        refresh 
    };
});