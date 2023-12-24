from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from handlers.callback_handlers.admin_part.admin_panel_ui.tariff_actions.edit_tariff.edit_tariff_handler import \
    edit_tariff_by_admin_handler


async def edit_tariff_data_controller(request: CallbackQuery | Message, state: FSMContext, incorrect=False):
    if not incorrect:
        memory_storage = await state.get_data()
        edit_tariff_data_mode = memory_storage.get('edit_tariff_data')

        if edit_tariff_data_mode and isinstance(request, Message):
            await edit_tariff_by_admin_handler(callback=request, state=state) #Подправить рекуест в обработке
            return True
