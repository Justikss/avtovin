from typing import Union


from aiogram.types import CallbackQuery, Message

from handlers.message_editor import travel_editor
from handlers.callback_handlers.search_auto_handler import redis_data

async def main_menu(request: Union[CallbackQuery, Message]):
    await travel_editor.edit_message(lexicon_key='main_menu', request=request, delete_mode=True)
    user_id = request.from_user.id
    redis_key = str(user_id) + ':last_lexicon_code'
    await redis_data.set_data(redis_key, 'main_menu')
