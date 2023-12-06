import peewee_async
from peewee import *
import asyncio
from database.db_connect import BaseModel
from database.tables.seller import Seller
from database.tables.user import User


class CarState(BaseModel):
    name = CharField(unique=True)

class CarEngine(BaseModel):
    name = CharField(unique=True)

class CarColor(BaseModel):
    name = CharField(unique=True)

class CarMileage(BaseModel):
    name = CharField(unique=True)

class CarYear(BaseModel):
    name = CharField(unique=True)

# class ModelCharacteristic(BaseModel):
#     model = ForeignKeyField(Model, backref='characteristics')
#     characteristic = ForeignKeyField(Characteristic, backref='models')
#     value = CharField()

class CarBrand(BaseModel):
    name = CharField(unique=True)

class CarModel(BaseModel):
    brand = ForeignKeyField(CarBrand, backref='models')
    name = CharField()


class CarComplectation(BaseModel):
    model = ForeignKeyField(CarModel, backref='complectations')
    engine = ForeignKeyField(CarEngine, backref='complectations')
    name = CharField()


class CarAdvert(BaseModel):
    seller = ForeignKeyField(Seller, field=Seller.telegram_id, backref='adverts')
    complectation = ForeignKeyField(CarComplectation, backref='adverts')
    state = ForeignKeyField(CarState, backref='adverts')
    engine_type = ForeignKeyField(CarEngine, backref='adverts')
    color = ForeignKeyField(CarColor, backref='adverts')
    price = CharField()

    mileage = ForeignKeyField(CarMileage, backref='adverts', null=True)
    year = ForeignKeyField(CarYear, backref='adverts', null=True)

    additional_info = TextField(null=True)



