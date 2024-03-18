import importlib
import traceback
from typing import Union, List
import datetime

from peewee import DoesNotExist, IntegrityError

from database.data_requests.car_advert_requests import AdvertRequester
from database.data_requests.dying_tariff import DyingTariffRequester
from database.tables.seller import Seller
from database.tables.tariff import Tariff, TariffsToSellers
from utils.asyncio_tasks.invalid_tariffs_deleter import set_timer_on_active_tariff
from utils.custom_exceptions.database_exceptions import NonExistentIdException, NonExistentTariffException, \
    SellerWithoutTariffException
from database.db_connect import manager



class TariffToSellerBinder:
    @staticmethod
    async def get_by_id(tariff_id):
        tariff_model = None
        try:
            tariff_model = await manager.get(TariffsToSellers.select(TariffsToSellers, Seller).where(TariffsToSellers == tariff_id))
            return tariff_model
        except:
            pass

        return tariff_model

    @staticmethod
    async def get_wires_by_tariff_id(tariff_id):
        if not isinstance(tariff_id, int):
            tariff_id = int(tariff_id)
        tariff_model = await manager.execute(TariffsToSellers.select(TariffsToSellers, Tariff).join(Tariff).where(Tariff.id == tariff_id))
        return tariff_model

    @staticmethod
    async def retrieve_all_data() -> Union[bool, List[TariffsToSellers]]:
        '''Асинхронный метод для извлечения всех связей тарифов с продавцами'''
        select_request = await manager.execute(TariffsToSellers.select(TariffsToSellers, Seller).join(Seller))
        return list(select_request) if select_request else False

    @staticmethod
    async def get_by_seller_id(seller_id):
        '''Асинхронный метод извлечения модели по телеграм id продавца'''
        try:
            tariff = await manager.get(TariffsToSellers
                                       .select(TariffsToSellers, Seller)
                                       .join(Seller)
                                       .where(Seller.telegram_id == seller_id))
            return tariff
        except TariffsToSellers.DoesNotExist:
            # traceback.print_exc()
            # Обработка ситуации, когда запись не найдена
            return None

    @staticmethod
    async def tariff_is_actuality(seller_model, bot):
        person_requester = importlib.import_module('database.data_requests.person_requests')

        if not isinstance(seller_model, int):
            seller = seller_model.telegram_id
        else:
            seller = seller_model
            seller_model = await person_requester.PersonRequester.get_user_for_id(seller, seller=True)

        feedbacks = await TariffToSellerBinder.subtract_feedback_and_check_tariff(seller, bot, check_mode=True)
        ic(feedbacks)
        # if not feedbacks:
        #     await TariffToSellerBinder.remove_bind(seller_model)

        return feedbacks

    @staticmethod
    async def check_simultaneous_announcements_residue(seller_id):
        if isinstance(seller_id, str):
            seller_id = int(seller_id)
        seller_to_tariff = list(await manager.execute(TariffsToSellers.select(TariffsToSellers, Tariff, Seller).join(Tariff).switch(TariffsToSellers).join(Seller).where(Seller.telegram_id == seller_id)))
        sellers_adverts = await AdvertRequester.get_advert_by_seller(seller_id, count=True)
        if seller_to_tariff:
            simultaneous_announcements_residual = seller_to_tariff[0].tariff.simultaneous_announcements
            ic(sellers_adverts, simultaneous_announcements_residual)
            if simultaneous_announcements_residual:
                ic(not sellers_adverts < simultaneous_announcements_residual)
                if simultaneous_announcements_residual:
                    if not sellers_adverts < simultaneous_announcements_residual:
                        return simultaneous_announcements_residual

            return True
        else:
            raise SellerWithoutTariffException()

    @staticmethod
    async def subtract_feedback_and_check_tariff(seller_telegram_id, bot, check_mode=False):
        async with manager.atomic():
            # Найти связь продавца с тарифом
            try:
                tariff_link = await manager.get(TariffsToSellers.select().where(
                    TariffsToSellers.seller == seller_telegram_id))
            except DoesNotExist:
                ic(DoesNotExist)
                return False
            try:
                if not await TariffToSellerBinder.tariff_waste(seller_telegram_id, bot):
                    # Уменьшить количество оставшихся откликов
                    if tariff_link.residual_feedback > 0:
                        if check_mode:
                            return True
                        else:
                            tariff_link.residual_feedback -= 1
                            await manager.update(tariff_link)

                        # Если откликов не осталось, удалить связь с тарифом
                        if tariff_link.residual_feedback == 0:
                            # await manager.delete(tariff_link)
                            # await AdvertRequester.set_sleep_status(True, seller_telegram_id)
                            await DyingTariffRequester.dying_tariff_handler(seller_telegram_id, bot)
                            # await TariffToSellerBinder.remove_bind(seller_telegram_id)
                            return 'last_feedback'
                        else:
                            ic(tariff_link.residual_feedback)
                            return True
                    else:
                        ic(tariff_link.residual_feedback)
                        return False
                else:
                    await DyingTariffRequester.dying_tariff_handler(seller_telegram_id, bot)
                    ic(await TariffToSellerBinder.tariff_waste(seller_telegram_id, bot))
                    return False
            except SellerWithoutTariffException as ex:
                raise SellerWithoutTariffException()

    @staticmethod
    async def tariff_waste(telegram_id, bot):
        '''Тариф истёк?'''
        query = TariffsToSellers.select().where(TariffsToSellers.seller_id == telegram_id)
        total_bind = await manager.execute(query)
        if total_bind:
            total_bind = total_bind[0]
            datetime_now = datetime.datetime.now()
            datetime_tariff_end = total_bind.end_date_time
            if datetime_tariff_end >= datetime_now:
                return False
            else:
                # await AdvertRequester.set_sleep_status(True, telegram_id)
                await DyingTariffRequester.dying_tariff_handler(telegram_id, bot)
                return True
        else:
            raise SellerWithoutTariffException()

    @staticmethod
    async def set_bind(data: dict, bot, seconds) -> bool:
        '''Асинхронный метод установки связей тарифов с продавцом'''
        if await TariffToSellerBinder.get_by_seller_id(data.get('seller')):
            await TariffToSellerBinder.remove_bind(data.get('seller'))
        great_data = await TariffToSellerBinder.__data_extraction_to_boot(data, seconds)
        try:
            new_bind = await manager.create(TariffsToSellers, **great_data)
            if new_bind:
                await set_timer_on_active_tariff(new_bind, bot)
        except IntegrityError:
            return False
        return True

    @staticmethod
    async def __data_extraction_to_boot(data, seconds = None):
        '''Асинхронный вспомогательный метод для извлечения и обработки данных'''
        tariff_requests_module = importlib.import_module('database.data_requests.tariff_requests')
        person_requester = importlib.import_module('database.data_requests.person_requests')
        seconds = True
        if isinstance(data, dict):
            config_module = importlib.import_module('config_data.config')

            seller_id = data.get('seller')
            tariff = data.get('tariff')
            if seller_id:
                data['seller'] = await person_requester.PersonRequester.get_user_for_id(user_id=seller_id, seller=True)
                data['seller'] = data['seller'][0] if data['seller'] else None
                if tariff:
                    ic(tariff)
                    if not isinstance(tariff, Tariff):
                        if str(tariff).isalpha():
                            tariff = await manager.get(Tariff, Tariff.name == tariff)
                        else:
                            tariff = await tariff_requests_module.TarifRequester.get_by_id(tariff)
                    now_time = datetime.datetime.now()
                    '''Эта часть только для теста'''
                    if not seconds:
                        days = int(tariff.duration_time)
                        end_plut_datetime = datetime.timedelta(days=days)
                    else:
                        end_plut_datetime = datetime.timedelta(seconds=seconds)

                    end_time = now_time + end_plut_datetime

                    data['tariff'] = tariff
                    data['start_date_time'] = datetime.datetime.strptime(now_time.strftime(config_module.DATETIME_FORMAT), config_module.DATETIME_FORMAT)
                    data['end_date_time'] = datetime.datetime.strptime(end_time.strftime(config_module.DATETIME_FORMAT), config_module.DATETIME_FORMAT)
                    data['residual_feedback'] = tariff.feedback_amount
                    ic(data)

                    return data
                else:
                    raise NonExistentTariffException(f'Tariff id {tariff.id} not exist in database.')
            else:
                raise NonExistentIdException(f'Seller id {seller_id} not exist in database.')

    @staticmethod
    async def remove_bind(seller_id):
        tariff_requests_module = importlib.import_module('database.data_requests.tariff_requests')
        try:
            delete_query = await manager.execute(TariffsToSellers.delete().where(TariffsToSellers.seller == seller_id))
        except IntegrityError:
            await DyingTariffRequester.remove_old_tariff_to_update(seller_id)
            delete_query = await manager.execute(TariffsToSellers.delete().where(TariffsToSellers.seller == seller_id))

        await tariff_requests_module.TarifRequester.try_delete_dying_tariff()
        return True if delete_query else False

    # @classmethod
    # async def set_bind(cls, data: dict) -> bool:
    #     '''Асинхронный метод установки связей тарифов с продавцом'''
    #     great_data = await cls.__data_extraction_to_boot(data)
    #     insert_query = TariffsToSellers.insert(**great_data)
    #     await manager.execute(insert_query)
    #     return True


data = {'seller': '902230076',
'tariff': 'minimum'
}

# TariffToSellerBinder.set_bind(data=data)