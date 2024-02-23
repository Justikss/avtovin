import asyncio
import functools
import importlib
import json
import logging
import traceback
from datetime import datetime, date
from typing import Union, Callable, Optional, Tuple

from aiogram.types import CallbackQuery, Message
from dateutil.parser import parse
from peewee import Model, DateTimeField, ForeignKeyField, DateField, DoesNotExist, ModelBase
from playhouse.shortcuts import model_to_dict
from redis import asyncio as aioredis

from config_data.config import TEST_MOMENT
from database.tables.car_configurations import CarAdvert, CarState, CarEngine, CarComplectation, CarModel, \
    CarBrand
from database.tables.offers_history import CacheBuyerOffers, ActiveOffers, RecommendedOffers


class RedisRequester:
    def __init__(self):
        self.pool = aioredis.ConnectionPool(
            host='localhost',
            decode_responses=True
        )
        self.redis_base = aioredis.StrictRedis(
            connection_pool=self.pool
        )
        self.scan_count = 300
        self.keys_storage = {
    'messages': (':last_user_message', ':last_message', ':last_seller_message',
                 '_notification', ':bot_header_message',
                 ':seller_media_group_messages', ':last_media_group'
    )
}



    async def _find_users_with_expired_keys(self, expired_mode=True):
        user_keys = {}
        user_id_to_message_id = {}
        for key_pattern in self.keys_storage['messages']:
            async for key in self._scan_keys(f'*{key_pattern}'):
                user_id = key.split(':')[0]
                if expired_mode:
                    ttl = await self.redis_base.ttl(key)
                    # ic(key, ttl)
                else:
                    ttl = -1
                if (ttl <= (60 * 30) and ttl not in (-1, -2)) or (not expired_mode):  # Меньше 40 минут и не истекший
                    value = await self.get_data(key=key, use_json=True)
                    if not isinstance(value, list):
                        value = [value]

                    user_keys.setdefault(user_id, []).append(key)
                    user_id_to_message_id.setdefault(user_id, []).extend(value)
        return user_keys, user_id_to_message_id

    async def _delete_keys_for_users_without_active_keys(self, users_with_expired_keys, user_id_to_message_id,
                                                         expired_mode=True):
        users_to_cleaning = []
        messages_to_delete = dict()
        for user_id, keys in users_with_expired_keys.items():
            # if await self._has_active_keys(user_id) and expired_mode:
            #     continue
            for key in keys:
                await self.redis_base.delete(key)
            users_to_cleaning.append(user_id)
            messages_to_delete[user_id] = user_id_to_message_id[user_id]
        ic(messages_to_delete)
        return messages_to_delete

    async def _scan_keys(self, pattern):
        cursor = 0
        while True:
            cursor, keys = await self.redis_base.scan(cursor, match=pattern, count=100)
            for key in keys:
                yield key
            if cursor == 0:
                break

    async def scan_list_of_keys(self, patterns):
        async def gather_keys(pattern):
            return [key async for key in self._scan_keys(pattern)]

        if isinstance(patterns, list):
            # Использование gather_keys для создания списка задач
            tasks = [gather_keys(pattern) for pattern in patterns]
            results = await asyncio.gather(*tasks)
            ic(results)
            # Объединение результатов из разных паттернов
            return [key for result in results for key in result]
        else:
            # Сбор ключей для одиночного паттерна и возврат как списка
            return await gather_keys(patterns)
    async def _has_active_keys(self, user_id):
        async for key in self._scan_keys(f'{user_id}:*'):
            ttl = await self.redis_base.ttl(key)

            if 0 <= ttl >= 1800:  # Еще активный или без ttl

                return True


        return False
    async def getset_data(self, key, value):
        try:
            if type(value) not in (int, float, str):
                value = value
                value = json.dumps(value)

            await self.redis_base.getset(key, value)
            value_is_set = await self.redis_base.get(key) == value
            if value_is_set:
                # print('good', {key: value})
                return True
            else:
