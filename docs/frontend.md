# Фронтенд

Vue 3 (`<script setup>`), Pinia, Axios, Vite 5. Тесты — Vitest (`frontend/tests/`).
Как всё связано — [architecture.md](architecture.md).

## Структура `frontend/src`

| Путь | Назначение |
|---|---|
| `api/client.ts` | Экземпляр Axios (`/api`), понятные ошибки `ApiError` (в т.ч. 422), повтор только GET после таймаута |
| `api/resource.ts` | Фабрика `personResource(name)`: `getForPerson`, `getById`, `create(personId, data)`, `update`, `delete` |
| `api/endpoints/*.ts` | По модулю на ресурс (`casesApi`, `vehiclesApi`, …); `persons`, `relations`, `categories` — свои |
| `stores/useTreeStore.ts` | Люди и связи для боковой панели: поиск, сортировка, дерево, `upsert*/remove*` |
| `stores/usePersonStore.ts` | Открытый профиль со всеми вкладками и все действия записи (см. ниже) |
| `composables/useToast.ts` | Очередь уведомлений; выводит `components/common/ToastHost.vue` |
| `utils/payload.ts` | `toPayload(form, isEdit)` и `fillForm(form, item)` для модалок |
| `components/modals/*` | Формы создания/изменения; сохраняют только через стор |
| `components/profile/*` | Вкладки профиля; читают коллекции из `person` |
| `views/ProfileView.vue` | Шапка профиля и переключение вкладок |
| `App.vue` | Раскладка, открытие модалок, удаление с подтверждением |

## `usePersonStore` — действия

| Действие | Что делает |
|---|---|
| `loadPerson(id)` | Человек + все коллекции параллельно; спиннер только при смене человека; устаревший ответ отбрасывается |
| `refreshCurrent()` | Тихая перезагрузка открытого профиля (кнопка «Обновить») |
| `createItem(key, data)` | Создаёт и добавляет ответ сервера в `currentPerson[key]` |
| `updateItem(key, id, data)` | Изменяет и заменяет запись ответом; `is_active === false` убирает её из списка |
| `deleteItem(key, id)` | Сразу убирает запись; если сервер отказал — возвращает и пробрасывает ошибку |
| `createRelation(data)` | Создаёт связь, обновляет дерево и список связей открытого человека |
| `createPerson / updatePerson / deletePerson` | Меняют человека и строку в боковой панели вместе |

Ключи коллекций: `relations`, `social_media`, `digital_accounts`, `real_estate`, `vehicles`, `cases`,
`medical_records`, `partners`, `devices`, `cross_records`.

## Как писать модалку

```js
const data = toPayload({ ...form }, isEdit.value)   // создание: без пустых полей; изменение: '' → null
if (isEdit.value) await personStore.updateItem('cases', currentId.value, data)
else await personStore.createItem('cases', data)
close()                                            // перезагружать ничего не нужно
```

При открытии на изменение: `fillForm(form, await casesApi.getById(id))` — копирует только поля формы,
поэтому `id`, `person_id` и даты не утекают в следующее создание. Кнопка «Сохранить» —
`:disabled="loading"` (защита от двойной записи).

## Добавить новый ресурс

1. `api/endpoints/x.ts`: `export const xApi = personResource('x')`.
2. `RESOURCES` в `usePersonStore.ts`: `x_items: xApi` (+ подпись в `LABELS`).
3. Вкладка в `components/profile/` читает `person.x_items`; модалка — как выше.
4. В `App.vue` — ключ вкладки в `TAB_COLLECTION` для удаления.
5. Тест в `tests/stores.test.ts`.

## Команды

```bash
npm run dev     # :3000, прокси /api → http://localhost:8000 (или VITE_API_TARGET)
npm test        # vitest, 19 тестов
npm run build   # dist/
```
