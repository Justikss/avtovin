from peewee import ForeignKeyField, BooleanField

from database.db_connect import BaseModel
from database.tables.car_configurations import CarAdvert


class AdvertsToAdminViewStatus(BaseModel):
    advert = ForeignKeyField(CarAdvert, backref='admin_view_status')
    view_status = BooleanField(default=False)
    