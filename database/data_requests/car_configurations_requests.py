import asyncio
import importlib
import json
import logging
import random
import traceback
from asyncio import Queue
from collections import defaultdict
from datetime import timedelta, datetime
from functools import reduce
from typing import List, Optional

from peewee import JOIN, IntegrityError, fn, Expression, DoesNotExist

from database.data_requests.new_car_photo_requests import PhotoRequester
from database.data_requests.statistic_requests.adverts_to_admin_view_status import \
    advert_to_admin_view_related_requester
from database.data_requests.utils.raw_sql_handler import execute_raw_sql
from database.data_requests.utils.set_color_1_in_last_position import set_other_color_on_last_position
from database.data_requests.utils.sort_objects_alphabetically import sort_objects_alphabetically
from database.db_connect import database, manager
from database.tables.admin import Admin

from database.tables.car_configurations import (CarBrand, CarModel, CarComplectation, CarState,
                                                CarEngine, CarColor, CarMileage, CarAdvert, CarYear)
from database.tables.commodity import AdvertPhotos, NewCarPhotoBase
from database.tables.offers_history import SellerFeedbacksHistory
from database.tables.seller import Seller
from database.tables.statistic_tables.advert_parameters import AdvertParameters
from database.tables.user import User
from utils.translator import translate

cache_redis_module = importlib.import_module('utils.redis_for_language')
cache_redis = cache_redis_module.cache_redis

def to_int(value):
    if isinstance(value, str) and value.isdigit():
        value = int(value)

    return value

class CarConfigs:
    @staticmethod
    async def get_model_by_brand_and_name(brand_id, model_name):

        model = await manager.get_or_none(CarModel, CarModel.name == model_name, CarModel.brand == brand_id)
        return model

    @staticmethod
    async def get_branch(params):


        complectation = params['complectation']
        if isinstance(complectation, dict):
            if complectation.get('_name'):
                complectation_condition = CarComplectation._name == complectation['_name']
            else:
                complectation_condition = ((CarComplectation.name_uz == complectation['name_uz']) & (CarComplectation.name_ru == complectation['name_ru']))
        else:
            complectation_condition = CarComplectation.id == complectation


        query = NewCarPhotoBase.select().join(CarComplectation).switch(NewCarPhotoBase).join(CarColor).where(
            (
                    (CarColor.id == params['color']) &
                    (CarComplectation.id == (
                        CarComplectation.select(CarComplectation.id).join(CarModel).where(
                            (
                                (CarModel.id == params['model']) &
                            (CarComplectation.engine == params['engine']) &
                            (complectation_condition) &
                                (CarComplectation.wired_state.is_null(True) | (CarComplectation.wired_state == 1))
                            )
                        )
                    ))
            )
        )

        result = await manager.count(query)

        return result
    @staticmethod
    async def sorted_integer_configs(query, current_table):
        ic(current_table)
        if current_table == CarYear:
            query = query.order_by(
                # Сортировка по числовой части строки в убывающем порядке
                fn.NULLIF(fn.REGEXP_REPLACE(current_table.name, '[^0-9].*$', ''), '').cast('integer').desc(),
                # Сортировка по полному имени в убывающем порядке
                current_table.name.desc()
            )
        else:
            query = query.order_by(
                fn.NULLIF(fn.REGEXP_REPLACE(current_table.name, '[^0-9].*$', ''), '').cast('integer'),
                current_table.name)
        return query

    @staticmethod
    async def add_brand(brand_name):
        brand, created = await database.get_or_create(CarBrand, name=brand_name)
        return brand





    @cache_redis.cache_update_decorator(model='car_config:branch')
    @staticmethod
    async def update_complectation_wired_state(complectation_id, color_id, new_state_id, old_state_id):
        async def run_update_query():
            def build_condition(field_name, value):
                """Возвращает часть SQL-запроса для условия и значение для параметра."""
                if value is None:
                    return f"{field_name} IS NULL", None
                else:
                    return f"{field_name} = %s", value

            conditions = []
            params = []
            last_args = []
            ic(color_id)
            ic()
            # ''''''
            # CarComplectation.update(wired_state_id=new_state_id).where(CarComplectation.id not in (
            #     CarComplectation.select(CarComplectation.id).where(единственная привязка к цвету) +? Где нет фотографий(надо будет удалить в конце, где удаляется комплектация)
            # ))
            # ''''''
            ic(str(new_state_id), str(old_state_id))
            if all(str(state_id) != '2' for state_id in (old_state_id, new_state_id)):
                print("UPDSTTE: all(str(state_id) != '2' for state_id in (old_state_id, new_state_id))")

                new_car_photo_base_query = '''
                UPDATE "Фотографии_Новых_Машин"
                SET car_complectation_id = (SELECT id FROM complectation_id)
                WHERE car_complectation_id = %s AND car_color_id = %s
                RETURNING car_complectation_id;
                '''
                last_args = [complectation_model.id, color_id]
            elif str(new_state_id) != '2':
                print("UPDSTTE: str(new_state_id) != '2'")
                new_car_photo_base_query = '''
                SELECT id FROM complectation_id
                '''
                # elif not color_id:
            elif str(new_state_id) == '2':
                print("UPDSTTE: str(new_state_id) == '2'")

                new_car_photo_base_query = '''
                DELETE FROM "Фотографии_Новых_Машин"
                where car_complectation_id = %s AND car_color_id = %s
                RETURNING car_complectation_id;
                '''
                last_args = [complectation_id, color_id]

            # Для каждого условия проверяем, является ли значение None и формируем условие
            fields_to_check = [
                ("carmodel.name", complectation_model.model.name),
                ("carengine._name", complectation_model.engine._name),
                ("carengine.name_uz", complectation_model.engine.name_uz),
                ("carengine.name_ru", complectation_model.engine.name_ru),
                ("carcomplectation._name", complectation_model._name),
                ("carcomplectation.name_uz", complectation_model.name_uz),
                ("carcomplectation.name_ru", complectation_model.name_ru),
                ("carcomplectation.wired_state_id", to_int(new_state_id))
            ]

            for field_name, value in fields_to_check:
                condition, param = build_condition(field_name, value)
                conditions.append(condition)
                if param is not None:  # Добавляем параметр, если он не None
                    params.extend([param])

            # Формирование основного запроса
            where_clause = " AND ".join(conditions)
            update_raw_query = f'''
            WITH existing_or_new_complectation AS (
                SELECT carcomplectation.id
                FROM carcomplectation
                JOIN carmodel ON carcomplectation.model_id = carmodel.id
                JOIN carbrand ON carmodel.brand_id = carbrand.id
                JOIN carengine ON carcomplectation.engine_id = carengine.id
                WHERE {where_clause}
                LIMIT 1
            ), inserted_complectation AS (
                INSERT INTO carcomplectation (model_id, engine_id, _name, name_uz, name_ru, wired_state_id)
                SELECT %s, %s, %s, %s, %s, %s
                WHERE NOT EXISTS (SELECT 1 FROM existing_or_new_complectation)
                RETURNING id
            ), complectation_id AS (
                SELECT id FROM existing_or_new_complectation
                UNION ALL
                SELECT id FROM inserted_complectation
            )
            {new_car_photo_base_query}
            
            '''

            # Добавляем оставшиеся параметры для INSERT и UPDATE частей
            params.extend([
                complectation_model.model.id, complectation_model.engine.id, complectation_model._name,
                complectation_model.name_uz, complectation_model.name_ru, to_int(new_state_id),
                *last_args
            ])
            ic()
            logging.debug(f'{update_raw_query}', *params)
            # Выполнение запроса с параметрами
            update_query = await execute_raw_sql(update_raw_query,
                                                 args=params,
                                                 transaction=True)
            ic(update_query)
            return update_query
        insert_complectation_subquery = ''
        update_query = None
        complectation_id, color_id, new_state_id = to_int(complectation_id), to_int(color_id), to_int(new_state_id)

        # ic(complectations_to_colors_wired)
        ic(complectation_id, color_id, new_state_id)

