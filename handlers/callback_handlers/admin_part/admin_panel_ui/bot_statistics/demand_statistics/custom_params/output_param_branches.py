from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from handlers.callback_handlers.admin_part.admin_panel_ui.bot_statistics.demand_statistics.custom_params.choose_period import \
    CustomParamsChoosePeriod
from handlers.callback_handlers.admin_part.admin_panel_ui.bot_statistics.demand_statistics.top_ten_display import \
    TopTenByDemandDisplayHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.bot_statistics.handle_tools.base_callbackquery_handler import \
    BaseStatisticCallbackHandler
from utils.lexicon_utils.Lexicon import LEXICON


class OutputStatisticAdvertParamsHandler(BaseStatisticCallbackHandler):
    async def callback_handler(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        async with self.idle_callback_answer(request):
            await self.set_state(state, self.statistic_manager.states.CustomParams.review_process)
            if request.data.startswith('custom_demand_param:'):
                pagination_data = await self.get_pagination_data(request, state)
                if pagination_data:
                    self.output_methods = [
                        self.menu_manager.admin_simple_pagination(
                            pagination_data=pagination_data
                        )
                    ]

    async def get_pagination_data(self, request: Message | CallbackQuery, state: FSMContext):
        memory_storage = await state.get_data()
        stats_period = memory_storage.get('stats_period')
        chosen_demand_params = memory_storage.get('chosen_demand_params')
        calculate_method = memory_storage.get('calculate_method')
        if chosen_demand_params:
            get_statistic_method_kwargs = {
                'engine_id': chosen_demand_params.get('engine'),
                'brand_id': chosen_demand_params.get('brand'),
                'model_id': chosen_demand_params.get('model'),
                'complectation_id': chosen_demand_params.get('complectation'),
                'color_id': chosen_demand_params.get('color')}
        else:
            await self.send_alert_answer(request, LEXICON['non_actiallity'])
            await CustomParamsChoosePeriod().callback_handler(request, state)
            return

        models_range = await self.statistic_manager.database_requests.get_statistics_by_params(
            calculate_method, period=stats_period, **get_statistic_method_kwargs
        )

        if models_range:
            pagination_data = []
            for index, feedback in enumerate(models_range):
                pagination_data.append(f'{feedback.id}:{index+1}')
            return pagination_data


    async def get_output_part(self, request, state, admin_pagination_object, data_to_output, message_editor):
        top_position = data_to_output.split(':')[-1]
        feedback_id = data_to_output.split(':')[0]
        lexicon_part = self.statistic_manager.lexicon['review_custom_stats_branches']
        feedback_model =
        message_text = TopTenByDemandDisplayHandler().construct_lexicon_part(state, top_position, )
        if message_text:
            memory_storage = await state.get_data()

            media_group = memory_storage.get('media_group_for_inline_pg')
            lexicon_part['message_text'] = message_text
            lexicon_part['buttons']['page_counter'] = lexicon_part['buttons']['page_counter'].format(
                start=admin_pagination_object.current_page,
                end=admin_pagination_object.total_pages
            )

            await message_editor.travel_editor.edit_message(request=request, lexicon_key='', lexicon_part=lexicon_part,
                                                            media_group=media_group, dynamic_buttons=2)

        else:
            await self.send_alert_answer(request, LEXICON['non_actiallity'])
            await CustomParamsChoosePeriod().callback_handler(request, state)
            return