#                 print('error', {key: value})
                return False
        except ConnectionError as ex:
            # traceback.print_exc()
            await asyncio.sleep(1)
            await redis_data.getset_data(key, value)


    async def set_data(self, key: str = None,
                       value: Union[set, list, str, float, dict] = None,
                       dicted_data: dict = None, expire=None) -> bool:

        expire = await self.set_ttl(key, expire)
        try:
            if dicted_data:
                for key, value in dicted_data.items():
                    if type(value) not in (int, float, str):
                        value = await value
                        value = json.dumps(value)

                    await self.redis_base.set(key, value)
                    value_is_set = await self.redis_base.get(key) == value
                    if value_is_set:
                        print('rodis good', {key: value})
                        if expire:
                            await self.redis_base.expire(key, expire)
                        pass
                    else:
                        print('rodis error', {key: value})
                        return False


            else:
                if type(value) not in (int, float, str):
                    value = json.dumps(value)
                #выдаёт false если числовое value(становится стр)
                await self.redis_base.set(key, value)

                if isinstance(value, int):
                    value_is_set = await self.redis_base.get(key) == str(value)
                else:
                    value_is_set = await self.redis_base.get(key) == value
                if value_is_set:
                    print('rodis good', {key: value})
                    if expire:
                        await self.redis_base.expire(key, expire)
                    return True
                else:
                    print('rodis error', {key: value})
                    return False
        except ConnectionError as ex:
            # traceback.print_exc()
            await asyncio.sleep(1)
            return await redis_data.set_data(key, value, dicted_data, expire)

    async def get_data(self, key: str, use_json=False) -> Union[bool, Union[set, list, str, float, dict]]:
        try:
            result = await self.redis_base.get(key)
            # print('redisult-get type', type(result))
            ic(result)
            ic()
            if use_json and result:
                result = json.loads(result)

            if result:
                print('rodis good_get', {key: result})
                return result
            else:
                print('rodis error_get', key)
                return False
        except ConnectionError as ex:
#             traceback.print_exc()
            await asyncio.sleep(1)
            return await redis_data.get_data(key, use_json)

    async def delete_key(self, key: str):
        try:
            # Удаляем ключ
            result = await self.redis_base.delete(key)
            if result == 1:
                print(f"rodis Ключ '{key}' успешно удален")
                return True
            else:
                print(f"rodis Ключ '{key}' не найден")
                return False

        except ConnectionError as ex:
            # traceback.print_exc()
            await asyncio.sleep(1)
            await redis_data.delete_key(key)

    async def set_ttl(self, key, expire):
        if not expire:
            ic(any(sub_key in key for sub_key in self.keys_storage['messages']))
            if any(sub_key in key for sub_key in self.keys_storage['messages']):
                expire = 48 * 60 * 60 - 60
                return expire



redis_data = RedisRequester()
offers_history_module = importlib.import_module('database.tables.offers_history')


