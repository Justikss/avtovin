import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler

class ResetCurrentRangeSideForBuyer(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
        from handlers.state_handlers.choose_car_for_buy.choose_car_utils.price_filtration.choose_diapason_side import \
            ChooseCarPriceFilterHandler

        memory_storage = await state.get_data()
        selected_diapason_side = memory_storage.get('selected_side_to_input')
        buyer_cost_filter_data = memory_storage.get('buyer_cost_filter_data')
        side_keys = {'from': 'min', 'before': 'max'}
        del buyer_cost_filter_data[side_keys[selected_diapason_side]]

        await state.update_data(buyer_cost_filter_data=buyer_cost_filter_data)
        await self.send_alert_answer(request, lexicon_module.captions['confirm'])
        await ChooseCarPriceFilterHandler().callback_handler(request, state)
