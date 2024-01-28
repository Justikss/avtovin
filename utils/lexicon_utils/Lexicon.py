from abc import ABC

from config_data.config import faq, faq_buyer_ru, faq_seller_ru, max_phone_number_len
# from config_data.config import
from utils.lexicon_utils.admin_lexicon.admin_catalog_lexicon import __CATALOG_LEXICON, catalog_captions
from utils.lexicon_utils.admin_lexicon.advert_parameters_lexicon import __ADVERT_PARAMETERS_LEXICON
from utils.lexicon_utils.admin_lexicon.bot_statistics_lexicon import __STATISTIC_LEXICON, statistic_captions
from utils.lexicon_utils.lexicon_uz.admin_lexicon_uz.admin_lexicon_uz import ADMIN_LEXICON_uz
from utils.lexicon_utils.lexicon_uz.admin_lexicon_uz.advert_action_lexicon_uz import ADVERT_LEXICON_UZ
from utils.lexicon_utils.lexicon_uz.admin_lexicon_uz.advert_parameters_uz import ADVERT_PARAMETERS_LEXICON_UZ
from utils.lexicon_utils.lexicon_uz.admin_lexicon_uz.bot_statistic_uz import STATISTIC_LEXICON_UZ, statistic_captions_uz
from utils.lexicon_utils.lexicon_uz.admin_lexicon_uz.catalog_lexicon_uz import CATALOG_LEXICON_UZ, catalog_captions_uz
from utils.lexicon_utils.lexicon_uz.lexicon_uz import LEXICON_UZ, money_valute, \
    max_price_len, max_contact_info_len, lexicon_uz, captions_uz
from utils.safe_dict_class import SafeDict
from utils.lexicon_utils.admin_lexicon.admin_lexicon import __ADMIN_LEXICON
from utils.lexicon_utils.admin_lexicon.advert_action_lexicon import __ADVERT_LEXICON

captions = {'backward': '◂ Назад ▸', 'was_selected': 'Вы выбрали', 'cancel': 'Отменить', 'confirm': 'Подтвердить',
            'sales': 'продажам', 'purchases': 'покупкам', 'any': 'всё время', 'day': 'день', 'week': 'неделю',
            'month': 'месяц', 'year': 'год', 'days': 'дней', 'feedbacks': 'откликов',
            'dont_write_html_tags': 'Запрещён ввод знаков "&lt; &gt;".',
            'all_users': 'всех', 'buyers': 'покупателей', 'sellers': 'продавцов', 'delete': 'Удалить',
            'by_dealership': 'автосалона',
            'by_seller': 'частного лица', 'close': 'Скрыть', 'surname_name_patronymic': 'ФИО: ', 'add': 'Добавить',
            'successfully': 'Успешно', 'tech_support_entity': '👨🏻‍💻Сотрудник поддержки: {SUPPORT_NUMBER}\n',
            'supports_pattern': f'''{' ' * 25 + '───────────────'}\n<blockquote>{'{0}'}</blockquote>\n{' ' * 25 + '───────────────'}'''
            }
