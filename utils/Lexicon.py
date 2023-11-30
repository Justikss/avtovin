import importlib

from dataclasses import dataclass

from config_data.config import SUPPORT_NUMBER, SUPPORT_TELEGRAM

class ChooseEngineType:
    message_text = 'Выберите тип двигателя'
    buttons_callback_data = 'cars_engine_type_'
    last_buttons = {'backward': 'Назад'}
    width = 1


class ChooseBrand:
    message_text = 'Выберите марку'
    last_buttons = {'backward_in_carpooling': 'Назад'}
    buttons_callback_data = 'cars_brand_'
    width = 1
class ChooseModel:
    message_text = 'Выберите модель'
    last_buttons = {'backward_in_carpooling': 'Назад'}
    buttons_callback_data = 'cars_model_'
    width = 1

class ChooseComplectation:
    message_text = 'Выберите комплектацию'
    last_buttons = {'backward_in_carpooling': 'Назад'}
    buttons_callback_data = 'cars_complectation_'
    width = 1

class ChooseYearOfRelease:
    message_text = 'Выберите год'
    last_buttons = {'backward_in_carpooling': 'Назад'}
    buttons_callback_data = 'cars_year_of_release_'
    width = 1
class ChooseMileage:
    message_text = 'Выберите пробег'
    last_buttons = {'backward_in_carpooling': 'Назад'}
    buttons_callback_data = 'cars_mileage_'
    width = 1
class ChooseColor:
    message_text = 'Выберите цвет'
    last_buttons = {'backward_in_carpooling': 'Назад'}
    buttons_callback_data = 'cars_color_'
    width = 1


