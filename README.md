# A.R.K. — Archive Registry by Korchagin

[![CI/CD](https://github.com/Vladislav-Kor/jade-archive/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Vladislav-Kor/jade-archive/actions/workflows/ci-cd.yml)

Локальная PRM-система (Personal Relationship Management): досье на контакты, связи между людьми и всё,
что к ним относится, — недвижимость, транспорт, цифровые аккаунты, соцсети, дела, медицинские записи,
партнёры, устройства и произвольные записи по категориям.

Интерфейс обновляется сразу после создания, изменения и удаления — без перезагрузки страницы.

## Возможности

- **Контакты** — карточка человека, важность, поиск и сортировка; дерево связей «родитель → потомок».
- **Профиль с вкладками** — информация, связи, недвижимость, транспорт, аккаунты, соцсети, дела, медицина,
  партнёры, устройства, записи; счётчики на вкладках.
- **Реактивный CRUD** — изменения видны мгновенно; удаление с откатом при ошибке сервера; уведомления.
- **Telegram-бот** для доступа к данным (`backend/bot.py`).

## Стек

| Часть | Технологии |
|---|---|
| Интерфейс | Vue 3, Pinia, Axios, Vite 5, Vitest |
| API | FastAPI, SQLAlchemy 2, Pydantic 2, PyMySQL, pytest |
| База | MySQL 8 (utf8mb4) |
| Инфраструктура | Docker Compose, GitHub Actions, GitHub Container Registry |

## Быстрый старт

```bash
git clone https://github.com/Vladislav-Kor/jade-archive.git && cd jade-archive
cp .env.example .env              # задайте пароли MySQL
docker compose up -d --build      # MySQL :3306, API :8000 (Swagger: /docs), phpMyAdmin :8081
cd frontend && npm ci && npm run dev   # интерфейс: http://localhost:3000
```

## Документация

| Документ | О чём |
|---|---|
| [docs/architecture.md](docs/architecture.md) | Компоненты, поток данных, реактивный CRUD, порты |
| [docs/api.md](docs/api.md) | Все 65 маршрутов API и общие правила (коды, ошибки, мягкое удаление) |
| [docs/data-model.md](docs/data-model.md) | 14 таблиц, связи (ER-диаграмма), особенности |
| [docs/backend.md](docs/backend.md) | Модули бэкенда, соглашения, как добавить ресурс |
| [docs/frontend.md](docs/frontend.md) | Структура, API-слой, сторы и их действия, как писать модалку |
| [docs/development.md](docs/development.md) | Окружение, тесты на отдельной базе, проверка на тестовых данных |
| [docs/deployment.md](docs/deployment.md) | docker compose, CI/CD, образы GHCR, резервные копии, откат |
| [docs/security.md](docs/security.md) | Известные риски и что с ними делать |
| [docs/decisions/](docs/decisions/) | Архитектурные решения (ADR) |
| [CHANGELOG.md](CHANGELOG.md) | История изменений |

## Структура

```
backend/             FastAPI: main.py, api_extension.py, crud.py, models.py, schemas.py, database.py, tests/
frontend/            Vue 3: src/api, src/stores, src/components, src/views; tests/
docs/                документация и ADR
.github/workflows/   CI/CD
docker-compose.yml   MySQL, API, phpMyAdmin
.env.example         шаблон настроек (сам .env в git не попадает)
```

## Тесты

```bash
cd backend && .venv/Scripts/python -m pytest tests -q   # 27 тестов, нужна тестовая MySQL — см. docs/development.md
cd frontend && npm test                                 # 19 тестов
```

В GitHub Actions всё это запускается на каждый pull request и push в `master`.

## Безопасность

Данные чувствительные. Перед использованием прочитайте [docs/security.md](docs/security.md): там список
открытых рисков (в том числе пароли аккаунтов открытым текстом и порты, открытые в локальную сеть).
