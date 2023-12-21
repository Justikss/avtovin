import importlib
import re

import phonenumbers

from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, chat

from database.data_requests.person_requests import PersonRequester


class CheckInputNumber(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext):
        input_phone_number_module = importlib.import_module('handlers.state_handlers.buyer_registration_handlers')
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
            current_method = input_phone_number_module.input_phone_number
            buyer_use = True
            seller_use = None

        phonenumber = message.text.strip().replace(' ', '')
        country = await redis_storage.redis_data.get_data(key=str(message.from_user.id) + ':language')

        formatted_number = await self.format_and_validate_phone_number(phonenumber)
        if formatted_number:

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

            print('last_valid_number')
            return False
        
        print('flew by', number_is_exists)


    @staticmethod
    async def format_and_validate_phone_number(phone_number):
        # Регулярное выражение для проверки номера телефона
        pattern = r'^(\+?7\d{10}|8\d{10}|\+?998\d{9}|998\d{9}|9\d{8})$'

        if re.match(pattern, phone_number):
            # Форматирование номера
            if phone_number.startswith('8'):
                formatted_number = '+7' + phone_number[1:]
            elif phone_number.startswith('9') and len(phone_number) == 9:
                # Форматирование локального узбекского номера
                return re.sub(r"(9\d{1})(\d{3})(\d{2})(\d{2})", r"\1-\2-\3-\4", phone_number)
            elif not phone_number.startswith('+'):
                formatted_number = '+' + phone_number
            else:
                formatted_number = phone_number

            # Добавление дефисов для разделения цифр
            if formatted_number.startswith('+7'):
                return re.sub(r"(\+7)(\d{3})(\d{3})(\d{2})(\d{2})", r"\1-\2-\3-\4-\5", formatted_number)
            elif formatted_number.startswith('+998'):
                return re.sub(r"(\+998)(\d{2})(\d{3})(\d{2})(\d{2})", r"\1-\2-\3-\4-\5", formatted_number)
        else:
            return False