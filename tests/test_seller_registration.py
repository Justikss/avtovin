# import unittest
# import asyncio
# from aiogram import Bot, Dispatcher, types
# from unittest.mock import AsyncMock
# from aiogram.fsm.context import FSMContext
# import sys
# from datetime import datetime

# sys.path.insert(0, '..')

# from config_data.config import BOT_TOKEN, DEAL_CHAT
# from handlers.state_handlers.seller_states_handler.seller_registration import hybrid_input_seller_number
# from handlers.custom_filters.correct_name import CheckInputName

# class TestBot(unittest.TestCase):
#     def setUp(self):
#         self.loop = asyncio.get_event_loop()
#         self.bot = Bot(token=BOT_TOKEN)
#         print(self.bot)
#         self.dp = Dispatcher(bot=self.bot)

#     def test_start_command(self):


#         async def test():
#             custom_filter = AsyncMock(CheckInputName)
#             custom_filter.check = AsyncMock(return_value=True)

#             message = types.Message(message_id=1, chat=types.Chat(id=DEAL_CHAT, type='public'), text="as", from_user=types.User(id=1, is_bot=False, first_name='Test'), date=datetime.now())



#             state = AsyncMock(FSMContext)
#             state.get_state = AsyncMock(return_value='HybridSellerRegistrationStates:input_number')

#             # Теперь вы можете вызвать обработчик с мок-объектом для FSMContext
#             self.dp.message(hybrid_input_seller_number, custom_filter(), state=state)

#             # Отправляем сообщение боту
#             await self.bot.send_message(chat_id=message.chat.id, text=message.text)
#             await asyncio.gather(test())
            

#         # self.loop.run_until_complete(test())

# if __name__ == '__main__':
#     unittest.main()


