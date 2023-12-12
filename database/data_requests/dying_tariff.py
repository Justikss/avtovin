import importlib
from datetime import datetime

from database.data_requests.car_advert_requests import AdvertRequester
from database.data_requests.person_requests import PersonRequester
from database.db_connect import manager
from database.tables.seller import Seller
from database.tables.tariff import DyingTariffs, TariffsToSellers
from utils.asyncio_tasks.invalid_tariffs_deleter import set_timer_on_dying_tariff
from utils.seller_notifications.seller_lose_tariff import send_notification_about_lose_tariff


class DyingTariffRequester:

    @staticmethod
    async def dying_tariff_handler(seller, bot):
        dying_status_is_exists = await DyingTariffRequester.tariff_was_dying(seller)
        if dying_status_is_exists:
            pass
        else:
            await DyingTariffRequester.set_status(seller, bot=bot)

    @staticmethod
    async def set_status(seller=None, tariff_model=None, bot=None):
        tariff_binder_module = importlib.import_module('database.data_requests.tariff_to_seller_requests')
        ic(seller)
        ic(tariff_model)
        if not seller and tariff_model:
            tariff_model = await tariff_binder_module.TariffToSellerBinder.get_by_id(tariff_model)

        if not tariff_model:
            tariff_model = await tariff_binder_module.TariffToSellerBinder.get_by_seller_id(seller.telegram_id)


        if not seller:
            ic(tariff_model)
            seller = tariff_model.seller
        ic(seller)
        ic(tariff_model)
        await AdvertRequester.set_sleep_status(True, seller)
        if bot:
            await send_notification_about_lose_tariff(seller_id=seller, bot=bot)
        ic(tariff_model)
        dying_tariff = await manager.create(DyingTariffs, tariff_wire=tariff_model)
        if dying_tariff:
            await set_timer_on_dying_tariff(dying_tariff, bot)

    @staticmethod
    async def check_end_time():
        end_tariffs = list(await manager.execute(DyingTariffs.select(Seller).where(DyingTariffs.end_time < datetime.now())))
        # if end_tariffs:
        #     for tariff in end_tariffs:
        #         await AdvertRequester.delete_advert_by_id(seller_id=tariff.seller.telegram_id)
        #
        # select_query = await manager.execute(DyingTariffs.delete().where(DyingTariffs.end_time < datetime.now()))
        return end_tariffs

    @staticmethod
    async def remove_dying_tariff_to_lose(tariff_id):
        '''стёрка деятельности продавца по id мёртвого тарифа'''
        try:
            ic(tariff_id)
            dying_tariff = await manager.get(DyingTariffs.select(DyingTariffs, TariffsToSellers, Seller).join(TariffsToSellers).join(Seller).where(DyingTariffs.id == tariff_id))
        except:
            dying_tariff = None
        ic(dying_tariff)
        if dying_tariff:
            active_tariffs_module = importlib.import_module('database.data_requests.tariff_to_seller_requests')

            await manager.execute(DyingTariffs.delete().where(DyingTariffs.id == tariff_id))
            await active_tariffs_module.TariffToSellerBinder.remove_bind(dying_tariff.tariff_wire.seller)
            await AdvertRequester.delete_advert_by_id(seller_id=dying_tariff.tariff_wire.seller)

    @staticmethod
    async def remove_old_tariff_to_update(seller):
        if not isinstance(seller, int):
            seller = seller.telegram_id
        old_tariff = await manager.execute(DyingTariffs.select().join(Seller).where(Seller.telegram_id == seller))
        if old_tariff:
            await manager.execute(DyingTariffs.delete().where(DyingTariffs.id == old_tariff.id))

    @staticmethod
    async def tariff_was_dying(seller):
        dying_is_exists = await manager.execute(DyingTariffs.select().join(TariffsToSellers).join(Seller).where(Seller.telegram_id == seller))
        return True if dying_is_exists else False

    @staticmethod
    async def retrieve_dying_tariffs():
        dying_tariffs = list(await manager.execute(DyingTariffs.select()))
        return dying_tariffs