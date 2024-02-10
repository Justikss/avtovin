import codecs
import json
import logging
import httpx
import chardet

import httpx

async_client = httpx.AsyncClient()

class ParseTranslator:
    async def has_english_char(self, text):
        return any('A' <= char <= 'Z' or 'a' <= char <= 'z'  for char in text)

    async def multi_decode_async(self, response):
        text = response.text
        result = chardet.detect(text.encode())
        detected_encoding = result['encoding']
        confidence = result['confidence']
        return detected_encoding, confidence
        # encodings = ['utf-8', 'latin-1', 'windows-1251', 'iso-8859-1']
        # for encoding in encodings:
        #
        #     try:
        #         decoded_text = response.content.decode(encoding)
        #         return decoded_text
        #     except UnicodeDecodeError:
        #         continue
        # return None

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
            # "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ru-RU,ru;q=0.7",
           'Accept-Encoding': 'identity'
        }

        if await self.has_english_char(text) and ((not maybe_sorse_uz) and from_lang == 'ru'):
            logging.debug('TRANSLATE: %s has english char', text)
            return {f'_{subkey}': text}
        ic(params, headers)
        response = await async_client.get(url, params=params, headers=headers)
        status_code = response.status_code
        if status_code == 200:
            response_text = response.content.decode('utf-8')
            print('0|||||| ', response_text)

            ic((not response_text.startswith("{")) and ('{' in response_text))
            if (not response_text.startswith("{")) and ('{' in response_text):
                response_text = response_text[response_text.index('{'):response_text.rindex('}')+1].strip()
                ic(type(response_text))

                # response_data = eval(response_text)
            # else:
            print('1|||||| ', response_text)
            ic(response_text)
            print('1|||||| ', response.headers)

            # try:
            response_data = json.loads(response_text)
            # except json.JSONDecodeError:
            #     response_text = await self.multi_decode_async(response)
            #     ic(response_text)
            #     response_data = json.loads(response_text)


                # response_data = response.json()

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
        url = f"https://mymemory.translated.net/api/ajaxfetch?q={text}&langpair=ru-RU|uz-UZ&mtonly=1"

        response = await async_client.get(url)

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