import peewee_async
from peewee import *
import asyncio
from database.db_connect import BaseModel
from database.tables.seller import Seller
from database.tables.user import User



class CarBrand(BaseModel):
    name = CharField(unique=True)

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

class CarModel(BaseModel):
    brand = ForeignKeyField(CarBrand, backref='models')
    name = CharField()


class CarComplectation(BaseModel):
    model = ForeignKeyField(CarModel, backref='complectations')
    name = CharField()


class CarAdvert(BaseModel):
    seller = ForeignKeyField(Seller, backref='adverts')
    complectation = ForeignKeyField(CarComplectation, backref='adverts')
    state = ForeignKeyField(CarState, backref='adverts')
    engine_type = ForeignKeyField(CarEngine, backref='adverts')
    price = BigIntegerField()


    color = ForeignKeyField(CarColor, backref='adverts', null=True)
    mileage = ForeignKeyField(CarMileage, backref='adverts', null=True)
    year = ForeignKeyField(CarYear, backref='adverts', null=True)

    additional_info = TextField(null=True)








