import importlib
import logging

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.data_requests.person_requests import PersonRequester
from database.data_requests.tariff_to_seller_requests import TariffToSellerBinder
from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_specific.choose_specific_person import \
    choose_specific_person_by_admin_handler
from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_specific.output_specific_seller import \
    output_specific_user_profile_handler
from handlers.callback_handlers.sell_part.checkout_seller_person_profile import get_seller_name
from utils.lexicon_utils.Lexicon import ADMIN_LEXICON
from utils.lexicon_utils.admin_lexicon.admin_lexicon import SelectTariff
from utils.lexicon_utils.logging_utils.admin_loggings import log_admin_action


async def confirm_question_set_tariff_to_seller_by_admin(callback: CallbackQuery, state: FSMContext):
    tariff_requests_module = importlib.import_module('database.data_requests.tariff_requests')
    message_editor_module = importlib.import_module('handlers.message_editor')
    memory_storage = await state.get_data()

    tariff_id = memory_storage.get('current_tariff')
    seller_id = memory_storage.get('current_seller_id')
    seller_tariff_exists = memory_storage.get('tariff_exists')

    tariff = await tariff_requests_module.TarifRequester.get_by_id(tariff_id)
    seller = await PersonRequester.get_user_for_id(seller_id, seller=True)
    ic(seller)
    if seller and tariff:
        seller_name = await get_seller_name(seller[0], get_only_fullname=True)
        lexicon_class = SelectTariff(seller_tariff_exists, tariff.name, seller_name)
        lexicon_part = lexicon_class.lexicon_part
        await message_editor_module.travel_editor.edit_message(request=callback, lexicon_key='',
                                                            lexicon_part=lexicon_part, dynamic_buttons=2)
    else:
        await callback.answer(ADMIN_LEXICON['user_non_active'])
        await choose_specific_person_by_admin_handler(callback, state, first_call=False)
        # logging.critical(
        #     f'''Администратор {callback.from_user.id {memory_storage.get('current_seller_id')}''')

async def confirm_action_tariff_to_seller_by_admin(callback: CallbackQuery, state: FSMContext):
    memory_storage = await state.get_data()
    seller_id = memory_storage.get('current_seller_id')
    set_tariff = await TariffToSellerBinder.set_bind({'seller': seller_id,
                                         'tariff': memory_storage.get('current_tariff')},
                                        seconds=None, bot=callback.bot)

    if set_tariff:
        await callback.answer(ADMIN_LEXICON['success_set_tariff'])
        await output_specific_user_profile_handler(callback, state)
        await log_admin_action(admin_username=callback.from_user.username,
                               action='set_seller_tariff_action',
                               subject=f'seller:{seller_id}')
    else:
        await callback.answer(ADMIN_LEXICON['failed_set_tariff'])
        await choose_specific_person_by_admin_handler(callback, state,
                                                      first_call=False)

