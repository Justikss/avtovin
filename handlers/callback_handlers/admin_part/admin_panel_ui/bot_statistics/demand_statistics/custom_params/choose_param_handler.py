import importlib
from copy import copy, deepcopy

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery


from handlers.callback_handlers.admin_part.admin_panel_ui.bot_statistics.demand_statistics.custom_params.output_param_branches import \
    OutputStatisticAdvertParamsHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.bot_statistics.handle_tools.base_callbackquery_handler import \
    BaseStatisticCallbackHandler
from utils.lexicon_utils.admin_lexicon.bot_statistics_lexicon import ChooseCustomParamsToStats

Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')


class ChooseParamToDemandStatsHandler(BaseStatisticCallbackHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        # async with self.idle_callback_answer(request):
        memory_storage = await state.get_data()

        await self.set_state(state, self.statistic_manager.states.CustomParams.choose_params) \
                                                        and request.data.startswith('select_bot_statistic_period:')


        chosen_params, chosen_param_name = await self.try_extract_inputted_data(request, state, memory_storage)
        ic(chosen_params, chosen_param_name)
        if all(value is None for value in (chosen_params, chosen_param_name)):
            return
        param_to_output = await self.get_choose_data(request, state, chosen_param_name)
        ic(param_to_output)
        if not param_to_output:
            self.output_methods = []
            return
        ic()
        memory_storage = await state.get_data()

        lexicon_class = await self.get_lexicon_class(request, state, memory_storage, chosen_params, param_to_output)
        if not lexicon_class:
            self.output_methods = []
            return
        config_module = importlib.import_module('config_data.config')


        # ic(lexicon_class.__dict__)
        self.output_methods = [
            self.menu_manager.inline_pagination(
                lexicon_class=lexicon_class,
                models_range=await self.get_models_range(state, memory_storage),
                page_size=config_module.admin_brand_pagination_pagesize
            )
        ]



    async def try_extract_inputted_data(self, request: Message | CallbackQuery, state: FSMContext,
                                        memory_storage):
        # if chosen_params:
        #     if param_to_output not in chosen_params:
        chosen_params = memory_storage.get('chosen_demand_params')
        if not chosen_params:
            chosen_params = {}
        # chosen_param_name = None

        chosen_param_name = await self.get_last_chosen_param(request, state,
                                                             get_next_param=not request.data.startswith('admin_backward:')
                                                             )
        if not chosen_param_name:
            chosen_param_name = 'engine'
        elif chosen_param_name == 'exit':
            return None, None

        if request.data.startswith('custom_demand_param:'):
            chosen_param_id = int(request.data.split(':')[-1])
            ic(chosen_param_name, chosen_param_id)
            chosen_params = {**chosen_params, chosen_param_name: chosen_param_id}
            await state.update_data(chosen_demand_params=chosen_params)

        return chosen_params, chosen_param_name

    async def get_models_range(self, state: FSMContext, memory_storage):
        calculate_method = memory_storage.get('calculate_method')
        chosen_demand_params = memory_storage.get('chosen_demand_params')
        if chosen_demand_params:
            get_statistic_method_kwargs = {
                'engine_id': chosen_demand_params.get('engine'),
                'brand_id': chosen_demand_params.get('brand'),
                'model_id': chosen_demand_params.get('model'),
                'complectation_id': chosen_demand_params.get('complectation'),
                'color_id': chosen_demand_params.get('color')}
        else:
            get_statistic_method_kwargs = {}
        models_range = await self.statistic_manager.database_requests.get_statistics_by_params(
            calculate_method, period=memory_storage.get('stats_period'), **get_statistic_method_kwargs
        )

        # ic(models_range)

        # models_range = await self.transform_feedbacks_to_car_param(models_range, chosen_demand_params)

        return models_range


    async def get_lexicon_class(self, request: Message | CallbackQuery, state: FSMContext, memory_storage, chosen_params, param_to_output):
        period = memory_storage.get('stats_period')
        calculate_method = memory_storage.get('calculate_method')
        ic(period)
        lexicon_class = deepcopy(ChooseCustomParamsToStats)(period, param_to_output, calculate_method,
                                                                           chosen_params)
        ic(lexicon_class)
        header = f'''{copy(Lexicon_module.statistic_captions['top_demand_on'])}'''
        if not chosen_params:
            header += f''' {copy(Lexicon_module.statistic_captions['car'])} '''
        elif chosen_params:
            car_configs_module = importlib.import_module('database.data_requests.car_configurations_requests')
            header += ':\n'
            for param_type, param_id in chosen_params.items():
                param_object = await car_configs_module.CarConfigs.get_by_id(param_type, param_id)
                if param_object:
                    header += f'''{Lexicon_module.statistic_captions[param_type]}: {param_object.name}\n'''
                else:
                    admin_backward_command_module = importlib.import_module('handlers.callback_handlers.admin_part.admin_panel_ui.utils.admin_backward_command')

                    await self.send_alert_answer(request, Lexicon_module.LEXICON['search_parameter_invalid'])
                    await admin_backward_command_module\
                            .choose_custom_params_stats_backwarder(request, state)
                    return
            header = header[:-1] + '; '
        lexicon_class.message_text = lexicon_class.message_text.format(header=header)
        ic(lexicon_class.__dict__)
        return lexicon_class

    async def get_choose_data(self, request, state, chosen_param_name):
        all_params_to_choose = ['engine', 'brand', 'model', 'complectation', 'color']
        ic(chosen_param_name)
        if chosen_param_name:
            if chosen_param_name == 'color':
                await OutputStatisticAdvertParamsHandler().callback_handler(request, state)
                return
            else:
                next_param_to_output = all_params_to_choose[all_params_to_choose.index(chosen_param_name)+1]
        else:
            next_param_to_output = 'engine'
        ic(next_param_to_output)
        return next_param_to_output

    async def get_last_chosen_param(self, request, state: FSMContext, get_next_param=False):
        memory_storage = await state.get_data()
        chosen_params = memory_storage.get('chosen_demand_params')
        if chosen_params:
            chosen_params_keys = chosen_params.keys()
            if 'color' in chosen_params_keys:
                await OutputStatisticAdvertParamsHandler().callback_handler(request, state)
                return 'exit'
            # elif chosen_params_keys in ()
            elif 'complectation' in chosen_params_keys:
                chosen_param = 'complectation'
            elif 'model' in chosen_params_keys:
                chosen_param = 'model'
            elif 'brand' in chosen_params_keys:
                chosen_param = 'brand'

            elif 'engine' in chosen_params_keys:
                chosen_param = 'engine'
            else:
                return False

            if get_next_param:
                all_params_to_choose = ['engine', 'brand', 'model', 'complectation', 'color']

                chosen_param = all_params_to_choose[all_params_to_choose.index(chosen_param) + 1]

            return chosen_param