import sys
from datetime import datetime
import pytest
from unittest.mock import AsyncMock
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




# @pytest.mark.asyncio()
# async def test_message_handler():
#     message = AsyncMock()
#     await #method
#     message.answer.assert_called_with()



@pytest.mark.asyncio()
async def test_callback_handler(bot, storage):
    #callback = AsyncMock()
    message = AsyncMock()
    current_method = seller_main_menu
    

    TEST_MESSAGE = utils.get_message('america')
    TEST_CALLBACK = utils.get_callback('oa')
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

    await seller_main_menu(callback=TEST_CALLBACK)
    await TEST_CALLBACK.message.assert_any_call()
    
