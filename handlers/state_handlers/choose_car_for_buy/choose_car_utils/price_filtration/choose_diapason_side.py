import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from states.cost_filter_in_buy_search import BuyerSearchCostFilterStates
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler

class ChooseCarPriceFilterHandler(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        await self.incorrect_manager.try_delete_incorrect_message(state=state, request=request, mode='buyer')
        await self.set_state(state, BuyerSearchCostFilterStates.review)
        lexicon_part = await self.construct_lexicon_part(request, state)
        self.output_methods = [
            self.menu_manager.travel_editor(
                lexicon_part=lexicon_part,
                dynamic_buttons=2,
                delete_mode=True
            )
        ]

    async def construct_lexicon_part(self, request, state):
        lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

        memory_storage = await state.get_data()
        price_diapason = memory_storage.get('buyer_cost_filter_data')
        lexicon_part = lexicon_module.LEXICON['buyer_price_filter_review']
        message_text_data = lexicon_part['message_text']
        lexicon_part['message_text'] = message_text_data['default']
        if price_diapason:
            lexicon_part['message_text'] += message_text_data['selected_caption']
            for key, value in price_diapason.items():
                usd_price = None
                sum_price = None
                match value['valute']:
                    case 'usd':
                        usd_price = value['price']
                    case 'sum':
                        sum_price = value['price']

                from utils.get_currency_sum_usd import get_valutes
                price_string = await get_valutes(usd=usd_price, sum_valute=sum_price, get_string=True)
                lexicon_part['message_text'] += message_text_data[f'{key}_caption'].format(price=price_string)

        return lexicon_part

