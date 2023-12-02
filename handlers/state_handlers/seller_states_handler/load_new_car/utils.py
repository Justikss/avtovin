from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from typing import Union
import importlib

from config_data.config import money_valute
from database.data_requests.car_configurations_requests import CarConfigs
from database.data_requests.new_car_photo_requests import PhotoRequester
from handlers.state_handlers.seller_states_handler.load_new_car.get_output_configs import output_load_config_for_seller
from handlers.state_handlers.seller_states_handler.load_new_car import second_hand_handlers
from utils.Lexicon import LEXICON, LexiconCommodityLoader
from states.load_commodity_states import LoadCommodityStates

async def rewrite_boot_state_stopper(request: Union[CallbackQuery, Message], state: FSMContext, return_output=None):
    memory_data = await state.get_data()
    rewrite_state_flag = memory_data.get('rewrite_state_flag')
    # car_states = await CarConfigs.get_all_states()
    if rewrite_state_flag == 2:
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
    edit_mode = await message_editor.redis_data.get_data(key=str(callback.from_user.id) + ':can_edit_seller_boot_commodity')
    if edit_mode\
        and int(last_car_state) != int(callback.data.split('_')[-1]):

        await state.update_data(state_for_load=int(callback.data.split('_')[-1]))
        await state.update_data(rewrite_state_flag=callback.data.split('_')[-1])
        if callback.data.endswith('1'):
            await set_photo_for_new_state_car(state)
            await state.update_data(year_for_load=None)
            await state.update_data(mileage_for_load=None)
            await state.update_data(color_for_load=None)


async def data_update_controller(request: Union[Message, CallbackQuery], state: FSMContext):
    '''Метод контроллирует процесс переписи полей добавляемого автомобиля'''
    message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт


    memory_storage = await state.get_data()
    there_data_update = await message_editor.redis_data.get_data(key=str(request.from_user.id) + ':can_edit_seller_boot_commodity')
    print('can_editt ', there_data_update)
    if isinstance(request, CallbackQuery):
        print('totest: ', request.data.startswith('rewrite_boot_'))
    ic()
    if there_data_update:
        last_config_message = await message_editor.redis_data.get_data(key=str(request.from_user.id) + ':last_message')
        ic(last_config_message)
        if isinstance(request, Message):
            message = request
        else:
            input_photo_module = importlib.import_module(
                'handlers.state_handlers.seller_states_handler.load_new_car.second_hand_handlers')

            ic(memory_storage.get('state_for_load'))
            current_state = str(await state.get_state())
            rewrite_state_flag = memory_storage.get('rewrite_state_flag')
            ic(rewrite_state_flag)



            if current_state in ('LoadCommodityStates:input_to_load_complectation',
                                         'LoadCommodityStates:input_to_load_model') and memory_storage.get('state_for_load') == 1:
                await set_photo_for_new_state_car(state)

            ic(rewrite_state_flag)
            if rewrite_state_flag:
                if int(rewrite_state_flag) == 1:
                    ic()
                    await state.update_data(rewrite_state_flag=None)
                    pass

                elif int(rewrite_state_flag) == 2:
                    ic()
                    if current_state == 'LoadCommodityStates:input_to_load_engine_type':
                        await state.set_state(LoadCommodityStates.input_to_load_year)

                        await second_hand_handlers.input_year_to_load(callback=request, state=state)
                        ic()
                        return True
                    elif current_state == 'LoadCommodityStates:input_to_load_price':
                        await state.set_state(LoadCommodityStates.photo_verification)
                        ic()
                        await state.set_state(LoadCommodityStates.input_to_load_photo)
                        await input_photo_module.input_photo_to_load(request, state)
                        # await output_load_config_for_seller(request=request, state=state)
                        await state.update_data(rewrite_state_flag=None)
                        ic()
                        return True
                    else:
                        ic()
                        return False

            else:
                if isinstance(request, CallbackQuery):
                    edit_mode = await message_editor.redis_data.get_data(
                        key=str(request.from_user.id) + ':can_edit_seller_boot_commodity')

                    # if not request.data.startswith('rewrite_boot_'):
                    if request.data[-1].isdigit():
                        selected_id = int(request.data.split('_')[-1])
                    else:
                        selected_id = None
                    # if selected_id and ((not edit_mode) or (memory_storage.get('rewrite_brand_mode'))):
                    #     if current_state == 'LoadCommodityStates.input_to_load_brand':
                    #         ic()
                    #         last_value = memory_storage.get('engine_for_load')
                    #         await state.update_data(engine_for_load=selected_id)
                    #         if last_value != selected_id:
                    #             await state.update_data(rewrite_brand_mode=True)
                    #             ic()
                    #             return False

                        if current_state == 'LoadCommodityStates:input_to_load_model':
                            last_value = memory_storage.get('brand_for_load')
                            await state.update_data(brand_for_load=selected_id)
                            if last_value != selected_id:
                                await state.update_data(rewrite_brand_mode=True)
                                ic()
                                return False

                        elif current_state == 'LoadCommodityStates:input_to_load_complectation':
                            last_value = memory_storage.get('model_for_load')
                            await state.update_data(model_for_load=selected_id)
                            if (memory_storage.get('rewrite_brand_mode')) or (
                                    last_value != int(request.data.split('_')[-1])):
                                ic()
                                return False


                        elif current_state in (
                        'LoadCommodityStates:input_to_load_price', 'LoadCommodityStates:input_to_load_year'):
                            ic()
                            ic('complectation1221', selected_id)
                            if (not edit_mode) or (memory_storage.get('rewrite_brand_mode')):
                                await state.update_data(complectation_for_load=selected_id)
                            if memory_storage.get('rewrite_brand_mode'):
                                # await state.update_data(complectation_for_load=int(request.data.split('_')[-1]))
                                ic()
                                pass

            message = request.message
        #при послестэйтных выборах не удалится что то?
        try:
            ic(await message.bot.delete_message(chat_id=message.chat.id, message_id=last_config_message))
        except TelegramBadRequest as ex:
            ic(ex)
            pass

        if ((isinstance(request, CallbackQuery) and not request.data.startswith('rewrite_boot_')) or isinstance(request, Message)):
            print("it's returnn")
            await output_load_config_for_seller(request=request, state=state)
            return True


