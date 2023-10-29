from peewee import IntegerField, CharField, BooleanField

from .start_tables import BaseModel

class Seller(BaseModel):
    '''Таблица продавцов(селлеры/автосалоны)'''
    telegram_id = IntegerField(primary_key=True, verbose_name='Телеграм ID')
    phone_number = CharField(unique=True, verbose_name='Номер телефона')
    dealship_name = CharField(null=True, verbose_name='Название автосалона')
    entity = CharField(verbose_name='Лицо')
    dealship_address = CharField(null=True, verbose_name='Адрес салона')
    name = CharField(null=True, verbose_name='Имя')  # поле ограничено символами(название столбца)
    surname = CharField(null=True, verbose_name='Фамилия')  # поле ограничено символами(возможно нулевое значение, название столбца)
    patronymic = CharField(null=True, verbose_name='Отчество')
    authorized = BooleanField(verbose_name='Наличие авторизации.')

    class Meta:
        db_table = 'Продавцы'

