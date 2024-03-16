import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from states.cost_filter_in_buy_search import BuyerSearchCostFilterStates
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler

class CloseWindowCarPriceFilterHandler(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        from handlers.state_handlers.choose_car_for_buy.hybrid_handlers import search_config_output_handler
        cost_filter = None
        match request.data:
            case 'set_buyer_cost_filter':
                cost_filter = await self.get_price_diapason(state)
            case 'remove_buyer_cost_filter':
                await state.update_data(buyer_cost_filter_data=None)

        await search_config_output_handler(request, state, False, cost_filter)


    async def get_price_diapason(self, state):
        data_to_query = None
        memory_storage = await state.get_data()
        buyer_cost_filter_data = memory_storage.get('buyer_cost_filter_data')
        ic(buyer_cost_filter_data)
        if buyer_cost_filter_data:
            data_to_query = dict()
            for diapason_point, cost_to_currency in buyer_cost_filter_data.items():
                ic(diapason_point, cost_to_currency)
                usd_price = None
                sum_price = None
                match cost_to_currency['valute']:
                    case 'usd':
                        usd_price = cost_to_currency['price']
                    case 'sum':
                        sum_price = cost_to_currency['price']

                from utils.get_currency_sum_usd import get_valutes
                prices = await get_valutes(usd=usd_price, sum_valute=sum_price)

                ic(prices)
                data_to_query[diapason_point] = {'usd': prices[0].replace(',', ''), 'sum': prices[1].replace(',', '')}
        return data_to_query