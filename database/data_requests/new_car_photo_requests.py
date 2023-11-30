from typing import List, Union, Optional

from aiogram.fsm.context import FSMContext
from icecream import install, ic

from database.tables.car_configurations import CarAdvert, CarComplectation, CarModel, CarBrand, CarEngine
from database.tables.commodity import NewCarPhotoBase
from database.tables.commodity import AdvertPhotos
from database.db_connect import database, manager


from utils.Lexicon import LexiconCommodityLoader

install()


class PhotoRequester:
    @staticmethod
    async def load_photo_in_base(photo_data: List[dict]):
        '''Асинхронный метод для установки фотографий новых автомобилей'''
        if 3 > len(photo_data) > 5:
            raise ValueError('Фотографий должно быть от трёх до пяти (включительно)')

        await manager.execute(NewCarPhotoBase.insert_many(photo_data))

        # insert_photo_query = AdvertPhotos.insert_many(photo_data)
        # await manager.execute(insert_photo_query)
        return

        car_brand = photo_data[0]['car_brand']
        car_model = photo_data[0]['car_model']
        car_engine = photo_data[0]['car_engine']
        car_complectation = photo_data[0]['car_complectation']
        existing_photos = await manager.execute(NewCarPhotoBase.select().where(
            (NewCarPhotoBase.car_brand == car_brand) & (NewCarPhotoBase.car_model == car_model)))

        if existing_photos:
            raise BufferError('Фотографии на эту конфигурацию уже загружены.')
        else:
            insert_query = NewCarPhotoBase.insert_many(photo_data)
            await manager.execute(insert_query)

        commodity_photos_subquery = [photo_model.car_id.car_id for photo_model in await manager.execute(AdvertPhotos.select(AdvertPhotos.car_id))]
        commodity_query = (CarAdvert
                           .select()
                           .join(CarComplectation, CarBrand, CarModel)
                           .where((CarBrand.id == car_brand) & (CarModel.id == car_model) &
                                  (CarAdvert.id.not_in(commodity_photos_subquery)) &
                                  (CarComplectation.id == car_complectation) & (CarEngine.id == car_engine)))

        insert_data = [{'car_id': car.car_id, 'photo_id': photo['photo_id'], 'photo_unique_id': photo['photo_unique_id']} for car in await manager.execute(commodity_query) for photo in photo_data]

        if insert_data:
            insert_photo_query = AdvertPhotos.insert_many(insert_data)
            await manager.execute(insert_photo_query)

    @staticmethod
    async def try_get_photo(state: FSMContext) -> Optional[list]:
        '''Асинхронная попытка подобрать фотографии для новой заявки на Новый автомобиль'''
        memory_storage = await state.get_data()
        ic(memory_storage)


        complectation = memory_storage['complectation_for_load']
        engine = memory_storage['engine_for_load']
        print('mettka')
        ic(engine, complectation)
        query = NewCarPhotoBase.select().join(CarComplectation).switch(NewCarPhotoBase).join(CarEngine).where(
        (CarComplectation.id == int(complectation)) & (CarEngine.id == int(engine)))
        select_response = list(await manager.execute(query))

        if select_response:
            result = [{'id': data_pack.photo_id, 'unique_id': data_pack.photo_unique_id} for data_pack in
                      select_response]
            return result
        else:
            return None
