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

