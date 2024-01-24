import asyncio
import importlib
import operator
from datetime import timedelta, datetime
from functools import reduce

from peewee import fn, JOIN, SQL, Window
from peewee_async import Manager

from database.data_requests.utils.raw_sql_handler import get_top_advert_parameters
from database.db_connect import manager
from database.tables.car_configurations import CarAdvert, CarComplectation, CarModel, CarState, CarColor, CarMileage, \
    CarYear, CarBrand, CarEngine
from database.tables.offers_history import SellerFeedbacksHistory
from database.tables.seller import Seller
from database.tables.statistic_tables.advert_parameters import AdvertParameters

offers_history_module = importlib.import_module('database.tables.offers_history')

class AdvertFeedbackRequester:
    @staticmethod
    async def delete_by_seller_id(seller_id):
        if isinstance(seller_id, str):
            seller_id = int(seller_id)

        await manager.execute(SellerFeedbacksHistory.delete().where(SellerFeedbacksHistory.seller_id == seller_id))

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
        await manager.execute(offers_history_module\
                              .SellerFeedbacksHistory.insert(seller_id=seller_id, advert_parameters=parameters[0]))


    @staticmethod
    async def update_parameters_to_null_by_specific_parameter(table_name, model_id):
        base_query = offers_history_module\
            .SellerFeedbacksHistory.select(offers_history_module\
                                           .SellerFeedbacksHistory.id).join(AdvertParameters)\
                                                                             .join(CarComplectation).join(CarModel)
        if table_name == 'color':
            base_query = base_query.where(AdvertParameters.color.in_(model_id))
        if table_name == 'complectation':
            base_query = base_query.where(CarComplectation.id.in_(model_id))
        if model_id:
            base_query = base_query.where(CarModel.id.in_(model_id))
        if table_name == 'brand':
            base_query = base_query.where(CarModel.brand.in_(model_id))

        await manager.execute(offers_history_module\
                              .SellerFeedbacksHistory().update(advert_parameters=None)\
                                                      .where(offers_history_module\
                                                             .SellerFeedbacksHistory.id.in_(base_query)))

    @staticmethod
    async def get_top_advert_parameters(period, top_direction='top', manager=manager):
        time_filter, time_filter_sql, time_param = await AdvertFeedbackRequester.get_time_filter(period)

        order_direction = "DESC" if top_direction == "top" else "ASC"


        ic(time_filter_sql, order_direction)

        sql_query = f'''
WITH FeedbackCounts AS (
    SELECT 
        sfh.advert_parameters_id,
        sfh.seller_id,
        COUNT(sfh.id) AS feedback_count
    FROM 
        SellerFeedbacksHistory sfh
{f'WHERE' + ' ' + time_filter_sql if time_filter_sql else ''}
    GROUP BY 
        sfh.advert_parameters_id, sfh.seller_id
),
TotalFeedbacks AS (
    SELECT
        advert_parameters_id,
        SUM(feedback_count) AS total_feedback_count
    FROM 
        FeedbackCounts
    GROUP BY 
        advert_parameters_id
),
MaxFeedbacks AS (
    SELECT
        fc.advert_parameters_id,
        fc.seller_id,
        fc.feedback_count,
        tf.total_feedback_count
    FROM 
        FeedbackCounts fc
    JOIN 
        TotalFeedbacks tf ON fc.advert_parameters_id = tf.advert_parameters_id
    WHERE 
        fc.feedback_count = (
            SELECT MAX(feedback_count)
            FROM FeedbackCounts
            WHERE advert_parameters_id = fc.advert_parameters_id
        )
)
SELECT 
    mfc.advert_parameters_id,
    mfc.seller_id,
    mfc.feedback_count,
    mfc.total_feedback_count AS count,
    ap.*,
    s.*,
    cc.*,
    ce.*,
    cm.*,
    cb.*
FROM 
    MaxFeedbacks mfc
JOIN
    AdvertParameters ap ON mfc.advert_parameters_id = ap.id
JOIN 
    Продавцы s ON mfc.seller_id = s.telegram_id
JOIN
    CarComplectation cc ON cc.id = ap.complectation_id
JOIN
    CarEngine ce ON ce.id = cc.engine_id
JOIN
    CarModel cm ON cm.id = cc.model_id
JOIN
    CarBrand cb ON cb.id = cm.brand_id
ORDER BY 
    mfc.total_feedback_count {order_direction}
LIMIT 10

    '''

        query = offers_history_module.SellerFeedbacksHistory.raw(sql_query, time_param)
        results = list(await manager.execute(query))
        ic([feedback.count for feedback in results])
        ic(results, len(results))
        # ic([model.__dict__ for model in top_10])
        return results


    @staticmethod
    async def get_seller_feedback_by_id(feedback_id):
        if not isinstance(feedback_id, int):
            feedback_id = int(feedback_id)
        ic(feedback_id)
        query = offers_history_module\
            .SellerFeedbacksHistory.select(offers_history_module\
                                           .SellerFeedbacksHistory, AdvertParameters,
                                                                       Seller).join(Seller)\
                                                                        .switch(offers_history_module\
                                                                                .SellerFeedbacksHistory)\
                                                                        .join(AdvertParameters).where(
                                                                            (offers_history_module\
                                                                             .SellerFeedbacksHistory.id == feedback_id)\
                                                            & (offers_history_module\
                                                               .SellerFeedbacksHistory.advert_parameters.is_null(False)))
        return await manager.get_or_none(query)


    @staticmethod
    async def statistic_is_exists():
        return list(await manager.execute(offers_history_module\
                                          .SellerFeedbacksHistory.select().limit(1)))

    @staticmethod
    async def get_time_filter(period):
        current_time = datetime.now()
        ic(period)
        # Фильтры для временных периодов
        if period == 'day':
            time_filter_peewee = (
                    offers_history_module.SellerFeedbacksHistory.feedback_time >= current_time - timedelta(
                days=1))
            time_filter_sql = "sfh.feedback_time >= %s"
            time_param = current_time - timedelta(days=1)
        elif period == 'week':
            time_filter_peewee = (
                    offers_history_module.SellerFeedbacksHistory.feedback_time >= current_time - timedelta(
                weeks=1))
            time_filter_sql = "sfh.feedback_time >= %s"
            time_param = current_time - timedelta(weeks=1)
        elif period == 'month':
            time_filter_peewee = (
                    offers_history_module.SellerFeedbacksHistory.feedback_time >= current_time - timedelta(
                days=30))
            time_filter_sql = "sfh.feedback_time >= %s"
            time_param = current_time - timedelta(days=30)
        elif period == 'year':
            time_filter_peewee = (
                    offers_history_module.SellerFeedbacksHistory.feedback_time >= current_time - timedelta(
                days=365))
            time_filter_sql = "sfh.feedback_time >= %s"
            time_param = current_time - timedelta(days=365)
        elif period in ('general', 'any', 'all'):
            return None, None, None  # Без временного фильтра
        else:
            raise ValueError("Invalid period parameter")

        return time_filter_peewee, time_filter_sql, time_param

    @staticmethod
    async def get_statistics_by_params(top_direction, period, engine_id=None, brand_id=None, model_id=None,
                             complectation_id=None, color_id=None, for_output=False):
        ic(engine_id, brand_id, model_id, top_direction, period,
                             complectation_id, color_id)


        ''''''
        # Определяем текущее время

        time_filter, time_filter_sql, time_param = await AdvertFeedbackRequester.get_time_filter(period)

        if for_output:
            conditions = []
            params = []
            if color_id is not None:
                conditions.append("ccol.id = %s")
                params.append(color_id)
            if complectation_id is not None:
                conditions.append("cc.id = %s")
                params.append(complectation_id)
            if model_id is not None:
                conditions.append("cm.id = %s")
                params.append(model_id)
            if brand_id is not None:
                conditions.append("cb.id = %s")
                params.append(brand_id)
            if engine_id is not None:
                conditions.append("cc.engine_id = %s")
                params.append(engine_id)

            conditions.append(time_filter_sql)
            params.append(time_param)

            # Формирование условия WHERE в SQL запросе
            where_clause = " AND ".join(conditions) if conditions else "1=1"
            order_direction = "DESC" if top_direction == "top" else "ASC"
            # Сформировать SQL запрос
            sql_query = f"""
WITH FeedbackCounts AS (
    SELECT 
        sfh.advert_parameters_id,
        sfh.seller_id,
        COUNT(sfh.id) AS feedback_count
    FROM 
        SellerFeedbacksHistory sfh
    JOIN AdvertParameters ap ON sfh.advert_parameters_id = ap.id
    JOIN CarComplectation cc ON ap.complectation_id = cc.id
    JOIN CarModel cm ON cc.model_id = cm.id
    JOIN CarBrand cb ON cm.brand_id = cb.id
    JOIN CarColor ccol ON ap.color_id = ccol.id
    WHERE 
        {where_clause}
    GROUP BY 
        sfh.advert_parameters_id, sfh.seller_id
),
MaxFeedbacks AS (
    SELECT
        advert_parameters_id,
        MAX(feedback_count) AS max_feedback_count
    FROM 
        FeedbackCounts
    GROUP BY 
        advert_parameters_id
)
SELECT 
    fc.advert_parameters_id,
    fc.seller_id,
    mfc.max_feedback_count AS count,
    ap.*,
    s.*,
    cc.*,
    ce.*,
    cm.*,
    cb.*
FROM 
    FeedbackCounts fc
JOIN 
    MaxFeedbacks mfc ON fc.advert_parameters_id = mfc.advert_parameters_id
JOIN
    Продавцы s ON fc.seller_id = s.telegram_id
JOIN
    AdvertParameters ap ON fc.advert_parameters_id = ap.id
JOIN
    CarComplectation cc ON cc.id = ap.complectation_id
JOIN
    CarEngine ce ON ce.id = cc.engine_id
JOIN
    CarModel cm ON cm.id = cc.model_id
JOIN
    CarBrand cb ON cb.id = cm.brand_id
WHERE 
    fc.feedback_count = mfc.max_feedback_count
ORDER BY 
    fc.feedback_count {order_direction}
            """
            ic(sql_query, params)
            # Выполнение сырого SQL-запроса в Peewee
            query = offers_history_module.SellerFeedbacksHistory.raw(sql_query, *params)
            results = list(await manager.execute(query))
            ic(len(results))
            ic(results)
            ic([result.__dict__ for result in results])
            return results
            # Получение и обработка результатов
            results = []
            for sfh in query.execute():
                results.append({
                    'seller_feedbacks_history': sfh,
                    'count': sfh.count  # Или соответствующий способ доступа к результату подсчета
                })




        # Изменяем логику запроса в зависимости от входных параметров
        elif complectation_id is not None:
            query = CarColor.select(CarColor, fn.COUNT(offers_history_module\
                                                       .SellerFeedbacksHistory.id).alias('count')).join(
                AdvertParameters).join(offers_history_module\
                                       .SellerFeedbacksHistory).switch(AdvertParameters).join(CarComplectation).join(CarModel).join(CarBrand).where(
                ((AdvertParameters.complectation_id == complectation_id) & (offers_history_module\
                                                                            .SellerFeedbacksHistory.advert_parameters.is_null(False)) & \
                 (CarModel.id == model_id) & (CarBrand.id == brand_id) & \
                 (CarComplectation.engine_id == engine_id)) & time_filter)\
                .group_by(CarColor)
        elif model_id is not None:
            query = CarComplectation.select(CarComplectation, fn.COUNT(offers_history_module\
                                                                       .SellerFeedbacksHistory.id).alias('count')).join(
                AdvertParameters).join(offers_history_module\
                                       .SellerFeedbacksHistory).switch(CarComplectation).join(CarModel)\
                .where(((CarModel.id == model_id) & (offers_history_module\
                                                     .SellerFeedbacksHistory.advert_parameters.is_null(False)) & \
                        (CarComplectation.engine_id == engine_id) & \
                        (CarModel.brand_id == brand_id)) & time_filter).group_by(CarComplectation)
        elif brand_id is not None:
            query = CarModel.select(CarModel, fn.COUNT(offers_history_module\
                                                       .SellerFeedbacksHistory.id).alias('count')).join(
                CarComplectation).join(AdvertParameters).join(offers_history_module\
                                                              .SellerFeedbacksHistory).switch(CarModel).join(CarBrand)\
                .where(((CarBrand.id == brand_id) & (offers_history_module\
                                                     .SellerFeedbacksHistory.advert_parameters.is_null(False)) \
                        & (CarComplectation.engine_id == engine_id)) &
                       time_filter).group_by(CarModel)
        elif engine_id is not None:
            query = CarBrand.select(CarBrand, fn.COUNT(offers_history_module\
                                                       .SellerFeedbacksHistory.id).alias('count')).join(CarModel).join(
                CarComplectation).join(AdvertParameters).join(offers_history_module\
                                                              .SellerFeedbacksHistory).switch(CarComplectation).join(CarEngine)\
                .where((CarEngine.id == engine_id) & (offers_history_module\
                                                      .SellerFeedbacksHistory.advert_parameters.is_null(False)) &
                       time_filter).group_by(CarBrand)
        else:
            query = CarEngine.select(CarEngine, fn.COUNT(offers_history_module\
                                                         .SellerFeedbacksHistory.id).alias('count')).join(
                CarComplectation).join(AdvertParameters).join(offers_history_module\
                                                              .SellerFeedbacksHistory).where(
                                                                                        time_filter
                                                                                    ).group_by(CarEngine)

        # Добавление сортировки
        print(query)
        if top_direction == 'top':
            query = query.order_by(fn.COUNT(offers_history_module\
                                            .SellerFeedbacksHistory.id).desc())
        else:
            query = query.order_by(fn.COUNT(offers_history_module\
                                            .SellerFeedbacksHistory.id).asc())

        # Выполнение запроса
        results = list(await manager.execute(query))
        ic(results)
        # if isinstance(results[0], offers_history_module\
        #         .SellerFeedbacksHistory):
        #
        #     ic(results[0].ids, results[0].count)

        return results

