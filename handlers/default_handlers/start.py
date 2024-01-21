import importlib
from datetime import datetime

from aiogram.fsm.context import FSMContext
from aiogram.types import Message


from handlers.utils.delete_message import delete_message
from handlers.utils.message_answer_without_callback import send_message_answer
from keyboards.inline.kb_creator import InlineCreator
from utils.oop_handlers_engineering.update_handlers.base_objects.utils_objects.incorrect_adapter import IncorrectAdapter
from utils.redis_for_language import redis_data
from handlers.custom_filters.message_is_photo import MessageIsPhoto
from handlers.callback_handlers.sell_part.seller_main_menu import delete_media_groups
from utils.chat_header_controller import header_controller

async def bot_start(message: Message, state: FSMContext):
    travel_editor = importlib.import_module('handlers.message_editor')

    await header_controller(message, need_delete=True)
    await delete_media_groups(request=message)

    await state.clear()
    try:
        await message.delete()
    except:
        pass
    # try:
    #     await AdminManager.get_admin(message, message.from_user.id)
    # except:
    #     await AdminManager.set_admin(message.from_user.id)
    await delete_message(message, await IncorrectAdapter().get_last_incorrect_message_id(state))
    await MessageIsPhoto.chat_cleaner(self=MessageIsPhoto,
                                    trash_redis_keys=(':last_seller_message', ':last_user_message', ':last_message'), message=message)
#     if message.from_user.id == 6306554751:
#         await manager.create(User, telegram_id = 6306554751,
# username = '@levtips',
# name = 'asddas',
# surname = 'sdafg',
# patronymic = None,
# phone_number = '+79371567373',
# data_registration = datetime.now().strftime(REGISTRATION_DATETIME_FORMAT))


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

    await redis_data.delete_key(key=str(message.from_user.id) + ':seller_registration_mode')

    await travel_editor.travel_editor.edit_message(lexicon_key='choose_language', request=message, delete_mode=True)
    await redis_data.delete_key(key=str(message.from_user.id) + ':can_edit_seller_registration_data')

    # await send_message_answer(message, 'asdasd')
    # lexicon_part = LEXICON['choose_language']
    # message_text = lexicon_part['message_text']
    # keyboard = await InlineCreator.create_markup(lexicon_part)
    #
    # message_object = await message.answer(text=message_text, reply_markup=keyboard)
    # await redis_data.set_data(str(message.from_user.id) + ':last_message', message_object.message_id)

