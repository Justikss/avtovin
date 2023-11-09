import importlib

from aiogram.types import CallbackQuery

from handlers.state_handlers.seller_states_handler.seller_registration.await_confirm_from_admin import utils
from database.data_requests.person_requests import PersonRequester
from keyboards.inline.kb_creator import InlineCreator
from utils.Lexicon import LEXICON
from handlers.callback_handlers.buy_part.confirm_from_seller_callback_handler import send_notification


async def accept_registraiton(callback: CallbackQuery):
    '''Метод обрабатывает кнопку принятия заявки на регистрацию продавца.'''

    seller_id = callback.data.split(':')[1]
    print('seller_confirmed', seller_id)
    triple_data = await utils.update_non_confirm_seller_registrations(callback=callback, get_by_seller_id=seller_id)
    print('triple data', triple_data)
    if triple_data:
        notification_id, user_id, user_chat_id = triple_data['notification_id'], triple_data['user_id'], triple_data['user_chat_id']
    else:
        print(triple_data)
        await callback.answer(LEXICON['unexpected_behavior'])
        return

    print('notif: ', notification_id, 'usid: ', user_id)

    change_query = await PersonRequester.change_authorized_state(telegram_id=user_id, boolean=True)
    print('change_query: ', change_query, ':', type(change_query))
    if change_query:
        await send_notification(callback=callback, user_status='seller', chat_id=user_chat_id)
        await callback.bot.delete_message(chat_id=callback.message.chat.id, message_id=notification_id)
        await callback.answer()
    elif change_query is False:
        await callback.answer(LEXICON['too_late'])
    elif not change_query:
        await callback.answer(LEXICON['unexpected_behavior']) 


    # print('chid, ', chat_id, notification_id)
