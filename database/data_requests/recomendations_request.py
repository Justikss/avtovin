import traceback

from peewee import JOIN

from database.data_requests.statistic_requests.advert_feedbacks_requests import AdvertFeedbackRequester
from database.db_connect import manager
from database.tables.car_configurations import CarAdvert, CarComplectation, CarState, CarEngine, CarColor, CarMileage, \
    CarYear, CarModel, CarBrand
from database.tables.offers_history import RecommendedOffers, RecommendationsToBuyer
from database.tables.statistic_tables.advert_parameters import AdvertParameters
from database.tables.user import User


class RecommendationParametersBinder:
    @staticmethod
    async def store_parameters(buyer_id, state_id, engine_type_id, color_id, mileage_id, year_id, complectation_id):
        try:
            state_id, complectation_id = int(state_id), int(complectation_id)
            ic(buyer_id, complectation_id, state_id, engine_type_id, color_id, mileage_id, year_id)
            # data = [{'buyer': buyer_id,
            #         'complectation': complectation_id,
            #         'state': state_id,
            #         'engine_type': engine_type_id,
            #         'color': color_id,
            #         'mileage': mileage_id,
            #         'year': year_id}]
            parameters = await AdvertFeedbackRequester.get_or_create_by_parameters(
                state_id=state_id,
                engine_type_id=engine_type_id,
                color_id=color_id,
                mileage_id=mileage_id,
                year_id=year_id,
                complectation_id=complectation_id)
            select_query = await manager.get_or_create(RecommendationsToBuyer, buyer=buyer_id, parameters=parameters[0])


        except Exception as ex:
            ic(ex)
            traceback.print_exc()
            pass

    @staticmethod
    async def get_wire_by_parameters(advert=None, complectation_id=None, state_id=None, engine_type_id=None, color_id=None, mileage_id=None, year_id=None, seller_id=None):
        if advert:
            complectation_id = advert.complectation.id
            state_id = advert.state.id
            engine_type_id = advert.complectation.engine.id
            color_id = advert.color.id
            # if advert.color:
            #     color_id = advert.color.id
            # else:
            #     color_id = None
            mileage_id = advert.mileage.id if advert.mileage else None
            year_id = advert.year.id if advert.year else None
            seller_id = advert.seller.telegram_id

        ic(complectation_id, state_id, engine_type_id, color_id, mileage_id, year_id)
        parameters = await AdvertFeedbackRequester.get_or_create_by_parameters(state_id, color_id, mileage_id, year_id, complectation_id)
        query = (RecommendationsToBuyer
                 .select()
                 .join(AdvertParameters)
                 .where(AdvertParameters.id == parameters.id)
                 .switch(RecommendationsToBuyer)
                 .join(User)
                 .where(User.telegram_id != int(seller_id))
                 # Добавлено условие, что покупатель и продавец не совпадают
                 )
        select_query = list(await manager.execute(query))
        return select_query



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
                return list(await manager.execute(RecommendedOffers.insert_many(data)))

    @staticmethod
    async def retrieve_by_buyer_id(buyer_id, get_brands=False, by_brand=None):
        ic(buyer_id)
        query = RecommendedOffers.select(RecommendedOffers, CarAdvert, AdvertParameters, RecommendationsToBuyer).join(CarAdvert).switch(RecommendedOffers).join(User).switch(RecommendedOffers).join(RecommendationsToBuyer).join(AdvertParameters).where(User.telegram_id == int(buyer_id))
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
        print(result)
        result = list(await manager.execute(query))
        if result:
            return result
        return False

    @staticmethod
    async def remove_recommendation_by_advert_id(advert_id=None):
        if not isinstance(advert_id, list):
            advert_id = [advert_id]
        try:
            await manager.execute(RecommendedOffers.delete().where(RecommendedOffers.advert.in_(advert_id)))
        except:
            traceback.print_exc()
            pass

