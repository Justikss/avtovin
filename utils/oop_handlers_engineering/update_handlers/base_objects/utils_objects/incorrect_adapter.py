import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from handlers.callback_handlers.admin_part.admin_panel_ui.tariff_actions.input_data_utils.memory_storage_incorrect_controller import \
    get_incorrect_flag
from handlers.utils.delete_message import delete_message


class IncorrectAdapter:
    async def get_incorrect_flag(self, state: FSMContext):
        return ic(await get_incorrect_flag(state))

    async def get_last_incorrect_message_id(self, state: FSMContext, message: Message = None, mode='admin'):
        memory_storage = await state.get_data()
        last_answer = None
        match mode:
            case 'admin':
                storage_key = 'last_admin_answer'
                last_answer = ic(memory_storage.get(storage_key))
            case 'buyer':
                redis_module = importlib.import_module('utils.redis_for_language')
                redis_key_user_message = str(message.from_user.id) + ':last_seller_message'
                last_answer = await redis_module.redis_data.get_data(key=redis_key_user_message)
                # if last_answer:
                #     await redis_module.redis_data.delete_key(key=redis_key_user_message)

        return last_answer

    async def get_lexicon_part_in_view_of_incorrect(self, lexicon_key, lexicon_object, incorrect, state: FSMContext) -> dict:
        ic(incorrect)
        ic()
        lexicon_part = lexicon_object[lexicon_key]
        ic(lexicon_part)
        if incorrect:
            if incorrect is True:
                incorrect_message_text = lexicon_object[f"{lexicon_key}(incorrect)"]
            else:
                incorrect_message_text = lexicon_object[f"{lexicon_key}{incorrect}"]

            lexicon_part['message_text'] = incorrect_message_text
        ic(lexicon_part)

        memory_storage = await state.get_data()
        if memory_storage.get('params_type_flag') == 'new':
            lexicon_part = await self.get_lexicon_part_with_blockquote_of_translating(lexicon_part, state)
        return lexicon_part
    async def get_lexicon_part_with_blockquote_of_translating(self, lexicon_part, state):
        new_car_state_parameters_module = importlib.import_module(
            'handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__new_state_handlers.new_car_state_parameters_handler')

        current_parameter_name, current_parameter_value = await new_car_state_parameters_module \
            .NewCarStateParameters().get_last_selected_param(state)
        ic(current_parameter_name, current_parameter_value)
        if current_parameter_name not in ('mileage', 'year', 'color'):
            parameters = ['state', 'engine', 'brand', 'model', 'complectation', 'color']
            current_parameter_name = parameters[parameters.index(current_parameter_name) + 1]

            if current_parameter_name in ('complectation', 'color'):
                from utils.lexicon_utils.admin_lexicon.advert_parameters_lexicon import advert_params_class_lexicon

                lexicon_part['message_text'] += advert_params_class_lexicon['translate_param_caption']

        return lexicon_part

    async def try_delete_incorrect_message(self, request, state):
        if await self.get_incorrect_flag(state):
            await delete_message(request, await self.get_last_incorrect_message_id(state))

