import importlib

from database.db_connect import manager
from database.tables.car_configurations import CarModel, CarEngine, CarBrand, CarComplectation, CarColor, CarMileage, \
    CarYear
from database.tables.statistic_tables.advert_parameters import AdvertParameters


offers_history_module = importlib.import_module('database.tables.offers_history')

class AdvertParameterManager:
    @staticmethod
    async def get_wire_to_config(parameter_table, base_table):
        if base_table == offers_history_module\
                .RecommendationsToBuyer:
            base_query = offers_history_module\
                .RecommendationsToBuyer.select(offers_history_module\
                                               .RecommendationsToBuyer.id).join(AdvertParameters)
        elif base_table == AdvertParameters:
            base_query = AdvertParameters.select(AdvertParameters.id)

        parameter_table_wires = {
            CarModel: base_query.join(CarComplectation).join(CarModel),
            CarEngine: base_query.join(CarComplectation).join(CarEngine),
            CarBrand: base_query.join(CarComplectation).join(CarModel).join(CarBrand),
            CarComplectation: base_query.join(CarComplectation),
            CarColor: base_query.join(CarColor),
        }

        return parameter_table_wires.get(parameter_table)

    @staticmethod
    async def get_by_id(params_id):
        if isinstance(params_id, str):
            params_id = int(params_id)

        return await manager.get_or_none(AdvertParameters, AdvertParameters.id == params_id)
