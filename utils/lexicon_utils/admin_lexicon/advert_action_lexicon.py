from utils.lexicon_utils.admin_lexicon.admin_lexicon import return_main_menu, captions

__ADVERT_LEXICON = {
    'edit_mailing_data_alert': 'Вы можете изменить введённые данные по нажатию кнопку соответствующего пункта.',
    'choose_advert_action': {'message_text': 'Выберите действие: ', 'buttons': {'mailing_action': 'Рассылка', **return_main_menu, 'width': 1}},
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

    'enter_mailing_media': {'message_text': 'Пришлите медиа (в одном сообщении) для рассылки:',
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
    'review_inputted_data': {'message_text': 'Рассылка для {mailing_recipients}:\n{mailing_text}\nВремя отправки: {mailing_date} в {mailing_time}',
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
    }}
}
