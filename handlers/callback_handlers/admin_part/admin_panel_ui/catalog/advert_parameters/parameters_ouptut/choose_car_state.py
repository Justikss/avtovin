import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler

Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')


class ChooseStateAddNewParamsHandler(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        await state.clear()
        lexicon_part = Lexicon_module.ADVERT_PARAMETERS_LEXICON['choose_state']
        self.output_methods = [
            self.menu_manager.travel_editor(
                lexicon_part=lexicon_part,
                dynamic_buttons=3
            )
        ]
        pass

