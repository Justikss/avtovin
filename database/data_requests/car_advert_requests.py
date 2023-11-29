from database.db_connect import database, manager

from database.tables.car_configurations import (CarBrand, CarModel, CarComplectation, CarState,
                                                CarEngine, CarColor, CarMileage, User, CarAdvert, CarYear)
from database.tables.commodity import AdvertPhotos
from database.tables.seller import Seller

class AdvertRequester:
    @staticmethod
    async def get_advert_by_seller(seller_id):
        return list(await manager.execute(CarAdvert.select().where(CarAdvert.seller == seller_id)))

    @staticmethod
    async def get_by_seller_id_and_brand(seller_id, brand):

        query = await manager.execute(CarAdvert
                                    .select()
                                    .join(CarComplectation)  # Соединяем CarAdvert с CarComplectation
                                    .join(CarModel)  # Соединяем CarComplectation с CarModel
                                    .join(CarBrand, on=(CarModel.brand == CarBrand.id))  # Соединяем CarModel с CarBrand
                                    .switch(CarAdvert)  # Переключаемся обратно на CarAdvert
                                    .join(Seller)  # Соединяем CarAdvert с Seller
                                    .where(
                                    (Seller.telegram_id == seller_id) &
                                    (CarBrand.id == brand)
                                    )
                                )
        if query:
            return list(query)

    @staticmethod
    async def get_photo_album_by_advert_id(advert_id, get_list=False):
        '''Метод извлекает фотографии автомобиля'''
        # current_car = CarAdvert.get_by_id(car_id)
        # if current_car:
        current_photo_album = await manager.execute(AdvertPhotos.select().where(AdvertPhotos.car_id == advert_id))
        if current_photo_album:
            current_photo_album = list(current_photo_album)
            if not get_list:
                current_photo_album = [{'id': photo_model.photo_id} for photo_model in current_photo_album]
            else:
                current_photo_album = [photo_model.photo_id for photo_model in current_photo_album]
            return current_photo_album
        else:
            return False

    @staticmethod
    async def delete_advert_by_id(advert_id):
        return await manager.execute(CarAdvert.delete().where(CarAdvert.id == int(advert_id)))