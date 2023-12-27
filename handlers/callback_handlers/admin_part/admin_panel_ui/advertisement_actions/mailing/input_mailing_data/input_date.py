from aiogram import types
from aiogram.fsm.context import FSMContext

from handlers.callback_handlers.admin_part.admin_panel_ui.advertisement_actions.mailing.input_mailing_data.edit_mailing_data.edit_data_controller import \
    edit_mailing_data_controller
from handlers.callback_handlers.admin_part.admin_panel_ui.tariff_actions.input_data_utils.incorrect_controller import \
    incorrect_controller
from states.admin_part_states.mailing_setup_states import MailingStates
import importlib

# Импорт модуля редактирования сообщений через importlib
message_editor_module = importlib.import_module('handlers.message_editor')

# Обработчик для запроса ввода даты и времени
# @dp.message_handler(state=MailingStates.entering_date_time)
async def request_mailing_date_time(request: types.Message | types.CallbackQuery, state: FSMContext, media_pack=False, incorrect=False):
    if media_pack or (isinstance(request, types.CallbackQuery) and request.data == 'mailing_without_media'):
        if not media_pack:
            media_pack = None
        ic(media_pack)
        memory_storage = await state.get_data()
        if memory_storage.get('add_other_media'):
            last_media = memory_storage.get('mailing_media')
            if media_pack:
                media_pack = last_media + media_pack
        await state.update_data(mailing_media=media_pack)

    if await edit_mailing_data_controller(request, state, incorrect):
        return

    await state.set_state(MailingStates.choosing_recipients)
    lexicon_part, reply_to_message = await incorrect_controller(request, state, incorrect, 'request_mailing_date_time')
    await message_editor_module.travel_editor.edit_message(request=request, lexicon_key='', lexicon_part=lexicon_part,
                                                           reply_message=reply_to_message, delete_mode=True)
