from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.data_requests.car_configurations_requests import CarConfigs
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.parameters_ouptut.output_specific_parameters import \
    OutputSpecificAdvertParameters
from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.utils.add_new_value_advert_parameter.add_new_value_advert_parameter import \
    AddNewValueAdvertParameter
from utils.lexicon_utils.admin_lexicon.admin_lexicon import captions
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler

class ConfirmAddNewValueOfAdvertParameter(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        # self.output_methods = [
        #     OutputSpecificAdvertParameters().callback_handler
        # ]
        memory_storage = await state.get_data()
        insert_query = await CarConfigs.custom_action(mode=memory_storage.get('admin_chosen_advert_parameter'),
                                       name=memory_storage.get('current_value'),
                                       action='insert')
        if insert_query == '(exists)':
            await AddNewValueAdvertParameter().callback_handler(request, state, incorrect=insert_query)
            await super().process_callback(request, state, **kwargs)
        else:
            ic()
            await self.send_alert_answer(request, captions['successfully'])
            ic()
            await OutputSpecificAdvertParameters().callback_handler(request, state)#

