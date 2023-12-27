import importlib

from database.tables.seller import Seller
from database.tables.tariff import Tariff
from database.tables.user import User
from handlers.callback_handlers.sell_part.checkout_seller_person_profile import get_seller_name
from handlers.utils.one_len_list_in_object import one_element_in_object


async def get_user_name(subject):
    person_request_module = importlib.import_module('database.data_requests.person_requests')

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
            name = await get_seller_name(seller_model)

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
        if tariff_model:
            name = tariff_model.name
    else:
        return subject

    return name