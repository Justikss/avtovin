from data_requests.commodity_requests import CommodityRequester
from tables.start_tables import db, BaseModel
from data_requests.user_requests import UserRequester

'''Примеры словарей для записи в таблицу через CommodityRequester
key: value
название столбца как в tables.py: значение маленькими буквами(ловеркейсом)
'''
# toyota = {
# 'car_brand': 'toyota',
# 'model': 'supra',
# 'mileage': 1000000,
# 'commodity_state': 'Б/У',
# 'color': 'red'
# }
#
# bmw = {
# 'car_brand': 'bmw',
# 'model': 'x5',
# 'mileage': 20,
# 'commodity_state': 'новая',
# 'color': 'black'
# }
#
# reno = {
# 'car_brand': 'renault',
# 'model': 'logan',
# 'mileage': 123,
# 'commodity_state': 'новая',
# 'color': 'pink',
# }
#
#
# kamaz = {
# 'car_brand': 'kamaz',
# 'model': 'big',
# 'mileage': 0,
# 'commodity_state': 'новая',
# 'color': 'orange'
# }

# new_cars = [kamaz, toyota, bmw, reno]

# a = CommodityRequester.store_data(new_cars)
color_cars = CommodityRequester.get_where_color('pink')
# print(a)
for car in color_cars:
    print(car.color, car.model)


user = {

'name': 'kesha',
'surname': 'meshev',
'patronymic': 'Afakeshovich',
'phone_number': 1212
}

UserRequester.store_data(user)