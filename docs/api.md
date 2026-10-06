# API

Справочник сгенерирован из декораторов маршрутов в `backend/main.py` и `backend/api_extension.py`.
Интерактивная документация FastAPI: http://localhost:8000/docs (Swagger) и /redoc.

## Общие правила

- База URL: `/api`. Тела запросов и ответов — JSON (UTF-8).
- Создание — `201`, удаление — `200` с `{"message": ...}` (категории — `204` без тела).
- Изменение (`PUT`) частичное: меняются только переданные поля; явный `null` очищает поле.
- Ошибки: `{"detail": "..."}`; `404` — нет записи или человека; `400` — неверные данные;
  `409` — дубликат slug категории; `422` — ошибка валидации (`detail` — список ошибок).
- Внутренние подробности ошибок в ответ не попадают — только в журнал сервера.
- **Мягкое удаление** у таблиц `devices`, `digital_accounts`, `real_estate`, `vehicles`: `DELETE` ставит `is_active = false`,
  запись пропадает из списков, но остаётся в базе и читается по id.
- `GET /api/persons` и `/api/search` отдают `PersonListItem` — без вложенных коллекций и секретов аккаунтов;
  полный профиль — `GET /api/persons/{id}`, коллекции — отдельными запросами `/api/persons/{id}/<ресурс>`.
- `GET /api/persons` поддерживает `skip` и `limit` (по умолчанию 1000, максимум 1000).

## Служебные

| Метод | Путь | Ответ | Код |
|---|---|---|---|
| `GET` | `/` | — | 200 |
| `GET` | `/api/health` | — | 200 |

## Люди

| Метод | Путь | Ответ | Код |
|---|---|---|---|
| `GET` | `/api/persons` | List[PersonListItem] | 200 |
| `POST` | `/api/persons` | PersonResponse | 201 |
| `GET` | `/api/persons/{person_id}` | PersonResponse | 200 |
| `PUT` | `/api/persons/{person_id}` | PersonResponse | 200 |
| `DELETE` | `/api/persons/{person_id}` | — | 200 |
| `GET` | `/api/search` | List[PersonListItem] | 200 |
| `GET` | `/api/tree` | TreeNode | 200 |

## Связи

| Метод | Путь | Ответ | Код |
|---|---|---|---|
| `GET` | `/api/persons/{person_id}/relations` | — | 200 |
| `GET` | `/api/relations` | List[RelationResponse] | 200 |
| `POST` | `/api/relations` | RelationResponse | 201 |
| `DELETE` | `/api/relations/{relation_id}` | — | 200 |

## Соцсети

| Метод | Путь | Ответ | Код |
|---|---|---|---|
| `GET` | `/api/persons/{person_id}/social` | List[SocialMediaResponse] | 200 |
| `POST` | `/api/persons/{person_id}/social` | SocialMediaResponse | 201 |
| `PUT` | `/api/social/{social_id}` | SocialMediaResponse | 200 |
| `DELETE` | `/api/social/{social_id}` | — | 200 |

## Теги

| Метод | Путь | Ответ | Код |
|---|---|---|---|
| `POST` | `/api/persons/{person_id}/tags` | — | 200 |
| `DELETE` | `/api/tags/{tag_id}` | — | 200 |

## Цифровые аккаунты

| Метод | Путь | Ответ | Код |
|---|---|---|---|
| `GET` | `/api/digital-accounts/{account_id}` | DigitalAccountResponse | 200 |
| `PUT` | `/api/digital-accounts/{account_id}` | DigitalAccountResponse | 200 |
| `DELETE` | `/api/digital-accounts/{account_id}` | — | 200 |
| `GET` | `/api/persons/{person_id}/digital-accounts` | List[DigitalAccountResponse] | 200 |
| `POST` | `/api/persons/{person_id}/digital-accounts` | DigitalAccountResponse | 201 |

## Недвижимость

