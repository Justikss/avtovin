from database.tables.car_configurations import CarModel, CarEngine, CarBrand, CarComplectation, CarColor, CarMileage, \
    CarYear
from database.tables.offers_history import RecommendationsToBuyer
from database.tables.statistic_tables.advert_parameters import AdvertParameters


class AdvertParameterManager:
    @staticmethod
    async def get_wire_to_config(parameter_table, base_table):
        if base_table == RecommendationsToBuyer:
            base_query = RecommendationsToBuyer.select(RecommendationsToBuyer.id).join(AdvertParameters)
        elif base_table == AdvertParameters:
            base_query = AdvertParameters.select(AdvertParameters.id)

        parameter_table_wires = {
            CarModel: base_query.join(CarComplectation).join(CarModel),
            CarEngine: base_query.join(CarComplectation).join(CarEngine),
            CarBrand: base_query.join(CarComplectation).join(CarModel).join(CarBrand),
            CarComplectation: base_query.join(CarComplectation),
            CarColor: base_query.join(CarColor),
            CarMileage: base_query.join(CarMileage),
            CarYear: base_query.join(CarYear)
        }

        return parameter_table_wires.get(parameter_table)
