from database.data_requests.person_requests import PersonRequester
from database.tables.seller import Seller
from database.tables.user import User
from handlers.callback_handlers.sell_part.checkout_seller_person_profile import get_seller_name
from handlers.utils.one_len_list_in_object import one_element_in_object


async def get_user_name(subject):
    seller_model = None
    buyer_model = None
    if isinstance(subject, User):
        buyer_model = subject
    elif isinstance(subject, Seller):
        seller_model = subject

    if (isinstance(subject, str) and subject.startswith('seller')) or isinstance(subject, Seller):
        if not seller_model:
            seller_model = await PersonRequester.get_user_for_id(subject.split(':')[-1], seller=True)
        if seller_model:
            seller_model = await one_element_in_object(seller_model)
            name = await get_seller_name(seller_model)

    elif (isinstance(subject, str) and subject.startswith('buyer')) or isinstance(subject, User):
        ic()

        ic(subject)
        if not buyer_model:
            buyer_model = await PersonRequester.get_user_for_id(subject.split(':')[-1], user=True)
        ic(buyer_model)
        if buyer_model:
            buyer_model = await one_element_in_object(buyer_model)
            name = f'''{buyer_model.surname} {buyer_model.name} {buyer_model.patronymic if buyer_model.patronymic else ''}'''
    else:
        return False

    return name