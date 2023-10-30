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
    check_reg_config_module = importlib.import_module('handlers.state_handlers.seller_states_handler.seller_registration.check_your_registration_config')

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
        return await check_reg_config_module.check_your_config(request=request, state=state)
    
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
                                                             reply_mode = message_reply_mode)
    
    await state.set_state(CarDealerShipRegistrationStates.input_dealship_name)



async def dealership_input_address(request: Union[CallbackQuery, Message], state: FSMContext, input_number=None, incorrect=None):
    print('dealer', type(request))
    message_editor_module = importlib.import_module('handlers.message_editor')
    redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт
    check_reg_config_module = importlib.import_module('handlers.state_handlers.seller_states_handler.seller_registration.check_your_registration_config')


    if input_number:
        await state.update_data(seller_number=input_number)

    
    seller_mode = await redis_module.redis_data.get_data(key=str(request.from_user.id) + ':seller_registration_mode')
    edit_mode = await redis_module.redis_data.get_data(key=str(request.from_user.id) + ':can_edit_seller_registration_data')

    if input_number and edit_mode=='true':
        await state.set_state(HybridSellerRegistrationStates.check_input_data)
        return await check_reg_config_module.check_your_config(request=request, state=state)

    if seller_mode == 'dealership':
        if incorrect:
            await state.update_data(incorrect_answer=True)
            await registartion_view_corrector(request=request, state=state)

            message_reply_mode = True
            await redis_module.redis_data.set_data(
                                        key=str(request.from_user.id) + ':last_user_message',
                                        value=request.message_id)
            lexicon_code = 'write_dealership_address' + incorrect
        else:
            await registartion_view_corrector(request=request, state=state)
            message_reply_mode=False
            lexicon_code = 'write_dealership_address'

        await message_editor_module.travel_editor.edit_message(request=request, lexicon_key=lexicon_code, reply_mode=message_reply_mode)
    else:
        await registartion_view_corrector(request=request, state=state)

    await state.set_state(HybridSellerRegistrationStates.check_input_data)
    
    if seller_mode == 'seller':
        await check_reg_config_module.check_your_config(request=request, state=state)

    print('this', await state.get_state())
    if isinstance(request, CallbackQuery):
        print('is', request.data)

    if not incorrect:
        try:
            await request.delete()
        except Exception:
            pass