from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from database.data_requests.person_requests import PersonRequester
from handlers.state_handlers.buyer_registration_handlers import BuyerRegistationStates
from handlers.state_handlers.buyer_registration_handlers import input_full_name
from handlers.state_handlers.buyer_registration_handlers import main_menu
from utils.Lexicon import LEXICON


async def start_buy(callback: CallbackQuery, state: FSMContext):
    user_from_db = await PersonRequester.get_user_for_id(str(callback.from_user.id), user=True)
    if user_from_db:
        await callback.answer(LEXICON['user_in_system']['message_text'])
        await main_menu(request=callback)
    else:
        await callback.answer()
        await state.clear()
        await state.set_state(BuyerRegistationStates.input_full_name)
        await state.update_data(last_message=callback.message.message_id)
        await input_full_name(request=callback, state=state)
