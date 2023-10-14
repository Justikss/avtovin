from .start_tables import BaseModel

class Seller(BaseModel):
    '''Таблица продавцов(селлеры/автосалоны)'''

    class Meta:
        db_table = 'Продавцы'
