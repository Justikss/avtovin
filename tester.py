# import asyncio
# from peewee import *
# from datetime import datetime, timedelta
#
# # Ваши классы моделей: Seller, Tariff, TariffsToSellers
# # Инициализация менеджера (предполагается, что у вас уже есть инициализированный объект database)
# manager = peewee_async.Manager(database)
#
#
# async def delete_expired_tariff(tariff_id, wait_seconds):
#     # Ждем до момента истечения срока действия тарифа
#     await asyncio.sleep(wait_seconds)
#
#     # Удаление тарифа
#     async with manager.atomic():
#         tariff = await manager.get(TariffsToSellers, TariffsToSellers.id == tariff_id)
#         if tariff:
#             await manager.delete(tariff)
#             print(f"Тариф {tariff.tariff.name} для продавца {tariff.seller.telegram_id} удален.")
#
#
# async def schedule_tariff_deletion():
#     now = datetime.now()
#
#     # Получение всех активных тарифов, которые еще не истекли
#     active_tariffs = await manager.execute(TariffsToSellers.select().where(
#         TariffsToSellers.end_date_time > now
#     ))
#
#     # Запланировать задачи для удаления тарифов
#     for tariff in active_tariffs:
#         wait_seconds = (tariff.end_date_time - now).total_seconds()
#         asyncio.create_task(delete_expired_tariff(tariff.id, wait_seconds))
#
#
# # Запуск планировщика удаления тарифов
# # asyncio.run(schedule_tariff_deletion())
#

#
# ##############################################
# import os
# import re
#
# from aiogram.types import InputFile, FSInputFile
#
# path = 'utils/carss\\9\\mers — копия (2).jpg'
#
# if os.path.exists(path):
#     print('true')
#
# with open(path, 'rb') as file:
#
#     if FSInputFile(path):
#         print('aasd')
#
#
# def format_and_validate_phone_number(phone_number):
#     # Регулярное выражение для проверки номера телефона
#     pattern = r'^(\+?7\d{10}|8\d{10}|\+?998\d{9}|998\d{9}|9\d{8})$'
#
#     if re.match(pattern, phone_number):
#         # Форматирование номера
#         if phone_number.startswith('8'):
#             formatted_number = '+7' + phone_number[1:]
#         elif phone_number.startswith('9') and len(phone_number) == 9:
#             # Форматирование локального узбекского номера
#             return re.sub(r"(9\d{1})(\d{3})(\d{2})(\d{2})", r"\1-\2-\3-\4", phone_number)
#         elif not phone_number.startswith('+'):
#             formatted_number = '+' + phone_number
#         else:
#             formatted_number = phone_number
#
#         # Добавление дефисов для разделения цифр
#         if formatted_number.startswith('+7'):
#             return re.sub(r"(\+7)(\d{3})(\d{3})(\d{2})(\d{2})", r"\1-\2-\3-\4-\5", formatted_number)
#         elif formatted_number.startswith('+998'):
#             return re.sub(r"(\+998)(\d{2})(\d{3})(\d{2})(\d{2})", r"\1-\2-\3-\4-\5", formatted_number)
#     else:
#         return False
#

# Примеры использования
# print(format_and_validate_phone_number("+79111234567"))  # Российский номер
# print(format_and_validate_phone_number("89111234567"))  # Российский номер без '+'
# print(format_and_validate_phone_number("+998911234567"))  # Узбекистанский номер
# print(format_and_validate_phone_number("998911234567"))  # Узбекистанский номер без '+'
# print(format_and_validate_phone_number("971234567"))  # Локальный Узбекистанский номер
# print(format_and_validate_phone_number("+1234567890"))  # Неверный номер

# import asyncio
# from time import time
# import aiohttp
# import requests
# from bs4 import BeautifulSoup
#
# async def currency_sum_to_usd():
#     url = 'https://onmap.uz/usd'
#
#     # start_time = time()
#
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             html_content = await response.text()
#
#             soup = BeautifulSoup(html_content, 'html.parser')
#             data = soup.find('div', class_='text-green-600 text-xl font-semibold')
#
#             if data:
#                 result = int(data.text.strip().replace('~', '').replace(' ', ''))
#             else:
#                 result = False
#
#     #total_time = time() - start_time
#     print(str(result))
# asyncio.run(currency_sum_to_usd())
##################################################################
# from time import time
# import requests
# from bs4 import BeautifulSoup, SoupStrainer
#
# all_times = []
#
# # Создание сессии requests
# session = requests.Session()
#
# # URL и SoupStrainer для оптимизации парсинга
# url = 'https://kursolog.com/usd/uzs'
#
# # Выполнение запросов
# for _ in range(5):
#     start_time = time()
#     only_text_green = SoupStrainer('input', class_='form-control js-converter-to-currency')
#
#     # Запрос с использованием сессии и таймаута
#     get_response_time = time()
#     response = session.get(url, timeout=5)
#     print('get response total = ', str(time() - get_response_time))
#     html_content = response.text
#
#     # Оптимизированный парсинг
#     parsing_time = time()
#     soup = BeautifulSoup(html_content, 'html.parser', parse_only=only_text_green)
#     print('get parsing total = ', str(time() - parsing_time))
#
#     # Поиск данных
#     find_data_time = time()
#     data = soup.find()
#     print('parsing process total = ', str(time() - find_data_time))
#     print()
#     if data:
#         print(data.text.strip(), end=':::')
#     else:
#         print("Данные не найдены")
#
#     total_time = time() - start_time
#     print(str(total_time))
#     all_times.append(total_time)
#
# # Вывод среднего времени
# print('middle cost: ', str(sum(all_times) / len(all_times)))
# print('all_time ', str(sum(all_times)))
# # Закрытие сессии
# session.close()
#



# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time
# from selenium.webdriver.common.by import By
#
# # Путь к ChromeDriver
#
# starter = time.time()
# # URL сайта
# url = 'https://kursolog.com/usd/uzs'
# options = webdriver.ChromeOptions()
# # Запуск драйвера и открытие страницы
# driver = webdriver.Chrome(options=options)
# driver.get(url)
#
# # Ожидание для полной загрузки страницы
# time.sleep(2)  # Можно настроить время ожидания
#
# # Нахождение поля для ввода и ввод данных
# input_field = driver.find_element(By.CLASS_NAME, 'js-converter-from-currency')
# input_field.clear()
# input_field.send_keys('512')
# input_field.send_keys(Keys.RETURN)
#
# # Даем странице время на обработку данных
# time.sleep(1)  # Можно настроить время ожидания
#
# # Нахождение поля с результатом и извлечение данных
# result_field = driver.find_element(By.CLASS_NAME, 'js-converter-to-currency')
# result = result_field.get_attribute('value')
#
# print("Результат:", result, ' ', str(time.time() - starter))
#
# # Закрытие браузера
# driver.quit()
#
