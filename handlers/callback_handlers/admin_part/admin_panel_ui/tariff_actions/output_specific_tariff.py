import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.state_handlers.seller_states_handler.seller_profile_branch.selected_tariff_preview import \
    tariff_preview_card_constructor


async def output_specific_tariff_for_admin_handler(callback: CallbackQuery, state: FSMContext, from_backward=False):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    if not from_backward and (isinstance(callback, CallbackQuery) and callback.data[-1].isdigit()):
        tariff_id = callback.data.split(':')[-1]
    else:
        memory_storage = await state.get_data()
        tariff_id = memory_storage.get('current_tariff_view')

    if tariff_id == 'None':
        return await callback.answer()
    tariff_lexicon_part = await tariff_preview_card_constructor(tariff_id=tariff_id, by_admin_tariff=True)
    await state.update_data(current_tariff_view=tariff_id)

    ic(tariff_lexicon_part)

    await message_editor.travel_editor.edit_message(
        request=callback, lexicon_key='', lexicon_part=tariff_lexicon_part
    )