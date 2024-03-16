import aiocron
from aiogram import Bot
from datetime import datetime, timedelta
import importlib

config_module = importlib.import_module('config_data.config')
# Ваши классы моделей: Seller, Tariff, TariffsToSellers
# Инициализация менеджера (предполагается, что у вас уже есть инициализированный объект database)

def end_time_control(end_time):
    two_minutes_future_time = datetime.now() + timedelta(minutes=2)
    if end_time <= two_minutes_future_time:
        end_time = two_minutes_future_time
    return end_time

async def delete_expired_dying_tariff(tariff, bot):
    dying_tariffs_module = importlib.import_module('database.data_requests.dying_tariff')

    await dying_tariffs_module.DyingTariffRequester.remove_dying_tariff_to_lose(tariff, bot)

async def stop_active_tariff(tariff, bot):
    dying_tariffs_module = importlib.import_module('database.data_requests.dying_tariff')

    await dying_tariffs_module.DyingTariffRequester.set_status(tariff_model=tariff, bot=bot)

async def set_timer_on_dying_tariff(dying_tariff, bot):
    end_time = dying_tariff.end_time
    if isinstance(end_time, str):
        end_time = datetime.strptime(end_time, config_module.DATETIME_FORMAT)

    end_time = end_time_control(end_time)

    # Конвертация времени в строку cron
    cron_time = end_time.strftime('%M %H %d %m *')

    # Планирование с использованием aiocron
    aiocron.crontab(cron_time, func=delete_expired_dying_tariff, args=(dying_tariff, bot))


async def set_timer_on_active_tariff(active_tariff, bot):
    end_time = active_tariff.end_date_time
    if isinstance(end_time, str):
        end_time = datetime.strptime(end_time, config_module.DATETIME_FORMAT)

    end_time = end_time_control(end_time)


    cron_time = end_time.strftime('%M %H %d %m *')
    aiocron.crontab(cron_time, func=stop_active_tariff, args=(active_tariff, bot))


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
