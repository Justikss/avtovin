from config_data.config import SUPPORT_NUMBER, SUPPORT_TELEGRAM, faq_seller, faq_buyer, faq, money_valute, \
    SUPPORT_NUMBER_2
from utils.safe_dict_class import SafeDict


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

class SecondsEndswith:
    one = 'а'
    two_four = 'ы'

LEXICON = {
            'sepp': '—',
            'new_recommended_offer_startswith': 'Поступило новое предложение:',
            'make_choose_brand': 'Выберите марку:',
            'buyer_havent_recommendated_offers': 'Список рекомендованных объявлений пуст!',
            'active_offers_non_exists': 'Список активных предложений пуст.',
            "buyer_haven't_cached_requests": 'История недавно просмотренных пуста.',
            'incoming_address_caption': 'Указанный адрес:\n',
            'address': 'Адрес',
            'waiting_request_process': "Ваш запрос обрабатывается. Примерное время ожидания: X секунд.",
            'cached_requests_for_buyer_message_text': {
                'message_text': 'Просмотр неподтверждённых вами предложений\n'},
            'active_offers_for_buyer_message_text': {
                'message_text': 'Просмотр активных предложений\n'},
            'recommended_offers_for_buyer_message_text' : {
                'message_text': 'Просмотр рекомендованных предложений\n'},
            'backward_from_buyer_offers': {'buyer_requests': 'Назад'},
            'output_inline_brands_pagination': {'inline_buttons_pagination:-': '←', 'page_count': '[C/M]', 'inline_buttons_pagination:+': '→'},
            'confirm_from_buyer': {'separator': '=' * 40, 'non_data_more': 'Нет данных для отображения'},
            'start_registration': 'Пройдите регистрацию!',
            'unexpected_behavior': 'Неожиданное поведение',
            'car_was_withdrawn_from_sale': 'Автомобиль был снят с продажи',
            'car_search_parameters_incactive': 'Данные параметры поиска больше неактивны. Пожалуйста обновите их.',
            'seller_dont_exists': 'Продавец больше неактивен',
            'order_was_created': 'Вы откликнулись! Теперь в объявлении указан контакт продавца,\nТак же пополнен список ваших предложений!',
            'too_late': 'Вы опоздали',
            'success_notification': 'Принято',
            'user_in_system': {'message_text': 'Вы в системе'},
            'choose_language': {'message_text': 'Выберите ваш язык', 'language_uz': '🇺🇿 Uzb',
                                'language_ru': "🇷🇺 Rus", 'width': 2},
            'hello_text': {'message_text': '<b>Привет, <i>X</i></b>!\nУ нас ты можешь купить или продать своё авто.\nВыбери один из пунктов ниже 👇🏼', 'start_sell': 'Продажа 👨🏻‍💼',
                           'start_buy': '👨🏻‍💻 Покупка', 'width': 2},
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
            'main_menu': {'message_text': 'Меню покупателя 👨🏻‍💻\nВыберите ваше действие:', 'buyer_requests': 'Предложения 📋', 'car_search': '🚘 Поиск Авто',
                          'faq': 'Инструкции 💬', 'support': '🌐 Поддержка', 'backward:set_language': 'Назад ', 'width': 2},
            'buyer_requests': {'message_text': 'Список предложений:', 'buttons': {'buyer_active_offers': '✅ Подтверждённые (X) ✅', 'buyer_cached_offers': '❌ Неподтверждённые (X) ❌', 'buyers_recommended_offers': '🔰 Новые (X) 🔰', 'return_main_menu': 'В меню', 'width': 1}},
            'f_a_q': {'message_text': f'Ответы на часто задаваемые вопросы: \n\nДля ознакомления с устройством купле-продажи в боте, выберите кнопки ниже.\n{faq}', 'seller_faq': 'Продажа 👨🏻‍💼', 'buyer_faq': '👨🏻‍💻 Покупка',
                      'return_main_menu': 'Назад', 'width': 2},
            'tech_support': {'message_text': 'Выберите ваше действие:', 'write_to_support': 'Написать 💬',
                             'call_to_support': 'Позвонить 📱', 'width': 2, 'return_main_menu': 'Назад'},
            'write_to_support': {'message_text': SUPPORT_TELEGRAM, 'backward:support': 'Назад', 'width': 1},
            'call_to_support': {'message_text': f'Вы можете позвонить нам по следующим номерам:\n👩🏻‍💻Сотрудница поддержки: {SUPPORT_NUMBER}\n👨🏻‍💻Сотрудник поддержки: {SUPPORT_NUMBER_2}', 'backward:support': 'Назад', 'width': 1},

            'search_car': {'message_text': 'Выберите тип автомобиля:', 'new_cars': 'Новое', 'second_hand_cars': 'Б\У',
                           'return_main_menu': 'Назад', 'width': 2},
            'cars_not_found': {'message_text': 'К сожалению автомобилей этого класса нет на витрине.',
                               'backward:choose_car_category': 'Назад', 'return_main_menu': 'В меню', 'width': 1},

            'search_configuration': {'message_text': 'Настройте ваш поиск', 'start_configuration_search': 'Начать',
                                     'backward': 'Назад', 'width': 1},
            'footer_for_output_active_offers': {'viewed_status': 'Статус просмотра продавцом: ', 'status_true': 'Просмотрено ✅', 'status_false': 'Не просмотрено ❌'},
            'active_offer_caption': 'Активная заявка:',
            'chosen_configuration': {
                'message_text': {'phone_number': 'Мобильный телефон: ',
                                'your_configs': '<b>Предложения по вашему запросу:</b>',
                                 'from_seller': 'От Продавца: X',
                                 'from_dealership': 'От Автосалона: <i>X</i>\nПо Адресу: <i>Y</i>',
                                 'car_state': 'Состояние: <i>X</i>',
                                 'engine_type': 'Тип двигателя: <i>X</i>',
                                 'model': 'Модель: <i>X</i>',
                                 'brand': 'Марка: <i>X</i>', 'complectation': 'Комплектация: <i>X</i>',
                                 'cost': f'<blockquote><b>Cтоимость: <i>X {money_valute}</i></b></blockquote>', 'mileage': 'Пробег: <i>X</i>', 'year': 'Год: <i>X</i>',
                                 'color': 'Цвет: <i>X</i>'}, 'buyer_car_pagination:-': '←', 'buyer_car_pagination:+': '→',
                'confirm_buy_settings:': '✓ Подтвердить ✓',
                'backward_in_carpooling': 'Редактировать', 'return_main_menu': '🏡 В меню 🏡', 'width': (2, 1, 1, 1)},

            'confirm_buy_configuration': {'message_text': 'Вы успешно оставили заявку!\nВам поступит уведомление о её одобрении.',
                                          'return_main_menu': 'В меню', 'width': 1},
            'buy_configuration_error': {'message_text': 'У вас уже оставлена такая заявка.',
                                        'return_main_menu': 'В меню', 'width': 1},
            'user_non_registration': {'message_text': 'Ошибка. Ваш аккаунт незарегестрирован\nНажмите /start'},

            'notification_from_seller_by_buyer_buttons': {'my_sell_feedbacks:': 'Смотреть отклики', 'close_seller_notification:': 'Скрыть уведомление', 'width': 1},


            'confirm_from_seller': {'message_text': {'feedback_header': '<b>Отлкик №X</b>', 'from_user': 'Пользователь <i>X</i>', 'tendered': 'оставил отклик на заявку <i>№X</i> :',
                                    'contacts': ' '*10 + 'Контакты:\nS<i>\nN\nP</i>', 'separator': ' ' *10 + '—' * 5}, 'confirm_button': 'Подтвердить'},

            'backward_name': 'Назад',
            "seller_haven't_this_car": 'У вас не продаётся такой автомобиль',
            'separator': '='*40,

            'who_is_seller': {'message_text': 'Выберите пункты ниже:', 'i_am_private_person': 'Частное лицо', 'i_am_car_dealership': 'Автосалон', 'backward:set_language': 'назад', 'width': 2},
            'write_full_seller_name': {'message_text': 'Укажите ФИО', 'backward:seller_registration_seller_person_name': 'Назад', 'width': 1},
            'write_full_seller_name(novalid)': {
                'message_text': 'Некорректный ввод, принимается 2-3 буквенных слова, разделённые пробелом',
                'backward:seller_registration_seller_person_name': 'Назад', 'width': 2},
            'write_full_seller_name(exists)': {'message_text': 'Это имя уже зарегестрировано\nожидается иное', 'backward:seller_registration_seller_person_name': 'Назад', 'width': 1},

            'write_dealership_name': {'message_text': 'Введите название автосалона:', 'backward:seller_registration_dealership_name': 'Назад', 'width': 1},
            'write_dealership_name(novalid)': {'message_text': 'Название автосалона должно быть длинной меньше чем 250 символов\nИ состоять только из букв и цифр:', 'backward:seller_registration_dealership_name': 'Назад', 'width': 1},
            'write_dealership_name(exists)': {'message_text': 'Это название уже зарегестрировано\nожидается иное', 'backward:seller_registration_dealership_name': 'Назад', 'width': 1},

            'write_seller_phone_number': {'message_text': 'Укажите номер телефона, начиная с +',
                                   'backward:seller_registration_number': 'Назад', 'width': 1},
            'write_seller_phone_number(novalid)': {'message_text': 'Некорректный ввод номера, укажите номер начиная с +',
                                              'backward:seller_registration_number': 'Назад', 'width': 1},
            'write_seller_phone_number(exists)': {'message_text': 'Некорректный ввод номера!\nОн уже зарегистрирован\nожидается иной',
                                              'backward:seller_registration_number': 'Назад', 'width': 1},

            'write_dealership_address': {'message_text': 'Введите адрес автосалона\nИли отправьте вашу геолокацию\n(значок скрепки в левом углу чата)', 'backward:seller_registration_dealership_address': 'Назад', 'width': 1},
            'write_dealership_address(novalid)': {'message_text': 'Ошибка\n Адрес автосалона должен содержать буквы', 'backward:seller_registration_dealership_address': 'Назад', 'width': 1},


            'checking_seller_entered_data': {'message_text': 'Введённые данные корректны?\n(Нажмите на поле для его переписи)', 'rewrite_seller_name': '', 'rewrite_seller_number': '', 'rewrite_dealership_address': '', 'confirm_registration_from_seller': 'Да, всё верно', 'width': 1},
            'confirm_registration_from_seller': {'message_text': 'Регистрация завершена\nДождитесь уведобления об одобрении от администрации.', 'start_sell': 'Меню продавца', 'width': 1},
            'try_again_seller_registration': {'message_text': 'Ошибка.\nдля подробностей перепройдите процесс регистрации.', 'return_to_start_seller_registration': 'Перепройти регистрацию', 'width': 1},

            'confirm_seller_profile_notification': {'message_text': '✅Успешно, профиль продавца подтверждён!', 'buttons': {'seller_main_menu': 'В меню продавца', 'close_seller_notification_by_redis:seller': 'Скрыть', 'width': 1}},

            'seller_main_menu': {'message_text': 'Меню продавца 👨🏻‍💼\nВыберите ваше действие:', 'seller_pofile': 'Профиль 📱', 'faq': '💬 Инструкции', 'support': 'Поддержка 🌐', 'seller_requests': '📋 Заявки', 'backward:set_language': 'Назад', 'width': 2},

            'confirm_new_seller_registration_from_admin_button': {'confirm_from_admin': 'Подтвердить', 'callback_startswith': 'confirm_new_seller_registration_from:'},
            'seller_waiting_registration_confirm': {'start_text_legal': 'Заявка на регистрацию автосалона:', 'start_text_natural': 'Заявка на регистрацию частного продавца:',
                                                 'legal_message': {'name': 'Название автосалона: ', 'address': 'Адрес: '},
                                                  'natural_message': {'name': 'Имя: ', 'surname': 'Фамилия: ', 'patronymic': 'Отчество: '},
                                                   'phone_number': 'Телефонный номер: '},
            'success_seller_registration_notice': {'message_text': 'Вы зарегестрированы в системе', 'return_main_menu': 'В меню продавца', 'width': 1},

            'seller_faq': {'message_text': faq_seller, 'return_main_menu': 'В меню', 'faq': 'Назад', 'width': 1},
            'buyer_faq': {'message_text': faq_buyer, 'return_main_menu': 'В меню', 'faq': 'Назад', 'width': 1},
            'seller_requests': {'message_text': 'Раздел работы с заявками\nВыберите ваше действие:', 'create_new_seller_request': '📨 Создать объявление 📨 ', 'my_sell_requests': '💰 Мои объявления 💰', 'my_sell_feedbacks': '📥 Отклики 📥', 'return_main_menu': 'В меню', 'width': 1},


            'confirm_load_config_from_seller_button': {'confirm_load_config_from_seller': 'Подтвердить', 'edit_boot_car_data': 'Изменить', 'return_main_menu': 'В меню', 'width': 1},
            'seller_load_notification_button': {'return_main_menu': 'В меню'},

            'message_not_digit': {'message_text': 'Сумма должна состоять только из цифр'},
            'message_not_photo': 'Прикрепите фотографию\n(значок скрепки в левом углу чата)\nНе отменяйте сжатие при отправке\nфотографии в телеграмм',

            'seller_start_delete_request': {'message_text': 'Введите номер удаляемой заявки', 'buttons': {'backward:seller_start_delete_request': 'Назад', 'width': 1}},

            'incorrect_input_removed_car_id': 'Неверный ввод номера заявки.\nСверьте номер по кнопке "Назад" и введите снова.',
            'confirm_delete_request': {'message_text': 'Вы действительно хотите удалить это авто?', 'confirm_delete': 'Подтвердить', 'backward:seller_delete_request': 'Назад', 'width': 1},

            'seller___my_feedbacks': {'message_text': 'Мои отклики', 'buttons': {'new_feedbacks': '✓ Новые ✓', 'viewed_feedbacks': '👁 Просмотренные 👁', 'backward:seller__my_feedbacks': 'Назад', 'width': 2}},
            'return_main_menu_button': {'return_main_menu': 'В меню'},

            'retry_now_allert': 'Попробуйте снова',
            'user_havent_permision': 'У вас нет прав',
            'seller_without_tariff': 'У вас нет откликов на счету',
            'seller_tarriff_expired': 'Ваш тариф неактуален',
            'non_actiallity': 'Не актуально',
            'successfully': 'Успешно',
            'seller_does_have_this_car': 'У вас не продаётся такая машина',
            'convertation_sub_string': '~',
            'uzbekistan_valute': 'X сум'
        }

