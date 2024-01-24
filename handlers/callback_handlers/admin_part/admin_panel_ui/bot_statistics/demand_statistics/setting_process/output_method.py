from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from handlers.callback_handlers.admin_part.admin_panel_ui.bot_statistics.handle_tools.base_callbackquery_handler import \
    BaseStatisticCallbackHandler
from states.admin_part_states.statistics_states import StatisticsStates


class StatisticsOutputMethodHandler(BaseStatisticCallbackHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        statistic_lexicon = await self.statistic_manager.statistic_lexicon()

        if await self.statistic_manager.database_requests.statistic_is_exists():

            await self.set_state(state, StatisticsStates.accept_demand_output_method)

            self.output_methods = [
                self.menu_manager.travel_editor(
                    lexicon_part=statistic_lexicon['choose_statistics_output_method'],
                    dynamic_buttons=1

                )
            ]
            ic()
            ic(request.data)
            await super().process_callback(request, state, **kwargs)
        else:
            await self.send_alert_answer(request, statistic_lexicon['stats_is_empty'].format(for_current_period=''))
            return


