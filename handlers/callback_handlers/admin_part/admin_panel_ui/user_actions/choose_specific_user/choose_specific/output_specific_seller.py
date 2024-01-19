import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from handlers.callback_handlers.sell_part.checkout_seller_person_profile import seller_profile_card_constructor
from utils.lexicon_utils.admin_lexicon.admin_catalog_lexicon import pagination_interface

Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

async def person_output_modification(profile_card, seller_entity):
    seller_profile_card_lexicon_part = Lexicon_module.ADMIN_LEXICON['review_seller_card']['message_header']

    profile_card = profile_card.split('\n')[1:]
    profile_card[0] = f'{seller_profile_card_lexicon_part}'
    profile_card[1], profile_card[-1] = f'<blockquote>{profile_card[1]}', f'{profile_card[-1]}</blockquote>'
    profile_card = '\n'.join(profile_card)

    return profile_card


async def output_specific_seller_profile_handler(request: CallbackQuery | Message, state: FSMContext, seller_model=None,
                                                 pagination=None):
    message_editor_module = importlib.import_module('handlers.message_editor')
    choose_specific_person_by_admin_module = importlib.import_module('handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_specific.choose_specific_person')
    seller_id = None

    memory_storage = await state.get_data()
    if not seller_model:
        if isinstance(request, CallbackQuery):
            if request.data[-1].isdigit():
                seller_id = request.data.split(':')[-1]
        if not seller_id or seller_id[-1].isalpha():
            seller_id = memory_storage.get('current_seller_id')
        else:
            await state.update_data(current_seller_id=seller_id)
    elif isinstance(seller_model, list) and len(seller_model) > 1:
        admin_pagination_module = importlib.import_module('handlers.callback_handlers.admin_part.admin_panel_ui.utils.admin_pagination')
        await admin_pagination_module\
            .AdminPaginationOutput.set_pagination_data(request, state, [user.telegram_id for user in seller_model])
        return
    elif isinstance(seller_model, list):
        seller_model = seller_model[0]

    if not seller_id:
        seller_id = seller_model

    seller_data = await seller_profile_card_constructor(user_id=seller_id, get_part='top', for_admin=True)

    if seller_data:
        profile_card, seller_entity = seller_data
        message_text = await person_output_modification(profile_card, seller_entity)
        lexicon_part = {'message_text': message_text, 'buttons': {**Lexicon_module.ADMIN_LEXICON['review_seller_card']['buttons']}}

        if pagination:
            lexicon_part['buttons'] = {**pagination_interface, **lexicon_part['buttons']}
            lexicon_part['buttons']['width'] = (3, 1, 1, 1)
            lexicon_part['buttons']['page_counter'] = lexicon_part['buttons']['page_counter'].format(
                start=pagination.current_page,
                end=pagination.total_pages
            )
        incorrect_flag = memory_storage.get('admin_incorrect_flag')
        if incorrect_flag:
            await state.update_data(incorrect_flag=False)
        await message_editor_module.travel_editor.edit_message(request=request, lexicon_key='',
                                                               lexicon_part=lexicon_part, dynamic_buttons=2,
                                                               delete_mode=not pagination or incorrect_flag)
    else:
        if isinstance(request, CallbackQuery):
            await request.answer(Lexicon_module.ADMIN_LEXICON['user_non_active'])
        return await choose_specific_person_by_admin_module.choose_specific_person_by_admin_handler(request, state,
                                                                                                    first_call=False)



