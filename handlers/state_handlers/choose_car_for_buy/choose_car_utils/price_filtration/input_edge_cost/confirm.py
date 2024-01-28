import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from handlers.state_handlers.choose_car_for_buy.choose_car_utils.price_filtration.choose_diapason_side import \
    ChooseCarPriceFilterHandler
from states.cost_filter_in_buy_search import BuyerSearchCostFilterStates
from utils.get_currency_sum_usd import get_valutes
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler

class ConfirmInputtedCarPriceFilterValueInputHandler(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

        await self.handle_confirm(state)
        await self.send_alert_answer(request, lexicon_module.captions['confirm'])
        await ChooseCarPriceFilterHandler().callback_handler(request, state)

    async def handle_confirm(self, state: FSMContext):
        memory_storage = await state.get_data()
        selected_diapason_side = memory_storage.get('selected_side_to_input')
        search_mode_cost_filter_confirmation = memory_storage.get('search_mode_cost_filter_confirmation')
        # buyer_cost_filter_data = memory_storage.get('buyer_cost_filter_data')
        ic(search_mode_cost_filter_confirmation)

        buyer_cost_filter_data = memory_storage.get('buyer_cost_filter_data')
        if not buyer_cost_filter_data:
            buyer_cost_filter_data = dict()

        diapason_side_name = ''
        match selected_diapason_side:
            case 'from':
                diapason_side_name = 'min'
            case 'before':
                diapason_side_name = 'max'

        buyer_cost_filter_data[diapason_side_name] = search_mode_cost_filter_confirmation
        ic(await state.update_data(buyer_cost_filter_data=buyer_cost_filter_data))