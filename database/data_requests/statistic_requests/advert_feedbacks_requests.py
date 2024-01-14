import asyncio
import importlib
import operator
from datetime import timedelta, datetime
from functools import reduce

from peewee import fn, JOIN, SQL
from peewee_async import Manager

from database.data_requests.utils.raw_sql_handler import get_top_advert_parameters
from database.db_connect import manager
from database.tables.car_configurations import CarAdvert, CarComplectation, CarModel, CarState, CarColor, CarMileage, \
    CarYear, CarBrand, CarEngine
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
                 .select(AdvertParameters,
                         # AdvertParameters,
                         # CarComplectation,
                         # CarModel,
                         # CarBrand,
                         # SellerFeedbacksHistory.seller_id,
                         fn.COUNT(SellerFeedbacksHistory.id).alias('count'),
                         Seller)
                 .join(Seller, on=(SellerFeedbacksHistory.seller_id == Seller.telegram_id))
                 .switch(SellerFeedbacksHistory)
                 .join(AdvertParameters)
                 .join(CarComplectation)
                 .join(CarModel)
                 .join(CarBrand)
                 .where(SellerFeedbacksHistory.advert_parameters.is_null(False))
                 .group_by(AdvertParameters, Seller)
                 .order_by(fn.COUNT(SellerFeedbacksHistory.id).desc()))

        if top_direction == 'bottom':
            query = query.order_by(fn.COUNT(SellerFeedbacksHistory.id))
        ic(type(manager), isinstance(manager, Manager))
        if isinstance(manager, Manager):
            top_10 = list(await manager.execute(query.limit(10)))
        else:
            top_10 = list(manager.execute(query.dicts().limit(10)))

        ic([feedback.count for feedback in top_10])
        ic(top_10, len(top_10))
        # ic([model.__dict__ for model in top_10])
        return top_10


    @staticmethod
    async def get_seller_feedback_by_id(feedback_id):
        if not isinstance(feedback_id, int):
            feedback_id = int(feedback_id)
        ic(feedback_id)
        query = SellerFeedbacksHistory.select(SellerFeedbacksHistory, AdvertParameters,
                                                                       Seller).join(Seller)\
                                                                        .switch(SellerFeedbacksHistory)\
                                                                        .join(AdvertParameters).where(
                                                                            (SellerFeedbacksHistory.id == feedback_id)\
                                                            & (SellerFeedbacksHistory.advert_parameters.is_null(False)))
        return await manager.get_or_none(query)

    @staticmethod
    async def get_statistics_by_params(top_direction, period, engine_id=None, brand_id=None, model_id=None,
                             complectation_id=None, color_id=None, for_output=False):
        ic(engine_id, brand_id, model_id, top_direction, period,
                             complectation_id, color_id)
        async def get_time_filter():
            current_time = datetime.now()

            # Фильтры для временных периодов
            if period == 'day':
                time_filter = (SellerFeedbacksHistory.feedback_time >= current_time - timedelta(days=1))
            elif period == 'week':
                time_filter = (SellerFeedbacksHistory.feedback_time >= current_time - timedelta(weeks=1))
            elif period == 'month':
                time_filter = (SellerFeedbacksHistory.feedback_time >= current_time - timedelta(days=30))
            elif period == 'year':
                time_filter = (SellerFeedbacksHistory.feedback_time >= current_time - timedelta(days=365))
            elif period in ('general', 'any', 'all'):
                time_filter = True  # Без временного фильтра
            else:
                raise ValueError("Invalid period parameter")

            return time_filter
        ''''''
        # Определяем текущее время

        time_filter = await get_time_filter()

        if for_output:
            conditions = []
            if color_id is not None:
                conditions.append(CarColor.id == color_id)
            if complectation_id is not None:
                conditions.append(AdvertParameters.complectation_id == complectation_id)
            if model_id is not None:
                conditions.append(CarModel.id == model_id)
            if brand_id is not None:
                conditions.append(CarBrand.id == brand_id)
            if engine_id is not None:
                conditions.append(CarComplectation.engine_id == engine_id)
            conditions.append(SellerFeedbacksHistory.advert_parameters.is_null(False))
            conditions.append(time_filter)

            combined_conditions = reduce(operator.and_, conditions)
            ic(combined_conditions)

            query = (SellerFeedbacksHistory
                     .select(Seller,
                             AdvertParameters,
                             fn.COUNT(SellerFeedbacksHistory.id).alias('count'),
                             fn.ARRAY_AGG(SellerFeedbacksHistory.id).alias('ids'))
                     .join(AdvertParameters)
                     .join(CarColor)
                     .switch(AdvertParameters)
                     .join(CarComplectation)
                     .join(CarModel)
                     .join(CarBrand)
                     .switch(SellerFeedbacksHistory)
                     .join(Seller)
                     .where(combined_conditions)
                     .group_by(Seller, AdvertParameters))


            # # Основной запрос с добавлением поля count
            # query = (SellerFeedbacksHistory
            #          .select(SellerFeedbacksHistory,
            #                  fn.COUNT(SellerFeedbacksHistory.id).alias('count')
            #                  ).join(AdvertParameters)
            #             .join(CarColor)
            #             .switch(AdvertParameters)
            #             .join(CarComplectation)
            #             .join(CarModel)
            #             .join(CarBrand)
            #             .where(combined_conditions, time_filter)
            #             .group_by(SellerFeedbacksHistory.seller_id, SellerFeedbacksHistory.advert_parameters_id))

        # Изменяем логику запроса в зависимости от входных параметров
        elif complectation_id is not None:
            query = CarColor.select(CarColor, fn.COUNT(SellerFeedbacksHistory.id).alias('count')).join(
                AdvertParameters).join(SellerFeedbacksHistory).switch(AdvertParameters).join(CarComplectation).join(CarModel).join(CarBrand).where(
                ((AdvertParameters.complectation_id == complectation_id) & (SellerFeedbacksHistory.advert_parameters.is_null(False)) & \
                 (CarModel.id == model_id) & (CarBrand.id == brand_id) & \
                 (CarComplectation.engine_id == engine_id)), time_filter)\
                .group_by(CarColor)
        elif model_id is not None:
            query = CarComplectation.select(CarComplectation, fn.COUNT(SellerFeedbacksHistory.id).alias('count')).join(
                AdvertParameters).join(SellerFeedbacksHistory).switch(CarComplectation).join(CarModel)\
                .where(((CarModel.id == model_id) & (SellerFeedbacksHistory.advert_parameters.is_null(False)) & \
                        (CarComplectation.engine_id == engine_id) & \
                        (CarModel.brand_id == brand_id)), time_filter).group_by(CarComplectation)
        elif brand_id is not None:
            query = CarModel.select(CarModel, fn.COUNT(SellerFeedbacksHistory.id).alias('count')).join(
                CarComplectation).join(AdvertParameters).join(SellerFeedbacksHistory).switch(CarModel).join(CarBrand)\
                .where(((CarBrand.id == brand_id) & (SellerFeedbacksHistory.advert_parameters.is_null(False)) \
                        & (CarComplectation.engine_id == engine_id)),
                       time_filter).group_by(CarModel)
        elif engine_id is not None:
            query = CarBrand.select(CarBrand, fn.COUNT(SellerFeedbacksHistory.id).alias('count')).join(CarModel).join(
                CarComplectation).join(AdvertParameters).join(SellerFeedbacksHistory).switch(CarComplectation).join(CarEngine)\
                .where((CarEngine.id == engine_id) & (SellerFeedbacksHistory.advert_parameters.is_null(False)),
                       time_filter).group_by(CarBrand)
        else:
            query = CarEngine.select(CarEngine, fn.COUNT(SellerFeedbacksHistory.id).alias('count')).join(
                CarComplectation).join(AdvertParameters).join(SellerFeedbacksHistory).group_by(CarEngine)

        # Добавление сортировки
        if top_direction == 'top':
            query = query.order_by(fn.COUNT(SellerFeedbacksHistory.id).desc())
        else:
            query = query.order_by(fn.COUNT(SellerFeedbacksHistory.id).asc())

        # Выполнение запроса
        results = list(await manager.execute(query))
        ic(results)
        if isinstance(results[0], SellerFeedbacksHistory):
            print('SFHH')
            print(results[0].ids, results[0].count)
            # print([{feedback.ids: feedback.count} for feedback in results])
            # for index, feedback in enumerate(results):
            #     if index != 0:
            #         assert feedback.count >= results[index - 1].count
                # ic(feedback)
        # ic(results)
        return results

