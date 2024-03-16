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
    from database.data_requests.admin_requests import AdminManager
    from config_data.config import TEST_MOMENT

    header_controller_module = importlib.import_module('handlers.default_handlers.start')
    await header_controller_module.header_controller(message, need_delete=True)


    if TEST_MOMENT:
        await AdminManager.set_red_admin(message.from_user.id)

    from utils.oop_handlers_engineering.update_handlers.base_objects.utils_objects.incorrect_adapter import \
        IncorrectAdapter
    await IncorrectAdapter().try_delete_incorrect_message(message, state)

    # await header_controller(message, need_delete=True)
    await delete_media_groups(request=message)

    await state.clear()
    if isinstance(message, Message):
        try:
            await message.delete()
        except:
            pass

    await MessageIsPhoto.chat_cleaner(self=MessageIsPhoto,
                                    trash_redis_keys=(':last_seller_message',
                                                      ':last_user_message',
                                                      ':last_message'),
                                      message=message)

    await redis_data.delete_key(key=str(message.from_user.id) + ':seller_registration_mode')

    await travel_editor.travel_editor.edit_message(lexicon_key='choose_language', request=message, delete_mode=True)
    await redis_data.delete_key(key=str(message.from_user.id) + ':can_edit_seller_registration_data')
