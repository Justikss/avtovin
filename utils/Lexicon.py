import importlib

from dataclasses import dataclass

from config_data.config import SUPPORT_NUMBER, SUPPORT_TELEGRAM

LEXICON = {
            'confirm_from_buyer': {'separator': '=' * 40, 'non_data_more': 'Нет данных для отображения'},
            'unexpected_behavior': 'Неожиданное поведение',
            'seller_dont_exists': 'Продавец больше неактивен',
            'order_was_created': 'Заявка создана, в скором времени с вами свяжется продавец',
            'too_late': 'Вы опоздали',
            'success_notification': 'Принято',
            'user_in_system': {'message_text': 'Вы в системе'},
            'choose_language': {'message_text': 'Выберите ваш язык', 'language_uz': '🇺🇿 Uzb',
                                'language_ru': "🇷🇺 Rus", 'width': 2},
            'hello_text': {'message_text': 'Приветственное сообщение', 'start_sell': 'Продажа',
                           'start_buy': 'Покупка', 'width': 2},
            'write_full_name': {'message_text': 'Укажите ФИО', 'backward:user_registration': 'Назад', 'width': 1},
            'write_full_name(novalid)': {
                'message_text': 'Некорректный ввод, принимается 2-3 буквенных слова, разделённые пробелом',
                'backward:user_registration': 'Назад', 'width': 2},
            'write_phone_number': {'message_text': 'Укажите номер телефона, начиная с +',
                                   'backward:user_registration_number': 'Назад', 'width': 1},
            'write_phone_number(novalid)': {'message_text': 'Некорректный ввод номера, укажите номер начиная с +',
                                              'backward:user_registration_number': 'Назад', 'width': 1},
            'write_phone_number(exists)': {'message_text': 'Некорректный ввод номера!\nОн уже зарегистрирован\nожидается иной',
                                              'backward:user_registration_number': 'Назад', 'width': 1},

            # 'most_answers': {'message_text': 'Ответы на часто задаваемые вопросы', 'in_main': 'В меню', 'width': 1},
            'main_menu': {'message_text': 'Меню', 'offers_to_user': 'Предложения', 'car_search': 'Поиск Авто',
                          'faq': 'F.A.Q.', 'support': 'Поддержка', 'backward:set_language': 'Назад', 'width': 2},
            'f_a_q': {'message_text': 'Ответы на часто задаваемые вопросы:', 'return_main_menu': 'В меню',
                      'width': 1},
            'tech_support': {'message_text': 'Выберите ваше действие', 'write_to_support': 'Написать',
                             'call_to_support': 'Позвонить', 'width': 2, 'return_main_menu': 'В меню'},
            'write_to_support': {'message_text': SUPPORT_TELEGRAM, 'backward:support': 'Назад', 'width': 1},
            'call_to_support': {'message_text': SUPPORT_NUMBER, 'backward:support': 'Назад', 'width': 1},

            'search_car': {'message_text': 'Выберите категорию', 'new_cars': 'Новое', 'second_hand_cars': 'Б\У',
                           'return_main_menu': 'В меню', 'width': 2},
            'cars_not_found': {'message_text': 'К сожалению автомобилей этого класса нет на витрине.',
                               'backward:choose_car_category': 'Назад', 'return_main_menu': 'В меню', 'width': 1},

            'search_configuration': {'message_text': 'Настройте ваш поиск', 'start_configuration_search': 'Начать',
                                     'backward': 'Назад', 'width': 1},

            'choose_engine_type': {'message_text': 'Выберите тип двигателя', 'backward': 'Назад',
                                               'width': 1},
            'choose_brand': {'message_text': 'Выберите марку', 'backward_in_carpooling': 'Назад', 'width': 1},
            'choose_model': {'message_text': 'Выберите модель', 'backward_in_carpooling': 'Назад', 'width': 1},

            'choose_complectation': {'message_text': 'Выберите комплектацию', 'backward_in_carpooling': 'Назад',
                                     'width': 1},

            'choose_year_of_release': {'message_text': 'Выберите год', 'backward_in_carpooling': 'Назад',
                                       'width': 1},
            'choose_mileage': {'message_text': 'Выберите пробег', 'backward_in_carpooling': 'Назад', 'width': 1},
            'choose_color': {'message_text': 'Выберите цвет', 'backward_in_carpooling': 'Назад', 'width': 1},

            'chosen_configuration': {
                'message_text': {'your_configs': 'Ваши настройки:', 'engine_type': 'Тип двигателя: ',
                                 'model': 'Модель: ',
                                 'brand': 'Марка: ', 'complectation': 'Комплектация: ',
                                 'cost': 'Cтоимость: ', 'mileage': 'Пробег: ', 'year': 'Год: ',
                                 'color': 'Цвет: '}, 'buyer_car_pagination:-': '<', 'buyer_car_pagination:+': '>',
                'confirm_buy_settings:': 'Подтвердить',
                'backward_in_carpooling': 'Вернуться', 'width': 2},
                
            'confirm_buy_configuration': {'message_text': 'Вы успешно оставили заявку!\nВам поступит уведомление о её одобрении.',
                                          'return_main_menu': 'В меню', 'width': 1},
            'buy_configuration_error': {'message_text': 'У вас уже оставлена такая заявка.', 
                                        'return_main_menu': 'В меню', 'width': 1},
            'buy_configuration_non_registration': {'message_text': 'Ошибка. Ваш аккаунт незарегестрирован\nНажмите /start'},

            'notification_from_seller_by_buyer_buttons': {'check_orders_history_by_seller': 'Активные заявки', 'close_seller_notification:': 'Скрыть уведомление', 'width': 1},


            'confirm_from_seller': {'message_text': {'from_user': 'Пользователь', 'tendered': 'оставил заявку:',
                                    'contacts': 'Контакты:', 'separator': '=' * 40}, 'confirm_button': 'Подтвердить'},

            'buyer_offer_notification': {'message_text': 'Ваша заявка на автомобиль одобрена!', 'buttons': {'offers_to_user': 'История заявок', 'confirm_notification:buyer': 'Принял', 'width': 1}},


            'buttons_history_output': {'pagination_left': '<', 'pagination_right': '>',
                                       'return_from_offers_history': 'В меню', 'width': 2},
            'backward_name': 'Назад',


            'show_offers_history': {'no_more_pages': 'Больше нет страниц', 'no_less_pages': 'Позади нет страниц',
                                    'history_not_found': 'История запросов пуста'},
            'offer_parts': {'dealship_name': 'Салон', 'car_price': 'Примерная цена',
                            'dealship_contacts': 'Контакты салона',
                            'individual': 'Частное лицо', 'individual_contacts': 'Контакты'},

            "buyer_haven't_confirm_offers": 'История запросов пуста',
            "seller_haven't_this_car": 'У вас не продаётся такой автомобиль',
            'separator': '='*40,
            
            'who_is_seller': {'message_text': 'Выберите пункты ниже:', 'i_am_private_person': 'Частное лицо', 'i_am_car_dealership': 'Автосалон', 'width': 2},
            'write_full_seller_name': {'message_text': 'Укажите ФИО', 'backward:seller_registration_seller_person_name': 'Назад', 'width': 1},
            'write_full_seller_name(novalid)': {
                'message_text': 'Некорректный ввод, принимается 2-3 буквенных слова, разделённые пробелом',
                'backward:seller_registration_seller_person_name': 'Назад', 'width': 2},
            'write_full_seller_name(exists)': {'message_text': 'Это имя уже зарегестрировано\nожидается иное', 'backward:seller_registration_seller_person_name': 'Назад', 'width': 1},
            
            'write_dealership_name': {'message_text': 'Введите название автосалона:', 'backward:seller_registration_dealership_name': 'Назад', 'width': 1},
            'write_dealership_name(novalid)': {'message_text': 'Название автосалона должно быть длинной < 250 символов\nИ Только из букв и цифр:', 'backward:seller_registration_dealership_name': 'Назад', 'width': 1},
            'write_dealership_name(exists)': {'message_text': 'Это название уже зарегестрировано\nожидается иное', 'backward:seller_registration_dealership_name': 'Назад', 'width': 1},
            
            'write_seller_phone_number': {'message_text': 'Укажите номер телефона, начиная с +',
                                   'backward:seller_registration_number': 'Назад', 'width': 1},
            'write_seller_phone_number(novalid)': {'message_text': 'Некорректный ввод номера, укажите номер начиная с +',
                                              'backward:seller_registration_number': 'Назад', 'width': 1},
            'write_seller_phone_number(exists)': {'message_text': 'Некорректный ввод номера!\nОн уже зарегистрирован\nожидается иной',
                                              'backward:seller_registration_number': 'Назад', 'width': 1},          
            
            'write_dealership_address': {'message_text': 'Введите адрес автосалона', 'backward:seller_registration_dealership_address': 'Назад', 'width': 1},
            'write_dealership_address(novalid)': {'message_text': 'Ошибка\n Адрес автосалона должен содержать буквы', 'backward:seller_registration_dealership_address': 'Назад', 'width': 1},


            'checking_seller_entered_data': {'message_text': 'Введённые данные корректны?\n(Нажмите на поле для его переписи)', 'rewrite_seller_name': '', 'rewrite_seller_number': '', 'rewrite_dealership_address': '', 'confirm_registration_from_seller': 'Да, всё верно', 'width': 1},
            'confirm_registration_from_seller': {'message_text': 'Регисрация завершена\nДождитесь уведобления об одобрении от администрации.', 'start_sell': 'Меню продавца', 'width': 1},
            'try_again_seller_registration': {'message_text': 'Ошибка.\nдля подробностей перепройдите процесс регистрации.', 'return_to_start_seller_registration': 'Перепройти регистрацию', 'width': 1},

            'confirm_seller_profile_notification': {'message_text': 'Меню продавца!', 'buttons': {'seller_main_menu': 'В меню продавца', 'confirm_notification:seller': 'Принял', 'width': 1}},
    
            'seller_main_menu': {'message_text': 'Успешно профиль подтверждён!', 'seller_pofile': 'Профиль', 'seller_faq': 'FAQ', 'support': 'Поддержка', 'seller_requests': 'Заявки', 'backward:set_language': 'Назад', 'width': 2},

            'confirm_new_seller_registration_from_admin_button': {'confirm_from_admin': 'Подтвердить', 'callback_startswith': 'confirm_new_seller_registration_from:'},
            'seller_waiting_registration_confirm': {'start_text_legal': 'Заявка на регистрацию автосалона:', 'start_text_natural': 'Заявка на регистрацию частного продавца:',
                                                 'legal_message': {'name': 'Название автосалона: ', 'address': 'Адрес: '},
                                                  'natural_message': {'name': 'Имя: ', 'surname': 'Фамилия: ', 'patronymic': 'Отчество: '},
                                                   'phone_number': 'Телефонный номер: '},
            'success_seller_registration_notice': {'message_text': 'Вы зарегестрированы в системе', 'return_main_menu': 'В меню продавца', 'width': 1},

            'seller_faq': {'message_text': 'Самые частые вопросы: ', 'return_main_menu': 'В меню', 'width': 1},
            'seller_requests': {'message_text': 'Заявки', 'my_sell_requests': 'Мои заявки', 'create_new_seller_request': 'Создать заявку', 'return_main_menu': 'В меню', 'width': 1},


            'confirm_load_config_from_seller_button': {'confirm_load_config_from_seller': 'Подтвердить', 'edit_boot_car_data': 'Изменить', 'return_main_menu': 'В меню', 'width': 1},
            'seller_load_notification_button': {'return_main_menu': 'В меню'},

            'message_not_digit': {'message_text': 'Сумма должна состоять только из цифр'},
            'message_not_photo': 'Прикрепите фотографию\n(значок скрепки в левом углу чата)\nНе отменяйте сжатие при отправке\nфотографии в телеграмм',

            'seller_start_delete_request': {'message_text': 'Введите номер удаляемой заявки', 'buttons': {'backward:seller_start_delete_request': 'Назад', 'width': 1}},

            'incorrect_input_removed_car_id': 'Неверный ввод номера заявки.\nСверьте номер по кнопке "Назад" и введите снова.',
            'confirm_delete_request': {'message_text': 'Вы действительно хотите удалить это авто?', 'confirm_delete': 'Подтвердить', 'backward:seller_delete_request': 'Назад', 'width': 1},

            'retry_now_allert': 'Попробуйте снова',
            'user_havent_permision': 'У вас нет прав',
            'seller_without_tariff': 'У вас нет откликов на счету',
            'seller_tarriff_expired': 'Ваш тариф неактуален',
            'non_actiallity': 'Не актуально',
            'successfully': 'Успешно',
            'seller_does_have_this_car': 'У вас не продаётся такая машина'
        }


