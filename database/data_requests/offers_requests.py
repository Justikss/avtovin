import sqlite3
from peewee import JOIN

from icecream import ic

from database.tables.offers_history import ActiveOffers
from database.tables.seller import Seller
from database.tables.start_tables import db
from database.tables.commodity import Commodity
from database.data_requests.person_requests import PersonRequester
from typing import List, Union



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
    async def set_viewed_false(offers: list):
        with db.atomic():
            update_query = ActiveOffers.update(viewed=True).where(ActiveOffers.id in (offer.id for offer in offers)).execute()
            ic(update_query)
            return update_query

    @staticmethod
    async def delete_offer(offer_id):
        with db.atomic():
            delete_query = ActiveOffers.delete_by_id(offer_id)
            return delete_query