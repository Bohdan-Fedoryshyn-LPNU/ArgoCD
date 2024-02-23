# Використання офіційного образу Python як базового
FROM python:3.8-slim

# Встановлення робочого каталогу у контейнері
WORKDIR /app

# Копіювання файлу залежностей у поточний каталог
COPY requirements.txt .

# Встановлення залежностей
RUN pip install --no-cache-dir -r requirements.txt

# Копіювання вмісту локального каталогу webserver у контейнер
COPY . .

# Встановлення команди, яка буде виконуватися при запуску контейнера
CMD ["python", "./web_server.py"]
