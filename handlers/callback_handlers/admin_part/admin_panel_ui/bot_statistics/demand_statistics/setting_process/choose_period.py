from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from handlers.callback_handlers.admin_part.admin_panel_ui.bot_statistics.handle_tools.base_callbackquery_handler import \
    BaseStatisticCallbackHandler
from utils.lexicon_utils.admin_lexicon.bot_statistics_lexicon import statistic_captions


class CustomParamsChoosePeriod(BaseStatisticCallbackHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        # async with self.idle_callback_answer(request):
        await self.set_state(state, self.statistic_manager.states.choose_period)
        await self.accept_calculate_method(request, state)
        self.output_methods = [
            self.menu_manager.travel_editor(
                lexicon_part=await self.format_message_text(state),
                dynamic_buttons=2
            )
        ]

    async def format_message_text(self, state):
        memory_storage = await state.get_data()
        output_method = memory_storage.get('output_method')
        lexicon_part = self.statistic_manager.lexicon['custom_params_period']
        match output_method:
            case 'top_ten':
                output_method = 'top_10_stats'
            case 'individual':
                output_method = 'individual_stats'

        output_method = statistic_captions[output_method]
        lexicon_part['message_text'] = lexicon_part['message_text'].format(output_method=output_method)
        return lexicon_part
    async def accept_calculate_method(self, request: Message | CallbackQuery, state: FSMContext):
        if 'calculate_method:' in request.data:
            calculate_method = request.data.split(':')[-1]
            await state.update_data(calculate_method=calculate_method)
