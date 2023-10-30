import importlib
import phonenumbers

from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from typing import Union


from handlers.state_handlers.buyer_registration_handlers import input_phone_number
from database.data_requests.person_requests import PersonRequester


class GetDealershipAddress(BaseFilter):
    async def __call__(self, request: Union[Message, CallbackQuery], state: FSMContext):
        input_dealship_name_module = importlib.import_module('handlers.state_handlers.seller_states_handler.seller_registration.seller_registration_handlers')

        if isinstance(request, Message):
            word_flag = False
            for symbol in request.text:
                if symbol.isalpha():
                    return {'dealership_address': request.text}
            await input_dealship_name_module.dealership_input_address(request=request, state=state, incorrect='(novalid)')
        else:
            return True