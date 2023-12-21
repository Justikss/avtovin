from database.data_requests.person_requests import PersonRequester
from handlers.callback_handlers.sell_part.checkout_seller_person_profile import get_seller_name


async def get_user_name(subject):
    if subject.startswith('seller'):
        seller_model = await PersonRequester.get_user_for_id(subject.split(':')[-1], seller=True)
        if seller_model:
            name = await get_seller_name(seller_model[0])
    elif subject.startswith('buyer'):
        buyer_model = await PersonRequester.get_user_for_id(subject.split(':')[-1], user=True)
        if buyer_model:
            buyer_model = buyer_model[0]
            name = f'''{buyer_model.surname} {buyer_model.name} {buyer_model.patronymic if buyer_model.patronymic else ''}'''
    else:
        return False

    return name