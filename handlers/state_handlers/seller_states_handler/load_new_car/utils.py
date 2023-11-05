from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from typing import Union
import importlib

from handlers.state_handlers.seller_states_handler.load_new_car.get_output_configs import output_load_config_for_seller
from utils.Lexicon import LEXICON, LexiconCommodityLoader


async def data_update_controller(request: Union[Message, CallbackQuery], state: FSMContext):
    '''Метод контроллирует процесс переписи полей добавляемого автомобиля'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    there_data_update = await message_editor.redis_data.get_data(key=str(request.from_user.id) + ':can_edit_seller_boot_commodity')
    print('can_editt ', there_data_update )
    if isinstance(request, CallbackQuery):
        print('totest: ', request.data.startswith('rewrite_boot_'))


    if there_data_update and (((isinstance(request, CallbackQuery) and not request.data.startswith('rewrite_boot_'))) or isinstance(request, Message)):
        print("it's returnn")
        await output_load_config_for_seller(request=request, state=state)
        return True


async def create_edit_buttons_for_boot_config(boot_data, output_string, state):
    '''Метод генерирует заготовку кнопок (для InlineCreator) с назначением переписи полей добавляемого автомобиля'''
    get_load_car_state_module = importlib.import_module('handlers.state_handlers.seller_states_handler.load_new_car.hybrid_handlers')
    cars_state = await get_load_car_state_module.get_load_car_state(state=state)
    boot_config_value = list(value for value in boot_data.values())
    lexicon_button_part = LEXICON['confirm_load_config_from_seller_button']
    print('pre ', LexiconCommodityLoader.config_for_seller_button_callbacks)
    if cars_state == 'new':
        # config_slice = ((1, 6), (9, 11))
        config_edit_buttons_callback_data = LexiconCommodityLoader.config_for_seller_button_callbacks
        callbacks = config_edit_buttons_callback_data[1:5] + config_edit_buttons_callback_data[8:11]
        captions = tuple(boot_config_value[2:6] + boot_config_value[9:10])


    elif cars_state == 'second_hand':
        #config_slice = (1, 11)
        config_edit_buttons_callback_data = LexiconCommodityLoader.config_for_seller_button_callbacks
        callbacks = config_edit_buttons_callback_data[1:11]
        captions = tuple(boot_config_value[2:10])


    print('cb: ', type(callbacks), callbacks)
    print('vl: ', type(captions), captions)
    all_captions = captions + (LexiconCommodityLoader.edit_photo_caption,)
        #config_edit_buttons_caption
    print('cb: ', type(callbacks), callbacks)
    print('vl: ', type(all_captions), all_captions)

    rewrite_data_buttons = zip(callbacks, all_captions)

    lexicon_part = {'message_text': output_string}

    for key, value in rewrite_data_buttons:
        lexicon_part[key] = value
        
    for key, value in lexicon_button_part.items():
        lexicon_part[key] = value

    return lexicon_part