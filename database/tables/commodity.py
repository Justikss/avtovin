from database.db_connect import BaseModel
from peewee import CharField, ForeignKeyField, BigIntegerField

from database.tables.car_configurations import CarAdvert, CarComplectation, CarEngine, CarColor, CarState
    # CarComplectationsToState


class AdvertPhotos(BaseModel):
    car_id = ForeignKeyField(CarAdvert, field=CarAdvert.id, backref='car_id')
    photo_id = CharField()
    photo_unique_id = CharField()

    class Meta:
        db_table = 'Фотографии_Машин'


class NewCarPhotoBase(BaseModel):
    car_complectation = ForeignKeyField(CarComplectation)
    car_color = ForeignKeyField(CarColor)
    photo_id = CharField()
    photo_unique_id = CharField()
    admin_id = BigIntegerField()


    class Meta:
        db_table = 'Фотографии_Новых_Машин'