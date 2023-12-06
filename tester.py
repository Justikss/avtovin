import asyncio
from time import time
import aiohttp
import requests
from bs4 import BeautifulSoup

async def currency_sum_to_usd():
    url = 'https://onmap.uz/usd'

    # start_time = time()

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html_content = await response.text()

            soup = BeautifulSoup(html_content, 'html.parser')
            data = soup.find('div', class_='text-green-600 text-xl font-semibold')

            if data:
                result = int(data.text.strip().replace('~', '').replace(' ', ''))
            else:
                result = False

    #total_time = time() - start_time
    print(str(result))
asyncio.run(currency_sum_to_usd())
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
