# Используйте официальный образ Python как базовый
FROM python:3.9-slim

# Установите рабочую директорию внутри контейнера
WORKDIR /app

# Копируйте файлы скрипта, зависимостей и логотипа в контейнер
COPY insert_wtmark_requirements.txt .


# Установите зависимости
RUN pip install --no-cache-dir -r insert_wtmark_requirements.txt

COPY insert_watermark.py .
COPY Avtovin-Design_System-Logo_v1-1.png .
COPY web_server.py .
# Установите любые дополнительные пакеты, если это необходимо
# Например, для OpenCV:
# RUN apt-get update && apt-get install -y libopencv-dev

# Запуск скрипта при старте контейнера
CMD ["uvicorn", "web_server:app", "--host", "0.0.0.0", "--port", "8000"]

#docker build -t watermark_inserter .
#
#docker run -p 8000:8000 \
#  -v "/mnt/d/PythCode/avtovin-main/utils/photo_utils/temp_photos:/app/photo_utils/temp_photos" \
#  -v "/mnt/d/PythCode/avtovin-main/utils/photo_utils/Avtovin-Design_System-Logo_v1-1.png:/app/photo_utils/Avtovin-Design_System-Logo_v1-1.png:ro" \
#  watermark_inserter