low_sep = '────────'
__LEXICON = {
            'callback_spam_detected': 'От замечена злоумышленная интенсивность нажатия на кнопки.\nВы можете продолжить взаимодействие с ботом через {time} секунд.',
            'spam_passed': 'Блокировка чата прошла.\nМожете продолжить общение с ботом.',
            'spam_detected': 'От вас замечена злоумышленная интенсивность отправки сообщений.\nВы сможете снова писать в чат через {time} секунд.',
            'address_was_not_found': 'Адрес не найден',
            # 'seller_cant_see_offer': 'К сожалению, продавец не сможет увидеть вашей заявки.'
            'cant_buy_yourself': 'Вы не можете купить товар у самого себя',
            'you_are_blocked_alert': 'Вы заблокированы в данной деятельности',
            'sepp': '—',
            'tariff_non_actuallity': 'Вам следует приобрести тариф!',
            'awaiting_process': 'Ожидайте',
            'new_recommended_offer_startswith': 'Поступило новое предложение:',
            'make_choose_brand': 'Выберите марку:',
            'buyer_havent_recommendated_offers': 'Список рекомендованных объявлений пуст!',
            'active_offers_non_exists': 'Список активных предложений пуст.',
            "buyer_haven't_cached_requests": 'История недавно просмотренных пуста.',
            'incoming_address_caption': 'Указанный адрес:\n',
            'address': 'Адрес',
            'waiting_request_process': "Ваш запрос обрабатывается. Примерное время ожидания: {time} {seconds}",
            'cached_requests_for_buyer_message_text': {
                'message_text': 'Просмотр неподтверждённых вами предложений\n'},
            'active_offers_for_buyer_message_text': {
                'message_text': 'Просмотр активных предложений\n'},
            'recommended_offers_for_buyer_message_text' : {
                'message_text': 'Просмотр рекомендованных предложений\n'},
            'backward_from_buyer_offers': {'buyer_requests': '◂ Назад ▸'},
            'output_inline_brands_pagination': {'inline_buttons_pagination:-': '←', 'page_count': '[C/M]', 'inline_buttons_pagination:+': '→'},
            'confirm_from_buyer': {'separator': '=' * 40, 'non_data_more': 'Нет данных для отображения'},
            'start_registration': 'Пройдите регистрацию!',
            'unexpected_behavior': 'Неожиданное поведение',
            'car_was_withdrawn_from_sale': 'Автомобиль был снят с продажи',
            'car_search_parameters_incactive': 'Данные параметры поиска больше неактивны. Пожалуйста обновите их.',
            'seller_dont_exists': 'Продавец больше неактивен',
            'search_parameter_invalid': 'Данный параметр не актуален',
            'order_was_created': 'Вы откликнулись! Теперь в объявлении указан контакт продавца,\nТак же пополнен список ваших предложений!',
            'too_late': 'Вы опоздали',
            'success_notification': 'Принято',
            'seller_lose_self_tariff_notification': {'message_text': 'Вы не успели продлить свой тариф!\nИстория вашей коммерческой деятельности была удалена.\nОформите новый тариф чтобы продолжить продавать у нас!',
                                        'buttons': {'tariff_extension': 'Каталог тарифов ✅', 'close_seller_notification_by_redis:delete_tariff': 'Скрыть уведомление.', 'width': 1}},
            'seller_without_tariff_notification': {'message_text': 'Ваш тариф потрачен,\nпо истечению суток ваш каталог товаров и история откликов будут очищены, во избежание этого случая\nвам следует приобрести тариф снова!',
                                                   'buttons': {'tariff_extension': 'Продлить тариф ✅', 'close_seller_notification_by_redis:lose_tariff': 'Скрыть уведомление.', 'width': 1}},
            'user_in_system': {'message_text': 'Вы в системе'},
            'choose_language': {'message_text': 'Tilingizni tanlang\nВыберите ваш язык', 'language_uz': '🇺🇿 Uzb',
                                'language_ru': "🇷🇺 Rus", 'width': 2},
            'hello_text': {'message_text': '<b>Привет <i>{user_name}</i></b>!\nУ нас ты можешь купить или продать своё авто.\nВыбери один из пунктов ниже 👇🏼', 'start_sell': 'Продажа 👨🏻‍💼',
                           'start_buy': '👨🏻‍💻 Покупка', 'width': 2},
            'write_full_name': {'message_text': 'Укажите ФИО', 'backward:user_registration': '◂ Назад ▸', 'width': 1},
            'write_full_name(exists)': 'Это имя уже зарегестрировано\nожидается иное',
            'write_full_name(novalid)': f'Некорректный ввод, принимается 2-3 буквенных слова, разделённые пробелом\nДлиной до {max_contact_info_len} символов.',
            'write_phone_number': {'message_text': 'Введите ваш номер телефона:',
                                   'backward:user_registration_number': '◂ Назад ▸', 'width': 1},
            'write_phone_number(novalid)': f'<b>Некорректный ввод номера</b>\nПроверьте правильность своего номера\nПринимаются только цифры, пробелы и знак + .\nС максимальным количеством символов: {max_phone_number_len}.',
            'write_phone_number(exists)': '<b>Некорректный ввод номера!</b>\nОн уже зарегистрирован\nожидается иной',
            'write_phone_number(banned)': 'Данный номер телефона заблокирован на площадке покупателей\nПожалуйста введите новый:',
            # 'most_answers': {'message_text': 'Ответы на часто задаваемые вопросы', 'in_main': 'В меню', 'width': 1},
            'main_menu': {'message_text': 'Меню покупателя 👨🏻‍💻\nВыберите ваше действие:', 'buyer_requests': 'Предложения 📋', 'car_search': '🚘 Поиск Авто',
                          'faq': 'Инструкции 💬', 'support': '🌐 Поддержка', 'backward:set_language': '◂ Назад ▸ ', 'width': 2},
            'buyer_requests': {'message_text': '<b>Список предложений:</b>', 'buttons': {'buyer_cached_offers': '🚫 Неподтверждённые ({non_confirmed})', 'buyer_active_offers': '✅ Подтверждённые ({confirmed})', 'buyers_recommended_offers': '🔥 Новые ({new})', 'return_main_menu': 'В Меню', 'width': 1}},
            'f_a_q': {'message_text': f'Ответы на часто задаваемые вопросы: \n\nДля ознакомления с устройством купле-продажи в боте, выберите кнопки ниже.\n{faq}', 'seller_faq': 'Продажа 👨🏻‍💼', 'buyer_faq': '👨🏻‍💻 Покупка',
                      'return_main_menu': '◂ Назад ▸', 'width': 2},
            'tech_support': {'message_text': 'Выберите ваше действие:', 'write_to_support': 'Написать 💬',
                             'call_to_support': 'Позвонить 📱', 'width': 2, 'return_main_menu': '◂ Назад ▸'},
            'write_to_support': {'message_text': 'Вы можете связаться с нами по телеграм:', 'backward:support': '◂ Назад ▸', 'width': 1},
            'call_to_support': {'message_text': 'Вы можете позвонить нам по следующим номерам:\n', 'backward:support': '◂ Назад ▸', 'width': 1},

            'search_car': {'message_text': 'Выберите тип автомобиля:', 'choose_state_1': 'Новое', 'choose_state_2': 'С пробегом',
                           'return_main_menu': '◂ Назад ▸', 'width': 2},
            'cars_not_found': {'message_text': 'К сожалению автомобилей этого класса нет на витрине.',
                               'backward:choose_car_category': '◂ Назад ▸', 'return_main_menu': '🏡 В Меню 🏡', 'width': 1},

            'search_configuration': {'message_text': 'Настройте ваш поиск', 'start_configuration_search': 'Начать',
                                     'backward': '◂ Назад ▸', 'width': 1},
            'footer_for_output_active_offers': {'viewed_status': 'Статус просмотра продавцом: ', 'status_true': 'Просмотрено ✅', 'status_false': 'Не просмотрено ❌'},
            'active_offer_caption': '<b>Активная заявка:</b>',
            'chosen_configuration': {
                'message_text': {'phone_number': '\nМобильный телефон: ',
                                'your_configs': '<b>Предложения по вашему запросу:</b>',
                                 'from_seller': '<b>От Продавца: </b>\n<i>{seller_name}</i>',
                                 'from_dealership': '<b>От Автосалона: </b>\n<i>{dealership_name}</i>\nПо Адресу: <i>{dealership_address}</i>',
                                 'car_state': 'Состояние: <i>X</i>',
                                 'engine_type': 'Тип двигателя: <i>X</i>',
                                 'model': 'Модель: <i>X</i>',
                                 'brand': 'Марка: <i>X</i>', 'complectation': 'Комплектация: <i>X</i>',
                                 'cost': f'<blockquote><b>Cтоимость: <i>X {money_valute}</i></b></blockquote>', 'mileage': 'Пробег: <i>X</i>', 'year': 'Год: <i>X</i>',
                                 'color': 'Цвет: <i>X</i>'}, 'buyer_car_pagination:-': '←', 'buyer_car_pagination:+': '→',
                'confirm_buy_settings:': '✓ Подтвердить ✓', 'backward_in_carpooling': '⚙️ Изменить ⚙️',
                'buy_search_price_filter': 'Фильтровать по цене', 'return_main_menu': '🏡 В меню 🏡',
                'width': (2, 1, 1, 1, 1)},

            'confirm_buy_configuration': {'message_text': 'Вы успешно оставили заявку!\nВам поступит уведомление о её одобрении.',
                                          'return_main_menu': '🏡 В Меню 🏡', 'width': 1},
            'buy_configuration_error': {'message_text': 'У вас уже оставлена такая заявка.',
                                        'return_main_menu': '🏡 В Меню 🏡', 'width': 1},
            'simultaneous_announcements_was_over': 'Вы попытались превысить лимит одновременно опубликованных объявлений\nУ вас уже {advert_count} из {advert_count} объявлений.',
            'user_non_registration': {'message_text': 'Ошибка. Ваш аккаунт незарегестрирован\nНажмите /start'},

            'notification_from_seller_by_buyer_buttons': {'my_sell_feedbacks:': 'Смотреть отклики', 'close_seller_notification:': 'Скрыть уведомление', 'width': 1},


            'confirm_from_seller': {'message_text': {'feedback_header': '<b>Отлкик №{feedback_number}</b>', 'from_user': 'Пользователь <i>{from_user}</i>', 'tendered': 'Оставил отклик на заявку <i>№{advert_number}</i> :',
                                    'contacts': '<b>Контакты:</b>\n<i>{name}</i>\n{phone}', 'separator': ' ' *10 + '—' * 5}, 'confirm_button': 'Подтвердить ✅'},

            'backward_name': '◂ Назад ▸',
            "seller_haven't_this_car": 'У вас не продаётся такой автомобиль',
            'separator': '='*40,

            'who_is_seller': {'message_text': 'Выберите пункты ниже:', 'i_am_private_person': 'Частное лицо 👨🏻', 'i_am_car_dealership': 'Автосалон 🚘', 'backward:set_language': '◂ Назад ▸', 'width': 2},
            'write_full_seller_name': {'message_text': 'Укажите ФИО', 'backward:seller_registration_seller_person_name': '◂ Назад ▸', 'width': 1},
            'write_full_seller_name(novalid)': {
                'message_text': f'Некорректный ввод, принимается 2-3 буквенных слова, разделённые пробелом\nДлиной до {max_contact_info_len} символов.',
                'backward:seller_registration_seller_person_name': '◂ Назад ▸', 'width': 2},
            'write_full_seller_name(exists)': {'message_text': 'Это имя уже зарегистрировано\nожидается иное', 'backward:seller_registration_seller_person_name': '◂ Назад ▸', 'width': 1},

            'write_dealership_name': {'message_text': 'Введите название автосалона:', 'backward:seller_registration_dealership_name': '◂ Назад ▸', 'width': 1},
            'write_dealership_name(novalid)': f'Название автосалона должно быть длинной менее {max_contact_info_len} символов\nИ состоять только из букв и цифр:',
            'write_dealership_name(exists)': 'Это название уже зарегестрировано\nожидается иное',

            'write_seller_phone_number': {'message_text': 'Введите ваш номер телефона:',
                                   'backward:seller_registration_number': '◂ Назад ▸', 'width': 1},
            'write_seller_phone_number(novalid)': f'<b>Некорректный ввод номера.</b>\nПроверьте правильность своего номера\nПринимаются только цифры, пробелы и знак + .\nС максимальным количеством символов: {max_phone_number_len}.',
            'write_seller_phone_number(exists)': '<b>Некорректный ввод номера!</b>\nОн уже зарегистрирован\nожидается иной',
            'write_seller_phone_number(banned)': '<b>Данный номер телефона заблокирован на площадке продавцов</b>\nПожалуйста введите новый:',

            'write_dealership_address': {'message_text': 'Введите адрес автосалона\nИли отправьте вашу геолокацию\n(значок скрепки в левом углу чата)', 'backward:seller_registration_dealership_address': '◂ Назад ▸', 'width': 1},
            'write_dealership_address(novalid)': {'message_text': f'Ошибка\n Адрес автосалона должен содержать буквы\nи содержать менее {max_contact_info_len} символов', 'backward:seller_registration_dealership_address': '◂ Назад ▸', 'width': 1},


            'checking_seller_entered_data': {'message_text': 'Введённые данные корректны?\n(Нажмите на поле для его переписи)', 'rewrite_seller_name': '', 'rewrite_seller_number': '', 'rewrite_dealership_address': '', 'confirm_registration_from_seller': 'Подтвердить ✅', 'width': 1},
            'confirm_registration_from_seller': {'message_text': 'Регистрация завершена\nДождитесь уведобления об одобрении от администрации.', 'start_sell': 'Меню продавца 👨🏻‍💼', 'width': 1},
            'try_again_seller_registration': {'message_text': 'Ошибка.\nдля подробностей перепройдите процесс регистрации.', 'return_to_start_seller_registration': 'Перепройти регистрацию', 'width': 1},

            'confirm_seller_profile_notification': {'message_text': '✅ Успешно, профиль продавца подтверждён!', 'buttons': {'seller_main_menu': 'В меню продавца 👨🏻‍💼', 'close_seller_notification_by_redis:seller': captions['close'], 'width': 1}},

            'seller_main_menu': {'message_text': 'Меню продавца 👨🏻‍💼\nВыберите ваше действие:', 'seller_pofile': 'Профиль 📱', 'seller_requests': '📋 Заявки', 'support': 'Поддержка 🌐', 'faq': '💬 Инструкции', 'backward:set_language': '◂ Назад ▸', 'width': 2},

            'confirm_new_seller_registration_from_admin_button': {'confirm_from_admin': 'Подтвердить ✅', 'callback_startswith': 'confirm_new_seller_registration_from:'},

            'seller_waiting_registration_confirm': {'start_text_legal': '<b>Заявка на регистрацию автосалона:</b>\n{username}\nПо адресу:\n{address}\n', 'start_text_natural': '<b>Заявка на регистрацию частного продавца:</b>\n{username}\n',
                                                 'legal_body_header': '─' * 8 + '\n<blockquote>Название автосалона: <i>{dealership_name}</i>\n',
                                                  'natural_body_header': '─' * 8 + '\n<blockquote>Имя: <i>{name}</i>\nФамилия: <i>{surname}</i>\nОтчество: <i>{patronymic}</i>\n',
                                                   'body': 'Номер: {phone_number}</blockquote>\n' + '─' * 8},

            'success_seller_registration_notice': {'message_text': 'Вы зарегистрированы в системе', 'return_main_menu': 'В меню продавца 👨🏻‍💼', 'width': 1},

            'seller_faq': {'message_text': faq_seller_ru, 'faq': '◂ Назад ▸', 'return_main_menu': '🏡 В Меню 🏡', 'width': 1},
            'buyer_faq': {'message_text': faq_buyer_ru, 'faq': '◂ Назад ▸', 'return_main_menu': '🏡 В Меню 🏡', 'width': 1},

            'seller_requests': {'message_text': '<b>Раздел работы с заявками</b>\nВыберите ваше действие:', 'create_new_seller_request': '📨 Создать объявление', 'my_sell_requests': '💰 Мои объявления', 'my_sell_feedbacks': '🔸 Отклики', 'return_main_menu': 'В Меню', 'width': 1},


            'confirm_load_config_from_seller_button': {'confirm_load_config_from_seller': '✓ Подтвердить ✓', 'edit_boot_car_data': '⚙️ Изменить ⚙️', 'return_main_menu': '🏡 В Меню 🏡', 'width': 1},
            'seller_load_notification_button': {'return_main_menu': '🏡 В Меню 🏡'},

            'message_not_digit': f'<b>Сумма должна состоять только из одного числа, длиной до {max_price_len} цифр</b>',
            'message_not_photo': 'Прикрепите фотографию\n(значок скрепки в левом углу чата)\nНе отменяйте сжатие при отправке\nфотографии в телеграм',

            'seller_start_delete_request': {'message_text': 'Введите номер удаляемой заявки', 'buttons': {'backward:seller_start_delete_request': '◂ Назад ▸', 'width': 1}},

            'incorrect_input_removed_car_id': 'Неверный ввод номера заявки.\nСверьте номер по кнопке "◂ Назад ▸" и введите снова.',
            'confirm_delete_request': {'message_text': 'Вы действительно хотите удалить это авто?', 'confirm_delete': 'Подтвердить ✅', 'backward:seller_delete_request': '◂ Назад ▸', 'width': 1},

            'seller___my_feedbacks': {'message_text': 'Мои отклики', 'buttons': {'new_feedbacks': '✓ Новые ✓', 'viewed_feedbacks': '👁 Изученные 👁', 'backward:seller__my_feedbacks': '◂ Назад ▸', 'width': 2}},
            'return_main_menu_button': {'return_main_menu': '🏡 В Меню 🏡'},

            'buyer_price_filter_review': {'message_text': {'default': '<b>Фильтрация по стоимости:</b>\n', 'selected_caption': 'Выбрано:\n',
                                                     'min_caption': 'От {price}\n', 'max_caption': 'До {price}\n'},
                                    'buttons': {
                'buyer_cost_filter:from': 'От', 'buyer_cost_filter:before': 'До',
                'set_buyer_cost_filter': 'Применить фильтр', 'remove_buyer_cost_filter': 'Отменить фильтр',
                'width': 2
            }},
            'buyer_price_filter_start_input': {'message_text': '<b>Возможный диапазон фильтра стоимости:'
                                                               '\nОт {min_cost}'
                                                               '\nДо {max_cost}.</b>'
                                                               '\nВведите сумму для фильтрации объявлений\n{default_side_name}:',
                                               'buttons': {
                                                   'backward:input_request_b_cost_filter': captions['backward'],
                                                   'width': 1
                                               }},
            'buyer_price_filter_input_confirmation': {'message_text': '<b>Добавить в фильтрацию объявлений диапазон цен\n{from_or_before}: {cost}</b>',
                                                      'buttons': {
                                                          'confirm_add_buyer_price_filter_part': captions['confirm'],
                                                          'rewrite_buyer_price_filter': 'Ввести заново',
                                                          'cancel_buyer_price_filter': captions['cancel'],
                                                          'width': 1
                                                      }},
            'price_incorrect': f'<b>Стоимость должна состоять из одного числа(до {max_price_len} цифр)</b>\nВозможен ввод со знаком " $ "',
            'price_not_in_range': '<b>Введённая стоимость выходит за приделы текущей выборки.</b>',
            'nominative_case_cost_side_from': 'Минимальная',
            'nominative_case_cost_side_before': 'Максимальная',
            'from_caption': 'От',
            'before_caption': 'До',
            'incorrect_nearest_price': '<b>Ваша настройка фильтрации не выбрала ни одного объявления.\nБлижайшая к вашему диапазону стоимость: {nearest_price}</b>',
            'filter_made_null_list': '',

            'retry_now_allert': 'Попробуйте снова',
            'user_havent_permision': 'У вас нет прав',
            'seller_without_tariff': 'У вас нет откликов на счету',
            'seller_tarriff_expired': 'Ваш тариф неактуален',
            'non_actiallity': 'Не актуально',
            'successfully': 'Успешно',
            'seller_does_have_this_car': 'У вас не продаётся такая машина',
            'convertation_sub_string': '~',
            'uzbekistan_valute': 'X сум',
            'other_caption': 'Другой',
            'color_caption': 'Цвет'
        }



