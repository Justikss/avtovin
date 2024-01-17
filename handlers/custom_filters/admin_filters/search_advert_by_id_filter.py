import importlib

from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.car_catalog_review.search_advert_by_id.input_advert_id_for_search import \
    input_advert_id_for_search_admin_handler
from handlers.callback_handlers.admin_part.admin_panel_ui.tariff_actions.input_data_utils.memory_storage_incorrect_controller import \
    incorrect
from handlers.utils.delete_message import delete_message

car_advert_requests_module = importlib.import_module('database.data_requests.car_advert_requests')

class InputAdvertIdFilter(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext) -> bool | dict:
        config_module = importlib.import_module('config_data.config')
        ic(str(await state.get_state()))
        ic(InputAdvertIdFilter)
        message_text = message.text.strip()
        memory_storage = await state.get_data()
        last_admin_answer = memory_storage.get('last_admin_answer')

        if last_admin_answer:
            await delete_message(message, last_admin_answer)


        if message_text.isdigit() and len(str(message.text)) < config_module.max_price_len:
            ic()
            advert_model = await car_advert_requests_module\
                .AdvertRequester.get_where_id(message_text)
            if advert_model:
                ic()
                await delete_message(message, message.message_id)
                return {'advert_model': advert_model}
            else:
                incorrect_flag = '(not_exists)'
        else:
            incorrect_flag = '(digit)'

        await incorrect(state, message.message_id)
        # await delete_message(message, message.message_id)
        return await input_advert_id_for_search_admin_handler(message, state, incorrect=incorrect_flag)
