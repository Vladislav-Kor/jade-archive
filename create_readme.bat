# Создание файла create_readme.bat
@'
@echo off
chcp 65001 >nul
title Создание документации Jade Archive
echo ========================================
echo    Jade Archive - Генератор документации
echo ========================================
echo.

set "README_FILE=README.md"

echo Создание файла %README_FILE%...
echo.

(
echo # 📁 Jade Archive - Нефритовая CRM
echo.
echo ## Полная документация проекта
echo.
echo ---
echo.
echo ## 📋 Оглавление
echo.
echo 1. [Описание проекта](#описание-проекта)
echo 2. [Технологии](#технологии)
echo 3. [Функциональные возможности](#функциональные-возможности)
echo 4. [Структура проекта](#структура-проекта)
echo 5. [Установка и запуск](#установка-и-запуск)
echo 6. [Настройка под себя](#настройка-под-себя)
echo 7. [API Эндпоинты](#api-эндпоинты)
echo 8. [Telegram Бот](#telegram-бот)
echo 9. [База данных](#база-данных)
echo 10. [Устранение проблем](#устранение-проблем)
echo 11. [Дорожная карта](#дорожная-карта)
echo 12. [Лицензия](#лицензия)
echo.
echo ---
echo.
echo ## Описание проекта
echo.
echo **Jade Archive** — это локальная CRM-система для управления социальным графом и персональными досье. Приложение позволяет создавать иерархическую структуру контактов, отслеживать связи между людьми, хранить расширенную информацию о каждом человеке (медицинские данные, документы, предпочтения) и управлять делами/проектами.
echo.
echo ### Ключевые особенности
echo.
echo - 🌳 **Иерархическое дерево контактов** - один человек может находиться в нескольких папках
echo - 📋 **Расширенное досье** - медицинские данные, документы, параметры тела, предпочтения
echo - 🔗 **Гибкая система связей** - любые типы отношений между людьми
echo - 🎨 **Темный нефритовый дизайн** - стильный интерфейс с CSS-иконками папок
echo - 🤖 **Telegram бот** - управление контактами через мессенджер
echo - 🐳 **Docker контейнеризация** - легкий запуск в любом окружении
echo.
echo ---
echo.
echo ## Технологии
echo.
echo ### Backend
echo.
echo | Технология | Версия | Назначение |
echo |------------|--------|------------|
echo | Python | 3.11 | Язык программирования |
echo | FastAPI | 0.104.1 | Веб-фреймворк |
echo | SQLAlchemy | 2.0.23 | ORM для работы с БД |
echo | PostgreSQL | 15 | Основная база данных |
echo | Pydantic | 2.5.0 | Валидация данных |
echo | Uvicorn | 0.24.0 | ASGI сервер |
echo.
echo ### Frontend
echo.
echo | Технология | Назначение |
echo |------------|------------|
echo | HTML5 | Структура страниц |
echo | Tailwind CSS | Утилитарный CSS-фреймворк |
echo | JavaScript (ES6+) | Клиентская логика |
echo | Font Awesome 6 | Иконки |
echo | Google Fonts (Inter) | Шрифты |
echo.
echo ### Инфраструктура
echo.
echo | Технология | Назначение |
echo |------------|------------|
echo | Docker | Контейнеризация |
echo | Docker Compose | Оркестрация |
echo | Nginx | Веб-сервер для статики |
echo | Traefik | Reverse proxy (опционально) |
echo.
echo ---
echo.
echo ## Функциональные возможности
echo.
echo ### 👥 Управление контактами
echo.
echo | Функция | Описание |
echo |---------|----------|
echo | Создание | Добавление нового человека с полными данными |
echo | Редактирование | Изменение любой информации о контакте |
echo | Удаление | Полное удаление со всеми связями |
echo | Поиск | Быстрый поиск по имени или короткому имени |
echo | Сортировка | По важности, иерархии, дате, имени |
echo.
echo ### 📋 Досье контакта
echo.
echo **Основная информация:**
echo - Полное имя и короткое имя
echo - Дата рождения и возраст
echo - Пол
echo - Адрес
echo - Телефон и Email
echo.
echo **Параметры тела:**
echo - Рост и вес
echo - Размер одежды и обуви
echo - Объемы (грудь, талия, бедра)
echo.
echo **Медицинские данные:**
echo - Группа крови и резус-фактор
echo - Аллергии
echo - Хронические заболевания
echo - Принимаемые лекарства
echo - Давление и пульс
echo.
echo **Документы:**
echo - Паспортные данные
echo - ИНН, СНИЛС
echo - Водительские права (категория, номер)
echo.
echo **Социальные параметры:**
echo - Семейное положение
echo - Количество детей
echo - Образование
echo - Профессия
echo - Место работы
echo.
echo **Предпочтения:**
echo - Любимый цвет
echo - Любимые цветы
echo - Любимая еда
echo - Любимая музыка
echo - Любимые фильмы
echo - Хобби
echo.
echo ---
echo.
echo ## Структура проекта
echo.
echo ```text
echo jade-archive/
echo ├── docker-compose.yml          # Оркестрация контейнеров
echo ├── .env.example                 # Пример переменных окружения
echo ├── README.md                    # Документация
echo │
echo ├── backend/                     # Бэкенд на FastAPI
echo │   ├── Dockerfile               # Docker образ бэкенда
echo │   ├── requirements.txt         # Python зависимости
echo │   ├── main.py                  # Главный файл приложения
echo │   ├── database.py              # Подключение к БД
echo │   ├── models.py                # SQLAlchemy модели
echo │   ├── schemas.py               # Pydantic схемы + валидация
echo │   ├── crud.py                  # CRUD операции
echo │   ├── bot.py                   # Telegram бот
echo │   └── run_bot.py               # Запуск бота отдельно
echo │
echo ├── frontend/                    # Фронтенд
echo │   ├── Dockerfile               # Docker образ фронтенда
echo │   ├── nginx.conf               # Конфигурация Nginx
echo │   └── static/                  # Статические файлы
echo │       ├── index.html           # Главная страница
echo │       ├── css/
echo │       │   └── styles.css       # Стили
echo │       └── js/
echo │           └── app.js           # Клиентская логика
echo │
echo └── traefik/                     # Traefik конфигурация (опционально)
echo     └── traefik.yml
echo ```
echo.
echo ---
echo.
echo ## Установка и запуск
echo.
echo ### Системные требования
echo.
echo | Компонент | Минимальная версия |
echo |-----------|-------------------|
echo | Docker | 20.10+ |
echo | Docker Compose | 2.0+ |
echo | RAM | 2 GB |
echo | Дисковое пространство | 1 GB |
echo | ОС | Windows, Linux, macOS |
echo.
echo ### Быстрый старт
echo.
echo #### 1. Клонирование репозитория
echo.
echo ```bash
echo git clone https://github.com/your-repo/jade-archive.git
echo cd jade-archive
echo ```
echo.
echo #### 2. Запуск через Docker Compose
echo.
echo ```bash
echo docker-compose up -d
echo ```
echo.
echo #### 3. Доступ к приложению
echo.
echo | Сервис | URL |
echo |--------|-----|
echo | Веб-интерфейс | http://localhost:3000 |
echo | API | http://localhost:8000 |
echo | API Документация | http://localhost:8000/docs |
echo.
echo ---
echo.
echo ## Настройка под себя
echo.
echo ### Изменение портов
echo.
echo В `docker-compose.yml` измените порты:
echo.
echo ```yaml
echo services:
echo   frontend:
echo     ports:
echo       - "8080:80"  # вместо 3000:80
echo   app:
echo     ports:
echo       - "8001:8000"  # вместо 8000:8000
echo ```
echo.
echo ### Кастомизация цветовой схемы
echo.
echo В `frontend/static/css/styles.css` измените CSS переменные:
echo.
echo ```css
echo :root {
echo     --jade-primary: #00a884;
echo     --jade-primary-dark: #008b6e;
echo }
echo ```
echo.
echo ---
echo.
echo ## API Эндпоинты
echo.
echo Базовый URL: `http://localhost:8000/api`
echo.
echo | Метод | Эндпоинт | Описание |
echo |-------|----------|----------|
echo | GET | `/health` | Проверка здоровья |
echo | GET | `/persons` | Список контактов |
echo | GET | `/persons/{id}` | Контакт по ID |
echo | POST | `/persons` | Создать контакт |
echo | PUT | `/persons/{id}` | Обновить контакт |
echo | DELETE | `/persons/{id}` | Удалить контакт |
echo | GET | `/search?q={query}` | Поиск |
echo | GET | `/tree` | Дерево контактов |
echo | POST | `/relations` | Создать связь |
echo | POST | `/persons/{id}/social` | Добавить соцсеть |
echo.
echo ---
echo.
echo ## Telegram Бот
echo.
echo ### Команды бота
echo.
echo | Команда | Описание | Пример |
echo |---------|----------|--------|
echo | `/start` | Приветствие | `/start` |
echo | `/help` | Помощь | `/help` |
echo | `/contacts` | Список контактов | `/contacts` |
echo | `/search <имя>` | Поиск | `/search Иван` |
echo | `/view <id>` | Просмотр досье | `/view 1` |
echo.
echo ---
echo.
echo ## Устранение проблем
echo.
echo ### 502 Bad Gateway
echo.
echo ```bash
echo docker logs jade_app --tail 50
echo docker-compose restart app
echo ```
echo.
echo ### Порт уже занят
echo.
echo Измените порты в `docker-compose.yml`
echo.
echo ---
echo.
echo ## Дорожная карта
echo.
echo ### v1.0 (текущая)
echo - ✅ Базовое управление контактами
echo - ✅ Иерархическое дерево
echo - ✅ Расширенное досье
echo - ✅ Связи между контактами
echo - ✅ Telegram бот
echo - ✅ Docker контейнеризация
echo.
echo ### v1.1 (планируется)
echo - [ ] Экспорт в PDF/Excel
echo - [ ] Импорт из CSV
echo - [ ] Массовые операции
echo.
echo ---
echo.
echo ## Лицензия
echo.
echo **MIT License**
echo.
echo Copyright (c) 2024 Jade Archive
echo.
echo ---
echo.
echo **⭐ Если проект вам понравился, поставьте звезду на GitHub!**
echo.
echo ---
echo *Документация актуальна для версии 1.0.0*
) > "%README_FILE%"

echo.
echo ========================================
echo    ✅ Файл %README_FILE% успешно создан!
echo ========================================
echo.
echo Расположение: %CD%\%README_FILE%
echo.
pause
'@ | Out-File -FilePath create_readme.bat -Encoding Default

Write-Host "✅ Файл create_readme.bat создан!" -ForegroundColor Green
Write-Host "Запустите его командой: .\create_readme.bat" -ForegroundColor Yellow