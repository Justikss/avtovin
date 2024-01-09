from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from handlers.callback_handlers.admin_part.admin_panel_ui.bot_statistics.handle_tools.base_callbackquery_handler import \
    BaseStatisticCallbackHandler

class CalculateDemandMethodHandler(BaseStatisticCallbackHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        ic()
        ic(request.data)
        await self.accept_output_method(request, state)

        await self.set_state(state, self.statistic_manager.states.accept_demand_calculate_method)

        self.output_methods = [
            self.menu_manager.travel_editor(
                lexicon_part=self.statistic_manager.lexicon['choose_method_of_calculating'],
                dynamic_buttons=2
            )
        ]
        await super().process_callback(request, state, **kwargs)

    async def accept_output_method(self, request: Message | CallbackQuery, state: FSMContext):
        ic(request.data)
        ic()
        if 'output_method:' in request.data:
            output_method = request.data.split(':')[-1]
            await state.update_data(output_method=output_method)
