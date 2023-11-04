from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
import importlib

from utils.Lexicon import LexiconCommodityLoader, LEXICON
from handlers.state_handlers.load_new_car.hybrid_handlers import get_load_car_state
from handlers.state_handlers.load_new_car.load_data_fromatter import data_formatter

async def output_load_config_for_seller(message: Message, state: FSMContext, photo: dict):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    await message.delete()
    await state.update_data(load_photo=photo)

    delete_mode = False

    memory_storage = await state.get_data()
    if memory_storage['incorrect_flag']:
        await state.update_data(incorrect_flag=False)
        delete_mode = True

    structured_boot_data = await data_formatter(request=message, state=state)

    output_string = await LexiconCommodityLoader.get_output_string(mode='to_seller',
                                                                    boot_data=structured_boot_data)

    await message_editor.redis_data.set_data(key=str(message.from_user.id) + ':boot_config', value=output_string)

    output_string = '\n'.join(output_string.split('\n')[:-1])

    lexicon_button_part = LEXICON['confirm_load_config_from_seller_button']
    lexicon_part = {'message_text': output_string}
    for key, value in lexicon_button_part.items():
        lexicon_part[key] = value
    
    await message_editor.travel_editor.edit_message(request=message, lexicon_key='', lexicon_part=lexicon_part, photo=structured_boot_data['photo']['id'], delete_mode=delete_mode, seller_boot=True)

