import importlib
import time

from aiogram.types import CallbackQuery
from handlers.state_handlers.choose_car_for_buy.hybrid_handlers import CommodityRequester
from handlers.callback_handlers.buy_part.callback_handler_start_buy import PersonRequester
from database.data_requests.offers_requests import OffersRequester
from database.data_requests.tariff_to_seller_requests import TariffToSellerBinder, SellerWithoutTariffException, TariffExpiredException
from keyboards.inline.kb_creator import InlineCreator
from utils.Lexicon import LEXICON
from utils.user_notification import send_notification


async def confirm_from_seller(callback: CallbackQuery):
    redis_data = importlib.import_module('utils.redis_for_language')

    callback_encoding = callback.data.split(':')
    #cars_id_range = callback_encoding[1:-2]
    cars_id_range = [int(car_id) for car_id in callback_encoding[1:-2]]

    print('raw cars id range', cars_id_range)
    # cars_id_range = [int(car_id) for car_id in cars_id_range]

    seller_id = callback.from_user.id

    print(callback_encoding)
    buyer_id = int(callback_encoding[-1])
    print('car id rangeeeeee', cars_id_range)


    need_cars = list()
    # for car_id in cars_id_range:
    need_cars = CommodityRequester.get_car_for_offer(seller_id=seller_id, car_range_id=cars_id_range)
    # if need_car:
    #     need_cars.append(need_car)




    redis_key = str(buyer_id) + ':active_non_confirm_offers'

    active_non_confirm_offers = await redis_data.redis_data.get_data(
        key=redis_key,
        use_json=True
    )

    if active_non_confirm_offers:
        lexicon_code = None
        try:
            query = TariffToSellerBinder.feedback_waste(telegram_id=callback.from_user.id)
        except SellerWithoutTariffException:
            lexicon_code = 'seller_without_tariff'
        except TariffExpiredException:
            lexicon_code = 'seller_tarriff_expired'

        else:
            print('qara: ', query)
            alert_lexicon_code = 'success_notification'
            if not need_cars:
                await callback.answer(text=LEXICON["seller_haven't_this_car"])
                return
            else:

                match_result = await OffersRequester.match_check(user_id=callback.from_user.id,
                                                                 cars_id_range=cars_id_range)

                if match_result:

                    a = await OffersRequester.store_data(buyer_id=buyer_id, seller_id=seller_id, cars=need_cars)

                else:
                    alert_lexicon_code = 'non_actiallity'

            cars_id_range = [str(car_id) for car_id in cars_id_range]
            need_message_data = next((key for key, value in active_non_confirm_offers.items() if value == ':'.join(cars_id_range)), None)
            if not need_message_data:
                time.sleep(2)
                need_message_data = next((key for key, value in active_non_confirm_offers.items() if value == ':'.join(cars_id_range)),
                     None)

            print('need_message id', need_message_data)
            print('cars_id_range', ':'.join(cars_id_range))
            active_non_confirm_offers.pop(need_message_data)
            print(need_message_data)


            need_message_data = need_message_data.split(':')

            chat_id = need_message_data[1]
            message_id = need_message_data[0]


            await send_notification(callback=callback, user_status='buyer', chat_id=chat_id)


            await callback.answer(LEXICON[alert_lexicon_code])
            await callback.message.chat.delete_message(message_id=message_id)

            await redis_data.redis_data.set_data(
                key=redis_key,
                value=active_non_confirm_offers
            )
        if lexicon_code:
            await callback.answer(LEXICON[lexicon_code], show_alert=True)
    else:
        print('gay')

    await callback.answer()

    #'confirm_from_seller:' + cars_id_range + ':to_buyer' + buyer_id)