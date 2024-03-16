import logging

from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
import time
import importlib
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from handlers.state_handlers.seller_states_handler.seller_registration import utils


async def output_for_admin_formater(callback: CallbackQuery):
    '''Форматировщик текста сообщения в Админский чат о регистрации нового продавца'''
    redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт
    person_requester_module = importlib.import_module('database.data_requests.person_requests')
    lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

    await redis_module.redis_data.set_data(key=str(callback.from_user.id) + ':chat_id', value=callback.message.chat.id)
    new_seller = await person_requester_module.PersonRequester.get_user_for_id(user_id=callback.from_user.id, seller=True)
    if new_seller:
        new_seller = new_seller[0]
        ic(new_seller.phone_number)
        lexicon_part = lexicon_module.__LEXICON['seller_waiting_registration_confirm']
        user_link = '@' + callback.from_user.username
        # head_string = lexicon_part['start_text_' + new_seller.entity] + f'''\n{user_link}\n{lexicon_part['phone_number']}\n{new_seller.phone_number}'''
        if new_seller.entity == 'legal':
            # body_string = f'''\n\n{lexicon_middle_part['name']}\n{new_seller.dealship_name}\n\n{lexicon_middle_part['address']}\n{new_seller.dealship_address}'''
            head_string = f'''{lexicon_part['start_text_legal'].format(username=user_link, address=new_seller.dealship_address)}{lexicon_part['legal_body_header'].format(dealership_name=new_seller.dealship_name)}'''
        elif new_seller.entity == 'natural':
            ic(new_seller.name,new_seller.patronymic)
            head_string = f'''{lexicon_part['start_text_natural'].format(username=user_link)}{lexicon_part['natural_body_header'].format(name=new_seller.name, surname=new_seller.surname, patronymic=str(new_seller.patronymic))}'''
            head_string = '\n'.join([part for part in head_string.split('\n') if 'None' not in part])
        else:
            logging.error('Не удалось определить entity продавца: %s', new_seller.entity)
        head_string += f'''{lexicon_part['body'].format(phone_number=new_seller.phone_number)}'''


            # body_string = f'''\n\n{lexicon_middle_part['name'] + new_seller.name}\n{lexicon_middle_part['surname'] + new_seller.surname + patronymic_string}'''

        # result_string = head_string + body_string
        ic(head_string)
        return head_string


async def send_message_to_admins(callback: CallbackQuery):
    '''Метод отправки оповещения о регистрации нового продавца в чат Админов.'''
    lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
    config_module = importlib.import_module('config_data.config')
    lexicon_part = lexicon_module.LEXICON['confirm_new_seller_registration_from_admin_button']

    '''клавиатура одобрения регистрации в архиве'''
    # keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
    # text=lexicon_part['confirm_from_admin'],
    # callback_data= lexicon_part['callback_startswith'] + str(callback.from_user.id))]])

    output_text = await output_for_admin_formater(callback=callback)

    message_for_admins = await callback.message.bot.send_message(chat_id=config_module.ADMIN_SELLERS_CHAT, text=output_text)

    await utils.update_non_confirm_seller_registrations(callback=callback, message_for_admins=message_for_admins.message_id)


async def seller_confirm_registration(callback: CallbackQuery, state: FSMContext):
    '''Обработчик подтверждённой(продавцом) регистрации.'''
    redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт
    message_editor_module = importlib.import_module('handlers.message_editor')



    load_try = await utils.load_seller_in_database(authorized_state=True, state=state, request=callback)
    if load_try:
        seller_main_menu_module = importlib.import_module('handlers.callback_handlers.sell_part.seller_main_menu')
        lexicon_code = 'confirm_seller_profile_notification'
        await send_message_to_admins(callback=callback)
        await seller_main_menu_module.seller_main_menu(callback, state=state)

    else:
        lexicon_code = 'try_again_seller_registration'
        await message_editor_module.travel_editor.edit_message(request=callback, lexicon_key=lexicon_code)

    
    #time.sleep(1)
    await state.clear()

    await redis_module.redis_data.delete_key(key=str(callback.from_user.id) + ':seller_registration_mode')
    await redis_module.redis_data.delete_key(key=str(callback.from_user.id) + ':can_edit_seller_registration_data')