ADMIN_LEXICON = SafeDict({'ru': __ADMIN_LEXICON,
                          'uz': ADMIN_LEXICON_uz})
CATALOG_LEXICON = SafeDict({'ru': __CATALOG_LEXICON,
                            'uz': CATALOG_LEXICON_UZ})
ADVERT_PARAMETERS_LEXICON = SafeDict({'ru': __ADVERT_PARAMETERS_LEXICON,
                                      'uz': ADVERT_PARAMETERS_LEXICON_UZ})
STATISTIC_LEXICON = SafeDict({'ru': __STATISTIC_LEXICON,
                              'uz': STATISTIC_LEXICON_UZ})

ADVERT_LEXICON = SafeDict({'ru': __ADVERT_LEXICON,
                           'uz': ADVERT_LEXICON_UZ})
LEXICON = SafeDict({'ru': __LEXICON,
                    'uz': LEXICON_UZ})
catalog_captions = SafeDict({'ru': catalog_captions,
                            'uz': catalog_captions_uz})

statistic_captions = SafeDict({'ru': statistic_captions,
                            'uz': statistic_captions_uz})

captions = SafeDict({'ru': captions,
                     'uz': captions_uz})

lexicon_ru = {
    'make_empty_field': 'Пропустить',
    'residual_simultaneous_announcements': '\n📗 Доступые места активных объявлений: <i>{}</i>',
    'simultaneous_announcements': '\n📗 Лимит активных объявлений: <i>{}</i>',
    'incorrect_price_$': "<b>Стоимость должна содержать не более одного знака ' $ '</b>",
    'infinity_feedbacks_caption': 'бесконечно',
    'free_cost': 'бесплатно',
    'to_offers': 'К заявкам',
    'backward_in_carpooling': '◂ Назад ▸',
    'choose_engine_type_text': 'Выберите тип двигателя',
    'choose_brand_text': 'Выберите марку',
    'choose_model_text': 'Выберите модель',
    'choose_complectation_text': 'Выберите комплектацию',
    'choose_year_text': 'Выберите год',
    'choose_mileage_text': 'Выберите пробег',
    'choose_color_text': 'Выберите цвет',
    'seller_sure_delete_car_ask_text': 'Вы уверены что хотите удалить с витрины машину №{number} ?',
    'seller_does_have_active_requests_alert': 'У вас нет активных заявок',
    'seller_does_have_active_car_by_brand': 'Эта марка не актуальна.',
    'matched_advert': 'У вас в каталоге уже имеется идентичное объявление, повторно не выложить!',
    'select_brand_message_text': 'Выберите марку автомобиля',
    'input_new_price': 'Введите новую стоимость.\nНынешняя цена: {current_price}',
    'input_new_price_incorrect_message_text': f'<b>Пожалуйста, укажите одно число, длиной до {max_price_len} цифр.</b>',
    'input_new_price_car_dont_exists': 'К сожалению автомобиль снят с продажи.',
    'succes_rewrite_price': 'Цена успешно изменена',
    'commodity_output_block': '''───────────────
<blockquote>Состояние: <i>{state}</i>
Тип двигателя: <i>{engine_type}</i>
Марка: <i>{brand_name}</i>
Модель: <i>{model_name}</i>
Комплектация: <i>{complectation}</i>
Год выпуска: <i>{year_of_release}</i>
Пробег: <i>{mileage}</i>
Цвет: <i>{color}</i></blockquote>
───────────────''',

    'output_car_request_header': 'Заявка <i>№{request_number}</i>',
    'commodity_state': 'Состояние: <i>{state}</i>',
    # ... И так далее для всех остальных текстов

    'commodity_brand': 'Марка: <i>{brand}</i>',
    'commodity_model': 'Модель: <i>{model}</i>',
    'commodity_complectation': 'Комплектация: <i>{complectation}</i>',
    'commodity_year_of_realise': 'Год выпуска: <i>{year_of_release}</i>',
    'commodity_mileage': 'Пробег: <i>{mileage}</i>',
    'commodity_color': 'Цвет: <i>{color}</i>',
    'commodity_price': '<b>Стоимость: <i>{price}</i></b>',
    'pages_were_end': 'Страницы кончились',
    'new_feedbacks_not_found': 'У вас не появилось новых откликов',
    'viewed_feedbacks_not_found': 'У вас нет просмотренных откликов',
    'did_you_sure_to_delete_feedback_ask': 'Вы уверены удалить отклик №{feedback_number} ?',
    'success_delete': 'Удалено',
    'profile_header': '<b>Профиль продавца</b>\n\n',
    'dealership_prefix': 'Юридическое лицо 🤵🏻‍♂️',
    'seller_prefix': 'Частное лицо 👨🏻‍💼\n',
    'dealership_name_prefix': 'Название автосалона: <i>{dealership_name}</i>',
    'dealership_address_prefix': 'Адрес автосалона: <i>{dealership_address}</i>',
    'seller_name_prefix': 'Ваше имя: <i>{seller_name}</i>',
    'phonenumber_prefix': 'Телефонный номер: {phone_number}',
    'tariff_block': '<blockquote>💰 Тариф: <i>{tariff_name}</i>\n🕰 До окончания подписки: <i>{days_remaining} Дней</i>\n🔸 Откликов: <i>{feedbacks_remaining}</i>{simultaneous_announcements_caption}{cost_caption}</blockquote>',
    'tariff_out_date_prefix': '<blockquote>🕰 До окончания подписки: <i>{days_remaining} Дней</i></blockquote>',
    'residual_feedback_prefix': '<blockquote>🔸 Остаток откликов: <i>{feedbacks_remaining}</i></blockquote>',
    'tariff_expired': 'Ваш тариф истёк',
    'tariff_selection_not_found_message_text': 'Тарифов не найдено',
    'tariff_selection_message_text': 'Все доступные тарифы',
    'selected_tariff_preview_header': '<b>Информация о тарифе:</b>',
    'tariff_name': '<blockquote>🪪 <b>Название: <i>{tariff_name}</i></b></blockquote>',
    'tariff_price': '\n💰 <b>Стоимость: <i>{tariff_price}</i></b>',
    'tariff_duration_time': '<blockquote>🕰 <b>Срок действия: <i>{tariff_duration} дней</i></b></blockquote>',
    'tariff_feedback_amount': '<blockquote>🔸 <b>Лимит откликов: <i>{tariff_feedback_limit}</i></b></blockquote>',
    'choice_payment_system_message_text': 'Выберите платёжную систему',
    'create_invoice_in_progress_notification': 'В разработке',
    'create_invoice_title': 'Оформление тарифа',
    'create_invoice_description': 'Подписка на {feedbacks_amount} откликов покупателей.\nПериодом {subscription_days} дней.',
    'create_invoice_load_price_label': 'Цена за тариф',
    'payment_operation_error_text': 'Ошибка оплаты, попробуйте снова, соблюдая тайм аут в 15 минут',
    'payment_operation_success_text': 'Удачно!',
    'payment_operation_cancel_button': '🚫 Отмена 🚫',
    'tariff_extension_button': 'Продлить тариф ✅',
    'tariff_store_button': 'Каталог тарифов 🎫',
    'confirm': 'Подтвердить ✅',
    'delete': 'Удалить',
    'rewrite_price_by_seller': 'Изменить цену',
    'withdrawn': 'Снять с продажи',
    'deal_fell_through': 'Сделка сорвалась',
    'page_view_separator': 'Страница: ',
    'tariff_prefix': '<blockquote>💰 Тариф: <i>X</i></blockquote>',
    'tarif_expired': 'Ваш тариф истёк',
    'start_choose_payment_method': 'Выбор платёжной системы',
    'offer': '<b>Заявка <i>№{offer_number}</i></b>'

}


