import importlib

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from handlers.callback_handlers.admin_part.admin_panel_ui.catalog.advert_parameters.advert_parameters__second_hand_state_handlers.choose_parameter_type import \
    BaseCallbackQueryHandler

# from utils.oop_handlers_engineering.update_handlers.base_objects.utils_objects.incorrect_adapter import IncorrectAdapter

message_editor_module = importlib.import_module('handlers.message_editor')
Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

class ChooseMailingAction(BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        await self.incorrect_manager.try_delete_incorrect_message(request, state)
            # await IncorrectAdapter().try_delete_incorrect_message(callback, state)
        if await state.get_state():
            await state.clear()
        lexicon_part = Lexicon_module.ADVERT_LEXICON['choose_mailing_action']
        await message_editor_module.travel_editor.edit_message(request=request, lexicon_key='', lexicon_part=lexicon_part,
                                                               delete_mode=True)



# async def request_choose_mailing_action(callback: types.CallbackQuery, state: FSMContext):
