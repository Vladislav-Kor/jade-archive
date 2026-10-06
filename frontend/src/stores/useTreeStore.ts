import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { personsApi } from '@/api/endpoints/persons'
import { relationsApi } from '@/api/endpoints/relations'

type SortMode = 'importance' | 'name' | 'hierarchy'

/** Список людей и связей для боковой панели. После CRUD обновляется точечно (upsert/remove). */
export const useTreeStore = defineStore('tree', () => {
    const persons = ref<any[]>([])
    const relations = ref<any[]>([])
    const isLoading = ref(false)
    const error = ref<string | null>(null)
    const selectedPersonId = ref<number | null>(null)
    const searchQuery = ref('')
    const sortMode = ref<SortMode>('importance')
    const expandedNodes = ref(new Set<number>())

    const loadPersons = async () => {
        isLoading.value = true
        error.value = null
        try {
            persons.value = await personsApi.getAll()
        } catch (err: any) {
            error.value = err.message || 'Ошибка загрузки'
        } finally {
            isLoading.value = false
        }
    }

    const loadRelations = async () => {
        try {
            relations.value = await relationsApi.getAll()
        } catch (err) {
            console.error('Не удалось загрузить связи', err)
        }
    }

    // ---- точечные изменения после CRUD (без перезагрузки списков) ----
    const upsertPerson = (person: any) => {
        const i = persons.value.findIndex((p) => p.id === person.id)
        if (i === -1) persons.value.push(person)
        else persons.value[i] = { ...persons.value[i], ...person }
    }

    const removePerson = (id: number) => {
        persons.value = persons.value.filter((p) => p.id !== id)
        relations.value = relations.value.filter((r) => r.parent_id !== id && r.child_id !== id)
        if (selectedPersonId.value === id) selectedPersonId.value = null
    }

    const upsertRelation = (relation: any) => {
        const i = relations.value.findIndex((r) => r.id === relation.id)
        if (i === -1) relations.value.push(relation)
        else relations.value[i] = relation
    }

    const removeRelation = (id: number) => {
        relations.value = relations.value.filter((r) => r.id !== id)
    }

    // ---- дерево и фильтры ----
    const byImportance = (a: any, b: any) => (b.importance || 0) - (a.importance || 0)
    const byName = (a: any, b: any) => (a.full_name || '').localeCompare(b.full_name || '', 'ru')

    const buildTree = () => {
        const personMap = new Map<number, any>()
        persons.value.forEach((person) => personMap.set(person.id, { ...person, children: [] }))

        const hasParent = new Set<number>()
        relations.value.forEach((rel) => {
            const parent = personMap.get(rel.parent_id)
            const child = personMap.get(rel.child_id)
            if (parent && child) parent.children.push(child)
            hasParent.add(rel.child_id)
        })

        const roots = [...personMap.values()].filter((p) => !hasParent.has(p.id))
        const compare = sortMode.value === 'name' ? byName : byImportance
        const sortChildren = (node: any) => {
            node.children.sort(compare)
            node.children.forEach(sortChildren)
        }
        roots.forEach(sortChildren)
        roots.sort(compare)
        return roots
    }

    const flattenTree = (nodes: any[], level = 0): any[] => {
        const result: any[] = []
        for (const node of nodes) {
            const expanded = expandedNodes.value.has(node.id)
            result.push({ ...node, _level: level, _hasChildren: node.children?.length > 0, _expanded: expanded })
            if (expanded && node.children?.length) result.push(...flattenTree(node.children, level + 1))
        }
        return result
    }

    const hierarchicalPersons = computed(() => (sortMode.value === 'hierarchy' ? flattenTree(buildTree()) : []))

    const filteredPersons = computed(() => {
        if (sortMode.value === 'hierarchy') return hierarchicalPersons.value

        let filtered = [...persons.value]
        if (searchQuery.value.length >= 2) {
            const query = searchQuery.value.toLowerCase()
            filtered = filtered.filter((p) =>
                p.full_name?.toLowerCase().includes(query) || p.short_name?.toLowerCase().includes(query))
        }
        return filtered.sort(sortMode.value === 'name' ? byName : byImportance)
    })

    const toggleNode = (nodeId: number) => {
        const next = new Set(expandedNodes.value)
        if (next.has(nodeId)) next.delete(nodeId)
        else next.add(nodeId)
        expandedNodes.value = next
    }

    const expandAll = () => {
        const next = new Set<number>()
        const walk = (nodes: any[]) => nodes.forEach((n) => { next.add(n.id); walk(n.children || []) })
        walk(buildTree())
        expandedNodes.value = next
    }

    const collapseAll = () => { expandedNodes.value = new Set() }

    const selectPerson = (id: number | null) => { selectedPersonId.value = id }
    const setSearchQuery = (query: string) => { searchQuery.value = query }
    const setSortMode = (mode: SortMode) => {
        sortMode.value = mode
        if (mode !== 'hierarchy') expandedNodes.value = new Set()
    }

    /** Полная загрузка — при старте и по кнопке «Обновить». После CRUD не нужна. */
    const refresh = async () => {
        await Promise.all([loadPersons(), loadRelations()])
        if (sortMode.value === 'hierarchy') expandAll()
    }

    return {
        persons, relations, isLoading, error, selectedPersonId, searchQuery, sortMode, expandedNodes,
        filteredPersons, hierarchicalPersons,
        loadPersons, loadRelations, refresh,
        upsertPerson, removePerson, upsertRelation, removeRelation,
        selectPerson, setSearchQuery, setSortMode, toggleNode, expandAll, collapseAll,
    }
})
