# Бэкенд

FastAPI 0.104, SQLAlchemy 2.0, Pydantic 2.5, PyMySQL, Python 3.11 (в Docker).
Список маршрутов — [api.md](api.md), таблицы — [data-model.md](data-model.md).

## Модули

| Файл | Назначение |
|---|---|
| `main.py` | Приложение FastAPI, CORS, все маршруты, кроме категорий; `init_db()` при импорте |
| `api_extension.py` | Маршруты категорий (`register_extension_routes`); `/categories/tree` объявлен до `/{id}` |
| `crud.py` | Операции с базой: `get_*`, `create_*`, `update_*` (частичное, `exclude_unset`), `delete_*` |
| `models.py` | SQLAlchemy-модели; используют общий `Base` из `database.py` |
| `schemas.py` | Pydantic-схемы: `*Create`, `*Update`, `*Response`, `PersonListItem` для списков |
| `database.py` | Движок, сессии, `get_db()`, `init_db()` (5 попыток подключения); `DATABASE_URL` обязателен |
| `bot.py`, `run_bot.py` | Telegram-бот; токен и прокси из `.env` (`BOT_TOKEN`, `PROXY_URL`) |
| `tests/` | Контракт API — 27 тестов на отдельном MySQL ([development.md](development.md)) |

Не используются: `models_extension.py`, `schemas_extension.py`, `crud_extension.py`, `alembic/`
(миграция `001_initial` не совпадает с `models.py`; таблицы создаёт `init_db()`).

> ⚠️ `create_tables.py` **удаляет все таблицы** перед созданием. Не запускайте его на рабочей базе.

## Соглашения

- **Маршрут ресурса человека:** список и создание — `/api/persons/{person_id}/<ресурс>`,
  чтение/изменение/удаление — `/api/<ресурс>/{id}`. Перед созданием проверяется, что человек есть (`404`).
- **Частичное изменение:** `crud.update_*` применяет `model_dump(exclude_unset=True)` — меняются только
  переданные поля; `null` очищает поле.
- **Мягкое удаление** (`is_active = False`): аккаунты, недвижимость, транспорт, устройства.
  Списки фильтруют `is_active == True`; чтение по id возвращает и удалённые записи.
- **Ошибки:** `HTTPException` с коротким `detail`; подробности исключений — только в журнал
  (`logger.error`), не в ответ.
- **Списки людей** отдают `PersonListItem` без вложенных коллекций: в них нет паролей аккаунтов,
  и нет запросов N+1.

## Добавить новый ресурс человека

1. Модель в `models.py` (`person_id` с `ForeignKey("persons.id", ondelete="CASCADE")`), связь в `Person`.
2. Схемы `XCreate`, `XUpdate` (все поля `Optional`), `XResponse` (`from_attributes=True`) в `schemas.py`.
3. `get_xs / get_x / create_x / update_x / delete_x` в `crud.py`.
4. Пять маршрутов в `main.py` по образцу дел (`/api/persons/{id}/cases`, `/api/cases/{id}`), создание — `201`.
5. Строка в `PERSON_RESOURCES` в `tests/test_api_contract.py` — контракт проверится автоматически.
6. Фронтенд: `personResource('x')` и ключ в `RESOURCES` стора — [frontend.md](frontend.md).
