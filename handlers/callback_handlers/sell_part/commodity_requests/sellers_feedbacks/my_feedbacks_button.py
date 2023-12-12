import importlib
from abc import ABC
from copy import copy

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.data_requests.car_advert_requests import AdvertRequester
from handlers.utils.create_advert_configuration_block import create_advert_configuration_block
from states.seller_feedbacks_states import SellerFeedbacks
from utils.lexicon_utils.Lexicon import LEXICON, LexiconSellerRequests
from handlers.callback_handlers.sell_part.commodity_requests.pagination_handlers import output_sellers_commodity_page
from utils.custom_exceptions.database_exceptions import UserExistsError, CarExistsError
from utils.get_currency_sum_usd import get_valutes
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
        error_flag = False
        error_alert_message = False
        ic(callback.data)
        ic()
        if callback.data in ('new_feedbacks', 'viewed_feedbacks'):
            redis_key = str(callback.from_user.id) + ':user_state'
            await redis_module.redis_data.set_data(redis_key, value='sell')

        await redis_module.redis_data.delete_key(key=f'{str(seller_id)}:seller_requests_pagination')

        if callback_data == 'new_feedbacks':
            viewed = False
            keyboard_part = LexiconSellerRequests.check_new_feedbacks_buttons
        elif 'viewed_feedbacks' in (command, callback_data):
            viewed = True
            keyboard_part = LexiconSellerRequests.check_viewed_feedbacks_buttons

        try:
            unpacked_output_data = await CheckFeedbacksHandler.make_unpacked_data_for_seller_output(callback, viewed)
        except UserExistsError:
            unpacked_output_data = False
            error_flag = UserExistsError

        except CarExistsError:
            error_flag = CarExistsError
            unpacked_output_data = False

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
            if error_flag:
                if error_flag == UserExistsError:
                    error_alert_message = LEXICON['seller_dont_exists']
                elif error_flag == CarExistsError:
                    error_alert_message = LEXICON['car_was_withdrawn_from_sale']
                else:
                    error_alert_message = False
            elif callback_data == 'new_feedbacks':
                callback_alert_message = copy(LexiconSellerRequests.new_feedbacks_not_found)
            elif callback_data == 'viewed_feedbacks':
                callback_alert_message = copy(LexiconSellerRequests.viewed_feedbacks_not_found)

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
    async def make_unpacked_data_for_seller_output(callback: CallbackQuery, viewed: bool, from_buyer=False, car_id=None):
        redis_data = importlib.import_module('utils.redis_for_language')
        cached_requests_module = importlib.import_module('database.data_requests.offers_requests')

        if from_buyer and car_id:
            seller_offers = await cached_requests_module.OffersRequester.get_for_buyer_id(buyer_id=callback.from_user.id, car_id=car_id)
        else:
            seller_offers = await cached_requests_module.OffersRequester.get_by_seller_id(seller_id_value=callback.from_user.id, viewed_value=viewed)
        if seller_offers:
            if viewed == False:
                ic()
                # await OffersRequester.set_viewed_true(seller_offers)
            card_body_lexicon_part = LEXICON.get('chosen_configuration').get('message_text')
            for_seller_lexicon_part = LEXICON['confirm_from_seller']['message_text']
            output_unpacked_data = []
            for offer in seller_offers:
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

                fullname = f'''{buyer.surname} {buyer.name} {buyer.patronymic if buyer.patronymic else ''}'''
                ic(offer_id)
                card_startswith = f'''{for_seller_lexicon_part['feedback_header'].replace('X', str(offer_id))}\n{for_seller_lexicon_part['from_user'].replace('X', f'@{buyer.username}')}\n{for_seller_lexicon_part['tendered'].replace('X', str(car.id))}\n{for_seller_lexicon_part['contacts'].replace('N', fullname).replace('P', buyer.phone_number)}'''

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

                photo_album = await AdvertRequester.get_photo_album_by_advert_id(car.id, get_list=True)

                result_part = {'offer_id': offer_id, 'car_id': car.id, 'message_text': result_string, 'album': photo_album}
                output_unpacked_data.append(result_part)
                ic(result_part)
            return output_unpacked_data


