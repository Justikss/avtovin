# from utils.lexicon_utils.admin_lexicon.admin_lexicon import pagination_interface
# from utils.lexicon_utils.lexicon_uz.admin_lexicon_uz.admin_lexicon_uz import captions_uz, return_main_menu_uz
mailing_text_max_len = 270
return_main_menu_uz = {'return_main_menu': 'Menyuga'}
captions_uz = {'backward': '◂ Orqaga ▸', 'was_selected': 'Siz tanladingiz', 'cancel': 'Bekor qilish', 'confirm': 'Tasdiqlash',
            'sales': 'sotishlar', 'purchases': 'xaridlar', 'any': 'har doim', 'day': 'kun', 'week': 'hafta',
            'month': 'oy', 'year': 'yil', 'days': 'kunlar', 'feedbacks': 'javoblar',
            'dont_write_html_tags': '"&lt; &gt;" belgilarini kiriting taqiqlanadi.',
            'all_users': 'barcha', 'buyers': 'xaridorlar', 'sellers': 'sotuvchilar', 'delete': 'O‘chirish',
            'by_dealership': 'avtosalon', 'by_seller': 'shaxsiy shaxs', 'close': 'Yashirish', 'surname_name_patronymic': 'F.I.Sh.: ', 'add': 'Qo‘shish',
            'successfully': 'Muvaffaqiyatli'
            }

pagination_interface = {'admin_pagination:-': '←', 'page_counter': '[{start}/{end}]', 'admin_pagination:+': '→'}

''''''

ADVERT_LEXICON_UZ = {
    'unsuccessfully_delete_mailing': 'Yuborishni o‘chirishda muvaffaqiyatsiz urinish',
    'successfully_delete_mailing': 'Tanlangan yuborish muvaffaqiyatli tozalandi!',
    'this_mailing_type_do_not_exists': 'Tanlangan yuborish turi bo‘sh ekan.',
    'unsuccessfull_boot_mail_message': 'Yuklashda muvaffaqiyatsiz urinish',
    'successfully_boot_mail_message': 'Siz muvaffaqiyatli yuborishni yukladingiz!',
    'edit_mailing_data_alert': 'Kiritilgan ma’lumotlarni mos punkt tugmasini bosish orqali o‘zgartirishingiz mumkin.\n',
    'choose_advert_action': {'message_text': '<b>Harakatni tanlang: </b>',
                             'buttons': {'mailing_action': '📄 Yuborish', **return_main_menu_uz, 'width': 1}},
    'choose_mailing_action': {'message_text': '<b>Siz pochta menyusidasiz</b>\nHarakatni tanlang:',
                              'buttons': {
                                  'mailing_storage': 'Yuklangan yuborishlar',
                                  'create_new_mailing': 'Yangi yuborish',
                                  'admin_backward:choose_mailing_action': captions_uz['backward'],
                              'width': 1
                              }},
    'enter_mailing_text': {
            'message_text': '<b>Yuborish matnini kiriting:</b>',
            'buttons': {
                'empty_mailing_text': 'Matnsiz',
                'admin_backward:input_mailing_data': captions_uz['cancel'],
                'width': 1
            }},
    'enter_mailing_text(incorrect)': f'<b>Matn uzunligi {mailing_text_max_len-20} belgidan oshmasligi kerak</b>\n',
    'request_mailing_date_time': {
        'message_text': '<b>Yuborish sanasini va vaqtini kiriting</b>\nFormat: <b>KK-OY-YIL SS:MM</b>',
        'buttons': {'admin_backward:input_mailing_data': captions_uz['cancel'], 'width': 1}},
    'request_mailing_date_time(incorrect)': 'Noto‘g‘ri format. Iltimos, sanani va vaqtni kiriting\nformatda KK-OY-YIL SS:MM',
    'request_mailing_date_time(time)': 'Kiritilgan vaqt o‘tib ketgan,\nqayta kiriting\nformatda KK-OY-YIL SS:MM',

    'enter_mailing_media': {'message_text': '<b>Yuborish uchun media yuboring:</b>\n<blockquote>Ko‘rsatma:\nBir vaqtda yuklash mumkin:\nVideo + foto (birga);\nAudio va hujjat - alohida;</blockquote>',
                            'buttons': {'mailing_without_media': 'Mediasiz',
                                        'admin_backward:input_mailing_data': captions_uz['cancel'], 'width': 1}},
    'edit_mailing_media_buttons': {'mailing_without_media': 'Mediasiz',
                                   'add_other_media': 'Yangi turdagi media qo‘shish',
                                    'admin_backward:input_mailing_data': captions_uz['cancel'], 'width': 1},

    'enter_mailing_recipients': {'message_text': "<b>Yuborish oluvchilarini tanlang:</b>",
'buttons': {'enter_mailing_recipients:sellers': 'Sotuvchilar',
'enter_mailing_recipients:buyers': 'Xaridorlar',
'enter_mailing_recipients:all_users': 'Barchaga',
'admin_backward:input_mailing_data': captions_uz['cancel'],
'width': 1}},
'review_inputted_data': {'message_text': "────────\n<b>{mailing_recipients} uchun yuborish</b>\nJo‘natish vaqti: <b>{mailing_date} soat {mailing_time}</b>\n────────\n<b>'Media' ni tahrirlashda siz boshqa media fayllarni qo'shishingiz mumkin</b>",
'buttons': {'confirm_mailing_action': captions_uz['confirm'],
'edit_mailing_data': 'O‘zgartirish',
'admin_backward:input_mailing_data': captions_uz['cancel'],
'width': 1}},
'edit_inputted_data': {'buttons': {
'confirm_mailing_action': captions_uz['confirm'],
'edit_mailing_text': 'Matn',
'edit_mailing_media': 'Media',
'edit_mailing_date': 'Sana',
'edit_mailing_recipients': 'Oluvchilar',
'admin_backward:input_mailing_data': captions_uz['cancel'],
'width': 1
}},
'sent_mailing': {'message_text': '—'*5},

'choose_type_of_mailing_storage': {'message_text': 'Mavjud yuborish turlarini tanlang: ',
                                   'buttons': {
                                       'select_mailings_viewed_status:0': 'Kutilayotgan',
                                       'select_mailings_viewed_status:1': 'Ko‘rsatilgan',
                                       'admin_backward:choose_review_mailing_type': captions_uz['backward'],
                                       **return_main_menu_uz,
                                       'width': 2
                                   }},


'send_mailing_review': {'message_text': '{mailing_text}{mailing_recipients} uchun yuborish\nJo‘natish vaqti: {mailing_date} soat {mailing_time}',
                        'buttons': {**pagination_interface,
    'delete_current_mailing': 'O‘chirish', 'admin_backward:review_mailings': captions_uz['backward'], 'width': 3
}}
}
