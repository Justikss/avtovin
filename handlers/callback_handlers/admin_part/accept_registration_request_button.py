import importlib

from aiogram.types import CallbackQuery

from handlers.state_handlers.seller_states_handler.seller_registration.await_confirm_from_admin import utils
from utils.user_notification import send_notification

Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

async def accept_registraiton(callback: CallbackQuery):
    '''Метод обрабатывает кнопку принятия заявки на регистрацию продавца.'''
    person_requester_module = importlib.import_module('database.data_requests.person_requests')

    seller_id = callback.data.split(':')[1]

    triple_data = await utils.update_non_confirm_seller_registrations(callback=callback, get_by_seller_id=seller_id)

    if triple_data:
        notification_id, user_id, user_chat_id = triple_data['notification_id'], triple_data['user_id'], triple_data['user_chat_id']
    else:

        await callback.answer(Lexicon_module.LEXICON['unexpected_behavior'])
        return



    change_query = await person_requester_module.PersonRequester.change_authorized_state(telegram_id=user_id, boolean=True)

    if change_query:
        await send_notification(callback=callback, user_status='seller', chat_id=user_chat_id)
        await callback.bot.delete_message(chat_id=callback.message.chat.id, message_id=notification_id)
        await callback.answer()
    elif change_query is False:
        await callback.answer(Lexicon_module.LEXICON['too_late'])
    elif not change_query:
        await callback.answer(Lexicon_module.LEXICON['unexpected_behavior'])


    #
