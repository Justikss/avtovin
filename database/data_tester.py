
from tables.start_tables import BaseModel
from data_requests.person_requests import PersonRequester

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

# PersonRequester.store_data(user)