class LexiconCommodityLoader:
    load_commodity_state = {'message_text': 'Состояние', 'buttons': {'load_state_new': 'Новое', 'load_state_second_hand': 'Б/у', 'backward:start_boot_new_car': 'Назад', 'width': 2}}
    load_engine_type = {'message_text': 'Тип двигателя', 'buttons': {'load_engine_hybrid': 'Гибрид', 'load_engine_DWS': 'ДВС', 'load_engine_electro': 'Электро', 'width': 2}}
    load_commodity_brand = {'message_text': 'Марка', 'buttons': {'load_brand_bmw': 'BMW', 'load_brand_mercedes': 'Mercedes', 'load_brand_renault': 'Renault', 'load_brand_skoda': 'Skoda', 'width': 2}}
    load_commodity_model = {'message_text': 'Модель', 'buttons': {'load_model_DualModel': 'DualModel', 'load_model_OneModel': 'OneModel', 'load_model_ThreeModel': 'ThreeModel', 'load_model_SeModel': 'SeModel', 'width': 2}}
    load_commodity_complectation = {'message_text': 'Комплектация', 'buttons': {'load_complectation_FullComplectation': 'FullComplectation', 'load_complectation_HalfComplectation': 'HalfComplectation', 'load_complectation_HalfHalfComplectation': 'HalfHalfComplectation', 'load_complectation_WithTruckComplectation': 'WithTruckComplectation', 'width': 2}}

    load_commodity_year_of_realise = {'message_text': 'Год выпуска', 'buttons': {'load_year_2005': '2005', 'load_year_2020': '2020', 'load_year_2015': '2015', 'load_year_2001': '2001', 'width': 2}}
    load_commodity_mileage = {'message_text': 'Пробег', 'buttons': {'load_mileage_5000': '5000', 'load_mileage_10000': '10000', 'load_mileage_15000': '15000', 'load_mileage_20000': '20000', 'load_mileage_25000': '25000', 'load_mileage_30000': '30000', 'load_mileage_35000': '35000', 'load_mileage_40000': '40000', 'load_mileage_45000': '45000', 'load_mileage_50000': '50000', 'load_mileage_750000': '750000', 'load_mileage_100000': '100000', 'load_mileage_100000+': '100000 +', 'width': 4}}
    load_commodity_color = {'message_text': 'Цвет', 'buttons': {'load_color_black': 'Чёрный', 'load_color_red': 'Красный', 'load_color_pink': 'Розовый', 'load_color_white': 'Белый', 'width': 2}}
    load_commodity_price = {'message_text': 'Сумма', 'buttons': {'return_main_menu': 'В меню', 'width': 1}}
    load_commodity_photo = {'message_text': 'Пришлите фото автомобиля\n(значок скрепки в левом углу чата)\n\n(!от 3 до 5 экземпляров!)\n\nНе отменяйте сжатие при отправке\nфотографии в телеграмм.', 'buttons': {'return_main_menu': 'В меню', 'width': 1}}

    edit_photo_caption = 'Фото'


    config_for_seller = 'Ваши конфигурации:'
    can_rewrite_config = '\n\nВозможна перепись полей по нажатию на нужную кнопку'
    config_for_seller_button_callbacks = ('rewrite_boot_state', 'rewrite_boot_engine', 'rewrite_boot_brand', 'rewrite_boot_model', 'rewrite_boot_complectation', 'rewrite_boot_year', 'rewrite_boot_mileage', 'rewrite_boot_color', 'rewrite_boot_price', 'rewrite_boot_photo')

    config_for_admins = 'Заявка от продавца @'

    seller_notification = {'message_text': 'Заявка №_ создана!'}

