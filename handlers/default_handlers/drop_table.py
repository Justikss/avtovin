import asyncio
import traceback
import uuid
from datetime import timedelta, datetime
from random import random, randint

import faker
from aiogram.types import Message
from faker import Faker

from database.data_requests.car_configurations_requests import mock_values, get_car, get_seller_account, mock_feedbacks
from database.data_requests.new_car_photo_requests import PhotoRequester
from database.data_requests.utils.drop_tables import drop_tables_except_one
from database.db_connect import create_tables, manager
import os

from database.tables.car_configurations import CarAdvert, CarColor, CarComplectation, CarEngine
from database.tables.commodity import AdvertPhotos
from database.tables.offers_history import SellerFeedbacksHistory
from database.tables.seller import Seller
from database.tables.statistic_tables.advert_parameters import AdvertParameters
from database.tables.statistic_tables.advert_to_admin_view_status import AdvertsToAdminViewStatus
from database.tables.tech_support_contacts import TechSupports


async def insert_phototo(dataa):
    insert_data=[]
    ic(dataa)
    for data in dataa:
        ic(data)
        commodity_query = (CarAdvert
                           .select()
                           .join(CarColor).switch(CarAdvert).join(CarComplectation).join(CarEngine)
                           .where(
            (CarComplectation.id == data['car_complectation']) & (CarColor.id == data['car_color'])
            ))
        nice_car = list(await manager.execute(commodity_query))
        if nice_car:
            nice_car = nice_car[0]


            insert_data.append({'car_id': nice_car.id, 'photo_id': data['photo_id'], 'photo_unique_id': data['photo_unique_id']})
        # ic(insert_data)
    if insert_data:
        ic(insert_data)
        insert_photo_query = AdvertPhotos.insert_many(insert_data)
        await manager.execute(insert_photo_query)
        ic(insert_photo_query)

async def load_type_photos(dota):
    data = []
    for idd, photos in dota.items():
        idd = int(idd)
        idd -= 1

        # pre_data = [[1, 1, 1], [2, 1, 1], [3, 1, 1], [4, 1, 1], [5, 1, 1], [6, 1, 1], [7, 1, 1], [8, 1, 1]]
        pre_data = [[1, 1, 2], [2, 2, 2], [3, 2, 2], [4, 2, 2], [5, 1, 2], [6, 1, 2], [7, 3, 2], [8, 3, 1]]
        current_part = pre_data[idd]
        for part in photos:
            data.append({'admin_id': 902230076,
                     'car_complectation': current_part[0],
                     'car_color': current_part[2],
                     'photo_id': part,
                     'photo_unique_id': f'{idd}_{uuid.uuid4()}'})

    try:
        await insert_phototo(data)
    except:
        pass
    ic(data)
    try:
        await PhotoRequester.load_photo_in_base(data)
    except:
        traceback.print_exc()
        pass

async def read_photos_by_brand(directory):
    brand_photos = {}
    # Перебор всех файлов и папок в директории
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        # Проверка, является ли элемент папкой
        if os.path.isdir(item_path):
            brand_id = item
            brand_photos[brand_id] = []
            # Перебор всех файлов в папке бренда
            for file in os.listdir(item_path):
                file_path = os.path.join(item_path, file)
                # Проверка, является ли файл изображением
                if os.path.isfile(file_path) and file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                    brand_photos[brand_id].append(file_path)
    ic(brand_photos)
    return brand_photos

async def set_viewed_status():
    adverts = list(await manager.execute(CarAdvert.select(CarAdvert.id)))
    insetred_data = [{'advert': advert.id} for advert in adverts]
    if insetred_data:
        await manager.execute(AdvertsToAdminViewStatus.insert_many(insetred_data))

async def create_ts_contacts():
    faker = Faker()
    links = [f'@{faker.name()}' for _ in range(6)]
    numbers = [faker.phone_number() for _ in range(6)]
    insert_tss = [{'link': link, 'type': 'telegram'} for link in links]
    insert_tsss = [{'link': link, 'type': 'number'} for link in numbers]
    await manager.execute(TechSupports.insert_many(insert_tss))
    await manager.execute(TechSupports.insert_many(insert_tsss))

async def dop_feedbacks():
    aps = list()
    for color, complectation in zip(range(1, 10), range(1, 9)):
        aps.append({'color': color,
                    'complectation': complectation})

    await manager.execute(AdvertParameters.insert_many(aps))
    advert_params_end_index = len(aps) + 10
    sfb = []
    for ap_id in range(11, advert_params_end_index):
        sfb.extend([{'seller_id': 902230076, 'advert_parameters': ap_id,
          'feedback_time': datetime.now() - timedelta(days=randint(150, 365))}])
    await manager.execute(SellerFeedbacksHistory.insert_many(sfb))

async def get_adverts():
    complectations = await manager.execute(CarComplectation.select())
    colors = await manager.execute(CarColor.select())

    insert_data = list()

    for index in range(9):
        if index > 7:
            index -= 3
        insert_data.append({
            'seller': 902230076,
        'complectation': complectations[0],
        'state': 1,
        'sum_price': 5000 * index,
        'dollar_price': None,
        'color': colors[index]

        })
    ic(insert_data)
    await manager.execute(CarAdvert.insert_many(insert_data))

async def drop_table_handler(message: Message):
    await get_adverts()
    return
    await message.answer('Waiting..')
    await drop_tables_except_one('Фотографии_Новых_Машин')
    await create_tables()
    await mock_values(0)
    sellers = await get_seller_account()
    photos = None
    photos = await read_photos_by_brand('utils/carss')
    inserted_cars = await get_car(photos, cars=0)
    asyncio.create_task(mock_feedbacks(sellers, inserted_cars))
    await dop_feedbacks()
    type_photos = await read_photos_by_brand('utils/type_carss')
    await load_type_photos(type_photos)
    await set_viewed_status()

    await create_ts_contacts()

    await message.answer('SUCCESS')