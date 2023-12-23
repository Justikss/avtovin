import importlib
from datetime import datetime, timedelta

from database.db_connect import manager
from database.tables.car_configurations import CarAdvert


async def calculate_stats(seller_id, period):
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

    # Запросы к базе данных
    adverts_query = CarAdvert.select().where(CarAdvert.seller == seller_id)
    feedbacks_query = seller_feedbacks_history_module.SellerFeedbacksHistory.select().where(seller_feedbacks_history_module.SellerFeedbacksHistory.seller_id == seller_id)

    if period_start:
        adverts_query = adverts_query.where(CarAdvert.post_datetime >= period_start)
        feedbacks_query = feedbacks_query.where(seller_feedbacks_history_module.SellerFeedbacksHistory.feedback_time >= period_start)

    # Выполнение асинхронных запросов
    adverts_count = await manager.count(adverts_query)
    feedbacks_count = await manager.count(feedbacks_query)

    return adverts_count, feedbacks_count