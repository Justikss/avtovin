import importlib
from copy import copy

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config_data.config import tariffs_pagesize
from states.admin_part_states.tariffs_branch_states import TariffAdminBranchStates
from utils.lexicon_utils.admin_lexicon.admin_lexicon import AllTariffsOutput, TariffNonExistsPlug

output_choose_module = importlib.import_module(
        'handlers.state_handlers.choose_car_for_buy.choose_car_utils.output_choose_handler')


async def output_tariffs_for_admin(request: CallbackQuery | Message, state: FSMContext):
    tariffs_requester_module = importlib.import_module('database.data_requests.tariff_requests')

    await state.update_data(edit_tariff_data=False)
    await state.set_state(TariffAdminBranchStates.tariffs_review)
    tariffs = await tariffs_requester_module.TarifRequester.retrieve_all_data()
    if not tariffs:
        tariffs = [TariffNonExistsPlug]
    lexicon_class = copy(AllTariffsOutput)
    await output_choose_module.output_choose(request, state, lexicon_class=lexicon_class, models_range=tariffs, page_size=tariffs_pagesize)