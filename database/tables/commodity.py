from .start_tables import BaseModel
from peewee import CharField, IntegerField

class Commodity(BaseModel):
    '''Таблица товаров.
    mileage = Числовое поле.'''
    brand = CharField()
    model = CharField()
    engine_type = CharField()
    year_of_release = CharField()
    complectation = CharField()
    mileage = IntegerField()
    state = CharField()
    color = CharField()
    photo_url = CharField()

    class Meta:
        db_table = 'Автомобили на продаже'


