return_main_menu_uz = {'return_main_menu': 'Menyuga'}
captions_uz = {'backward': '◂ Orqaga ▸', 'was_selected': 'Siz tanladingiz', 'cancel': 'Bekor qilish', 'confirm': 'Tasdiqlash',
            'sales': 'sotishlar', 'purchases': 'xaridlar', 'any': 'har doim', 'day': 'kun', 'week': 'hafta',
            'month': 'oy', 'year': 'yil', 'days': 'kunlar', 'feedbacks': 'javoblar',
            'dont_write_html_tags': '"&lt; &gt;" belgilarini kiriting taqiqlanadi.',
            'all_users': 'barcha', 'buyers': 'xaridorlar', 'sellers': 'sotuvchilar', 'delete': 'O‘chirish',
            'by_dealership': 'avtosalon', 'by_seller': 'shaxsiy shaxs', 'close': 'Yashirish', 'surname_name_patronymic': 'F.I.Sh.: ', 'add': 'Qo‘shish',
            'successfully': 'Muvaffaqiyatli'
            }

catalog_captions_uz = {'catalog_review__make_block': 'bloklash', 'to_block': 'bloklash', 'to_delete': 'o‘chirish',
                    'catalog_review__make_delete': 'e’lonni o‘chirish', 'advert': '<b>E’lon: №{advert_id}\n</b>',
                    'inactive_advert_or_seller': 'E’lon yoki sotuvchi faol emas',
                    'advert_successfully_closed': 'Avtomobil muvaffaqiyatli sotuvdan olib tashlandi!',
                    'empty': 'Bo‘sh'

                    }
pagination_interface = {'admin_pagination:-': '←', 'page_counter': '[{start}/{end}]', 'admin_pagination:+': '→'}

''''''

CATALOG_LEXICON_UZ = {
    'search_advert_by_id_await_input': {'message_text': '<b>Qidirilayotgan e’lonning ID raqamini kiriting: </b>',
                                        'buttons': {
                                            'admin_backward:await_input_id_to_search_advert': captions_uz['backward'],
                                            **return_main_menu_uz,
                                            'width': 1
    }},
    'search_advert_by_id_await_input(digit)': 'E’lonni ID raqami orqali qidirish uchun butun son qiymatini kiritish kutilmoqda:',
    'search_advert_by_id_await_input(not_exists)': 'Kiritilgan ID raqamidagi e’lon mavjud emas.\nBoshqa raqamni kiriting:',
    'start_catalog_menu': {'message_text': '<b>Siz katalogga kirdingiz</b>\nAmalingizni tanlang:', 'buttons': {
        'admin_catalog__advert_parameters': '⚙️ Avtomobil parametrlari',
        'admin_catalog__car_catalog_review': '📋 Avtomobil katalogi',
        **return_main_menu_uz,
        'width': 1
    }},
    'car_catalog_review_choose_category': {'message_text': '<b>Ko‘rib chiqiladigan e’lonlar turini tanlang:</b>', 'buttons': {
        'car_catalog_review__new': 'Yangi',
        'car_catalog_review__viewed': 'Ko‘rilgan',
        'search_by_id': 'ID bo‘yicha qidirish',
        'admin_backward:choose_catalog_review_advert_type': captions_uz['backward'],
        'width': 2
    }},
    'review_specific_advert_catalog': {'message_text': 'E’lon: №{advert_id}\n{seller_entity}:', 'buttons': {
        **pagination_interface,
        'admin_review_catalog_delete_advert': 'Cheklovlar',
        'admin_backward:review_specific_advert_catalog': captions_uz['backward'],
        **return_main_menu_uz,
        'width': 3
    }},
    'catalog__choose_specific_advert_action': {'message_text': "<b>Sizga kerak bo'lgan cheklov turini tanlang:</b>", 'buttons': {
        'catalog_action__delete_advert': 'E’lonni o‘chirish',
        'catalog_action__block_seller': 'Sotuvchini bloklash',
        'admin_backward:catalog__choose_specific_advert_action': captions_uz['backward'],
        'width': 1
    }},
    'catalog_close_advert__input_reason': {'message_text': '{acton_subject} uchun sababni kiriting:', 'buttons': {
        'admin_backward:input_reason_to_close_advert': captions_uz['backward'],
        **return_main_menu_uz,
        'width': 1
    }},
    'catalog_close_advert__confirmation_advert_close_action': { 'message_text': '{action_subject} amalga oshirish\n{seller_entity}\n{advert_caption}Sababi:\n{action_reason}',
    'buttons': {'catalog_review__confirm_close_action': captions_uz['confirm'],
                'admin_backward:to_catalog_review_adverts': 'E’lonlarga qaytish',
                'admin_backward:catalog_review_close_action_confirmation': captions_uz['backward'],
                **return_main_menu_uz,
                'width': 1}},
'close_advert_seller_notification': {'message_text': 'Sizning №{advert_id} raqamli e’loningiz admin tomonidan quyidagi sababga ko‘ra o‘chirildi: {close_reason}',
                                     'close_seller_notification_by_redis:close_advert': captions_uz['close'],
                                     'width': 1}}

catalog_mini_lexicon_uz = {
    'admin_review_catalog_choose_car_brand_message_text': '<b>Ko‘rib chiqish uchun mashina markasini tanlang:</b>'
}
