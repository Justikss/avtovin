from aiogram.types import CallbackQuery
from utils.Lexicon import LEXICON
from keyboards.inline.kb_creator import InlineCreator
from utils.redis_for_language import redis_data


async def set_language(callback: CallbackQuery):
    user_id = callback.from_user.id
    redis_key = str(user_id) + ':language'
    redis_value = callback.data.split('_')[1]
    await redis_data.set_data(key=redis_key, value=redis_value)

    #Будет меняться язык от callback.data#
    lexicon_code = 'hello_text'
    lexicon_part = LEXICON[lexicon_code]
    message_text = lexicon_part['message_text']
    keyboard = await InlineCreator.create_markup(lexicon_part)

    await redis_data.set_data(str(user_id) + ':last_lexicon_code', lexicon_code)
    await callback.message.edit_text(text=message_text, reply_markup=keyboard)




    await callback.answer()