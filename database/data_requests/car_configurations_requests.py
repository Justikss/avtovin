import asyncio

from database.db_connect import database, manager

from database.tables.car_configurations import (CarBrand, CarModel, CarComplectation, CarState,
                                                CarEngine, CarColor, CarMileage, User, CarAdvert, CarYear)
from database.tables.commodity import AdvertPhotos
from database.tables.seller import Seller


class CarConfigs:



    @staticmethod
    async def add_brand(brand_name):
        brand, created = await database.get_or_create(CarBrand, name=brand_name)
        return brand

    @staticmethod
    async def get_by_name(name, mode):
        query = None
        if mode == 'color':
            query = CarColor.select().where(CarColor.name == name)

        if query:
            try:
                result = await manager.get(CarColor, CarColor.name == name)
                return result
            except:
                pass


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
    async def get_characteristic(year=False, color=False, mileage=False):
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
    async def get_models_by_brand_and_engine(brand_id, engine_id):
        return await manager.execute(CarModel.select().join(CarComplectation).join(CarEngine).where((CarEngine.id == engine_id) & (CarModel.brand_id == brand_id)))


    @staticmethod
    async def add_complectation(model_id, complectation_name):
        model = await database.get(CarModel, CarModel.id == model_id)
        complectation, created = await database.get_or_create(CarComplectation, model=model, name=complectation_name)
        return complectation

    @staticmethod
    async def get_complectations_by_model_and_engine(model_id, engine_id):
        return list(await manager.execute(CarComplectation.select().join(CarModel).switch(CarComplectation).join(CarEngine).where((CarModel.id == model_id) & (CarEngine.id == engine_id))))

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

            photo_album = data.get('photos')
            if listing and photo_album:
                if isinstance(photo_album, dict):
                    object_for_iteration = [photo_data for photo_data in photo_album.values()][0]
                else:
                    object_for_iteration = photo_album

                ic(object_for_iteration)
                structured_data = [{'car_id': listing.id, 'photo_id': photo_part['id'], 'photo_unique_id': photo_part['unique_id']} for photo_part in object_for_iteration]
                photo_insert = await manager.execute(AdvertPhotos.insert_many(structured_data))
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



async def mock_values():
    brand_names = ['Сhevrolet', 'Li Xiang', 'Leapmotor', 'BYD']
    await insert_many(CarBrand, brand_names)

    state_names = ['Новое', 'Б/У']
    await insert_many(CarState, state_names)

    engine_names = ['ГИБРИД', 'ЭЛЕКТРО', 'ДВС']
    await insert_many(CarEngine, engine_names)

    await insert_many(CarColor, ['Серый', 'Белый', 'Чёрный', 'Синий', 'Коричневый', 'Бирюзовый'])
    await insert_many(CarYear, ['2010-2013', '2013-2016', '2016-2019', '2019-2022'])
    await insert_many(CarMileage, ['5000-10000', '10000-15000', '15000-20000', '20000-25000', '25000-30000', '30000-35000', '35000-40000', '40000-45000', '45000-50000', '50000-75000', '75000-100000', '100000+'])

    await insert_many_with_foregin(CarModel, {'BYD': ['SONG PLUS CHAMPION', 'CHAZOR'], 'Leapmotor': ['C11'], 'Li Xiang': ['L9', 'L7'], 'Сhevrolet': ['Gentra', 'Nexia 3']})
    await insert_many_with_foregin(CarComplectation, {'CHAZOR': [{'ГИБРИД': 'XXX'}], 'SONG PLUS CHAMPION': [
        {'ЭЛЕКТРО': 'FLAGSHIP PLUS 605 km'}], 'C11': [{'ЭЛЕКТРО': ['Deluxe Edition 500 km (1)', 'Dual Motor 4WD 580 Km']}], 'L9': [
        {'ГИБРИД': 'L9 Max'}], 'L7': [{'ГИБРИД': 'L7 Pro'}], 'Gentra': [{'ДВС': '3'}], 'Nexia 3': [{'ДВС': '2'}]})

    # await database.create(CarColor)
    # await database.create(CarMileage)
    # await database.create(CarYear)
    pass

async def get_car():
    await manager.create(CarAdvert, seller=902230076, complectation=1, state=1, engine_type=1, price=56634, color=None, mileage=None, year=None)
    await manager.create(CarAdvert, seller=902230076, complectation=2, state=1, engine_type=2, price=45545, color=None, mileage=None, year=None)
    await manager.create(CarAdvert, seller=902230076, complectation=3, state=1, engine_type=2, price=5556645, color=None, mileage=None, year=None)
    await manager.create(CarAdvert, seller=902230076, complectation=4, state=1, engine_type=2, price=75632, color=None, mileage=None, year=None)
    await manager.create(CarAdvert, seller=902230076, complectation=5, state=1, engine_type=1, price=23423, color=None, mileage=None, year=None)
    await manager.create(CarAdvert, seller=902230076, complectation=6, state=1, engine_type=1, price=22222, color=None, mileage=None, year=None)
    await manager.create(CarAdvert, seller=902230076, complectation=7, state=1, engine_type=3, price=1234223, color=None, mileage=None, year=None)
    await manager.create(CarAdvert, seller=902230076, complectation=8, state=1, engine_type=3, price=53458799, color=None, mileage=None, year=None)
