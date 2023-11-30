import importlib
from copy import copy

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.data_requests.car_advert_requests import AdvertRequester
from handlers.callback_handlers.sell_part.commodity_requests.commodity_requests_handler import \
    commodity_reqests_by_seller
from handlers.callback_handlers.sell_part.commodity_requests.my_requests_handler import seller_requests_callback_handler
from handlers.callback_handlers.sell_part.commodity_requests.output_sellers_requests import \
    output_sellers_requests_by_car_brand_handler

from handlers.callback_handlers.sell_part.commodity_requests.sellers_feedbacks.my_feedbacks_button import \
    my_feedbacks_callback_handler, CheckFeedbacksHandler
from utils.Lexicon import LexiconSellerRequests


class DeleteCarRequest:

    @staticmethod
    async def delete_car_handler(callback: CallbackQuery):
        message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
        redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт

        seller_request_data = await redis_module.redis_data.get_data(
            key=f'{str(callback.from_user.id)}:seller_request_data', use_json=True)
        car_id = seller_request_data['car_id']
        ic(car_id)
        lexicon_part = copy(LexiconSellerRequests().seller_sure_delete_car_ask)
        ic(lexicon_part)
        lexicon_part['message_text'] = lexicon_part['message_text'].replace('X', str(car_id))
        ic(lexicon_part)
        await message_editor.travel_editor.edit_message(request=callback, lexicon_key='',
                                                        lexicon_part=lexicon_part,
                                                        delete_mode=True)

    @staticmethod
    async def accept_delete_car_and_backward_from_delete_menu_handler(callback: CallbackQuery, state: FSMContext):
        redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт

        if callback.data == "i'm_sure_delete":
            ic(callback.data)
            seller_request_data = await redis_module.redis_data.get_data(
                key=f'{str(callback.from_user.id)}:seller_request_data', use_json=True)
            car_id = seller_request_data['car_id']

            await AdvertRequester.delete_advert_by_id(car_id)

            await callback.answer(LexiconSellerRequests.success_delete)

        return_path = await redis_module.redis_data.get_data(
            key=f'{str(callback.from_user.id)}:return_path_after_delete_car')

        await redis_module.redis_data.delete_key(
            key=f'{str(callback.from_user.id)}:seller_requests_pagination')

        return_requests = None

        ic(return_path)
        if return_path in ('viewed_feedbacks', "i'm_sure_delete_feedback"):
            return_requests = await CheckFeedbacksHandler.check_feedbacks_handler(callback, command='viewed_feedbacks', state=state)
            # return_requests = await my_feedbacks_callback_handler(callback, return_path)

            if not return_requests:
                return_requests = await my_feedbacks_callback_handler(callback)
            # if not return_requests:
            #     await commodity_reqests_by_seller(callback)

        elif return_path.startswith('seller_requests_brand'):
            chosen_brand = await redis_module.redis_data.get_data(
                key=str(callback.from_user.id) + ':sellers_requests_car_brand_cache')

            return_requests = await output_sellers_requests_by_car_brand_handler(callback, state, chosen_brand)
            ic(return_requests)

            if not return_requests:
                return_requests = await seller_requests_callback_handler(callback, state)
                if not return_requests:
                    await commodity_reqests_by_seller(callback)
        # await redis_module.redis_data.delete_key(
        #     key=f'{str(callback.from_user.id)}:return_path_after_delete_car')

