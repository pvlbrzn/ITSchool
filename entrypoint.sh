#!/bin/bash

# Ждём Redis
echo "Waiting for Redis..."
while ! nc -z redis 6379; do
  sleep 0.5
done
echo "Redis is up"

# Применяем миграции
python manage.py migrate

# Собираем статику
python manage.py collectstatic --noinput

# Запуск команды из Dockerfile (например, gunicorn или django runserver)
exec "$@"
