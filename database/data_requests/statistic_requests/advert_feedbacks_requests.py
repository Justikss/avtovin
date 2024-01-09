import importlib

from peewee import fn, JOIN

from database.db_connect import manager
from database.tables.car_configurations import CarAdvert, CarComplectation, CarModel
from database.tables.offers_history import SellerFeedbacksHistory
from database.tables.seller import Seller
from database.tables.statistic_tables.advert_parameters import AdvertParameters


class AdvertFeedbackRequester:
    @staticmethod
    async def get_or_create_by_parameters(state_id, color_id, mileage_id, year_id, complectation_id, only_get=False):
        ic(state_id, color_id, mileage_id, year_id, complectation_id)
        if only_get:
            manager_method = manager.get_or_none
        else:
            manager_method = manager.get_or_create

        query = await manager_method(AdvertParameters,
                                     complectation=complectation_id,
                                     state=state_id, color=color_id,
                                     mileage=mileage_id, year=year_id)

        # if not only_get:
        #     query = query[0]
        #
        if isinstance(query, tuple):
            query = query[0]

        return query

    @staticmethod
    async def extract_parameters(advert: CarAdvert):
        parameters = await manager.get_or_create(AdvertParameters, complectation=advert.complectation, state=advert.state,
                                                 color=advert.color,
                                    mileage=advert.mileage, year=advert.year)

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
    async def get_top_advert_parameters(top_direction='top'):
        # Фильтруем записи, где advert_parameters не равно null
        # query = (SellerFeedbacksHistory
        #          .select(SellerFeedbacksHistory.advert_parameters,
        #                  fn.COUNT(SellerFeedbacksHistory.id).alias('feedbacks_count'),
        #                  Seller)
        #          .join(Seller, on=(SellerFeedbacksHistory.seller_id == Seller.telegram_id))
        #          .where(SellerFeedbacksHistory.advert_parameters.is_null(False))
        #          .group_by(SellerFeedbacksHistory.advert_parameters, Seller)
        #          .order_by(fn.COUNT(SellerFeedbacksHistory.id).desc()))
        #
        # if top_direction == 'bottom':
        #     query = query.order_by(fn.COUNT(SellerFeedbacksHistory.id))
        #
        # top_10 = list(await manager.execute(query.dicts().limit(10)))
        query = (SellerFeedbacksHistory
                 .select(SellerFeedbacksHistory.advert_parameters,
                         SellerFeedbacksHistory.seller_id,
                         Seller,
                         AdvertParameters,
                         fn.COUNT(SellerFeedbacksHistory.id).alias('feedbacks_count'))
                 .join(Seller, JOIN.LEFT_OUTER, on=(SellerFeedbacksHistory.seller_id == Seller.telegram_id))
                 .switch(SellerFeedbacksHistory)
                 .join(AdvertParameters, JOIN.LEFT_OUTER,
                       on=(SellerFeedbacksHistory.advert_parameters == AdvertParameters.id))
                 .where(SellerFeedbacksHistory.advert_parameters.is_null(False))
                 .group_by(SellerFeedbacksHistory.advert_parameters, SellerFeedbacksHistory.seller_id, Seller,
                           AdvertParameters)
                 .order_by(fn.COUNT(SellerFeedbacksHistory.id).desc()))

        if top_direction == 'bottom':
            query = query.order_by(fn.COUNT(SellerFeedbacksHistory.id))

        # Получение результатов запроса
        top_10_raw = await manager.execute(query.dicts().limit(10))

        top_10 = []
        for item in top_10_raw:
            seller = Seller()
            advert_params = AdvertParameters()
            feedback_history = SellerFeedbacksHistory()

            for key in Seller._meta.fields.keys():
                if key in item:
                    setattr(seller, key, item[key])

            for key in AdvertParameters._meta.fields.keys():
                if key in item:
                    setattr(advert_params, key, item[key])

            for key in SellerFeedbacksHistory._meta.fields.keys():
                if key in item:
                    setattr(feedback_history, key, item[key])

            feedback_history.seller = seller
            feedback_history.advert_parameters = advert_params
            feedback_history.feedbacks_count = item['feedbacks_count']
            top_10.append(feedback_history)

        ic(top_10)
        return top_10

    @staticmethod
    async def get_seller_feedback_by_id(feedback_id):
        if not isinstance(feedback_id, int):
            feedback_id = int(feedback_id)
        return await manager.get_or_none(SellerFeedbacksHistory.select(SellerFeedbacksHistory, AdvertParameters,
                                                                       Seller).where(
                                                                            SellerFeedbacksHistory.id == feedback_id))