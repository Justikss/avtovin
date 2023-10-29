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
from tests.utils import TEST_USER, TEST_USER_CHAT, TEST_MESSAGE
sys.path.insert(0, '..')
from loader import seller_registration




# @pytest.mark.asyncio()
# async def test_message_handler():
#     message = AsyncMock()
#     await #method
#     message.answer.assert_called_with()



@pytest.mark.asyncio()
async def test_callback_handler(bot, storage):
    #callback = AsyncMock()
    message = AsyncMock()
    hybrid_input_seller_number = seller_registration.hybrid_input_seller_number
    

    message = Message(
        message_id=123,
        date=datetime.now(),
        chat=TEST_USER_CHAT,
        text='america'
    )


    state = FSMContext(
        
        storage=storage,
        key=StorageKey(
            bot_id=bot.id,
            user_id=TEST_USER.id,
            chat_id=TEST_USER_CHAT.id
        )
    )

    await hybrid_input_seller_number(request=TEST_MESSAGE, state=state, bot=bot)
    await bot.method.assert_called_with(incorrect=True)
    
