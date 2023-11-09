import importlib

from aiogram.types import CallbackQuery

from keyboards.inline.kb_creator import InlineCreator
from utils.Lexicon import LEXICON


async def try_delete_notification(callback: CallbackQuery, user_status: str=None):
    redis_module = importlib.import_module('utils.redis_for_language')  # Ленивый импорт

    callback_data = callback.data
    if ':' in callback_data:
        user_status = callback_data.split(':')[1]

    if user_status == 'seller':
        redis_sub_key = 'seller_registration_notification'
    elif user_status == 'buyer':
        redis_sub_key = 'buyer_offer_notification'

    notification_message_id = await redis_module.redis_data.get_data(key=str(callback.from_user.id) + redis_sub_key)
    if notification_message_id:
        try:
            await callback.bot.delete_message(chat_id=callback.message.chat.id, message_id=notification_message_id)
            await redis_module.redis_data.delete_key(key=str(callback.from_user.id) + redis_sub_key)
        except:
            pass

async def send_notification(callback: CallbackQuery, user_status: str, chat_id=None):
    redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт

    if user_status == 'seller':
        redis_sub_key = 'seller_registration_notification'
        lexicon_key = 'confirm_seller_profile_notification'
    elif user_status == 'buyer':
        redis_sub_key = 'buyer_offer_notification'
        lexicon_key = 'buyer_offer_notification'

    notification_message_id = await redis_module.redis_data.get_data(key=str(callback.from_user.id) + redis_sub_key)
    if notification_message_id:
        #return
        pass


    await callback.answer(LEXICON['success_notification'])
    if not chat_id:
        chat_id = await redis_module.redis_data.get_data(key=str(callback.from_user.id) + ':chat_id')
    lexicon_part = LEXICON[lexicon_key]
    keyboard = await InlineCreator.create_markup(input_data=lexicon_part)
    notification_message = await callback.message.bot.send_message(chat_id=chat_id, text=lexicon_part['message_text'],
                                            reply_markup=keyboard)

    await redis_module.redis_data.set_data(key=str(callback.from_user.id) + redis_sub_key,
                                            value=notification_message.message_id)

