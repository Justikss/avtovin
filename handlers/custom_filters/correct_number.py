import importlib
import phonenumbers

from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, chat


from handlers.state_handlers.buyer_registration_handlers import input_phone_number



class CheckInputNumber(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext):
        redis_storage = importlib.import_module('utils.redis_for_language')  # Ленивый импорт
        seller_registration_module = importlib.import_module('handlers.state_handlers.seller_states_handler.seller_registration_handlers')
        edit_mode = await redis_storage.redis_data.get_data(key=str(message.from_user.id) + ':can_edit_seller_registration_data')

        
        current_state = str(await state.get_state())
        if current_state.startswith('HybridSellerRegistrationStates'):
            current_method = seller_registration_module.hybrid_input_seller_number
        elif current_state.startswith('BuyerRegistationStates'):
            current_method = input_phone_number

        phonenumber = message.text.strip()
        country = await redis_storage.redis_data.get_data(key=str(message.from_user.id) + ':language')
        try:
            parsed_number = phonenumbers.parse(phonenumber, country)
            valid_number = phonenumbers.is_valid_number(parsed_number)
        except phonenumbers.NumberParseException:
            valid_number = False

        if valid_number:
            formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)
            print('GOOOOOOOOO', formatted_number)
            return {'input_number': formatted_number}
        else:
            message_id = await redis_storage.redis_data.get_data(key=str(message.from_user.id) + ':last_message')
            if edit_mode == 'true':
                await chat.Chat.delete_message(self=message.chat, message_id=message_id)
            await current_method(request=message, state=state, incorrect=True)
            return False