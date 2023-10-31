import importlib

from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, chat
import importlib

from handlers.state_handlers.buyer_registration_handlers import input_full_name
from database.data_requests.person_requests import PersonRequester


class CheckInputName(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext):
        print('iamcorrect_name')
        seller_registration_module = importlib.import_module('handlers.state_handlers.seller_states_handler.seller_registration.seller_registration_handlers')
        memory_storage = await state.get_data()
        redis_storage = importlib.import_module('utils.redis_for_language')  # Ленивый импорт
        message_id = await redis_storage.redis_data.get_data(key=str(message.from_user.id) + ':last_message')

        seller_mode = await redis_storage.redis_data.get_data(key=str(message.from_user.id) + ':seller_registration_mode')
        dealership_mode = seller_mode == 'dealership'

        current_state = str(await state.get_state())
        if current_state.startswith('HybridSellerRegistrationStates'):
            current_object = seller_registration_module.input_seller_name
            buyer_use = None
            seller_use = True
        elif current_state.startswith('BuyerRegistationStates'):
            current_object = input_full_name
            seller_use = None
            buyer_use = True

        full_name = message.text
        if not dealership_mode:
            formatted_full_name = full_name.split(' ')
        elif dealership_mode:
            formatted_full_name = full_name


        print('correct_name,', dealership_mode, seller_mode)
        if not dealership_mode and 1 < len(formatted_full_name) < 4 or dealership_mode and len(formatted_full_name) <= 250:
            for word in formatted_full_name:
                if not word.isalpha() and not dealership_mode or dealership_mode and not (word.isalpha() or word.isdigit() or word==' '):
                    await chat.Chat.delete_message(self=message.chat, message_id=message_id)
                    return await current_object(request=message, state=state, incorrect='(novalid)')
            # await redis_storage.redis_data.delete_key(key=str(message.from_user.id) + ':last_user_message')
            print('drop_name', full_name)

            
            name_is_exists = PersonRequester.this_name_is_exists(name=full_name.strip(), user=buyer_use, seller=seller_use)
            if name_is_exists:
                await chat.Chat.delete_message(self=message.chat, message_id=message_id)
                return await current_object(request=message, state=state, incorrect='(exists)')
            else:
                return {'user_name': full_name}
        else:
            await chat.Chat.delete_message(self=message.chat, message_id=message_id)
            return await current_object(request=message, state=state, incorrect='(novalid)')
            
