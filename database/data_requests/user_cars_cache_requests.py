from datetime import datetime

from database.tables.offers_history import CacheBuyerOffers
from database.db_connect import database, manager



class UserCarCacheRequester:
    @staticmethod
    async def store_data(car_models, buyer_id):
        '''Асинхронный метод для сохранения данных автомобилей покупателя в кэш'''
        data = [{'buyer_id': buyer_id, 'car_id': car_model.car_id} for car_model in car_models]
        insert_query = CacheBuyerOffers.insert_many(data)
        await manager.execute(insert_query)
        return True

    @staticmethod
    async def get_data_by_buyer_id(buyer_id):
        '''Асинхронный метод для получения данных кэша автомобилей покупателя по его ID'''
        query_response = CacheBuyerOffers.select().where(CacheBuyerOffers.buyer_id == buyer_id)
        models = await manager.execute(query_response)
        white_models = [model for model in models if model.datetime_of_deletion > datetime.now()]
        for model in white_models:
            if model.datetime_of_deletion <= datetime.now():
                delete_query = CacheBuyerOffers.delete().where(CacheBuyerOffers.id == model.id)
                await manager.execute(delete_query)
        return list(reversed(white_models))

    @staticmethod
    async def delete_cache_element(buyer_id, car_id):
        '''Асинхронный метод для удаления элемента кэша автомобилей покупателя'''
        delete_query = CacheBuyerOffers.delete().where((CacheBuyerOffers.buyer_id == buyer_id) &
                                                       (CacheBuyerOffers.car_id == car_id))
        await manager.execute(delete_query)
        return True