#         if complectations_to_colors_wired:
#             wired_colors = {photo_model.car_color.id for photo_model in complectations_to_colors_wired}
#             ic(wired_colors)
        if isinstance(complectation_id, CarComplectation):
            complectation_model = complectation_id
        else:
            complectation_model = await CarConfigs.get_by_id('complectation', complectation_id)
        ic(complectation_model)
        if complectation_model:
            update_query = await run_update_query()
            if not color_id:
                photo_branches = None

            elif complectation_model.wired_state != 2:
                photo_branches = list(await manager.execute(
                    NewCarPhotoBase.select(NewCarPhotoBase, CarColor).join(CarColor).where(NewCarPhotoBase.car_complectation == complectation_model)
                ))
            else:
                photo_branches = None
            ic(complectation_model.__data__['wired_state'])
            # ic(complectation_model.__dict__, update_query, complectation_model.wired_state == 2 and not update_query, complectation_model.wired_state, complectation_model.wired_state == 2, update_query, bool(update_query))
            # ic(photo_branches, update_query, complectation_model.wired_state, len({photo_model.car_color for photo_model in photo_branches}))
            if ((complectation_model.__data__['wired_state'] == 2 or not photo_branches)
                    and update_query):
                #or (photo_branches and len({photo_model.car_color if photo_model.car_color.id != color_id for photo_model in photo_branches}) == 1)) #(всего один цвет в привязке)
                await manager.execute(NewCarPhotoBase.delete().where(NewCarPhotoBase.car_complectation == complectation_model))
                await manager.execute(CarComplectation.delete().where(CarComplectation.id == complectation_model))
            elif complectation_model.__data__['wired_state'] == 2 and not update_query:
                return [(complectation_model.id,)]
        return update_query

    @cache_redis.cache_update_decorator(model='car_config:branch')
    @staticmethod
    async def custom_action(mode, action: str, name=None, model_id=None,
                            first_subject=None, second_subject=None, third_subject=None):
        result = None
        if isinstance(model_id, (list, set)):
            model_id = [int(id_element) for id_element in model_id]
        elif model_id and not isinstance(model_id, int):
            model_id = int(model_id)

        ic(name, mode, action, model_id, first_subject, second_subject, third_subject)
        if mode == 'color':
            current_table = CarColor
        elif mode == 'mileage':
            current_table = CarMileage
        elif mode == 'year':
            current_table = CarYear
        elif mode == 'brand':
            current_table = CarBrand
        elif mode == 'model':
            current_table = CarModel
        elif mode == 'complectation':
            current_table = CarComplectation
        else:
            return

        if not isinstance(model_id, int):
            default_condition = current_table.id.in_(model_id)
        else:
            default_condition = current_table.id == model_id
        ic(model_id)

        condition = current_table.name == name
        map_condition = {'name': name}
        if current_table in (CarComplectation, CarColor) and name:
            map_condition = await translate.translate(name, 'name', maybe_sorse_uz=True)
            if map_condition.get('_name'):
                condition = current_table._name == map_condition['_name']
                map_condition.update({'name_ru': None, 'name_uz': None})
            else:
                condition = current_table.name_uz == map_condition['name_uz'] and \
                            current_table.name_ru == map_condition['name_ru']
                map_condition.update({'_name': None})

            ic()
            ic(condition, map_condition)

        insert_kwargs = None
        if mode in ('color', 'complectation'):
            insert_kwargs = await translate.translate(name, 'name')
            ic(insert_kwargs)
        if not insert_kwargs:
            insert_kwargs = {'name': name}
        if first_subject and not second_subject:
            insert_kwargs['brand'] = first_subject
        elif all(subject for subject in (first_subject, second_subject)):
            insert_kwargs['model'] = first_subject
            insert_kwargs['engine'] = second_subject
            insert_kwargs['wired_state'] = third_subject
        ic(insert_kwargs)
        if not insert_kwargs:
            return '(translate_error)'

        match action:
            case 'get_by_name' if name:
                result = await manager.get_or_none(current_table, condition)

            case 'get_*':
                query = current_table.select()
                if current_table in (CarYear, CarMileage):
                    query = await CarConfigs.sorted_integer_configs(query, current_table)
                result = list(await manager.execute(query))

            case 'insert' if name:

                try:

                    result = await manager.create(current_table, **insert_kwargs)
                    # if result:
                    #     result = current_table
                except IntegrityError:
                    # traceback.print_exc()
                    return '(exists)'

            case 'delete' if model_id:
                if not mode in ('mileage', 'year'):
                    from database.data_requests.recomendations_request import RecommendationParametersBinder

                    await RecommendationParametersBinder.remove_wire_by_parameter(current_table, model_id)
                try:
                    result = await manager.execute(current_table.delete().where(default_condition))
                except:
                    return False

            case 'update' if name and model_id:
                try:
                    result = await manager.execute(current_table.update(**map_condition).where(default_condition))
                except:
                    return False
            case 'insert_or_get':
                ic(map_condition)
                result = await manager.get_or_create(current_table, **insert_kwargs)
                if result[1]:
                    result = (result[0], current_table)
                else:
                    result = result[0]

        if result and isinstance(result, list) and not current_table in (CarYear, CarMileage):
            if hasattr(result[0], 'name'):
                result = await sort_objects_alphabetically(result)

        return result


    @staticmethod
    async def get_by_id(table, model_id):
        if table == 'state':
            table = CarState
        elif table in ('engine_type', 'engine'):
            table = CarEngine
        elif table == 'brand':
            table = CarBrand
        elif table == 'model':
            table = CarModel
        elif table == 'complectation':
            table = CarComplectation
        elif table in ('year_of_release', 'year'):
            table = CarYear
        elif table == 'mileage':
            table = CarMileage
        elif table == 'color':
            table = CarColor
        else:
            table = None
        ic(table, model_id)
        if model_id and table:
            if isinstance(model_id, str):
                model_id = int(model_id)
            if isinstance(model_id, int):
                return await manager.get_or_none(table, table.id == model_id,)

    # @cache_redis.cache_decorator(model=CarColor)
    @staticmethod
    async def get_color_by_complectaiton(complectation_id, without_other=False):
        ic()
        ic(complectation_id)
        if isinstance(complectation_id, str):
            if '[' in complectation_id:
                complectation_id = eval(complectation_id)
            else:
                complectation_id = int(complectation_id)
        if not isinstance(complectation_id, list):
            complectation_id = [complectation_id]
        ic(complectation_id)
        # query = NewCarPhotoBase.select().join(CarComplectation).where(CarComplectation.id == complectation_id)
        query = CarColor.select().join(NewCarPhotoBase).join(CarComplectation).where(CarComplectation.id.in_(complectation_id)).distinct()
        result = list(await manager.execute(query))
        ic(result)
        ic()
        if result:
            if hasattr(result[0], 'name'):
                result = await sort_objects_alphabetically(result)

            result = await set_other_color_on_last_position(result, without_other=without_other)
            ic(result)



            return result
            # if without_other:
            #     ic(result)
            #     result.pop()
            #     ic(result)
            return result


    @cache_redis.cache_decorator(model=CarEngine)
    @staticmethod
    async def get_all_engines():
        result = list(await manager.execute(CarEngine.select()))
        if result:
            if hasattr(result[0], 'name'):
                result = await sort_objects_alphabetically(result)

        return result

    @cache_redis.cache_decorator(model=CarState)
    @staticmethod
    async def get_all_states():
        result = list(await manager.execute(CarState.select()))
        if result:
            if hasattr(result[0], 'name'):
                result = await sort_objects_alphabetically(result)

        return result

    @staticmethod
    async def get_or_add_color(name):
        try:
            color = None
            map_condition = await translate.translate(name, 'name')
            ic(map_condition)
            # color = await manager.get_or_none(CarColor, **map_condition)
            try:
                color = await manager.create_or_get(CarColor, **map_condition)
            except DoesNotExist:
                try:
                    await manager.create(CarColor, **map_condition)
                    color = await manager.get_or_none(CarColor, **map_condition)
                except IntegrityError:

                    ic()
                    for key, value in map_condition.items():
                        if value:
                            color = await manager.get_or_none(CarColor, **{key: value})
                            if color:
                                return color

            ic(color)
            if isinstance(color, tuple):
                color = color[0]
            ic(color)

            return color
        except:
            # return [await manager.get(CarColor, _name=name)]
            traceback.print_exc()
            pass

    @staticmethod
    async def update_color_or_complectation(mode, model_id, new_name):
        if isinstance(model_id, str):
            model_id = int(model_id)
        match mode:
            case 'complectation':
                table = CarComplectation
            case 'color':
                table = CarColor
            case _:
                return
        update_kwargs = await translate.translate(new_name, 'name')
        await manager.execute(table.update(**update_kwargs).where(table.id == model_id))
    @staticmethod
    async def bind_state_wire_conditions(conditions: List[bool], state: Optional[str], for_admin: bool,
                                         without_state: bool):
        ic(state)
        ic()
        if not without_state:
            if state:
                if for_admin:
                    condition_to_append = (CarComplectation.wired_state == to_int(state))
                else:
                    condition_to_append = (CarComplectation.wired_state == to_int(state)) | (
                        CarComplectation.wired_state.is_null(True))
            else:
                condition_to_append = CarComplectation.wired_state.is_null(True)

            conditions.append(condition_to_append)
        if len(conditions) > 1:
            combined_conditions = reduce(lambda a, b: a & b, conditions)
        elif len(conditions) == 1:
            combined_conditions = conditions[0]
        else:
            raise IndexError(f'len conditions = {len(conditions)}')
        return combined_conditions


    @cache_redis.cache_decorator(model=CarBrand)
    @staticmethod
    async def get_brands_by_engine_and_state(engine_id, state, for_admin=False, without_state=False):
        conditions = [CarEngine.id == to_int(engine_id)]
        ic(state)

        combined_conditions = await CarConfigs.bind_state_wire_conditions(conditions, state, for_admin, without_state)

        result = list(await manager.execute(CarBrand.select().join(CarModel).join(CarComplectation).join(CarEngine)
                                     .where(combined_conditions)))
        if result:
            if hasattr(result[0], 'name'):
                result = await sort_objects_alphabetically(result)

        return result

    # Функции для работы с Model
    @staticmethod
    async def add_model(brand_id, model_name):
        brand = await database.get(CarBrand, CarBrand.id == brand_id)
        model, created = await database.get_or_create(CarModel, brand=brand, name=model_name)
        return model

    @cache_redis.cache_decorator(model=CarModel)
    @staticmethod
    async def get_models_by_brand_and_engine_and_state(brand_id, state, engine_id=None, for_admin=False,
                                                       without_state=False):
        ic(brand_id, engine_id)
        conditions = [CarModel.brand_id == brand_id]
        if engine_id:
            conditions.append(CarEngine.id == engine_id)

        combined_conditions = await CarConfigs.bind_state_wire_conditions(conditions, state, for_admin, without_state)
        base_query = (CarModel.select(CarModel, CarComplectation, CarBrand, CarEngine).join(CarComplectation)
                      .join(CarEngine).switch(CarModel).join(CarBrand))

        result = list(await manager.execute(base_query.where(combined_conditions)))

        if result:
            if hasattr(result[0], 'name'):
                result = await sort_objects_alphabetically(result)
        ic()
        ic(result)
        return result

    @staticmethod
    async def add_complectation(model_id, complectation_name):
        model = await database.get(CarModel, CarModel.id == model_id)
        complectation, created = await database.get_or_create(CarComplectation, model=model, name=complectation_name)
        return complectation

    # @cache_redis.cache_decorator(model=CarComplectation)
    @staticmethod
    async def get_complectations_by_model_and_engine_and_state(model_id, state, engine_id=None, for_admin=False,
                                                               without_state=False, for_seller=False, name=None):
        conditions = [CarModel.id == model_id]
        if engine_id:
            conditions.append(CarEngine.id == engine_id)
        ic()
        base_query = (CarComplectation.select(CarComplectation, CarModel, CarBrand, CarEngine).join(CarModel)
                      .join(CarBrand).switch(CarComplectation).join(CarEngine))

        combined_conditions = await CarConfigs.bind_state_wire_conditions(conditions, state, for_admin, without_state)
        base_query = base_query.where(combined_conditions)
        if name:
            if name.get('_name'):
                complectation_condition = CarComplectation._name == name.get('_name')
            else:
                complectation_condition = ((CarComplectation.name_ru == name.get('name_ru')) & (CarComplectation.name_uz == name.get('name_uz')))

            result = await manager.count(base_query.where(complectation_condition))
            return result

        result = list(await manager.execute(base_query))
        ic(for_seller and result)
        ic(for_seller, result)
        if for_seller and result:
            good_result = []
            name_storage = dict()
            for result_element in result:
                element_name = result_element.name
                # element_id = result_element.id
                if element_name not in name_storage:
                    name_storage[element_name] = [result_element]
                else:
                    # repeated_element_id = name_storage[result_element]
                    name_storage[element_name].append(result_element)
            for name, models in name_storage.items():
                if len(models) > 1:
                    repeated_models = [model for model in result if model in models]
                    ic([repeated_model.id for repeated_model in repeated_models])
                    model = repeated_models[0]
                    model.id = [repeated_model.id for repeated_model in repeated_models]
                else:
                    model = models[0]
                good_result.append(model)
            ic(good_result, name_storage)
            result = good_result

        if result:
            if hasattr(result[0], 'name'):
                result = await sort_objects_alphabetically(result)

        return result

    # Функции для работы с Listing
    @staticmethod
    async def add_advert(user_id, data):
        seller = await manager.get(Seller, Seller.telegram_id == user_id)

        if seller:
            if data.get('color') and str(data.get('color')).isalpha():
                color_object = await CarConfigs.get_or_add_color(data.get('color'))
                ic(color_object)
                if color_object:
                    data['color'] = color_object[0].id

            ic(data, data['engine_type'])
            listing = await manager.create(CarAdvert, seller=seller.telegram_id, complectation=data['complectation'], sum_price=data['sum_price'], dollar_price=data['dollar_price'],
                                            state=data['state'], engine_type=data['engine_type'],
                                            color=data.get('color'), mileage=data.get('mileage'), year=data.get('year_of_release'))

            photo_album = data.get('photos')
            ic(listing)
            ic(listing.id)
            if listing and photo_album:
                if isinstance(photo_album, dict):
                    object_for_iteration = [photo_data for photo_data in photo_album.values()][0]
                else:
                    object_for_iteration = photo_album

                ic(object_for_iteration)
                structured_data = [{'car_id': listing.id, 'photo_id': photo_part['id'], 'photo_unique_id': photo_part['unique_id']} for photo_part in object_for_iteration]
                await manager.execute(AdvertPhotos.insert_many(structured_data))
                await advert_to_admin_view_related_requester.create_relation(listing.id)
            return listing



