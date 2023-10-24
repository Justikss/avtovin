from .start_tables import BaseModel
from peewee import CharField, IntegerField, ForeignKeyField, PrimaryKeyField, AutoField
from database.tables.seller import Seller


class Commodity(BaseModel):
    '''Таблица товаров.
    mileage = Числовое поле.'''
    car_id = PrimaryKeyField()
    seller_id = ForeignKeyField(Seller, backref='commodities') #вставляется модель селлера
    brand = CharField()
    model = CharField()
    engine_type = CharField()
    year_of_release = CharField(null=True)
    complectation = CharField(null=True)
    mileage = IntegerField(null=True)
    state = CharField()
    color = CharField(null=True)
    photo_url = CharField()
    price = IntegerField()


    class Meta:
        db_table = 'Автомобили'


