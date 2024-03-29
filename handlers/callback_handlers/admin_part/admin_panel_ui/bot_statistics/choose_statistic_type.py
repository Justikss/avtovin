import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery


base_callback_query_module = importlib.import_module('utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler')
Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

class ChooseStatisticTypeHandler(base_callback_query_module\
                                 .BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):

        await self.clean_state(state)

        self.output_methods = [
            self.menu_manager.travel_editor(
                lexicon_part=Lexicon_module.STATISTIC_LEXICON['choose_statistic_type'],
                delete_mode=True
            )
        ]


