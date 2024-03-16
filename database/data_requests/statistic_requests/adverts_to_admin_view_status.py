
from database.db_connect import manager
from database.tables.car_configurations import CarAdvert, CarComplectation, CarModel, CarBrand
from database.tables.statistic_tables.advert_to_admin_view_status import AdvertsToAdminViewStatus

class AdvertsToAdminViewStatusRequester:
    def __init__(self):
        self.table = AdvertsToAdminViewStatus

    async def retrieve_by_view_status(self, status: bool, get_brands=False, get_by_brand=False):
        ic(status)
        query = (self.table.select(CarAdvert.id)
                 .join(CarAdvert)
                 .where(AdvertsToAdminViewStatus.view_status == status))

        query = query.where((CarAdvert.sleep_status == False) | (CarAdvert.sleep_status.is_null(True)))

        if get_brands:
            query = (CarBrand.select(CarBrand).join(CarModel).join(CarComplectation)
                                                .join(CarAdvert).where(CarAdvert.id.in_(query)).distinct())
        elif get_by_brand:
            query = (query
                     .join(CarComplectation)
                     .join(CarModel)
                     .join(CarBrand)
                     .where(CarBrand.id == get_by_brand))

        result = list(await manager.execute(query))

        if get_by_brand and result:
            result = [advert_relate.advert.id for advert_relate in result]

        return result



    async def activate_view_status(self, advert_id):
        if not isinstance(advert_id, (int, CarAdvert)):
            advert_id = int(advert_id)
        await manager.execute(self.table.update(view_status=True).where(self.table.advert == advert_id))

    async def create_relation(self, advert_id):
        await manager.create(self.table, advert=advert_id)

    async def delete_relation(self, advert_id):
        if not isinstance(advert_id, list):
            condition = self.table.advert == advert_id
        else:
            condition = self.table.advert.in_(advert_id)

        await manager.execute(self.table.delete().where(condition))


advert_to_admin_view_related_requester = AdvertsToAdminViewStatusRequester()