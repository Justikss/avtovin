import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.callback_handlers.sell_part.checkout_seller_person_profile import seller_profile_card_constructor
from utils.lexicon_utils.Lexicon import ADMIN_LEXICON

async def person_output_modification(profile_card, seller_entity):
    seller_profile_card_lexicon_part = ADMIN_LEXICON['review_seller_card']['message_header']

    profile_card = profile_card.split('\n')[1:]
    profile_card[0] = f'{seller_profile_card_lexicon_part}'
    profile_card[1], profile_card[-1] = f'<blockquote>{profile_card[1]}', f'{profile_card[-1]}</blockquote>'
    profile_card = '\n'.join(profile_card)

    return profile_card


async def output_specific_user_profile_handler(callback: CallbackQuery, state: FSMContext):
    message_editor_module = importlib.import_module('handlers.message_editor')

    seller_id = callback.data.split(':')[-1]
    if seller_id[-1].isalpha():
        memory_storage = await state.get_data()
        seller_id = memory_storage.get('current_seller_id')
    else:
        await state.update_data(current_seller_id=seller_id)

    seller_data = await seller_profile_card_constructor(user_id=seller_id, get_part='top')

    if seller_data:
        profile_card, seller_entity = seller_data

        message_text = await person_output_modification(profile_card, seller_entity)
        lexcion_part = {'message_text': message_text, 'buttons': {**ADMIN_LEXICON['review_seller_card']['buttons']}}
        await message_editor_module.travel_editor.edit_message(request=callback, lexicon_key='',
                                                               lexicon_part=lexcion_part, dynamic_buttons=2)
    else:

        return await callback.answer(ADMIN_LEXICON['user_non_active'])



