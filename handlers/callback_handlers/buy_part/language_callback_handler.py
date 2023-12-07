import importlib
from aiogram.exceptions import TelegramBadRequest

from aiogram.types import CallbackQuery
from utils.Lexicon import LEXICON
from keyboards.inline.kb_creator import InlineCreator
from utils.redis_for_language import redis_data


async def set_language(callback: CallbackQuery, delete_mode=False, set_languange=True):
    travel_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    user_id = callback.from_user.id
    if set_languange:
        redis_key = str(user_id) + ':language'
        redis_value = callback.data.split('_')
        if len(redis_value) >= 1:
            if redis_value[0] == 'language':
                redis_value = redis_value[1]
                await redis_data.set_data(key=redis_key, value=redis_value)

    #Будет меняться язык от callback.data#
    lexicon_code = 'hello_text'
    lexicon_part = LEXICON[lexicon_code]
    message_text = lexicon_part['message_text'].replace('X', callback.from_user.username)
    keyboard = await InlineCreator.create_markup(lexicon_part)

    user_id = str(callback.from_user.id)
    redis_key_last_lexicon = user_id + ':last_lexicon_code'
    await redis_data.set_data(redis_key_last_lexicon, lexicon_code)
    
    if delete_mode:
        last_message_id = await redis_data.get_data(key=user_id + ':last_message')
        # await redis_data.delete_key(key=user_id + ':last_message')
        await callback.bot.delete_message(chat_id=callback.message.chat.id, message_id=last_message_id)
        message_object = await callback.message.answer(text=message_text, reply_markup=keyboard)
    else:
        try:
            message_object = await callback.message.edit_text(text=message_text, reply_markup=keyboard)
        except TelegramBadRequest:
            message_object = await callback.message.answer(text=message_text, reply_markup=keyboard)
    
    await redis_data.set_data(user_id + ':last_message', message_object.message_id)





    await callback.answer()