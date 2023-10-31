from aiogram.types import User, Chat, Message, Update, CallbackQuery
import datetime

TEST_USER = User(id=123, is_bot=False, first_name='Test', last_name='test_name', username='test_username', 
                language_code='ru-RU', is_premium=True)

TEST_USER_CHAT = Chat(id=12, type='private', username=TEST_USER.username, first_name=TEST_USER.first_name,
                        last_name=TEST_USER.last_name)


def get_message(text:str):
    return Message(chat=TEST_USER_CHAT, message_id=2, text=text, from_user=TEST_USER, date=datetime.datetime.now(), sender_chat=TEST_USER_CHAT )
    
def get_callback(data: str):
    message = get_message(text=None)
    return CallbackQuery(id='123', from_user=TEST_USER, chat_instance='non', message=message, data=data)

def get_update(message=None, callback=None):
    return Update(update_id=123, message=message, callback=callback)