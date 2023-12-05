import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from handlers.message_editor import InlineCreator
from handlers.callback_handlers.buy_part.language_callback_handler import redis_data
from handlers.custom_filters.message_is_photo import MessageIsPhoto
from database.data_requests.tariff_to_seller_requests import TariffsToSellers
from handlers.callback_handlers.sell_part.seller_main_menu import delete_media_groups
from utils.chat_header_controller import header_controller


async def bot_start(message: Message, state: FSMContext):
    travel_editor = importlib.import_module('handlers.message_editor')
    redis_module = importlib.import_module('utils.redis_for_language')

    await header_controller(message, need_delete=True)
    await delete_media_groups(request=message)

    await state.clear()
    try:
        await message.delete()
    except:
        pass

    await MessageIsPhoto.chat_cleaner(self=MessageIsPhoto,
                                    trash_redis_keys=(':last_seller_message', ':last_user_message', ':last_message'), message=message)

    # if last_user_message:
    #     try:
    #         await message.chat.delete_message(message_id=last_user_message)
    #     except:
    #         await redis_module.redis_data.delete_key(key=str(message.from_user.id) + ':last_user_message')

    #     await redis_module.redis_data.delete_key(key=str(message.from_user.id) + ':last_user_message')

    # user_id = message.from_user.id
    # redis_key = str(user_id) + ':last_message'
    #
    #redis_key = str(message.from_user.id) + ':active_non_confirm_seller_registrations'
    #seller_registration_stack = await redis_module.redis_data.delete_key(key=redis_key)

    await redis_module.redis_data.delete_key(key=str(message.from_user.id) + ':seller_registration_mode')

    await travel_editor.travel_editor.edit_message(lexicon_key='choose_language', request=message, delete_mode=True)
    await redis_module.redis_data.delete_key(key=str(message.from_user.id) + ':can_edit_seller_registration_data')

    # lexicon_part = LEXICON['choose_language']
    # message_text = lexicon_part['message_text']
    # keyboard = await InlineCreator.create_markup(lexicon_part)
    #
    # message_object = await message.answer(text=message_text, reply_markup=keyboard)
    # await redis_data.set_data(str(message.from_user.id) + ':last_message', message_object.message_id)