# Основная функция для демонстрации использования

async def insert_many(table, names):
    for name in names:
        if table == CarMileage:
            if '+' in name:
                head_symbol = '+'
                name = name.split(head_symbol)
                name = f'''{head_symbol.join([f"{int(name[0]):,}".replace(",", ".")])}+'''

            else:
                head_symbol = '-'

                name = name.split(head_symbol)
                name = head_symbol.join([f"{int(nam):,}".replace(",", ".") for nam in name])
        # elif table == CarColor:
        #     await manager.create(table, name=name)
        #     continue

        if table in (CarColor, CarEngine, CarState) and isinstance(name, tuple):
            insert_data = {}
            insert_data.update({'name_ru': name[0], 'name_uz': name[1]})
        else:
            insert_data = {'name': name}
        await manager.create(table, **insert_data)

async def insert_many_with_foregin(table, wire_to_name):
    for wire, names in wire_to_name.items():
        if table != CarComplectation:
            for name in names:
                if table == CarModel:
                    ic(table, wire, name)
                    await manager.create(table, name=name,
                                         brand=await manager.get(CarBrand.select().where(CarBrand.name == wire)))
        elif table == CarComplectation:
            if isinstance(names, list):
                for elem in names:
                    for engine_wire, real_name in elem.items():
                        ic()
                        ic(engine_wire, real_name, wire)
                        engine_wire = await translate.translate(engine_wire, 'name')

                        if isinstance(real_name, list) and len(real_name) > 1:
                            for nam in real_name:
                                ic()
                                ic(engine_wire, nam, wire)
                                await manager.create(table, name=nam,
                                                     model=await manager.get(CarModel.select().where(CarModel.name == wire)),
                                                     engine=await manager.get(CarEngine, **engine_wire))
                        else:
                            ic()
                            ic(engine_wire, real_name, wire)
                            await manager.create(table, name=real_name,
                                                 model=await manager.get(CarModel.select().where(CarModel.name == wire)),
                                                 engine=await manager.get(CarEngine, **engine_wire))

            elif isinstance(names, dict):
                for engine, comps in names.items():
                    engine_wire = await translate.translate(engine, 'name')
                    for comp in comps:
                        ic(wire, comp, engine, engine_wire)
                        await manager.create(table, name=comp,
                                             model=await manager.get(CarModel.select().where(CarModel.name == wire)),
                                             engine=await manager.get(CarEngine, **engine_wire))

