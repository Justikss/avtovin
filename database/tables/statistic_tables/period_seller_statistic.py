import importlib
from datetime import datetime, timedelta

from database.db_connect import manager
from database.tables.car_configurations import CarAdvert
from database.tables.seller import Seller
from database.tables.user import User


async def calculate_stats(period, seller_id=None):
    from database.data_requests.utils.raw_sql_handler import execute_raw_sql

    # Определение начала периода
    now = datetime.now()
    period_start = {
        'day': now - timedelta(days=1),
        'week': now - timedelta(weeks=1),
        'month': now - timedelta(days=30),
        'year': now - timedelta(days=365),
    }.get(period, None)

    # Условия для временного периода
    period_start_condition = f"'{period_start.strftime('%Y-%m-%d %H:%M:%S')}'" if period_start else "NULL"
    user_seller_period_condition = f"WHERE {'{date_field}'} >= {period_start_condition} AND" if period_start else "WHERE"

    # Условие для seller_id
    seller_condition = f"WHERE seller_id = {seller_id}" if seller_id else "WHERE TRUE"

    sql_query_base = f"""
        SELECT
            (SELECT COUNT(*) FROM CarAdvert {seller_condition} {f'AND post_datetime >= {period_start_condition}' if period_start else ''}) AS advert_count,
            (SELECT COUNT(*) FROM SellerFeedbacksHistory {seller_condition} {f'AND feedback_time >= {period_start_condition}' if period_start else ''}) AS feedback_count
    """

    # Дополнительная часть SQL запроса для случая, когда seller_id не задан
    sql_query_extra = f""",
            (SELECT COUNT(*) FROM "Пользователи" {user_seller_period_condition.format(date_field='data_registration')} is_banned = FALSE) AS active_users_count,
            (SELECT COUNT(*) FROM "Продавцы" {user_seller_period_condition.format(date_field='data_registration')} is_banned = FALSE) AS active_sellers_count,
            (SELECT COUNT(*) FROM "Пользователи" {user_seller_period_condition.format(date_field='block_date')} is_banned = TRUE) AS blocked_users_count,
            (SELECT COUNT(*) FROM "Продавцы" {user_seller_period_condition.format(date_field='block_date')} is_banned = TRUE) AS blocked_sellers_count
    """ if not seller_id else ""

    # Формирование окончательного SQL запроса
    sql_query = sql_query_base + sql_query_extra

    # Выполнение запроса
    result_row = await execute_raw_sql(sql_query)

    # Формирование результатов с учетом условий по seller_id
    result = {
        'advert': result_row[0],
        'feedback': result_row[1],
    }
    # Дополнительные вычисления
    if not seller_id:
        result.update({
            'person': result_row[2] + result_row[3],
            'block_users': result_row[4] + result_row[5],

            'user': result_row[2],
            'seller': result_row[3],
            'block_buyers': result_row[4],
            'block_sellers': result_row[5],
        })

    # Форматирование результатов
    formatted_result = {key: "{:,}".format(value) for key, value in result.items()}

    return formatted_result

# async def calculate_stats(period, seller_id=None):
#     seller_feedbacks_history_module = importlib.import_module('database.tables.offers_history')
#     # Определяем период для поиска
#     now = datetime.now()
#     if period == 'day':
#         period_start = now - timedelta(days=1)
#     elif period == 'week':
#         period_start = now - timedelta(weeks=1)
#     elif period == 'month':
#         period_start = now - timedelta(days=30)
#     elif period == 'year':
#         period_start = now - timedelta(days=365)
#     else:  # для 'all' не устанавливаем начальную дату
#         period_start = None
#
#     if not seller_id:
#         users_query = User.select()
#         sellers_query = Seller.select()
#         advert_to_seller_query_condition = None
#         feedbacks_to_seller_query_condition = None
#     else:
#         advert_to_seller_query_condition = CarAdvert.seller == seller_id
#         feedbacks_to_seller_query_condition = seller_feedbacks_history_module.SellerFeedbacksHistory.seller_id == seller_id
#
#     # Запросы к базе данных
#     adverts_query = CarAdvert.select().where(advert_to_seller_query_condition)
#     feedbacks_query = seller_feedbacks_history_module.SellerFeedbacksHistory.select().where(feedbacks_to_seller_query_condition)
#
#     ic(period_start, seller_id)
#
#     if period_start:
#         adverts_query = adverts_query.where(CarAdvert.post_datetime >= period_start)
#         feedbacks_query = feedbacks_query.where(seller_feedbacks_history_module.SellerFeedbacksHistory.feedback_time >= period_start)
#         if not seller_id:
#             users_query = users_query.where(User.data_registration >= period_start)
#             sellers_query = sellers_query.where(Seller.data_registration >= period_start)
#
#     # Выполнение асинхронных запросов
#     adverts_count = await manager.count(adverts_query)
#     feedbacks_count = await manager.count(feedbacks_query)
#
#     result = {'advert': adverts_count, 'feedback': feedbacks_count}
#     if not seller_id:
#         blocked_users = users_query.where(User.is_banned == True)
#         blocked_sellers = sellers_query.where(Seller.is_banned == True)
#         users_query = users_query.where(User.is_banned == False)
#         sellers_query = sellers_query.where(Seller.is_banned == False)
#
#         users_count = await manager.count(users_query)
#         sellers_count = await manager.count(sellers_query)
#         blocked_sellers = await manager.count(blocked_sellers)
#         blocked_buyers = await manager.count(blocked_users)
#
#         result.update({'user': users_count, 'seller': sellers_count,
#                        'person': users_count + sellers_count,
#                        'block_users': blocked_buyers + blocked_sellers,
#                        'block_buyers': blocked_buyers, 'block_sellers': blocked_sellers})
#
#     foramtted_result = dict()
#     for key, value in result.items():
#         foramtted_result[key] = "{:,}".format(value)
#
#     return foramtted_result