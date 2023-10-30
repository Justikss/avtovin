import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from utils.Lexicon import LEXICON
from handlers.message_editor import InlineCreator
from handlers.callback_handlers.buy_part.language_callback_handler import redis_data


async def bot_start(message: Message, state: FSMContext):
    travel_editor = importlib.import_module('handlers.message_editor')
    redis_module = importlib.import_module('utils.redis_for_language')

    await state.clear()
    await message.delete()

    last_user_message = await redis_module.redis_data.get_data(key=str(message.from_user.id) + ':last_user_message')
    if last_user_message:
        try:
            await message.chat.delete_message(message_id=last_user_message)
        except:
            await redis_module.redis_data.delete_key(key=str(message.from_user.id) + ':last_user_message')

        await redis_module.redis_data.delete_key(key=str(message.from_user.id) + ':last_user_message')

    # user_id = message.from_user.id
    # redis_key = str(user_id) + ':last_message'
    #

    await travel_editor.travel_editor.edit_message(lexicon_key='choose_language', request=message)
    await redis_module.redis_data.delete_key(key=str(message.from_user.id) + ':can_edit_seller_registration_data')

    # lexicon_part = LEXICON['choose_language']
    # message_text = lexicon_part['message_text']
    # keyboard = await InlineCreator.create_markup(lexicon_part)
    #
    # message_object = await message.answer(text=message_text, reply_markup=keyboard)
    # await redis_data.set_data(str(message.from_user.id) + ':last_message', message_object.message_id)

