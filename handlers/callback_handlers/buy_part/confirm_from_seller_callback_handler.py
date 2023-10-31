import importlib
import time

from aiogram.types import CallbackQuery
from handlers.state_handlers.choose_car_for_buy.hybrid_handlers import CommodityRequester
from handlers.callback_handlers.buy_part.callback_handler_start_buy import PersonRequester
from database.data_requests.offers_requests import OffersRequester
from utils.Lexicon import LEXICON


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

    if not need_cars:
        await callback.answer(text=LEXICON["seller_haven't_this_car"])
        #return
    else:
        # buyer_person = PersonRequester.get_user_for_id(user_id=buyer_id, user=True)
        # seller_person = PersonRequester.get_user_for_id(user_id=seller_id, seller=True)
        # print(buyer_person)
        # print(seller_id)
        # buyer_person = buyer_person[0]
        # seller_person = seller_person[0]




        a = await OffersRequester.store_data(buyer_id=buyer_id, seller_id=seller_id, cars=need_cars)
        print(a)


        redis_key = str(buyer_id) + ':active_non_confirm_offers'

        active_non_confirm_offers = await redis_data.redis_data.get_data(
            key=redis_key,
            use_json=True
        )

        if active_non_confirm_offers:
            print(active_non_confirm_offers)
            print(cars_id_range)
            cars_id_range = list(map(str, cars_id_range))
            print(cars_id_range)
            # if len(cars_id_range) == 1:
            #     cars_id_range = str(cars_id_range[0])
            #
            # else:
            #     cars_id_range = (str(cars_id) for cars_id in cars_id_range)
            #deleted_message = [key for key, value in active_non_confirm_offers.items() if str(value) == cars_id_range]
            # print('del mes ', deleted_message)
            # deleted_message = deleted_message[0]
            # print('del mes2 ', deleted_message)

            need_message_id = next((key for key, value in active_non_confirm_offers.items() if value == ':'.join(cars_id_range)), None)
            if not need_message_id:
                time.sleep(2)
                need_message_id = next((key for key, value in active_non_confirm_offers.items() if value == ':'.join(cars_id_range)),
                     None)

            print('need_message id', need_message_id)
            print('cars_id_range', ':'.join(cars_id_range))
            active_non_confirm_offers.pop(need_message_id)
            print(need_message_id)
            await callback.answer(LEXICON['success_notification'])
            await callback.message.chat.delete_message(message_id=need_message_id)

            await redis_data.redis_data.set_data(
                key=redis_key,
                value=active_non_confirm_offers
            )
        else:
            print('gay')

        await callback.answer()

        #'confirm_from_seller:' + cars_id_range + ':to_buyer' + buyer_id)