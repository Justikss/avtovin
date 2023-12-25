import importlib

from aiogram.types import CallbackQuery, Message

from database.data_requests.admin_requests import AdminManager
from handlers.callback_handlers.buy_part.language_callback_handler import set_language
from handlers.utils.message_answer_without_callback import send_message_answer
from utils.custom_exceptions.database_exceptions import AdminDoesNotExistsError
from utils.lexicon_utils.Lexicon import ADMIN_LEXICON


async def admin_exists_checker(callback: CallbackQuery):

    try:
        await AdminManager.get_admin(request=callback)
        return True
    except AdminDoesNotExistsError:

        redis_data_module = importlib.import_module('utils.redis_for_language')
        redis_key = f'{callback.from_user.id}:user_state'
        await redis_data_module.redis_data.delete_key(redis_key)

        await admin_does_not_exists_handler(callback)
        return False
async def admin_does_not_exists_handler(request: CallbackQuery | Message):
    lexicon_text = ADMIN_LEXICON['user_havent_admin_permission']
    if isinstance(request, CallbackQuery):
        await request.answer(lexicon_text)
    else:
        await send_message_answer(request, lexicon_text, 1)

    await set_language(request, set_languange=False)