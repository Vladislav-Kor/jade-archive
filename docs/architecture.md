# Архитектура

## Компоненты

```mermaid
flowchart LR
    subgraph Браузер
        UI[Vue 3 компоненты<br/>Sidebar, ProfileView, вкладки, модалки]
        Stores[Pinia сторы<br/>useTreeStore, usePersonStore]
        API[API-слой<br/>client.ts, resource.ts, endpoints/*]
        UI <--> Stores --> API
    end
    Vite[Vite dev server :3000<br/>прокси /api] 
    subgraph Docker["docker compose (проект arc_agent)"]
        App[jade_app — FastAPI :8000<br/>main.py, api_extension.py, crud.py]
        DB[(jade_db — MySQL 8 :3306<br/>том arc_agent_mysql_data)]
        PMA[jade_phpmyadmin :8081]
        App --> DB
        PMA --> DB
    end
    API --> Vite --> App
    Bot[Telegram-бот<br/>bot.py / run_bot.py] --> DB
```

| Компонент | Где | Подробнее |
|---|---|---|
| Интерфейс | `frontend/` — Vue 3, Pinia, Vite, Axios | [frontend.md](frontend.md) |
| API | `backend/` — FastAPI, SQLAlchemy 2, Pydantic 2 | [backend.md](backend.md), [api.md](api.md) |
| База | MySQL 8, utf8mb4 | [data-model.md](data-model.md) |
| Запуск и выпуск | docker compose, GitHub Actions, GHCR | [deployment.md](deployment.md) |

## Поток данных при изменении (реактивный CRUD)

```mermaid
sequenceDiagram
    participant M as Модалка (например, CaseModal)
    participant S as usePersonStore
    participant A as casesApi (resource.ts)
    participant B as FastAPI
    M->>S: createItem('cases', toPayload(form))
    S->>A: create(personId, data)
    A->>B: POST /api/persons/{id}/cases
    B-->>A: 201 + созданное дело
    A-->>S: дело
    S->>S: currentPerson.cases.push(дело)
    Note over M,S: вкладка обновилась сразу, без перезагрузки
```

Правила (решение — [ADR-001](decisions/ADR-001-reactive-stores.md)):

- Сервер — источник правды; стор меняется **ответом** сервера, а не повторной загрузкой.
- Удаление оптимистичное: запись исчезает сразу, при ошибке возвращается на место.
- Связи в профиле — производный вид, поэтому после изменения перечитывается только их список.
- Ответ на устаревший запрос профиля отбрасывается; спиннер — только при смене человека.
- Список людей в боковой панели (`useTreeStore`) обновляется точечно: `upsertPerson`,
  `removePerson`, `upsertRelation`, `removeRelation`.

## Порты

| Порт | Что |
|---|---|
| 3000 | Vite dev server (интерфейс), проксирует `/api` → 8000 |
| 8000 | API (`jade_app`), Swagger: `/docs` |
| 3306 | MySQL (`jade_db`) |
| 8081 | phpMyAdmin |

Все порты Docker сейчас открыты на `0.0.0.0` — см. [security.md](security.md).
