import importlib

from utils.lexicon_utils.lexicon_uz.admin_lexicon_uz.catalog_lexicon_uz import catalog_mini_lexicon_uz
from utils.safe_dict_class import SafeDict, SmartGetattr

captions = {'backward': '◂ Назад ▸', 'was_selected': 'Вы выбрали', 'cancel': 'Отменить', 'confirm': 'Подтвердить',
            'sales': 'продажам', 'purchases': 'покупкам', 'any': 'всё время', 'day': 'день', 'week': 'неделю',
            'month': 'месяц', 'year': 'год', 'days': 'дней', 'feedbacks': 'откликов',
            'dont_write_html_tags': 'Запрещён ввод знаков "&lt; &gt;".',
            'all_users': 'всех', 'buyers': 'покупателей', 'sellers': 'продавцов', 'delete': 'Удалить',
            'by_dealership': 'автосалона',
            'by_seller': 'частного лица', 'close': 'Скрыть', 'surname_name_patronymic': 'ФИО: ', 'add': 'Добавить',
            'successfully': 'Успешно'
            }
pagination_interface = {'admin_pagination:-': '←', 'page_counter': '[{start}/{end}]', 'admin_pagination:+': '→'}
return_main_menu = {'return_main_menu': 'В меню'}

catalog_captions = {'catalog_review__make_block': 'блокировку', 'to_block': 'блокировки', 'to_delete': 'удаления',
                    'catalog_review__make_delete': 'удаление объявления', 'advert': '<b>Объявление:</b> <i>№{advert_id}</i>\n',
                    'inactive_advert_or_seller': 'Объявление или продавец неактивен',
                    'advert_successfully_closed': 'Автомобиль успешно снят с продажи!',
                    'empty': 'Раздел оказался пуст'
                    }

__CATALOG_LEXICON = {
    'search_advert_by_id_await_input': {'message_text': '<b>Введите ID искомого объявления: </b>',
                                        'buttons': {
                                            'admin_backward:await_input_id_to_search_advert': captions['backward'],
                                            **return_main_menu,
                                            'width': 1
    }},
    'search_advert_by_id_await_input(digit)': 'Ожидается ввод целочисленного значения для поиска объявления по ID:',
    'search_advert_by_id_await_input(not_exists)': 'Введённый ID объявления не существует.\nМожете ввести другой:',
    'start_catalog_menu': {'message_text': '<b>Вы перешли в каталог</b>\nВыберите ваше действие:', 'buttons': {
        'admin_catalog__advert_parameters': '⚙️ Параметры авто',
        'admin_catalog__car_catalog_review': '📋 Каталог авто',
        **return_main_menu,
        'width': 1
    }},
    'car_catalog_review_choose_category': {'message_text': '<b>Выберите тип просматриваемых объявлений:</b>', 'buttons': {
        'car_catalog_review__new': 'Новые',
        'car_catalog_review__viewed': 'Просмотренные',
        'search_by_id': 'Поиск по ID',
        'admin_backward:choose_catalog_review_advert_type': captions['backward'],
        'width': 2
    }},
    'review_specific_advert_catalog': {'message_text': '<b>Объявление:</b> <i>№{advert_id}</i>\n{seller_entity}:', 'buttons': {
        **pagination_interface,
        'admin_review_catalog_delete_advert': 'Ограничения',
        'admin_backward:review_specific_advert_catalog': captions['backward'],
        **return_main_menu,
        'width': 3
    }},
    'catalog__choose_specific_advert_action': {'message_text': '<b>Выберите тип нужного ограничения:</b>', 'buttons': {
        'catalog_action__delete_advert': 'Удалить объявление',
        'catalog_action__block_seller': 'Заблокировать продавца',
        'admin_backward:catalog__choose_specific_advert_action': captions['backward'],
        'width': 1
    }},
    'catalog_close_advert__input_reason': {'message_text': '<b>Введите причину {acton_subject}:</b>', 'buttons': {
        'admin_backward:input_reason_to_close_advert': captions['backward'],
        **return_main_menu,
        'width': 1
    }},
    'catalog_close_advert__confirmation_advert_close_action': {
        'message_text': '<b>Произвести {action_subject}</b>\n{seller_entity}\n{advert_caption}По причине:\n<b>{action_reason}</b>',
        'buttons': {'catalog_review__confirm_close_action': captions['confirm'],
                    'admin_backward:to_catalog_review_adverts': 'Вернуться к объявлениям',
                    'admin_backward:catalog_review_close_action_confirmation': captions['backward'],
                    **return_main_menu,
                    'width': 1}},
    'close_advert_seller_notification': {'message_text': 'Ваше объявление №{advert_id} было удалено администратором по причине: {close_reason}',
                                         'close_seller_notification_by_redis:close_advert': captions['close'],
                                         'width': 1}
}


catalog_mini_lexicon_ru = {
    'admin_review_catalog_choose_car_brand_message_text': '<b>Выберите марку машины для просмотра:</b>'
}



catalog_mini_lexicon = SafeDict({'ru': catalog_mini_lexicon_ru,
                                 'uz': catalog_mini_lexicon_uz})

class AdminReviewCatalogChooseCarBrand(SmartGetattr):
    def __init__(self):
        super().__init__()
        self.message_text = catalog_mini_lexicon['admin_review_catalog_choose_car_brand_message_text']  # Для русской версии
        self.buttons_callback_data = 'admin_catalog_review_brand:'
        self.dynamic_buttons = 2
        self.width = 1
        self.backward_command = {'admin_backward:catalog_review_choose_brand': captions['backward'], **return_main_menu}

AdminReviewCatalogChooseCarBrand = AdminReviewCatalogChooseCarBrand()