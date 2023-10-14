from data_requests.commodity_requests import CommodityRequester
from tables.start_tables import db, BaseModel
from data_requests.user_requests import UserRequester

'''Примеры словарей для записи в таблицу через CommodityRequester
key: value
название столбца как в tables.py: значение маленькими буквами(ловеркейсом)
'''


# print(a)


user = {

'name': 'kesha',
'surname': 'meshev',
'patronymic': 'Afakeshovich',
'phone_number': 1212
}

UserRequester.store_data(user)