from database.tables.offers_history import ActiveOffers
from database.tables.start_tables import db


class OffersRequester:
    @staticmethod
    def store_data(data: dict):
        try:
            with db.atomic():
                ActiveOffers.create(**data)
                return True
        except Exception:
            return False

    @staticmethod
    def get_for_buyer_id(buyer_id: int):
        with db.atomic():
            buyer_offers = ActiveOffers.select().where(ActiveOffers.buyer == buyer_id)
            buyer_offers = list(buyer_offers)
        if buyer_offers:
            return buyer_offers
        else:
            return False