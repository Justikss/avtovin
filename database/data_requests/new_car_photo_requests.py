from typing import List, Union, Optional
from icecream import install, ic

from database.tables.commodity import NewCarPhotoBase
from database.tables.commodity import Commodity, CommodityPhotos
from database.tables.start_tables import db
from utils.Lexicon import LexiconCommodityLoader

install()


class PhotoRequester:
    @staticmethod
    async def load_photo_in_base(photo_data: List[dict]):
        '''Установка фотографий для новых машин.
        :photo_data[dict]: admin_id, car_brand, car_model, photo_id, photo_unique_id
        '''
        ic()
        ic(photo_data)
        if 3 > len(photo_data) > 5:
            raise ValueError('фотографий должно быть от трёх до пяти(включительно)')
        with db.atomic():
            # Вставка данных о фотографиях
            ic(photo_data[0]['car_brand'], photo_data[0]['car_model'])
            car_brand = photo_data[0]['car_brand']
            car_model = photo_data[0]['car_model']
            select_photo_base_response = list(NewCarPhotoBase.select().where(
                (NewCarPhotoBase.car_brand == car_brand) & (NewCarPhotoBase.car_model == car_model)
            ))
            ic(select_photo_base_response)
            if select_photo_base_response:
                raise BufferError('Фотографии на эту конфигурацию уже загружены.')
            else:
                NewCarPhotoBase.insert_many(photo_data).execute()

            # Предполагаем, что все фотографии относятся к одному виду машины
            sample_photo = photo_data[0]
            brand, model = sample_photo['car_brand'], sample_photo['car_model']

            commodity_photos_subquery = [photo_model.car_id.car_id for photo_model in CommodityPhotos.select(CommodityPhotos.car_id)]
            ic(commodity_photos_subquery)
            # Находим автомобили, соответствующие критериям
            commodity_query = (Commodity
                               .select()
                               .where((Commodity.brand == brand) &
                                      (Commodity.model == model) &
                                      (Commodity.state == 'Новое') &
                                      Commodity.car_id not in commodity_photos_subquery))

            # Собираем данные для массовой вставки
            insert_data = []
            for car in commodity_query:
                for photo in photo_data:
                    insert_data.append({
                        'car_id': car.car_id,
                        'photo_id': photo['photo_id'],
                        'photo_unique_id': photo['photo_unique_id']
                    })

            # Массовая вставка фотографий для каждого автомобиля
            if insert_data:
                insert_response = CommodityPhotos.insert_many(insert_data).execute()

                ic(insert_response)

    @staticmethod
    async def try_get_photo(car_data: dict) -> Optional[list]:
        '''Попытка подобрать фотографии для новой заявки на Новый автомобиль
        :car_data[dict]: brand, model
        '''

        brand = LexiconCommodityLoader.load_commodity_brand['buttons'][car_data['brand']]
        model = LexiconCommodityLoader.load_commodity_model['buttons'][car_data['model']]
        ic(brand, model)
        # correct_data = []
        # for parameter in (brand, model):
        #     correct_data.append(parameter if not parameter.startswith('load') else parameter.replace('load_', ''))
        # ic(correct_data)
        with db.atomic():
            select_response = list(NewCarPhotoBase.select().where((NewCarPhotoBase.car_brand == brand) &
                                                              (NewCarPhotoBase.car_model == model)))
            ic(select_response)
            if select_response:
                result = list()
                for data_pack in select_response:
                    result.append({'id': data_pack.photo_id, 'unique_id': data_pack.photo_unique_id})
                ic(result)
                return result
            else:
                return None
