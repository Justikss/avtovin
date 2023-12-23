import importlib
import logging

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from typing import Union


async def seller_are_registrated_notification(callback: CallbackQuery):
    '''Метод уведомляющий продавца о подтверждении его регистрации'''

    message_editor_module = importlib.import_module('handlers.message_editor')

    await message_editor_module.travel_editor.edit_message(request=callback, lexicon_key='success_seller_registration_notice')

    
async def update_non_confirm_seller_registrations(callback: CallbackQuery, message_for_admins=None, get_by_seller_id=None):
    '''Метод обновляет стэк ожидающих одобрение продавцов
    :message_for_admins: Отправить оповещение о попытке регистрации администрации.
    :get_by_seller_id: Получить пару со стэка( в случае одобрения или отказа регистрации )'''

    redis_module = importlib.import_module('utils.redis_for_language')

    redis_key = 'active_non_confirm_seller_registrations'
    seller_registration_stack = await redis_module.redis_data.get_data(key=redis_key, use_json=True)
    print('seller_reg_stack', seller_registration_stack)

    if message_for_admins:
        value = str(callback.from_user.id) + ':' + str(callback.message.chat.id)
        if seller_registration_stack:
            seller_registration_stack[message_for_admins] = value
        else:
            seller_registration_stack = {message_for_admins: value}

        await redis_module.redis_data.set_data(key=redis_key, value=seller_registration_stack)

    elif get_by_seller_id:

        if not seller_registration_stack:
            return False
        else:
            for key, value in seller_registration_stack.items():
                value = value.split(':')
                user_id = value[0]
                user_chat_id = value[1]
                if str(user_id) == get_by_seller_id:
                    exists_user_notification_data = {'notification_id': key, 'user_id': user_id, 'user_chat_id': user_chat_id}
                    current_data_pair = seller_registration_stack.pop(key)
                    await redis_module.redis_data.set_data(key=redis_key, value=seller_registration_stack)
                    return exists_user_notification_data

async def load_seller_in_database(request: Union[CallbackQuery, Message], state: FSMContext, authorized_state: bool):
    '''Метод подготовки аргументов(данных продавца) к загрузке в базу данных'''
    person_requester_module = importlib.import_module('database.data_requests.person_requests')

    redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт
    seller_mode = await redis_module.redis_data.get_data(key=str(request.from_user.id) + ':seller_registration_mode')
    memory_storage = await state.get_data()
    formatted_load_pattern = dict()
    user_id = request.from_user.id
    phonenumber = memory_storage['seller_number']
    fullname = memory_storage['seller_name']
    print('number:', phonenumber, '\nname: ', fullname)
    print('seller_mode: ', seller_mode)
    if isinstance(request, CallbackQuery):
        message = request.message
    else:
        message = request

    if seller_mode == 'dealership':
        address = memory_storage['dealership_address']
        formatted_load_pattern = {
            'telegram_id': user_id,
            'phone_number': phonenumber,
            'dealship_name': fullname,
            'entity': 'legal',
            'dealship_address': address,
            'name': None,
            'surname': None,
            'patronymic': None,
            'authorized': authorized_state,

        }
    elif seller_mode == 'person':
        person_full_name = fullname.split(' ')
        
        if len(person_full_name) == 3:
            patronymic = person_full_name[2]
        elif len(person_full_name) == 2:
            patronymic = None
        name = person_full_name[1]
        surname = person_full_name[0]

        formatted_load_pattern = {
            'telegram_id': user_id,
            'phone_number': phonenumber,
            'dealship_name': None,
            'entity': 'natural',
            'dealship_address': None,
            'name': name,
            'surname': surname,
            'patronymic': patronymic,
            'authorized': authorized_state,

        }
    print(formatted_load_pattern)
    try_load = await person_requester_module.PersonRequester.store_data(formatted_load_pattern, seller=True)
    if not (isinstance(try_load, tuple) and len(try_load) == 2):
        return True
    else:
        logging.error(f'Продавцу на удалось зарегестрироваться с такими данными в методе "load_seller_in_database": {load_seller_in_database}\nС ошибкой:\b{try_load[1]}')
        return False