async def mock_values(only_base_params):
    ''' V HEAD PARAMS V '''
    await insert_many(CarState, [('Новое', 'Yangi'), ('С пробегом', 'Ishlatilgan')])
    await insert_many(CarColor, [('Другой', 'Boshqa')])
    ''' ^ HEAD PARAMS ^ '''

    engine_names = [('Гибрид', 'Gibrid'), ('Электро', 'Elektro'), ('ДВС', 'IYD')]
    await insert_many(CarEngine, engine_names)
    await insert_many(CarColor, [
    ('Серый', 'Kulrang'),
    ('Чёрный', 'Qora'),
    ('Синий', "Ko\\'k"),
    ('Белый', 'Oq'),
    ('Жёлтый', 'Sariq'),
    ('Красный', 'Qizil'),
    ('Коричневый', 'Jigarrang'),
    ('Зелёный', 'Yashil'),
    ('Бордовый', 'Binafsha rang')
])

    await insert_many(CarYear,
                      ['2001-2007', '2004-2007', '2007-2010', '2010-2013', '2013-2016', '2016-2019', '2019-2020',
                       '2020-2021', '2021-2022', '2022-2023', '2023-2024'])
    await insert_many(CarMileage,
                      ['5000-10000', '10000-15000', '15000-20000', '20000-25000', '25000-30000', '30000-35000',
                       '35000-40000', '40000-45000', '45000-50000', '50000-75000', '75000-100000', '100000+'])

    if only_base_params:
        return

    brand_names = ['Сhevrolet', 'Li Xiang', 'Leapmotor', 'BYD', 'Mercedes', 'Audi', 'Ford', 'BMW', 'Renault', 'Jeep', 'Ferrari']
    await insert_many(CarBrand, brand_names)



    await insert_many_with_foregin(CarModel, {'BYD': ['SONG PLUS CHAMPION', 'CHAZOR'], 'Leapmotor': ['C11'], 'Li Xiang': ['L9', 'L7'], 'Сhevrolet': ['Gentra', 'Nexia 3'],

                                              'Mercedes': ['GLS', 'Metris', 'S-Class', 'EQS SUV', 'EQS Sedan'],
                                              'Audi': ['Q3', 'Q4 e-tron', 'Q5', 'A6', 'A8', 'S8', 'A7', 'S7', 'RS7'],
                                              'Ford': ['F-150', 'F-150 Lightning', 'Ford GT', 'Ford Maverick', 'Ford Mustang', 'Ford Mustang Mach-E'],
                                              'BMW': ['i3', 'iX', 'X1', 'X3', 'X4', 'X5', '8 Series'],
                                              'Renault': ['Megane E-Tech', 'Scenic E-Tech', '5', '4', 'Renault Twingo'],
                                              'Jeep': ['Grand Cherokee', 'Grand Cherokee L', 'Renegade', 'Wrangler', 'Wrangler'],
                                              'Ferrari': ['SF90 Stradale', 'F8 Tributo', 'Roma', 'Portofino M', '812 Superfast']})

    await insert_many_with_foregin(CarComplectation, {'CHAZOR': [{'Гибрид': 'XXX'}], 'SONG PLUS CHAMPION': [
        {'Электро': 'FLAGSHIP PLUS 605 km'}], 'C11': [{'Электро': ['Deluxe Edition 500 km (1)', 'Dual Motor 4WD 580 Km']}], 'L9': [
        {'Гибрид': 'L9 Max'}], 'L7': [{'Гибрид': 'L7 Pro'}], 'Gentra': [{'ДВС': '3'}], 'Nexia 3': [{'ДВС': '2'}],

            'GLS': {'Электро': ['Стандарт', 'Расширенный', 'Продвинутый']},
            'Metris': {'Гибрид': ['Эко', 'Премиум', 'Улучшенный']},
            'S-Class': {'ДВС': ['Базовая', 'Спортивная', 'Люкс']},
            'EQS SUV': {'Электро': ['Стандарт', 'Расширенный', 'Продвинутый']},
            'EQS Sedan': {'Гибрид': ['Эко', 'Премиум', 'Улучшенный']},

            'Q3': {'ДВС': ['Базовая', 'Спортивная', 'Люкс']},
            'Q4 e-tron': {'Гибрид': ['Эко', 'Премиум', 'Улучшенный']},
            'Q5': {'Гибрид': ['Эко', 'Премиум', 'Улучшенный']},
            'A6': {'ДВС': ['Базовая', 'Спортивная', 'Люкс']},
            'A8': {'ДВС': ['Базовая', 'Спортивная', 'Люкс']},
            'S8': {'Электро': ['Стандарт', 'Расширенный', 'Продвинутый']},
            'A7': {'Гибрид': ['Эко', 'Премиум', 'Улучшенный']},
            'S7': {'Гибрид': ['Эко', 'Премиум', 'Улучшенный']},
            'RS7': {'Электро': ['Стандарт', 'Расширенный', 'Продвинутый']},

            'F-150': {'Электро': ['Стандарт', 'Расширенный', 'Продвинутый']},
            'F-150 Lightning': {'ДВС': ['Базовая', 'Спортивная', 'Люкс']},
            'Ford GT': {'ДВС': ['Базовая', 'Спортивная', 'Люкс']},
            'Ford Maverick': {'Электро': ['Стандарт', 'Расширенный', 'Продвинутый']},
            'Ford Mustang': {'ДВС': ['Базовая', 'Спортивная', 'Люкс']},
            'Ford Mustang Mach-E': {'Электро': ['Стандарт', 'Расширенный', 'Продвинутый']},

            'i3': {'Гибрид': ['Эко', 'Премиум', 'Улучшенный']},
            'iX': {'Гибрид': ['Эко', 'Премиум', 'Улучшенный']},
            'X1': {'Гибрид': ['Эко', 'Премиум', 'Улучшенный']},
            'X3': {'Электро': ['Стандарт', 'Расширенный', 'Продвинутый']},
            'X4': {'Электро': ['Стандарт', 'Расширенный', 'Продвинутый']},
            'X5': {'ДВС': ['Базовая', 'Спортивная', 'Люкс']},
            '8 Series': {'ДВС': ['Базовая', 'Спортивная', 'Люкс']},

            'Megane E-Tech': {'Гибрид': ['Эко', 'Премиум', 'Улучшенный']},
            'Scenic E-Tech': {'Гибрид': ['Эко', 'Премиум', 'Улучшенный']},
            '5': {'Гибрид': ['Эко', 'Премиум', 'Улучшенный']},
            '4': {'ДВС': ['Базовая', 'Спортивная', 'Люкс']},
            'Renault Twingo': {'Электро': ['Стандарт', 'Расширенный', 'Продвинутый']},

            'Grand Cherokee': {'Электро': ['Стандарт', 'Расширенный', 'Продвинутый']},
            'Grand Cherokee L': {'Электро': ['Стандарт', 'Расширенный', 'Продвинутый']},
            'Renegade': {'Электро': ['Стандарт', 'Расширенный', 'Продвинутый']},
            'Wrangler': {'Гибрид': ['Эко', 'Премиум', 'Улучшенный']},

            'SF90 Stradale': {'Гибрид': ['Эко', 'Премиум', 'Улучшенный']},
            'F8 Tributo': {'Гибрид': ['Эко', 'Премиум', 'Улучшенный']},
            'Roma': {'ДВС': ['Базовая', 'Спортивная', 'Люкс']},
            'Portofino M': {'Гибрид': ['Эко', 'Премиум', 'Улучшенный']},
            '812 Superfast': {'Гибрид': ['Эко', 'Премиум', 'Улучшенный']}})





    # await database.create(CarColor)
    # await database.create(CarMileage)
    # await database.create(CarYear)
    pass
