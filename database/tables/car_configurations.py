import importlib
from abc import ABC
from datetime import datetime

from playhouse.postgres_ext import ArrayField

# from config_data.config import REGISTRATION_DATETIME_FORMAT
from database.db_connect import BaseModel
from database.tables.seller import Seller
from peewee import BigIntegerField, ForeignKeyField, BooleanField, TextField, CharField, DateTimeField
#
# safe_dict_class_module = importlib.import_module('')
# current_language = safe_dict_class_module.current_language

# class AttributeLanguageManager:
#     def __init__(self, language='ru'):
#         self.language = language
#
#     async def set_language(self, language):
#         self.language = language
#
# # clas(ABC):
#
#
# attribute_language_manager = AttributeLanguageManager()

class CarState(BaseModel):
    _name = CharField(unique=True, null=True)
    name_uz = CharField(unique=True, null=True)
    name_ru = CharField(unique=True, null=True)

    @property
    def name(self):
        from utils.safe_dict_class import current_language
        language_name = getattr(self, f'name_{current_language.get()}', None)
        return language_name if language_name else self._name

    @name.setter
    def name(self, new_value):
        self._name = new_value


class CarEngine(BaseModel):
    _name = CharField(unique=True, null=True)
    name_uz = CharField(unique=True, null=True)
    name_ru = CharField(unique=True, null=True)

    @property
    def name(self):
        from utils.safe_dict_class import current_language

        language_name = getattr(self, f'name_{current_language.get()}', None)
        return language_name if language_name else self._name


    @name.setter
    def name(self, new_value):
        self._name = new_value


class CarColor(BaseModel):
    _name = CharField(unique=True, null=True)
    name_uz = CharField(unique=False, null=True)
    name_ru = CharField(unique=True, null=True)

    @property
    def name(self):
        from utils.safe_dict_class import current_language
        language_name = getattr(self, f'name_{current_language.get()}', None)
        return language_name if language_name else self._name

    @name.setter
    def name(self, new_value):
        self._name = new_value

    # base_status = BooleanField(null=True)



class CarMileage(BaseModel):
    name = CharField(unique=True)

class CarYear(BaseModel):
    name = CharField(unique=True)


class CarBrand(BaseModel):
    name = CharField(unique=True)

class CarModel(BaseModel):
    brand = ForeignKeyField(CarBrand, backref='models')
    name = CharField()


class CarComplectation(BaseModel):
    model = ForeignKeyField(CarModel, backref='complectations')
    engine = ForeignKeyField(CarEngine, backref='complectations')
    _name = CharField(null=True)
    name_uz = CharField(null=True)
    name_ru = CharField(null=True)
    wired_state = ForeignKeyField(CarState, null=True)

    @property
    def name(self):
        from utils.safe_dict_class import current_language
        # ic(current_language.get())
        language_name = getattr(self, f'name_{current_language.get()}', None)
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


    # def __str__(self):
    #     return self.__class__.__name__
