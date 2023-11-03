from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
import importlib

from utils.Lexicon import LexiconCommodityLoader, LEXICON
from handlers.state_handlers.load_new_car.hybrid_handlers import get_load_car_state
from handlers.state_handlers.load_new_car.load_data_fromatter import data_formatter

async def output_load_config_for_seller(message: Message, state: FSMContext):
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    await message.delete()
    await state.update_data(load_photo=message.text)
    # memory_storage = await state.get_data()
    # car_state = await get_load_car_state(state=state)

    # state = memory_storage['state_for_load']
    # engine = memory_storage['engine_for_load']
    # brand = memory_storage['brand_for_load']
    # model = memory_storage['model_for_load']
    # complectation = memory_storage['complectation_for_load']
    # price = message.text

    # if car_state == 'new':
    #     year = None
    #     mileage = None
    #     color = None

    # elif car_state == 'second_hand':
    #     # year
    #     # mileage
    #     # color
    #     pass

    structured_boot_data = await data_formatter(request=message, state=state)

    output_string = await LexiconCommodityLoader.get_output_string(mode='to_seller',
                                                                    boot_data=structured_boot_data)


    await message_editor.redis_data.set_data(key=str(message.from_user.id) + ':boot_config', value=output_string)

    output_string = '\n'.join(output_string.split('\n')[:-1])

    lexicon_button_part = LEXICON['confirm_load_config_from_seller_button']
    lexicon_part = {'message_text': output_string}
    for key, value in lexicon_button_part.items():
        lexicon_part[key] = value
    
    await message_editor.travel_editor.edit_message(request=message, lexicon_key='', lexicon_part=lexicon_part, photo=structured_boot_data['photo_url'])

