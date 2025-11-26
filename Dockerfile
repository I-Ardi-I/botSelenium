# Используем минимальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем файлы проекта
COPY . /app/

# Переменные окружения (Chromium уже в другом контейнере)
ENV SELENIUM_REMOTE_URL="http://selenium:4444/wd/hub"

# Запускаем Python-скрипт
CMD ["python", "main.py"]
