import sys
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

sys.path.insert(0, '..')
print(sys.path)

#from handlers.state_handlers.seller_states_handler.seller_registration import hybrid_input_seller_number
from tests import utils
sys.path.insert(0, '..')
from loader import dp
from handlers.callback_handlers.sell_part.seller_main_menu import seller_main_menu
from keyboards.inline.kb_creator import InlineCreator
from utils.lexicon_utils.Lexicon import LEXICON
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
async def test_callback_handler(bot, storage, dispatcher):
    #callback = AsyncMock()
    message = get_message(photo=True)
    current_method = seller_main_menu
    photo = {'id': '123123', 'unique_id': '1231424114'}
    
    # storage = storage()
    
    #TEST_MESSAGE = utils.get_message('america')
    

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
    await state.update_data(load_photo = {'id': '12344', 'unique_id': '3333333'})

    await state.set_state(LoadCommodityStates.load_config_output)

    input_data = LEXICON['seller_main_menu']
    text = input_data['message_text']
    keyboard = await InlineCreator.create_markup(input_data=input_data)

    with patch('aiogram.Bot.send_photo', new_callable=AsyncMock) as mock_photo:
        
        with patch('aiogram.Bot', new_callable=MagicMock) as mock_bot:

            mock_riddle = AsyncMock()

            TEST_CALLBACK = utils.get_callback(data='rewrite_boot_color')
            TEST_UPDATE = utils.get_update(callback=TEST_CALLBACK)
            dp.update(TEST_UPDATE)
            print('rewrite args ', mock_bot.call_args)
            print('bot_called ', mock_bot.mock_calls)
            #mock_message.assert_called_once()


        TEST_CALLBACK = utils.get_callback(data='load_color_red')
        TEST_UPDATE = utils.get_update(callback=TEST_CALLBACK)
        dp.update(TEST_UPDATE)
        


        print('after_rewrite args', mock_photo.call_args)

        mock_photo.assert_called()
        
    await redis_data.delete_key(key=str(message.from_user.id) + ':can_edit_seller_boot_commodity')
 