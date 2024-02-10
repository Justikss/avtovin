import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery


async def edit_boot_car_data_handler(callback: CallbackQuery, state: FSMContext):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    lexicon_module = importlib.import_module('utils.lexicon_utils.commodity_loader')

    last_message_id = await message_editor.redis_data.get_data(key=f'{str(callback.from_user.id)}:last_message')
    if last_message_id:
        inline_creator_module = importlib.import_module('keyboards.inline.kb_creator')
        create_buttons_module = importlib.import_module(
            'handlers.state_handlers.seller_states_handler.load_new_car.utils')

        structured_boot_data = await message_editor.redis_data.get_data(key=f'{str(callback.from_user.id)}:structured_boot_data', use_json=True)
        lexicon_part = await create_buttons_module.create_edit_buttons_for_boot_config(state=state,
                                                                                       boot_data=structured_boot_data,
                                                                                       output_string='', rewrite_mode=True)
        keyboard = await inline_creator_module.InlineCreator.create_markup(input_data=lexicon_part)
        await callback.message.edit_reply_markup(reply_markup=keyboard)
        await callback.answer(lexicon_module.LexiconCommodityLoader.can_rewrite_config, show_alert=True)
