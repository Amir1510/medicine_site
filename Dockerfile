FROM python:3

ENV PYTHONUNBUFFERED=1

WORKDIR /django-site

# Копируем только файл requirements.txt
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем остальные файлы проекта
COPY . .
