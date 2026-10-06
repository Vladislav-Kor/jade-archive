FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование всего приложения
COPY . .

# Проверка что файлы скопированы
RUN ls -la /app && ls -la /app/*.py


# Таблицы создаёт init_db() при импорте main.py (с повторами подключения к БД).
# alembic upgrade head здесь падал при каждом старте: схема 001_initial не совпадает с models.py.

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
