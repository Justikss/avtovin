from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from handlers.callback_handlers.admin_part.admin_panel_ui.bot_statistics.handle_tools.base_callbackquery_handler import \
    BaseStatisticCallbackHandler



class CustomParamsChoosePeriod(BaseStatisticCallbackHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        async with self.idle_callback_answer(request):
            await self.set_state(state, self.statistic_manager.states.CustomParams.choose_period)

            self.output_methods = [
                self.menu_manager.travel_editor(
                    lexicon_part=self.statistic_manager.lexicon['custom_params_period'],
                    dynamic_buttons=2
                )
            ]