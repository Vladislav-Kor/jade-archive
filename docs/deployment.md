# Запуск, CI/CD и резервные копии

## docker compose

`docker-compose.yml` поднимает три контейнера проекта `arc_agent`:

| Сервис | Контейнер | Порт | Данные |
|---|---|---|---|
| `db` | `jade_db` (MySQL 8) | 3306 | том `arc_agent_mysql_data` |
| `app` | `jade_app` (FastAPI) | 8000 | — |
| `phpmyadmin` | `jade_phpmyadmin` | 8081 | — |

Пароли берутся из `.env` (`MYSQL_ROOT_PASSWORD`, `MYSQL_PASSWORD`, …; шаблон — `.env.example`),
в репозитории их нет.

```bash
docker compose up -d --build --no-deps app   # обновить только API, база не трогается
docker compose logs -f app
```

Таблицы создаёт `init_db()` при старте API; существующие таблицы и данные не меняются.

## CI/CD (GitHub Actions)

Файл: [`.github/workflows/ci-cd.yml`](../.github/workflows/ci-cd.yml).

| Задача | Когда | Что делает |
|---|---|---|
| `backend` | PR и push в `master` | 27 тестов API на сервисном контейнере MySQL 8 |
| `frontend` | PR и push в `master` | `npm ci`, 19 тестов Vitest, `npm run build`, артефакт `frontend-dist` (14 дней) |
| `docker` | PR и push в `master` | Проверочная сборка образа бэкенда |
| `publish` (CD) | push в `master` и теги `v*`, только если всё выше зелёное | Образ `ghcr.io/vladislav-kor/jade-archive-backend` с тегами `latest`, `sha-…`, версией из тега |

Выпуск версии: `git tag v3.1.0 && git push origin v3.1.0` — образ получит тег `3.1.0`.

### Обновить рабочий сервер из GHCR

Пакет в GHCR приватный — один раз войдите токеном с правом `read:packages`:

```bash
echo <токен> | docker login ghcr.io -u Vladislav-Kor --password-stdin
docker pull ghcr.io/vladislav-kor/jade-archive-backend:latest
docker tag ghcr.io/vladislav-kor/jade-archive-backend:latest arc_agent-app:latest
docker compose up -d --no-deps --no-build app
```

Автоматического развёртывания на компьютер нет намеренно: для этого нужен self-hosted runner, а в
публичном репозитории он позволил бы чужим pull request выполнять код на вашей машине.

## Резервные копии

```bash
# база (копии держите вне репозитория; *.sql в .gitignore)
docker exec jade_db sh -c 'exec mysqldump -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" --single-transaction --no-tablespaces --routines --triggers --default-character-set=utf8mb4 "$MYSQL_DATABASE"' > jade_archive_$(date +%Y%m%d_%H%M%S).sql

# код с полной историей всех веток
git bundle create arc_agent_$(date +%Y%m%d_%H%M%S).bundle --all
```

Восстановление базы:

```bash
docker exec -i jade_db sh -c 'exec mysql -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" --default-character-set=utf8mb4 "$MYSQL_DATABASE"' < jade_archive_<дата>.sql
```

Проверяйте копию восстановлением в отдельный контейнер и сравнением числа строк — копия, которую ни разу
не восстанавливали, не считается копией.

## Откат API

```bash
docker images arc_agent-app                         # локальные образы, например before-fix-20261006
docker tag arc_agent-app:<тег> arc_agent-app:latest
docker compose up -d --no-deps --no-build app
```
