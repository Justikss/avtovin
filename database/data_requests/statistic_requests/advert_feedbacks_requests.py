import importlib

from database.db_connect import manager
from database.tables.car_configurations import CarAdvert
from database.tables.offers_history import SellerFeedbacksHistory
from database.tables.statistic_tables.advert_parameters import AdvertParameters


class AdvertFeedbackRequester:
    @staticmethod
    async def get_or_create_by_parameters(state_id, engine_type_id, color_id, mileage_id, year_id, complectation_id, only_get=False):
        ic(state_id, engine_type_id, color_id, mileage_id, year_id, complectation_id)
        if only_get:
            manager_method = manager.get_or_none
        else:
            manager_method = manager.get_or_create

        query = await manager_method(AdvertParameters,
                                     complectation=complectation_id,
                                     state=state_id, engine_type=engine_type_id, color=color_id,
                                     mileage=mileage_id, year=year_id)
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
