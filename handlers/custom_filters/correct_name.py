import importlib

from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, chat
import importlib

from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.choose_specific_user.choose_specific.input_name_to_search.start_input_name_request import \
    input_person_name_to_search_request_handler


class CheckInputName(BaseFilter):
    async def send_incorrect_flag(self, message, state, current_object, incorrect_flag):
        ic()

        ic(await state.update_data(incorrect_message=message.message_id))

        if current_object == input_person_name_to_search_request_handler and incorrect_flag == '(exists)':
            return {'user_name': message.text.strip()}
        else:
            await current_object(message, state=state, incorrect=incorrect_flag)

    async def __call__(self, message: Message, state: FSMContext):
        config_module = importlib.import_module('config_data.config')
        person_requester_module = importlib.import_module('database.data_requests.person_requests')
        input_full_name_module = importlib.import_module('handlers.state_handlers.buyer_registration_handlers')

        seller_registration_module = importlib.import_module('handlers.state_handlers.seller_states_handler.seller_registration.seller_registration_handlers')
        memory_storage = await state.get_data()
        redis_storage = importlib.import_module('utils.redis_for_language')  # Ленивый импорт
        message_id = await redis_storage.redis_data.get_data(key=str(message.from_user.id) + ':last_message')
        seller_use = False
        buyer_use = False
        seller_mode = await redis_storage.redis_data.get_data(key=str(message.from_user.id) + ':seller_registration_mode')
        dealership_mode = seller_mode == 'dealership'

        current_state = str(await state.get_state())
        if current_state.startswith('HybridSellerRegistrationStates'):
            current_object = seller_registration_module.input_seller_name
            seller_use = True
        elif current_state.startswith('BuyerRegistationStates'):
            current_object = input_full_name_module.input_full_name
            buyer_use = True
        elif current_state.endswith(('legal_entity_search', 'natural_entity_search', 'buyer_entity_search')):
            current_object = input_person_name_to_search_request_handler
            if current_state.endswith('buyer_entity_search'):
                buyer_use = True
            else:
                seller_use = True

        full_name = message.text
        if not dealership_mode:
            formatted_full_name = full_name.split(' ')
        elif dealership_mode:
            formatted_full_name = full_name

        if not dealership_mode and 1 < len(formatted_full_name) < 4 or dealership_mode and len(formatted_full_name) <= config_module.max_contact_info_len:
            for word in formatted_full_name:
                if not word.isalpha() and not dealership_mode or dealership_mode and not (word.isalpha() or word.isdigit() or word==' '):
                    try:
                        await chat.Chat.delete_message(self=message.chat, message_id=message_id)
                    except:
                        pass
                    ic()
                    return await self.send_incorrect_flag(message, state, current_object, '(novalid)')

            name_is_exists = await person_requester_module.PersonRequester.this_name_is_exists(name=full_name.strip(),
                                                                                               user=buyer_use,
                                                                                               seller=seller_use)
            if name_is_exists:
                await chat.Chat.delete_message(self=message.chat, message_id=message_id)
                ic()
                return await self.send_incorrect_flag(message, state, current_object, '(exists)')
            else:
                await state.update_data(incorrect_message=None)
                ic()
                return {'user_name': full_name}
        else:
            try:
                await chat.Chat.delete_message(self=message.chat, message_id=message_id)
            except:
                pass
            ic()
            return await self.send_incorrect_flag(message, state, current_object,'(novalid)')

            
