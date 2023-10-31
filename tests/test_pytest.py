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
from keyboards.inline.kb_creator import InlineCreator
from utils.Lexicon import LEXICON



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

    input_data = LEXICON['seller_main_menu']
    text = input_data['message_text']
    keyboard = await InlineCreator.create_markup(input_data=input_data)

    with patch('aiogram.Bot.edit_message_text', new_callable=AsyncMock) as mock:

        await seller_main_menu(callback=TEST_CALLBACK, bot=bot)
        #mock.assert_called_once_with(text=text, reply_markup=keyboard)
        print('cal args', mock.call_args)
        mock.assert_called()
        