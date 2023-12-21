import importlib
from copy import copy

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config_data.config import tariffs_pagesize
from database.data_requests.person_requests import PersonRequester
from database.data_requests.tariff_requests import TarifRequester
from handlers.callback_handlers.sell_part.checkout_seller_person_profile import get_seller_name
from handlers.state_handlers.choose_car_for_buy.choose_car_utils.output_choose_handler import output_choose
from handlers.state_handlers.seller_states_handler.seller_profile_branch.selected_tariff_preview import \
    tariff_preview_card_constructor
from utils.lexicon_utils.admin_lexicon import ChooseTariff


async def choose_tariff_for_seller_by_admin_handler(callback: CallbackQuery, state: FSMContext):

    async def generate_choose_tariff_by_admin_lexicon_class(callback: CallbackQuery, state: FSMContext):
        lexicon_class = copy(ChooseTariff)

        memory_storage = await state.get_data()
        seller_id = memory_storage.get('current_seller_id')
        seller_model = await PersonRequester.get_user_for_id(user_id=seller_id, seller=True)
        seller_model = seller_model[0]
        seller_name = await get_seller_name(seller_model, get_only_fullname=True)
        lexicon_class.message_text = lexicon_class.message_text.format(name=seller_name)
        return lexicon_class


    tariffs = await TarifRequester.retrieve_all_data()

    lexicon_class = await generate_choose_tariff_by_admin_lexicon_class(callback, state)
    await output_choose(callback, state, lexicon_class, tariffs, tariffs_pagesize)


async def checkout_tariff_for_seller_by_admin_handler(callback: CallbackQuery, state: FSMContext):
    message_editor_module = importlib.import_module('handlers.message_editor')

    if callback.data[-1].isdigit():
        tariff_id = callback.data.split(':')[-1]
        await state.update_data(current_tariff=tariff_id)
    else:
        memory_storage = await state.get_data()
        tariff_id = memory_storage.get('current_tariff')

    lexicon_part = await tariff_preview_card_constructor(tariff_id, by_admin=True)

    await message_editor_module.travel_editor.edit_message(request=callback, lexicon_key='', lexicon_part=lexicon_part)