async def get_seller_account(mock_feedbacks=False):
    sellers = list(await manager.execute(Seller.select()))
    if sellers:
        return sellers
    await manager.create(User, telegram_id=902230076, username='Justion', name='Boris', surname='Борисов', phone_number='+79371567898')
    await manager.create(Admin, telegram_id=902230076)
    await manager.create(User, telegram_id=6306554751, username='JuJU', name='ReRe', surname='WWW', phone_number='+79333367898')


    justion = await manager.create(Seller, telegram_id=902230076, dealship_name='Борис Пром', entity='legal', dealship_address='Угол Борисова 45', authorized=True, phone_number='+79371567898')
    # mockseller = await manager.create(Seller, telegram_id=902330076, dealship_name='Мокнутый', entity='legal', dealship_address='Шпельм', authorized=True, phone_number='+79323567898')
    # mockselle2 = await manager.create(Seller, telegram_id=912330076, entity='natural', name='Мокнутый', surname='Частюк', patronymic=None, dealship_address=None, authorized=True, phone_number='+79323557898')
    sellers = list(await manager.execute(Seller.select()))
    if sellers:
        return sellers


async def mock_feedbacks(sellers, raw_cars):
    ic(sellers)
    if not sellers:
        sellers = list(await manager.execute(Seller.select()))
    if not list(await manager.execute(AdvertParameters.select().limit(1))):
        good_cars = []
        for car in raw_cars:
            good_cars.append({
                'complectation': car['complectation'],
                'color': car['color'],
            })
        # serialized_dicts = {json.dumps(d, sort_keys=True) for d in good_cars}
        unique_cars_tuples = {tuple(sorted(car.items())) for car in good_cars}

        # Преобразование обратно в список словарей
        good_cars = [dict(car_tuple) for car_tuple in unique_cars_tuples]
        # Десериализация обратно в словари
        # good_cars = [json.loads(d) for d in serialized_dicts]
        ic(len(good_cars))
        async with manager.atomic():
            # Вставка данных в AdvertParameters
            await manager.execute(AdvertParameters.insert_many(good_cars))

    async def worker(queue, manager):
        while True:
            batch = await queue.get()
            if batch is None:
                break
            await manager.execute(SellerFeedbacksHistory.insert_many(batch))
            queue.task_done()

    # Получение всех id для AdvertParameters
    advert_params_ids = [ap.id for ap in await manager.execute(AdvertParameters.select())]

    # Генерация данных для SellerFeedbacksHistory для каждого продавца
    queue = Queue(maxsize=10)
    workers = [asyncio.create_task(worker(queue, manager)) for _ in range(5)]  # Создание 5 рабочих

    # Добавление задач в очередь
    batch_size = 1000
    ic()
    for seller in sellers:
        for ap_id in advert_params_ids:
            batch = [{'seller_id': seller, 'advert_parameters': ap_id, 'feedback_time': datetime.now() - timedelta(days=random.randint(0, 365))} for _ in range(random.randint(2, 50))]
            await queue.put(batch)

    # Завершение работы рабочих
    for _ in workers:
        await queue.put(None)
    for worker in workers:
        await worker
        #
        #     # Вставка данных в SellerFeedbacksHistory
        # await manager.execute(SellerFeedbacksHistory.insert_many(feedbacks_history_data))


