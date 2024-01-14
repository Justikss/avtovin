import importlib
import traceback

from peewee import JOIN

from database.data_requests.advert_parameters_requests import AdvertParameterManager
from database.data_requests.statistic_requests.advert_feedbacks_requests import AdvertFeedbackRequester
from database.db_connect import manager
from database.tables.car_configurations import CarAdvert, CarComplectation, CarState, CarEngine, CarColor, CarMileage, \
    CarYear, CarModel, CarBrand
# from database.tables.offers_history import offers_history_module\
#     .RecommendedOffers, offers_history_module\
#     .RecommendationsToBuyer
from database.tables.statistic_tables.advert_parameters import AdvertParameters
from database.tables.user import User

offers_history_module = importlib.import_module('database.tables.offers_history')


class RecommendationParametersBinder:
    @staticmethod
    async def store_parameters(buyer_id, color_id, complectation_id):
        try:
            complectation_id = int(complectation_id)
            ic(buyer_id, complectation_id, color_id)
            parameters = await AdvertFeedbackRequester.get_or_create_by_parameters(
                color_id=color_id,
                complectation_id=complectation_id)
            select_query = await manager.get_or_create(offers_history_module\
                                                       .RecommendationsToBuyer, buyer=buyer_id, parameters=parameters)


        except Exception as ex:
            ic(ex)
            traceback.print_exc()
            pass

    @staticmethod
    async def get_wire_by_parameters(advert=None, complectation_id=None, color_id=None, seller_id=None):
        if advert:
            complectation_id = advert.complectation.id
            color_id = advert.color.id
            seller_id = advert.seller.telegram_id

        ic(complectation_id, color_id)
        parameters = await AdvertFeedbackRequester.get_or_create_by_parameters(color_id, complectation_id)
        query = (offers_history_module\
                 .RecommendationsToBuyer
                 .select()
                 .join(AdvertParameters)
                 .where(AdvertParameters.id == parameters.id)
                 .switch(offers_history_module\
                         .RecommendationsToBuyer)
                 .join(User)
                 .where(User.telegram_id != int(seller_id))
                 # Добавлено условие, что покупатель и продавец не совпадают
                 )
        select_query = list(await manager.execute(query))
        return select_query

    @staticmethod
    async def remove_wire_by_parameter(parameter_table, parameter_id):
        if not isinstance(parameter_id, list):
            parameter_id = [parameter_id]
        parameter_recommendations_to_buyer_wire = await AdvertParameterManager.get_wire_to_config(
            parameter_table, offers_history_module\
                .RecommendationsToBuyer
        )

        ic(parameter_recommendations_to_buyer_wire)
        ic(await manager.execute(offers_history_module\
            .RecommendationsToBuyer.delete().where(
            offers_history_module\
                .RecommendationsToBuyer.id.in_(
                parameter_recommendations_to_buyer_wire.where(parameter_table.id.in_(parameter_id))
            ))
        ))
        ic()
        advert_parameters_wire = await AdvertParameterManager.get_wire_to_config(parameter_table, AdvertParameters)

        ic(await manager.execute(
            AdvertParameters.delete().where(AdvertParameters.id.in_(
                advert_parameters_wire.where(parameter_table.id.in_(parameter_id))
            )
            )
        ))

class RecommendationRequester:
    @staticmethod
    async def add_recommendation(advert):

        parameter_wire = await RecommendationParametersBinder.get_wire_by_parameters(
                                                                                advert)
        ic(parameter_wire)
        if parameter_wire:
            data = []
            for wire in parameter_wire:
                ic(advert, wire.buyer.telegram_id, parameter_wire)
                data.append({'advert': advert, 'buyer': wire.buyer.telegram_id, 'parameters': wire.id})
                return list(await manager.execute(offers_history_module\
                                                  .RecommendedOffers.insert_many(data)))

    @staticmethod
    async def retrieve_by_buyer_id(buyer_id, get_brands=False, by_brand=None):
        ic(buyer_id)
        query = offers_history_module\
            .RecommendedOffers.select(offers_history_module\
                                      .RecommendedOffers, CarAdvert, offers_history_module\
                                      .RecommendationsToBuyer).join(CarAdvert).switch(offers_history_module\
                                                                                                                    .RecommendedOffers).join(User).switch(offers_history_module\
                                                                                                                                                          .RecommendedOffers).join(offers_history_module\
                                                                                                                                                                                   .RecommendationsToBuyer).where(User.telegram_id == int(buyer_id))
        result = await manager.execute(query)
        if get_brands and result:
            ic()
            result = {f'load_brand_{str(recommendation.advert.complectation.model.brand.id)}': recommendation.advert.complectation.model.brand.name for recommendation in result}
            return result
        elif by_brand:
            ic()
            result = query.switch(CarAdvert).join(CarComplectation).join(CarModel).join(CarBrand).where(
                CarBrand.id == int(by_brand)
            )
        ic(result)

        result = list(await manager.execute(query))
        if result:
            return result
        return False

    @staticmethod
    async def remove_recommendation_by_advert_id(advert_id=None):
        if not isinstance(advert_id, list):
            advert_id = [advert_id]
        try:
            await manager.execute(offers_history_module\
                                  .RecommendedOffers.delete().where(offers_history_module\
                                                                    .RecommendedOffers.advert.in_(advert_id)))
        except:
            traceback.print_exc()
            pass

