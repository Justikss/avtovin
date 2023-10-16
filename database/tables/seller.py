from peewee import IntegerField, CharField

from .start_tables import BaseModel

class Seller(BaseModel):
    '''Таблица продавцов(селлеры/автосалоны)'''
    telegram_id = IntegerField(primary_key=True)
    phone_number = CharField(unique=True)
    entity = CharField(verbose_name='Лицо')
    dealship_address = CharField(null=True, verbose_name='Адрес салона')
    name = CharField(null=True, verbose_name='Имя')  # поле ограничено символами(название столбца)
    surname = CharField(null=True, verbose_name='Фамилия')  # поле ограничено символами(возможно нулевое значение, название столбца)
    patronymic = CharField(null=True, verbose_name='Отчество')

    class Meta:
        db_table = 'Продавцы'
