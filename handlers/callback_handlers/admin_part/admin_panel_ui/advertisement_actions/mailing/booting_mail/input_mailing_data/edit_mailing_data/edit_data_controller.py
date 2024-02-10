from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from handlers.callback_handlers.admin_part.admin_panel_ui.advertisement_actions.mailing.booting_mail.review_inputted_data import \
    request_review_mailing_data


async def edit_mailing_data_controller(request: CallbackQuery | Message, state: FSMContext, incorrect=False):

    if isinstance(request, CallbackQuery) and request.data == 'add_other_media':
        return False
    if not incorrect:
        current_state = str(await state.get_state())
        memory_storage = await state.get_data()
        edit_mailing_flag = memory_storage.get('can_edit_mailing_flag')

        if edit_mailing_flag and current_state != 'MailingStates:edit_inputted_data':
            await request_review_mailing_data(request, state=state)
            return True