import importlib
import phonenumbers
from typing import Union
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest

from utils.Lexicon import LEXICON
from handlers.state_handlers.seller_states_handler.seller_registration import utils
from handlers.state_handlers.buyer_registration_handlers import registartion_view_corrector
from states.seller_registration_states import HybridSellerRegistrationStates, PersonSellerRegistrationStates, CarDealerShipRegistrationStates
from handlers.custom_filters import correct_name, correct_number


async def input_seller_name(request: Union[CallbackQuery, Message], state: FSMContext, incorrect = None):
    message_editor_module = importlib.import_module('handlers.message_editor')
    redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт

    seller_mode = await redis_module.redis_data.get_data(key=str(request.from_user.id) + ':seller_registration_mode')
    print('seller_mode', seller_mode)

    if str(await state.get_state()) != 'PersonSellerRegistrationStates:input_fullname':
        await state.set_state(PersonSellerRegistrationStates.input_fullname)

    if isinstance(request, CallbackQuery):
        request = request.message
    elif isinstance(request, Message):
        pass
    


    if incorrect:
        await state.update_data(incorrect_answer=True)
        if seller_mode == 'dealership':
            lexicon_code = 'write_dealership_name' + incorrect
        elif seller_mode == 'person':
            lexicon_code = 'write_full_seller_name' + incorrect

        message_reply_mode = True
        print('reply_mode1')
        delete_last_message_mode = True

            
        await registartion_view_corrector(request=request, state=state)
        

        await redis_module.redis_data.set_data(
            key=str(request.from_user.id) + ':last_user_message',
            value=request.message_id)

    else:
        print(seller_mode)
        if seller_mode == 'dealership':
            
            lexicon_code = 'write_dealership_name'
            print('lexdeal', lexicon_code)
        elif seller_mode == 'person':
            lexicon_code = 'write_full_seller_name'
            

        message_reply_mode = False
        delete_last_message_mode = False

    print('start_editor_with', lexicon_code)
    await message_editor_module.travel_editor.edit_message(request=request, lexicon_key=lexicon_code, lexicon_cache=False,
                                                            reply_mode=message_reply_mode)

    await state.set_state(HybridSellerRegistrationStates.input_number)
    

#Фильтр CorrectName()
async def hybrid_input_seller_number(request: Union[CallbackQuery, Message], state: FSMContext, user_name=None, incorrect = None):
    message_editor_module = importlib.import_module('handlers.message_editor')
    redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт
    print('user_name', user_name)
    if user_name:
        await state.update_data(seller_name=user_name)

    if isinstance(request, CallbackQuery):
        message = request.message
    elif isinstance(request, Message):
        message = request

    edit_mode = await redis_module.redis_data.get_data(key=str(request.from_user.id) + ':can_edit_seller_registration_data')
    if user_name and edit_mode=='true':
        await state.set_state(HybridSellerRegistrationStates.check_input_data)
        return await check_your_config(request=request, state=state)
    
    bot = message.chat.bot

    if incorrect:
        await state.update_data(incorrect_answer=True)
        lexicon_code = 'write_seller_phone_number' + incorrect
        message_reply_mode = True
        print('reply_mode1')
        delete_last_message_mode = True

        await registartion_view_corrector(request=request, state=state)
        
        

        await redis_module.redis_data.set_data(
            key=str(request.from_user.id) + ':last_user_message',
            value=message.message_id)
        
    else:
        redis_key = str(request.from_user.id) + ':last_user_message'
        try:
            last_user_message = await redis_module.redis_data.get_data(key=redis_key)
        except TelegramBadRequest:
            pass
        if last_user_message:
            await bot.delete_message(chat_id=message.chat.id, message_id=last_user_message)
            await redis_module.redis_data.delete_key(key=redis_key)
        await bot.delete_message(chat_id=message.chat.id, message_id = message.message_id)
        lexicon_code = 'write_seller_phone_number'
        message_reply_mode = False
        delete_last_message_mode = False

    await message_editor_module.travel_editor.edit_message(request=request, lexicon_key=lexicon_code,
                                                             lexicon_cache=False, 
                                                             reply_mode = message_reply_mode)
    
    await state.set_state(HybridSellerRegistrationStates.check_input_data)


#Фильтр CorrectNumber
async def check_your_config(request: Union[CallbackQuery, Message], state: FSMContext, input_number=None):
    '''Обработчик конечного состояния регистрации пользовтаеля:
    Сверка введённых рег. данных'''
    message_editor_module = importlib.import_module('handlers.message_editor')
    redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт


    if input_number:
        await state.update_data(seller_number=input_number)
        print('seller_number', input_number)

    bot = request.chat.bot
    await bot.delete_message(chat_id=request.chat.id, message_id=request.message_id)
    memory_storage = await state.get_data()
    await registartion_view_corrector(request=request, state=state)
    

    lexicon_part = LEXICON['checking_seller_entered_data']
    lexicon_part['rewrite_seller_name'] = memory_storage['seller_name']
    lexicon_part['rewrite_seller_number'] = memory_storage['seller_number']
    print(lexicon_part)

    edit_mode = await redis_module.redis_data.get_data(key=str(request.from_user.id) + ':can_edit_seller_registration_data')

    if edit_mode == 'true':
        delete_mode = False
    else:
        delete_mode = True


    await message_editor_module.travel_editor.edit_message(lexicon_key=None, request=request, lexicon_part=lexicon_part, delete_mode=True)

    await redis_module.redis_data.set_data(key=str(request.from_user.id) + ':can_edit_seller_registration_data', value='true')


    # if data_is_valid:
    #     await utils.load_seller_in_database(callback=request)

    #person=True
    # if person:
    #     person_fullname = memory_storage.get('seller_person_name')
    #     person_number = input_number

    # elif dealership:
    #     dealership_name = memory_storage.get('dealership_name')
    #     dealership_number = memory_storage.get('dealership_number')
    


    

    