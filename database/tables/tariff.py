import datetime

from peewee import CharField, ForeignKeyField, DateTimeField, BigIntegerField, BooleanField

from database.db_connect import BaseModel
from database.tables.seller import Seller


class Tariff(BaseModel):
    '''Таблица тарифов'''
    name = CharField()
    price = BigIntegerField()
    duration_time = BigIntegerField() # days
    feedback_amount = BigIntegerField()
    dying_status = BooleanField(null=True)

    class Meta:
        db_table = 'Тарифы'

class TariffsToSellers(BaseModel):
    seller = ForeignKeyField(Seller, field=Seller.telegram_id, backref='tariffs')
    tariff = ForeignKeyField(Tariff, backref='tariffs')
    start_date_time = DateTimeField()
    end_date_time = DateTimeField()
    residual_feedback = BigIntegerField()

    class Meta:
        db_table = 'Тарифы_Продавцы'


class DyingTariffs(BaseModel):
    tariff_wire = ForeignKeyField(TariffsToSellers, backref='dying_status')
    end_time = DateTimeField(default=datetime.datetime.now() + datetime.timedelta(days=1)) #days=1
                                                                                            #seconds=5

