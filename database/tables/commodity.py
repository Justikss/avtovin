from .start_tables import BaseModel
from peewee import CharField, IntegerField

class Commodity(BaseModel):
    '''Таблица товаров.
    mileage = Числовое поле.'''
    car_brand = CharField()
    model = CharField()
    mileage = IntegerField()
    commodity_state = CharField()
    color = CharField()

    class Meta:
        db_table = 'Автомобили на продаже'
