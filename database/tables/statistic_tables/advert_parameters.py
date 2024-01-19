from peewee import ForeignKeyField, SQL

from database.db_connect import BaseModel
from database.tables.car_configurations import CarComplectation, CarState, CarEngine, CarColor, CarMileage, CarYear


class AdvertParameters(BaseModel):
    complectation = ForeignKeyField(CarComplectation, backref='parameters')
    color = ForeignKeyField(CarColor, backref='parameters')

    class Meta:
        constraints = [SQL('UNIQUE (complectation_id, color_id)')]

