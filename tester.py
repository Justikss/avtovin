import asyncio

import requests
from icecream import ic
from langdetect import detect


async def detect_language(text):
    if isinstance(text, list):
        text = text[0]
    language = detect(text)
    return language


async def translate(texts):

    start_language = await detect_language(texts)
    target_language = 'ru'
    # start_language = 'ru' if inputted_language == 'ru' else 'uz'

    YANDEX_IAM_TOKEN = 't1.9euelZrKxomPnMqblZ7Gy5yMlsyPz-3rnpWajo-TkI2Tl4yMi5zHj5yRxpfl8_dHEGZS-e8AGmsp_d3z9wc_Y1L57wAaayn9zef1656VmpSJj8aPzI-bjZeNkJudjJvH7_zF656VmpSJj8aPzI-bjZeNkJudjJvH.2TJpmi3fPOgy8f16GAUwFNOppQ6nYq6ezhYoPgiGSstztXvCZzZo7qz0f7qYwOLSh0mD14xQCMHq6vZ-Qbw9AQ'
    YANDEX_folder_id = 'b1gi4hqlk5765s1otffr'

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
    ic(result['translations'])
    for index, translation in enumerate(result['translations']):
        good_result.append({target_language: translation['text'], start_language: texts[index]})

    print(good_result)
    return good_result

asyncio.run(translate('Complectation'))