async def create_edit_buttons_for_boot_config(boot_data, output_string, state, rewrite_mode=False):
    '''Метод генерирует заготовку кнопок (для InlineCreator) с назначением переписи полей добавляемого автомобиля'''
    get_load_car_state_module = importlib.import_module('handlers.state_handlers.seller_states_handler.load_new_car.hybrid_handlers')
    cars_state = await get_load_car_state_module.get_load_car_state(state=state)
    boot_config_value = list(value for value in boot_data.values())
    lexicon_button_part = LEXICON['confirm_load_config_from_seller_button']
    if rewrite_mode:
        # all_captions = None
        print('pre ', LexiconCommodityLoader.config_for_seller_button_callbacks)
        if cars_state == 'new':
            # config_slice = ((1, 6), (9, 11))
            config_edit_buttons_callback_data = LexiconCommodityLoader.config_for_seller_button_callbacks
            callbacks = config_edit_buttons_callback_data[0:5] + config_edit_buttons_callback_data[8:9] + config_edit_buttons_callback_data[10:11]
            captions = list(boot_config_value[1:6] + boot_config_value[9:10])
            ic(captions)
            ic(callbacks)
            captions[5] = LexiconCommodityLoader.load_commodity_price['message_text'] + ' ' + str(captions[5] + ' '+ money_valute)

        elif cars_state == 'second_hand':
            #config_slice = (1, 11)
            config_edit_buttons_callback_data = LexiconCommodityLoader.config_for_seller_button_callbacks
            callbacks = config_edit_buttons_callback_data[0:11]
            captions = list(boot_config_value[1:10])
            captions[5] = LexiconCommodityLoader.load_commodity_year_of_realise.message_text + ' ' + captions[5]
            captions[6] = LexiconCommodityLoader.load_commodity_mileage.message_text + ' ' + captions[6]
            captions[8] = LexiconCommodityLoader.load_commodity_price['message_text'] + ' ' + str(captions[8] + ' '+ money_valute)
            ic(type(captions))
            captions.append(LexiconCommodityLoader.edit_photo_caption)
            # all_captions = captions + (LexiconCommodityLoader.edit_photo_caption,)


        captions = tuple(captions)
        # print('cb: ', type(callbacks), callbacks)
        # print('vl: ', type(captions), captions)
        #
        #     #config_edit_buttons_caption
        # print('cb: ', type(callbacks), callbacks)
        # print('vl: ', type(all_captions), all_captions)
        # if not all_captions:
        #     all_captions = captions

        rewrite_data_buttons = zip(callbacks, captions)

        lexicon_part = {'message_text': output_string}
        ic(lexicon_part)
        for key, value in rewrite_data_buttons:
            lexicon_part[key] = value
        ic(lexicon_part)

        for key, value in lexicon_button_part.items():
            if key != 'edit_boot_car_data':
                lexicon_part[key] = value
        ic(lexicon_part)
        return lexicon_part

    else:
        return {'message_text': output_string, 'buttons': lexicon_button_part}

async def set_photo_for_new_state_car(state: FSMContext):
    memory_storage = await state.get_data()
    new_photographies = await PhotoRequester.try_get_photo(state)
    ic(new_photographies)
    await state.update_data(load_photo=new_photographies)