# Разработка

## Требования

Docker Desktop, Python 3.11+, Node.js 22, Git.

## Первый запуск

```bash
cp .env.example .env            # задайте пароли MySQL (и BOT_TOKEN, если нужен бот)
docker compose up -d --build    # MySQL, API на :8000, phpMyAdmin на :8081
cd frontend && npm ci && npm run dev   # интерфейс на http://localhost:3000
```

## Тесты бэкенда

Тесты **никогда не работают с рабочей базой**: `tests/conftest.py` отказывается запускаться, если в адресе
есть `jade_archive`. Нужна одноразовая база:

```bash
docker run -d --name arc_test_db -p 127.0.0.1:3307:3306 --tmpfs /var/lib/mysql:rw \
  -e MYSQL_ROOT_PASSWORD=test_root -e MYSQL_DATABASE=arc_test \
  -e MYSQL_USER=arc_test -e MYSQL_PASSWORD=arc_test mysql:8

cd backend
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt -r requirements-dev.txt   # Linux/macOS: .venv/bin/pip
.venv/Scripts/python -m pytest tests -q
```

Адрес тестовой базы можно переопределить переменной `TEST_DATABASE_URL`. Таблицы очищаются перед каждым
тестом. На Windows один `TestClient` живёт всю сессию — так тесты не тратят сокеты на каждый запрос.

## Тесты фронтенда

```bash
cd frontend
npm test          # Vitest: сторы (реактивный CRUD, откат удаления, гонки) и utils/payload
npm run build
```

API в тестах подменён (`vi.mock`), сторы — настоящие.

## Проверка интерфейса на тестовых данных

Чтобы кликать по интерфейсу, не трогая рабочую базу:

```bash
# бэкенд на тестовой базе
cd backend && DATABASE_URL="mysql+pymysql://arc_test:arc_test@127.0.0.1:3307/arc_test?charset=utf8mb4" \
  .venv/Scripts/python -m uvicorn main:app --port 8001
# интерфейс с прокси на него
cd frontend && VITE_API_TARGET=http://localhost:8001 npx vite --port 3001
```

## Ветки и коммиты

Основная ветка — `master`; изменения — через ветку и pull request, CI должен быть зелёным
([deployment.md](deployment.md)). Сообщения коммитов — `type: что сделано` (`feat`, `fix`, `docs`, `test`,
`build`, `chore`), в теле — зачем.

## Известное окружение

Если локально тесты или страница падают с `WinError 10055/10048` или `ERR_NO_BUFFER_SPACE` — исчерпаны сокеты
Windows (например, VPN-клиентом). Перезапуск VPN/компьютера освобождает их; код тут ни при чём.
