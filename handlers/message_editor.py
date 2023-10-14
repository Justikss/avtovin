
from aiogram.types import Message, chat, CallbackQuery

from handlers.callback_handlers.language_callback_handler import InlineCreator, redis_data
from utils.Lexicon import LEXICON


class TravelEditor:
    @staticmethod
    async def edit_message(lexicon_key: str, request):
        lexicon_part = LEXICON[lexicon_key]
        redis_key = str(request.from_user.id) + ':last_message'
        last_message_id = await redis_data.get_data(redis_key)

        if isinstance(request, CallbackQuery):
            message_object = request.message
        else:
            message_object = request

        chat_object = message_object.chat

        keyboard = await InlineCreator.create_markup(lexicon_part)
        message_text = lexicon_part['message_text']
        await chat.Chat.delete_message(self=chat_object, message_id=last_message_id)
        new_message = await message_object.answer(text=message_text, reply_markup=keyboard)

        await redis_data.set_data(redis_key, new_message.message_id)


travel_editor = TravelEditor()