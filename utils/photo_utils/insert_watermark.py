import importlib
import os
import time
from uuid import uuid4

import aiofiles
import aiohttp
import asyncio
from aiogram import Bot, types

from aiogram.types import FSInputFile


import cv2
import numpy as np

# watermark_cache = {}
# redis_data_module = importlib.import_module('utils.redis_for_language')



# def resize_watermark(image_width, image_height, watermark, scale=0.1):
#     # global watermark_cache
#     # # Поскольку теперь мы работаем с объектом, ключ кеша не должен включать нехешируемые типы
#     # cache_key = (scale, image_width, image_height)
#     #
#     # if cache_key in watermark_cache:
#     #     print('from cache')
#     #     return watermark_cache[cache_key]
#     # else:
#     #     print('not from cache')
#
#     if all(side < 300 for side in (image_height, image_width)):
#         scale = 0.3
#         image_width, image_height = image_width * 0.9, image_height * 0.9
#     watermark_width = int(image_width * scale)
#     aspect_ratio = watermark.shape[1] / watermark.shape[0]
#     watermark_height = int(watermark_width / aspect_ratio)
#     resized_watermark = cv2.resize(watermark, (watermark_width, watermark_height), interpolation=cv2.INTER_AREA)
#
#     # Сохраняем обработанный водяной знак в кеш
#     # watermark_cache[cache_key] = resized_watermark
#     return resized_watermark
##################################
def resize_watermark(image_width, image_height, watermark, scale=0.1):
    # Определите минимальные ширину и высоту водяного знака
    min_watermark_width = 80  # Минимальная ширина водяного знака, например 100 пикселей
    min_watermark_height = 40  # Минимальная высота водяного знака, например 50 пикселей

    # Рассчитайте предполагаемый размер водяного знака с учетом масштаба
    watermark_width = int(image_width * scale)
    watermark_height = int(watermark.shape[0] * (watermark_width / watermark.shape[1]))

    # Если рассчитанные ширина или высота меньше минимальных, используйте минимальные размеры
    if watermark_width < min_watermark_width:
        watermark_width = min_watermark_width
        watermark_height = int(watermark.shape[0] * (min_watermark_width / watermark.shape[1]))

    if watermark_height < min_watermark_height:
        watermark_height = min_watermark_height
        watermark_width = int(watermark.shape[1] * (min_watermark_height / watermark.shape[0]))

    # Используйте интерполяцию INTER_AREA для уменьшения размера, INTER_LINEAR или INTER_CUBIC для увеличения
    if watermark.shape[1] > watermark_width or watermark.shape[0] > watermark_height:
        interpolation = cv2.INTER_AREA
    else:
        interpolation = cv2.INTER_LINEAR

    # Измените размер водяного знака
    resized_watermark = cv2.resize(watermark, (watermark_width, watermark_height), interpolation=interpolation)

    return resized_watermark
def add_watermark(image_data, watermark, position="bottom-right", scale=0.06):
    image = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_UNCHANGED)

    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

    # Установка логотипа для маленьких изображений в угол с уменьшенным отступом снизу
    if min(image.shape[0], image.shape[1]) <= 150:
        # Уменьшение водяного знака до размера, который точно поместится в угол
        scale = 0.25  # или другой масштаб, подходящий для маленьких изображений
        resized_watermark = resize_watermark(image.shape[1], image.shape[0], watermark, scale)

        # Позиционирование в нижнем правом углу с половинным отступом снизу
        x_offset = image.shape[1] - resized_watermark.shape[1]
        y_offset = image.shape[0] - resized_watermark.shape[0] - int(resized_watermark.shape[0] / 1500)
    else:
        resized_watermark = resize_watermark(image.shape[1], image.shape[0], watermark, scale)

        # Динамически определяем отступы на основе размера изображения
        offset_x = max(20, int(image.shape[1] * 0.02))  # минимум 20 пикселей или 2% от ширины изображения
        offset_y = max(5, int(image.shape[0] * 0.01))  # минимум 5 пикселей или 1% от высоты изображения

        # Проверяем, не выходит ли водяной знак за пределы изображения после применения отступов
        x_offset = image.shape[1] - resized_watermark.shape[1] - offset_x
        y_offset = image.shape[0] - resized_watermark.shape[0] - offset_y

    if y_offset < 0:
        y_offset = 0

    # Наложение водяного знака с учетом альфа-канала
    alpha_s = resized_watermark[:, :, 3] / 255.0 if resized_watermark.shape[2] == 4 else 1
    alpha_l = 1.0 - alpha_s
    for c in range(0, 3):
        image[y_offset:y_offset + resized_watermark.shape[0], x_offset:x_offset + resized_watermark.shape[1], c] = \
            (alpha_s * resized_watermark[:, :, c] + alpha_l * image[y_offset:y_offset + resized_watermark.shape[0],
                                                              x_offset:x_offset + resized_watermark.shape[1], c])

    return cv2.imencode('.png', image)[1].tobytes()