insert_data = []
insert_carars = []


async def get_car_adverts_by_brand_and_color(brand_id, color):
    return await manager.execute(CarAdvert.select().join(CarBrand).where(
        (CarAdvert.color == color) & (CarBrand.id == brand_id)
    ))



async def insert_advert_photos(new_car_photos, params):
    async def collect_data(brand_id, photos):
        async def iteration_on_adverts(advert, photos, iteration_counter = 0):
            for photo_id in photos:
                iteration_counter += 1
                advert_photo_data_list.append({
                    'car_id': advert.id,
                    'photo_id': photo_id,
                    'photo_unique_id': str(uuid.uuid4())
                })
                if advert.color.id != 1:
                    photo_base.append({
                        'admin_id': 902230076,
                        'car_complectation': advert.complectation.id,
                        'car_color': advert.color.id,
                        'photo_id': photo_id,
                        'photo_unique_id': f'{brand_id}_{uuid.uuid4()}'
                    })
            if iteration_counter < 5:
                await iteration_on_adverts(advert, photos,
                                           iteration_counter=iteration_counter)
        # Получаем все объявления для данного бренда
        # if params:
        #     current_table = AdvertParameters
        # else:
        current_table = CarAdvert
        matching_adverts = await manager.execute(
            current_table.select(current_table, CarComplectation, CarColor).join(CarColor).switch(current_table) \
                .join(CarComplectation).join(CarEngine).switch(CarComplectation).join(CarModel).join(CarBrand).where(
                CarBrand.id == int(brand_id))
        )
        ic(brand_id, len(matching_adverts))
        # Подготовка данных для массовой вставки
        tasks = [iteration_on_adverts(advert, photos) for advert in matching_adverts]
        await asyncio.gather(*tasks)

    # await manager.connect()
    try:
        advert_photo_data_list = []
        photo_base = []
        ic(insert_carars)
        tasks_two = [collect_data(brand_id, photos) for brand_id, photos in new_car_photos.items()]
        await asyncio.gather(*tasks_two)

        # Массовая вставка данных
        if advert_photo_data_list:
            # pass
            await manager.execute(AdvertPhotos.insert_many(advert_photo_data_list))
            print(f"Вставлено {len(advert_photo_data_list)} записей фотографий.")
        else:
            print("Нет данных для вставки")
        # return
        try:
            await PhotoRequester.load_photo_in_base(photo_base)
        except:
            traceback.print_exc()
            ic(photo_base)
            pass
    except Exception as e:
        traceback.print_exc()
        print(f"Ошибка при вставке данных: {e}")


