# сперва сборка зависимостей
FROM python:3.11-slim AS builder

WORKDIR /app

# сначала копируем только requirements.txt
COPY requirements.txt .

# ставим зависимости в отдельную папку, чтобы потом перенести
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# финальный образ
FROM python:3.11-slim

WORKDIR /app

# забираем установленные зависимости из стадии builder
COPY --from=builder /install /usr/local

# копируем код приложения
COPY app.py .

# переменные окружения (значения по умолчанию)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# документируем порт
EXPOSE 5000

# точка входа — gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]