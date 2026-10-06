import { describe, it, expect } from 'vitest'
import { toPayload, fillForm } from '@/utils/payload'

describe('toPayload', () => {
    it('drops empty fields when creating', () => {
        expect(toPayload({ title: 'Дело', notes: '', price: null, date: undefined }, false))
            .toEqual({ title: 'Дело' })
    })

    it('sends cleared fields as null when editing so the server erases them', () => {
        expect(toPayload({ title: 'Дело', notes: '' }, true)).toEqual({ title: 'Дело', notes: null })
    })

    it('never sends read-only server fields', () => {
        expect(toPayload({ id: 1, created_at: 'x', updated_at: 'y', title: 'Дело' }, true))
            .toEqual({ title: 'Дело' })
    })

    it('keeps false and zero', () => {
        expect(toPayload({ is_active: false, floor: 0 }, false)).toEqual({ is_active: false, floor: 0 })
    })
})

describe('fillForm', () => {
    it('copies only the fields the form has, so server fields do not leak into the next create', () => {
        const form: Record<string, unknown> = { title: '', notes: '' }

        fillForm(form, { id: 5, person_id: 1, title: 'Дело', notes: 'n', created_at: 'x' })

        expect(form).toEqual({ title: 'Дело', notes: 'n' })
    })

    it('keeps the form default when the server value is null', () => {
        const form: Record<string, unknown> = { title: '', priority: 'medium' }

        fillForm(form, { title: 'Дело', priority: null })

        expect(form).toEqual({ title: 'Дело', priority: 'medium' })
    })
})