# def add_watermark(image_data, watermark, position="bottom-right", scale=0.1):
#     image = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_UNCHANGED)
#
#     if len(image.shape) == 3:
#         image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
#
#     # Установка логотипа для маленьких изображений в угол без отступов
#     if min(image.shape[0], image.shape[1]) <= 150:
#         # Уменьшение водяного знака до размера, который точно поместится в угол
#         # Например, устанавливаем ширину водяного знака в 1/4 от ширины изображения
#         scale = 0.25
#         resized_watermark = resize_watermark(image.shape[1], image.shape[0], watermark, scale)
#
#         # Позиционирование в нижнем правом углу без отступов
#         x_offset = image.shape[1] - resized_watermark.shape[1]
#         y_offset = image.shape[0] - resized_watermark.shape[0]
#     else:
#         resized_watermark = resize_watermark(image.shape[1], image.shape[0], watermark, scale)
#
#         # Динамически определяем отступы на основе размера изображения
#         offset_x = max(20, int(image.shape[1] * 0.02))  # минимум 20 пикселей или 2% от ширины изображения
#         offset_y = max(5, int(image.shape[0] * 0.01))  # минимум 5 пикселей или 1% от высоты изображения
#
#         # Проверяем, не выходит ли водяной знак за пределы изображения после применения отступов
#         x_offset = image.shape[1] - resized_watermark.shape[1] - offset_x
#         y_offset = image.shape[0] - resized_watermark.shape[0] - offset_y
#         if y_offset < 0:
#             y_offset = 0
#
#     # Наложение водяного знака с учетом альфа-канала
#     alpha_s = resized_watermark[:, :, 3] / 255.0 if resized_watermark.shape[2] == 4 else 1
#     alpha_l = 1.0 - alpha_s
#     for c in range(0, 3):
#         image[y_offset:y_offset + resized_watermark.shape[0], x_offset:x_offset + resized_watermark.shape[1], c] = \
#             (alpha_s * resized_watermark[:, :, c] + alpha_l * image[y_offset:y_offset + resized_watermark.shape[0],
#                                                               x_offset:x_offset + resized_watermark.shape[1], c])
#
#     return cv2.imencode('.png', image)[1].tobytes()

async def add_watermark_async(image_data, watermark_path, position="bottom-right", scale=0.1):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        None,
        add_watermark,
        image_data,
        watermark_path,
        position,
        scale
    )



async def process_photo(file_url, watermark):#watermark_path="utils/photo_utils/Avtovin-Design_System-Logo_v1-1.png"):


    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as resp:
            image_data = await resp.read()

    # Используйте уже загруженный водяной знак
    watermarked_image = await add_watermark_async(image_data, watermark)

    unique_filename = f"{uuid4()}.png"
    file_path = f"temp_photos/{unique_filename}"
    await save_image_async(watermarked_image, file_path)
    file_path = 'utils/photo_utils/' + file_path
    return file_path

async def save_image_async(image, file_path):
    async with aiofiles.open(file_path, 'wb') as out_file:
        await out_file.write(image)

async def insert_watermark(photo_list):

    watermark_path = "Avtovin-Design_System-Logo_v1-1.png"

    watermark = cv2.imread(watermark_path, cv2.IMREAD_UNCHANGED)
    if watermark.shape[2] < 4:
        watermark = cv2.cvtColor(watermark, cv2.COLOR_BGR2BGRA)

    tasks = [process_photo(photo_url, watermark) for photo_url in photo_list]
    file_paths = await asyncio.gather(*tasks)
    return file_paths