class RedisForCache:
    def __init__(self):
        self.redis_base = redis_data.redis_base
        self.threshold = 2 if not TEST_MOMENT else -1
        self.counter_ttl = 120
        self.top_count_ttl = 60 * 60 * 24 * 5
        self.keys_relate = {
            CarAdvert: ('car_advert_requests:get_where_id')
        }

    async def construct_cache_key(self, method, id_value, *args, **kwargs):
        # Создание ключа из имени метода
        ic(args, kwargs)

        if id_value in (CarBrand, CarModel, CarComplectation):
            if 'state' in kwargs:
                state_id = kwargs.get('state')
            else:
                if len(args) >= 2:
                    state_id = args[1]
                else:
                    raise IndexError(f'State param not found\nargs: {args}\nkwargs: {kwargs}')
            key_parts = [f'cached_car_config:{id_value}{state_id}']
            key_parts.extend(str(arg) for arg in args)

        else:
            module_name = method.__module__.split('.')[-1]
            key_parts = [module_name, method.__name__]
            # Добавление позиционных аргументов
            if id_value:
                key_parts.append(str(id_value))
            else:
                key_parts.extend(str(arg) for arg in args)

            # Добавление именованных аргументов
            for kwarg_name, value in sorted(kwargs.items()):
                ic(kwarg_name, value)
                key_parts.append(f"{kwarg_name}:{value}")

        # Соединение частей ключа с разделителем
        ic(key_parts)
        result = ":".join(key_parts)
        return result

    async def extract_id_arg(self, id_key, model=None, *args, **kwargs):
        async def get_table_by_string(table_name):
            ic(table_name)
            table = None
            match table_name:
                case 'brand':
                    table = CarBrand
                case 'model':
                    table = CarModel
                case 'complectation':
                    table = CarComplectation

            return table
        id_value = None
        buyer_id = None
        ic(id_key, model)
        if model in ('model', 'brand', 'complectation'):
            id_value = await get_table_by_string(model)
            ic()
            ic(id_value)
            return id_value, None
        if id_key:
            # ic(any(param in kwargs.keys() for param in ('count', 'get_brands')))
            # if ((model in (RecommendedOffers, CacheBuyerOffers, ActiveOffers) and 'count' in kwargs.keys())

            kwarg_name = id_key.split(':')[1]
            arg_index = id_key.split(':')[0]
            id_value = kwargs.get(kwarg_name)
            if (not id_value) and (0 <= int(arg_index) < len(args)):
                id_value = args[int(arg_index)]

            if model in (RecommendedOffers, CacheBuyerOffers, ActiveOffers):
                buyer_id = id_value
                id_value = None
        if model in (CarBrand, CarModel, CarComplectation):
            buyer_id = id_value
            id_value = model
        if id_value in ('model', 'brand', 'complectation'):
            id_value = await get_table_by_string(id_value)
            ic()
            ic(id_value)
            return id_value, None
        return id_value, buyer_id

    # def car_advert_search_decorator(self):
    #     def wrapped_decorator(func)
    #         @functools.wraps(func)
    #         async def wrapper(*args, **kwargs):

    def cache_decorator(self, model, id_key: Optional[str] = None):
        def wrapped_decorator(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                id_value, buyer_id = await self.extract_id_arg(id_key, model, *args, **kwargs)
                ic(id_value)
                command = await self.construct_cache_key(func, id_value, *args, **kwargs)

                result = await redis_data.get_data(command)
                ic()
                ic(result)
                if not result:
                    logging.debug('REDIS without cache\n by command: %s', command)

                    result = await func(*args, **kwargs)
                    ic()
                    ic(result)
                    ic(id_value)
                    id_value = await self.insert_result_in_id_value_if_need(result, id_value, buyer_id)
                    ic(id_value)
                    ic(type(id_value))
                    if (isinstance(id_value, (list, str, int, ModelBase))
                            or buyer_id):
                        await self.update_usage_stats_and_cache(command, id_value, result, model, buyer_id)

                    else:
                        logging.error('REDIS without command\nid_value: %s', str(id_value))


                else:
                    ic(result)
                    ic(command)
                    result = await self.async_deserialize_from_json(model, result)
                    logging.debug('REDIS got %s\n by command: %s', str(result), command)
                ic(result)
                return result
            return wrapper
        return wrapped_decorator

    async def update_all_config_branch(self):
        key_pattern = 'cached_car_config*'
        keys_to_delete = [key async for key in redis_data._scan_keys(key_pattern)]
        if keys_to_delete:
            await self.redis_base.delete(*keys_to_delete)

    def cache_update_decorator(self, model: Model | Tuple[Model], id_key: Optional[str] = None,
                               mode: Optional[str] = None, action=None, second_id_key=None):
        def wrapped_decorator(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                # Выполнение основной функции
                ic(args, kwargs)
                result = await func(*args, **kwargs)
                ic(result)
                if result:
                    if model == 'car_config:branch':
                        await self.update_all_config_branch()
                        return result

                    car_config_update_case = model == 'car_config' and any(argument in massive for massive in (args, kwargs.values())
                                                     for argument in ('insert_or_get', 'insert', 'delete', 'update'))
                    if model == 'car_config' and not any(argument in massive for massive in (args, kwargs.values())
                                                     for argument in ('insert_or_get', 'insert', 'delete', 'update')):
                        return result
                    else:
                        ic(model == 'car_config' and not any(argument in massive for massive in (args, kwargs.values())
                                                     for argument in ('insert_or_get', 'insert', 'delete', 'update')))
                        ic(model, args, kwargs.values())
                    ic(model)
                    if isinstance(model, str) and model == 'car_config':
                        models, buyer_id = await self.extract_id_arg(second_id_key, *args, **kwargs)
                        ic()
                        ic(models)
                        models = (models,)
                    elif not isinstance(model, tuple):
                        models = (model,)
                    else:
                        models = model
                    ic(models)
                    for model_element in models:
                        if model != 'car_config':
                            ic()
                            id_value, buyer_id = await self.extract_id_arg(id_key, model_element, *args, **kwargs)
                        else:
                            ic()
                            id_value, buyer_id = model_element, None
                        ic(id_value)
                        ic(action, model, buyer_id)

                        ic()
                        ic(id_value)
                        id_value = await self.insert_result_in_id_value_if_need(result, id_value, None, model_element if model == 'car_config' else None)
                        related_keys = None
                        ic()
                        ic(id_value)
                        ic(id_value, model_element, type(model_element), offers_history_module.RecommendedOffers, mode)
                        if mode == 'by_scan':
                            raw_patterns = []
                            if model_element is offers_history_module.RecommendedOffers:
                                raw_patterns = ['recomendations_request:retrieve_by_buyer_id:buyer_id:',
                                                'recomendations_request:retrieve_by_buyer_id:']
                                ic()
                            elif model_element is CacheBuyerOffers:
                                raw_patterns = ['offers_requests:get_cache:',
                                                'offers_requests:get_cache:buyer_id:']
                            elif model_element is ActiveOffers:
                                raw_patterns = ['offers_requests:get_for_buyer_id:',
                                                'offers_requests:get_for_buyer_id:buyer_id:']
                            else:
                                logging.error('REDIS model: %s\n Does not found his key-scan patterns', str(model_element))
                                ic(hash(model_element), hash(offers_history_module.RecommendedOffers))

                            if isinstance(id_value, list) and raw_patterns:
                                patterns = [f'{raw_pattern}*{id_element}*' for raw_pattern in raw_patterns
                                                                          for id_element in id_value]
                                patterns.extend([])
                                ic(patterns)
                                related_keys = await redis_data.scan_list_of_keys(patterns)
                                ic(related_keys)

                        elif model_element is CarAdvert and str(id_value).isdigit():
                            related_keys = await redis_data.scan_list_of_keys(f'car_advert_requests:get_where_id:*{id_value}*')
                        if car_config_update_case:
                            ic()
                            related_keys = await redis_data.scan_list_of_keys(
                                [f'cached_car_config:*{str(model_element)}:*']
                            )
                        if not related_keys:
                            '''Забыл что конкретно обрабатывает эта строка'''
                            ic()
                            related_keys = await self.get_related_keys(model_element, id_value, *args, **kwargs)
                        if related_keys:
                            ic(await self.redis_base.delete(*related_keys))
                            logging.debug('REDIS UPDATE delete: %s \n   by id: %s\nand related_keys: %s',
                                          str(related_keys), id_value, str(related_keys))
                        else:
                            logging.debug('REDIS UPDATE UNSUCCESS:\nwithout related keys\nby %s', id_value)

                return result
            return wrapper
        return wrapped_decorator

    async def update_cache_transactionally(self, related_keys, action: str):
        async with redis_data.redis_base.pipeline() as pipe:
            for key in related_keys:
                value = await redis_data.get_data(key, use_json=True)
                if isinstance(value, (str, int, float, bool)):
                    # if value == False:
                    await pipe.delete(key)

            # await pipe.set(key_to_set, new_value)
            await pipe.execute()

    async def insert_result_in_id_value_if_need(self, result, id_value, buyer_id, model_element = None):
        if model_element:
            return model_element
        if not id_value and not buyer_id:
            id_value = []
            if result:
                # ic(result, result[0].id)
                if not isinstance(result, list):
                    result = [result]
                for result_part in result:
                    if isinstance(result_part, Model):
                        result_part = result_part.id
                    id_value.append(result_part)
                # else:
                #     id_value = [result]
            logging.debug('REDIS new raw id_value from result: %s\nnew_Id_value: %s', result, str(id_value))

        return id_value

    async def update_usage_stats_and_cache(self, command, id_value, result, model, buyer_id):
        count_command = f'{command}:count:'
        count = await self.redis_base.get(count_command)
        ic(count_command)
        # logging.debug(f'REDIS count command: %s', count_command)
        if not count:
            await redis_data.set_data(count_command, 1, expire=self.counter_ttl)
        else:
            count = int(count)
            if count < self.threshold:
                await self.redis_base.incr(count_command)
            else:
                logging.debug('REDIS set %s\nby command: %s', str(result), command)
                result = await self.async_serialize_to_json(result)
                await self.redis_base.set(command, result)
                await self.update_related_keys(command, id_value if not buyer_id else buyer_id, model)
                # Сбросить счетчик после достижения порога
                # await self.redis_base.delete(count_command)
                await redis_data.set_data(count_command, count, expire=self.top_count_ttl)


    async def update_related_keys(self, main_key, id_value, model):
        if model in (CarState, CarEngine, offers_history_module.RecommendedOffers):
            return
        # main_key = ':'.join(main_key.split(':')[:2])
        exists_keys = await self.get_related_keys(model, id_value)
        if main_key not in exists_keys:
            if id_value:
                exists_keys.append(main_key)
                head_relate_key = f"related:{model}" + f':{id_value}'
                await redis_data.set_data(head_relate_key,
                                          exists_keys)
                logging.debug('REDIS new related_keys = %s\n    by id: %s\n    by key: %s', str(exists_keys), id_value,
                              head_relate_key)
            else:
                logging.debug('REDIS new related keys: UNSUCCESS\nNot id_value')

    async def get_related_keys(self, model, id_value, *args, **kwargs):
        if not id_value:
            return []
        # Получение списка связанных ключей
        if isinstance(id_value, (list, tuple, set)):
            keys = []
            for id_element in id_value:
                new_keys = await self.get_related_keys(model, id_element)
                if new_keys:
                    keys.extend(new_keys)
        if isinstance(id_value, Model):
            id_value = id_value.id
        head_relate_key = f"related:{model}" + f':{id_value}' if id_value else ''
        keys = await redis_data.get_data(head_relate_key, use_json=True)

        if not keys:
            keys = []
            logging.debug('REDIS unsuccess try get related keys = %s\n    by id: %s\n    by relate_key: %s', str(keys),
                          id_value, head_relate_key)
        else:
            logging.debug('REDIS related_keys = %s\n    by id: %s\n    by relate_key: %s', str(keys),
                          id_value, head_relate_key)

        return keys

    async def async_deserialize_from_json(self, model_class, json_string):
        ic(model_class)
        ic(json_string)
        data = json.loads(json_string)
        ic(data)
        return await self._async_deserialize_model(model_class, data)

    async def async_serialize_to_json(self, model_instance):
        ic(model_instance)
        serialized_data = await self._async_serialize_model(model_instance)
        ic(serialized_data)
        # if isinstance(serialized_data.)
        return json.dumps(serialized_data)

    async def _async_serialize_model(self, model_instance):
        if isinstance(model_instance, list):
            tasks = [self._async_serialize_model(model) for model in model_instance]
            result = await asyncio.gather(*tasks)
            return result

        if not isinstance(model_instance, Model):
            return model_instance

        model_dict = {}

        # Обработка полей модели
        for field_name in model_instance._meta.sorted_field_names:
            field = model_instance._meta.fields[field_name]
            # ic(model_instance, field_name)
            try:
                has_attribute = hasattr(model_instance, field_name)
            except DoesNotExist:
                has_attribute = False
            if not has_attribute:
                field_name = f'{field_name}_id'
            value = getattr(model_instance, field_name)

            if isinstance(field, ForeignKeyField):
                # Рекурсивная обработка внешних ключей
                related_object = getattr(model_instance, field_name)
                model_dict[field_name] = await self._async_serialize_model(related_object)
            elif isinstance(value, (datetime, date)):
                # Конвертация datetime в строку
                model_dict[field_name] = value.isoformat()
            else:
                model_dict[field_name] = value

        return model_dict

    async def _async_deserialize_model(self, model_class, data):
        # Создаем экземпляр модели
        if isinstance(data, list):
            tasks = [self._async_deserialize_model(model_class, data_element) for data_element in data]
            result = await asyncio.gather(*tasks)
            return result
        elif isinstance(data, (str, int, float, bool)):
            return data
        model_instance = model_class()

        for field_name, field_value in data.items():
            # ic(field_name)
            field = model_class._meta.fields.get(field_name)
            # if not field:
            #     field = model_class._meta.fields.get(f'{field_name}_id')

            # ic(type(field))
            if isinstance(field_value, dict):
                related_class = field.rel_model
                nested_instance = await self._async_deserialize_model(related_class, field_value)
                setattr(model_instance, field_name, nested_instance)
            elif isinstance(field, (DateTimeField, DateField)) and isinstance(field_value, str):
                # Преобразование строки в datetime или date
                parsed_date = parse(field_value)
                setattr(model_instance, field_name, parsed_date.date() if isinstance(field, DateField) else parsed_date)
            else:
                setattr(model_instance, field_name, field_value)

        return model_instance

cache_redis = RedisForCache()


class RedisCacheUserStatus:
    def __init__(self):
        self.cache_redis = cache_redis

    def user_status_cache_update_decorator(self, model):
        def wrapped_decorator(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                result = await func(*args, **kwargs)

                user_id = await self.get_telegram_id(*args, **kwargs)
                if not user_id or not str(user_id).isdigit():
                    logging.error('REDIS user update status: telegram id not found in args-kwargs: %s %s', str(args), str(kwargs))
                    return

                match model:
                    case 'ban':
                        user_state = await self.get_user_state_from_arguments(*args, **kwargs)
                        redis_key = f'user_ban:{user_state}:{user_id}'
                    case _:
                        logging.error('REDIS user update status: model kwarg not implemented')
                        return
                if user_state:
                    await redis_data.delete_key(redis_key)
                    logging.debug('REDIS user update status: success delete key: %s', redis_key)
                else:
                    logging.debug('REDIS user update status: user state not found by args-kwargs: %s, %s', args, kwargs)
                return result
            return wrapper
        return wrapped_decorator

    def user_status_cache_decorator(self, model):
        def wrapped_decorator(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                user_id = await self.get_telegram_id(*args, **kwargs)
                if not user_id or not str(user_id).isdigit():
                    logging.error('REDIS user status: telegram id not found in args-kwargs: %s %s, user_id = %s',
                                     str(args), str(kwargs), user_id)
                    return

                match model:
                    case 'ban':
                        user_state = await self.get_user_state_from_arguments(*args, **kwargs)
                        redis_key = f'user_ban:{user_state}:{user_id}'

                    case _:
                        logging.error('REDIS user status: model kwarg not implemented')
                        return

                result = await redis_data.get_data(redis_key)
                ic(result, result is False)
                if not result:
                    logging.debug('REDIS user status: func result not been cached by key: %s', redis_key)
                    result = await func(*args, **kwargs)
                    if user_state:
                        await redis_data.set_data(redis_key, result)
                        logging.debug('REDIS user status: set new result by key: %s and value: %s',
                                         redis_key, result)
                    else:
                        logging.debug('REDIS user status: user state not found by args-kwargs: %s, %s',
                                      args,
                                      kwargs)

                else:
                    logging.debug('REDIS user status: result from redis: %s, by key: %s', str(result), redis_key)

                return result
            return wrapper
        return wrapped_decorator

    async def get_user_state_from_arguments(self, *args, **kwargs):
        user_state = ''
        for key in ('seller', 'user'):
            is_user_state = kwargs.get(key)
            if is_user_state:
                user_state = key
                break

        return user_state
    async def get_telegram_id(self, *args, **kwargs):
        user_id = kwargs.get('telegram_id')
        if not user_id:
            user_id = kwargs.get('user_id')
            if not user_id:
                for arg in args:
                    if str(arg).isdigit():
                        user_id = arg
        return user_id
cache_user_status = RedisCacheUserStatus()

