from typing import List, Union, Optional

from aiogram.fsm.context import FSMContext
from icecream import install, ic

from database.tables.car_configurations import CarAdvert, CarComplectation, CarModel, CarBrand, CarEngine, CarColor
from database.tables.commodity import NewCarPhotoBase
from database.tables.commodity import AdvertPhotos
from database.db_connect import database, manager

install()


class PhotoRequester:
    @staticmethod
    async def load_photo_in_base(photo_data: List[dict]):
        '''Асинхронный метод для установки фотографий новых автомобилей'''
        if 3 > len(photo_data) > 5:
            raise ValueError('Фотографий должно быть от трёх до пяти (включительно)')

        # await manager.execute(NewCarPhotoBase.insert_many(photo_data))

        # insert_photo_query = AdvertPhotos.insert_many(photo_data)
        # await manager.execute(insert_photo_query)
        # ic(photo_data)
        car_engine = int(photo_data[0]['car_engine'])
        car_complectation = int(photo_data[0]['car_complectation'])
        car_color = int(photo_data[0]['car_color'])
        existing_photos = await manager.execute(NewCarPhotoBase.select().join(CarComplectation)
                                                                        .switch(NewCarPhotoBase).join(CarEngine)
                                                                        .switch(NewCarPhotoBase).join(CarColor)
                                        .where(
                                            (CarEngine.id == car_engine) & (CarComplectation.id == car_complectation) &
                                            (CarColor.id == car_color)))

        if existing_photos:
            ic(car_complectation, car_engine, car_color)
            raise BufferError('Фотографии на эту конфигурацию уже загружены.')
        else:
            insert_query = NewCarPhotoBase.insert_many(photo_data)
            await manager.execute(insert_query)

        exists_photo_adverts = list(await manager.execute(CarAdvert.select(CarAdvert.id).join(AdvertPhotos)))
        ic(exists_photo_adverts)
        commodity_photos_subquery = [AdvertModel.id
                                     for AdvertModel in exists_photo_adverts]

        commodity_query = (CarAdvert
                           .select()
                           .join(CarColor).switch(CarAdvert).join(CarComplectation).join(CarEngine)
                           .where((CarComplectation.id == car_complectation) & (CarEngine.id == car_engine) & (CarColor.id == car_color) &
                                  (CarAdvert.id.not_in(commodity_photos_subquery))))
        nice_cars = list(await manager.execute(commodity_query))

        insert_data = [{'car_id': car.id, 'photo_id': photo['photo_id'], 'photo_unique_id': photo['photo_unique_id']} for car in nice_cars for photo in photo_data]
        # ic(insert_data)
        if insert_data:
            insert_photo_query = AdvertPhotos.insert_many(insert_data)
            await manager.execute(insert_photo_query)

    @staticmethod
    async def try_get_photo(state: FSMContext, color=None) -> Optional[list]:
        '''Асинхронная попытка подобрать фотографии для новой заявки на Новый автомобиль'''
        memory_storage = await state.get_data()
        ic(memory_storage)


        complectation = memory_storage['complectation_for_load']
        engine = memory_storage['engine_for_load']
        color = color if color else memory_storage.get('color_for_load')
        if color is None:
            return None
        ic(engine, complectation)
        query = (NewCarPhotoBase.select().join(CarComplectation)
                                .switch(NewCarPhotoBase).join(CarEngine)
                                .switch(NewCarPhotoBase).join(CarColor).where(
                        (CarComplectation.id == int(complectation)) & (CarEngine.id == int(engine)) &
                                                                       (CarColor.id == color)))
        select_response = list(await manager.execute(query))
        ic(select_response)
        if select_response:
            result = [{'id': data_pack.photo_id, 'unique_id': data_pack.photo_unique_id} for data_pack in
                      select_response]
            return result
        else:
            return None