async def get_complectations_by_brand(brand_id):
    # brand = await manager.get(CarBrand, CarBrand.id == brand_id)
    return await manager.execute(CarComplectation.select().join(CarModel).join(CarBrand).where(CarBrand.id == brand_id))

from icecream import ic
import uuid
async def add_photo(car_photos_info, car_info_list):
    try:
        photo_data_list = []
        ic(len(car_info_list))  # Выводим длину списка car_info_list
        counter = 0

        for brand_id, photos in car_photos_info.items():
            complectations = await get_complectations_by_brand(brand_id)
            ic(brand_id, len(complectations))  # Выводим brand_id и количество комплектаций

            for car_info in car_info_list:
                # Фильтруем комплектации, соответствующие данным в car_info
                filtered_complectations = [c for c in complectations if c.id == car_info['complectation']]
                for complectation in filtered_complectations:
                    counter += 1
                    for photo_path in photos:
                        photo_data = {
                            'car_complectation': complectation,
                            'car_color': car_info.get('color'),
                            'car_engine': complectation.engine,
                            'photo_id': photo_path,
                            'photo_unique_id': f"{brand_id}_{uuid.uuid4()}",
                            'admin_id': car_info.get('seller')
                        }
                        photo_data_list.append(photo_data)
                        if counter % 10000 == 0:
                            ic(photo_data)  # Выводим данные каждой фотографии
                            ic(len(photo_data_list))

        # Массовая вставка данных
        if photo_data_list:
            await manager.execute(NewCarPhotoBase.insert_many(photo_data_list))
            ic(len(photo_data_list))  # Выводим количество вставленных записей
        else:
            ic("Нет данных для вставки")
    except Exception as e:
        ic(e)  # Выводим исключение, если оно возникло

