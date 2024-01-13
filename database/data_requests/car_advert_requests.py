from peewee import fn

from database.data_requests.car_configurations_requests import CarConfigs
from database.data_requests.recomendations_request import RecommendationRequester
from database.data_requests.statistic_requests.adverts_to_admin_view_status import \
    advert_to_admin_view_related_requester
from database.data_requests.utils.set_color_1_in_last_position import set_other_color_on_last_position
from database.db_connect import database, manager

from database.tables.car_configurations import (CarBrand, CarModel, CarComplectation, CarState,
                                                CarEngine, CarColor, CarMileage, CarAdvert, CarYear)
from database.tables.commodity import AdvertPhotos
from database.tables.offers_history import CacheBuyerOffers, ActiveOffers
from database.tables.seller import Seller
from database.tables.statistic_tables.advert_parameters import AdvertParameters


class AdvertRequester:
    @staticmethod
    async def load_related_data_for_advert(advert):
        async def async_fetch_deep_related(objects, intermediate_model, final_model, intermediate_field, final_field):
            if not objects:
                return []

            intermediate_ids = {getattr(obj, intermediate_field) for obj in objects if getattr(obj, intermediate_field)}
            intermediate_objects = await manager.execute(
                intermediate_model.select().where(intermediate_model.id.in_(intermediate_ids)))

            final_ids = {getattr(intermediate_obj, final_field) for intermediate_obj in intermediate_objects if
                         getattr(intermediate_obj, final_field)}
            final_objects = await manager.execute(final_model.select().where(final_model.id.in_(final_ids)))

            final_dict = {final_obj.id: final_obj for final_obj in final_objects}
            intermediate_dict = {intermediate_obj.id: intermediate_obj for intermediate_obj in intermediate_objects}

            for intermediate_obj in intermediate_objects:
                setattr(intermediate_obj, final_model.__name__.lower(),
                        final_dict.get(getattr(intermediate_obj, final_field)))

            for obj in objects:
                setattr(obj, intermediate_model.__name__.lower(),
                        intermediate_dict.get(getattr(obj, intermediate_field)))

            return objects

        async def async_fetch_related(objects, related_model, foreign_key_field, related_field_name):
            if not objects:
                return []

            related_ids = {getattr(obj, foreign_key_field) for obj in objects if getattr(obj, foreign_key_field)}
            related_objects = await manager.execute(related_model.select().where(related_model.id.in_(related_ids)))
            related_dict = {related.id: related for related in related_objects}

            for obj in objects:
                setattr(obj, related_field_name, related_dict.get(getattr(obj, foreign_key_field)))

            return objects
        """"""
        ic(advert)
        if not advert:
            return []
        elif not isinstance(advert, list):
            adverts = [advert]
        else:
            adverts = advert

        if not isinstance(adverts[0], (CarAdvert, AdvertParameters)):
            adverts = [offer.car_id for offer in adverts]

        ic(adverts)

        adverts = await async_fetch_related(adverts, CarComplectation, 'complectation_id', 'complectation')
        await async_fetch_deep_related([advert.complectation for advert in adverts],  CarModel, CarBrand, 'model_id', 'brand_id')
        # await async_fetch_deep_related([advert.complectation for advert in adverts],  CarComplectation, CarEngine, 'complectation', 'engine_id')

        await async_fetch_related(adverts, CarColor, 'color_id', 'color')
        await async_fetch_related([advert.complectation for advert in adverts], CarEngine, 'engine_id', 'engine ')


        return adverts if not len(adverts) == 1 else adverts[0]

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
    async def get_where_id(advert_id: str | int | list):
        '''Получение моделей с определённым параметром id'''
        ic(advert_id)

        base_query = None
        if isinstance(advert_id, list):
            base_query = CarAdvert.select().where(CarAdvert.id.in_(advert_id))

        if isinstance(advert_id, str):
            advert_id = int(advert_id)
            ic(advert_id)

        if not base_query:

            base_query = CarAdvert.select().where(CarAdvert.id == advert_id)

        try:
            advert = await manager.get(base_query)
        except:
            return None
        # Загрузка связанных данных
        return await AdvertRequester.load_related_data_for_advert(advert)


    # @staticmethod
    # async def delete_adverts_by_seller(seller):
    #     await manager.execute(CarAdvert.delete().where(CarAdvert.seller == seller))
    # @staticmethod
    # async def get_unique_values(state_id=None, engine_type_id=None, brand_id=None, model_id=None, complectation_id=None, color_id=None, mileage_id=None, year_of_release_id=None):
    #     # Формирование базового запроса
    #     int_flag = False
    #     query = None
    #     ic(state_id, engine_type_id, brand_id, model_id, complectation_id, color_id, mileage_id, year_of_release_id)
    #     if state_id:
    #         query = CarEngine.select().join(CarComplectation).join(CarAdvert).where(CarAdvert.state == state_id).order_by(CarEngine.id)
    #     if engine_type_id:
    #         query = CarBrand.select().join(CarModel).join(CarComplectation).join(CarAdvert).switch(CarComplectation).where((CarComplectation.engine == engine_type_id) & (CarComplectation.engine.in_(query))).order_by(CarBrand.id)
    #     if brand_id:
    #         query = CarModel.select().where((CarModel.brand == brand_id) & (CarModel.brand.in_(query))).order_by(CarModel.id)
    #     if model_id:
    #         query = CarComplectation.select().where((CarComplectation.model == model_id) & (CarComplectation.model.in_(query))).order_by(CarComplectation.id)
    #     if complectation_id:
    #         query = CarColor.select().join(CarAdvert).where((CarAdvert.complectation == complectation_id) & (CarAdvert.complectation.in_(query))).order_by(CarColor.id)
    #     if color_id:
    #         query = CarMileage.select().join(CarAdvert).join(CarComplectation).where((CarAdvert.color == color_id) & (CarAdvert.complectation_id == complectation_id)).distinct()
    #         int_flag = CarMileage
    #     if mileage_id:
    #         query = CarYear.select().join(CarAdvert).join(CarComplectation).where((CarAdvert.mileage == mileage_id) & (CarAdvert.complectation_id == complectation_id)).distinct()
    #         int_flag = CarYear
    #     if year_of_release_id:
    #         query = CarAdvert.select().where((CarAdvert.year == year_of_release_id) & (CarAdvert.year.in_(query)))
    #
    #     if int_flag:
    #         query = (int_flag
    #         .select(int_flag.id, int_flag.name)
    #         .join(query, on=(int_flag.id == query.c.id))
    #         .where(int_flag.id.in_(query))
    #         .order_by(
    #             fn.NULLIF(fn.REGEXP_REPLACE(int_flag.name, '[^0-9].*$', ''), '').cast('integer'),
    #             int_flag.name))
    #     else:
    #         query = query.distinct()
    #
    #     if query:
    #
    #         results = await manager.execute(query)
    #         return [item for item in results]
    #     else:
    #         return []
    #

    @staticmethod
    async def get_advert_by(state_id=None, engine_type_id=None, brand_id=None, model_id=None, complectation_id=None,
                            color_id=None, mileage_id=None, year_of_release_id=None, seller_id=None, without_actual_filter=None):
        ic(state_id, engine_type_id, brand_id, model_id, complectation_id, color_id, mileage_id, year_of_release_id, seller_id)
        int_flag = None
        result_adverts = None

        if not without_actual_filter:
            query = CarAdvert.select().where((CarAdvert.sleep_status == False) | (CarAdvert.sleep_status.is_null(True)))
        else:
            query = CarAdvert.select()

        if seller_id:
            ic()
            query = query.join(Seller).where(Seller.telegram_id == int(seller_id))
            query = query.switch(CarAdvert)

        if state_id:
            state_id = int(state_id)
            query = query.join(CarState).where(CarState.id == state_id)

        sub_query = query.select().switch(CarAdvert).join(CarComplectation).join(CarEngine)
        query = sub_query.select(CarEngine.id)
        last_table = CarEngine

        if engine_type_id:
            ic()
            sub_query = sub_query.switch(CarComplectation).join(CarModel).join(CarBrand).where(CarEngine.id == int(engine_type_id))
            query = sub_query.select(CarBrand.id)

            last_table = CarBrand
        if brand_id:
            ic()
            sub_query = sub_query.where(CarBrand.id == int(brand_id))
            query = sub_query.select(CarModel.id)
            last_table = CarModel

        if model_id:
            ic()
            sub_query = sub_query.where(CarModel.id == int(model_id))
            query = sub_query.select(CarComplectation.id)
            last_table = CarComplectation

        if complectation_id:
            ic()
            # Подразумевается, что предыдущие join уже выполнены
            complectation_id = int(complectation_id)
            sub_query = sub_query.switch(CarAdvert).join(CarColor, on=(CarColor.id == CarAdvert.color)).where(CarComplectation.id == complectation_id)
            query = sub_query.select(CarColor.id)
            last_table = CarColor

        if color_id:

            ic()
            sub_query = sub_query.where(CarColor.id == int(color_id))
            if state_id == 2:
                int_flag = CarMileage
                query = sub_query.select(CarMileage.id).switch(CarAdvert).join(CarMileage)
                last_table = CarMileage
            else:
                query = sub_query
                last_table = None


        if mileage_id:
            int_flag, last_table = CarYear, CarYear
            ic()
            query = sub_query.switch(CarAdvert).join(CarMileage).where(CarMileage.id == int(mileage_id))
            # query = sub_query.switch(CarAdvert).join(CarYear).select(CarYear)

        if year_of_release_id:
            ic()
            query = query.switch(CarAdvert).join(CarYear).where(CarYear.id == int(year_of_release_id))
            last_table, int_flag = None, None


        query = query.distinct()
        print(query)
        if without_actual_filter:
            result_adverts = list(await manager.execute(query))
        else:
            if (int_flag and not seller_id) and state_id == 2:
                if int_flag == CarMileage:
                    sub_query_ids = sub_query.select(CarAdvert.mileage_id).distinct()
                    query = (CarMileage
                    .select(CarMileage.id, CarMileage.name)
                    .join(sub_query_ids, on=(CarMileage.id == sub_query_ids.c.mileage_id))
                    .order_by(
                        fn.NULLIF(fn.REGEXP_REPLACE(CarMileage.name, '[^0-9].*$', ''), '').cast('integer'),
                        CarMileage.name))
                elif int_flag == CarYear:
                    sub_query_ids = sub_query.select(CarAdvert.year_id).distinct()

                    query = (int_flag
                    .select(int_flag.id, int_flag.name)
                    .join(sub_query_ids, on=(int_flag.id == sub_query_ids.c.year_id))
                    .order_by(
                        fn.NULLIF(fn.REGEXP_REPLACE(int_flag.name, '[^0-9].*$', ''), '').cast('integer'),
                        int_flag.name))
                result_adverts = list(await manager.execute(query))


            if not result_adverts:
                if not seller_id and last_table:
                    query = last_table.select().where(last_table.id.in_(query))

                if (seller_id or int_flag):
                    result_adverts = list(await manager.execute(query))

            if not result_adverts:
                result_adverts = list(await manager.execute(query))

            if seller_id and not last_table:
                result_adverts = await AdvertRequester.load_related_data_for_advert(result_adverts)

        if result_adverts:
            result_adverts = [advert for advert in result_adverts if advert.id is not None]

        ic(result_adverts)

        return result_adverts

    # @staticmethod
    # async def get_unique_values(model_class, base_query):
    #     query = None
    #
    #     adverts = await AdvertRequester.load_related_data_for_advert(list(await manager.execute(base_query)))
    #     if adverts:
    #         if not isinstance(adverts, list):
    #             adverts = [adverts]
    #         advert_ids = [advert.id for advert in adverts]
    #         ic()
    #         ic(adverts)
    #         if model_class == CarEngine:
    #             query = (CarEngine
    #                      .select()
    #                      .join(CarComplectation)
    #                      .join(CarAdvert)
    #                      .where(CarAdvert.id.in_(advert_ids))
    #                      .distinct())
    #         elif model_class == CarBrand:
    #             query = (CarBrand
    #                      .select()
    #                      .join(CarModel)
    #                      .join(CarComplectation)
    #                      .join(CarAdvert)
    #                      .where(CarAdvert.id.in_(advert_ids))
    #                      .distinct())
    #         elif model_class == CarModel:
    #             query = (CarModel
    #                      .select()
    #                      .join(CarComplectation, on=(CarComplectation.model == CarModel.id))
    #                      .join(CarAdvert, on=(CarAdvert.complectation == CarComplectation.id))
    #                      .where(CarAdvert.id.in_(advert_ids))
    #                      .distinct())
    #         elif model_class == CarColor:
    #             query = (CarColor
    #                      .select()
    #                      .join(CarAdvert, on=(CarAdvert.color == CarColor.id))
    #                      .where(CarAdvert.id.in_(advert_ids))
    #                      .distinct())
    #         elif model_class == CarMileage:
    #             query = (CarMileage
    #                      .select()
    #                      .join(CarAdvert, on=(CarAdvert.mileage == CarMileage.id))
    #                      .where(CarAdvert.id.in_(advert_ids))
    #                      .distinct())
    #         elif model_class == CarYear:
    #             query = (CarYear
    #                      .select()
    #                      .join(CarAdvert, on=(CarAdvert.year == CarYear.id))
    #                      .where(CarAdvert.id.in_(advert_ids))
    #                      .distinct())
    #         elif model_class == CarState:
    #             query = (CarState
    #                      .select()
    #                      .join(CarAdvert, on=(CarAdvert.state == CarState.id))
    #                      .where(CarAdvert.id.in_(advert_ids))
    #                      .distinct())
    #         elif model_class == CarComplectation:
    #             query = (CarComplectation.select().join(CarAdvert).where(CarAdvert.id.in_(advert_ids)).distinct())
    #
    #         result = list(await manager.execute(query))
    #         if result and model_class == CarColor:
    #             result = await set_other_color_on_last_position(result)
    #         return result
    #     else:
    #         return False

    @staticmethod
    async def get_active_adverts_by_complectation_and_color(complectation, color):
        # Получение активных объявлений
        return list(await manager.execute(CarAdvert.select().where(
            (CarAdvert.state == 1) &
            (CarAdvert.complectation == complectation) &
            (CarAdvert.color == color)
        )))

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
        if not isinstance(seller_id, int):
            seller_id = seller_id.telegram_id
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
        return list(await manager.execute(CarAdvert.select().where(CarAdvert.seller == seller_id).order_by(CarAdvert.id)))

    @staticmethod
    async def get_by_seller_id_and_brand(seller_id, brand):
        ic(seller_id, brand)
        query = await manager.execute((CarAdvert
                                      .select(CarAdvert.id)
                                      .join(CarComplectation)
                                      .join(CarModel)
                                      .join(CarBrand, on=(CarModel.brand == CarBrand.id))
                                      .switch(CarAdvert)
                                      .join(Seller)

                                      .where((Seller.telegram_id == seller_id) & (CarBrand.id == brand)).order_by(CarAdvert.id)
        ))
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
    async def remove_user_view_to_advert(seller_id, advert_id):
        ic(advert_id)
        if not isinstance(advert_id, list):
            advert_id = [advert_id]
        advert_id = [advert.id if isinstance(advert, CarAdvert) else advert for advert in advert_id]
        ic(advert_id)
        car_advert_subquery = CarAdvert.select().where((CarAdvert.id.in_(advert_id)) & (CarAdvert.seller == seller_id))

        await manager.execute(CacheBuyerOffers.delete().where(CacheBuyerOffers.car_id.in_(car_advert_subquery)))
        await RecommendationRequester.remove_recommendation_by_advert_id(advert_id)

        return car_advert_subquery

    @staticmethod
    async def delete_advert_by_id(seller_id, advert_id=None):
        if isinstance(seller_id, str):
            seller_id = int(seller_id)

        if not advert_id:
            adverts = await AdvertRequester.get_advert_by_seller(seller_id)
        else:
            adverts = [advert_id]
        ic(adverts, seller_id)
        result = []
        # for advert_id in adverts:
        #     if not isinstance(advert_id, int):
        #         advert_id = advert_id.id
        car_advert_subquery = await AdvertRequester.remove_user_view_to_advert(seller_id, adverts)
        # await manager.execute(ActiveOffers.delete().where(ActiveOffers.car_id.in_(car_advert_subquery)))
        # await manager.execute(CacheBuyerOffers.delete().where(CacheBuyerOffers.car_id.in_(car_advert_subquery)))
        # await RecommendationRequester.remove_recommendation_by_advert_id(advert_id)
        await manager.execute(ActiveOffers.delete().where(ActiveOffers.car_id.in_(car_advert_subquery)))
        await manager.execute(AdvertPhotos.delete().where(AdvertPhotos.car_id.in_(car_advert_subquery)))
        await advert_to_admin_view_related_requester.delete_relation(adverts)
        result.append(await manager.execute(CarAdvert.delete().where((CarAdvert.id.in_(car_advert_subquery)) & (CarAdvert.seller == seller_id))))
        if result:
            return result
