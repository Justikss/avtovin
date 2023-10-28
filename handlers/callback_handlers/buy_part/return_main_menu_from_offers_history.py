import importlib

from aiogram.types import CallbackQuery
from utils.Lexicon import LEXICON


async def return_from_offers_history(callback: CallbackQuery):
    redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт
    inline_creator = importlib.import_module('keyboards.inline.kb_creator')  # Ленивый импорт

    first_last_message_key = str(callback.from_user.id) + ':history_requests_pagination' + ':first'
    second_last_message_key = str(callback.from_user.id) + ':history_requests_pagination' + ':second'
    head_last_message_key = str(callback.from_user.id) + ':history_requests_pagination' + ':head'

    first_last_message_id = int(await redis_module.redis_data.get_data(key=first_last_message_key))
    second_last_message_id = int(await redis_module.redis_data.get_data(key=second_last_message_key))
    head_last_message_id = int(await redis_module.redis_data.get_data(key=head_last_message_key))

    if first_last_message_id > 0:
        await callback.message.bot.delete_message(chat_id=callback.message.chat.id,
                                                  message_id=int(first_last_message_id))
    if second_last_message_id > 0:
        await callback.message.bot.delete_message(chat_id=callback.message.chat.id,
                                                  message_id=int(second_last_message_id))

    message_part = LEXICON['main_menu']
    keyboard = await inline_creator.InlineCreator.create_markup(input_data=message_part)
    message_object = await callback.message.bot.edit_message_text(chat_id=callback.message.chat.id,
                                                                 message_id=head_last_message_id,
                                                                 text=message_part['message_text'],
                                                                 reply_markup=keyboard)

    await redis_module.redis_data.set_data(key=str(callback.from_user.id) + ':last_message',
                              value=message_object.message_id)
