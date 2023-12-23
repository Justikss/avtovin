import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from handlers.callback_handlers.sell_part.checkout_seller_person_profile import seller_profile_card_constructor
from utils.lexicon_utils.Lexicon import ADMIN_LEXICON

async def person_output_modification(profile_card, seller_entity):
    seller_profile_card_lexicon_part = ADMIN_LEXICON['review_seller_card']['message_header']

    profile_card = profile_card.split('\n')[1:]
    profile_card[0] = f'{seller_profile_card_lexicon_part}'
    profile_card[1], profile_card[-1] = f'<blockquote>{profile_card[1]}', f'{profile_card[-1]}</blockquote>'
    profile_card = '\n'.join(profile_card)

    return profile_card


async def output_specific_seller_profile_handler(request: CallbackQuery | Message, state: FSMContext, seller_id=None):
    message_editor_module = importlib.import_module('handlers.message_editor')
    choose_specific_person_by_admin_module = importlib.import_module('handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_specific.choose_specific_person')

    memory_storage = await state.get_data()

    if not seller_id:
        if isinstance(request, CallbackQuery):
            if request.data[-1].isdigit():
                seller_id = request.data.split(':')[-1]
        if not seller_id:
            seller_id = memory_storage.get('current_seller_id')
    if seller_id[-1].isalpha():
        seller_id = memory_storage.get('current_seller_id')
    else:
        await state.update_data(current_seller_id=seller_id)

    seller_data = await seller_profile_card_constructor(user_id=seller_id, get_part='top')

    if seller_data:
        profile_card, seller_entity = seller_data

        message_text = await person_output_modification(profile_card, seller_entity)
        lexcion_part = {'message_text': message_text, 'buttons': {**ADMIN_LEXICON['review_seller_card']['buttons']}}
        await message_editor_module.travel_editor.edit_message(request=request, lexicon_key='',
                                                               lexicon_part=lexcion_part, dynamic_buttons=2,
                                                               delete_mode=True)
    else:
        if isinstance(request, CallbackQuery):
            await request.answer(ADMIN_LEXICON['user_non_active'])
        return await choose_specific_person_by_admin_module.choose_specific_person_by_admin_handler(request, state,
                                                                                                    first_call=False)



