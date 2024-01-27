from peewee import fn


from database.data_requests.recomendations_request import RecommendationRequester
from database.data_requests.statistic_requests.adverts_to_admin_view_status import \
    advert_to_admin_view_related_requester
from database.data_requests.utils.sort_objects_alphabetically import sort_objects_alphabetically

from database.db_connect import database, manager

from database.tables.car_configurations import (CarBrand, CarModel, CarComplectation, CarState,
                                                CarEngine, CarColor, CarMileage, CarAdvert, CarYear)
from database.tables.commodity import AdvertPhotos
from database.tables.offers_history import CacheBuyerOffers, ActiveOffers
from database.tables.seller import Seller
from database.tables.statistic_tables.advert_parameters import AdvertParameters
from database.tables.user import User


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
            related_ids_tuple = tuple(related_ids)  # Преобразуем список в кортеж для безопасного форматирования
            raw_sql = f"SELECT * FROM {related_model._meta.table_name} WHERE id IN %s" % (related_ids_tuple,)

            related_objects = await manager.execute(related_model.raw(raw_sql))

            # related_objects = await manager.execute(related_model.select().where(related_model.id.in_(related_ids)))
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
        if isinstance(adverts[0], CarAdvert):
            await async_fetch_related(adverts, Seller, 'seller_id', 'seller')

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


    @staticmethod
    async def get_advert_by(state_id=None, engine_type_id=None, brand_id=None, model_id=None, complectation_id=None,
                            color_id=None, mileage_id=None, year_of_release_id=None, seller_id=None,
                            without_actual_filter=None, buyer_search_mode=False):
        ic(state_id, engine_type_id, brand_id, model_id, complectation_id, color_id, mileage_id, year_of_release_id, seller_id)
        int_flag = None
        result_adverts = None

        if not without_actual_filter:
            query = CarAdvert.select().where((CarAdvert.sleep_status == False) | (CarAdvert.sleep_status.is_null(True)))
        else:
            query = CarAdvert.select()

        if (query and buyer_search_mode) and str(buyer_search_mode):
            if isinstance(buyer_search_mode, str):
                buyer_search_mode = int(buyer_search_mode)
            ic(buyer_search_mode)
            query = query.where((CarAdvert.id.not_in(
                ActiveOffers.select(CarAdvert.id).join(CarAdvert).switch(ActiveOffers).join(User).switch(CarAdvert).where(
                    ((ActiveOffers.buyer_id == buyer_search_mode)))
            )) & (CarAdvert.id.not_in(CarAdvert.select(CarAdvert.id).where(CarAdvert.seller_id == buyer_search_mode))))
        #     print(query)
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
            sub_query = (sub_query.switch(CarAdvert).join(CarColor, on=(CarColor.id == CarAdvert.color))
                         .where((CarComplectation.id == int(complectation_id)) if complectation_id != 'null' else True))
            query = sub_query.select(CarColor.id)
            last_table = CarColor

        if color_id:

            ic()

            sub_query = sub_query.where((CarColor.id == int(color_id))
                                        if color_id != 'null' else True)
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

            query = sub_query.switch(CarAdvert).join(CarMileage).where((CarMileage.id == int(mileage_id))
                                                                       if mileage_id != 'null' else True)
            # query = sub_query.switch(CarAdvert).join(CarYear).select(CarYear)

        if year_of_release_id:
            ic()

            query = query.switch(CarAdvert).join(CarYear).where((CarYear.id == int(year_of_release_id))
                                                                if year_of_release_id != 'null' else True)
            last_table, int_flag = None, None



        query = query.distinct()
        ic(without_actual_filter, int_flag, seller_id)
        if without_actual_filter:
            query = query.select(CarAdvert)
            result_adverts = list(await manager.execute(query))
            if without_actual_filter == 'for_deletion':
                ic(result_adverts)
                # ic(result_adverts[0].__dict__)

                return result_adverts
            ic()
        else:
            # ic(int_flag)
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
                        fn.NULLIF(fn.REGEXP_REPLACE(int_flag.name, '[^0-9].*$', ''), '').cast('integer').desc(),
                        int_flag.name.desc()))
                ic()
                result_adverts = list(await manager.execute(query))
                ic(result_adverts)
                if not result_adverts:
                    return False


            if not result_adverts:
                if not seller_id and last_table:
                    query = last_table.select().where(last_table.id.in_(query))


                if (seller_id or int_flag):
                    result_adverts = list(await manager.execute(query))
                    ic(result_adverts)
                    ic()

            if not result_adverts:
                result_adverts = list(await manager.execute(query))
                ic(result_adverts)
                ic()

            if seller_id and not last_table:
                result_adverts = await AdvertRequester.load_related_data_for_advert(result_adverts)
                ic(result_adverts)
                ic()

        if result_adverts:
            if not isinstance(result_adverts, list):
                result_adverts = [result_adverts]
            result_adverts = [advert for advert in result_adverts if advert.id is not None]

            if hasattr(result_adverts[0], 'name'):
                if not result_adverts[0].name.replace('.', '').replace('-', '').isdigit():
                    result_adverts = await sort_objects_alphabetically(result_adverts)

        ic(result_adverts)

        return result_adverts


    @staticmethod
    async def get_active_adverts_by_complectation_and_color(complectation, color):
        # Получение активных объявлений
        result = list(await manager.execute(CarAdvert.select().where(
            (CarAdvert.state == 1) &
            (CarAdvert.complectation == complectation) &
            (CarAdvert.color == color)
        )))

        if result:
            if hasattr(result[0], 'name'):
                result = await sort_objects_alphabetically(result)

        return result

    @staticmethod
    async def get_unique_engine_types(current_query):
        # Подзапрос для получения уникальных типов двигателей
        unique_engine_types_query = (CarEngine
                                     .select()
                                     .join(CarComplectation)
                                     .where(CarComplectation.id.in_(current_query.select(CarComplectation.id)))
                                     .distinct())

        result = list(await manager.execute(unique_engine_types_query))

        if result:
            if hasattr(result[0], 'name'):
                result = await sort_objects_alphabetically(result)

        return result

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
        result = list(await manager.execute(query))
        if result:
            if hasattr(result[0], 'name'):
                result = await sort_objects_alphabetically(result)

        return result

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
        if len(adverts) == 1:
            result = await manager.get_or_none(CarAdvert, CarAdvert.id == adverts[0])
        await manager.execute(CarAdvert.delete().where((CarAdvert.id.in_(car_advert_subquery)) & (CarAdvert.seller == seller_id)))
        if result:
            return result
