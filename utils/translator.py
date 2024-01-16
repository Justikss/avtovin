
import requests

from config_data.config import YANDEX_IAM_TOKEN, YANDEX_folder_id

from langdetect import detect

async def detect_language(text):
    if isinstance(text, list):
        text = text[0]
    language = detect(text)
    return language


async def translate(texts, subkey=''):
    if subkey:
        subkey += '_'
    inputted_language = await detect_language(texts[0])
    if inputted_language == 'ru':
        target_language = 'uz'

        start_language = 'ru'
    else:
        return [{f'{subkey}': texts}]

    body = {
        "targetLanguageCode": target_language,
        "texts": texts,
        "folderId": YANDEX_folder_id,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(YANDEX_IAM_TOKEN)
    }

    response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
        json=body,
        headers=headers
    )

    result = response.json()
    good_result = []
    for index, translation in enumerate(result['translations']):
        good_result.append({f'{subkey}{target_language}': translation['text'],
                            f'{subkey}{start_language}': texts[index]})

    return good_result