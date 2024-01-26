import asyncio

from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
import importlib

from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.utils.add_new_value_advert_parameter.input_media_group_to_advert.input_media import \
    InputCarPhotosToSetParametersBranchHandler


class MessageIsPhoto(BaseFilter):
    '''Этот фильтр контролирует вхождение фотографии в конечное состояние загрузки товара'''
    async def chat_cleaner(self, trash_redis_keys, message, user_id=None):
        redis_module = importlib.import_module('utils.redis_for_language')
        if isinstance(message, CallbackQuery):
            message = message.message
        if not user_id:
            user_id = str(message.from_user.id)
            chat_id = message.chat.id
        else:
            chat_id = user_id
        tasks = []
        for redis_key in trash_redis_keys:
            redis_key = f'{user_id}{redis_key}'
            last_message_id = await redis_module.redis_data.get_data(key=redis_key)
            if last_message_id:
                if not isinstance(last_message_id, int):
                    last_message_id = int(last_message_id)
                ic(last_message_id)
                tasks.append(MessageIsPhoto().delete_message(message=message, chat_id=chat_id,
                                                             last_message_id=last_message_id))
                await redis_module.redis_data.delete_key(key=redis_key)

        await asyncio.gather(*tasks)


    async def delete_message(self, message, chat_id, last_message_id):
        try:
            await message.bot.delete_message(chat_id=chat_id, message_id=last_message_id)
        except:
            pass

    async def __call__(self, message: Message, state: FSMContext):
        '''Сама вызывающаяся функция фильтра. Контролирует вхождение фотографии'''
        redis_module = importlib.import_module('utils.redis_for_language')
        redis_key_seller = str(message.from_user.id) + ':last_seller_message'
        photo_to_load_module = importlib.import_module('handlers.state_handlers.seller_states_handler.load_new_car.hybrid_handlers')

        input_photo = message.photo
        ic(input_photo)
        reply_mode = False
        if not input_photo:
            reply_mode = True

        await self.chat_cleaner(trash_redis_keys=(':last_message', ':last_seller_message'),
                                 message=message)

        await redis_module.redis_data.set_data(key=redis_key_seller,
                                                value=message.message_id)
        ic()

        current_state = str(await state.get_state())
        match current_state:
            case 'LoadCommodityStates:photo_verification':
                await photo_to_load_module.input_photo_to_load(request=message, state=state, incorrect=True)  #

            case 'AdminAdvertParametersStates.NewStateStates:await_input_new_car_photos':
                await InputCarPhotosToSetParametersBranchHandler().callback_handler(message, state, incorrect=True)
