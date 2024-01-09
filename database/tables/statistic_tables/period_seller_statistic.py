import importlib
from datetime import datetime, timedelta

from database.db_connect import manager
from database.tables.car_configurations import CarAdvert
from database.tables.seller import Seller
from database.tables.user import User


async def calculate_stats(period, seller_id=None):
    seller_feedbacks_history_module = importlib.import_module('database.tables.offers_history')
    # Определяем период для поиска
    now = datetime.now()
    if period == 'day':
        period_start = now - timedelta(days=1)
    elif period == 'week':
        period_start = now - timedelta(weeks=1)
    elif period == 'month':
        period_start = now - timedelta(days=30)
    elif period == 'year':
        period_start = now - timedelta(days=365)
    else:  # для 'all' не устанавливаем начальную дату
        period_start = None

    if not seller_id:
        users_query = User.select()
        sellers_query = Seller.select()
        advert_to_seller_query_condition = None
        feedbacks_to_seller_query_condition = None
    else:
        advert_to_seller_query_condition = CarAdvert.seller == seller_id
        feedbacks_to_seller_query_condition = seller_feedbacks_history_module.SellerFeedbacksHistory.seller_id == seller_id

    # Запросы к базе данных
    adverts_query = CarAdvert.select().where(advert_to_seller_query_condition)
    feedbacks_query = seller_feedbacks_history_module.SellerFeedbacksHistory.select().where(feedbacks_to_seller_query_condition)



    if period_start:
        adverts_query = adverts_query.where(CarAdvert.post_datetime >= period_start)
        feedbacks_query = feedbacks_query.where(seller_feedbacks_history_module.SellerFeedbacksHistory.feedback_time >= period_start)
        if not seller_id:
            users_query = users_query.where(User.data_registration >= period_start)
            sellers_query = sellers_query.where(Seller.data_registration >= period_start)

    # Выполнение асинхронных запросов
    adverts_count = await manager.count(adverts_query)
    feedbacks_count = await manager.count(feedbacks_query)

    result = {'advert': "{:,}".format(adverts_count), 'feedback': "{:,}".format(feedbacks_count)}
    if not seller_id:

        users_count = await manager.count(users_query)
        sellers_count = await manager.count(sellers_query)

        result.update({'user': "{:,}".format(users_count), 'seller': "{:,}".format(sellers_count),
                       'person': "{:,}".format(users_count + sellers_count)})


    return result