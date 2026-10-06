
# 🗄️ A.R.K. - Archive Registry by Korchagin

## 📋 О проекте
**A.R.K. (Archive Registry by Korchagin)** - это современное веб-приложение для управления личными контактами и связями между ними. Система позволяет вести подробное досье на каждого человека, отслеживать связи, управлять недвижимостью, транспортом, цифровыми аккаунтами и многое другое. Фвктичски проект можно развить в PRM — Personal Relationship Management
### 🎯 Основные возможности
- **Управление контактами** - полный CRUD для всех контактов
- **Иерархия связей** - отслеживание отношений между людьми
- **Детальное досье** - медицинская информация, физические параметры, документы
- **Недвижимость** - управление объектами недвижимости (квартиры, дома, участки)
- **Транспорт** - учет автомобилей, мотоциклов и другого транспорта
- **Цифровые аккаунты** - хранение данных об аккаунтах в соцсетях и играх
- **Дела и задачи** - планирование и отслеживание дел
- **Медицинские записи** - хранение информации о здоровье
- **Поиск и фильтрация** - быстрый поиск по контактам
- **Адаптивный дизайн** - удобная работа на любых устройствах
## 🚀 Технологии
### Frontend
- **Vue 3** - прогрессивный JavaScript фреймворк
- **Pinia** - управление состоянием
- **Vite** - быстрая сборка и разработка
- **Axios** - HTTP клиент
- **SCSS** - препроцессор CSS
### Backend
- **FastAPI** - современный веб-фреймворк для Python
- **SQLAlchemy** - ORM для работы с базой данных
- **Pydantic** - валидация данных
- **Uvicorn** - ASGI сервер
- **PostgreSQL** - реляционная база данных
### DevOps
- **Docker** - контейнеризация
- **Docker Compose** - оркестрация сервисов
- **Nginx** - веб-сервер для статики
## 📁 Структура проекта

arc_agent/  
├── backend/ # FastAPI бекенд  
│ ├── main.py # Точка входа API  
│ ├── models.py # SQLAlchemy модели  
│ ├── schemas.py # Pydantic схемы  
│ ├── crud.py # CRUD операции  
│ ├── database.py # Настройка БД  
│ ├── Dockerfile # Dockerfile для бекенда  
│ └── requirements.txt # Python зависимости  
├── frontend/ # Vue 3 фронтенд  
│ ├── src/  
│ │ ├── api/ # API клиенты  
│ │ ├── components/ # Vue компоненты  
│ │ │ ├── common/ # Общие компоненты  
│ │ │ ├── modals/ # Модальные окна  
│ │ │ └── tree/ # Компонент дерева  
│ │ ├── composables/ # Хуки и логика  
│ │ ├── stores/ # Pinia store  
│ │ ├── types/ # TypeScript типы  
│ │ ├── App.vue # Корневой компонент  
│ │ └── main.ts # Точка входа  
│ ├── index.html  
│ ├── package.json  
│ ├── Dockerfile  
│ └── nginx.conf  
├── docker-compose.yml # Docker Compose конфиг  
└── README.md # Документация

text

