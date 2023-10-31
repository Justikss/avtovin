from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
import time
import importlib
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from handlers.state_handlers.seller_states_handler.seller_registration import utils
from config_data.config import ADMIN_CHAT
from utils.Lexicon import LEXICON
from database.data_requests.person_requests import PersonRequester

async def output_for_admin_formater(callback: CallbackQuery):
    '''Форматировщик текста сообщения в Админский чат о регистрации нового продавца'''
    new_seller = PersonRequester.get_user_for_id(user_id=callback.from_user.id, seller=True)
    if new_seller:
        new_seller = new_seller[0]
        if not new_seller.authorized:
            lexicon_part = LEXICON['seller_waiting_registration_confirm']
            lexicon_middle_part = lexicon_part[new_seller.entity + '_message']
            user_link = '@' + callback.from_user.username
            head_string = lexicon_part['start_text_' + new_seller.entity] + f'''\n{user_link}\n{lexicon_part['phone_number'] + new_seller.phone_number}'''
            if new_seller.entity == 'legal':
                body_string = f'''\n{lexicon_middle_part['name'] + new_seller.dealship_name}\n{lexicon_middle_part['address'] + new_seller.dealship_address}'''

            elif new_seller.entity == 'natural':
                patronymic = new_seller.patronymic
                if patronymic:
                    patronymic_string = f'''\n{lexicon_middle_part['patronymic'] + new_seller.patronymic}'''
                else:
                    patronymic_string = ' '

                body_string = f'''\n{lexicon_middle_part['name'] + new_seller.name}\n{lexicon_middle_part['surname'] + new_seller.surname + patronymic_string}'''

            result_string = head_string + body_string
            return result_string
        else:
            await utils.seller_are_registrated_notification(callback=callback)


async def send_message_to_admins(callback: CallbackQuery):
    '''Метод отправки оповещения о регистрации нового продавца в чат Админов.'''
    lexicon_part = LEXICON['confirm_new_seller_registration_from_admin_button']

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
    text=lexicon_part['confirm_from_admin'],
    callback_data= lexicon_part['callback_startswith'] + str(callback.from_user.id))]])

    output_text = await output_for_admin_formater(callback=callback)

    message_for_admins = await callback.message.bot.send_message(chat_id=ADMIN_CHAT, text=output_text, reply_markup=keyboard)

    await utils.update_non_confirm_seller_registrations(callback=callback, message_for_admins_id=message_for_admins.message_id)


async def seller_await_confirm_by_admin(callback: CallbackQuery, state: FSMContext):
    '''Обработчик подтверждённой(продавцом) регистрации.'''
    redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт
    message_editor_module = importlib.import_module('handlers.message_editor')


    load_try = await utils.load_seller_in_database(authorized_state=False, state=state, request=callback)
    if load_try:
        lexicon_code = 'confirm_registration_from_seller'
        await send_message_to_admins(callback=callback)

    else:
        lexicon_code = 'try_again_seller_registration'

    
    await message_editor_module.travel_editor.edit_message(request=callback, lexicon_key=lexicon_code)
    #time.sleep(1)
    await state.clear()

    await redis_module.redis_data.delete_key(key=str(callback.from_user.id) + ':seller_registration_mode')
    await redis_module.redis_data.delete_key(key=str(callback.from_user.id) + ':can_edit_seller_registration_data')
