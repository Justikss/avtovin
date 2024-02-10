import asyncio
import importlib
import phonenumbers
from typing import Union
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from states.seller_registration_states import HybridSellerRegistrationStates, PersonSellerRegistrationStates, CarDealerShipRegistrationStates



async def input_seller_name(request: Union[CallbackQuery, Message], state: FSMContext, incorrect = None, from_backward_Delete_mode=None):
    message_editor_module = importlib.import_module('handlers.message_editor')
    redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт
    buyer_registration_handlers_module = importlib.import_module('handlers.state_handlers.buyer_registration_handlers')
    delete_mode = False
    seller_mode = await redis_module.redis_data.get_data(key=str(request.from_user.id) + ':seller_registration_mode')

    if not await state.get_state():
        if seller_mode == 'dealership':
            await state.set_state(CarDealerShipRegistrationStates.input_dealship_name)
        elif seller_mode == 'person':
            await state.set_state(PersonSellerRegistrationStates.input_fullname)

    if not await state.get_state():
        await state.set_state(PersonSellerRegistrationStates.input_fullname)

    travel_object = request

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
            
        await buyer_registration_handlers_module.registartion_view_corrector(request=request, state=state)

        await redis_module.redis_data.set_data(
            key=str(request.from_user.id) + ':last_user_message',
            value=request.message_id)
    else:
        if seller_mode == 'dealership':
            lexicon_code = 'write_dealership_name'
        elif seller_mode == 'person':
            lexicon_code = 'write_full_seller_name'

        message_reply_mode = False

    if from_backward_Delete_mode:
        # from keyboards.reply.delete_reply_markup import delete_reply_markup
        # await delete_reply_markup(request)
        delete_mode = from_backward_Delete_mode

    await message_editor_module.travel_editor.edit_message(request=travel_object, lexicon_key=lexicon_code, lexicon_cache=False,
                                                            reply_mode=message_reply_mode, delete_mode=delete_mode)
    await state.set_state(HybridSellerRegistrationStates.input_number)
    

#Фильтр CorrectName()
async def hybrid_input_seller_number(request: Union[CallbackQuery, Message], state: FSMContext, user_name=None, incorrect = None, from_backward_Delete_mode=None):
    message_editor_module = importlib.import_module('handlers.message_editor')
    redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт
    buyer_registration_handlers_module = importlib.import_module('handlers.state_handlers.buyer_registration_handlers')
    check_reg_config_module = importlib.import_module('handlers.state_handlers.seller_states_handler.seller_registration.check_your_registration_config')
    Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
    if isinstance(request, CallbackQuery):
        ic(request.data)
    if user_name:
        user_name = ' '.join([name_part.capitalize() for name_part in user_name.split(' ')])
        await state.update_data(seller_name=user_name)

    travel_object = request
    lexicon_part = Lexicon_module\
        .LEXICON['write_seller_phone_number']

    if isinstance(request, CallbackQuery):
        message = request.message
    elif isinstance(request, Message):
        message = request

    edit_mode = await redis_module.redis_data.get_data(key=str(request.from_user.id) + ':can_edit_seller_registration_data')
    if user_name and edit_mode == 'true':
        await state.set_state(HybridSellerRegistrationStates.check_input_data)
        return await check_reg_config_module.check_your_config(request=request, state=state)
    
    bot = message.chat.bot

    if incorrect:
        await state.update_data(incorrect_answer=True)
        lexicon_part['message_text'] = Lexicon_module\
            .LEXICON[f'write_seller_phone_number{incorrect}']
        message_reply_mode = True

        delete_last_message_mode = False
        if edit_mode == 'true': 
            delete_mode = False
        else:
            delete_mode = True
        await buyer_registration_handlers_module.registartion_view_corrector(request=request, state=state, delete_mode=delete_mode)

        await redis_module.redis_data.set_data(
            key=str(request.from_user.id) + ':last_user_message',
            value=message.message_id)
        
    else:
        redis_key = str(request.from_user.id) + ':last_user_message'
        try:
            last_user_message = await redis_module.redis_data.get_data(key=redis_key)
        except TelegramBadRequest:
            pass
        from handlers.utils.delete_message import delete_message

        if last_user_message:
            await delete_message(message, last_user_message)

            await redis_module.redis_data.delete_key(key=redis_key)

        await delete_message(message, message.message_id)

        message_reply_mode = False


    from keyboards.reply.send_reply_markup import send_reply_button_contact
    if isinstance(request, Message):
        await send_reply_button_contact(message)


    await message_editor_module.travel_editor.edit_message(request=travel_object, lexicon_key='', lexicon_part=lexicon_part,
                                                             reply_mode = message_reply_mode, delete_mode=True)


    await state.set_state(CarDealerShipRegistrationStates.input_dealship_name)



async def dealership_input_address(request: Union[CallbackQuery, Message], state: FSMContext, input_number=None, incorrect=None):

    buyer_registration_handlers_module = importlib.import_module('handlers.state_handlers.buyer_registration_handlers')
    message_editor_module = importlib.import_module('handlers.message_editor')
    redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт
    check_reg_config_module = importlib.import_module('handlers.state_handlers.seller_states_handler.seller_registration.check_your_registration_config')

    if incorrect:
        delete_mode = True
    else:
        delete_mode = False

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
            await buyer_registration_handlers_module.registartion_view_corrector(request=request, state=state, delete_mode=delete_mode )

            message_reply_mode = True
            message_delete_mode = False
            await redis_module.redis_data.set_data(
                                        key=str(request.from_user.id) + ':last_user_message',
                                        value=request.message_id)
            lexicon_code = 'write_dealership_address' + incorrect
        else:
            await buyer_registration_handlers_module.registartion_view_corrector(request=request, state=state, delete_mode=delete_mode )
            message_delete_mode = True
            message_reply_mode = False
            lexicon_code = 'write_dealership_address'

        await message_editor_module.travel_editor.edit_message(request=request, lexicon_key=lexicon_code, reply_mode=message_reply_mode, delete_mode=message_delete_mode)
    else:
        await buyer_registration_handlers_module.registartion_view_corrector(request=request, state=state, delete_mode=True)
        await check_reg_config_module.check_your_config(request=request, state=state)
    await state.set_state(HybridSellerRegistrationStates.check_input_data)
    
    # if seller_mode == 'seller':
    #     await check_reg_config_module.check_your_config(request=request, state=state)



    if not incorrect:
        try:
            await request.delete()
        except Exception:
            pass