class_lexicon = SafeDict({'ru': lexicon_ru,
                          'uz': lexicon_uz})




class LastButtonsInCarpooling(ABC):
    def __init__(self):
        self.last_buttons = {'backward_in_carpooling': class_lexicon['backward_in_carpooling'],
                            **LEXICON['return_main_menu_button']}
        self.buttons_callback_data = None
        self.width = 2
        self.message_text = ''
        self.dynamic_buttons = 2

class BaseOptionalField(LastButtonsInCarpooling, ABC):
    def __init__(self):
        super().__init__()
        self.last_buttons = {'empty_field_carpooling': class_lexicon['make_empty_field'], **self.last_buttons}
        self.dynamic_buttons = 3
class ChooseEngineType(LastButtonsInCarpooling):
    def __init__(self):
        super().__init__()
        self.message_text = class_lexicon['choose_engine_type_text']
        self.buttons_callback_data = 'cars_engine_type_'
        self.width = 2

class ChooseBrand(LastButtonsInCarpooling):
    def __init__(self):
        super().__init__()

        self.message_text = class_lexicon['choose_brand_text']
        self.buttons_callback_data = 'cars_brand_'
        self.last_buttons = None

class ChooseModel(LastButtonsInCarpooling):
    def __init__(self):
        super().__init__()

        self.message_text = class_lexicon['choose_model_text']
        self.buttons_callback_data = 'cars_model_'
        self.last_buttons = None

