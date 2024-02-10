import importlib

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.data_requests.advert_parameters_requests import AdvertParameterManager
from handlers.callback_handlers.admin_part.admin_panel_ui.bot_statistics.demand_statistics.setting_process.choose_period import \
    CustomParamsChoosePeriod
from handlers.callback_handlers.admin_part.admin_panel_ui.bot_statistics.demand_statistics.top_ten_display import \
    TopTenByDemandDisplayHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.bot_statistics.handle_tools.base_callbackquery_handler import \
    BaseStatisticCallbackHandler

Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')


class OutputStatisticAdvertParamsHandler(BaseStatisticCallbackHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        ic()
        ic()
        # async with self.idle_callback_answer(request):
        await self.set_state(state, self.statistic_manager.states.CustomParams.review_process)

        if isinstance(request, CallbackQuery):
            if not (request.data.startswith('custom_demand_param:') or request.data == 'output_current_demand_stats'):
                return
        elif isinstance(request, Message):
            pass
        statistic_lexicon = await self.statistic_manager.statistic_lexicon()
        if not kwargs.get('test'):
            await self.send_alert_answer(request, statistic_lexicon['stats_loading'])
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
        ic(chosen_demand_params)
        if chosen_demand_params:
            get_statistic_method_kwargs = {
                'engine_id': chosen_demand_params.get('engine'),
                'brand_id': chosen_demand_params.get('brand'),
                'model_id': chosen_demand_params.get('model'),
                'complectation_id': chosen_demand_params.get('complectation'),
                'color_id': chosen_demand_params.get('color')
            }

        else:
            await self.send_alert_answer(request, Lexicon_module.LEXICON['non_actiallity'])
            await CustomParamsChoosePeriod().callback_handler(request, state)
            return

        models_range = await self.statistic_manager.database_requests.get_statistics_by_params(
            calculate_method, period=stats_period, **get_statistic_method_kwargs, for_output=True
        )
        ic(stats_period, calculate_method, models_range)
        if models_range:
            # person_requests_module = importlib.import_module('database.data_requests.person_requests')

            pagination_data = []
            for index, feedback in enumerate(models_range):
                # advert_parameters = await AdvertParameterManager.get_by_id(feedback.advert_parameters)
                # seller_model = await person_requests_module.PersonRequester.get_user_for_id(feedback.seller_id,
                #                                                                             seller=True)
                pagination_data.append(f'{feedback.count}:{feedback.seller_id.telegram_id}:{feedback.advert_parameters.id}:{index+1}')
            # ic(pagination_data)
            return pagination_data


    async def get_output_part(self, request, state, admin_pagination_object, data_to_output, message_editor):
        person_requests_module = importlib.import_module('database.data_requests.person_requests')
        car_advert_requests_module = importlib.import_module('database.data_requests.car_advert_requests')

        data_to_output = data_to_output[0]

        feedback_count = data_to_output.split(':')[0]
        seller_id = data_to_output.split(':')[1]
        advert_parameters_id = data_to_output.split(':')[2]
        top_position = data_to_output.split(':')[-1]
        statistic_lexicon = await self.statistic_manager.statistic_lexicon()

        # feedback_id = data_to_output.split(':')[0]
        lexicon_part = statistic_lexicon['review_custom_stats_branches']
        advert_parameters_model = await AdvertParameterManager.get_by_id(advert_parameters_id)
        advert_parameters_model = await car_advert_requests_module.AdvertRequester.load_related_data_for_advert(advert_parameters_model)
        seller_model = await person_requests_module\
                .PersonRequester.get_user_for_id(seller_id, seller=True)
        ic(data_to_output)
        if seller_model and advert_parameters_model:
            class Feedback:
                seller_id = seller_model[0]
                advert_parameters = advert_parameters_model
                count = feedback_count
            message_text = await TopTenByDemandDisplayHandler().construct_lexicon_part(state, top_position,
                                                                                       Feedback,
                                                                                       only_message_text=True)
            ic(message_text)
            if message_text:
                message_text = '\n'.join(message_text.split('\n'))
                memory_storage = await state.get_data()
                media_group = memory_storage.get('media_group_for_inline_pg')

                lexicon_part['message_text'] = message_text

                lexicon_part['buttons']['page_counter'] = lexicon_part['buttons']['page_counter'].format(
                    start=admin_pagination_object.current_page,
                    end=admin_pagination_object.total_pages
                )

                await message_editor.travel_editor.edit_message(request=request, lexicon_key='', lexicon_part=lexicon_part,
                                                                media_group=media_group, dynamic_buttons=2, delete_mode=not media_group)
                return

        await self.send_alert_answer(request, Lexicon_module.LEXICON['non_actiallity'])
        await CustomParamsChoosePeriod().callback_handler(request, state)
        return
