import asyncio
import importlib
import traceback

from peewee import JOIN, IntegrityError

from database.data_requests.advert_parameters_requests import AdvertParameterManager
from database.db_connect import manager
from database.tables.car_configurations import CarAdvert, CarComplectation, CarState, CarEngine, CarColor, CarMileage, \
    CarYear, CarModel, CarBrand
from database.tables.offers_history import SellerFeedbacksHistory, RecommendedOffers

from database.tables.statistic_tables.advert_parameters import AdvertParameters
from database.tables.user import User

offers_history_module = importlib.import_module('database.tables.offers_history')
cache_redis_module = importlib.import_module('utils.redis_for_language')
cache_redis = cache_redis_module.cache_redis

class RecommendationParametersBinder:
    @staticmethod
    async def store_parameters(buyer_id, color_id, complectation_id, model):
        advert_feedbacks_requests_module = importlib.import_module('database.data_requests.statistic_requests.advert_feedbacks_requests')

        try:
            if str(complectation_id).isdigit():
                complectation_id = int(complectation_id)
            ic(buyer_id, complectation_id, color_id)
            parameters = await advert_feedbacks_requests_module\
                .AdvertFeedbackRequester.get_or_create_by_parameters(
                color_id=color_id,
                complectation_id=complectation_id,
                model=model)
            if not isinstance(parameters, list):
                parameters = [parameters]
            ic(parameters)
            tasks = [manager.get_or_create(offers_history_module\
                                                       .RecommendationsToBuyer, buyer=buyer_id, parameters=parameter)
                                            for parameter in parameters]
            try:
                await asyncio.gather(*tasks)
            except IntegrityError:
                return False
            # select_query = await manager.get_or_create(offers_history_module\
            #                                            .RecommendationsToBuyer, buyer=buyer_id, parameters=parameters)


        except Exception as ex:
            ic(ex)
            # traceback.print_exc()
            pass

    @staticmethod
    async def get_wire_by_parameters(advert=None, complectation_id=None, color_id=None, seller_id=None, model_id=None):
        advert_feedbacks_requests_module = importlib.import_module('database.data_requests.statistic_requests.advert_feedbacks_requests')
        if advert:
            complectation_id = advert.complectation.id
            model_id = advert.complectation.model.id
            color_id = advert.color.id
            seller_id = advert.seller.telegram_id

        ic(complectation_id, color_id)
        parameters = await advert_feedbacks_requests_module\
            .AdvertFeedbackRequester.get_or_create_by_parameters(color_id, complectation_id, model_id)
        if parameters:
            parameters = [parameter.id for parameter in parameters]

        query = (offers_history_module\
                 .RecommendationsToBuyer
                 .select()
                 .join(AdvertParameters)
                 .where(AdvertParameters.id.in_(parameters))
                 .switch(offers_history_module\
                         .RecommendationsToBuyer)
                 .join(User)
                 .where(User.telegram_id != int(seller_id))
                 # Добавлено условие, что покупатель и продавец не совпадают
                 )
        select_query = list(await manager.execute(query))
        return select_query

    @cache_redis.cache_update_decorator(model=offers_history_module.RecommendedOffers, mode='by_scan')
    @staticmethod
    async def remove_wire_by_parameter(parameter_table, parameter_id):
        if not isinstance(parameter_id, list):
            parameter_id = [parameter_id]
        parameter_recommendations_to_buyer_wire = await AdvertParameterManager.get_wire_to_config(
            parameter_table, offers_history_module\
                .RecommendationsToBuyer
        )

        ic(parameter_recommendations_to_buyer_wire)
        recommendations = list(await manager.execute(offers_history_module.RecommendedOffers
        .select(offers_history_module.RecommendedOffers, User).join(User).where(
            offers_history_module.RecommendedOffers.parameters_id.in_(offers_history_module\
                .RecommendationsToBuyer.select(offers_history_module\
                                               .RecommendationsToBuyer.id).where(offers_history_module\
                .RecommendationsToBuyer.id.in_(
                parameter_recommendations_to_buyer_wire.where(parameter_table.id.in_(parameter_id)

        )))))))
        await manager.execute(offers_history_module.RecommendedOffers.delete().where(offers_history_module.RecommendedOffers.parameters_id.in_(
                        offers_history_module\
                                .RecommendationsToBuyer.select(offers_history_module\
                                .RecommendationsToBuyer.id).where(offers_history_module\
                       .RecommendationsToBuyer.id.in_(
                parameter_recommendations_to_buyer_wire.where(parameter_table.id.in_(parameter_id)

        ))))))
        ic(await manager.execute(offers_history_module\
            .RecommendationsToBuyer.delete().where(
            offers_history_module\
                .RecommendationsToBuyer.id.in_(
                parameter_recommendations_to_buyer_wire.where(parameter_table.id.in_(parameter_id))
            ))
        ))
        ic()
        advert_parameters_wire = await AdvertParameterManager.get_wire_to_config(parameter_table, AdvertParameters)

        condition_by_advert_parameter_and_selected_param = advert_parameters_wire.where(parameter_table.id.in_(parameter_id))

        await manager.execute(SellerFeedbacksHistory.update(advert_parameters=None).where(SellerFeedbacksHistory.id.in_(
            SellerFeedbacksHistory.select(SellerFeedbacksHistory.id).join(AdvertParameters)\
                                       .where(AdvertParameters.id.in_(condition_by_advert_parameter_and_selected_param)))))

        ic(await manager.execute(
            AdvertParameters.delete().where(AdvertParameters.id.in_(condition_by_advert_parameter_and_selected_param))))

        buyer_ids = list({recommendation.buyer.telegram_id for recommendation in recommendations})
        return buyer_ids

    @cache_redis.cache_update_decorator(model=offers_history_module.RecommendedOffers, mode='by_scan')
    @staticmethod
    async def remove_recommendation_by_recommendation_id(recommendations):
        if isinstance(recommendations, list):
            condition = RecommendedOffers.id.in_(recommendations)
        else:
            condition = RecommendedOffers.id == recommendations

        await manager.execute(RecommendedOffers.delete().where(condition))

    @cache_redis.cache_update_decorator(model=offers_history_module.RecommendedOffers, mode='by_scan')
    @staticmethod
    async def remove_recommendation_by_advert_and_buyer_ids(advert_id, user_id, from_output=False):
        delete_query = await manager.execute(
            RecommendedOffers.delete().where(RecommendedOffers.id ==
                RecommendedOffers.select(RecommendedOffers.id).where(((RecommendedOffers.advert == advert_id) & (
                    RecommendedOffers.buyer == user_id
                ))
            ))
        )
        ic(from_output)
        if from_output and delete_query:
            from database.data_requests.offers_requests import CachedOrderRequests
            await CachedOrderRequests.set_cache(user_id, advert_id if isinstance(advert_id, list) else [advert_id])
        ic(delete_query)
        if delete_query:

            return [user_id]