class ChooseComplectation(BaseOptionalField):
    def __init__(self):
        super().__init__()

        self.message_text = class_lexicon['choose_complectation_text']
        self.buttons_callback_data = 'cars_complectation_'
        self.last_buttons = None

class ChooseYearOfRelease(BaseOptionalField):
    def __init__(self):
        super().__init__()

        self.message_text = class_lexicon['choose_year_text']
        self.buttons_callback_data = 'cars_year_of_release_'
        self.last_buttons = None

class ChooseMileage(BaseOptionalField):
    def __init__(self):
        super().__init__()

        self.message_text = class_lexicon['choose_mileage_text']
        self.buttons_callback_data = 'cars_mileage_'
        self.last_buttons = None

class ChooseColor(BaseOptionalField):
    def __init__(self):
        super().__init__()
        self.message_text = class_lexicon['choose_color_text']
        self.buttons_callback_data = 'cars_color_'

class SecondsEndswith:
    one = 'а'
    two_four = 'ы'


class LexiconSellerRequests:
    def __init__(self):
        self.backward_from_delete_in_feedbacks = {'viewed_feedbacks': class_lexicon['backward_in_carpooling']}

        self.seller_sure_delete_car_ask = {'message_text': class_lexicon['seller_sure_delete_car_ask_text'],
                                      'buttons': {"i'm_sure_delete": class_lexicon['delete'],
                                                  'backward_from_delete_car_menu': class_lexicon['backward_in_carpooling'],
                                                  'width': 1}}
        self.seller_does_have_active_requests_alert = class_lexicon['seller_does_have_active_requests_alert']
        self.seller_does_have_active_car_by_brand = class_lexicon['seller_does_have_active_car_by_brand']
        self.matched_advert = class_lexicon['matched_advert']
        self.select_brand_message_text = {'message_text': class_lexicon['select_brand_message_text']}
        self.callback_prefix = 'seller_requests_brand:'
        self.keyboard_end_part = {'backward:sales_brand_choose': class_lexicon['backward_in_carpooling']}
        self.return_to_requests_buttons = {'buttons': {'backward:rewrite_price_by_seller': class_lexicon['to_offers'],
                                                  'width': 1}}
        self.input_new_price = {'message_text': class_lexicon['input_new_price'], **self.return_to_requests_buttons}
        self.input_new_price_incorrect_message_text = class_lexicon['input_new_price_incorrect_message_text']
        self.input_new_price_car_dont_exists = {'message_text': class_lexicon['input_new_price_car_dont_exists'], **self.return_to_requests_buttons}
        self.succes_rewrite_price = {'message_text': class_lexicon['succes_rewrite_price'], **self.return_to_requests_buttons}

        self.pagination_vectors = {'seller_requests_pagination_left': '←', 'seller_requests_pagination_right': '→'}

        self.selected_brand_output_buttons = {'buttons': {**self.pagination_vectors,
                                                     'rewrite_price_by_seller': class_lexicon['rewrite_price_by_seller'],
                                                    'withdrawn': class_lexicon['withdrawn'],
                                                    'backward:sales_order_review': class_lexicon['backward_in_carpooling'],
                                                     'width': (2, 1, 1, 1)}}

        self.check_viewed_feedbacks_buttons = {'buttons': {**self.pagination_vectors,
                                                   'withdrawn': class_lexicon['withdrawn'], 'deal_fell_through': class_lexicon['deal_fell_through'],
                                                   'backward:check_feedbacks': class_lexicon['backward_in_carpooling'], 'width': (2, 2, 1)}}

        self.check_new_feedbacks_buttons = {'buttons': {**self.pagination_vectors,
                                                   'backward:check_feedbacks': class_lexicon['backward_in_carpooling'], 'width': (2, 1)}}

        self.commodity_output_block = class_lexicon['commodity_output_block']


        self.output_car_request_header = class_lexicon['offer']
        # commodity_state = '\nСостояние: <i>X</i>'
        # engine_type = '\nТип двигателя: <i>X</i>'
        # commodity_brand = '\nМарка: <i>X</i>'
        # commodity_model = '\nМодель: <i>X</i>'
        # commodity_complectation = '\nКомплектация: <i>X</i>'
        # commodity_year_of_realise = '\nГод выпуска: <i>X</i>'
        # commodity_mileage = '\nПробег: <i>X</i>'
        # commodity_color = '\nЦвет: <i>X</i>'
        # commodity_price = '\n<b>Стоимость: <i>X</i></b>'

        self.sep = '─' * 8

        self.pagination_pagesize = 1

        self.page_view_separator = class_lexicon['page_view_separator']

        self.pages_were_end = class_lexicon['pages_were_end']
        self.new_feedbacks_not_found = class_lexicon['new_feedbacks_not_found']
        self.viewed_feedbacks_not_found = class_lexicon['viewed_feedbacks_not_found']

        self.did_you_sure_to_delete_feedback_ask = {'message_text': class_lexicon['did_you_sure_to_delete_feedback_ask'],
                                               'buttons': {"i'm_sure_delete_feedback": class_lexicon['confirm'],
                                                           'backward_from_delete_feedback_menu': class_lexicon['backward_in_carpooling'],
                                                           'width': 1}}
        self.success_delete = class_lexicon['success_delete']


