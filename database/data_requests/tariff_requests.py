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
        except Exception as ex:
            logging.critical('')
            traceback.print_exc()
            print(ex)
            return False

    @staticmethod
    async def get_by_id(tariff_id):
        '''Асинхронный метод получения тарифа по ID'''
        if not isinstance(tariff_id, int):
            tariff_id = int(tariff_id)
        try:
            tariff = await manager.get(Tariff, ((Tariff.id == tariff_id) & ((Tariff.dying_status == False) | (Tariff.dying_status.is_null(True)))))
        except:
            tariff = None
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

# TarifRequester.set_tariff(data)
# TarifRequester.set_tariff(data3)
# TarifRequester.set_tariff(data2)
