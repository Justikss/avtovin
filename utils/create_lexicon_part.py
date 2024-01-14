from database.tables.offers_history import SellerFeedbacksHistory
from database.tables.seller import Seller
from database.tables.user import User
from handlers.state_handlers.seller_states_handler.load_new_car.boot_car_buttons_controller import \
    RedisBootCommodityHelper

async def add_lively_buttons(lexicon_part, buttons_captions, buttons_callback_data):
    ic(buttons_captions, lexicon_part)
    for button_part in buttons_captions:
        if isinstance(button_part, User) or isinstance(button_part, Seller) and not button_part.dealship_name:
            name = f'''{button_part.surname} {button_part.name} {button_part.patronymic if button_part.patronymic else ''}'''
            object_id = button_part.telegram_id
        elif isinstance(button_part, Seller) and button_part.dealship_name:
            name = button_part.dealship_name
            object_id = button_part.telegram_id
        else:
            name = button_part.name
            object_id = button_part.id

        lexicon_part['buttons'][f'{str(buttons_callback_data)}{object_id}'] = name
    ic(lexicon_part)
    return lexicon_part

async def create_lexicon_part(lexicon_part_abc, buttons_captions, request=None, state=None, need_width=False,
                              need_last_buttons=True):
    ic(lexicon_part_abc.__class__.__dict__)
    ic(lexicon_part_abc.__dict__)

    ic(lexicon_part_abc, buttons_captions)
    message_text = lexicon_part_abc.message_text
    buttons_callback_data = lexicon_part_abc.buttons_callback_data
    buttons_width = lexicon_part_abc.width
    ic(lexicon_part_abc.__class__.__name__, lexicon_part_abc.__class__.__name__.startswith('load_commodity'), isinstance(lexicon_part_abc, RedisBootCommodityHelper))
    if isinstance(lexicon_part_abc, RedisBootCommodityHelper) and lexicon_part_abc.__class__.__name__.startswith('load_commodity'):
        ic()
        ic(state)
        ic(hasattr(lexicon_part_abc, 'initializate'))
        if hasattr(lexicon_part_abc, 'initializate'):
            ic(lexicon_part_abc.__dict__)
            await lexicon_part_abc.initializate(request, state)
            ic(lexicon_part_abc.__dict__)
        ic(lexicon_part_abc.last_buttons)
    lexicon_part = {'message_text': message_text}
    lexicon_part['buttons'] = {}
    if buttons_captions:
        lexicon_part = await add_lively_buttons(lexicon_part, buttons_captions, buttons_callback_data)
    if lexicon_part_abc.__dict__.get('last_buttons'):
        if need_last_buttons == True:
            ic(need_last_buttons)
            iterable = lexicon_part_abc.last_buttons.items()
        elif need_last_buttons != False:
            iterable = need_last_buttons.items()
        else:
            iterable = None
        ic(iterable)
        if iterable:
            for callback_data, caption in iterable:
                lexicon_part['buttons'][callback_data] = caption
    if need_width:
        lexicon_part['buttons']['width'] = buttons_width
    ic(lexicon_part)
    ic(lexicon_part_abc.__dict__.get('last_buttons'))
    return lexicon_part