class LexiconSellerProfile:
    def __init__(self):
        self.header = class_lexicon['profile_header']
        self.dealership_prefix = class_lexicon['dealership_prefix']
        self.seller_prefix = class_lexicon['seller_prefix']
        self.dealership_name_prefix = class_lexicon['dealership_name_prefix']
        self.dealership_address_prefix = class_lexicon['dealership_address_prefix']
        self.seller_name_prefix = class_lexicon['seller_name_prefix']
        self.phonenumber_prefix = class_lexicon['phonenumber_prefix']

        self.tariff_block = class_lexicon['tariff_block']
        self.simultaneous_announcements_caption = class_lexicon['residual_simultaneous_announcements']

        self.tariff_prefix = class_lexicon['tariff_prefix']
        self.tariff_out_date_prefix = class_lexicon['tariff_out_date_prefix']
        self.residual_feedback_prefix = class_lexicon['residual_feedback_prefix']
        self.tariff_extension_button = {'tariff_extension': class_lexicon['tariff_extension_button']}
        self.width = 1
        self.tariff_store_button = {'tariff_extension': class_lexicon['tariff_store_button']}
        self.tarif_expired = class_lexicon['tarif_expired']
        self.sep = ' ' * 10 + '─' * 8
        self.infinity_feedbacks_caption = class_lexicon['infinity_feedbacks_caption']

