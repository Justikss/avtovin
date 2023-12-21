from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_specific.choose_specific_person import \
    choose_specific_person_by_admin_handler


async def backward_from_user_profile_review(request: CallbackQuery | Message, state: FSMContext):
    await choose_specific_person_by_admin_handler(request, state,
                                                  first_call=False)



