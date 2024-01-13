import asyncio
import random
import traceback
from asyncio import Queue
from collections import defaultdict
from datetime import timedelta, datetime

from peewee import JOIN, IntegrityError, fn

from database.data_requests.new_car_photo_requests import PhotoRequester
from database.data_requests.recomendations_request import RecommendationParametersBinder
from database.data_requests.statistic_requests.adverts_to_admin_view_status import \
    advert_to_admin_view_related_requester
from database.data_requests.utils.set_color_1_in_last_position import set_other_color_on_last_position
from database.db_connect import database, manager
from database.tables.admin import Admin

from database.tables.car_configurations import (CarBrand, CarModel, CarComplectation, CarState,
                                                CarEngine, CarColor, CarMileage, CarAdvert, CarYear)
from database.tables.commodity import AdvertPhotos, NewCarPhotoBase
from database.tables.offers_history import SellerFeedbacksHistory
from database.tables.seller import Seller
from database.tables.statistic_tables.advert_parameters import AdvertParameters
from database.tables.user import User


class CarConfigs:
    @staticmethod
    async def sorted_integer_configs(query, current_table):
        query = query.order_by(
            fn.NULLIF(fn.REGEXP_REPLACE(current_table.name, '[^0-9].*$', ''), '').cast('integer'),
            current_table.name)
        return query

    @staticmethod
    async def add_brand(brand_name):
        brand, created = await database.get_or_create(CarBrand, name=brand_name)
        return brand

    @staticmethod
    async def custom_action(mode, action: str, name=None, model_id=None,
                            first_subject=None, second_subject=None):
        if isinstance(model_id, (list, set)):
            model_id = [int(id_element) for id_element in model_id]
        elif model_id and not isinstance(model_id, int):
            model_id = int(model_id)

        ic(name, mode, action, model_id)
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
        # elif mode == 'state':
        #     current_table = CarState
        else:
            return

        if not isinstance(model_id, int):
            default_condition = current_table.id.in_(model_id)
        else:
            default_condition = current_table.id == model_id
        ic(model_id)
        match action:
            case 'get_by_name' if name:
                result = await manager.get_or_none(current_table, current_table.name == name)

            case 'get_*':
                query = current_table.select()
                if current_table in (CarYear, CarMileage):
                    query = await CarConfigs.sorted_integer_configs(query, current_table)
                result = list(query)

            case 'insert' if name:
                insert_kwargs = {'name': name}
                try:
                    if first_subject and not second_subject:
                      insert_kwargs['brand'] = first_subject
                    elif all(subject for subject in (first_subject ,second_subject)):
                        insert_kwargs['model'] = first_subject
                        insert_kwargs['engine'] = second_subject
                    result = await manager.create(current_table, **insert_kwargs)
                except IntegrityError:
                    return '(exists)'

            case 'delete' if model_id:
                if not mode in ('mileage', 'year'):
                    await RecommendationParametersBinder.remove_wire_by_parameter(current_table, model_id)
                result = await manager.execute(current_table.delete().where(default_condition))

            case 'update' if name and model_id:
                result = await manager.execute(current_table.update(name=name).where(default_condition))
        ic(result)
        return result

    # @staticmethod
    # async def delete_new_car_state_params(mode, model_id, binded_params: dict):
    #     if mode == 'brand':


        #удалить и с фото базы

    # @staticmethod
    # async def get_colors_by_name(color_name):
    #     color_models = list(await manager.execute(CarColor.select().where(CarColor.name == color_name)))
    #     return color_models

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
            return await manager.get_or_none(table, table.id == model_id)

    @staticmethod
    async def get_color_by_complectaiton(complectation_id, without_other=False):
        if not isinstance(complectation_id, int):
            complectation_id = int(complectation_id)
        ic(complectation_id)
        # query = NewCarPhotoBase.select().join(CarComplectation).where(CarComplectation.id == complectation_id)
        query = CarColor.select().join(NewCarPhotoBase).join(CarComplectation).where(CarComplectation.id == complectation_id).distinct()
        result = list(await manager.execute(query))
        ic(result)
        ic()
        if result:
            result = await set_other_color_on_last_position(result, without_other=without_other)
            ic(result)
            # if without_other:
            #     ic(result)
            #     result.pop()
            #     ic(result)
            return result


    # @staticmethod
    # async def get_characteristic(year=False, color=False, mileage=False):
    #     if year:
    #         current_table = CarYear
    #     elif color:
    #         current_table = CarColor
    #     elif mileage:
    #         current_table = CarMileage
    #     else:
    #         current_table = None
    #
    #     if current_table:
    #         return await manager.execute(current_table.select())


    @staticmethod
    async def get_all_engines():
        return await manager.execute(CarEngine.select())

    @staticmethod
    async def get_all_states():
        return await manager.execute(CarState.select())


    @staticmethod
    async def get_or_add_color(name):
        try:
            return await manager.get_or_create(CarColor, name=name)
        except:
            pass

    @staticmethod
    async def get_brands_by_engine(engine_id):
        return await manager.execute(CarBrand.select().join(CarModel).join(CarComplectation).join(CarEngine)
                                     .where(CarEngine.id == int(engine_id)))

    # Функции для работы с Model
    @staticmethod
    async def add_model(brand_id, model_name):
        brand = await database.get(CarBrand, CarBrand.id == brand_id)
        model, created = await database.get_or_create(CarModel, brand=brand, name=model_name)
        return model

    @staticmethod
    async def get_models_by_brand_and_engine(brand_id, engine_id=None):
        ic(brand_id, engine_id)
        if engine_id:
            return list(await manager.execute(CarModel.select().join(CarComplectation).join(CarEngine).where((CarEngine.id == engine_id) & (CarModel.brand_id == brand_id))))
        else:
            return list(await manager.execute(CarModel.select().join(CarComplectation).where(CarModel.brand_id == brand_id)))


    @staticmethod
    async def add_complectation(model_id, complectation_name):
        model = await database.get(CarModel, CarModel.id == model_id)
        complectation, created = await database.get_or_create(CarComplectation, model=model, name=complectation_name)
        return complectation

    @staticmethod
    async def get_complectations_by_model_and_engine(model_id, engine_id=None):
        if engine_id:
            return list(await manager.execute(CarComplectation.select().join(CarModel).switch(CarComplectation).join(CarEngine).where((CarModel.id == model_id) & (CarEngine.id == engine_id))))
        else:
            return list(await manager.execute(CarComplectation.select().join(CarModel).switch(CarComplectation).where((CarModel.id == model_id))))
    # Функции для работы с User
    @staticmethod
    async def add_user(username, role):
        user, created = await database.get_or_create(User, username=username, role=role)
        return user

    @staticmethod
    async def get_all_users():
        return await manager.execute(User.select())

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
        elif table == CarColor:
            await manager.create(table, name=name)
            continue

        await manager.create(table, name=name)

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
                        if isinstance(real_name, list) and len(real_name) > 1:
                            for nam in real_name:
                                ic()
                                ic(engine_wire, nam, wire)
                                await manager.create(table, name=nam,
                                                     model=await manager.get(CarModel.select().where(CarModel.name == wire)),
                                                     engine=await manager.get(CarEngine.select().where(CarEngine.name == engine_wire)))
                        else:
                            ic()
                            ic(engine_wire, real_name, wire)
                            await manager.create(table, name=real_name,
                                                 model=await manager.get(CarModel.select().where(CarModel.name == wire)),
                                                 engine=await manager.get(
                                                     CarEngine.select().where(CarEngine.name == engine_wire)))

            elif isinstance(names, dict):
                for engine, comps in names.items():
                    for comp in comps:
                        ic(wire, comp, engine)
                        await manager.create(table, name=comp,
                                             model=await manager.get(CarModel.select().where(CarModel.name == wire)),
                                             engine=await manager.get(
                                                 CarEngine.select().where(CarEngine.name == engine)))

