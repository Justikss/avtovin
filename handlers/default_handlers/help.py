import importlib
from datetime import time

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config_data.config import DEFAULT_COMMANDS
from database.data_requests.tariff_to_seller_requests import TariffToSellerBinder
from database.data_requests.person_requests import PersonRequester

async def create_tarifs():
    a = importlib.import_module('database.data_requests.tariff_requests')
    data = {'name': 'minimum',
            'price': 50,
            'duration_time': '365',
            'feedback_amount': 100}

    data2 = {'name': 'medium',
             'price': 200,
             'duration_time': '365',
             'feedback_amount': 500}

    data3 = {'name': 'maximum',
             'price': 1000,
             'duration_time': '365',
             'feedback_amount': 10000}

    a.TarifRequester.set_tariff(data)
    a.TarifRequester.set_tariff(data3)
    a.TarifRequester.set_tariff(data2)


async def bot_help(message: Message):
    a = importlib.import_module('database.data_requests.tariff_requests')

    person_exists = await PersonRequester.get_user_for_id(user_id=message.from_user.id, seller=True)
    if not person_exists:
        await message.answer('Зарегистрируйтесь продавцом')

    tariffs = a.TarifRequester.retrieve_all_data()
    if not tariffs:
        await create_tarifs()


    data = {'seller': str(message.from_user.id),
            'tariff': 'minimum'
            }

    await TariffToSellerBinder.set_bind(data=data, bot=message.bot)


