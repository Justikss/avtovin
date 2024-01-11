from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from handlers.callback_handlers.admin_part.admin_panel_ui.bot_statistics.handle_tools.base_callbackquery_handler import \
    BaseStatisticCallbackHandler
from states.admin_part_states.statistics_states import StatisticsStates


class StatisticsOutputMethodHandler(BaseStatisticCallbackHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        await self.set_state(state, StatisticsStates.accept_demand_output_method)
        self.output_methods = [
            self.menu_manager.travel_editor(
                lexicon_part=self.statistic_manager.lexicon['choose_statistics_output_method'],
                dynamic_buttons=2

            )
        ]
        ic()
        ic(request.data)
        await super().process_callback(request, state, **kwargs)
