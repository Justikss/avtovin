import asyncio
import importlib
import sqlite3
import traceback
from datetime import datetime, time

from peewee import JOIN, DoesNotExist

from icecream import ic

from database.tables.car_configurations import CarComplectation, CarAdvert, CarModel, CarBrand
from database.tables.offers_history import ActiveOffers, CacheBuyerOffers, RecommendationsToBuyer, RecommendedOffers
from database.tables.seller import Seller

from typing import List, Union

from database.tables.user import User
from database.db_connect import manager

car_advert_requests_module = importlib.import_module('database.data_requests.car_advert_requests')
cache_redis_module = importlib.import_module('utils.redis_for_language')
cache_redis = cache_redis_module.cache_redis
def to_int(value):
    return int(value) if isinstance(value, str) else value


class OffersRequester:
    @staticmethod
    async def delete_seller_offers(telegram_id):
        if isinstance(telegram_id, str):
            telegram_id = int(telegram_id)

        query = ActiveOffers.select(ActiveOffers.id).where(ActiveOffers.seller_id == telegram_id)
        offers = list(await manager.execute(query))
        offer_ids = [offer.id for offer in offers]
        await OffersRequester.delete_offer(offer_id=offer_ids)

    @cache_redis.cache_update_decorator(model=(RecommendedOffers, CacheBuyerOffers, ActiveOffers), mode='by_scan')
    @staticmethod
    async def delete_all_buyer_history(telegram_id):
        if isinstance(telegram_id, str):
            telegram_id = int(telegram_id)
        await manager.execute(ActiveOffers.delete().where(ActiveOffers.buyer_id == telegram_id))
        await manager.execute(CacheBuyerOffers.delete().where(CacheBuyerOffers.buyer_id == telegram_id))
        await manager.execute(RecommendedOffers.delete().where(RecommendedOffers.buyer == telegram_id))
        await manager.execute(RecommendationsToBuyer.delete().where(RecommendationsToBuyer.buyer == telegram_id))

        buyers = [telegram_id]
        return buyers


    @staticmethod
    async def get_by_offer_id(offer_id):
        if isinstance(offer_id, str):
            offer_id = int(offer_id)
        try:
            result = await manager.get((ActiveOffers
                                            .select(ActiveOffers, CarAdvert, Seller, User)
                                            .join(CarAdvert)
                                            .switch(ActiveOffers)
                                            .join(Seller)
                                            .switch(ActiveOffers)
                                            .join(User)
                                        .where(ActiveOffers.id == offer_id)))

            advert_model = await car_advert_requests_module\
                .AdvertRequester.load_related_data_for_advert(result.car_id)
            result.car_id = advert_model
            ic(result, result.car_id)
        except:
            result = None
        return result

    @staticmethod
    async def get_offer_model(buyer, car):
        '''Асинхронный метод получения модели предложения'''
        query = ActiveOffers.select().join(CarAdvert).where((ActiveOffers.buyer_id == buyer) & (ActiveOffers.car_id == car))
        try:
            select_response = await manager.get(query)
        except:
            return False
        return select_response if select_response else False

    @cache_redis.cache_update_decorator(model=ActiveOffers, mode='by_scan')
    @staticmethod
    async def set_offer_model(buyer_id, car_id, seller_id):
        '''Асинхронный метод установки модели предложения'''

        if not await OffersRequester.get_offer_model(buyer_id, car_id):
            query = ActiveOffers.insert(car_id=car_id, buyer_id=buyer_id, seller_id=seller_id, viewed=False)
            insert_response = await manager.execute(query)
            if insert_response:
                advert_feedbacks_requests_module = importlib.import_module(
                    'database.data_requests.statistic_requests.advert_feedbacks_requests')

                await advert_feedbacks_requests_module\
                    .AdvertFeedbackRequester.write_string(seller_id, car_id)
                return [buyer_id]
            else:
                return False

        else:
            raise BufferError('Такая заявка уже создана')



    @cache_redis.cache_decorator(model=ActiveOffers, id_key='0:buyer_id')
    @staticmethod
    async def get_for_buyer_id(buyer_id, brand=None, car_id=None, count=False, get_brands = False):
        '''Асинхронный метод получения открытых предложений для покупателя'''
        query = (ActiveOffers.select(ActiveOffers.id, ActiveOffers.car_id, CarAdvert.id).join(CarAdvert).switch(ActiveOffers).join(User)
                 .where(ActiveOffers.buyer_id == int(buyer_id)))

        if brand:
            query = (query.switch(CarAdvert).join(CarComplectation).join(CarModel).join(CarBrand)
                     .where(CarBrand.id == int(brand)).order_by(ActiveOffers.id))
        elif car_id:
            query = query.where(ActiveOffers.car_id == int(car_id))
        elif get_brands:
            query = (CarBrand.select().where(CarBrand.id.in_(query.select(CarBrand.id)
                     .switch(CarAdvert).join(CarComplectation).join(CarModel).join(CarBrand))))
        elif count:
            return await manager.count(query)



        buyer_offers = list(await manager.execute(query))

        return buyer_offers


    @staticmethod
    async def get_by_seller_id(seller_id_value, viewed_value):
        '''Асинхронный метод получения предложений по ID продавца'''
        active_offers = list(await manager.execute(ActiveOffers.select(ActiveOffers, Seller, User).join(Seller).switch(ActiveOffers).join(User).where(
            (ActiveOffers.viewed == viewed_value) & (Seller.telegram_id == seller_id_value)).order_by(ActiveOffers.id)))
        ic(active_offers)
        return active_offers

    @staticmethod
    async def set_viewed_true(offer_id):
        '''Асинхронный метод установки статуса предложения как просмотренного'''
        update_query = ActiveOffers.update(viewed=True).where(ActiveOffers.id == offer_id)
        updated = await manager.execute(update_query)
        return updated

    @cache_redis.cache_update_decorator(model=ActiveOffers, mode='by_scan')
    @staticmethod
    async def delete_offer(offer_id=None, advert_id=None, buyer_id=None):
        '''Асинхронный метод удаления предложения'''
        ic(offer_id, advert_id, buyer_id)
        if offer_id:
            if isinstance(offer_id, list):
                condition = ActiveOffers.id.in_([to_int(id_element) if isinstance(id_element, str) else id_element
                                                 for id_element in offer_id])
            else:
                offer_id = to_int(offer_id)
                condition = ActiveOffers.id == offer_id

        elif advert_id and buyer_id:
            if isinstance(advert_id, list):
                condition = ((ActiveOffers.car_id.in_([to_int(id_element) if isinstance(id_element, str) else id_element
                                                     for id_element in advert_id])) & (ActiveOffers.buyer_id == buyer_id))
            else:
                advert_id = to_int(advert_id)
                buyer_id = to_int(buyer_id)
                condition = ActiveOffers.id.in_(ActiveOffers.select(ActiveOffers.id)
                                                .where((ActiveOffers.car_id == advert_id) &
                                                        (ActiveOffers.buyer_id == buyer_id)))
        elif advert_id:
            if not isinstance(advert_id, list):
                advert_id = [advert_id]

            condition = ActiveOffers.car_id.in_([to_int(id_element) if isinstance(id_element, str) else id_element
                                                     for id_element in advert_id])


        else:
            return
        ic(condition.__dict__)

        selected = list(await manager.execute(ActiveOffers.select(ActiveOffers, User).join(User).where(condition)))
        ic(selected)
        buyer_ids = list({offer.buyer_id.telegram_id for offer in selected})
        ic(buyer_ids)
        await manager.execute(ActiveOffers.delete()
                            .where(ActiveOffers.id.in_(selected)))
        return buyer_ids