class DateTimeFormat:
    get_string = '%d-%m-%Y %H:%M:%S'

class LexiconTariffSelection:
    def __init__(self):
        self.not_found_message_text = class_lexicon['tariff_selection_not_found_message_text']
        self.message_text = class_lexicon['tariff_selection_message_text']
        self.width = 2
        self.buttons_callback_data = 'select_tariff:'
        self.backward_command = {'backward:affordable_tariffs': class_lexicon['backward_in_carpooling']}

class LexiconSelectedTariffPreview:
    def __init__(self):
        self.header = class_lexicon['selected_tariff_preview_header']
        self.tariff_block = class_lexicon['tariff_block']
        self.simultaneous_announcements_caption = class_lexicon['simultaneous_announcements']
        self.separator = ' ' * 10 + '─' * 8
        self.low_separator = ' ' * 10 + '─' * 8
        self.buttons = {'start_choose_payment_method': class_lexicon['start_choose_payment_method'],
                       'backward:tariff_preview': class_lexicon['backward_in_carpooling'], 'width': 1}

class LexiconChoicePaymentSystem:
    def __init__(self):
        self.message_text = class_lexicon['choice_payment_system_message_text']
        self.payment_click = {'run_tariff_payment:click': '💷 CLICK'}
        self.payment_payme = {'run_tariff_payment:payme': '💴 PayMe'}
        self.payment_uzumPay = {'run_tariff_payment:uzumPay': '💶 UzumPay'}
        self.bottom_buttons = {'backward:choose_payment_system': class_lexicon['backward_in_carpooling'], 'width': 1}
        self.buttons_list = [self.payment_click, self.payment_payme, self.payment_uzumPay, self.bottom_buttons]

