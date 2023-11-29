import importlib
from abc import ABC

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.data_requests.commodity_requests import CommodityRequester
from states.seller_feedbacks_states import SellerFeedbacks
from utils.Lexicon import LEXICON, LexiconCommodityLoader, LexiconSellerRequests
from handlers.callback_handlers.sell_part.commodity_requests.pagination_handlers import output_sellers_commodity_page
from utils.user_notification import delete_notification_for_seller


async def my_feedbacks_callback_handler(callback: CallbackQuery, delete_media_group_mode=False):
    message_editor_module = importlib.import_module('handlers.message_editor')
    if ':' in callback.data:
        await delete_notification_for_seller(callback)

    await message_editor_module.travel_editor.edit_message(request=callback, delete_mode=True, lexicon_key='seller___my_feedbacks', delete_media_group_mode=delete_media_group_mode)

    return True



class CheckFeedBacksABC(ABC):
    pass


class CheckFeedbacksHandler(CheckFeedBacksABC):
    def __init__(self):
        pass

    @staticmethod
    async def check_feedbacks_handler(callback: CallbackQuery, state: FSMContext, command=None):
        redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт
        callback_alert_message = None
        callback_data = callback.data
        seller_id = callback.from_user.id

        await redis_module.redis_data.delete_key(key=f'{str(seller_id)}:seller_requests_pagination')

        if callback_data == 'new_feedbacks':
            viewed = False
            keyboard_part = LexiconSellerRequests.check_new_feedbacks_buttons
        elif 'viewed_feedbacks' in (command, callback_data):
            viewed = True
            keyboard_part = LexiconSellerRequests.check_viewed_feedbacks_buttons


        unpacked_output_data = await CheckFeedbacksHandler.make_unpacked_data_for_seller_output(callback, viewed)
        if unpacked_output_data:
            await redis_module.redis_data.set_data(
                key=f'{str(seller_id)}:last_keyboard_in_seller_pagination',
                value=keyboard_part)

            if callback_data != 'viewed_feedbacks':
                await redis_module.redis_data.set_data(
                    key=f'{str(seller_id)}:return_path_after_delete_car',
                    value='viewed_feedbacks')
            ic()
            await state.set_state(SellerFeedbacks.review)
            await output_sellers_commodity_page(callback, state, unpacked_output_data)

            # await CheckFeedbacksHandler.check_new_feedbacks(callback, unpacked_output_data)
            return True
        else:
            if callback_data == 'new_feedbacks':
                callback_alert_message = LexiconSellerRequests.new_feedbacks_not_found
            elif callback_data == 'viewed_feedbacks':
                callback_alert_message = LexiconSellerRequests.viewed_feedbacks_not_found

            if callback_alert_message:
                await callback.answer(text=callback_alert_message)
            return False

        #
        #
        # await redis_module.redis_data.set_data(key=f'{str(seller_id)}:seller__new_active_offers', value=seller_offers)
        #
        # await redis_module.redis_data.set_data(key=f'{str(seller_id)}:seller__viewed_active_offers', value=seller_offers)
        #

    @staticmethod
    async def make_unpacked_data_for_seller_output(callback: CallbackQuery, viewed: bool):
        cached_requests_module = importlib.import_module('database.data_requests.offers_requests')

        seller_offers = await cached_requests_module.OffersRequester.get_by_seller_id(seller_id_value=callback.from_user.id, viewed_value=viewed)
        if seller_offers:
            if viewed == False:
                ic()
                # await OffersRequester.set_viewed_true(seller_offers)
            card_body_lexicon_part = LEXICON.get('chosen_configuration').get('message_text')
            for_seller_lexicon_part = LEXICON['confirm_from_seller']['message_text']
            output_unpacked_data = []
            for offer in seller_offers:
                car = offer.car_id
                buyer = offer.buyer_id
                card_startswith = f'''{for_seller_lexicon_part['feedback_header'].replace('X', str(offer.id))}\n{for_seller_lexicon_part['from_user']} @{buyer.username}\n{for_seller_lexicon_part['tendered'].replace('X', str(car.car_id))}\n{for_seller_lexicon_part['contacts']} {buyer.phone_number}'''

                if car.state == LexiconCommodityLoader.load_commodity_state['buttons']['load_state_second_hand']:
                    result_string = f'''
                        {card_startswith}\n{card_body_lexicon_part['car_state']} {car.state}\n{card_body_lexicon_part['engine_type']} {car.engine_type}\n{card_body_lexicon_part['color']} {car.color}\n{card_body_lexicon_part['model']} {car.model}\n{card_body_lexicon_part['brand']} {car.brand}\n{card_body_lexicon_part['complectation']} {car.complectation}\n{card_body_lexicon_part['year']} {car.year_of_release}\n{card_body_lexicon_part['mileage']} {car.mileage}\n{card_body_lexicon_part['cost']} {car.price}'''
                elif car.state == LexiconCommodityLoader.load_commodity_state['buttons']['load_state_new']:
                    result_string = f'''
                        {card_startswith}\n{card_body_lexicon_part['car_state']} {car.state}\n{card_body_lexicon_part['engine_type']} {car.engine_type}\n{card_body_lexicon_part['model']} {car.model}\n{card_body_lexicon_part['brand']} {car.brand}\n{card_body_lexicon_part['complectation']} {car.complectation}\n{card_body_lexicon_part['cost']} {car.price}'''

                photo_album = CommodityRequester.get_photo_album_by_car_id(car_id=car.car_id, get_list=True)

                result_part = {'offer_id': offer.id, 'car_id': car.car_id, 'message_text': result_string, 'album': photo_album}
                output_unpacked_data.append(result_part)
                ic(result_part)
            return output_unpacked_data