class CachedOrderRequests:
    @staticmethod
    async def get_by_advert_and_seller(advert_id, seller_id):
        if not isinstance(advert_id, list):
            advert_id = [advert_id]
        query = (CacheBuyerOffers.select(CacheBuyerOffers, User, CarAdvert).join(CarAdvert).join(Seller).switch(CacheBuyerOffers).join(User)
                 .where((CarAdvert.id.in_(advert_id)) & (CarAdvert.seller == seller_id)))
        result = list(await manager.execute(query))
        return result

    @cache_redis.cache_decorator(model=CacheBuyerOffers, id_key='0:buyer_id')
    @staticmethod
    async def get_cache(buyer_id, brand=None, car_id=None, count=False, get_brands=False):
        '''Асинхронный метод получения кэша'''
        if buyer_id:
            query = CacheBuyerOffers.select(CacheBuyerOffers, CarAdvert, User).join(CarAdvert).switch(CacheBuyerOffers).join(User).where(
                User.telegram_id == buyer_id)

            if count or get_brands:
                query = query.where(CacheBuyerOffers.datetime_of_deletion > datetime.now())
            if count:
                return await manager.count(query)
            elif get_brands:
                query = (CarBrand.select().where(CarBrand.id.in_(query.select(CarBrand.id)
                         .switch(CarAdvert).join(CarComplectation).join(CarModel).join(CarBrand))))
            else:
                query = query.switch(CarAdvert).join(CarComplectation).join(CarModel).join(CarBrand)

            ic(brand, buyer_id, car_id)
            if car_id:
                query = query.where(CarAdvert.id == car_id)
            if brand and not car_id:
                query = (query.where(CarBrand.id == int(brand)))

            result = list(await manager.execute(query))
            if not get_brands:
                result = await CachedOrderRequests.check_overtime_requests(result)
                from database.data_requests.car_advert_requests import AdvertRequester
                tasks = [AdvertRequester.load_related_data_for_advert(offer.car_id) for offer in result]
                await asyncio.gather(*tasks)

            return result if result else False

    @cache_redis.cache_update_decorator(model=CacheBuyerOffers, mode='by_scan')
    @staticmethod
    async def set_cache(buyer_id: Union[str, int], car_data):
        '''Асинхронный метод установки кэша'''

        exists_offers = await OffersRequester.get_for_buyer_id(buyer_id)


        car_ids = car_data
        query = CacheBuyerOffers.select(CacheBuyerOffers, CarAdvert).join(CarAdvert).where(
            (CacheBuyerOffers.buyer_id == buyer_id) & (CacheBuyerOffers.car_id.in_(car_ids)))
        select_query = list(await manager.execute(query))
        if exists_offers:
            select_query = select_query + exists_offers
        try:
            not_unique_models = [offer.car_id.id for offer in select_query] if select_query else []
        except:
            not_unique_models = []
        data = [{'buyer_id': int(buyer_id), 'car_id': car_part}
                for car_part in car_data if car_part not in not_unique_models]

        ic()
        ic(data)
        if data:
            insert_query = CacheBuyerOffers.insert_many(data)
            ic(insert_query)
            try:
                await manager.execute(insert_query)
                buyer_id = [buyer_id]
                return buyer_id
            except:
                # traceback.print_exc()
                pass


    @cache_redis.cache_update_decorator(model=CacheBuyerOffers, mode='by_scan')
    @staticmethod
    async def remove_cache(buyer_id=None, car_id=None, offer_model=None):
        '''Асинхронный метод удаления кэша'''
        delete_query = None
        buyers = []
        ic(car_id, buyer_id, offer_model)
        if offer_model:
            if isinstance(offer_model, list):
                delete_condition = CacheBuyerOffers.id.in_(offer_model)
            else:
                delete_condition = CacheBuyerOffers == offer_model
                offer_model = [offer_model]
            buyers = list({offer_model_element.buyer_id.telegram_id for offer_model_element in offer_model})

            ic(buyers)
            ic(offer_model[0].buyer_id)
            ic()
            delete_query = CacheBuyerOffers.delete().where(delete_condition)
        elif buyer_id and car_id:
            ic()
            ic(buyers)
            buyers = [buyer_id]
            delete_query = CacheBuyerOffers.delete().where(
                (CacheBuyerOffers.buyer_id == int(buyer_id)) & (CacheBuyerOffers.car_id == int(car_id)))
            ic(delete_query)
        else:
            return
        delete_response = await manager.execute(delete_query)
        if delete_response:
            return buyers


    @staticmethod
    async def check_overtime_requests(select_query):
        '''Асинхронная проверка запросов на превышение времени'''
        if not select_query:
            return
        ic(select_query[0].datetime_of_deletion)
        requests_to_remove = [request for request in select_query if request.datetime_of_deletion < datetime.now()]
        if requests_to_remove:
            if isinstance(requests_to_remove[0], CacheBuyerOffers):
                await CachedOrderRequests.remove_cache(offer_model=requests_to_remove)
            elif isinstance(requests_to_remove[0], RecommendedOffers):
                from database.data_requests.recomendations_request import RecommendationParametersBinder
                await RecommendationParametersBinder.remove_recommendation_by_recommendation_id(requests_to_remove)
        result = [request for request in select_query if request not in requests_to_remove]

        return result

