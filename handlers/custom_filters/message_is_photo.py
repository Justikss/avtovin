from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from typing import Union
import importlib
import requests
# import cv2
# import numpy as np

from handlers.state_handlers.seller_states_handler.load_new_car.hybrid_handlers import input_photo_to_load


class MessageIsPhoto(BaseFilter):
    '''Этот фильтр контролирует вхождение фотографии в конечное состояние загрузки товара'''
    # async def is_image_url(self, url):
    #     '''Метод проверки входящей ссылки на наличие в ней изображения'''
    #     response = requests.head(url)
    #     content_type = response.headers.get("content-type")
    #     if "image" in content_type:
    #         return True
    #     return False

    # async def is_valid_image(self, url):
    #     '''Метод проверяет входящую ссылку на валидность ссылки на  фотографию'''
    #     try:
    #         response = requests.get(url, stream=True)
    #         response.raise_for_status()
    #         arr = np.asarray(bytearray(response.content), dtype=np.uint8)
    #         image = cv2.imdecode(arr, -1) # 'Load it as it is'
    #         # Дополнительные проверки изображения, если необходимо
    #         return True
    #     except (requests.HTTPError, requests.ConnectionError, IOError):
    #         return False

    async def chat_cleaner(self, trash_redis_keys, message):
        redis_module = importlib.import_module('utils.redis_for_language')
        user_id = str(message.from_user.id)
        for redis_key in trash_redis_keys:
            redis_key = user_id + redis_key
            last_message_id = await redis_module.redis_data.get_data(key=redis_key)
            if last_message_id:
                try:
                    await message.bot.delete_message(chat_id=message.chat.id, message_id=last_message_id)
                    await redis_module.redis_data.delete_key(key=redis_key)
                    #print('|||dele_mes ', message_id)

                except:
                    # print('|||fuck_delete, ', message_id)
                    pass

 

        # for message_id, redis_key in trash_messages_data:
        #     if len(trash_messages_data[0]) == 1:
        #         message_id, redis_key = trash_messages_data[0], trash_messages_data[1]
        #     if message_id != None:
        #         try:
        #             await message.bot.delete_message(chat_id=message.chat.id, message_id=message_id)
        #             await redis_module.redis_data.delete_key(key=redis_key)
        #             print('|||dele_mes ', message_id)

        #         except:
        #             print('|||fuck_delete, ', message_id)
        #             pass

    async def __call__(self, message: Message, state: FSMContext):
        '''Сама вызывающаяся функция фильтра. Контролирует вхождение фотографии'''
        redis_module = importlib.import_module('utils.redis_for_language')
        redis_key_seller = str(message.from_user.id) + ':last_seller_message'
        # redis_key_bot = str(message.from_user.id) + ':last_message'

        # last_seller_message = await redis_module.redis_data.get_data(key=redis_key_seller)
        # last_bot_message = await redis_module.redis_data.get_data(key=redis_key_bot)
        input_photo = message.photo
        if not input_photo:
            a = '|||user_mes '
            print(a, message.message_id)
        else:
            a='|||user_pho '
            print(a, message.message_id)
            

        #if not input_photo and self.is_image_url(message.text) and self.is_valid_image(message.text):
        #   return {'photo': {'photo_url': message.text}}

        if input_photo:
   
            

            # print('ласт в удовл: ', last_seller_message)
            await self.chat_cleaner(trash_redis_keys=(':last_message', ':last_seller_message'),
                                     message=message)

            return {'photo': {'id': input_photo[0].file_id, 'unique_id': input_photo[0].file_unique_id}}

        else:
            
            trash_messages_data = (':last_message', ':last_seller_message')

            await self.chat_cleaner(trash_redis_keys=trash_messages_data, message=message)
            print('|||adde_us_mes: ', message.message_id)
            await redis_module.redis_data.set_data(key=redis_key_seller, 
                                                    value=message.message_id)

            await input_photo_to_load(request=message, state=state, incorrect=True)