async def mock_values():
    brand_names = ['Сhevrolet', 'Li Xiang', 'Leapmotor', 'BYD', 'Mercedes', 'Audi', 'Ford', 'BMW', 'Renault', 'Jeep', 'Ferrari']
    await insert_many(CarBrand, brand_names)

    state_names = ['Новое', 'Б/У']
    await insert_many(CarState, state_names)

    engine_names = ['ГИБРИД', 'ЭЛЕКТРО', 'ДВС']
    await insert_many(CarEngine, engine_names)

    await insert_many(CarColor, ['Другой', 'Серый', 'Чёрный', 'Синий', 'Белый', 'Жёлтый', 'Красный', 'Коричневый', 'Зелёный', 'Бордовый'])
    await insert_many(CarYear, ['2001-2007', '2004-2007', '2007-2010', '2010-2013', '2013-2016', '2016-2019', '2019-2022'])
    await insert_many(CarMileage, ['5000-10000', '10000-15000', '15000-20000', '20000-25000', '25000-30000', '30000-35000', '35000-40000', '40000-45000', '45000-50000', '50000-75000', '75000-100000', '100000+'])

    await insert_many_with_foregin(CarModel, {'BYD': ['SONG PLUS CHAMPION', 'CHAZOR'], 'Leapmotor': ['C11'], 'Li Xiang': ['L9', 'L7'], 'Сhevrolet': ['Gentra', 'Nexia 3'],

                                              'Mercedes': ['GLS', 'Metris', 'S-Class', 'EQS SUV', 'EQS Sedan'],
                                              'Audi': ['Q3', 'Q4 e-tron', 'Q5', 'A6', 'A8', 'S8', 'A7', 'S7', 'RS7'],
                                              'Ford': ['F-150', 'F-150 Lightning', 'Ford GT', 'Ford Maverick', 'Ford Mustang', 'Ford Mustang Mach-E'],
                                              'BMW': ['i3', 'iX', 'X1', 'X3', 'X4', 'X5', '8 Series'],
                                              'Renault': ['Megane E-Tech', 'Scenic E-Tech', '5', '4', 'Renault Twingo'],
                                              'Jeep': ['Grand Cherokee', 'Grand Cherokee L', 'Renegade', 'Wrangler', 'Wrangler'],
                                              'Ferrari': ['SF90 Stradale', 'F8 Tributo', 'Roma', 'Portofino M', '812 Superfast']})

    await insert_many_with_foregin(CarComplectation, {'CHAZOR': [{'ГИБРИД': 'XXX'}], 'SONG PLUS CHAMPION': [
        {'ЭЛЕКТРО': 'FLAGSHIP PLUS 605 km'}], 'C11': [{'ЭЛЕКТРО': ['Deluxe Edition 500 km (1)', 'Dual Motor 4WD 580 Km']}], 'L9': [
        {'ГИБРИД': 'L9 Max'}], 'L7': [{'ГИБРИД': 'L7 Pro'}], 'Gentra': [{'ДВС': '3'}], 'Nexia 3': [{'ДВС': '2'}],

            'GLS': {'ЭЛЕКТРО': ['Стандарт', 'Расширенный', 'Продвинутый']},
            'Metris': {'ГИБРИД': ['Эко', 'Премиум', 'Улучшенный']},
            'S-Class': {'ДВС': ['Базовая', 'Спортивная', 'Люкс']},
            'EQS SUV': {'ЭЛЕКТРО': ['Стандарт', 'Расширенный', 'Продвинутый']},
            'EQS Sedan': {'ГИБРИД': ['Эко', 'Премиум', 'Улучшенный']},

            'Q3': {'ДВС': ['Базовая', 'Спортивная', 'Люкс']},
            'Q4 e-tron': {'ГИБРИД': ['Эко', 'Премиум', 'Улучшенный']},
            'Q5': {'ГИБРИД': ['Эко', 'Премиум', 'Улучшенный']},
            'A6': {'ДВС': ['Базовая', 'Спортивная', 'Люкс']},
            'A8': {'ДВС': ['Базовая', 'Спортивная', 'Люкс']},
            'S8': {'ЭЛЕКТРО': ['Стандарт', 'Расширенный', 'Продвинутый']},
            'A7': {'ГИБРИД': ['Эко', 'Премиум', 'Улучшенный']},
            'S7': {'ГИБРИД': ['Эко', 'Премиум', 'Улучшенный']},
            'RS7': {'ЭЛЕКТРО': ['Стандарт', 'Расширенный', 'Продвинутый']},

            'F-150': {'ЭЛЕКТРО': ['Стандарт', 'Расширенный', 'Продвинутый']},
            'F-150 Lightning': {'ДВС': ['Базовая', 'Спортивная', 'Люкс']},
            'Ford GT': {'ДВС': ['Базовая', 'Спортивная', 'Люкс']},
            'Ford Maverick': {'ЭЛЕКТРО': ['Стандарт', 'Расширенный', 'Продвинутый']},
            'Ford Mustang': {'ДВС': ['Базовая', 'Спортивная', 'Люкс']},
            'Ford Mustang Mach-E': {'ЭЛЕКТРО': ['Стандарт', 'Расширенный', 'Продвинутый']},

            'i3': {'ГИБРИД': ['Эко', 'Премиум', 'Улучшенный']},
            'iX': {'ГИБРИД': ['Эко', 'Премиум', 'Улучшенный']},
            'X1': {'ГИБРИД': ['Эко', 'Премиум', 'Улучшенный']},
            'X3': {'ЭЛЕКТРО': ['Стандарт', 'Расширенный', 'Продвинутый']},
            'X4': {'ЭЛЕКТРО': ['Стандарт', 'Расширенный', 'Продвинутый']},
            'X5': {'ДВС': ['Базовая', 'Спортивная', 'Люкс']},
            '8 Series': {'ДВС': ['Базовая', 'Спортивная', 'Люкс']},

            'Megane E-Tech': {'ГИБРИД': ['Эко', 'Премиум', 'Улучшенный']},
            'Scenic E-Tech': {'ГИБРИД': ['Эко', 'Премиум', 'Улучшенный']},
            '5': {'ГИБРИД': ['Эко', 'Премиум', 'Улучшенный']},
            '4': {'ДВС': ['Базовая', 'Спортивная', 'Люкс']},
            'Renault Twingo': {'ЭЛЕКТРО': ['Стандарт', 'Расширенный', 'Продвинутый']},

            'Grand Cherokee': {'ЭЛЕКТРО': ['Стандарт', 'Расширенный', 'Продвинутый']},
            'Grand Cherokee L': {'ЭЛЕКТРО': ['Стандарт', 'Расширенный', 'Продвинутый']},
            'Renegade': {'ЭЛЕКТРО': ['Стандарт', 'Расширенный', 'Продвинутый']},
            'Wrangler': {'ГИБРИД': ['Эко', 'Премиум', 'Улучшенный']},

            'SF90 Stradale': {'ГИБРИД': ['Эко', 'Премиум', 'Улучшенный']},
            'F8 Tributo': {'ГИБРИД': ['Эко', 'Премиум', 'Улучшенный']},
            'Roma': {'ДВС': ['Базовая', 'Спортивная', 'Люкс']},
            'Portofino M': {'ГИБРИД': ['Эко', 'Премиум', 'Улучшенный']},
            '812 Superfast': {'ГИБРИД': ['Эко', 'Премиум', 'Улучшенный']}})





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
    justion = await manager.create(Seller, telegram_id=902230076, dealship_name='Борис Пром', entity='legal', dealship_address='Угол Борисова 45', authorized=True, phone_number='+79371567898')
    mockseller = await manager.create(Seller, telegram_id=902330076, dealship_name='Мокнутый', entity='legal', dealship_address='Шпельм', authorized=True, phone_number='+79323567898')
    mockselle2 = await manager.create(Seller, telegram_id=912330076, entity='natural', name='Мокнутый', surname='Частюк', patronymic=None, dealship_address=None, authorized=True, phone_number='+79323557898')

    return [justion, mockseller, mockselle2]

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
    await manager.connect()
    try:
        advert_photo_data_list = []
        photo_base = []

        for brand_id, photos in new_car_photos.items():
            # Получаем все объявления для данного бренда
            if params:
                current_table = AdvertParameters
            else:
                current_table = CarAdvert
            matching_adverts = await manager.execute(
                current_table.select(current_table, CarComplectation, CarColor).join(CarColor).switch(current_table).join(CarComplectation).join(CarEngine).switch(CarComplectation).join(CarModel).join(CarBrand).where(CarBrand.id == brand_id)
            )
            ic(brand_id, len(matching_adverts))
            # Подготовка данных для массовой вставки
            for advert in matching_adverts:
                for photo_id in photos:
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
    for index in range(9, 132):
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
        insert_carars = insert_carars#[:len(insert_carars)//100]
        await manager.execute(CarAdvert.insert_many(insert_carars))
    # await add_photo(photos, insert_carars)
    # if insert_data:
    #     insert_photo_query = AdvertPhotos.insert_many(insert_data)
    #     await manager.execute(insert_photo_query)

    # return

    if photos:
        await insert_advert_photos(photos, 0)

    return insert_carars