LEXICON = {
            'cached_requests_for_buyer_message_text': {
                'message_text': 'Просмотр неподтверждённых вами предложений\nВыберите марку:'},
            'return_main_menu_only': {'return_main_menu': 'Назад'},
            'output_inline_brands_pagination': {'inline_buttons_pagination:-': '<', 'page_count': '[C/M]', 'inline_buttons_pagination:+': '>'},
            'confirm_from_buyer': {'separator': '=' * 40, 'non_data_more': 'Нет данных для отображения'},

            'unexpected_behavior': 'Неожиданное поведение',
            'car_was_withdrawn_from_sale': 'Автомобиль был снят с продажи',
            'car_search_parameters_incactive': 'Данные параметры поиска больше неактивны. Пожалуйста обновите их.',
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
            'main_menu': {'message_text': 'Меню', 'cached_requests': 'Предложения', 'car_search': 'Поиск Авто',
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


            'chosen_configuration': {
                'message_text': {'your_configs': 'Ваши настройки:',
                                 'car_state': 'Состояние:',
                                 'engine_type': 'Тип двигателя:',
                                 'model': 'Модель:',
                                 'brand': 'Марка:', 'complectation': 'Комплектация:',
                                 'cost': 'Cтоимость:', 'mileage': 'Пробег:', 'year': 'Год:',
                                 'color': 'Цвет:'}, 'buyer_car_pagination:-': '<', 'buyer_car_pagination:+': '>',
                'confirm_buy_settings:': 'Подтвердить',
                'backward_in_carpooling': 'Вернуться', 'return_main_menu': 'В меню', 'width': (2, 1, 1, 1)},

            'confirm_buy_configuration': {'message_text': 'Вы успешно оставили заявку!\nВам поступит уведомление о её одобрении.',
                                          'return_main_menu': 'В меню', 'width': 1},
            'buy_configuration_error': {'message_text': 'У вас уже оставлена такая заявка.',
                                        'return_main_menu': 'В меню', 'width': 1},
            'buy_configuration_non_registration': {'message_text': 'Ошибка. Ваш аккаунт незарегестрирован\nНажмите /start'},

            'notification_from_seller_by_buyer_buttons': {'my_sell_feedbacks:': 'Смотреть отклики', 'close_seller_notification:': 'Скрыть уведомление', 'width': 1},


            'confirm_from_seller': {'message_text': {'feedback_header': 'Отлкик №X', 'from_user': 'Пользователь', 'tendered': 'оставил отклик на заявку #X :',
                                    'contacts': 'Контакты:', 'separator': '=' * 40}, 'confirm_button': 'Подтвердить'},

            'backward_name': 'Назад',


            "buyer_haven't_cached_requests": 'История недавно просмотренных пуста',
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
            'seller_requests': {'message_text': 'Заявки', 'my_sell_requests': 'Мои заявки', 'my_sell_feedbacks': 'Мои отклики', 'create_new_seller_request': 'Создать заявку', 'return_main_menu': 'В меню', 'width': 1},


            'confirm_load_config_from_seller_button': {'confirm_load_config_from_seller': 'Подтвердить', 'edit_boot_car_data': 'Изменить', 'return_main_menu': 'В меню', 'width': 1},
            'seller_load_notification_button': {'return_main_menu': 'В меню'},

            'message_not_digit': {'message_text': 'Сумма должна состоять только из цифр'},
            'message_not_photo': 'Прикрепите фотографию\n(значок скрепки в левом углу чата)\nНе отменяйте сжатие при отправке\nфотографии в телеграмм',

            'seller_start_delete_request': {'message_text': 'Введите номер удаляемой заявки', 'buttons': {'backward:seller_start_delete_request': 'Назад', 'width': 1}},

            'incorrect_input_removed_car_id': 'Неверный ввод номера заявки.\nСверьте номер по кнопке "Назад" и введите снова.',
            'confirm_delete_request': {'message_text': 'Вы действительно хотите удалить это авто?', 'confirm_delete': 'Подтвердить', 'backward:seller_delete_request': 'Назад', 'width': 1},

            'seller___my_feedbacks': {'message_text': 'Мои отклики', 'buttons': {'new_feedbacks': 'Новые', 'viewed_feedbacks': 'Просмотренные', 'backward:seller__my_feedbacks': 'Назад', 'width': 2}},


            'retry_now_allert': 'Попробуйте снова',
            'user_havent_permision': 'У вас нет прав',
            'seller_without_tariff': 'У вас нет откликов на счету',
            'seller_tarriff_expired': 'Ваш тариф неактуален',
            'non_actiallity': 'Не актуально',
            'successfully': 'Успешно',
            'seller_does_have_this_car': 'У вас не продаётся такая машина'
        }


class LexiconCommodityLoader:
    class load_commodity_state:
        message_text = 'Состояние'
        buttons_callback_data = 'load_state_'
        width = 2

    class load_engine_type:
        message_text = 'Тип двигателя'
        buttons_callback_data = 'load_engine_'
        width = 2

    class load_commodity_brand:
        message_text = 'Марка'
        buttons_callback_data = 'load_brand_'
        width = 2

    class load_commodity_model:
        message_text = 'Модель'
        buttons_callback_data = 'load_model_'
        width = 2

    # load_commodity_model = {, 'buttons': {, , 'width': 2}}
    class load_commodity_complectation:
        message_text = 'Комплектация'
        buttons_callback_data = 'load_complectation_'
        width = 2

    class load_commodity_year_of_realise:
        message_text = 'Год выпуска'
        buttons_callback_data = 'load_year_'
        width = 2
    class load_commodity_mileage:
        message_text = 'Пробег'
        buttons_callback_data = 'load_mileage_'
        width = 2
    class load_commodity_color:
        message_text = 'Цвет'
        buttons_callback_data = 'load_color_'
        width = 2

    load_commodity_price = {'message_text': 'Сумма', 'buttons': {'return_main_menu': 'В меню', 'width': 1}}
    load_commodity_photo = {'message_text': 'Пришлите фото автомобиля\n(значок скрепки в левом углу чата)\n\n(!от 3 до 5 экземпляров!)\n\nНе отменяйте сжатие при отправке\nфотографии в телеграмм.', 'buttons': {'return_main_menu': 'В меню', 'width': 1}}

    edit_photo_caption = 'Фото'


    config_for_seller = 'Ваши конфигурации:'
    can_rewrite_config = '\n\nВозможна перепись полей по нажатию на нужную кнопку'
    config_for_seller_button_callbacks = ('rewrite_boot_state', 'rewrite_boot_engine', 'rewrite_boot_brand', 'rewrite_boot_model', 'rewrite_boot_complectation', 'rewrite_boot_year', 'rewrite_boot_mileage', 'rewrite_boot_color', 'rewrite_boot_price', 'rewrite_boot_photo')

    config_for_admins = 'Заявка от продавца @'

    seller_notification = {'message_text': 'Заявка №_ создана!'}


class LexiconSellerRequests:
    backward_from_delete_in_feedbacks = {'viewed_feedbacks': 'Назад'}

    seller_sure_delete_car_ask = {'message_text': 'Вы уверены что хотите удалить с витрины машину №X ?',
                                  'buttons': {"i'm_sure_delete": 'Удалить', 'backward_from_delete_car_menu': 'Назад', 'width': 1}}
    seller_does_have_active_requests_alert = 'У вас нет активных заявок'
    seller_does_have_active_car_by_brand = 'Эта марка не актуальна.'
    select_brand_message_text = {'message_text': 'Выберите марку автомобиля'}
    callback_prefix = 'seller_requests_brand:'
    # backward_button = {'backward:sales_brand_choose': 'Назад'}
    keyboard_end_part = {'backward:sales_brand_choose': 'Назад'}
    # choose_brand_keyboard_width = 1
    return_to_requests_buttons = {'buttons': {'backward:rewrite_price_by_seller': 'К заявкам', 'width': 1}}
    input_new_price = {'message_text': 'Введите новую стоимость.\n[Нынешняя цена: X]', **return_to_requests_buttons}
    input_new_price_incorrect_message_text = 'Введите новую стоимость.\n[Нынешняя: X]\nПожалуйста, укажите целочисленное значение!'
    input_new_price_car_dont_exists = {'message_text': 'К сожалению автомобиль снят с продажи.\nИли введено большое число.', **return_to_requests_buttons}
    succes_rewrite_price = {'message_text': 'Цена успешно изменена', **return_to_requests_buttons}

    pagination_vectors = {'seller_requests_pagination_left': '<', 'seller_requests_pagination_right': '>'}

    selected_brand_output_buttons = {'buttons': {**pagination_vectors,
                                                 'rewrite_price_by_seller': 'Изменить цену',
                                                'withdrawn': 'Удалить из каталога',
                                                'backward:sales_order_review': 'Назад', 'width': (2, 1, 1, 1)}}

    check_viewed_feedbacks_buttons = {'buttons': {**pagination_vectors,
                                               'withdrawn': 'Снять с продажи', 'deal_fell_through': 'Сделка сорвалась',
                                               'backward:check_feedbacks': 'Назад', 'width': (2, 2, 1)}}

    check_new_feedbacks_buttons = {'buttons': {**pagination_vectors,
                                               'backward:check_feedbacks': 'Назад', 'width': (2, 1)}}

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
    new_feedbacks_not_found = 'У вас не появилось новых откликов'
    viewed_feedbacks_not_found = 'У вас нет просмотренных откликов'
    did_you_sure_to_delete_feedback_ask = {'message_text': 'Вы уверены удалить отклик №X ?',
                                           'buttons': {"i'm_sure_delete_feedback": 'Подтвердить', 'backward_from_delete_feedback_menu': 'Назад', 'width': 1}}
    success_delete = 'Удалено'



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