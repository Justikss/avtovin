from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from utils.Lexicon import LEXICON
from keyboards.inline.kb_creator import InlineCreator
from handlers.callback_handlers.language_callback_handler import redis_data


async def bot_start(message: Message, state: FSMContext):
    await state.clear()
    lexicon_part = LEXICON['choose_language']
    message_text = lexicon_part['message_text']
    keyboard = await InlineCreator.create_markup(lexicon_part)

    message_object = await message.answer(text=message_text, reply_markup=keyboard)
    await redis_data.set_data(str(message.from_user.id) + ':last_message', message_object.message_id)