## 🛠️ Установка и запуск
### Предварительные требования
- **Node.js** 18+ и **npm** 9+
- **Python** 3.11+
- **Docker** и **Docker Compose** (опционально)
- **PostgreSQL** 15+ (или использовать Docker)
### 🐳 Запуск через Docker (рекомендуется)
```bash
# Клонируем репозиторий
git clone <repository-url>
cd arc_agent
# Запускаем все сервисы
docker-compose up -d --build
# Импортируем тестовые данные
docker exec -it jade_app python import_data.py

Приложение будет доступно:

-   **Фронтенд**: [http://localhost:3000](http://localhost:3000/)
    
-   **API**: [http://localhost:8000](http://localhost:8000/)
    
-   **Документация API**: [http://localhost:8000/docs](http://localhost:8000/docs)
    

### 🖥️ Локальный запуск для разработки

#### 1. Запуск бекенда

bash

cd backend
# Создаем виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
# Устанавливаем зависимости
pip install -r requirements.txt
# Запускаем сервер
uvicorn main:app --reload --port 8000

#### 2. Запуск фронтенда

bash

cd frontend
# Устанавливаем зависимости
npm install
# Запускаем в режиме разработки
npm run dev

#### 3. Настройка базы данных

bash

# Запускаем PostgreSQL в Docker
docker run -d --name postgres \
 -e POSTGRES_USER=jade_user \
 -e POSTGRES_PASSWORD=jade_password \
 -e POSTGRES_DB=jade_archive \
 -p 5432:5432 \
 postgres:15
# Импортируем тестовые данные
python import_data.py

## 📊 API Эндпоинты

Метод

Эндпоинт

Описание

GET

`/api/health`

Проверка здоровья API

GET

`/api/persons`

Список всех контактов

GET

`/api/persons/{id}`

Получить контакт по ID

POST

`/api/persons`

Создать новый контакт

PUT

`/api/persons/{id}`

Обновить контакт

DELETE

`/api/persons/{id}`

Удалить контакт

GET

`/api/search?q={query}`

Поиск контактов

GET

`/api/relations`

Список всех связей

POST

`/api/relations`

Создать связь

DELETE

`/api/relations/{id}`

Удалить связь

GET

`/api/persons/{id}/relations`

Связи контакта

POST

`/api/persons/{id}/social`

Добавить соцсеть

GET

`/api/persons/{id}/digital-accounts`

Цифровые аккаунты

POST

`/api/persons/{id}/digital-accounts`

Добавить аккаунт

GET

`/api/persons/{id}/real-estate`

Недвижимость

POST

`/api/persons/{id}/real-estate`

Добавить недвижимость

GET

`/api/persons/{id}/vehicles`

Транспорт

POST

`/api/persons/{id}/vehicles`

Добавить транспорт

GET

`/api/persons/{id}/cases`

Дела

POST

`/api/persons/{id}/cases`

Добавить дело

GET

`/api/persons/{id}/medical`

Медицинские записи

POST

`/api/persons/{id}/medical`


## 🤝 Вклад в проект

1.  Форкните репозиторий
    
2.  Создайте ветку для фичи (`git checkout -b feature/amazing-feature`)
    
3.  Зафиксируйте изменения (`git commit -m 'Add some amazing feature'`)
    
4.  Запушьте ветку (`git push origin feature/amazing-feature`)
    
5.  Откройте Pull Request
    
## 📧 Контакты

**Автор**: Korchagin Vladislav

-   **Email**: corchagin.vlad2005@yandex.ru
    
-   **Telegram**: [@VLAD_K0R](https://t.me/VLAD_K0R)
    
-   **GitHub**: [Vladislav-Kor](https://github.com/Vladislav-Kor)
    
----------

⭐ Поставьте звезду на GitHub, если проект вам полезен!

text

Также создадим файл `.env.example` для переменных окружения:
```powershell
notepad ...\.env.example

env

# Database
DATABASE_URL=postgresql://jade_user:jade_password@db:5432/jade_archive
POSTGRES_USER=jade_user
POSTGRES_PASSWORD=jade_password
POSTGRES_DB=jade_archive
# Backend
BACKEND_PORT=8000
BACKEND_HOST=0.0.0.0
# Frontend
FRONTEND_PORT=3000
VITE_API_URL=http://localhost:8000
# Telegram Bot (опционально)
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_PROXY_URL=socks5://localhost:1080

И файл `.gitignore`:

powershell

notepad ...\.gitignore

gitignore

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/
*.log
*.sqlite3
# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnpm-debug.log*
dist/
dist-ssr/
*.local
# Environment
.env
.env.local
.env.*.local
# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store
# Docker
*.pid
*.seed
# Backups
*.backup
*.bak
backups/
# Misc
*.tmp
.cache/
coverage/
.nyc_output/
