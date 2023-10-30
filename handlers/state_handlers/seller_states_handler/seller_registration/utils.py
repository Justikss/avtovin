import importlib
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from typing import Union

from database.data_requests.person_requests import PersonRequester

async def load_seller_in_database(request: Union[CallbackQuery, Message], state: FSMContext, authorized_state: bool):
    '''Метод подготовки аргументов(данных продавца) к загрузке в базу данных'''

    redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт
    seller_mode = await redis_module.redis_data.get_data(key=str(request.from_user.id) + ':seller_registration_mode')
    memory_storage = await state.get_data()
    formatted_load_pattern = dict()
    user_id = request.from_user.id
    phonenumber = memory_storage['seller_number']
    fullname = memory_storage['seller_name']
    print('number:', phonenumber, '\nname: ', fullname)
    print('seller_mode: ', seller_mode)

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
            'authorized': authorized_state
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
            'authorized': authorized_state
        }
    print(formatted_load_pattern)
    try_load = PersonRequester.store_data(formatted_load_pattern, seller=True)
    if try_load:
        return True
    else:
        return False