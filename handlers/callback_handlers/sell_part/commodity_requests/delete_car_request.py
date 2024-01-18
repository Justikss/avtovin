import importlib
from copy import copy

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.callback_handlers.sell_part.commodity_requests.commodity_requests_handler import \
    commodity_reqests_by_seller
from handlers.callback_handlers.sell_part.commodity_requests.my_requests_handler import seller_requests_callback_handler


from handlers.callback_handlers.sell_part.commodity_requests.sellers_feedbacks.my_feedbacks_button import \
    CheckFeedbacksHandler
from handlers.state_handlers.choose_car_for_buy.choose_car_utils.output_cars_pagination_system.pagination_system_for_buyer import \
    BuyerCarsPagination
from handlers.utils.pagination_heart import Pagination

Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')


class DeleteCarRequest:
    @staticmethod
    async def send_seller_requests_page_without_current(callback: CallbackQuery, state: FSMContext):
        message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
        output_seller_request_module = importlib.import_module('handlers.callback_handlers.sell_part.commodity_requests.output_sellers_requests')

        pagination_data = await message_editor.redis_data.get_data(
            key=f'{str(callback.from_user.id)}:seller_requests_pagination', use_json=True)
        ic(pagination_data)

        # pagination_data['data'].pop(pagination_data['current_page'] - 1)
        # pagination_data['current_page'] -= 1
        ic(pagination_data)

        pagination = Pagination(**pagination_data)
        ic(len(pagination.data))
        try:
            pagination.data.pop(pagination.current_page)
        except:
            return False
        ic(len(pagination.data))

        # pagination.current_page -= 1
        # ic(pagination_data['data'])
        ic(len(pagination_data['data']) < 1)
        if len(pagination_data['data']) < 1:
            return False
        await message_editor.redis_data.set_data(
            key=f'{str(callback.from_user.id)}:seller_requests_pagination', value=await pagination.to_dict())
        await output_seller_request_module.output_sellers_commodity_page(callback, state, pagination.data)

        # await message_editor.redis_data.set_data(
        #     key=f'{str(callback.from_user.id)}:seller_requests_pagination',
        #     value=pagination_data)

        return True

    @staticmethod
    async def delete_car_handler(callback: CallbackQuery):
        message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
        redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт

        seller_request_data = await redis_module.redis_data.get_data(
            key=f'{str(callback.from_user.id)}:seller_request_data', use_json=True)
        car_id = seller_request_data['car_id']
        ic(car_id)
        lexicon_part = copy(Lexicon_module.LexiconSellerRequests.seller_sure_delete_car_ask)
        ic(lexicon_part)
        lexicon_part['message_text'] = lexicon_part['message_text'].format(number=car_id)
        ic(lexicon_part)
        await message_editor.travel_editor.edit_message(request=callback, lexicon_key='',
                                                        lexicon_part=lexicon_part,
                                                        delete_mode=True)

    @staticmethod
    async def accept_delete_car_and_backward_from_delete_menu_handler(callback: CallbackQuery, state: FSMContext):
        redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт

        if callback.data == "i'm_sure_delete":
            car_advert_requests_module = importlib.import_module('database.data_requests.car_advert_requests')

            ic(callback.data)
            seller_request_data = await redis_module.redis_data.get_data(
                key=f'{str(callback.from_user.id)}:seller_request_data', use_json=True)
            car_id = seller_request_data['car_id']

            await car_advert_requests_module\
                .AdvertRequester.delete_advert_by_id(callback.from_user.id, car_id)

            await callback.answer(Lexicon_module.LexiconSellerRequests.success_delete)

        return_path = await redis_module.redis_data.get_data(
            key=f'{str(callback.from_user.id)}:return_path_after_delete_car')

        ic(return_path)

        if not await DeleteCarRequest.send_seller_requests_page_without_current(callback, state):
            if return_path in ('viewed_feedbacks', "i'm_sure_delete_feedback"):


                return_requests = await CheckFeedbacksHandler.check_feedbacks_handler(callback, command='viewed_feedbacks', state=state)

                if not return_requests:
                   await CheckFeedbacksHandler.my_feedbacks_callback_handler(callback, state)


            elif return_path.startswith('seller_requests_brand'):
                output_seller_request_module = importlib.import_module(
                    'handlers.callback_handlers.sell_part.commodity_requests.output_sellers_requests')

                chosen_brand = await redis_module.redis_data.get_data(
                    key=str(callback.from_user.id) + ':sellers_requests_car_brand_cache')

                return_requests = await output_seller_request_module.output_sellers_requests_by_car_brand_handler(callback, state, chosen_brand)
                ic(return_requests)

                if not return_requests:
                    return_requests = await seller_requests_callback_handler(callback, state)
                    if not return_requests:
                        await commodity_reqests_by_seller(callback, state)
            # await redis_module.redis_data.delete_key(
            #     key=f'{str(callback.from_user.id)}:return_path_after_delete_car')

