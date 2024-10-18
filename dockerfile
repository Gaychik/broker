# Используем базовый образ Python
FROM python:3.11.3

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы сервисов
COPY service_a/ /app/service_a/
COPY service_b/ /app/service_b/
COPY broker/ /app/broker/

# Устанавливаем зависимости для каждого сервиса
RUN pip install -r service_a/requirements.txt
RUN pip install -r service_b/requirements.txt
RUN pip install -r broker/requirements.txt

# Открываем порты для каждого сервиса
EXPOSE 5001 5002 8000

# Запускаем все три сервиса
CMD ["sh", "-c", "python service_a/app.py & python service_b/app.py & uvicorn broker.app:app --host 0.0.0.0 --port 8000"]
