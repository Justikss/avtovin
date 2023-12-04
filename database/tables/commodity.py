from database.db_connect import BaseModel
from peewee import CharField, IntegerField, ForeignKeyField, PrimaryKeyField, AutoField, BigIntegerField

from database.tables.car_configurations import CarAdvert, CarBrand, CarModel, CarComplectation, CarEngine
from database.tables.seller import Seller


# class Commodity(BaseModel):
#     '''Таблица товаров.
#     mileage = Числовое поле.'''
#     car_id = PrimaryKeyField()
#     seller_id = ForeignKeyField(Seller, backref='cars') #вставляется модель селлера
#     brand = CharField()
#     model = CharField()
#     engine_type = CharField()
#     year_of_release = CharField(null=True)
#     complectation = CharField()
#     mileage = IntegerField(null=True)
#     state = CharField()
#     color = CharField(null=True)
#     price = IntegerField()
#
#     class Meta:
#         db_table = 'Автомобили'


class AdvertPhotos(BaseModel):
    car_id = ForeignKeyField(CarAdvert, field=CarAdvert.id, backref='car_id')
    photo_id = CharField()
    photo_unique_id = CharField()

    class Meta:
        db_table = 'Фотографии_Машин'


class NewCarPhotoBase(BaseModel):
    car_complectation = ForeignKeyField(CarComplectation)
    car_engine = ForeignKeyField(CarEngine)
    photo_id = CharField()
    photo_unique_id = CharField()
    admin_id = BigIntegerField()

    class Meta:
        db_table = 'Фотографии_Новых_Машин'