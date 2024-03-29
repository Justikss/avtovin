import importlib
from typing import Dict

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from handlers.callback_handlers.admin_part.admin_panel_ui.bot_statistics.handle_tools.base_callbackquery_handler import \
    BaseStatisticCallbackHandler
from states.admin_part_states.statistics_states import StatisticsStates


class GeneralBotStatisticHandler(BaseStatisticCallbackHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        await self.set_state(state, StatisticsStates.general_bot_statistic)

        period, change_period_flag = await self.get_period_status(request)

        lexicon_part = await self.construct_statistic_view(period)

        self.output_methods = [
            self.menu_manager.travel_editor(
                lexicon_part=lexicon_part,
                dynamic_buttons=False
            )
        ]

        if change_period_flag:
            Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

            await self.send_alert_answer(request, Lexicon_module.ADMIN_LEXICON['information_was_updated'])


    async def get_period_status(self, request) -> tuple:
        if request.data == 'general_statistics':
            period = ''
            change_period_flag = None
        else:
            period = request.data.split(':')[-1]
            change_period_flag=True
        return period, change_period_flag



    async def construct_statistic_view(self, period) -> Dict[str, str | dict | int]:
        counts = await self.statistic_manager.calculate_statistics(period=period)
        period_string = await self.statistic_manager.ident_period_string(period)
        statistic_lexicon = await self.statistic_manager.statistic_lexicon()

        lexicon_part = statistic_lexicon['general_bot_statistics']

        lexicon_part['message_text'] = lexicon_part['message_text'].format(feedbacks=counts['feedback'],
                                                                           adverts=counts['advert'],
                                                                           period=period_string,
                                                                           users=counts['person'],
                                                                           sellers=counts['seller'],
                                                                           buyers=counts['user'],
                                                                           block_users=counts['block_users'],
                                                                           block_buyers=counts['block_buyers'],
                                                                           block_sellers=counts['block_sellers'])
        return lexicon_part