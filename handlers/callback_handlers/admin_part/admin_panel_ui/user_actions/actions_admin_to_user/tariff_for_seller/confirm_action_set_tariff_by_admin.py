import importlib
import logging

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_specific.output_specific_seller import \
    output_specific_seller_profile_handler
from handlers.callback_handlers.sell_part.checkout_seller_person_profile import get_seller_name
from utils.lexicon_utils.logging_utils.admin_loggings import log_admin_action

Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

async def confirm_question_set_tariff_to_seller_by_admin(callback: CallbackQuery, state: FSMContext):
    tariff_requests_module = importlib.import_module('database.data_requests.tariff_requests')
    person_requester_module = importlib.import_module('database.data_requests.person_requests')
    choose_specific_person_by_admin_module = importlib.import_module('handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_specific.choose_specific_person')
    message_editor_module = importlib.import_module('handlers.message_editor')
    memory_storage = await state.get_data()

    tariff_id = memory_storage.get('current_tariff')
    seller_id = memory_storage.get('current_seller_id')
    seller_tariff_exists = memory_storage.get('tariff_exists')

    tariff = await tariff_requests_module.TarifRequester.get_by_id(tariff_id)
    seller = await person_requester_module.PersonRequester.get_user_for_id(seller_id, seller=True)
    ic(seller)
    if seller and tariff:
        admin_lexicon_module = importlib.import_module('utils.lexicon_utils.admin_lexicon.admin_lexicon')

        seller_name = await get_seller_name(seller[0], get_only_fullname=True)
        lexicon_class = admin_lexicon_module.SelectTariff(seller_tariff_exists, tariff.name, seller_name)
        lexicon_part = lexicon_class.lexicon_part
        await message_editor_module.travel_editor.edit_message(request=callback, lexicon_key='',
                                                            lexicon_part=lexicon_part, dynamic_buttons=2)
    else:
        await callback.answer(Lexicon_module.ADMIN_LEXICON['user_non_active'])
        await choose_specific_person_by_admin_module.choose_specific_person_by_admin_handler(callback, state, first_call=False)
        # logging.critical(
        #     f'''Администратор {callback.from_user.id {memory_storage.get('current_seller_id')}''')

async def confirm_action_tariff_to_seller_by_admin(callback: CallbackQuery, state: FSMContext):
    tariff_to_seller_binder = importlib.import_module('database.data_requests.tariff_to_seller_requests')
    choose_specific_person_by_admin_module = importlib.import_module('handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_specific.choose_specific_person')

    memory_storage = await state.get_data()
    seller_id = memory_storage.get('current_seller_id')
    set_tariff = await tariff_to_seller_binder.TariffToSellerBinder.set_bind({'seller': seller_id,
                                         'tariff': memory_storage.get('current_tariff')},
                                        seconds=None, bot=callback.bot)

    if set_tariff:
        await callback.answer(Lexicon_module.ADMIN_LEXICON['success_set_tariff'])
        await output_specific_seller_profile_handler(callback, state)
        await log_admin_action(admin_username=callback.from_user.username,
                               action='set_seller_tariff_action',
                               subject=f'seller:{seller_id}')
    else:
        await callback.answer(Lexicon_module.ADMIN_LEXICON['failed_set_tariff'])
        await choose_specific_person_by_admin_module.choose_specific_person_by_admin_handler(callback, state,
                                                      first_call=False)

