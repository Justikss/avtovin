from peewee import CharField, IntegerField, ForeignKeyField, DateTimeField

from database.db_connect import BaseModel
from database.tables.seller import Seller


class Tariff(BaseModel):
    '''Таблица тафрифов'''
    name = CharField(unique=True)
    price = IntegerField()
    duration_time = IntegerField() # days
    feedback_amount = IntegerField()

    class Meta:
        db_table = 'Тарифы'

class TariffsToSellers(BaseModel):
    seller = ForeignKeyField(Seller, field=Seller.telegram_id, backref='tariffs')
    tariff = ForeignKeyField(Tariff, backref='tariffs')
    start_date_time = DateTimeField()
    end_date_time = DateTimeField()
    residual_feedback = IntegerField()

    class Meta:
        db_table = 'Тарифы_Продавцы'