class RecommendationRequester:
    @cache_redis.cache_update_decorator(model=offers_history_module.RecommendedOffers, mode='by_scan')
    @staticmethod
    async def add_recommendation(advert):
        ic(advert)
        parameter_wire = await RecommendationParametersBinder.get_wire_by_parameters(
                                                                                advert)
        ic(parameter_wire)
        if parameter_wire:

            data = [{'advert': advert, 'buyer': wire.buyer.telegram_id, 'parameters': wire.id}
                    for wire in parameter_wire]
            ic(data)
            buyers = list({wire.buyer.telegram_id for wire in parameter_wire})
            # Формирование SQL запроса с RETURNING для получения вставленных объектов
            await manager.execute(offers_history_module.RecommendedOffers.insert_many(data))

            return buyers

    @cache_redis.cache_decorator(model=offers_history_module.RecommendedOffers)
    @staticmethod
    async def retrieve_by_buyer_id(buyer_id, by_brand=None, count=False, get_brands=False):
        ic(buyer_id)
        query = (RecommendedOffers.select(RecommendedOffers.id, RecommendedOffers.datetime_of_deletion, CarAdvert, offers_history_module\
                                      .RecommendationsToBuyer).join(CarAdvert).switch(RecommendedOffers)
                                    .join(User).switch(RecommendedOffers)
                                        .join(offers_history_module\
                                                           .RecommendationsToBuyer).where(User.telegram_id == int(buyer_id)))
        if count:
            return await manager.count(query)
        elif get_brands:
            query = (CarBrand.select().where(CarBrand.id.in_(query.select(CarBrand.id)
                     .switch(CarAdvert).join(CarComplectation).join(CarModel).join(CarBrand))))

        elif by_brand:
            query = (query.switch(CarAdvert).join(CarComplectation).join(CarModel).join(CarBrand)
                     .where(CarBrand.id == int(by_brand)))


        result = list(await manager.execute(query))
        if not get_brands:
            from database.data_requests.offers_requests import CachedOrderRequests
            result = await CachedOrderRequests.check_overtime_requests(result)

        return result

    @cache_redis.cache_update_decorator(model=offers_history_module.RecommendedOffers, mode='by_scan')
    @staticmethod
    async def remove_recommendation_by_advert_id(advert_id=None):
        if not isinstance(advert_id, list):
            advert_id = [advert_id]
        ic(advert_id)
        # id_list_str = ','.join([str(id) for id in advert_id])  # Прямая подстановка значений

        select_query = (RecommendedOffers.select(RecommendedOffers.buyer, RecommendedOffers.id, User).join(User)
                        .where(RecommendedOffers.advert_id.in_(advert_id)))
        recommendations = list(await manager.execute(select_query))
        ic(recommendations)
        delete_query = RecommendedOffers.delete().where(RecommendedOffers.id.in_(recommendations))
        await manager.execute(delete_query)

        buyer_ids_of_deleted_recommendations = list({recommendation.buyer.telegram_id for recommendation in recommendations})

        return buyer_ids_of_deleted_recommendations

