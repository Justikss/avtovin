import importlib

from database.tables.seller import Seller
from database.tables.user import User


async def handle_banned_person_card(lexicon_part, user_model: Seller | User):
    Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

    banned_lexicon_part = Lexicon_module.ADMIN_LEXICON['banned_user_endswith']
    if not user_model.is_banned:
        return lexicon_part

    block_datetime = str(user_model.block_date).split()
    block_time = block_datetime[1]
    block_date = block_datetime[0]

    block_reason = user_model.ban_reason

    lexicon_part['message_text'] += banned_lexicon_part['message_text'].format(date=block_date, time=block_time,
                                                                               reason=block_reason)

    del lexicon_part['buttons']['user_block_action_by_admin']
    if 'tariff_actions_by_admin' in lexicon_part['buttons'].keys():
        del lexicon_part['buttons']['tariff_actions_by_admin']
        lexicon_part['buttons']['width'] = 1
    lexicon_part['buttons'] = {**banned_lexicon_part['buttons'], **lexicon_part['buttons']}

    ic(lexicon_part)
    ic()
    return lexicon_part
