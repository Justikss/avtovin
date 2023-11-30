import sqlite3
from datetime import datetime, time

from peewee import JOIN

from icecream import ic

from config_data.config import DATETIME_FORMAT
from database.tables.car_configurations import CarComplectation, CarAdvert, CarModel, CarBrand
from database.tables.offers_history import ActiveOffers, CacheBuyerOffers
from database.tables.seller import Seller

from database.data_requests.person_requests import PersonRequester
from typing import List, Union

from database.tables.user import User
from utils.custom_exceptions.database_exceptions import UserExistsError
from database.db_connect import database, manager



class OffersRequester:
    @staticmethod
    async def get_offer_model(buyer, car):
        '''Асинхронный метод получения модели предложения'''
        query = ActiveOffers.select().where((ActiveOffers.buyer_id == buyer) & (ActiveOffers.car_id == car))
        select_response = await manager.execute(query)
        return select_response if select_response else False

    @staticmethod
    async def set_offer_model(buyer_id, car_id, seller_id):
        '''Асинхронный метод установки модели предложения'''
        if not await OffersRequester.get_offer_model(buyer_id, car_id):
            query = ActiveOffers.insert(car_id=car_id, buyer_id=buyer_id, seller_id=seller_id, viewed=False)
            select_response = await manager.execute(query)
            return select_response if select_response else False
        else:
            raise BufferError('Такая заявка уже создана')

    @staticmethod
    async def get_for_buyer_id(buyer_id: int):
        '''Асинхронный метод получения предложений для покупателя'''
        query = ActiveOffers.select().where(ActiveOffers.buyer == buyer_id)
        buyer_offers = await manager.execute(query)
        return list(buyer_offers) if buyer_offers else False
    ''''''

    @staticmethod
    async def get_by_seller_id(seller_id_value, viewed_value):
        '''Асинхронный метод получения предложений по ID продавца'''
        active_offers = list(await manager.execute(ActiveOffers.select().join(Seller).where(
            (ActiveOffers.viewed == viewed_value) & (Seller.telegram_id == seller_id_value)
        )))
        ic(active_offers)
        return active_offers

    @staticmethod
    async def set_viewed_true(offer_id):
        '''Асинхронный метод установки статуса предложения как просмотренного'''
        update_query = ActiveOffers.update(viewed=True).where(ActiveOffers.id == offer_id)
        updated = await manager.execute(update_query)
        return updated

    @staticmethod
    async def delete_offer(offer_id):
        '''Асинхронный метод удаления предложения'''
        delete_query = ActiveOffers.delete().where(ActiveOffers.id == offer_id)
        deleted = await manager.execute(delete_query)
        return deleted

class CachedOrderRequests:
    @staticmethod
    async def set_cache(buyer_id: Union[str, int], car_data):
        '''Асинхронный метод установки кэша'''
        car_ids = [car['car_id'] for car in car_data]
        query = CacheBuyerOffers.select().where(
            (CacheBuyerOffers.buyer_id == buyer_id) & (CacheBuyerOffers.car_id.in_(car_ids)))
        select_query = await manager.execute(query)
        not_unique_models = [offer.car_id.car_id for offer in select_query] if select_query else []

        data = [{'buyer_id': str(buyer_id), 'car_id': car_part['car_id'], 'message_text': car_part['message_text']}
                for car_part in car_data if car_part['car_id'] not in not_unique_models]
        ic(data)
        if data:
            insert_query = CacheBuyerOffers.insert_many(data)
            await manager.execute(insert_query)
        return True

    @staticmethod
    async def get_cached_brands(buyer_id):
        '''Асинхронный метод получения кэшированных брендов'''
        query = CacheBuyerOffers.select().where(CacheBuyerOffers.buyer_id == buyer_id)
        select_query = await manager.execute(query)
        if select_query:
            select_query = await CachedOrderRequests.check_overtime_requests(select_query)
            result = {f'load_brand_{request.car_id.complectation.model.brand.id}': request.car_id.complectation.model.brand.name for request in select_query}
            return result
        else:
            return set()

    @staticmethod
    async def get_cache(buyer_id, brand=None, car_id=None):
        '''Асинхронный метод получения кэша'''
        query = CacheBuyerOffers.select().join(User).switch(CacheBuyerOffers).join(CarAdvert).where(
            (User.telegram_id == buyer_id) & (CarAdvert.id == car_id) if car_id else None)
        if brand:
            query = query.select().join(CarComplectation).join(CarModel).join(CarBrand).where(CarBrand.id == int(brand))
        select_query = await manager.execute(query)
        result = await CachedOrderRequests.check_overtime_requests(select_query)
        if brand:
            result = {offer.car_id for offer in result}

        return result if result else False
            # if brand:
            #     result = [request.car_id for request in select_query if request.car_id.brand == brand]
            #     return result


    @staticmethod
    async def remove_cache(buyer_id, car_id):
        '''Асинхронный метод удаления кэша'''
        delete_query = CacheBuyerOffers.delete().where(
            (CacheBuyerOffers.buyer_id == buyer_id) & (CacheBuyerOffers.car_id == car_id))
        await manager.execute(delete_query)
        return True

    @staticmethod
    async def check_overtime_requests(select_query):
        '''Асинхронная проверка запросов на превышение времени'''
        requests_to_remove = [request for request in select_query if request.datetime_of_deletion < datetime.now()]
        if requests_to_remove:
            delete_query = CacheBuyerOffers.delete().where(
                CacheBuyerOffers.id.in_([request.id for request in requests_to_remove]))
            await manager.execute(delete_query)
        return [request for request in select_query if request not in requests_to_remove]
