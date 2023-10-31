from aiogram.types import CallbackQuery

from handlers.state_handlers.seller_states_handler.seller_registration.await_confirm_from_admin import utils
from database.data_requests.person_requests import PersonRequester
from utils.Lexicon import LEXICON


async def accept_registraiton(callback: CallbackQuery):
    '''Метод обрабатывает кнопку принятия заявки на регистрацию продавца.'''
    seller_id = callback.data.split(':')[1]
    print('seller_confirmed', seller_id)
    data_pair = await utils.update_non_confirm_seller_registrations(callback=callback, get_by_seller_id=seller_id)
    if data_pair:
        notification_id, user_id = data_pair[0], data_pair[1]
    else:
        print(data_pair)
        await callback.answer(LEXICON['unexpected_behavior']) 

    print('notif: ', notification_id, 'usid: ', user_id)

    change_query = await PersonRequester.change_authorized_state(telegram_id=user_id, boolean=True)
    if change_query:
        await callback.answer(LEXICON['success_notification'])
    elif change_query is False:
        await callback.answer(LEXICON['too_late'])
    elif not change_query:
        await callback.answer(LEXICON['unexpected_behavior']) 

    chat_id = callback.message.chat.id
    print('chid, ', chat_id, notification_id)
    await callback.bot.delete_message(chat_id=chat_id, message_id=notification_id)