class LexiconSellerRequests:
    seller_does_have_active_requests_alert = 'У вас нет активных заявок'
    seller_does_have_active_car_by_brand = 'Эта марка неактуальна.'
    select_brand_message_text = 'Выберите марку автомобиля'
    callback_prefix = 'seller_requests_brand:'
    # backward_button = {'backward:sales_brand_choose': 'Назад'}
    keyboard_end_part = {'backward:sales_brand_choose': 'Назад', 'width': 2}
    # choose_brand_keyboard_width = 1

    selected_brand_output_buttons = {'buttons': {'seller_requests_pagination_left': '<', 'seller_requests_pagination_right': '>',
                                                'delete_request_from_seller': 'Удалить по номеру заявки',
                                                'backward:sales_order_review': 'Назад', 'width': 2}}

    output_car_request_header = 'Заявка №_'
    commodity_state = '\nСостояние: '
    engine_type = '\nТип двигателя: '
    commodity_brand = '\nМарка: '
    commodity_model = '\nМодель: '
    commodity_complectation = '\nКомплектация: '
    commodity_year_of_realise = '\nГод выпуска: '
    commodity_mileage = '\nПробег: '
    commodity_color = '\nЦвет: '
    commodity_price = '\nСумма: '

    pagination_pagesize = 1

    page_view_separator = 'Страница: '

    pages_were_end = 'Страницы кончились'



