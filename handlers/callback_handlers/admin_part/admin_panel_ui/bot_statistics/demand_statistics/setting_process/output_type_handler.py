from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from handlers.callback_handlers.admin_part.admin_panel_ui.bot_statistics.demand_statistics.custom_params.choose_param_handler import \
    ChooseParamToDemandStatsHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.bot_statistics.demand_statistics.setting_process.choose_period import \
    CustomParamsChoosePeriod
from handlers.callback_handlers.admin_part.admin_panel_ui.bot_statistics.demand_statistics.top_ten_display import \
    TopTenByDemandDisplayHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.bot_statistics.handle_tools.base_callbackquery_handler import \
    BaseStatisticCallbackHandler
from utils.lexicon_utils.Lexicon import statistic_captions


class DemandOutputSplitterHandler(BaseStatisticCallbackHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        ic()
        if not await self.accept_period_method(request, state):
            return


        await self.split_by_output_method(request, state)

        await super().process_callback(request, state, **kwargs)
        return



    async def split_by_output_method(self, request: Message | CallbackQuery, state: FSMContext):
        memory_storage = await state.get_data()
        output_method = memory_storage.get('output_method')
        ic()
        ic(output_method)
        match output_method:
            case 'top_ten':
                statistic_lexicon = await self.statistic_manager.statistic_lexicon()

                await self.send_alert_answer(request, statistic_lexicon['stats_loading'])
                await TopTenByDemandDisplayHandler().callback_handler(request, state)

            case 'individual':
                await ChooseParamToDemandStatsHandler().callback_handler(request, state)

    async def accept_period_method(self, request: Message | CallbackQuery, state: FSMContext):
        if request.data.startswith('select_bot_statistic_period:'):
            period = request.data.split(':')[-1]
            memory_storage = await state.get_data()
            calculate_method = memory_storage.get('calculate_method')
            models_range = await self.statistic_manager.database_requests.get_top_advert_parameters(
                top_direction=calculate_method, period=period
            )
            if not models_range:
                statistic_lexicon = await self.statistic_manager.statistic_lexicon()
                await self.send_alert_answer(request, statistic_lexicon['stats_is_empty'].format(
                    for_current_period=statistic_captions['for_current_period']
                ), message=True)
                await CustomParamsChoosePeriod().callback_handler(request, state)
                return False# await self.send_alert_answer(request, Lexicon_module.LEXICON['non_actiallity'])

            await state.update_data(stats_period=period)
        return True

