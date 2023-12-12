from database.data_requests.car_configurations_requests import CarConfigs
from database.data_requests.recomendations_request import RecommendationRequester
from database.db_connect import database, manager

from database.tables.car_configurations import (CarBrand, CarModel, CarComplectation, CarState,
                                                CarEngine, CarColor, CarMileage, User, CarAdvert, CarYear)
from database.tables.commodity import AdvertPhotos
from database.tables.offers_history import CacheBuyerOffers, ActiveOffers
from database.tables.seller import Seller

class AdvertRequester:
    @staticmethod
    async def set_sleep_status(sleep_status: bool, seller_id=None, advert_id=None):
        adverts = await AdvertRequester.get_advert_by_seller(seller_id)
        if adverts:
            adverts = [advert.id for advert in adverts]
            await manager.execute(CarAdvert.update(sleep_status=sleep_status).where(CarAdvert.id.in_(adverts)))

    @staticmethod
    async def update_price(advert_id, new_price, head_valute):
        try:
            if head_valute == 'sum':
                update_request = await manager.execute(CarAdvert.update(sum_price=int(new_price)).where(CarAdvert.id == int(advert_id)))
                delete_update_request = await manager.execute(CarAdvert.update(dollar_price=None).where(CarAdvert.id == int(advert_id)))

            elif head_valute == 'usd':
                update_request = await manager.execute(CarAdvert.update(dollar_price=int(new_price)).where(CarAdvert.id == int(advert_id)))
                delete_update_request = await manager.execute(CarAdvert.update(sum_price=None).where(CarAdvert.id == int(advert_id)))


            return (update_request, delete_update_request) if (update_request, delete_update_request) else False
        except Exception as ex:
            ic(ex)
            return False

    @staticmethod
    async def get_where_id(advert_id: str):
        '''Получение моделей с определённым параметром id'''
        try:
            select_request = await manager.get(CarAdvert.select().join(Seller).where(CarAdvert.id == int(advert_id)))
            ic()
            ic(advert_id, select_request.seller.telegram_id)
            return select_request
        except Exception as ex:
            ic()
            ic(advert_id)
            print('exx', ex)
            return False

    # @staticmethod
    # async def delete_adverts_by_seller(seller):
    #     await manager.execute(CarAdvert.delete().where(CarAdvert.seller == seller))

    @staticmethod
    async def get_advert_by(state_id, engine_type_id=None, brand_id=None, model_id=None, complectation_id=None,
                            color_id=None, mileage_id=None, year_of_release_id=None, seller_id=None):
        ic(state_id, engine_type_id, brand_id, model_id, complectation_id, color_id, mileage_id, year_of_release_id, seller_id)

        unique_models = None

        query = CarAdvert.select().where((CarAdvert.sleep_status == False) | (CarAdvert.sleep_status.is_null(True)))
        if seller_id:
            query = query.join(Seller).where(Seller.telegram_id == int(seller_id))
            query = query.switch(CarAdvert)
        # Всегда добавляем условие по state_id
        query = query.join(CarState)
        state_id = int(state_id)
        query = query.where(CarState.id == state_id)
        ic(query)
        # Последовательно добавляем условия, если они предоставлены
        if engine_type_id:
            query = query.switch(CarAdvert).join(CarComplectation).join(CarEngine)
            query = query.where(CarEngine.id == int(engine_type_id))
        else:
            unique_models = await AdvertRequester.get_unique_values(CarEngine, query)


        ic(query)

        query = query.switch(CarComplectation).join(CarModel).join(CarBrand)
        if brand_id:

            query = query.where(CarBrand.id == int(brand_id))
        elif not unique_models:
            unique_models = await AdvertRequester.get_unique_values(CarBrand, query)

        if model_id:
            # Подразумевается, что предыдущие join уже выполнены
            query = query.where(CarModel.id == int(model_id))
        elif not unique_models:
            unique_models = await AdvertRequester.get_unique_values(CarModel, query)

        if complectation_id:
            # Подразумевается, что предыдущие join уже выполнены
            complectation_id = int(complectation_id)
            query = query.where(CarComplectation.id == complectation_id)
            ic()
            print(query)
        elif not unique_models:
            unique_models = await AdvertRequester.get_unique_values(CarComplectation, query)
        query = query.switch(CarAdvert).join(CarColor)
        if color_id:
            ic()

            if str(color_id).isdigit():
                query = query.where(CarColor.id == int(color_id))
            else:
                color_name = color_id
                color_object = await CarConfigs.get_by_name(color_name, 'color')
                if color_object:
                    query = query.where(CarColor.name == color_name)
        elif not unique_models:
            unique_models = await AdvertRequester.get_unique_values(CarColor, query)
        query = query.switch(CarAdvert).join(CarMileage)
        if mileage_id:
            query = query.where(CarMileage.id == int(mileage_id))
        elif not unique_models:
            unique_models = await AdvertRequester.get_unique_values(CarMileage, query)

        query = query.switch(CarAdvert).join(CarYear)
        if year_of_release_id:
            query = query.where(CarYear.id == int(year_of_release_id))
        elif not unique_models:
            ic()
            unique_models = await AdvertRequester.get_unique_values(CarYear, query)
        ic(unique_models)
        print(query)
        ic(print(query))
        if unique_models:
            return unique_models
        result = list(await manager.execute(query))
        ic(result)
        return result

    @staticmethod
    async def get_advert_models(state_id, engine_type_id=None, brand_id=None, model_id=None, complectation_id=None,
                            color_id=None, mileage_id=None, year_of_release_id=None, seller_id=None):
        # ... Предыдущий код ...

        query = CarAdvert.select().where((CarAdvert.sleep_status == False) | (CarAdvert.sleep_status.is_null(True)))

        if seller_id:
            query = query.join(Seller).where(Seller.telegram_id == int(seller_id))
            query = query.switch(CarAdvert)

        query = query.join(CarState).where(CarState.id == int(state_id))

        if engine_type_id:
            query = query.switch(CarAdvert).join(CarComplectation).join(CarEngine).where(
                CarEngine.id == int(engine_type_id))
            query = query.switch(CarAdvert)

        if brand_id:
            query = query.switch(CarComplectation).join(CarModel).join(CarBrand).where(CarBrand.id == int(brand_id))
            query = query.switch(CarAdvert)

        if model_id:
            query = query.where(CarModel.id == int(model_id))
            query = query.switch(CarAdvert)

        if complectation_id:
            query = query.where(CarComplectation.id == int(complectation_id))
            query = query.switch(CarAdvert)

        if color_id:
            query = query.join(CarColor).where(
                CarColor.id == int(color_id) if str(color_id).isdigit() else CarColor.name == color_id)
            query = query.switch(CarAdvert)

        if mileage_id:
            query = query.join(CarMileage).where(CarMileage.id == int(mileage_id))
            query = query.switch(CarAdvert)

        if year_of_release_id:
            query = query.join(CarYear).where(CarYear.id == int(year_of_release_id))
            query = query.switch(CarAdvert)

        result = list(await manager.execute(query))
        return result

    @staticmethod
    async def get_unique_values(model_class, base_query):
        ic(model_class, base_query)
        if model_class == CarEngine:
            query = (CarEngine
                     .select()
                     .join(CarComplectation)
                     .join(CarAdvert)
                     .where(CarAdvert.id.in_(base_query.select(CarAdvert.id)))
                     .distinct())
        elif model_class == CarBrand:
            query = (CarBrand
                     .select()
                     .join(CarModel)
                     .join(CarComplectation)
                     .join(CarAdvert)
                     .where(CarAdvert.id.in_(base_query.select(CarAdvert.id)))
                     .distinct())
        elif model_class == CarModel:
            query = (CarModel
                     .select()
                     .join(CarComplectation, on=(CarComplectation.model == CarModel.id))
                     .join(CarAdvert, on=(CarAdvert.complectation == CarComplectation.id))
                     .where(CarAdvert.id.in_(base_query.select(CarAdvert.id)))
                     .distinct())
        elif model_class == CarColor:
            query = (CarColor
                     .select()
                     .join(CarAdvert, on=(CarAdvert.color == CarColor.id))
                     .where(CarAdvert.id.in_(base_query.select(CarAdvert.id)))
                     .distinct())
        elif model_class == CarMileage:
            query = (CarMileage
                     .select()
                     .join(CarAdvert, on=(CarAdvert.mileage == CarMileage.id))
                     .where(CarAdvert.id.in_(base_query.select(CarAdvert.id)))
                     .distinct())
        elif model_class == CarYear:
            query = (CarYear
                     .select()
                     .join(CarAdvert, on=(CarAdvert.year == CarYear.id))
                     .where(CarAdvert.id.in_(base_query.select(CarAdvert.id)))
                     .distinct())
        elif model_class == CarState:
            query = (CarState
                     .select()
                     .join(CarAdvert, on=(CarAdvert.state == CarState.id))
                     .where(CarAdvert.id.in_(base_query.select(CarAdvert.id)))
                     .distinct())
        elif model_class == CarComplectation:
            query = (CarComplectation.select().join(CarAdvert).where(CarAdvert.id.in_(base_query.select(CarAdvert.id))).distinct())
        return list(await manager.execute(query))

    @staticmethod
    async def get_unique_engine_types(current_query):
        # Подзапрос для получения уникальных типов двигателей
        unique_engine_types_query = (CarEngine
                                     .select()
                                     .join(CarComplectation)
                                     .where(CarComplectation.id.in_(current_query.select(CarComplectation.id)))
                                     .distinct())

        return list(await manager.execute(unique_engine_types_query))

    @staticmethod
    async def get_advert_brands_by_seller_id(seller_id):
        query = (CarBrand
                 .select()
                 .distinct()
                 .join(CarModel, on=(CarBrand.id == CarModel.brand))
                 .join(CarComplectation, on=(CarModel.id == CarComplectation.model))
                 .join(CarAdvert, on=(CarComplectation.id == CarAdvert.complectation))
                 .join(Seller)
                 .where(
            Seller.telegram_id == seller_id))  # предполагаем, что seller_telegram_id - это ваш идентификатор

        # Теперь выполним запрос и получим результат
        unique_brands = list(await manager.execute(query))
        return unique_brands

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
    async def delete_advert_by_id(seller_id, advert_id=None):
        if isinstance(seller_id, str):
            seller_id = int(seller_id)

        if not advert_id:
            adverts = await AdvertRequester.get_advert_by_seller(seller_id)
        else:
            adverts = [advert_id]
        ic(advert_id, seller_id)
        result = []
        for advert_id in adverts:
            if not isinstance(advert_id, int):
                advert_id = advert_id.id
            car_advert_subquery = CarAdvert.select().where((CarAdvert.id == advert_id) & (CarAdvert.seller == seller_id))
            await manager.execute(ActiveOffers.delete().where(ActiveOffers.car_id.in_(car_advert_subquery)))
            await manager.execute(CacheBuyerOffers.delete().where(CacheBuyerOffers.car_id.in_(car_advert_subquery)))
            await manager.execute(AdvertPhotos.delete().where(AdvertPhotos.car_id.in_(car_advert_subquery)))
            await RecommendationRequester.remove_recommendation_by_advert_id(advert_id)
            result.append(await manager.execute(CarAdvert.delete().where((CarAdvert.id == int(advert_id)) & (CarAdvert.seller == int(seller_id)))))
        if result:
            return result