| Метод | Путь | Ответ | Код |
|---|---|---|---|
| `GET` | `/api/persons/{person_id}/real-estate` | List[RealEstateResponse] | 200 |
| `POST` | `/api/persons/{person_id}/real-estate` | RealEstateResponse | 201 |
| `GET` | `/api/real-estate/{property_id}` | RealEstateResponse | 200 |
| `PUT` | `/api/real-estate/{property_id}` | RealEstateResponse | 200 |
| `DELETE` | `/api/real-estate/{property_id}` | — | 200 |

## Транспорт

| Метод | Путь | Ответ | Код |
|---|---|---|---|
| `GET` | `/api/persons/{person_id}/vehicles` | List[VehicleResponse] | 200 |
| `POST` | `/api/persons/{person_id}/vehicles` | VehicleResponse | 201 |
| `GET` | `/api/vehicles/{vehicle_id}` | VehicleResponse | 200 |
| `PUT` | `/api/vehicles/{vehicle_id}` | VehicleResponse | 200 |
| `DELETE` | `/api/vehicles/{vehicle_id}` | — | 200 |

## Дела

| Метод | Путь | Ответ | Код |
|---|---|---|---|
| `GET` | `/api/cases/{case_id}` | CaseResponse | 200 |
| `PUT` | `/api/cases/{case_id}` | CaseResponse | 200 |
| `DELETE` | `/api/cases/{case_id}` | — | 200 |
| `GET` | `/api/persons/{person_id}/cases` | List[CaseResponse] | 200 |
| `POST` | `/api/persons/{person_id}/cases` | CaseResponse | 201 |

## Медицинские записи

| Метод | Путь | Ответ | Код |
|---|---|---|---|
| `GET` | `/api/medical/{record_id}` | MedicalRecordResponse | 200 |
| `PUT` | `/api/medical/{record_id}` | MedicalRecordResponse | 200 |
| `DELETE` | `/api/medical/{record_id}` | — | 200 |
| `GET` | `/api/persons/{person_id}/medical` | List[MedicalRecordResponse] | 200 |
| `POST` | `/api/persons/{person_id}/medical` | MedicalRecordResponse | 201 |

## Партнёры

| Метод | Путь | Ответ | Код |
|---|---|---|---|
| `GET` | `/api/partners/{partner_id}` | PartnerResponse | 200 |
| `PUT` | `/api/partners/{partner_id}` | PartnerResponse | 200 |
| `DELETE` | `/api/partners/{partner_id}` | — | 200 |
| `GET` | `/api/persons/{person_id}/partners` | List[PartnerResponse] | 200 |
| `POST` | `/api/persons/{person_id}/partners` | PartnerResponse | 201 |

## Устройства

| Метод | Путь | Ответ | Код |
|---|---|---|---|
| `GET` | `/api/devices/{device_id}` | DeviceResponse | 200 |
| `PUT` | `/api/devices/{device_id}` | DeviceResponse | 200 |
| `DELETE` | `/api/devices/{device_id}` | — | 200 |
| `GET` | `/api/persons/{person_id}/devices` | List[DeviceResponse] | 200 |
| `POST` | `/api/persons/{person_id}/devices` | DeviceResponse | 201 |

## Перекрёстные записи

| Метод | Путь | Ответ | Код |
|---|---|---|---|
| `POST` | `/api/cross-records` | CrossRecordResponse | 201 |
| `GET` | `/api/cross-records/{record_id}` | CrossRecordResponse | 200 |
| `PUT` | `/api/cross-records/{record_id}` | CrossRecordResponse | 200 |
| `DELETE` | `/api/cross-records/{record_id}` | — | 200 |
| `GET` | `/api/persons/{person_id}/cross-records` | List[CrossRecordResponse] | 200 |

## Категории

| Метод | Путь | Ответ | Код |
|---|---|---|---|
| `GET` | `/api/categories` | List[CategoryResponse] | 200 |
| `POST` | `/api/categories` | CategoryResponse | 201 |
| `GET` | `/api/categories/tree` | List[dict] | 200 |
| `GET` | `/api/categories/{category_id}` | CategoryResponse | 200 |
| `PUT` | `/api/categories/{category_id}` | CategoryResponse | 200 |
| `DELETE` | `/api/categories/{category_id}` | — | 204 |

Всего маршрутов: 65.
