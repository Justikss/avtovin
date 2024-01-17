# def is_english_with_spaces(text):
#     return any('A' <= char <= 'Z' or 'a' <= char <= 'z'  for char in text)
#
# text = "ф ыффыв"
# if is_english_with_spaces(text):
#     print("Text consists of English letters and spaces.")
# else:
#     print("Text does not consist of English letters and spaces.")
# import asyncio
# import httpx
#
# async def send_request():
#     url = "https://prekladac24.cz/wp-content/themes/translatica/inc/translator.php"
#     params = {
#         "from": "ru",
#         "to": "uz",
#         "text": "White"
#     }
#
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#         "Referer": "https://prekladac24.cz/",
#         "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"',
#         "Sec-Ch-Ua-Mobile": "?0",
#         "Sec-Ch-Ua-Platform": '"Windows"',
#         "Sec-Fetch-Dest": "empty",
#         "Sec-Fetch-Mode": "cors",
#         "Sec-Fetch-Site": "same-origin",
#         "Sec-Gpc": "1",
#         "Accept": "*/*",
#         "Accept-Encoding": "gzip, deflate, br",
#         "Accept-Language": "ru-RU,ru;q=0.7"
#     }
#
#     async with httpx.AsyncClient() as client:
#         response = await client.get(url, params=params, headers=headers)
#         print("Status Code:", response.status_code)
#         print("Response Content:", response.text)
#
# if __name__ == "__main__":
#     asyncio.run(send_request())