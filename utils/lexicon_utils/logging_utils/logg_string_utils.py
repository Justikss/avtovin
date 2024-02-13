import importlib

from icecream import ic

from database.tables.seller import Seller
from database.tables.tariff import Tariff
from database.tables.user import User
from handlers.callback_handlers.sell_part.checkout_seller_person_profile import get_seller_name
from handlers.utils.one_len_list_in_object import one_element_in_object
from utils.lexicon_utils.admin_lexicon.advert_parameters_lexicon import advert_parameters_captions

car_configurations_requests_module = importlib.import_module('database.data_requests.car_configurations_requests')
ic.enable()

async def get_user_name(subject):
    person_request_module = importlib.import_module('database.data_requests.person_requests')
    try:
        ic(len(subject))
    except:
        pass
    seller_model = None
    buyer_model = None
    tariff_model = None
    if isinstance(subject, User):
        buyer_model = subject
    elif isinstance(subject, Seller):
        seller_model = subject
    elif isinstance(subject, Tariff):
        tariff_model = subject

    if (isinstance(subject, str) and subject.startswith('seller')) or isinstance(subject, Seller):
        if not seller_model:
            seller_model = await person_request_module.PersonRequester.get_user_for_id(subject.split(':')[-1], seller=True)
        if seller_model:
            seller_model = await one_element_in_object(seller_model)
            name = await get_seller_name(seller_model, for_admin=True, logg_mode=True)

    elif (isinstance(subject, str) and subject.startswith('buyer')) or isinstance(subject, User):
        ic()

        ic(subject)
        if not buyer_model:
            buyer_model = await person_request_module.PersonRequester.get_user_for_id(subject.split(':')[-1], user=True)
        ic(buyer_model)
        if buyer_model:
            buyer_model = await one_element_in_object(buyer_model)
            name = f'''{buyer_model.surname} {buyer_model.name} {buyer_model.patronymic if buyer_model.patronymic else ''}'''
    elif (isinstance(subject, str) and subject.startswith('tariff')) or isinstance(subject, Tariff):
        tariff_requester_module = importlib.import_module('database.data_requests.tariff_requests')

        if not tariff_model:
            tariff_model = await tariff_requester_module.TarifRequester.get_by_id(subject.split(':')[-1])
            ic(tariff_model)
        if tariff_model:
            name = tariff_model.name
    elif isinstance(subject, dict):
        name = ''
        for key, value in subject.items():
            if isinstance(value, dict):
                if 'added' in value.keys():
                    value = value['added']
                else:
                    old_value = [param_name for param_name in value.keys()][0]
                    new_value = [param_name for param_name in value.values()][0]
                    value = f'С {old_value} на {new_value}'
            if isinstance(value, int):
                value = await car_configurations_requests_module.CarConfigs.get_by_id(key, value)

            value_name = value if isinstance(value, str) else value.name
            name += f"\n{advert_parameters_captions._data['ru'][key]}: {value_name}"

    elif isinstance(subject, tuple):
        param_subject = await get_user_name(subject[0])
        param_branch = await get_user_name(subject[1]) if subject[1] else ''
        return f'{param_branch}{param_subject}'
    else:
        return subject

    return name