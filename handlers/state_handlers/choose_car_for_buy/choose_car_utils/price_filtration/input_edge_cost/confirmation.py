import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from states.cost_filter_in_buy_search import BuyerSearchCostFilterStates
from utils.get_currency_sum_usd import get_valutes
from utils.oop_handlers_engineering.update_handlers.base_objects.base_message_handler_init import BaseMessageHandler


class ConfirmationCarPriceFilterInputHandler(BaseMessageHandler):
    async def process_message(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        await self.set_state(state, BuyerSearchCostFilterStates.confirmation)
        self.output_methods = [
            self.menu_manager.travel_editor(
                lexicon_part=await self.construct_lexicon_part(state, **kwargs),
                delete_mode=True
            )
        ]


    async def construct_lexicon_part(self, state: FSMContext, **kwargs):
        lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
        memory_storage = await state.get_data()
        selected_diapason_side = memory_storage.get('selected_side_to_input')
        lexicon_part = lexicon_module.LEXICON['buyer_price_filter_input_confirmation']

        price_string = await self.inputted_price_accepter(state, kwargs.get('price'), kwargs.get('head_valute'))

        lexicon_part['message_text'] = lexicon_part['message_text'].format(from_or_before=lexicon_module.LEXICON[
            f'{selected_diapason_side}_caption'
        ],
                                                                           cost=price_string)
        return lexicon_part

    async def inputted_price_accepter(self, state: FSMContext, price, head_valute):
        usd_price = None
        sum_price = None
        match head_valute:
            case 'usd':
                usd_price = price
            case 'sum':
                sum_price = price

        await state.update_data(search_mode_cost_filter_confirmation={'price': price, 'valute': head_valute})
        price_string = await get_valutes(usd=usd_price, sum_valute=sum_price, get_string=True)
        ic(price_string)
        return price_string
