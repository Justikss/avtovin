import importlib
from aiogram.exceptions import TelegramBadRequest

from aiogram.types import CallbackQuery

from database.data_requests.admin_requests import AdminManager
from keyboards.inline.kb_creator import InlineCreator
from utils.lexicon_utils.Lexicon import ADMIN_LEXICON
from utils.redis_for_language import redis_data

async def unpack_lexicon_to_start_using(callback, string_user_id):
    lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

    lexicon_code = 'hello_text'
    lexicon_part = lexicon_module.LEXICON[lexicon_code]
    if await AdminManager.admin_authentication(callback.from_user.id):
        admin_lexicon_part = {}
        for callback_value, button_caption in lexicon_part.items():
            if callback_value == 'width':
                admin_lexicon_part['admin_panel_button'] = ADMIN_LEXICON['admin_panel_button_caption']
            admin_lexicon_part[callback_value] = button_caption
        if admin_lexicon_part:
            lexicon_part = admin_lexicon_part
    message_text = lexicon_part['message_text'].replace('X', callback.from_user.username)
    ic(lexicon_part)
    keyboard = await InlineCreator.create_markup(lexicon_part)

    redis_key_last_lexicon = string_user_id + ':last_lexicon_code'
    await redis_data.set_data(redis_key_last_lexicon, lexicon_code)

    return keyboard, message_text

async def set_language(callback: CallbackQuery, delete_mode=False, set_languange=True):
    # travel_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    # lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

    string_user_id = str(callback.from_user.id)
    if set_languange:
        redis_key = str(string_user_id) + ':language'
        redis_value = callback.data.split('_')
        if len(redis_value) >= 1:
            if redis_value[0] == 'language':
                redis_value = redis_value[1]
                await redis_data.set_data(key=redis_key, value=redis_value)

    #Будет меняться язык от callback.data#

    keyboard, message_text = await unpack_lexicon_to_start_using(callback, string_user_id)
    ic(message_text, keyboard)
    
    if delete_mode:
        last_message_id = await redis_data.get_data(key=string_user_id + ':last_message')
        # await redis_data.delete_key(key=user_id + ':last_message')
        await callback.bot.delete_message(chat_id=callback.message.chat.id, message_id=last_message_id)
        message_object = await callback.message.answer(text=message_text, reply_markup=keyboard)
    else:
        try:
            message_object = await callback.message.edit_text(text=message_text, reply_markup=keyboard)
        except TelegramBadRequest:
            message_object = await callback.message.answer(text=message_text, reply_markup=keyboard)
    
    await redis_data.set_data(string_user_id + ':last_message', message_object.message_id)





    await callback.answer()