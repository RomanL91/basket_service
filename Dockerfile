# Используем базовый образ с Python
FROM python:3.11.9-alpine

# Устанавливаем рабочий каталог
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN apk update && apk add --no-cache postgresql-dev gcc python3-dev musl-dev
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . .

# Открываем порт, на котором будет работать FastAPI
EXPOSE 8989

# Делаем скрипт исполняемым
RUN chmod +x /app/entrypoint.sh

# Устанавливаем скрипт как точку входа
# ENTRYPOINT ["/app/entrypoint.sh"]