class LexiconSellerProfile:
    header = 'Профиль: \n'
    dealership_prefix = 'Юридическое лицо'
    seller_prefix = 'Частное лицо\n'
    dealership_name_prefix = 'Название автосалона: '
    dealership_address_prefix = 'Адрес автосалона : '
    seller_name_prefix = 'ФИО продавца: '
    phonenumber_prefix = 'Телефонный номер: '

    tariff_prefix = '\n- Тариф: '
    tariff_out_date_prefix = '\nДо '
    residual_feedback_prefix = '\n- Остаток откликов: '
    tariff_extension_button = {'tariff_extension': 'Продлить тариф', 'return_main_menu': 'В меню', 'width': 1}
    tarif_expired = 'Ваш тариф истёк'

class DateTimeFormat:
    get_string = '%d-%m-%Y %H:%M:%S'

class LexiconTariffSelection:
    not_found_message_text = 'Тарифов не найдено'
    message_text = 'Все доступные тарифы'
    callback_type = 'select_tariff:'
    backward_button_callback = 'backward:affordable_tariffs'
    backward_button_caption = 'Отмена'
    keyboard_width_value = 2

class LexiconSelectedTariffPreview:
    header = 'Информация о тарифе:'
    name = '\n- '
    price = '\n- Стоимость: '
    duration_time = '\n- Срок действия: '
    feedback_amount = '\n- Лимит отзывов: '
    buttons = {'start_choose_payment_method': 'Выбор платёжной системы', 'backward:tariff_preview': 'Назад', 'width': 1}

class LexiconChoicePaymentSystem:
    message_text = 'Выберите платёжную систему'
    payment_click = {'run_tariff_payment:click': 'CLICK'}
    payment_payme = {'run_tariff_payment:payme': 'PayMe'}
    payment_uzumPay = {'run_tariff_payment:uzumPay': 'UzumPay'}
    bottom_buttons = {'backward:choose_payment_system': 'Назад', 'width': 1} 
    buttons_list = [payment_click, payment_payme, payment_uzumPay, bottom_buttons]


class LexiconCreateInvoice:
    in_progress_notification = 'В разработке'
    title = 'Оформление тарифа '
    description = 'Подписка на -_- откликов покупателей.\nПериодом -_- дней.'
    load_price_label = 'Цена за тариф'

class LexiconPaymentOperation:
    error_payment_text = 'Ошибка оплаты, попробуйте снова, соблюдая тайм аут в 15 минут'

    success_payment_text = 'Удачно!'

    cancel_button = {'Отмена': 'backward:make_payment'}
    return_main_menu = {'В меню': 'return_main_menu'}
    width_parameter = {'width': 1}