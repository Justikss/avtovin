import importlib

from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.data_requests.banned_person_requests import BannedRequester
from handlers.callback_handlers.buy_part.language_callback_handler import set_language
from handlers.utils.message_answer_without_callback import send_message_answer



class UserBlockStatusController(BaseFilter):
    def __init__(self, user_status = None):
        self.user_status = user_status
    async def stop_user_actions(self, request):
        lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

        lexicon_text = lexicon_module.LEXICON['you_are_blocked_alert']
        await send_message_answer(request, lexicon_text, 1)

        await set_language(request, set_languange=False)

    async def check_user_status(self, request: Message | CallbackQuery, state: FSMContext):
        redis_data_module = importlib.import_module('utils.redis_for_language')
        person_requester_module = importlib.import_module('database.data_requests.person_requests')
        ic()
        redis_key = f'{request.from_user.id}:user_state'
        user_state = self.user_status
        if not user_state:
            user_state = await redis_data_module.redis_data.get_data(key=redis_key)
        if user_state:
            user = False
            seller = False
            match user_state:
                case 'buy':
                    user = True
                case 'sell':
                    seller = True

            banned_user = await BannedRequester.user_is_blocked(telegram_id=request.from_user.id,
                                                                seller=seller,
                                                                user=user)
            ic(banned_user)
            if banned_user == 'yes':
                await redis_data_module.redis_data.delete_key(redis_key)
                await self.stop_user_actions(request)
                if await state.get_state():
                    await state.clear()
                return False
            else:
                return True

    async def __call__(self, request: Message | CallbackQuery, state: FSMContext):
        return await self.check_user_status(request, state)

