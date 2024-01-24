from urllib.parse import quote

import requests
from icecream import ic

text_to_encode = "Крутой бот будет если плохо ему не станет"
encoded_text = quote(text_to_encode, encoding='utf-8')
url = f"https://mymemory.translated.net/api/ajaxfetch?q={text_to_encode}&langpair=ru-RU|uz-UZ&mtonly=1"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()  # Парсим ответ в формате JSON
    ic(data)
    ic(data.keys()) #translatedText
    print(data['matches'][0]['translation'].replace("&#39;", "'"))
else:
    print(f"Ошибка при выполнении запроса. Код статуса: {response.status_code}")
