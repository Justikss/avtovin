import sqlite3
from datetime import datetime, time

from peewee import JOIN

from icecream import ic

from config_data.config import DATETIME_FORMAT
from database.tables.offers_history import ActiveOffers, CacheBuyerOffers
from database.tables.seller import Seller
from database.tables.start_tables import db
from database.tables.commodity import Commodity
from database.data_requests.person_requests import PersonRequester
from typing import List, Union

from database.tables.user import User
from utils.custom_exceptions.database_exceptions import UserExistsError


class OffersRequester:
    @staticmethod
    async def get_by_offer_id(active_offer_id):
        with db.atomic():
            select_request = ActiveOffersToCars.select().where(ActiveOffersToCars.offer_id == active_offer_id)
            select_request = list(select_request)
            if select_request:
                return select_request
            else:
                return False

    ''''''''''''''''''
    @staticmethod
    async def get_offer_model(buyer, car):
        with db.atomic():
            ic()
            select_response = ActiveOffers.select().where((ActiveOffers.buyer_id == buyer) & (ActiveOffers.car_id == car))
            ic(select_response)
            if select_response:
                return select_response
            else:
                return False

    @staticmethod
    async def set_offer_model(buyer_id, car_id, seller_id):
        with db.atomic():
            ic()
            if not await OffersRequester.get_offer_model(buyer_id, car_id):
                ic()
                select_response = ActiveOffers.insert(car_id=car_id, buyer_id=buyer_id, seller_id=seller_id, viewed=False).execute()
                # ic.configureOutput(prefix='set_method ')
                # ic(select_response)
                if select_response:
                    return select_response
                else:
                    raise Exception('Неудачная вставка в ActiveOffers')


            else:
                raise BufferError('Такая заявка уже создана')


    ''''''''''''''''''
    @staticmethod
    async def store_data(seller_id, buyer_id, cars: list, db=db):

        # try:
        with db.atomic():
            seller = PersonRequester.get_user_for_id(user_id=seller_id, seller=True)
            buyer = PersonRequester.get_user_for_id(user_id=buyer_id, user=True)

            # Создать новый заказ с продавцом и покупателем
            print(seller, buyer)
            order = ActiveOffers.create(seller=seller[0], buyer=buyer[0])

            # Для каждой машины в списке
            for car in cars:
                # Найти машину по ее id
                car = Commodity.get_by_id(car)
                print('car: ', type(car), 'order: ', type(order))

                ActiveOffersToCars.create(car_id=car, offer_id=order)


            return order.id


    @staticmethod
    async def get_for_buyer_id(buyer_id: int):
        with db.atomic():
            buyer_offers = ActiveOffers.select().where(ActiveOffers.buyer == buyer_id)
            buyer_offers = list(buyer_offers)
        if buyer_offers:
            return buyer_offers
        else:
            return False

    @staticmethod
    async def get_by_seller_id(seller_id_value, viewed_value):
        with db.atomic():
            result = []
            seller = Seller.get_by_id(seller_id_value)
            ic(seller.telegram_id)
            ic(seller.active_offers)
            for offer in (seller.active_offers):
                if offer.viewed == viewed_value:
                    result.append(offer)

            return result


    @staticmethod
    async def set_viewed_true(offer_id):
        with db.atomic():
            update_query = ActiveOffers.update(viewed=True).where((ActiveOffers.id == offer_id)).execute()
            ic(update_query)
            return update_query

    @staticmethod
    async def delete_offer(offer_id):
        with db.atomic():
            delete_query = ActiveOffers.delete_by_id(offer_id)
            return delete_query

class CachedOrderRequests:
    @staticmethod
    async def set_cache(buyer_id: Union[str, int], car_data):
        car_ids = [car['car_id'] for car in car_data]
        ic(car_ids)
        with db.atomic():
            ic(car_data)
            select_query = list(CacheBuyerOffers.select().where((CacheBuyerOffers.buyer_id == buyer_id) &\
                                                                (CacheBuyerOffers.car_id.in_([car['car_id'] for car in car_data]))))
            if select_query:
                not_unique_models = [offer.car_id.car_id for offer in select_query]
                ic(not_unique_models)
                # data = [{'buyer_id': buyer_id, 'car_id': car_part['car_id'], 'message_text': car_part['message_text']}
                #         for car_part in car_data
                #         if car_part['car_id'] not in not_unique_models]
            else:
                not_unique_models = None
                # data = [{'buyer_id': buyer_id, 'car_id': car_part['car_id'], 'message_text': car_part['message_text']}
                #         for car_part in car_data]

            data = []
            for car_part in car_data:
                if not (not_unique_models and car_part['car_id'] not in not_unique_models):
                    data.append({'buyer_id': buyer_id, 'car_id': car_part['car_id'], 'message_text': car_part['message_text']})

        with db.atomic():
            insert_query = CacheBuyerOffers.insert_many(data).execute()

            return insert_query

    @staticmethod
    async def get_cached_brands(buyer_id):
        with db.atomic():
            ic(buyer_id)
            select_query = list(CacheBuyerOffers.select().where(CacheBuyerOffers.buyer_id == buyer_id).execute())

            if select_query:
                ic(select_query)
                select_query = await CachedOrderRequests.check_overtime_requests(select_query)

                result = {request.car_id.brand for request in select_query}
                ic(result)
                return result

    @staticmethod
    async def get_cache(buyer_id, brand=None, car_id=None):
        with db.atomic():
            select_query = list(CacheBuyerOffers.select().where((CacheBuyerOffers.buyer_id == buyer_id) & (CacheBuyerOffers.car_id == car_id) if car_id else None).execute())

            if select_query:
                ic(select_query)
                if brand:
                    result = []
                    for request in select_query:
                        if request.car_id.brand == brand:
                            result.append(request.car_id)
                    ic(result)
                    return result
                select_query = await CachedOrderRequests.check_overtime_requests(select_query)

                return select_query


    @staticmethod
    async def remove_cache(buyer_id, car_id):
        with db.atomic():
            delete_query = CacheBuyerOffers.delete().where((CacheBuyerOffers.buyer_id == buyer_id) & (CacheBuyerOffers.car_id == car_id)).execute()
            ic(delete_query)
            return delete_query

    @staticmethod
    async def check_overtime_requests(select_query):
        requests_to_remove = []
        for request in select_query:
            ic(request.buyer_id, request.datetime_of_deletion)
            if request.datetime_of_deletion < datetime.now():
                requests_to_remove.append(select_query.pop(request))

        if requests_to_remove:
            with db.atomic():
                CacheBuyerOffers.delete().where(
                    CacheBuyerOffers.id in (request.id for request in requests_to_remove))

        return select_query