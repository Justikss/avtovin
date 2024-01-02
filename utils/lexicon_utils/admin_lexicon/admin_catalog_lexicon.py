from utils.lexicon_utils.admin_lexicon.admin_lexicon import return_main_menu, captions, pagination_interface

catalog_captions = {'catalog_review__make_block': 'блокировку', 'to_block': 'блокировки', 'to_delete': 'удаления',
                    'catalog_review__make_delete': 'удаление объявления', 'advert': 'Объявление: №{advert_id}\n',
                    'inactive_advert_or_seller': 'Объявление или продавец неактивен',
                    'advert_successfully_closed': 'Автомобиль успешно снят с продажи!'
                    }

__CATALOG_LEXICON = {
    'search_advert_by_id_await_input': {'message_text': 'Введите ID искомого объявления: ',
                                        'buttons': {
                                            'admin_backward:await_input_id_to_search_advert': captions['backward'],
                                            **return_main_menu,
                                            'width': 1
    }},
    'search_advert_by_id_await_input(digit)': 'Ожидается ввод целочисленного значения для поиска объявления по ID:',
    'search_advert_by_id_await_input(not_exists)': 'Введённый ID объявления не существует.\nМожете ввести другой:',
    'start_catalog_menu': {'message_text': 'Каталог\nВыберите действие:', 'buttons': {
        'admin_catalog__advert_parameters': 'Параметры авто',
        'admin_catalog__car_catalog_review': 'Каталог авто',
        **return_main_menu,
        'width': 1
    }},
    'car_catalog_review_choose_category': {'message_text': 'Выберите тип просматриваемых объявлений:', 'buttons': {
        'car_catalog_review__new': 'Новые',
        'car_catalog_review__viewed': 'Просмотренные',
        'search_by_id': 'Поиск по ID',
        'admin_backward:choose_catalog_review_advert_type': captions['backward'],
        'width': 2
    }},
    'review_specific_advert_catalog': {'message_text': 'Объявление: №{advert_id}\n{seller_entity}:', 'buttons': {
        **pagination_interface,
        'admin_review_catalog_delete_advert': 'Санкции',
        'admin_backward:review_specific_advert_catalog': captions['backward'],
        **return_main_menu,
        'width': 3
    }},
    'catalog__choose_specific_advert_action': {'message_text': 'Выберите конкретное действие:', 'buttons': {
        'catalog_action__delete_advert': 'Удалить объявление',
        'catalog_action__block_seller': 'Заблокировать продавца',
        'admin_backward:catalog__choose_specific_advert_action': captions['backward'],
        'width': 1
    }},
    'catalog_close_advert__input_reason': {'message_text': 'Введите причину {acton_subject}:', 'buttons': {
        'admin_backward:input_reason_to_close_advert': captions['backward'],
        **return_main_menu,
        'width': 1
    }},
    'catalog_close_advert__confirmation_advert_close_action': {
        'message_text': 'Произвести {action_subject}\n{seller_entity}\n{advert_caption}По причине:\n{action_reason}',
        'buttons': {'catalog_review__confirm_close_action': captions['confirm'],
                    'admin_backward:to_catalog_review_adverts': 'Вернуться к объявлениям',
                    'admin_backward:catalog_review_close_action_confirmation': captions['backward'],
                    **return_main_menu,
                    'width': 1}},
    'close_advert_seller_notification': {'message_text': 'Ваше объявление №{advert_id} было удалено администратором по причине: {close_reason}',
                                         'close_seller_notification_by_redis:close_advert': captions['close'],
                                         'width': 1}
}


class AdminReviewCatalogChooseCarBrand:
    message_text = 'Выберите марку машины для просмотра:'
    buttons_callback_data = 'admin_catalog_review_brand:'
    dynamic_buttons = 2
    width = 1
    backward_command = {'admin_backward:catalog_review_choose_brand': captions['backward'], **return_main_menu}