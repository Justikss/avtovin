from aiogram.types import CallbackQuery, Message
from typing import Union
import importlib

from database.data_requests.person_requests import PersonRequester
from utils.Lexicon import LEXICON


async def user_permission_controller(request: Union[CallbackQuery, Message], mode: str):
    travel_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    
    user_id = request.from_user.id

    seller = False
    user = False
    
    if mode == 'buyer':
        user = True

    elif mode == 'seller':
        seller = True
        

    user_model = PersonRequester.get_user_for_id(user_id=user_id, seller=seller, user=user)
    if not user_model:
        if isinstance(request, CallbackQuery):
            await request.answer(LEXICON['user_havent_permision'])
        return await travel_editor.travel_editor.edit_message(lexicon_key='hello_text', request=request, delete_mode=True)
        