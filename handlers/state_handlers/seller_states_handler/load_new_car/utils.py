from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from typing import Union
import importlib

from handlers.state_handlers.seller_states_handler.load_new_car.get_output_configs import output_load_config_for_seller
from handlers.state_handlers.seller_states_handler.load_new_car import second_hand_handlers
from utils.Lexicon import LEXICON, LexiconCommodityLoader
from states.load_commodity_states import LoadCommodityStates

async def rewrite_boot_state_stopper(request: Union[CallbackQuery, Message], state: FSMContext, return_output=None):
    memory_data = await state.get_data()
    rewrite_state_flag = memory_data.get('rewrite_state_flag')
    if rewrite_state_flag == LexiconCommodityLoader.load_commodity_state['buttons']['load_state_second_hand']:
        print("it's returnn")
        if return_output:
            await output_load_config_for_seller(request=request, state=state)
        return False
    else:
        return True


async def change_boot_car_state_controller(callback, state):
    '''Метод для контроля работы дополнительной записи конфигураций при переписи состояния с Новой на Бу'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
    
    memory_storage = await state.get_data()
    last_car_state = memory_storage.get('state_for_load')
    print('cbd: ', callback.data)
    if await message_editor.redis_data.get_data(key=str(callback.from_user.id) + ':can_edit_seller_boot_commodity')\
        and last_car_state != callback.data:
    
        await state.update_data(state_for_load=callback.data)
        await state.update_data(rewrite_state_flag=LexiconCommodityLoader.load_commodity_state['buttons'][callback.data])
        if callback.data.endswith('new'):
            await state.update_data(year_for_load=None)
            await state.update_data(mileage_for_load=None)
            await state.update_data(color_for_load=None)


async def data_update_controller(request: Union[Message, CallbackQuery], state: FSMContext):
    '''Метод контроллирует процесс переписи полей добавляемого автомобиля'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт

    memory_storage = await state.get_data()
    there_data_update = await message_editor.redis_data.get_data(key=str(request.from_user.id) + ':can_edit_seller_boot_commodity')
    print('can_editt ', there_data_update )
    if isinstance(request, CallbackQuery):
        print('totest: ', request.data.startswith('rewrite_boot_'))

    if there_data_update:
        last_config_message = await message_editor.redis_data.get_data(key=str(request.from_user.id) + ':last_message')
        if isinstance(request, Message):
            message = request
        else:
            rewrite_state_flag = memory_storage.get('rewrite_state_flag')
            if rewrite_state_flag:
                print('rewrf: ', rewrite_state_flag)
                current_state = str(await state.get_state())
                print('curst: ', current_state)
                if rewrite_state_flag == LexiconCommodityLoader.load_commodity_state['buttons']['load_state_new']:
                    pass
                elif rewrite_state_flag == LexiconCommodityLoader.load_commodity_state['buttons']['load_state_second_hand']:
                    if current_state == 'LoadCommodityStates:input_to_load_engine_type':
                        await state.set_state(LoadCommodityStates.input_to_load_year)
                        await second_hand_handlers.input_year_to_load(callback=request, state=state)
                        return True
                    elif current_state == 'LoadCommodityStates:input_to_load_price':
                        await state.update_data(rewrite_state_flag=None)
                        pass
                    else:
                        return False
            
            message = request.message
        #при послестэйтных выборах не удалится что то?
        try:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=last_config_message)
        except TelegramBadRequest:
            pass


        if ((isinstance(request, CallbackQuery) and not request.data.startswith('rewrite_boot_')) or isinstance(request, Message)):
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
        callbacks = config_edit_buttons_callback_data[0:5] + config_edit_buttons_callback_data[8:11]
        captions = list(boot_config_value[1:6] + boot_config_value[9:10])
        print(captions)
        captions[5] = LexiconCommodityLoader.load_commodity_price['message_text'] + ' ' + captions[5]

    elif cars_state == 'second_hand':
        #config_slice = (1, 11)
        config_edit_buttons_callback_data = LexiconCommodityLoader.config_for_seller_button_callbacks
        callbacks = config_edit_buttons_callback_data[0:11]
        captions = list(boot_config_value[1:10])
        captions[5] = LexiconCommodityLoader.load_commodity_year_of_realise['message_text'] + ' ' + captions[5]
        captions[6] = LexiconCommodityLoader.load_commodity_mileage['message_text'] + ' ' + captions[6]
        captions[8] = LexiconCommodityLoader.load_commodity_price['message_text'] + ' ' + captions[8]
    
    captions = tuple(captions)
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