class LexiconCreateInvoice:
    def __init__(self):
        self.in_progress_notification = class_lexicon['create_invoice_in_progress_notification']
        self.title = class_lexicon['create_invoice_title']
        self.description = class_lexicon['create_invoice_description']
        self.load_price_label = class_lexicon['create_invoice_load_price_label']

class LexiconPaymentOperation:
    def __init__(self):
        self.error_payment_text = class_lexicon['payment_operation_error_text']
        self.success_payment_text = class_lexicon['payment_operation_success_text']
        self.cancel_button = {'backward:make_payment': class_lexicon['payment_operation_cancel_button']}
        self.width_parameter = {'width': 1}


LexiconSellerRequests = LexiconSellerRequests()
LexiconTariffSelection = LexiconTariffSelection()
LexiconSelectedTariffPreview = LexiconSelectedTariffPreview()
LexiconChoicePaymentSystem = LexiconChoicePaymentSystem()
LexiconCreateInvoice = LexiconCreateInvoice()
LexiconPaymentOperation = LexiconPaymentOperation()
LexiconSellerProfile = LexiconSellerProfile()
LastButtonsInCarpooling = LastButtonsInCarpooling()
ChooseEngineType = ChooseEngineType()
ChooseBrand = ChooseBrand()
ChooseModel = ChooseModel()
ChooseComplectation = ChooseComplectation()
ChooseYearOfRelease = ChooseYearOfRelease()
ChooseMileage = ChooseMileage()
ChooseColor = ChooseColor()
BaseOptionalField = BaseOptionalField()