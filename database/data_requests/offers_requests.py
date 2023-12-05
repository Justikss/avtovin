import sqlite3
from datetime import datetime, time

from peewee import JOIN, DoesNotExist

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
        try:
            select_response = await manager.get(query)
        except:
            return False
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
    async def get_for_buyer_id(buyer_id, brand=None, get_brands=False, car_id=None):
        '''Асинхронный метод получения открытых предложений для покупателя'''
        query = ActiveOffers.select().where(ActiveOffers.buyer_id == int(buyer_id))
        if brand:
            query = query.join(CarAdvert).join(CarComplectation).join(CarModel).join(CarBrand).where(CarBrand.id == int(brand))
        elif car_id:
            query = query.where(ActiveOffers.car_id == int(car_id))
        try:
            buyer_offers = list(await manager.execute(query))
        except:
            buyer_offers = None
        ic(buyer_offers)
        if buyer_offers:
            if get_brands:
                ic(get_brands)
                return {f'load_brand_{request.car_id.complectation.model.brand.id}': request.car_id.complectation.model.brand.name for request in buyer_offers}
            else:
                return buyer_offers
        else:
            return False
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

        exists_offers = await OffersRequester.get_for_buyer_id(buyer_id)


        car_ids = [car['car_id'] for car in car_data]
        query = CacheBuyerOffers.select().where(
            (CacheBuyerOffers.buyer_id == buyer_id) & (CacheBuyerOffers.car_id.in_(car_ids)))
        select_query = list(await manager.execute(query))
        if exists_offers:
            select_query = select_query + exists_offers
        not_unique_models = [offer.car_id.id for offer in select_query] if select_query else []

        data = [{'buyer_id': str(buyer_id), 'car_id': car_part['car_id'], 'message_text': car_part['message_text']}
                for car_part in car_data if car_part['car_id'] not in not_unique_models]
        ic(data)
        if data:
            insert_query = CacheBuyerOffers.insert_many(data)
            await manager.execute(insert_query)
        return True

    @staticmethod
    async def get_offer_brands(buyer_id):
        '''Асинхронный метод получения кэшированных брендов'''
        query = CacheBuyerOffers.select().where(CacheBuyerOffers.buyer_id == buyer_id)
        select_query = list(await manager.execute(query))
        if select_query:
            ic(select_query)
            select_query = await CachedOrderRequests.check_overtime_requests(select_query)
            try:
                result = {f'load_brand_{request.car_id.complectation.model.brand.id}': request.car_id.complectation.model.brand.name for request in select_query}
                return result
            except DoesNotExist:
                for offer in select_query:
                    ic(offer, offer.id)
                    await CachedOrderRequests.remove_cache(offer_model=offer)
                    return set()
        else:
            return set()

    @staticmethod
    async def get_cache(buyer_id, brand=None, car_id=None):
        '''Асинхронный метод получения кэша'''
        if buyer_id:
            query = CacheBuyerOffers.select().join(User).where(
                User.telegram_id == buyer_id)
            
            if car_id:
                query = query.switch(CacheBuyerOffers).join(CarAdvert).where(CarAdvert.id == car_id)
            if brand and not car_id:
                query = (query.switch(CacheBuyerOffers).join(CarAdvert).join(CarComplectation).join(CarModel).join(CarBrand)
                         .where(CarBrand.id == int(brand)))

            select_query = await manager.execute(query)
            result = await CachedOrderRequests.check_overtime_requests(select_query)
            if brand:
                result = [offer.car_id for offer in result]

            return result if result else False
            # if brand:
            #     result = [request.car_id for request in select_query if request.car_id.brand == brand]
            #     return result


    @staticmethod
    async def remove_cache(buyer_id=None, car_id=None, offer_model=None):
        '''Асинхронный метод удаления кэша'''
        delete_query = None
        if offer_model:
            ic()
            delete_query = CacheBuyerOffers.delete().where(CacheBuyerOffers == offer_model)
        elif buyer_id and car_id:
            delete_query = CacheBuyerOffers.delete().where(
                (CacheBuyerOffers.buyer_id == int(buyer_id)) & (CacheBuyerOffers.car_id == int(car_id)))
            ic(delete_query)

        if await manager.execute(delete_query):
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
