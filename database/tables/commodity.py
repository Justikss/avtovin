from .start_tables import BaseModel
from peewee import CharField, IntegerField, ForeignKeyField, PrimaryKeyField, AutoField
from database.tables.seller import Seller


class Commodity(BaseModel):
    '''Таблица товаров.
    mileage = Числовое поле.'''
    car_id = PrimaryKeyField()
    seller_id = ForeignKeyField(Seller, backref='cars') #вставляется модель селлера
    brand = CharField()
    model = CharField()
    engine_type = CharField()
    year_of_release = CharField(null=True)
    complectation = CharField()
    mileage = IntegerField(null=True)
    state = CharField()
    color = CharField(null=True)
    price = IntegerField()

    class Meta:
        db_table = 'Автомобили'


class CommodityPhotos(BaseModel):
    car_id = ForeignKeyField(Commodity, backref='car_id')
    photo_id = CharField()
    photo_unique_id = CharField()

    class Meta:
        db_table = 'Фотографии_автомобилей'


class NewCarPhotoBase(BaseModel):
    car_brand = CharField()
    car_model = CharField()
    photo_id = CharField()
    photo_unique_id = CharField()
    admin_id = CharField()

    class Meta:
        db_table = 'Фотографии_новых_машин'