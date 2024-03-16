import importlib
from copy import copy

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.callback_handlers.sell_part.commodity_requests.delete_car_request import CheckFeedbacksHandler, \
    DeleteCarRequest


Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')


class DeleteFeedback:

    @staticmethod
    async def did_you_sure_to_delete_feedback_ask(callback: CallbackQuery):
        message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
        redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт

        lexicon_part = copy(Lexicon_module.LexiconSellerRequests.did_you_sure_to_delete_feedback_ask)

        seller_request_data = await redis_module.redis_data.get_data(
            key=f'{str(callback.from_user.id)}:seller_request_data', use_json=True)

        offer_id = seller_request_data.get('offer_id')
        lexicon_part['message_text'] = lexicon_part['message_text'].format(feedback_number=offer_id)

        await message_editor.travel_editor.edit_message(request=callback, lexicon_key='',
                                                        lexicon_part=lexicon_part,
                                                        delete_mode=True)


    @staticmethod
    async def delete_feedback_handler(callback: CallbackQuery, state: FSMContext):
        redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт
        cached_requests_module = importlib.import_module('database.data_requests.offers_requests')

        seller_request_data = await redis_module.redis_data.get_data(
            key=f'{str(callback.from_user.id)}:seller_request_data', use_json=True)

        delete_query = await cached_requests_module.OffersRequester.delete_offer(seller_request_data.get('offer_id'))

        await callback.answer(Lexicon_module.LexiconSellerRequests.success_delete)

        if not await DeleteCarRequest.send_seller_requests_page_without_current(callback, state):
            # return_path = await redis_module.redis_data.get_data(
            #     key=f'{str(callback.from_user.id)}:return_path_after_delete_car')

            return_requests = await CheckFeedbacksHandler.check_feedbacks_handler(callback, command='viewed_feedbacks', state=state)
        else:
            return_requests = True
        if not return_requests:

            return_requests = await CheckFeedbacksHandler.my_feedbacks_callback_handler(callback, state)