from utils.lexicon_utils.admin_lexicon.admin_lexicon import return_main_menu, captions, pagination_interface

catalog_captions = {'catalog_review__make_block': 'блокировку', 'to_block': 'блокировки', 'to_delete': 'удаления',
                    'catalog_review__make_delete': 'удаление объявления', 'advert': 'Объявление: {advert_id}\n',
                    'inactive_advert': 'Объявление неактивно'
                    }

__CATALOG_LEXICON = {
    'start_catalog_menu': {'message_text': 'Каталог\nВыберите действие:', 'buttons': {
        'admin_catalog__add_new_car_parameters': 'Добавить авто',
        'admin_catalog__car_catalog_review': 'Каталог авто',
        **return_main_menu,
        'width': 1
    }},
    'car_catalog_review_choose_category': {'message_text': 'Выберите тип просматриваемых объявлений:', 'buttons': {
        'car_catalog_review__new': 'Новые',
        'car_catalog_review__viewed': 'Просмотренные',
        'search_by_?': 'Поиск по ?',
        'admin_backward:choose_catalog_review_advert_type': captions['backward'],
        'width': 2
    }},
    'review_specific_advert_catalog': {'message_text': 'Объявление: №{advert_id}\n{seller_entity}:', 'buttons': {
        **pagination_interface,
        'admin_review_catalog_delete_advert': captions['delete'],
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
        'message_text': 'Произвести {action_subject}\n{seller_entity}\n{telegram_username}\n{advert_caption}По причине:\n{action_reason}',
        'buttons': {'catalog_review__confirm_close_action': captions['confirm'],
                    'admin_backward:to_catalog_review_adverts': 'Вернуться к объявлениям',
                    'admin_backward:catalog_review_close_action_confirmation': captions['backward'],
                    **return_main_menu,
                    'width': 1}}
}

class AdminReviewCatalogChooseCarBrand:
    message_text = 'Выберите марку машины для просмотра:'
    buttons_callback_data = 'admin_catalog_review_brand:'
    dynamic_buttons = 2
    width = 1
    backward_command = {'admin_backward:catalog_review_choose_brand': captions['backward'], **return_main_menu}