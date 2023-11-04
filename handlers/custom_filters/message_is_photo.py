from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from typing import Union
import importlib
import requests
from PIL import Image

from handlers.state_handlers.load_new_car.hybrid_handlers import input_photo_to_load


class MessageIsPhoto(BaseFilter):
    '''Этот фильтр контролирует вхождение фотографии в конечное состояние загрузки товара'''
    async def is_image_url(self, url):
        '''Метод проверки входящей ссылки на наличие в ней изображения'''
        response = requests.head(url)
        content_type = response.headers.get("content-type")
        if "image" in content_type:
            return True
        return False

    async def is_valid_image(self, url):
        '''Метод проверяет входящую ссылку на валидность ссылки на  фотографию'''
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            image = Image.open(response.raw)
            # Дополнительные проверки изображения, если необходимо
            return True
        except (requests.HTTPError, requests.ConnectionError, IOError):
            return False

    async def __call__(self, message: Message, state: FSMContext):
        '''Сама вызывающаяся функция фильтра. Контролирует вхождение фотографии'''
        redis_module = importlib.import_module('utils.redis_for_language')
        redis_key = str(message.from_user.id) + ':last_seller_message'

        input_photo = message.photo
        if not input_photo and self.is_image_url(message.text) and self.is_valid_image(message.text):
            return {'photo': {'photo_url': message.text}}

        elif input_photo:
            return {'photo': {'id': input_photo[0].file_id, 'unique_id': input_photo[0].file_unique_id}}

        else:
            last_seller_message = await redis_module.redis_data.get_data(key=redis_key)
            if last_seller_message:
                try:
                    await message.bot.delete_message(chat_id=message.chat.id, message_id=last_seller_message)
                    await redis_module.redis_data.delete_key(key=redis_key)
                except:
                    pass

            await redis_module.redis_data.set_data(key=redis_key, 
                                                    value=message.message_id)

            await input_photo_to_load(message=message, state=state, incorrect=True)
