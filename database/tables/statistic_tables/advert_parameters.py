from peewee import ForeignKeyField

from database.db_connect import BaseModel
from database.tables.car_configurations import CarComplectation, CarState, CarEngine, CarColor, CarMileage, CarYear


class AdvertParameters(BaseModel):
    complectation = ForeignKeyField(CarComplectation, backref='parameters')
    state = ForeignKeyField(CarState, backref='parameters')
    color = ForeignKeyField(CarColor, backref='parameters')
