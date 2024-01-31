import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
import asyncio
import importlib



# Предположим, что dying_tariffs_module и config_module уже импортированы

async def stop_active_tariff(tariff, bot):
    # dying_tariffs_module = importlib.import_module('database.data_requests.dying_tariff')
    print('stop_active_trff')
    # await dying_tariffs_module.DyingTariffRequester.set_status(tariff_model=tariff, bot=bot)

async def delete_expired_dying_tariff(tariff_id, bot):
    # Логика удаления истёкшего тарифа
    print(f"Deleting expired dying tariff {tariff_id}")

def schedule_task(scheduler, end_time, func, *args):
    """Планирует выполнение задачи на определённое время."""
    if isinstance(end_time, str):
        end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    scheduler.add_job(func, 'date', run_date=end_time, args=args)

async def main():
    # logger = logging.getLogger()
    # logger.setLevel(logging.DEBUG)
    logging.getLogger('apscheduler').setLevel(logging.DEBUG)
    scheduler = AsyncIOScheduler()
    scheduler.start()

    # Допустим, у нас есть объекты tariff и dying_tariff для демонстрации
    active_tariff = {"end_date_time": datetime.now() + timedelta(seconds=10)}
    dying_tariff = {"end_time": datetime.now() + timedelta(seconds=20), "id": "123"}

    # Планирование задач
    schedule_task(scheduler, active_tariff["end_date_time"], stop_active_tariff, active_tariff, "bot")
    schedule_task(scheduler, dying_tariff["end_time"], delete_expired_dying_tariff, dying_tariff["id"], "bot")

    # Цикл событий, чтобы скрипт продолжал работать
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
