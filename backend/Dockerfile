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


RUN echo '#!/bin/bash\n\
echo "⏳ Waiting for database..."\n\
sleep 10\n\
echo "🔄 Running migrations..."\n\
alembic upgrade head\n\
echo "🚀 Starting application..."\n\
uvicorn main:app --host 0.0.0.0 --port 8000\n\
' > /app/start.sh && chmod +x /app/start.sh

EXPOSE 8000

CMD ["/app/start.sh"]
