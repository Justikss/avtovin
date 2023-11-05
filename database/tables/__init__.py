from . import commodity, offers_history, seller, user, tariff
from .start_tables import db, BaseModel


try:
    db.create_tables(BaseModel.__subclasses__(), safe=True)
    print('Таблицы успешно созданы')
except Exception as ex:
    print('Ошибочка при создании таблиц: {}, {}'.format(ex, type(ex)))

db.close()