async def get_car(photos=None, cars=False):
    global insert_carars
    # await get_seller_account()
    if cars:
        await manager.create(CarAdvert, seller=902230076, complectation=1, state=1, dollar_price=56634, color=await manager.get(CarColor, CarColor.id == 2), mileage=None, year=None)
        await manager.create(CarAdvert, seller=902230076, complectation=2, state=1, dollar_price=45545, color=await manager.get(CarColor, CarColor.id == 2), mileage=None, year=None)
        await manager.create(CarAdvert, seller=902230076, complectation=3, state=1, sum_price=5556645, color=await manager.get(CarColor, CarColor.id == 2), mileage=None, year=None)
        await manager.create(CarAdvert, seller=902230076, complectation=4, state=1, dollar_price=75632, color=await manager.get(CarColor, CarColor.id == 2), mileage=None, year=None)
        await manager.create(CarAdvert, seller=902230076, complectation=5, state=1, sum_price=2312423, color=await manager.get(CarColor, CarColor.id == 2), mileage=None, year=None)
        await manager.create(CarAdvert, seller=902230076, complectation=6, state=1, sum_price=2322222, color=await manager.get(CarColor, CarColor.id == 2), mileage=None, year=None)
        await manager.create(CarAdvert, seller=902230076, complectation=7, state=1, dollar_price=1234223, color=await manager.get(CarColor, CarColor.id == 2), mileage=None, year= None)
        await manager.create(CarAdvert, seller=902230076, complectation=8, state=1, dollar_price=53458799, color=await manager.get(CarColor, CarColor.id == 1), mileage=None, year=None )
    car_id = 0
    complectations = [param.id for param in await manager.execute(CarComplectation.select(CarComplectation.id))]

    for index in complectations:
        for state_index in range(1, 3):
            for color_index in range(1, 10):
                if state_index == 1:
                    mileage, year = None, None
                    car_id += 1
                    # await CarConfigs.add_advert(902230076, )
                    insert_carars.append({'seller': 902230076, 'complectation': index, 'state': state_index,
                                         'dollar_price': random.randint(500000, 3800000),
                                         'color': color_index, 'mileage': mileage,
                                         'year': year})

                elif state_index == 2:
                    for mileage in range(1, 13):
                        for year in range(1, 8):
                            car_id += 1
                            # insert_photos.append({"car_id": car_id, 'photo_id': 1, 'photo_unique_id': 1})
                            insert_carars.append({'seller': 902230076, 'complectation': index, 'state': state_index,
                                                  'dollar_price': random.randint(500000, 3800000),
                                                  'color': color_index,
                                                  'mileage': mileage,
                                                  'year': year})

    if cars:
        # insert_carars = insert_carars[:len(insert_carars)//1000]
        await manager.execute(CarAdvert.insert_many(insert_carars))
    # await add_photo(photos, insert_carars)
    # if insert_data:
    #     insert_photo_query = AdvertPhotos.insert_many(insert_data)
    #     await manager.execute(insert_photo_query)

    # return
    ic(photos, insert_carars)
    if photos:
        await insert_advert_photos(photos, insert_carars)

    return insert_carars
