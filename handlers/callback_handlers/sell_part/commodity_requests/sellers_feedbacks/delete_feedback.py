import importlib
from copy import copy

from aiogram.types import CallbackQuery

from database.data_requests.offers_requests import OffersRequester
from utils.Lexicon import LexiconSellerRequests
from handlers.callback_handlers.sell_part.commodity_requests.delete_car_request import CheckFeedbacksHandler, my_feedbacks_callback_handler

class DeleteFeedback:

    @staticmethod
    async def did_you_sure_to_delete_feedback_ask(callback: CallbackQuery):
        message_editor = importlib.import_module('handlers.message_editor')  # Ленивый импорт
        redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт

        lexicon_part = copy(LexiconSellerRequests.did_you_sure_to_delete_feedback_ask)

        seller_request_data = await redis_module.redis_data.get_data(
            key=f'{str(callback.from_user.id)}:seller_request_data', use_json=True)

        offer_id = seller_request_data.get('offer_id')
        lexicon_part['message_text'] = lexicon_part['message_text'].replace('X', str(offer_id))

        await message_editor.travel_editor.edit_message(request=callback, lexicon_key='',
                                                        lexicon_part=lexicon_part,
                                                        delete_mode=True)


    @staticmethod
    async def delete_feedback_handler(callback: CallbackQuery):
        redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт

        seller_request_data = await redis_module.redis_data.get_data(
            key=f'{str(callback.from_user.id)}:seller_request_data', use_json=True)

        delete_query = await OffersRequester.delete_offer(seller_request_data.get('offer_id'))

        await callback.answer(LexiconSellerRequests.success_delete)

        return_requests = await CheckFeedbacksHandler.check_feedbacks_handler(callback, command='viewed_feedbacks')
        # return_requests = await my_feedbacks_callback_handler(callback, return_path)

        if not return_requests:
            return_requests = await my_feedbacks_callback_handler(callback)