from aiogram.types import User, Chat, Message
import datetime

TEST_USER = User(id=123, is_bot=False, first_name='Test', last_name='test_name', username='test_username', 
                language_code='ru-RU', is_premium=True)

TEST_USER_CHAT = Chat(id=12, type='private', username=TEST_USER.username, first_name=TEST_USER.first_name,
                        last_name=TEST_USER.last_name)

TEST_MESSAGE = Message(chat=TEST_USER_CHAT, message_id=2, text='as', from_user=TEST_USER, date=datetime.datetime.now(), )