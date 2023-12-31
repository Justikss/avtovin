import importlib
import logging

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.callback_handlers.sell_part.checkout_seller_person_profile import seller_profile_card_constructor, \
    get_seller_name
from utils.lexicon_utils.Lexicon import ADMIN_LEXICON
from utils.lexicon_utils.admin_lexicon.admin_lexicon import ReviewSellerTariff


async def construct_review_tariff_by_admin(callback: CallbackQuery, state: FSMContext, get_header=False):
    person_requester_module = importlib.import_module('database.data_requests.person_requests')

    memory_storage = await state.get_data()
    seller_id = memory_storage.get('current_seller_id')
    ic(seller_id)
    tariff_card, tariff_exists = await seller_profile_card_constructor(user_id=seller_id,
                                                                        get_part='bottom', for_admin=True)
    seller_model = await person_requester_module.PersonRequester.get_user_for_id(user_id=seller_id, seller=True)

    if seller_model:
        seller_model = seller_model[0]

        review_tariff_card_materials = ReviewSellerTariff(tariff_exists)
        await state.update_data(tariff_exists=tariff_exists)
        seller_name = await get_seller_name(seller_model, get_only_fullname=True)
        if seller_name:
            tariff_output_header = f'''{review_tariff_card_materials.message_header[seller_model.entity].format(name=seller_name)}'''
            if get_header:
                return tariff_output_header

            if tariff_card:
                tariff_card = tariff_card.split('\n')
                tariff_card[0] = f'{tariff_output_header}{tariff_card[0]}'
                tariff_card = '\n'.join(tariff_card)
                lexicon_part = {'message_text': tariff_card, 'buttons': {**review_tariff_card_materials.buttons}}
                return lexicon_part
            else:
                if seller_model:
                    lexicon_part = {'message_text': f'{tariff_output_header}{review_tariff_card_materials.tariff_not_exists}',
                                    'buttons': {**review_tariff_card_materials.buttons}}
                    return lexicon_part
    return False


async def checkout_seller_tariff_by_admin_handler(callback: CallbackQuery, state: FSMContext):
    choose_specific_person_by_admin_module = importlib.import_module('handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_specific.choose_specific_person')
    message_editor_module = importlib.import_module('handlers.message_editor')
    ic()
    tariff_card = await construct_review_tariff_by_admin(callback, state)
    if not tariff_card:
        memory_storage = await state.get_data()
        await callback.answer(ADMIN_LEXICON['user_non_active'])
        await choose_specific_person_by_admin_module.choose_specific_person_by_admin_handler(callback, state, first_call=False)
        logging.critical(
            f'''Администратор {callback.from_user.id} не смог получить вывод тарифа продавца {memory_storage.get('current_seller_id')}''')
        return
    ic(tariff_card)
    await message_editor_module.travel_editor.edit_message(request=callback, lexicon_key='',
                                                           lexicon_part=tariff_card, dynamic_buttons=2)