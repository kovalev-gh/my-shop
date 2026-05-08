FROM python:3.13-slim

# Рабочая директория
WORKDIR /app

# Устанавливаем uv
RUN pip install --no-cache-dir uv

# Копируем только lock-файл и pyproject.toml для кэширования зависимостей
COPY pyproject.toml uv.lock ./

# Устанавливаем зависимости строго по lock-файлу
RUN uv sync --frozen

# Копируем весь проект
COPY . .

# Устанавливаем PYTHONPATH, чтобы app/ был корнем исходников
ENV PYTHONPATH=/app/app

# Экспонируем порт
EXPOSE 8000

# Запуск FastAPI через uv
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]