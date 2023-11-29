import asyncio

from database.db_connect import database, manager

from database.tables.car_configurations import (CarBrand, CarModel, CarComplectation, CarState,
                                                CarEngine, CarColor, CarMileage, User, CarAdvert, CarYear)
from database.tables.seller import Seller


class CarConfigs:

    @staticmethod
    async def add_brand(brand_name):
        brand, created = await database.get_or_create(CarBrand, name=brand_name)
        return brand

    @staticmethod
    async def get_by_id(table, model_id):
        if table == 'state':
            table = CarState
        elif table == 'engine_type':
            table = CarEngine
        elif table == 'brand':
            table = CarBrand
        elif table == 'model':
            table = CarModel
        elif table == 'complectation':
            table = CarComplectation
        elif table == 'year_of_release':
            table = CarYear
        elif table == 'mileage':
            table = CarMileage
        elif table == 'color':
            table = CarColor
        else:
            table = None

        if model_id and table:
            return await manager.get(table.select().where(table.id == model_id))


    @staticmethod
    async def get_for_second_hand(year=False, color=False, mileage=False):
        if year:
            current_table = CarYear
        elif color:
            current_table = CarColor
        elif mileage:
            current_table = CarMileage
        else:
            current_table = None

        if current_table:
            return await manager.execute(current_table.select())


    @staticmethod
    async def get_all_engines():
        return await manager.execute(CarEngine.select())

    @staticmethod
    async def get_all_states():
        return await manager.execute(CarState.select())


    @staticmethod
    async def get_all_brands():
        return await manager.execute(CarBrand.select())

    # Функции для работы с Model
    @staticmethod
    async def add_model(brand_id, model_name):
        brand = await database.get(CarBrand, CarBrand.id == brand_id)
        model, created = await database.get_or_create(CarModel, brand=brand, name=model_name)
        return model

    @staticmethod
    async def get_models_by_brand(brand_id):
        return await manager.execute(CarModel.select().where(CarModel.brand_id == brand_id))


    @staticmethod
    async def add_complectation(model_id, complectation_name):
        model = await database.get(CarModel, CarModel.id == model_id)
        complectation, created = await database.get_or_create(CarComplectation, model=model, name=complectation_name)
        return complectation

    @staticmethod
    async def get_complectations_by_model(model_id):
        return await manager.execute(CarComplectation.select().join(CarModel).where(CarModel.id == model_id))

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
    async def add_listing(user_id, data):
        seller = await manager.get(Seller, Seller.telegram_id == user_id)

        if seller:
            complectation = await manager.get(
                CarComplectation
                .select()
                .join(CarModel)  # Первое соединение с CarModel
                .switch(CarComplectation)  # Переключаемся обратно на CarComplectation
                .join(CarBrand, on=(CarModel.brand == CarBrand.id))  # Соединение с CarBrand через CarModel
                .where((CarModel.id == data['model']) & (CarBrand.id == data['brand']))
            )
            ic(data, data['engine_type'])
            listing = await manager.create(CarAdvert, seller=seller.telegram_id, complectation=complectation.id, price=data['price'],
                                            state=data['state'], engine_type=data['engine_type'],
                                            color=data.get('color'), mileage=data.get('mileage'), year=data.get('year_of_release'))
            return listing



# Основная функция для демонстрации использования

async def insert_many(table, names):
    for name in names:
        await manager.create(table, name=name)

async def insert_many_with_foregin(table, wire_to_name):
    for wire, names in wire_to_name.items():
        for name in names:
            if table == CarModel:
                ic(table, wire, name)
                await manager.create(table, name=name,
                                     brand=await manager.get(CarBrand.select().where(CarBrand.name == wire)))
            elif table == CarComplectation:
                await manager.create(table, name=name,
                                     model=await manager.get(CarModel.select().where(CarModel.name == wire)))



async def mock_values():
    brand_names = ['Сhevrolet', 'Li Xiang', 'Leapmotor', 'BYD']
    await insert_many(CarBrand, brand_names)

    state_names = ['Новое', 'Б/У']
    await insert_many(CarState, state_names)

    engine_names = ['ГИБРИД', 'ЭЛЕКТРО', 'ДВС']
    await insert_many(CarEngine, engine_names)

    await insert_many_with_foregin(CarModel, {'BYD': ['SONG PLUS CHAMPION', 'CHAZOR'], 'Leapmotor': ['C11'], 'Li Xiang': ['L9', 'L7'], 'Сhevrolet': ['Gentra', 'Nexia 3']})
    await insert_many_with_foregin(CarComplectation, {'CHAZOR': ['XXX'], 'SONG PLUS CHAMPION': ['FLAGSHIP PLUS 605 km'], 'C11': ['Deluxe Edition 500 km (1)', 'Dual Motor 4WD 580 Km'], 'L9': ['L9 Max'], 'L7': ['L9 Pro'], 'Gentra': ['3'], 'Nexia 3': ['2']})

    # await database.create(CarColor)
    # await database.create(CarMileage)
    # await database.create(CarYear)
    pass

async def get_car():
    await manager.create(CarAdvert, seller=902230076, complectation=3, state=1, engine_type=1, price=1233, color=None, mileage=None, year=None)