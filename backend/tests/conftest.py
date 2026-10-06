"""Тесты API идут на отдельном MySQL (docker-контейнер arc_test_db), боевая база не трогается.

Запуск базы:
  docker run -d --name arc_test_db -p 127.0.0.1:3307:3306 --tmpfs /var/lib/mysql:rw \
    -e MYSQL_ROOT_PASSWORD=test_root -e MYSQL_DATABASE=arc_test \
    -e MYSQL_USER=arc_test -e MYSQL_PASSWORD=arc_test mysql:8
"""
import os
import sys
from pathlib import Path

import pytest

TEST_DB = os.environ.setdefault(
    "TEST_DATABASE_URL", "mysql+pymysql://arc_test:arc_test@127.0.0.1:3307/arc_test?charset=utf8mb4")
if "@db:" in TEST_DB or "jade_archive" in TEST_DB:
    raise RuntimeError("Тесты не должны работать с боевой базой jade_archive")
os.environ["DATABASE_URL"] = TEST_DB  # database.py читает его при импорте

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import text  # noqa: E402

import main  # noqa: E402
from database import Base, engine  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def schema():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture(scope="session")
def _client(schema):
    # Один клиент и один event loop на всю сессию: без `with` TestClient создаёт новый loop
    # (и пару сокетов) на каждый запрос — на Windows с занятыми портами это зависает.
    with TestClient(main.app) as c:
        yield c


@pytest.fixture(autouse=True)
def clean_tables(_client):
    # Перед тестом: так в данных нет и записи «me», которую создаёт startup приложения.
    with engine.begin() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        for table in Base.metadata.sorted_tables:
            conn.execute(text(f"DELETE FROM `{table.name}`"))
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
    yield


@pytest.fixture
def client(_client):
    return _client


@pytest.fixture
def person(client):
    r = client.post("/api/persons", json={"full_name": "Иван Тестов", "short_name": "ivan"})
    assert r.status_code == 201, r.text
    return r.json()


@pytest.fixture
def other_person(client):
    r = client.post("/api/persons", json={"full_name": "Пётр Второй", "short_name": "petr"})
    assert r.status_code == 201, r.text
    return r.json()
