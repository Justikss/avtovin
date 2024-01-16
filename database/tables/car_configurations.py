from datetime import datetime

# from config_data.config import REGISTRATION_DATETIME_FORMAT
from database.db_connect import BaseModel
from database.tables.seller import Seller
from peewee import BigIntegerField, ForeignKeyField, BooleanField, TextField, CharField, DateTimeField
class AttributeLanguageManager:
    def __init__(self, language='ru'):
        self.language = language

    async def set_language(self, language):
        self.language = language



attribute_language_manager = AttributeLanguageManager()

class CarState(BaseModel):
    name = CharField(unique=True)

class CarEngine(BaseModel):
    name = CharField(unique=True)

class CarColor(BaseModel):
    _name = CharField(unique=True, null=True)
    name_uz = CharField(unique=True, null=True)
    name_ru = CharField(unique=True, null=True)
    # base_status = BooleanField(null=True)

    @property
    def name(self):
        language_name = self.__dict__.get(f'_CarColor__name_{attribute_language_manager.language}')
        return language_name if language_name else self._name

    @name.setter
    def name(self, new_value):
        self._name = new_value


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
    _name = CharField(unique=True, null=True)
    name_uz = CharField(unique=True, null=True)
    name_ru = CharField(unique=True, null=True)

    @property
    def name(self):
        language_name = self.__dict__.get(f'_CarComplectation__name_{attribute_language_manager.language}')
        return language_name if language_name else self._name

    @name.setter
    def name(self, new_value):
        self._name = new_value


class CarAdvert(BaseModel):
    seller = ForeignKeyField(Seller, field=Seller.telegram_id, backref='adverts')
    complectation = ForeignKeyField(CarComplectation, backref='adverts')
    state = ForeignKeyField(CarState, backref='adverts')
    sum_price = BigIntegerField(null=True)
    dollar_price = BigIntegerField(null=True)

    color = ForeignKeyField(CarColor, backref='adverts', null=True)
    mileage = ForeignKeyField(CarMileage, backref='adverts', null=True)
    year = ForeignKeyField(CarYear, backref='adverts', null=True)

    sleep_status = BooleanField(null=True)

    additional_info = TextField(null=True)
    post_datetime = DateTimeField(default=datetime.now().strftime('%d-%m-%Y'))


