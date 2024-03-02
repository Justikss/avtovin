import asyncio
import importlib
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
    async def update_adverts_photos(adverts, media_group):
        # adverts_media_group - это словарь вида {advert_id: media_group}
        # Сначала получаем все advert_ids

        # Удаляем все старые фотографии для этих объявлений одним запросом
        await manager.execute(AdvertPhotos.delete().where(AdvertPhotos.car_id.in_(adverts)))

        # Подготавливаем все новые фотографии для вставки
        photo_inserts = []
        for advert in adverts:
            for photo in media_group:
                photo_inserts.append({
                    'car_id': advert.id,
                    'photo_id': photo['id'],
                    'photo_unique_id': photo['unique_id']
                })

        # Вставляем все фотографии одним запросом
        if photo_inserts:
            await manager.execute(AdvertPhotos.insert_many(photo_inserts))

    @staticmethod
    async def insert_photos_in_param_branch(media_group, car_color, car_complectation, admin_id):
        if isinstance(media_group, dict):
            media_group = [media_part for media_part in media_group.values()][0]
        photo_base_inserted_data = [{'car_complectation': car_complectation, 'car_color': car_color,
                                     'photo_id': media_part['id'], 'photo_unique_id': media_part['unique_id'],
                                     'admin_id': admin_id} for media_part in media_group]
        ic(photo_base_inserted_data)
        if photo_base_inserted_data:
            advert_requester_module = importlib.import_module('database.data_requests.car_advert_requests')

            seek_photo_base_object_condition = (NewCarPhotoBase.car_complectation == car_complectation) & (NewCarPhotoBase.car_color == car_color)
            if list(await manager.execute(NewCarPhotoBase.select().where(seek_photo_base_object_condition).limit(1))):
                delete_query = await manager.execute(NewCarPhotoBase.delete().where(seek_photo_base_object_condition))
                ic(delete_query)

            insert_query = await manager.execute(NewCarPhotoBase.insert_many(photo_base_inserted_data))
            ic(insert_query)
            ic()
            # adverts = await advert_requester_module\
            #         .AdvertRequester.get_active_adverts_by_complectation_and_color(car_complectation, car_color)
            # ic(adverts, len(adverts))
            adverts = await advert_requester_module\
                    .AdvertRequester.get_advert_by(complectation_id=car_complectation,
                                                          color_id=car_color.id,
                                                          state_id=1,
                                                          without_actual_filter=True)
            ic(adverts, len(adverts))
            asyncio.create_task(PhotoRequester.update_adverts_photos(adverts, media_group))
            return True

    @staticmethod
    async def load_photo_in_base(photo_data: List[dict]):
        '''Асинхронный метод для установки фотографий новых автомобилей
        МЕТОД ДЛЯ ТЕСТИРОВАНИЯ'''
        if 3 > len(photo_data) > 5:
            raise ValueError('Фотографий должно быть от трёх до пяти (включительно)')

        # await manager.execute(NewCarPhotoBase.insert_many(photo_data))

        # insert_photo_query = AdvertPhotos.insert_many(photo_data)
        # await manager.execute(insert_photo_query)
        # ic(photo_data)
        ic(photo_data)
        car_complectation = int(photo_data[0]['car_complectation'])
        car_color = int(photo_data[0]['car_color'])
        # existing_photos = await manager.execute(NewCarPhotoBase.select().join(CarComplectation)
        #                                                                 .switch(NewCarPhotoBase).join(CarColor)
        #                                 .where(
        #                                     (CarComplectation.id == car_complectation) &
        #                                     (CarColor.id == car_color)))
        #
        # if existing_photos:
        #     raise BufferError('Фотографии на эту конфигурацию уже загружены.')
        # else:
        insert_query = NewCarPhotoBase.insert_many(photo_data)
        await manager.execute(insert_query)

        exists_photo_adverts = list(await manager.execute(CarAdvert.select(CarAdvert.id).join(AdvertPhotos)))
        ic(exists_photo_adverts)
        commodity_photos_subquery = [AdvertModel.id
                                     for AdvertModel in exists_photo_adverts]

        commodity_query = (CarAdvert
                           .select()
                           .join(CarColor).switch(CarAdvert).join(CarComplectation)
                           .where((CarComplectation.id == car_complectation) & (CarColor.id == car_color) &
                                  (CarAdvert.id.not_in(commodity_photos_subquery))))
        nice_cars = list(await manager.execute(commodity_query))

        insert_data = [{'car_id': car.id, 'photo_id': photo['photo_id'], 'photo_unique_id': photo['photo_unique_id']} for car in nice_cars for photo in photo_data]
        # ic(insert_data)
        if insert_data:
            insert_photo_query = AdvertPhotos.insert_many(insert_data)
            await manager.execute(insert_photo_query)

    @staticmethod
    async def try_get_photo(state: FSMContext = None, for_admin=False, complectation=None, color=None) -> Optional[list]:
        '''Асинхронная попытка подобрать фотографии для новой заявки на Новый автомобиль'''
        memory_storage = await state.get_data()
        if for_admin:
            ic()
            memory_storage = memory_storage.get('selected_parameters')
        ic(memory_storage)

        if all(not param for param in (complectation, color)):
            complectation = memory_storage['complectation_for_load' if not for_admin else 'complectation']
            color = memory_storage.get('color_for_load' if not for_admin else 'color')

        if any(not param for param in (color, complectation)):
            return

        ic(complectation, color)
        query = (NewCarPhotoBase.select().join(CarComplectation)
                                .switch(NewCarPhotoBase).join(CarColor).where(
                        (CarComplectation.id == complectation) & (CarColor.id == color)))
        select_response = list(await manager.execute(query))
        ic(select_response)
        if select_response:
            result = [{'id': data_pack.photo_id, 'unique_id': data_pack.photo_unique_id} for data_pack in
                      select_response]
            return result
        else:
            return None

    @staticmethod
    async def find_photos_by_complectation_and_color(complectation_id, color_id=None):
        ic(complectation_id, color_id)
        if not color_id:
            query = NewCarPhotoBase.select().where(NewCarPhotoBase.car_complectation == complectation_id)
        else:
            query = NewCarPhotoBase.select().where((NewCarPhotoBase.car_complectation == complectation_id) & (NewCarPhotoBase.car_color == color_id))

        return list(await manager.execute(query))

    @staticmethod
    async def find_photos_by_model_and_engine_and_state(model_id, engine_id, state_id):
        query = NewCarPhotoBase.select().join(CarComplectation).switch(CarComplectation).join(CarEngine).where((CarComplectation.model == model_id) & (CarComplectation.wired_state == state_id) & (CarEngine.id == engine_id))
        return list(await manager.execute(query))

    @staticmethod
    async def find_photos_by_brand_and_engine(brand_id, engine_id, state_id):
        query = (NewCarPhotoBase
                 .select()
                 .join(CarComplectation)
                 .join(CarModel)
                 .switch(CarComplectation)
                 .join(CarEngine)
                 .where((CarModel.brand == brand_id) & (CarComplectation.wired_state == state_id) & (CarEngine.id == engine_id)))
        return list(await manager.execute(query))

    @staticmethod
    async def delete_by_id(photo_id):
        if not isinstance(photo_id, list):
            photo_id = [photo_id]

        good_ids = []
        for id_element in photo_id:
            if not isinstance(id_element, int):
                id_element = int(id_element)
            good_ids.append(id_element)
        ic(good_ids)
        ic(await manager.execute(NewCarPhotoBase.delete().where(NewCarPhotoBase.id.in_(good_ids))))

    @staticmethod
    async def delete_by_color_and_complectation(complectation, color):
        query = NewCarPhotoBase.delete().where(
            ((NewCarPhotoBase.car_complectation == complectation) & (NewCarPhotoBase.car_color == color))
        )
        delete_response = await manager.execute(query)
        return delete_response