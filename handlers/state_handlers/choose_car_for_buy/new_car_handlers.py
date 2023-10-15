from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery

from states.hybrid_choose_states import HybridChooseStates
from database.data_requests.commodity_requests import CommodityRequester
from handlers.callback_handlers.main_menu import travel_editor





async def choose_complectation_handler(callback: CallbackQuery, state: FSMContext):
    memory_storage = await state.get_data()
    user_answer = callback.data.split(':')[1]  # Второе слово - ключевое к значению бд
    await state.update_data(cars_engine_type=user_answer)

    models_range = CommodityRequester.get_for_request(state=memory_storage['cars_state'],
                                                      brand=memory_storage['cars_brand'],
                                                      model=memory_storage['cars_model'],
                                                      engine_type=user_answer)

    button_texts = {car.complectation for car in models_range}
    await travel_editor.edit_message(request=callback, lexicon_key='choose_complectation', button_texts=button_texts,
                                     callback_sign='cars_complectation:')

    await state.set_state(HybridChooseStates.config_output)
