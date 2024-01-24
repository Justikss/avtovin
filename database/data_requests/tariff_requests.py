import importlib
import logging
import traceback
from typing import Union, List

from database.tables.tariff import Tariff, TariffsToSellers, DyingTariffs
from utils.custom_exceptions.database_exceptions import TariffHasClientsException, TariffHasWireError
from database.db_connect import database, manager



class TarifRequester:
    @staticmethod
    async def try_delete_dying_tariff():
        query = (Tariff
        .delete()
        .where(
            (Tariff.dying_status == True) &
            ~(Tariff.id.in_(TariffsToSellers.select(TariffsToSellers.tariff))) &
            ~(Tariff.id.in_(
                DyingTariffs.select(DyingTariffs.tariff_wire.tariff).join(TariffsToSellers)
            ))
        )
        )
        await manager.execute(query)

    @staticmethod
    async def set_dying_tariff_status(tariff_id):
        tariff_to_seller_binder_module = importlib.import_module('database.data_requests.tariff_to_seller_requests')

        if not isinstance(tariff_id, int):
            tariff_id = int(tariff_id)
        tariff_to_seller = await tariff_to_seller_binder_module.TariffToSellerBinder.get_wires_by_tariff_id(tariff_id)
        if tariff_to_seller:
            await manager.execute(Tariff.update(dying_status=True).where(Tariff.id == tariff_id))
        else:
            await manager.execute(Tariff.delete().where(Tariff.id == tariff_id))

        return True


    @staticmethod
    async def get_tariff_by_name(tariff_name):
        return await manager.get_or_none(Tariff, ((Tariff.name == tariff_name) & ((Tariff.dying_status == False) | (Tariff.dying_status.is_null(True)))))

    @staticmethod
    async def retrieve_all_data() -> Union[bool, List[Tariff]]:
        '''Асинхронный метод для извлечения всех моделей тарифов'''
        query = Tariff.select().where((Tariff.dying_status == False) | (Tariff.dying_status.is_null(True))).order_by(Tariff.id)
        select_request = await manager.execute(query)
        return list(select_request) if select_request else False

    @staticmethod
    async def set_tariff(data: dict) -> bool:
        '''Асинхронный метод для установки тарифа'''
        try:
            insert_query = Tariff.insert(**data)
            await manager.execute(insert_query)
            inserted_model = await TarifRequester.get_tariff_by_name(data.get('name'))
            return inserted_model
        except Exception:
            logging.error('', exc_info=True)
            return False

    @staticmethod
    async def get_by_id(tariff_id):
        '''Асинхронный метод получения тарифа по ID'''
        ic(tariff_id)
        if isinstance(tariff_id, str):
            tariff_id = int(tariff_id)
        try:
            tariff = await manager.get(Tariff, ((Tariff.id == tariff_id) & ((Tariff.dying_status == False) | (Tariff.dying_status.is_null(True)))))
        except:
            tariff = None
        ic(tariff)
        ic(await manager.get_or_none(Tariff, id=tariff_id))
        return tariff


    @staticmethod
    async def delete_tariff(tariff_id: int | str) -> bool:
        '''Асинхронный метод удаления тарифа'''
        if isinstance(tariff_id, str):
            tariff_id = int(tariff_id)
        try:
            sub_query = TariffsToSellers.select(TariffsToSellers.tariff)
            tariff_model = await manager.get_or_none(Tariff.select().where((Tariff.id == tariff_id) & (Tariff.id.not_in(sub_query))))
            ic(tariff_model)
            if tariff_model:
                delete_query = Tariff.delete().where(Tariff.id == tariff_model.id)
                await manager.execute(delete_query)
                return True
            else:
                raise TariffHasWireError()
        except Exception as ex:
            traceback.print_exc()
            return False

    @staticmethod
    async def create_tarifs():
        if not list(await manager.execute(Tariff.select())):
            insert_tariffs = [{'name': 'BEPUL', 'price': 0, 'duration_time': 90, 'feedback_amount': 999999999999999999,
                               'simultaneous_announcements': 10},
                              {'name': 'BEPUL', 'price': 0, 'duration_time': 90, 'feedback_amount': 999999999999999999,
                               'simultaneous_announcements': 20}]

            await manager.execute(Tariff.insert_many(insert_tariffs))

    @staticmethod
    async def get_free_tariff(seller_entity):
        ic(seller_entity == 'natural', seller_entity == 'legal')
        simultaneous_announcements = None
        match seller_entity:
            case 'natural':
                simultaneous_announcements = 10
            case 'legal':
                simultaneous_announcements = 20

        if simultaneous_announcements:
            tariff = await manager.get_or_none(Tariff, name='BEPUL', simultaneous_announcements=simultaneous_announcements)
            ic(tariff)
            if not tariff:
                logging.error('[1/2]Продавцу %s не был найден тариф по simultaneous_announcements - %d',
                              seller_entity,
                              simultaneous_announcements)
            else:
                return tariff