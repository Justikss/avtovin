import importlib

from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, chat
from handlers.state_handlers.seller_states_handler.seller_registration_handlers import input_seller_name
from handlers.state_handlers.buyer_registration_handlers import input_full_name


class CheckInputName(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext):
        memory_storage = await state.get_data()
        redis_storage = importlib.import_module('utils.redis_for_language')  # Ленивый импорт
        message_id = await redis_storage.redis_data.get_data(key=str(message.from_user.id) + ':last_message')

        seller_mode = await redis_storage.redis_data.get_data(key=str(message.from_user.id) + ':seller_registration_mode')
        dealership_mode = seller_mode == 'dealership'

        current_state = str(await state.get_state())
        if current_state.startswith('HybridSellerRegistrationStates'):
            current_object = input_seller_name
        elif current_state.startswith('BuyerRegistationStates'):
            current_object = input_full_name

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
                    return await current_object(request=message, state=state, incorrect=True)
            # await redis_storage.redis_data.delete_key(key=str(message.from_user.id) + ':last_user_message')
            return {'user_name': full_name}
        else:
            await chat.Chat.delete_message(self=message.chat, message_id=message_id)
            return await current_object(request=message, state=state, incorrect=True)
            
