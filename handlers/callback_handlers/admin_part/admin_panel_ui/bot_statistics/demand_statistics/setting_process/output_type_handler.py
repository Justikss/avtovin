from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from handlers.callback_handlers.admin_part.admin_panel_ui.bot_statistics.demand_statistics.top_ten_display import \
    TopTenByDemandDisplayHandler
from handlers.callback_handlers.admin_part.admin_panel_ui.bot_statistics.handle_tools.base_callbackquery_handler import \
    BaseStatisticCallbackHandler

class DemandOutputSplitterHandler(BaseStatisticCallbackHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        ic()
        await self.accept_calculate_method(request, state)
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
                await TopTenByDemandDisplayHandler().callback_handler(request, state)

            case 'individual':
                pass

    async def accept_calculate_method(self, request: Message | CallbackQuery, state: FSMContext):
        if 'calculate_method:' in request.data:
            await self.send_alert_answer(request, self.statistic_manager.lexicon['stats_loading'])
            calculate_method = request.data.split(':')[-1]
            await state.update_data(calculate_method=calculate_method)
