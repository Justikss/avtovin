from utils.lexicon_utils.admin_lexicon.admin_lexicon import return_main_menu, captions, pagination_interface

__ADVERT_LEXICON = {
    'this_mailing_type_do_not_exists': 'Выбранный тип рассылки оказался пуст.',
    'unsuccessfull_boot_mail_message': 'Неуспешная попытка загрузки',
    'successfully_boot_mail_message': 'Вы успешно загрузили рассылку!',
    'edit_mailing_data_alert': 'Вы можете изменить введённые данные по нажатию кнопку соответствующего пункта.\n',
    'choose_advert_action': {'message_text': 'Выберите действие: ',
                             'buttons': {'mailing_action': 'Рассылка', **return_main_menu, 'width': 1}},
    'choose_mailing_action': {'message_text': 'Рассылка:\nВыберите действие:',
                              'buttons': {
                                  'mailing_storage': 'Загруженные рассылки',
                                  'create_new_mailing': 'Новая рассылка',
                                  'admin_backward:choose_mailing_action': captions['backward'],
                              'width': 1
                              }},
    'enter_mailing_text': {
            'message_text': 'Введите текст рассылки: ',
            'buttons': {
                'empty_mailing_text': 'Без текста',
                'admin_backward:input_mailing_data': captions['cancel'],
                'width': 1
            }},
    'request_mailing_date_time': {
        'message_text': 'Введите дату и время рассылки\nв формате ДД-ММ-ГГГГ ЧЧ:ММ',
        'buttons': {'admin_backward:input_mailing_data': captions['cancel'], 'width': 1}},
    'request_mailing_date_time(incorrect)': 'Неверный формат. Пожалуйста, введите дату и время\nв формате ДД-ММ-ГГГГ ЧЧ:ММ',
    'request_mailing_date_time(time)': 'Введённое время истекло,\nповторите ввод\nв формате ДД-ММ-ГГГГ ЧЧ:ММ',

    'enter_mailing_media': {'message_text': 'Пришлите медиа для рассылки:\n<blockquote>Инструкция:\nЗа один раз можно загрузить только:\nВидео + фото (вместе);\nАудио и документ - отдельно;</blockquote>',
                            'buttons': {'mailing_without_media': 'Без медиа',
                                        'admin_backward:input_mailing_data': captions['cancel'], 'width': 1}},
    'edit_mailing_media_buttons': {'mailing_without_media': 'Без медиа',
                                   'add_other_media': 'Добавить новый тип медиа',
                                    'admin_backward:input_mailing_data': captions['cancel'], 'width': 1},

    'enter_mailing_recipients': {'message_text': "Выберите получателей рассылки: ",
                                  'buttons': {'enter_mailing_recipients:sellers': 'Продавцы',
                                              'enter_mailing_recipients:buyers': 'Покупатели',
                                              'enter_mailing_recipients:all_users': 'Всем',
                                              'admin_backward:input_mailing_data': captions['cancel'],
                                              'width': 1}},
    'review_inputted_data': {'message_text': 'Рассылка для {mailing_recipients}:\n{mailing_text}\nВремя отправки: {mailing_date} в {mailing_time}\n<b>Так же вы можете добавить иные медиа-файлы при соответсвующем редактировании "Медиа"</b>',
                             'buttons': {'confirm_mailing_action': captions['confirm'],
                                         'edit_mailing_data': 'Изменить',
                                         'admin_backward:input_mailing_data': captions['cancel'],
                                         'width': 1}},
    'edit_inputted_data': {'buttons': {
        'confirm_mailing_action': captions['confirm'],
        'edit_mailing_text': 'Текст',
        'edit_mailing_media': 'Медиа',
        'edit_mailing_date': 'Дата',
        'edit_mailing_recipients': 'Получатели',
        'admin_backward:input_mailing_data': captions['cancel'],
        'width': 1
    }},

    'sent_mailing': {'message_text': '—'*5, 'buttons': {'close_mailing_message:': 'Скрыть', 'width': 1}},

    'choose_type_of_mailing_storage': {'message_text': 'Выберите тип имеющихся рассылок: ',
                                       'buttons': {
                                           'select_mailings_viewed_status:0': 'Ожидаемые',
                                           'select_mailings_viewed_status:1': 'Показываемые',
                                           'admin_backward:choose_review_mailing_type': captions['backward'],
                                           **return_main_menu,
                                           'width': 2
                                       }},


    'send_mailing_review': {'message_text': 'Рассылка для {mailing_recipients}:\n{mailing_text}\nВремя отправки: {mailing_date} в {mailing_time}',
                            'buttons': {**pagination_interface,
        'delete_current_mailing': 'Удалить', 'admin_backward:review_mailings': captions['backward'], 'width': 3
    }}

}
