import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from states.cost_filter_in_buy_search import BuyerSearchCostFilterStates
from utils.get_currency_sum_usd import get_valutes, convertator
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler

class StartInputCarPriceFilterStartInputHandler(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        await self.set_state(state, BuyerSearchCostFilterStates.awaited_input)
        self.output_methods = [
            self.menu_manager.travel_editor(
                lexicon_part=await self.construct_lexicon_part(request, state, kwargs.get('incorrect')),
                reply_message=await self.incorrect_manager.get_last_incorrect_message_id(state, request, 'buyer')
            )
        ]
    async def construct_lexicon_part(self, request, state, incorrect_flag):
        lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

        diapason_side = await self.identify_filter_diapason_side(request, state) # from or before
        lexicon_part = lexicon_module.LEXICON['buyer_price_filter_start_input']
        memory_storage = await state.get_data()

        default_cost_diapason, buyer_cost_filter_data_flag = await self.get_diapason_edges(memory_storage, diapason_side)

        ic(diapason_side, default_cost_diapason)
        lexicon_part['message_text'] = lexicon_part['message_text'].format(
            max_cost=await get_valutes(default_cost_diapason['before'], None, get_string=True),
            min_cost=await get_valutes(default_cost_diapason['from'], None, get_string=True),
            default_side_name=lexicon_module.LEXICON[f'accusative_case_lower_caption_side_{diapason_side}']
        )
        lexicon_part = await self.incorrect_case_handler(incorrect_flag, lexicon_part, lexicon_module)

        if buyer_cost_filter_data_flag:
            selected_diapason_side = memory_storage.get('selected_side_to_input')
            ic(selected_diapason_side, buyer_cost_filter_data_flag)
            side_keys = {'from': 'min', 'before': 'max'}
            if side_keys[selected_diapason_side] in buyer_cost_filter_data_flag:
                lexicon_part['buttons'] = {**lexicon_module.LEXICON['reset_current_range_side_buttons'],
                                           **lexicon_part['buttons']}

        return lexicon_part

    async def incorrect_case_handler(self, incorrect, lexicon_part, lexicon_module):
        match incorrect:
            case '$':
                sub_string = lexicon_module.class_lexicon['incorrect_price_$']
            case True:
                sub_string = lexicon_module.LEXICON['price_incorrect']
            case '(range)':
                sub_string = lexicon_module.LEXICON['price_not_in_range']
            case _ if incorrect and incorrect.startswith('nearest_price:'):
                nearest_price = incorrect.split(':')[-1]
                sub_string = lexicon_module.LEXICON['incorrect_nearest_price'].format(
                    nearest_price=await get_valutes(int(nearest_price), None, get_string=True)
                )
            case _:
                sub_string = ''

        if sub_string:
            sub_string = f'\n<blockquote>{sub_string}\n</blockquote>{lexicon_module.low_sep}\n'

        lexicon_part['message_text'] = f'''{sub_string}{lexicon_part['message_text']}'''
        return lexicon_part

    async def get_diapason_edges(self, memory_storage: dict, current_side=None):
        default_cost_diapason = memory_storage.get('default_costs_diapason_on_buy_search') #keys from / before
        buyer_cost_filter_data = memory_storage.get('buyer_cost_filter_data')

        key_storage = {'min': 'from', 'max': 'before'}


        if buyer_cost_filter_data:
            buyer_cost_filter_data_flag = []
            for key, value in buyer_cost_filter_data.items():
                buyer_cost_filter_data_flag.append(key)
                if current_side == key_storage.get(key):
                    continue
                currency = value['valute']
                cost = value['price']
                match currency:
                    case 'usd':
                        default_cost_diapason[key_storage[key]] = cost
                    case 'sum':
                        default_cost_diapason[key_storage[key]] = await convertator(currency, cost)
        else:
            buyer_cost_filter_data_flag = None
        return default_cost_diapason, buyer_cost_filter_data_flag

    async def identify_filter_diapason_side(self, request, state):
        selected_side = None
        if isinstance(request, CallbackQuery):
            callback_data = request.data
            ic(callback_data)
            if callback_data.startswith('buyer_cost_filter'):
                selected_side = callback_data.split(':')[-1]
                await state.update_data(selected_side_to_input=selected_side)
        if not selected_side:
            memory_storage = await state.get_data()
            selected_side = memory_storage.get('selected_side_to_input')
        ic(selected_side)
        return selected_side