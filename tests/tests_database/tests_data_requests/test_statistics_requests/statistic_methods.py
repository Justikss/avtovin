from peewee import fn

from tests.tests_database.mock_tables import (Seller, CarBrand, CarComplectation, CarModel, CarColor, CarEngine,
                                              AdvertParameters, SellerFeedbacksHistory)

async def test_get_top_advert_parameters(manager, top_direction='top'):
    query = (SellerFeedbacksHistory
             .select(SellerFeedbacksHistory.advert_parameters,
                     # AdvertParameters,
                     # CarComplectation,
                     # CarModel,
                     # CarBrand,
                     # SellerFeedbacksHistory.seller_id,
                     fn.COUNT(SellerFeedbacksHistory.id).alias('feedbacks_count'),
                     Seller)
             .join(Seller, on=(SellerFeedbacksHistory.seller_id == Seller.telegram_id))
             .switch(SellerFeedbacksHistory)
             .join(AdvertParameters)
             .join(CarComplectation)
             .join(CarModel)
             .join(CarBrand)
             .where(SellerFeedbacksHistory.advert_parameters.is_null(False))
             .group_by(SellerFeedbacksHistory.advert_parameters, Seller)
             .order_by(fn.COUNT(SellerFeedbacksHistory.id).desc()))

    if top_direction == 'bottom':
        query = query.order_by(fn.COUNT(SellerFeedbacksHistory.id))

    top_10 = list(await manager.execute(query.limit(10)))
    ic(top_10, len(top_10))
    ic([model.__dict__ for model in top_10])
    return top_10
