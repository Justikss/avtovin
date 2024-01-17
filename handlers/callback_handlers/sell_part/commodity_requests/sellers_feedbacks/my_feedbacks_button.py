import importlib
import traceback
from abc import ABC
from copy import copy

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from handlers.utils.create_advert_configuration_block import create_advert_configuration_block
from states.seller_feedbacks_states import SellerFeedbacks
from utils.custom_exceptions.database_exceptions import UserExistsError, CarExistsError
from utils.get_currency_sum_usd import get_valutes
from utils.get_username import get_username
from utils.user_notification import delete_notification_for_seller


Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

class CheckFeedBacksABC(ABC):
    pass


class CheckFeedbacksHandler(CheckFeedBacksABC):
    def __init__(self):
        pass

    @staticmethod
    async def create_offer_data(request: CallbackQuery | Message, offer_id):
        active_offers_module = importlib.import_module('database.data_requests.offers_requests')
        car_advert_requests_module = importlib.import_module('database.data_requests.car_advert_requests')
        offer = await active_offers_module.OffersRequester.get_by_offer_id(offer_id)

        try:
            car = offer.car_id
        except:
            await active_offers_module.OffersRequester.delete_offer(offer_id)
            raise CarExistsError()
        try:
            buyer = offer.buyer_id
        except:
            await active_offers_module.OffersRequester.delete_offer(offer_id)
            raise UserExistsError()

        for_seller_lexicon_part = Lexicon_module.LEXICON['confirm_from_seller']['message_text']

        fullname = f'''{buyer.surname} {buyer.name} {buyer.patronymic if buyer.patronymic else ''}'''
        ic(offer_id)
        card_startswith = f'''{for_seller_lexicon_part['feedback_header']}\n{for_seller_lexicon_part['from_user']}\n{for_seller_lexicon_part['tendered']}\n{for_seller_lexicon_part['contacts']}'''
        ic(card_startswith)
        card_startswith = card_startswith.format(feedback_number=offer_id,
                                                 from_user=f'@{await get_username(request.bot, buyer.telegram_id)}',
                                                 advert_number=car.id, name=fullname, phone=buyer.phone_number)

        mileage = car.mileage.name if car.state.id == 2 else None
        year_of_realise = car.year.name if car.state.id == 2 else None

        advert_data = await create_advert_configuration_block(car_state=car.state.name,
                                                              engine_type=car.complectation.engine.name,
                                                              brand=car.complectation.model.brand.name,
                                                              model=car.complectation.model.name,
                                                              complectation=car.complectation.name,
                                                              color=car.color.name, mileage=mileage,
                                                              year_of_realise=year_of_realise,
                                                              sum_price=car.sum_price,
                                                              usd_price=car.dollar_price)

        result_string = f'''{card_startswith}{advert_data}'''

        photo_album = await car_advert_requests_module\
            .AdvertRequester.get_photo_album_by_advert_id(car.id, get_list=True)

        result_data = {'offer_id': offer_id, 'car_id': offer.car_id, 'message_text': result_string, 'album': photo_album}
        return result_data

    @staticmethod
    async def my_feedbacks_callback_handler(callback: CallbackQuery, state: FSMContext, delete_media_group_mode=False):
        message_editor_module = importlib.import_module('handlers.message_editor')
        if ':' in callback.data:
            await delete_notification_for_seller(callback)

        await message_editor_module.travel_editor.edit_message(request=callback, delete_mode=True,
                                                               lexicon_key='seller___my_feedbacks',
                                                               delete_media_group_mode=delete_media_group_mode)
        await state.set_state(SellerFeedbacks.choose_feedbacks_state)
        return True

    @staticmethod
    async def check_feedbacks_handler(callback: CallbackQuery, state: FSMContext, command=None):
        cached_requests_module = importlib.import_module('database.data_requests.offers_requests')
        redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт
        output_seller_requests_module = importlib.import_module('handlers.callback_handlers.sell_part.commodity_requests.output_sellers_requests')

        callback_alert_message = None
        callback_data = callback.data
        seller_id = callback.from_user.id
        error_flag = False
        error_alert_message = False
        offer_ids = False
        ic(callback.data)
        ic()
        if callback.data in ('new_feedbacks', 'viewed_feedbacks'):
            redis_key = str(callback.from_user.id) + ':user_state'
            await redis_module.redis_data.set_data(redis_key, value='sell')

        await redis_module.redis_data.delete_key(key=f'{str(seller_id)}:seller_requests_pagination')

        if callback_data == 'new_feedbacks':
            viewed = False
            keyboard_part = Lexicon_module\
                .LexiconSellerRequests.check_viewed_feedbacks_buttons
        elif 'viewed_feedbacks' in (command, callback_data):
            viewed = True
            keyboard_part = Lexicon_module\
                .LexiconSellerRequests.check_viewed_feedbacks_buttons

        try:
            ic(viewed)
            seller_offers = await cached_requests_module.OffersRequester.get_by_seller_id(seller_id_value=callback.from_user.id, viewed_value=viewed)
            if seller_offers:
                offer_ids = [offer.id for offer in seller_offers]
            # unpacked_output_data = await CheckFeedbacksHandler.make_unpacked_data_for_seller_output(callback, viewed)
        except UserExistsError:
            traceback.print_exc()
            error_flag = UserExistsError

        except CarExistsError:
            error_flag = CarExistsError

        if offer_ids:
            await redis_module.redis_data.set_data(
                key=f'{str(seller_id)}:last_keyboard_in_seller_pagination',
                value=keyboard_part)

            if callback_data != 'viewed_feedbacks':
                await redis_module.redis_data.set_data(
                    key=f'{str(seller_id)}:return_path_after_delete_car',
                    value='viewed_feedbacks')
            ic()
            await state.set_state(SellerFeedbacks.review_applications)
            await output_seller_requests_module.output_sellers_commodity_page(callback, state, offer_ids)

            # await CheckFeedbacksHandler.check_new_feedbacks(callback, unpacked_output_data)
            return True
        else:
            if error_flag:
                if error_flag == UserExistsError:
                    error_alert_message = Lexicon_module.LEXICON['seller_dont_exists']
                elif error_flag == CarExistsError:
                    error_alert_message = Lexicon_module.LEXICON['car_was_withdrawn_from_sale']
                else:
                    error_alert_message = False
            elif callback_data == 'new_feedbacks':
                callback_alert_message = copy(Lexicon_module\
                                              .LexiconSellerRequests.new_feedbacks_not_found)
            elif callback_data == 'viewed_feedbacks':
                callback_alert_message = copy(Lexicon_module\
                                              .LexiconSellerRequests.viewed_feedbacks_not_found)

            if callback_alert_message:
                if error_alert_message:
                    callback_alert_message = f'{error_alert_message} {callback_alert_message}'
                await callback.answer(text=callback_alert_message)
            return False

        #
        #
        # await redis_module.redis_data.set_data(key=f'{str(seller_id)}:seller__new_active_offers', value=seller_offers)
        #
        # await redis_module.redis_data.set_data(key=f'{str(seller_id)}:seller__viewed_active_offers', value=seller_offers)
        #

    @staticmethod
    async def make_unpacked_data_for_seller_output(callback: CallbackQuery, viewed: bool, from_buyer=False, car_id=None, offer_id=None):
        redis_data = importlib.import_module('utils.redis_for_language')
        cached_requests_module = importlib.import_module('database.data_requests.offers_requests')
        offers = None
        seller_offers = None
        offer = None
        if offer_id:
            offers = [await cached_requests_module.OffersRequester.get_by_offer_id(offer_id)]
        elif from_buyer and car_id:
            offers = await cached_requests_module.OffersRequester.get_for_buyer_id(buyer_id=callback.from_user.id, car_id=car_id)
        else:
            offers = await cached_requests_module.OffersRequester.get_by_seller_id(seller_id_value=callback.from_user.id, viewed_value=viewed)
        ic(offers)
        if offers:
            if viewed == False:
                ic()
                # await OffersRequester.set_viewed_true(seller_offers)
            # card_body_lexicon_part = LEXICON.get('chosen_configuration').get('message_text')
            output_unpacked_data = []
            for offer in offers:
                offer_id = offer.id
                ic(offer)
                try:
                    car = offer.car_id
                except:
                    await cached_requests_module.OffersRequester.delete_offer(offer_id)
                    raise CarExistsError()
                try:
                    buyer = offer.buyer_id
                except:
                    await cached_requests_module.OffersRequester.delete_offer(offer_id)
                    raise UserExistsError()

                output_unpacked_data.append(offer_id)
            # ic(result_part)
            return output_unpacked_data


