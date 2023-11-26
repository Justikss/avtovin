from datetime import datetime

from database.tables import db
from database.tables.offers_history import CacheBuyerOffers


class UserCarCacheRequester:
    @staticmethod
    async def store_data(car_models, buyer_id):
        # , 'car_brand': car_model.brand
        data = [{'buyer_id': buyer_id, 'car_id': car_model.car_id} for car_model in car_models]
        with db.atomic():
            query = CacheBuyerOffers.insert_many(*data).execute()
            if query:
                return True

    @staticmethod
    async def get_data_by_buyer_id(buyer_id):
        with db.atomic():
            query_response = (CacheBuyerOffers.select().where(CacheBuyerOffers.buyer_id == buyer_id))
            white_models = []
            if query_response:
                for model in query_response:
                    if model.datetime_of_deletion > datetime.now():
                        delete_response = CacheBuyerOffers.delete_by_id(model.id).execute()
                    else:
                        white_models.append(model)

            return reversed(white_models)

    @staticmethod
    async def delete_cache_element(buyer_id, car_id):
        with db.atomic():
            query = CacheBuyerOffers.delete().where((CacheBuyerOffers.buyer_id == buyer_id) &
                                                    (CacheBuyerOffers.car_id == car_id))
            if query:
                return True

