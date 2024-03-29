import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from utils.oop_handlers_engineering.update_handlers.base_objects.base_handler import TravelMessageEditorInit
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler\
    import BaseCallbackQueryHandler

Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')


class ChooseSecondHandAdvertParametersType(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):

        await self.incorrect_manager.try_delete_incorrect_message(request, state)

        await state.update_data(params_type_flag='second_hand')
        self.output_methods = [
            TravelMessageEditorInit(
                lexicon_part=Lexicon_module.ADVERT_PARAMETERS_LEXICON['choose_second_hand_parameter_type'],
                dynamic_buttons=2
            )
        ]
