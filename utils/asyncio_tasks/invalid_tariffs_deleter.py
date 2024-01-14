import asyncio
import importlib

from aiogram import Bot
from peewee import *
from datetime import datetime, timedelta


config_module = importlib.import_module('config_data.config')
# Ваши классы моделей: Seller, Tariff, TariffsToSellers
# Инициализация менеджера (предполагается, что у вас уже есть инициализированный объект database)

async def delete_expired_dying_tariff(tariff, wait_seconds, bot):
    dying_tariffs_module = importlib.import_module('database.data_requests.dying_tariff')
    print('stop_dying_trff')
    # Ждем до момента истечения срока действия тарифа
    await asyncio.sleep(wait_seconds)
    # Удаление тарифа
    await dying_tariffs_module.DyingTariffRequester.remove_dying_tariff_to_lose(tariff, bot)

async def stop_active_tariff(tariff, wait_seconds, bot):
    dying_tariffs_module = importlib.import_module('database.data_requests.dying_tariff')
    print('stop_active_trff')

    await asyncio.sleep(wait_seconds)

    await dying_tariffs_module.DyingTariffRequester.set_status(tariff_model=tariff, bot=bot)

async def set_timer_on_dying_tariff(dying_tariff, bot):
    print('set_time_dying_trff')
    now = datetime.now()
    end_time = dying_tariff.end_time
    if isinstance(end_time, str):
        end_time = datetime.strptime(end_time, config_module.DATETIME_FORMAT)
    wait_seconds = (end_time - now).total_seconds()
    asyncio.create_task(delete_expired_dying_tariff(dying_tariff.id, wait_seconds, bot))


async def set_timer_on_active_tariff(active_tariff, bot):
    print('set_time_active_trff')
    '''Активные тарифы:'''
    now = datetime.now()
    end_time = active_tariff.end_date_time
    if isinstance(end_time, str):
        end_time = datetime.strptime(end_time, config_module.DATETIME_FORMAT)
    wait_seconds = (end_time - now).total_seconds()
    asyncio.create_task(stop_active_tariff(active_tariff, wait_seconds, bot))

async def schedule_tariff_deletion(bot: Bot):
    active_tariffs_module = importlib.import_module('database.data_requests.tariff_to_seller_requests')
    dying_tariffs_module = importlib.import_module('database.data_requests.dying_tariff')
    # Получение всех мёртвых тарифов, которые еще не истекли
    dying_tariffs = await dying_tariffs_module.DyingTariffRequester.retrieve_dying_tariffs()
    # Запланировать задачи для удаления тарифов
    if dying_tariffs:
        for dying_tariff in dying_tariffs:
            await set_timer_on_dying_tariff(dying_tariff, bot)

    active_tariffs = await active_tariffs_module.TariffToSellerBinder.retrieve_all_data()
    if active_tariffs:
        for active_tariff in active_tariffs:
            await set_timer_on_active_tariff(active_tariff, bot)
