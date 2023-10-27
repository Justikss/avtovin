import sqlite3

from database.tables.offers_history import ActiveOffers, ActiveOffersToCars
from database.tables.start_tables import db
from database.data_requests.commodity_requests import CommodityRequester, Commodity
from database.data_requests.person_requests import PersonRequester
from typing import List, Union



class OffersRequester:
    @staticmethod
    async def get_wire_by_offer_id(active_offer_id):
        with db.atomic():
            select_request = ActiveOffersToCars.select().where(ActiveOffersToCars.offer_id == active_offer_id)
            select_request = list(select_request)
            if select_request:
                return select_request
            else:
                return False


    @staticmethod
    async def store_data(seller_id, buyer_id, cars: list, db=db):

        # try:
        with db.atomic():
            seller = PersonRequester.get_user_for_id(user_id=seller_id, seller=True)
            buyer = PersonRequester.get_user_for_id(user_id=buyer_id, user=True)

            # Создать новый заказ с продавцом и покупателем
            print(seller, buyer)
            order = ActiveOffers.create(seller=seller[0], buyer=buyer[0])

            # Для каждой машины в списке
            for car in cars:
                # Найти машину по ее id
                car = Commodity.get_by_id(car)
                print('car: ', type(car), 'order: ', type(order))
                # Создать связь между машиной и заказом
                # data = 'car': car, 'offer': offer
                # ActiveOffersToCars.insert(**data).execute()
                ActiveOffersToCars.create(car_id=car, offer_id=order)


            # Вернуть id созданного заказа
            return order.id

            # car_models = CommodityRequester.retrieve_all_data()
           # print(car_models)




                #     print(car_model)
                #     load_pattern.append({'car_id': car_model, 'offer_id': offer_model})
                # print(load_pattern)
                #
                # ActiveOffersToCars.insert_many(load_pattern).execute()
                # ActiveOffers.create(**data)
        # except Exception as ex:
        #     print('db except:', ex)
        #     return False

    @staticmethod
    async def get_for_buyer_id(buyer_id: int):
        with db.atomic():
            buyer_offers = ActiveOffers.select().where(ActiveOffers.buyer == buyer_id)
            buyer_offers = list(buyer_offers)
        if buyer_offers:
            return buyer_offers
        else:
            return False

    @staticmethod
    async def match_check(user_id, cars_id_range) -> Union[List[str], bool]:
        '''Проверка на наличие таких же автомобилей в покупках'''
        # cars_id_range = [str(car_id) for car_id in cars_id_range]
        active_offers = await OffersRequester.get_for_buyer_id(buyer_id=user_id)
        matched = list()
        if not active_offers:
            return cars_id_range
        for offer in active_offers:
            related_strings = await OffersRequester.get_wire_by_offer_id(offer.id)
            for related_string in related_strings:
                if str(related_string.car_id) in cars_id_range:
                    matched.append(str(related_string.car_id))
        
        print('cars', cars_id_range)
        print('matched', matched)
        if len(matched) == len(cars_id_range):
            return False
        elif len(matched) != 0 and len(matched) < len(cars_id_range):
            alive_cars = set(cars_id_range).symmetric_difference(set(matched))
            return alive_cars
        elif len(matched) == 0:
            return cars_id_range

    