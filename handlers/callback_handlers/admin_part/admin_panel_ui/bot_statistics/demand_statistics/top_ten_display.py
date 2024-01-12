import importlib
from copy import copy, deepcopy

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from config_data.config import top_ten_pagesize
from database.data_requests.advert_parameters_requests import AdvertParameterManager
from database.data_requests.car_advert_requests import AdvertRequester
from database.data_requests.new_car_photo_requests import PhotoRequester
from database.tables.offers_history import SellerFeedbacksHistory
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

        self.output_methods = [
            self.menu_manager.inline_pagination(
                lexicon_class=await self.construct_lexicon_part(
                    state=state,
                    position=models_range[0].name[:models_range[0].name.index('.')],
                    feedback_model=models_range[0]),
                page_size=top_ten_pagesize,
                models_range=models_range
            )
        ]

    async def get_photos_by_params(self, state: FSMContext, params_model):
        media_group = await PhotoRequester.try_get_photo(state=state,
                                                         complectation=params_model.complectation.id,
                                                         color=params_model.color.id,
                                                         for_admin=True)
        ic(media_group)
        ic()
        await state.update_data(media_group_for_inline_pg=media_group)

    async def edit_displayed_data(self, state: FSMContext, advert_parameters, seller_model, position):
        # todo Добавить edit media group
        feedback_model = SellerFeedbacksHistory()
        feedback_model.seller_id = seller_model
        feedback_model.advert_parameters = advert_parameters
        ic(feedback_model.advert_parameters)
        ic(feedback_model.advert_parameters.complectation.model.brand.name)
        new_message_text = await self.construct_lexicon_part(state=state,
                                                             position=position,
                                                             feedback_model=feedback_model,
                                                             only_message_text=True)
        ic(new_message_text)
        self.output_methods = [
            self.menu_manager.inline_pagination(
                remove_last_pagination_data=False,
                lexicon_class=new_message_text,
                page_size=top_ten_pagesize,
                models_range=1,
            )
        ]


    async def get_selected_params_model(self, request: Message | CallbackQuery, state: FSMContext):
        person_requests_module = importlib.import_module('database.data_requests.person_requests')

        ic(request.data)
        params_id = int(request.data.split(':')[-2])
        seller_id = int(request.data.split(':')[-1])
        ic(params_id, seller_id)
        redis_key = f'{str(request.from_user.id)}:inline_buttons_pagination_data'
        params_in_queue = await self.redis_module.redis_data.get_data(redis_key, use_json=True)
        position = await self.get_params_top_position(params_in_queue, params_id=params_id, seller_id=seller_id)

        advert_parameters = await AdvertParameterManager.get_by_id(params_id)
        seller_model = await person_requests_module.PersonRequester.get_user_for_id(seller_id, seller=True)
        ic(advert_parameters)
        ic(advert_parameters.complectation.model.brand.name)
        if advert_parameters and seller_model:
            await self.edit_displayed_data(state, advert_parameters, seller_model, position)
        else:
            await state.clear()
            await self.send_alert_answer(request, LEXICON['non_actiallity'])
            return await self.callback_handler(request, state)

    async def get_params_top_position(self, params_in_queue, params_id, seller_id):
        ic(params_in_queue['data'])
        for part in params_in_queue['data']:
            for key, value in part.items():
                other_params_id = int(key.split(':')[-2])
                other_seller_id = int(key.split(':')[-1])
                ic(key, other_seller_id, other_params_id)
                if (other_params_id == params_id and other_seller_id == seller_id):
                    return value[:value.index('.')]

    async def construct_lexicon_part(self, state: FSMContext, position, feedback_model, only_message_text=False):
        async def get_seller_entity():
            seller_entity = await get_seller_name(feedback_model.seller_id, for_admin=True)
            if seller_entity:
                if isinstance(seller_entity, tuple):
                    seller_entity = f'{seller_entity[0]}\n{seller_entity[1]}'

                return seller_entity

        await self.get_photos_by_params(state, feedback_model.advert_parameters)
        lexicon_class = deepcopy(TopTenDisplay)
        params_text = await self.statistic_manager.car_params_card_pattern(advert_id=feedback_model.advert_parameters)
        ic(params_text)
        params_text = '\n'.join(params_text.split('\n')[:-1])
        ic(params_text)
        ic()
        ic(hasattr(lexicon_class, 'message_text'))
        lexicon_class.message_text = copy(self.statistic_manager.lexicon['top_ten_message_text']).format(
            top_position=position,
            parameters=params_text,
            seller_entity=await get_seller_entity())

        ic(lexicon_class.message_text)
        ic()
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
                model.id = f'{model.advert_parameters_id}:{model.seller_id}'
                ic(hasattr(model, 'name'))
                ic(model.id)
        return models_range

    async def get_demand_direction(self, state: FSMContext):
        memory_storage = await state.get_data()
        calculate_method = memory_storage.get('calculate_method')
        return calculate_method