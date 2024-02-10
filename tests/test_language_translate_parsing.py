import asyncio
import logging

import httpx
import pytest
from icecream import ic
import time

client = httpx.AsyncClient()


class ParseTranslator:
    async def has_english_char(self, text):
        return any('A' <= char <= 'Z' or 'a' <= char <= 'z'  for char in text)



    async def translate(self, text, subkey, from_lang='ru', to_lang='uz', maybe_sorse_uz=False, last_tries=3):
        if not text:
            return None
        if text in ('ДВС', 'IYD'):
            return {f'{subkey}_ru': 'ДВС', f'{subkey}_uz': 'IYD'}
        good_text = False
        url = "https://prekladac24.cz/wp-content/themes/translatica/inc/translator.php"
        params = {
            "from": from_lang,
            "to": to_lang,
            "text": text
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://prekladac24.cz/",
            "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Gpc": "1",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ru-RU,ru;q=0.7"
        }

        if await self.has_english_char(text) and ((not maybe_sorse_uz) and from_lang == 'ru'):
            logging.debug('TRANSLATE: %s has english char', text)
            return {f'_{subkey}': text}

        response = await client.get(url, params=params, headers=headers)
        status_code = response.status_code
        if status_code == 200:
            response_data = response.json()
            logging.debug('FIRST TRANSLATE: response_data: %s', response.text)
            good_text = response_data.get('text')
            logging.debug('FIRST TRANSLATE: Good text: %s', good_text)
            if response_data.get('code') == 'error':
                if last_tries:
                    return await self.translate(text, subkey, from_lang, to_lang, maybe_sorse_uz, last_tries-1)
                else:
                    use_extra_trans=True
                    logging.critical('FIRST TRANSLATE: Three tries was not work!!!')
            else:
                use_extra_trans=True
                logging.error(
                    'FIRST TRANSLATE: Response status code 200, but good text does not translated from %s to %s where source text == %s\nResponse text: %s',
                    from_lang, to_lang, text, response.text)
        else:
            use_extra_trans=True
            logging.error(
                'FIRST TRANSLATE: Response status code: %d. Translated from %s to %s where source text == %s\nResponse text: %s',
            from_lang, to_lang, text, response.text, status_code)

        if not good_text:
            good_text = await self.extra_translate(text)
            if not good_text and last_tries:
                return await self.translate(text, subkey, from_lang, to_lang, maybe_sorse_uz, last_tries - 1)
            elif not good_text and not last_tries:
                logging.critical('SECOND TRANSLATE: Three tries was run out!')

        if good_text:
            good_text = good_text[0]
            if good_text == text and maybe_sorse_uz:
                await self.translate(text, subkey=subkey, from_lang=to_lang, to_lang=from_lang)
            result = {f'{subkey}_{to_lang}': good_text,
                            f'{subkey}_{from_lang}': text}
            return result

        else:
            logging.critical('ALL TRANSLATE: good text is empty!')

    async def extra_translate(self, text):
        from urllib.parse import quote

        import requests
        from icecream import ic

        # text_to_encode = "Крутой бот будет если плохо ему не станет"
        encoded_text = quote(text, encoding='utf-8')
        url = f"https://mymemory.translated.net/api/ajaxfetch?q={text}&langpair=ru-RU|uz-UZ&mtonly=1"

        response = await client.get(url)

        if response.status_code == 200:
            data = response.json()  # Парсим ответ в формате JSON
            result = data['matches'][0]['translation'].replace("&#39;", "'")
            if not result:
                logging.error(
                    'FIRST TRANSLATE: Response status code 200, but good text does not translated source text == %s\nResponse text: %s',
                    text, response.text)
            else:

                return result
        else:
            logging.error(
                'SECOND TRANSLATE: Response status code: %d. source text == %s\nResponse text: %s',
                text, response.text, response.status_code)


translate = ParseTranslator()


@pytest.mark.asyncio
async def test_parse_translator():
    event_loop = asyncio.get_running_loop()
    words = ['Синий Спорт', 'Красный', 'Белый', 'Полный привод', 'Двойной двигатель', 'Жёлтый', 'Фиолетовый',
                "Дом", "Солнце", "Вода", "Мать", "Отец", "Медведь", "Цветок", "Море", "Гора", "Лес", "Дерево", "Рыба",
                "Камень", "Поле", "Воздух", "Звезда", "Ветер", "Снег", "Птица", "Небо", "Земля", "Ручей", "Луна",
                "Звук", "Дверь", "Ключ", "Книга", "Рука", "Глаз", "Ухо"]

    # words = [
    #     "salom",  # привет
    #     "rahmat",  # спасибо
    #     "do'st",  # друг
    #     "kitob",  # книга
    #     "maktab",  # школа
    #     "bog'",  # сад
    #     "qalam",  # ручка
    #     "shahar",  # город
    #     "choy",  # чай
    #     "non",  # хлеб
    #     "olma",  # яблоко
    #     "qiz",  # девушка
    #     "bolalar",  # дети
    #     "uy",  # дом
    #     "kuchuk"  # собака
    # ]
    # words_list = words * (10000 // len(words))
    # words_list += words[:10000 % len(words)]
    words_list = words
    ic(len(words_list))
    tasks = []
    start_time = time.time()
    # async with httpx.AsyncClient() as client:
    #     ic(client)
    for word in words_list:
        task = event_loop.create_task(translate.extra_translate(text=word.capitalize()))
        tasks.append(task)

    responses = await asyncio.gather(*tasks)
    ic(responses)
    all_time = time.time() - start_time
    ic(all_time)
    assert all(responses)
    uz_words = []
    for items in responses:
        # uz_words.append(items['name_uz'])
        uz_words.append(items)
    ic(uz_words)
    uz_words_set = set(uz_words)
    ic(uz_words_set)
    assert len(uz_words_set) == len(uz_words)
    print(f'Корректно переведено [{len(words_list)}] из [{len(words_list)}] слов за [{round(all_time)}] секунд.')

    for task in asyncio.all_tasks():
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
