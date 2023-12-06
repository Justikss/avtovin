from peewee import JOIN

from database.db_connect import manager
from database.tables.car_configurations import CarAdvert, CarComplectation, CarState, CarEngine, CarColor, CarMileage, \
    CarYear, CarModel, CarBrand
from database.tables.offers_history import RecommendedOffers, RecommendationsToBuyer
from database.tables.user import User


class RecommendationParametersBinder:
    @staticmethod
    async def store_parameters(buyer_id, complectation_id, state_id, engine_type_id, color_id, mileage_id, year_id):
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

            select_query = await manager.get(RecommendedOffers, buyer=buyer_id, complectation=complectation_id,
                                                state=state_id, engine_type=engine_type_id, color=color_id,
                                                mileage=mileage_id, year=year_id)
            ic(select_query)
            if not select_query:

                insert_query = await manager.create(RecommendationsToBuyer, buyer=buyer_id, complectation=complectation_id,
                                                    state=state_id, engine_type=engine_type_id, color=color_id,
                                                    mileage=mileage_id, year=year_id)

        except Exception as ex:
            ic(ex)
            pass

    @staticmethod
    async def get_wire_by_parameters(advert=None, complectation_id=None, state_id=None, engine_type_id=None, color_id=None, mileage_id=None, year_id=None, seller_id=None):
        if advert:
            complectation_id = advert.complectation.id
            state_id = advert.state.id
            engine_type_id = advert.engine_type.id
            color_id = advert.color.id
            mileage_id = advert.mileage.id if advert.mileage else None
            year_id = advert.year.id if advert.year else None
            seller_id = advert.seller.telegram_id

        ic(complectation_id, state_id, engine_type_id, color_id, mileage_id, year_id)

        query = (RecommendationsToBuyer
                 .select()
                 .join(CarComplectation)
                 .where(CarComplectation.id == complectation_id)
                 .switch(RecommendationsToBuyer)
                 .join(CarState)
                 .where(CarState.id == state_id)
                 .switch(RecommendationsToBuyer)
                 .join(CarEngine)
                 .where(CarEngine.id == engine_type_id)
                 .switch(RecommendationsToBuyer)
                 .join(CarColor, JOIN.LEFT_OUTER)  # Используйте LEFT JOIN для полей, которые могут быть NULL
                 .where((CarColor.id == color_id) | (CarColor.id.is_null(True)))  # Проверка на NULL
                 .switch(RecommendationsToBuyer)
                 .join(CarMileage, JOIN.LEFT_OUTER)
                 .where((CarMileage.id == mileage_id) | (CarMileage.id.is_null(True)))
                 .switch(RecommendationsToBuyer)
                 .join(CarYear, JOIN.LEFT_OUTER)
                 .where((CarYear.id == year_id) | (CarYear.id.is_null(True)))
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
                ic(advert_id, wire.buyer.telegram_id, parameter_wire)
                data.append({'advert': advert_id, 'buyer': wire.buyer.telegram_id, 'parameters': wire.id})
                return await manager.execute(RecommendedOffers.insert_many(data))


    @staticmethod
    async def retrieve_by_buyer_id(buyer_id, get_brands=False, by_brand=None):
        ic(buyer_id)
        query = RecommendedOffers.select().join(User).where(User.telegram_id == int(buyer_id))
        result = await manager.execute(query)
        if get_brands and result:
            ic()
            result = {f'load_brand_{str(recommendation.advert.complectation.model.brand.id)}': recommendation.advert.complectation.model.brand.name for recommendation in result}
            return result
        elif by_brand:
            ic()
            result = query.switch(RecommendedOffers).join(CarAdvert).join(CarComplectation).join(CarModel).join(CarBrand).where(
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
        try:
            await manager.execute(RecommendedOffers.delete().where(RecommendedOffers.advert == int(advert_id)))
        except:
            pass