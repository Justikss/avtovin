import asyncio
import importlib

from peewee import fn, JOIN
from peewee_async import Manager

from database.data_requests.utils.raw_sql_handler import get_top_advert_parameters
from database.db_connect import manager
from database.tables.car_configurations import CarAdvert, CarComplectation, CarModel, CarState, CarColor, CarMileage, \
    CarYear, CarBrand
from database.tables.offers_history import SellerFeedbacksHistory
from database.tables.seller import Seller
from database.tables.statistic_tables.advert_parameters import AdvertParameters


class AdvertFeedbackRequester:
    @staticmethod
    async def get_or_create_by_parameters(color_id, complectation_id, only_get=False):
        ic(color_id, complectation_id)
        if only_get:
            manager_method = manager.get_or_none
        else:
            manager_method = manager.get_or_create

        query = await manager_method(AdvertParameters,
                                     complectation=complectation_id,
                                     color=color_id)

        # if not only_get:
        #     query = query[0]
        #
        if isinstance(query, tuple):
            query = query[0]

        return query

    @staticmethod
    async def extract_parameters(advert: CarAdvert):
        parameters = await manager.get_or_create(AdvertParameters, complectation=advert.complectation,
                                                 color=advert.color)

        return parameters

    @staticmethod
    async def write_string(seller_id, advert: CarAdvert | str | int):
        car_advert_requests_module = importlib.import_module('database.data_requests.car_advert_requests')

        if not isinstance(advert, CarAdvert):
            if isinstance(advert, str):
                advert = int(advert)
            advert = await car_advert_requests_module.AdvertRequester.get_where_id(advert)

        parameters = await AdvertFeedbackRequester.extract_parameters(advert)
        await manager.execute(SellerFeedbacksHistory.insert(seller_id=seller_id, advert_parameters=parameters[0]))


    @staticmethod
    async def update_parameters_to_null_by_specific_parameter(table_name, model_id):
        base_query = SellerFeedbacksHistory.select(SellerFeedbacksHistory.id).join(AdvertParameters)\
                                                                             .join(CarComplectation).join(CarModel)
        if table_name == 'color':
            base_query = base_query.where(AdvertParameters.color.in_(model_id))
        if table_name == 'complectation':
            base_query = base_query.where(CarComplectation.id.in_(model_id))
        if model_id:
            base_query = base_query.where(CarModel.id.in_(model_id))
        if table_name == 'brand':
            base_query = base_query.where(CarModel.brand.in_(model_id))

        await manager.execute(SellerFeedbacksHistory().update(advert_parameters=None)\
                                                      .where(SellerFeedbacksHistory.id.in_(base_query)))

    @staticmethod
    async def get_top_advert_parameters(top_direction='top', manager=manager):
        query = (SellerFeedbacksHistory
                 .select(SellerFeedbacksHistory.advert_parameters,
                         # AdvertParameters,
                         # CarComplectation,
                         # CarModel,
                         # CarBrand,
                         # SellerFeedbacksHistory.seller_id,
                         fn.COUNT(SellerFeedbacksHistory.id).alias('feedbacks_count'),
                         Seller)
                 .join(Seller, on=(SellerFeedbacksHistory.seller_id == Seller.telegram_id))
                 .switch(SellerFeedbacksHistory)
                 .join(AdvertParameters)
                 .join(CarComplectation)
                 .join(CarModel)
                 .join(CarBrand)
                 .where(SellerFeedbacksHistory.advert_parameters.is_null(False))
                 .group_by(SellerFeedbacksHistory.advert_parameters, Seller)
                 .order_by(fn.COUNT(SellerFeedbacksHistory.id).desc()))

        if top_direction == 'bottom':
            query = query.order_by(fn.COUNT(SellerFeedbacksHistory.id))

        if isinstance(manager, Manager):
            top_10 = list(await manager.execute(query.limit(10)))

        else:
            top_10 = list(manager.execute(query.limit(10)))

        ic(top_10, len(top_10))
        # ic([model.__dict__ for model in top_10])
        return top_10


    @staticmethod
    async def get_seller_feedback_by_id(feedback_id):
        if not isinstance(feedback_id, int):
            feedback_id = int(feedback_id)
        return await manager.get_or_none(SellerFeedbacksHistory.select(SellerFeedbacksHistory, AdvertParameters,
                                                                       Seller).where(
                                                                            SellerFeedbacksHistory.id == feedback_id))