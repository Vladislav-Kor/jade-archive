const READ_ONLY = new Set(['id', 'created_at', 'updated_at'])

const isEmpty = (v: unknown) => v === '' || v === null || v === undefined

/**
 * Тело запроса из формы.
 * Создание: пустые поля не отправляем. Изменение: очищенное поле уходит как null —
 * сервер обновляет только переданные поля (exclude_unset), и иначе очистить поле нельзя.
 */
export function toPayload(form: Record<string, unknown>, isEdit: boolean): Record<string, unknown> {
    const out: Record<string, unknown> = {}
    for (const [key, value] of Object.entries(form)) {
        if (READ_ONLY.has(key)) continue
        if (isEmpty(value)) {
            if (isEdit) out[key] = null
            continue
        }
        out[key] = value
    }
    return out
}

/**
 * Заполняет форму записью с сервера: только поля, которые есть в форме
 * (id, person_id, даты не попадают в следующую отправку), null оставляет значение по умолчанию.
 */
export function fillForm(form: Record<string, unknown>, item: Record<string, unknown>): void {
    for (const key of Object.keys(form)) {
        if (key in item) form[key] = item[key] ?? form[key]
    }
}
