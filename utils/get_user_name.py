from database.tables.seller import Seller


async def get_user_name(model):
    entity = None
    name = None
    if isinstance(model, list) and len(model) == 1:
        model = model[0]
    if isinstance(model, Seller):
        if model.dealship_name:
            entity = 'dealership'
            name = model.dealship_name
            return name, entity
        else:
            entity = 'seller'
    else:
        entity = 'buyer'

    if entity:
        name = f'''{model.surname} {model.name} {model.patronymic if model.patronymic else ''}'''
        return name, entity