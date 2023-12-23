from aiogram.types import CallbackQuery, Message
from typing import Union
import importlib

from utils.lexicon_utils.Lexicon import LEXICON

from aiogram.filters import BaseFilter

class StatusControl(BaseFilter):
    def __init__(self, status):
        self.status = status
    async def __call__(self, request: Union[CallbackQuery, Message]):
        travel_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
        person_requester_module = importlib.import_module('database.data_requests.person_requests')
        user_id = request.from_user.id

        seller = False
        user = False

        if self.status == 'buyer':
            user = True

        elif self.status == 'seller':
            seller = True

        else:
            return True

        user_model = await person_requester_module.PersonRequester.get_user_for_id(user_id=user_id, seller=seller, user=user)
        if not user_model:
            if isinstance(request, CallbackQuery):
                await request.answer(LEXICON['user_havent_permision'])
            return await travel_editor.travel_editor.edit_message(lexicon_key='hello_text', request=request,
                                                                  delete_mode=True)
        else:
            return True