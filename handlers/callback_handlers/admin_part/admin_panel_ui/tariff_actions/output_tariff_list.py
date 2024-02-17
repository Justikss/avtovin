import importlib
from copy import copy

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from states.admin_part_states.tariffs_branch_states import TariffAdminBranchStates

output_choose_module = importlib.import_module(
        'handlers.state_handlers.choose_car_for_buy.choose_car_utils.output_choose_handler')
config_module = importlib.import_module('config_data.config')
admin_lexicon_module = importlib.import_module('utils.lexicon_utils.admin_lexicon.admin_lexicon')


async def output_tariffs_for_admin(request: CallbackQuery | Message, state: FSMContext):
    tariffs_requester_module = importlib.import_module('database.data_requests.tariff_requests')

    await state.update_data(edit_tariff_data=False)
    await state.set_state(TariffAdminBranchStates.tariffs_review)
    tariffs = await tariffs_requester_module.TarifRequester.retrieve_all_data()
    if not tariffs:
        tariffs = [admin_lexicon_module.TariffNonExistsPlug()]
    lexicon_class = copy(admin_lexicon_module.AllTariffsOutput)()
    await output_choose_module.output_choose(request, state, lexicon_class=lexicon_class, models_range=tariffs,
                                             page_size=config_module.tariffs_pagesize)