import importlib
from datetime import time

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from config_data.config import DEFAULT_COMMANDS
from database.db_connect import manager
from database.tables.car_configurations import CarAdvert
from handlers.callback_handlers.admin_part.admin_panel_ui.bot_statistics.demand_statistics.top_ten_display import \
    TopTenByDemandDisplayHandler


# from database.data_requests.person_requests import PersonRequester

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


async def bot_help(callback: CallbackQuery, state: FSMContext):
    # await state.set_state()
    await state.update_data(calculate_method='top')
    await TopTenByDemandDisplayHandler().callback_handler(callback, state)
    # await manager.create(CarAdvert, seller=message.from_user.id, complectation=2, state=1, dollar_price=45545, color=2, mileage=None, year=None)
    # a
#     a = importlib.import_module('database.data_requests.tariff_requests')
#     tariff_to_seller_binder = importlib.import_module('database.data_requests.tariff_to_seller_requests')

    # person_exists = await PersonRequester.get_user_for_id(user_id=message.from_user.id, seller=True)
    # if not person_exists:
    #     await message.answer('Зарегистрируйтесь продавцом')
#
#     tariffs = a.TarifRequester.retrieve_all_data()
#     if not tariffs:
#         await create_tarifs()
#
#
#     data = {'seller': str(message.from_user.id),
#             'tariff': 'minimum'
#             }
#
#     await tariff_to_seller_binder.TariffToSellerBinder.set_bind(data=data, bot=message.bot)
#
#
