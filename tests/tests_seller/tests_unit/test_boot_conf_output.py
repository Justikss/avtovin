import sys
from datetime import datetime
import pytest
from unittest.mock import AsyncMock, patch
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey


import asyncio
sys.path.insert(0, '..')
print(sys.path)

#from handlers.state_handlers.seller_states_handler.seller_registration import hybrid_input_seller_number
from tests import utils
sys.path.insert(0, '..')
from handlers.callback_handlers.sell_part.seller_main_menu import seller_main_menu
from handlers.state_handlers.seller_states_handler.load_new_car.get_output_configs import output_load_config_for_seller
from keyboards.inline.kb_creator import InlineCreator
from utils.Lexicon import LEXICON
from states.load_commodity_states import LoadCommodityStates
from utils.redis_for_language import redis_data

from tests.conftest import dispatcher, storage
from tests.utils import get_message


# @pytest.mark.asyncio()
# async def test_message_handler():
#     message = AsyncMock()
#     await #method
#     message.answer.assert_called_with()



@pytest.mark.asyncio()
async def test_callback_handler(bot, storage):
    #callback = AsyncMock()
    message = get_message(photo=True)
    current_method = seller_main_menu
    photo = {'id': '123123', 'unique_id': '1231424114'}
    
    # storage = storage()
    
    #TEST_MESSAGE = utils.get_message('america')
    TEST_CALLBACK = utils.get_callback(data='oa')

    TEST_USER = utils.TEST_USER
    TEST_USER_CHAT = utils.TEST_USER_CHAT

    state = FSMContext(
        
        storage=storage,
        key=StorageKey(
            bot_id=bot.id,
            user_id=TEST_USER.id,
            chat_id=TEST_USER_CHAT.id
        )
    )

    await redis_data.set_data(key=str(message.from_user.id) + ':can_edit_seller_boot_commodity', value=True)
    
    # await state.update_data(key = 'value')
    await state.update_data(state_for_load = 'load_state_new')
    await state.update_data(engine_for_load = 'load_engine_hybrid')
    await state.update_data(brand_for_load = 'load_brand_bmw')
    await state.update_data(model_for_load = 'load_model_1')
    await state.update_data(complectation_for_load = 'load_complectation_1')
    await state.update_data(year_for_load = 'load_year_2005')
    await state.update_data(mileage_for_load = 'load_mileage_25000')
    await state.update_data(color_for_load = 'load_color_black')
    await state.update_data(load_price = '1234')

    input_data = LEXICON['seller_main_menu']
    text = input_data['message_text']
    keyboard = await InlineCreator.create_markup(input_data=input_data)

    with patch('aiogram.Bot.send_photo', new_callable=AsyncMock) as mock:

        await output_load_config_for_seller(request=message, photo=photo, state=state, bot=bot)
        #mock.assert_called_once_with(text=text, reply_markup=keyboard)
        # print('cal args', mock.call_args)
        mock.assert_called()
        
    await redis_data.delete_key(key=str(message.from_user.id) + ':can_edit_seller_boot_commodity')
    