from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from config_data.config import top_ten_pagesize
from database.data_requests.car_advert_requests import AdvertRequester
from handlers.callback_handlers.admin_part.admin_panel_ui.bot_statistics.handle_tools.base_callbackquery_handler import \
    BaseStatisticCallbackHandler
from handlers.callback_handlers.sell_part.checkout_seller_person_profile import get_seller_name
from utils.lexicon_utils.Lexicon import LEXICON
from utils.lexicon_utils.admin_lexicon.bot_statistics_lexicon import TopTenDisplay


class TopTenByDemandDisplayHandler(BaseStatisticCallbackHandler):
    async def process_callback(self, request: Message | CallbackQuery, state: FSMContext, **kwargs):
        set_state = await self.set_state(state, self.statistic_manager.states.display_top_ten)
        ic()
        ic(request.data)
        if set_state == 'exists':
            await self.get_selected_params_model(request, state)
        else:
            await self.set_pagination_display(request, state)

    async def set_pagination_display(self, request: Message | CallbackQuery, state: FSMContext):
        models_range = await self.construct_models_structure(state)

        # todo добавить вывод фото
        ic(models_range[0].__dict__)
        self.output_methods = [
            self.menu_manager.inline_pagination(
                lexicon_class=await self.construct_lexicon_part(position=models_range[0].name[:models_range[0].name.index('.')],
                                                                feedback_model=models_range[0]),
                page_size=top_ten_pagesize,
                models_range=models_range
            )
        ]

    async def get_selected_params_model(self, request: Message | CallbackQuery, state: FSMContext):
        position_to_output = int(request.data.split(':')[-1])
        redis_key = f'{str(request.from_user.id)}:inline_buttons_pagination_data'
        params_in_queue = await self.redis_module.redis_data.get_data(redis_key, use_json=True)
        params_to_output = await self.get_params_to_output(params_in_queue, position_to_output)

        if params_to_output:
            feedback_model = await self.statistic_manager.database_requests.get_seller_feedback_by_id(
                params_to_output['id'])

            if feedback_model.advert_parameters:
                await self.edit_displayed_data(request, params_to_output, feedback_model)
            else:
                await state.clear()
                await self.send_alert_answer(request, LEXICON['non_actiallity'])
                return await self.callback_handler(request, state)

    async def edit_displayed_data(self, request: Message | CallbackQuery, params_to_output, feedback_model):
        # todo Добавить edit media group
        new_message_text = await self.construct_lexicon_part(position=params_to_output['position'],
                                                             feedback_model=feedback_model,
                                                             only_message_text=True)
        message_object: Message = await self.message_object(request)
        await request.bot.edit_message_text(chat_id=message_object.chat.id,
                                            message_id=await self.redis_module.redis_data.get_data(
                                                key=f'{request.from_user.id}:last_message'
                                            ),
                                            text=new_message_text)


    async def get_params_to_output(self, params_in_queue, position_to_output):
        for part in params_in_queue:
            for key, value in part:
                feedback_id = int(key.split(':')[-1])
                if feedback_id == position_to_output:
                    params_to_output = {'position': int(ic(value[:value.index('.')])), 'id': feedback_id}
                    return params_to_output

    async def construct_lexicon_part(self, position, feedback_model, only_message_text=False):
        lexicon_class = TopTenDisplay
        lexicon_class.message_text = lexicon_class.message_text.format(
            top_position=position,
            parameters=await self.statistic_manager.car_params_card_pattern(advert_id=feedback_model.advert_parameters),
            seller_entity=await get_seller_name(feedback_model.seller_id, for_admin=True))

        if only_message_text:
            return lexicon_class.message_text
        return lexicon_class



    async def construct_models_structure(self, state: FSMContext):
        models_range = await self.statistic_manager.database_requests.get_top_advert_parameters(
            top_direction=await self.get_demand_direction(state)
        )

        if not models_range:
            models_range = [self.statistic_manager.empty_button_field]
        else:
            for index,  model in enumerate(models_range):
                await AdvertRequester.load_related_data_for_advert(model.advert_parameters)
                model.name = f'{index+1}. {model.advert_parameters.complectation.model.brand.name} - {model.advert_parameters.complectation.model.name}'
                ic(hasattr(model, 'name'))
                ic(model.id)
        return models_range

    async def get_demand_direction(self, state: FSMContext):
        memory_storage = await state.get_data()
        calculate_method = memory_storage.get('calculate_method')
        return calculate_method