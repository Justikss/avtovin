from copy import copy

from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import importlib

from handlers.callback_handlers.admin_part.admin_panel_ui.tariff_actions.input_tariff_data import process_tariff_cost
from handlers.callback_handlers.sell_part.commodity_requests.rewrite_price_by_seller import \
    rewrite_price_by_seller_handler
from handlers.state_handlers.choose_car_for_buy.choose_car_utils.price_filtration.input_edge_cost.utils.price_filter_module import \
    price_adverts_filter_module
from handlers.state_handlers.seller_states_handler.load_new_car.hybrid_handlers import input_price_to_load
from handlers.utils.delete_message import delete_message

config_module = importlib.import_module('config_data.config')

class PriceIsDigit(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext):
        '''Фильтр контроллирует вход числа во время загрузки нового товара'''
        redis_module = importlib.import_module('utils.redis_for_language')
        redis_key_user_message = str(message.from_user.id) + ':last_seller_message'
        redis_key_bot_message = str(message.from_user.id) + ':last_message'
        message_text = copy(message.text)
        incorrect_flag = False
        if '$' in message_text:
            ic()
            if message_text.count('$') > 1:
                incorrect_flag = '$'
            message_text = message_text.replace('$', ' ').strip()
            dollar_cost = True
            ic(message_text)
        else:
            dollar_cost = False
        head_valute = 'sum' if not dollar_cost else 'usd'
        car_price = int(message_text) if message_text.isdigit() else message_text
        ic()
        if not incorrect_flag:
            incorrect_flag = await price_adverts_filter_module(inputted_cost=car_price, currency=head_valute, state=state)
        if message_text.isdigit() and len(str(message_text)) < config_module.max_price_len and not incorrect_flag:

            ic(message.text.isdigit())
            await delete_message(message, chat_id=message.chat.id, message_id=message.message_id)
            last_seller_message = await redis_module.redis_data.get_data(key=redis_key_user_message)
            if last_seller_message:
                await delete_message(message, chat_id=message.chat.id, message_id=last_seller_message)
                await redis_module.redis_data.delete_key(key=redis_key_user_message)
            ic()
            ic(head_valute)
            await state.update_data(head_valute=head_valute)
            return {'price': car_price, 'head_valute': head_valute}
        else:
            if not incorrect_flag:
                incorrect_flag = True
            last_seller_message = await redis_module.redis_data.get_data(key=redis_key_user_message)
            last_bot_message = await redis_module.redis_data.get_data(key=redis_key_bot_message)

            if last_seller_message:
                    await delete_message(message, chat_id=message.chat.id, message_id=last_seller_message)
                    await redis_module.redis_data.delete_key(key=redis_key_user_message)

            if last_bot_message:
                await delete_message(message, chat_id=message.chat.id, message_id=last_bot_message)
                await redis_module.redis_data.delete_key(key=redis_key_bot_message)

            await redis_module.redis_data.set_data(key=redis_key_user_message, 
                                                    value=message.message_id)
            current_state = str(await state.get_state())

            if current_state.startswith('TariffAdminBranchStates'):
                await state.update_data(admin_incorrect_flag=True)
                await process_tariff_cost(message, state, incorrect=incorrect_flag)

            elif current_state == 'RewritePriceBySellerStates:await_input':
                await rewrite_price_by_seller_handler(message, state, incorrect=incorrect_flag)

            elif current_state.startswith('BuyerSearchCostFilterStates'):

                from handlers.state_handlers.choose_car_for_buy.choose_car_utils.price_filtration.input_edge_cost.start import \
                    StartInputCarPriceFilterStartInputHandler
                await StartInputCarPriceFilterStartInputHandler().callback_handler(message, state, incorrect=incorrect_flag)

            else:
                await input_price_to_load(request=message, state=state, incorrect=incorrect_flag)