LEXICON = SafeDict(LEXICON)




class LexiconSellerRequests:
    backward_from_delete_in_feedbacks = {'viewed_feedbacks': 'Назад'}

    seller_sure_delete_car_ask = {'message_text': 'Вы уверены что хотите удалить с витрины машину №X ?',
                                  'buttons': {"i'm_sure_delete": 'Удалить', 'backward_from_delete_car_menu': 'Назад', 'width': 1}}
    seller_does_have_active_requests_alert = 'У вас нет активных заявок'
    seller_does_have_active_car_by_brand = 'Эта марка не актуальна.'
    matched_advert = 'У вас в каталоге уже имеется идентичное объявление, повторно не выложить!'
    select_brand_message_text = {'message_text': 'Выберите марку автомобиля'}
    callback_prefix = 'seller_requests_brand:'
    # backward_button = {'backward:sales_brand_choose': 'Назад'}
    keyboard_end_part = {'backward:sales_brand_choose': 'Назад'}
    # choose_brand_keyboard_width = 1
    return_to_requests_buttons = {'buttons': {'backward:rewrite_price_by_seller': 'К заявкам', 'width': 1}}
    input_new_price = {'message_text': 'Введите новую стоимость.\nНынешняя цена: X', **return_to_requests_buttons}
    input_new_price_incorrect_message_text = '\nПожалуйста, укажите целочисленное значение.'
    input_new_price_car_dont_exists = {'message_text': 'К сожалению автомобиль снят с продажи.\nИли введено большое число.', **return_to_requests_buttons}
    succes_rewrite_price = {'message_text': 'Цена успешно изменена', **return_to_requests_buttons}

    pagination_vectors = {'seller_requests_pagination_left': '←', 'seller_requests_pagination_right': '→'}

    selected_brand_output_buttons = {'buttons': {**pagination_vectors,
                                                 'rewrite_price_by_seller': 'Изменить цену',
                                                'withdrawn': 'Удалить из каталога',
                                                'backward:sales_order_review': 'Назад', 'width': (2, 1, 1, 1)}}

    check_viewed_feedbacks_buttons = {'buttons': {**pagination_vectors,
                                               'withdrawn': 'Снять с продажи', 'deal_fell_through': 'Сделка сорвалась',
                                               'backward:check_feedbacks': 'Назад', 'width': (2, 2, 1)}}

    check_new_feedbacks_buttons = {'buttons': {**pagination_vectors,
                                               'backward:check_feedbacks': 'Назад', 'width': (2, 1)}}

    output_car_request_header = '<b>Заявка <i>№_</i></b>'
    commodity_state = '\nСостояние: <i>X</i>'
    engine_type = '\nТип двигателя: <i>X</i>'
    commodity_brand = '\nМарка: <i>X</i>'
    commodity_model = '\nМодель: <i>X</i>'
    commodity_complectation = '\nКомплектация: <i>X</i>'
    commodity_year_of_realise = '\nГод выпуска: <i>X</i>'
    commodity_mileage = '\nПробег: <i>X</i>'
    commodity_color = '\nЦвет: <i>X</i>'
    commodity_price = '\n<b>Стоимость: <i>X</i></b>'

    pagination_pagesize = 1

    page_view_separator = 'Страница: '

    pages_were_end = 'Страницы кончились'
    new_feedbacks_not_found = 'У вас не появилось новых откликов'
    viewed_feedbacks_not_found = 'У вас нет просмотренных откликов'

    did_you_sure_to_delete_feedback_ask = {'message_text': 'Вы уверены удалить отклик №X ?',
                                           'buttons': {"i'm_sure_delete_feedback": 'Подтвердить', 'backward_from_delete_feedback_menu': 'Назад', 'width': 1}}
    success_delete = 'Удалено'



