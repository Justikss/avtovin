from database.db_connect import database, manager

from database.tables.car_configurations import (CarBrand, CarModel, CarComplectation, CarState,
                                                CarEngine, CarColor, CarMileage, User, CarAdvert, CarYear)
from database.tables.commodity import AdvertPhotos
from database.tables.offers_history import CacheBuyerOffers, ActiveOffers
from database.tables.seller import Seller

class AdvertRequester:
    @staticmethod
    async def update_price(advert_id, new_price):
        try:
            select_request = await manager.execute(CarAdvert.update(price=int(new_price)).where(CarAdvert.id == int(advert_id)))
            return select_request if select_request else False
        except Exception as ex:
            ic(ex)
            return False

    @staticmethod
    async def get_where_id(advert_id: str):
        '''Получение моделей с определённым параметром id'''
        try:
            select_request = await manager.get(CarAdvert.select().where(CarAdvert.id == int(advert_id)))
            ic()
            ic(advert_id, select_request.seller.telegram_id)
            return select_request
        except Exception as ex:
            ic()
            ic(advert_id)
            print('exx', ex)
            return False
    @staticmethod
    async def get_advert_by(state_id, engine_type_id=None, brand_id=None, model_id=None, complectation_id=None,
                            color_id=None, mileage_id=None, year_of_release_id=None):
        query = CarAdvert.select()
        ic(state_id, engine_type_id, brand_id, model_id, complectation_id, color_id, mileage_id, year_of_release_id)
        # Всегда добавляем условие по state_id
        query = query.join(CarState)
        state_id = int(state_id)
        query = query.where(CarState.id == state_id)
        ic(query)
        # Последовательно добавляем условия, если они предоставлены
        if engine_type_id:
            query = query.switch(CarAdvert).join(CarEngine)
            query = query.where(CarEngine.id == int(engine_type_id))
        ic(query)
        if brand_id:
            query = query.switch(CarAdvert).join(CarComplectation).join(CarModel).join(CarBrand)
            query = query.where(CarBrand.id == int(brand_id))

        if model_id:
            # Подразумевается, что предыдущие join уже выполнены
            query = query.where(CarModel.id == int(model_id))

        if complectation_id:
            # Подразумевается, что предыдущие join уже выполнены
            complectation_id = int(complectation_id)
            query = query.where(CarComplectation.id == complectation_id)
            ic()
            print(query)

        if color_id:
            ic()
            query = query.switch(CarAdvert).join(CarColor)
            query = query.where(CarColor.id == int(color_id))

        if mileage_id:
            query = query.switch(CarAdvert).join(CarMileage)
            query = query.where(CarMileage.id == int(mileage_id))

        if year_of_release_id:
            query = query.switch(CarAdvert).join(CarYear)
            query = query.where(CarYear.id == int(year_of_release_id))


        ic(print(query))
        result = list(await manager.execute(query))
        ic(result)
        return result
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
        ic(advert_id)
        current_photo_album = list(await manager.execute(AdvertPhotos.select().join(CarAdvert).where(CarAdvert.id == advert_id)))
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
        ic(advert_id)
        car_advert_subquery = CarAdvert.select().where(CarAdvert.id == advert_id)

        await manager.execute(ActiveOffers.delete().where(ActiveOffers.car_id.in_(car_advert_subquery)))
        await manager.execute(CacheBuyerOffers.delete().where(CacheBuyerOffers.car_id.in_(car_advert_subquery)))
        await manager.execute(AdvertPhotos.delete().where(AdvertPhotos.car_id.in_(car_advert_subquery)))
        return await manager.execute(CarAdvert.delete().where(CarAdvert.id == int(advert_id)))