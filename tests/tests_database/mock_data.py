import asyncio

from faker import Faker
import random


from tests.tests_database.mock_tables import (Seller, CarBrand, CarComplectation, CarModel, CarColor, CarEngine,
                                              AdvertParameters, SellerFeedbacksHistory)

fake = Faker()


async def create_random_sellers(mock_manager, n):
    sellers = []
    for _ in range(n):
        entity_type = random.choice(["Individual", "Company"])

        if entity_type == "Company":
            # Создаем запись для автосалона
            seller = await mock_manager.create(Seller,
                                               telegram_id=fake.random_number(digits=9, fix_len=True),
                                               phone_number=fake.phone_number(),
                                               dealship_name=fake.company(),
                                               entity=entity_type,
                                               dealship_address=fake.address(),
                                               authorized=fake.boolean(),
                                               data_registration=fake.date())
        else:
            # Создаем запись для частного продавца
            seller = await mock_manager.create(Seller,
                                               telegram_id=fake.random_number(digits=9, fix_len=True),
                                               phone_number=fake.phone_number(),
                                               entity=entity_type,
                                               name=fake.first_name(),
                                               surname=fake.last_name(),
                                               patronymic=fake.first_name(),
                                               authorized=fake.boolean(),
                                               data_registration=fake.date())

        sellers.append(seller)
    return sellers


async def create_random_car_data(mock_manager, n):
    brands = []
    models = []
    engines = []
    colors = []

    for _ in range(n):
        brand_name = fake.company()
        brand, created = await mock_manager.get_or_create(CarBrand, name=brand_name)
        brands.append(brand)

        car_model_name = fake.word()
        car_model, created = await mock_manager.get_or_create(CarModel, brand=brand, name=car_model_name)
        models.append(car_model)

        engine_name = fake.word()
        engine, created = await mock_manager.get_or_create(CarEngine, name=engine_name)
        engines.append(engine)

        color_name = fake.color_name()
        color, created = await mock_manager.get_or_create(CarColor, name=color_name)
        colors.append(color)

    return brands, models, engines, colors


async def create_random_advert_parameters(mock_manager, n):
    _, models, engines, colors = await create_random_car_data(mock_manager, n)
    advert_parameters = []

    for model, engine, color in zip(models, engines, colors):
        complectation = await mock_manager.create(CarComplectation, model=model, engine=engine, name=fake.word())
        advert_param = await mock_manager.create(AdvertParameters, complectation=complectation, color=color)
        advert_parameters.append(advert_param)

    return advert_parameters


async def create_random_feedbacks(mock_manager, n, sellers, advert_parameters):
    for _ in range(n):
        seller = random.choice(sellers)
        advert_param = random.choice(advert_parameters)
        await mock_manager.create(SellerFeedbacksHistory,
                             seller_id=seller,
                             advert_parameters=advert_param,
                             feedback_time=fake.date())


# Использование функций для создания моковых данных
async def generate_mock_data(mock_manager, mock_database):
    # await mock_manager.connect()

    sellers = await create_random_sellers(mock_manager, 10)
    advert_parameters = await create_random_advert_parameters(mock_manager, 10)
    await create_random_feedbacks(mock_manager, 50, sellers, advert_parameters)
    # await mock_manager.close()


# asyncio.run()