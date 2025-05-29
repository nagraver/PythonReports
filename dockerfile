FROM python:3.11-slim

# Установка зависимостей для pipx и uv
RUN apt-get update && apt-get install -y curl pipx && \
    pipx ensurepath && \
    pipx install uv

# Обновляем PATH (для pipx установленного софтлинка)
ENV PATH="/root/.local/bin:$PATH"

# Создание рабочей директории
WORKDIR /app

# Копирование файлов
COPY pyproject.toml ./
COPY src/ ./src
COPY data1.csv data2.csv data3.csv ./

# Установка зависимостей через uv
RUN uv sync

# Команда по умолчанию
CMD ["uv", "run", "./src/main.py", "data1.csv", "data2.csv", "data3.csv", "--report", "payout"]
