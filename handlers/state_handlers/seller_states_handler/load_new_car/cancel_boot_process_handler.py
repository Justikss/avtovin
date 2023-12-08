import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.callback_handlers.sell_part.commodity_requests.commodity_requests_handler import \
    commodity_reqests_by_seller
from handlers.state_handlers.seller_states_handler.load_new_car.get_output_configs import output_load_config_for_seller


async def set_former_advert_configurations(callback: CallbackQuery, state: FSMContext):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    advert_old_configurations = await message_editor.redis_data.get_data(
        key=f'{str(callback.from_user.id)}:boot_advert_ids_kwargs',
        use_json=True)
    await state.update_data(state_for_load=advert_old_configurations.get('state'))
    await state.update_data(engine_for_load=advert_old_configurations.get('engine_type'))
    await state.update_data(brand_for_load=advert_old_configurations.get('brand'))
    await state.update_data(model_for_load=advert_old_configurations.get('model'))
    await state.update_data(complectation_for_load=advert_old_configurations.get('complectation'))
    await state.update_data(year_for_load=advert_old_configurations.get('year_of_release'))
    await state.update_data(mileage_for_load=advert_old_configurations.get('mileage'))
    await state.update_data(color_for_load=advert_old_configurations.get('color'))
    await state.update_data(sum_price=advert_old_configurations.get('sum_price'))
    await state.update_data(dollar_price=advert_old_configurations.get('dollar_price'))


async def cancel_boot_process_callback_handler(callback: CallbackQuery, state: FSMContext):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    there_data_update = await message_editor.redis_data.get_data(key=str(callback.from_user.id) + ':can_edit_seller_boot_commodity')

    if there_data_update:

        await set_former_advert_configurations(callback, state)

        structured_boot_data = await message_editor.redis_data.get_data(key=f'{str(callback.from_user.id)}:structured_boot_data', use_json=True)
        await output_load_config_for_seller(callback, state, structured_boot_data=structured_boot_data)
    else:
        await commodity_reqests_by_seller(callback, state=state, delete_mode=True)
