import importlib
import phonenumbers

from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, chat


from handlers.state_handlers.buyer_registration_handlers import input_phone_number
from database.data_requests.person_requests import PersonRequester


class CheckInputNumber(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext):
        print('in_number_filter')
        redis_storage = importlib.import_module('utils.redis_for_language')  # Ленивый импорт
        seller_registration_module = importlib.import_module('handlers.state_handlers.seller_states_handler.seller_registration.seller_registration_handlers')
        edit_mode = await redis_storage.redis_data.get_data(key=str(message.from_user.id) + ':can_edit_seller_registration_data')
        message_id = await redis_storage.redis_data.get_data(key=str(message.from_user.id) + ':last_message')

        
        current_state = str(await state.get_state())
        if current_state.startswith('CarDealerShipRegistrationStates'):
            current_method = seller_registration_module.hybrid_input_seller_number
            buyer_use = None
            seller_use = True

        elif current_state.startswith('BuyerRegistationStates'):
            current_method = input_phone_number
            buyer_use = True
            seller_use = None

        phonenumber = message.text.strip()
        country = await redis_storage.redis_data.get_data(key=str(message.from_user.id) + ':language')
        try:
            if not country:
                country = 'ru'
            parsed_number = phonenumbers.parse(phonenumber, country)
            valid_number = phonenumbers.is_valid_number(parsed_number)
        except phonenumbers.NumberParseException as ex:
            print(ex)
            valid_number = False

        if valid_number:
            ic(parsed_number)
            formatted_number = '-'.join(phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL).split())
            ic(formatted_number)

            number_is_exists = await PersonRequester.this_number_is_exists(formatted_number, user=buyer_use, seller=seller_use)
            if number_is_exists:
                print('number_is_exists', number_is_exists)
                await chat.Chat.delete_message(self=message.chat, message_id=message_id)

                if current_state.startswith('CarDealerShipRegistrationStates'):
                    await current_method(request=message, state=state, incorrect='(exists)')
                elif current_state.startswith('BuyerRegistationStates'):
                    await current_method(message=message, state=state, incorrect='(exists)')


                return False
                
            return {'input_number': formatted_number}

        else:
            if edit_mode == 'true':
                await chat.Chat.delete_message(self=message.chat, message_id=message_id)

            if current_state.startswith('CarDealerShipRegistrationStates'):
                await current_method(request=message, state=state, incorrect='(novalid)')
            elif current_state.startswith('BuyerRegistationStates'):
                await current_method(message=message, state=state, incorrect='(novalid)')

            print('last_valid_number', valid_number)
            return False
        
        print('flew by', number_is_exists, valid_number)