import asyncio

from database.data_requests.car_advert_requests import AdvertRequester

print(asyncio.run(AdvertRequester.get_advert_by(state_id = '1',
    engine_type_id = 3,
    brand_id = 3,
    model_id = 1,
    complectation_id = '3',
    color_id = None,
    mileage_id = None,
    year_of_release_id = None)))