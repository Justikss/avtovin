import logging
import httpx



class ParseTranslator:
    async def has_english_char(self, text):
        return any('A' <= char <= 'Z' or 'a' <= char <= 'z'  for char in text)



    async def translate(self, text, subkey, from_lang='ru', to_lang='uz', maybe_sorse_uz=False, last_tries=3):
        if not text:
            return None
        if text in ('ДВС', 'IYD'):
            return {f'{subkey}_ru': 'ДВС', f'{subkey}_uz': 'IYD'}

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

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, headers=headers)
            status_code = response.status_code
            if status_code == 200:
                response_data = response.json()
                logging.debug('TRANSLATE: response_data: %s', response.text)
                good_text = response_data.get('text')
                logging.debug('TRANSLATE: Good text: %s', good_text)
                if response_data.get('code') == 'error':
                    if last_tries:
                        return await self.translate(text, subkey, from_lang, to_lang, maybe_sorse_uz, last_tries-1)
                    else:
                        logging.critical('TRANSLATE: Three tries was not work!!!')
                if good_text:
                    good_text = good_text[0]
                    if good_text == text and maybe_sorse_uz:
                        await self.translate(text, subkey=subkey, from_lang=to_lang, to_lang=from_lang)
                    result = {f'{subkey}_{to_lang}': good_text,
                                    f'{subkey}_{from_lang}': text}
                    return result
                else:
                    logging.error('TRANSLATE: Response status code 200, but good text does not translated from %s to %s where source text == %s\nResponse text: %s',
                                  from_lang, to_lang, text, response.text)
            else:
                logging.critical('TRANSLATE: Response status code: %d. Translated from %s to %s where source text == %s\nResponse text: %s',
                                  from_lang, to_lang, text, response.text, status_code)

translate = ParseTranslator()