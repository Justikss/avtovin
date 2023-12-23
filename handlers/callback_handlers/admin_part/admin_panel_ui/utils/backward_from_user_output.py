import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery


async def backward_from_user_profile_review(request: CallbackQuery | Message, state: FSMContext):
    choose_specific_person_by_admin_module = importlib.import_module('handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_specific.choose_specific_person')

    await choose_specific_person_by_admin_module.choose_specific_person_by_admin_handler(request, state,
                                                  first_call=False)