class LexiconSellerProfile:
    header = '<b>Профиль продавца</b>\n\n'
    dealership_prefix = 'Юридическое лицо 🤵🏻‍♂️'
    seller_prefix = 'Частное лицо 👨🏻‍💼\n'
    dealership_name_prefix = 'Название автосалона: <i>X</i>'
    dealership_address_prefix = 'Адрес автосалона: <i>X</i>'
    seller_name_prefix = 'Ф.И.О продавца: <i>X</i>'
    phonenumber_prefix = 'Телефонный номер: <i>X</i>'

    tariff_prefix = '\n<blockquote>💰 Тариф: <i>X</i></blockquote>'
    tariff_out_date_prefix = '\nДо <i>X</i>'
    residual_feedback_prefix = '\n<blockquote>📥 Остаток откликов: <i>X</i></blockquote>'
    tariff_extension_button = {'tariff_extension': 'Продлить тариф ✅'}
    width = 1
    tariff_store_button = {'tariff_extension': 'Каталог тарифов 🎫'}
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
    name = '\n<blockquote>🪪 Название: <i>X</i></blockquote>'
    price = '\n<blockquote>💰 Стоимость: <i>X</i></blockquote>'
    duration_time = '\n<blockquote>🕰 Срок действия: <i>X</i></blockquote>'
    feedback_amount = '\n<blockquote>📛 Лимит отзывов: <i>X</i></blockquote>'
    separator = '—' * 13
    low_separator = '—' * 7
    buttons = {'start_choose_payment_method': 'Выбор платёжной системы', 'backward:tariff_preview': 'Назад', 'width': 1}

class LexiconChoicePaymentSystem:
    message_text = 'Выберите платёжную систему'
    payment_click = {'run_tariff_payment:click': '💷 CLICK'}
    payment_payme = {'run_tariff_payment:payme': '💴 PayMe'}
    payment_uzumPay = {'run_tariff_payment:uzumPay': '💶 UzumPay'}
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
    width_parameter = {'width': 1}