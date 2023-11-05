from peewee import CharField, IntegerField, ForeignKeyField, DateTimeField

from .start_tables import BaseModel
from database.tables.seller import Seller


class Tariff(BaseModel):
    '''Таблица тафрифов'''
    name = CharField(unique=True)
    price = IntegerField()
    duration_time = DateTimeField() # days, hours
    feedback_amount = IntegerField()

    class Meta:
        db_table = 'Тарифы'

class TariffsToSellers(BaseModel):
    seller = ForeignKeyField(Seller, backref='seller')
    tariff = ForeignKeyField(Tariff, backref='tariff')
    start_date_time = DateTimeField()
    end_date_time = DateTimeField()
    residual_feedback = IntegerField()

    class Meta:
        db_table = 'Тарифы-Продавцы'