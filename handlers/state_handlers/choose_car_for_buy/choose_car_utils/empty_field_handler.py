from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

# from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
#     BaseCallbackQueryHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.bot_statistics.choose_statistic_type import base_callback_query_module

class EmptyFieldCarpoolingHandler(base_callback_query_module.BaseCallbackQueryHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):

        callable_method_name = await self.get_callable_method_name(state)

        await self.call_method(request, state, callable_method_name)

    async def call_method(self, request, state, callable_method_name):
        match callable_method_name:
            case 'complectation':
                from handlers.state_handlers.choose_car_for_buy.hybrid_handlers import choose_complectation_handler
                await choose_complectation_handler(request, state, first_call=False)
            case 'color':
                from handlers.state_handlers.choose_car_for_buy.hybrid_handlers import choose_color_handler
                await choose_color_handler(request, state, first_call=False)

            case 'mileage':
                from handlers.state_handlers.choose_car_for_buy.second_hand_car_handlers import choose_mileage_handler
                await choose_mileage_handler(request, state, first_call=False)
            case 'year_of_release':
                from handlers.state_handlers.choose_car_for_buy.second_hand_car_handlers import \
                    choose_year_of_release_handler
                await choose_year_of_release_handler(request, state, first_call=False)

            case 'output':
                from handlers.state_handlers.choose_car_for_buy.hybrid_handlers import search_config_output_handler

                await search_config_output_handler(request, state, first_call=False)

    async def get_callable_method_name(self, state: FSMContext):
        memory_storage = await state.get_data()
        current_state = str(await state.get_state())
        cars_state = memory_storage.get('cars_state')
        parameters = ['complectation', 'color', 'mileage', 'year_of_release', 'output']
        callable_method_name = None
        match current_state:                                       #on used      on new
            case 'SecondHandChooseStates:select_mileage': #color                X
                if int(cars_state) == 2:
                    callable_method_name = 'mileage'
            case 'HybridChooseStates:select_color' | 'SecondHandChooseStates:select_color': #complect complect
                callable_method_name = 'color'
            case 'SecondHandChooseStates:select_year': #mileage
                callable_method_name = 'year_of_release'
            case 'HybridChooseStates:config_output': #year                     color
                callable_method_name = 'output'

        if callable_method_name:
            memory_storage[f'cars_{parameters[parameters.index(callable_method_name)-1]}'] = 'null'
            await state.set_data(memory_storage)
        return callable_method_name
    #
    # cars_year_of_release
    # cars_mileage
    # cars_complectation
    # cars_color
