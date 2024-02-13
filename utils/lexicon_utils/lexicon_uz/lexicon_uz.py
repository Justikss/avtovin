import importlib



max_phone_number_len = 25

captions_uz = {'backward': '◂ Orqaga ▸', 'was_selected': 'Siz tanladingiz', 'cancel': 'Bekor qilish', 'confirm': 'Tasdiqlash',
            'sales': 'sotishlar', 'purchases': 'xaridlar', 'any': 'har doim', 'day': 'kun', 'week': 'hafta',
            'month': 'oy', 'year': 'yil', 'days': 'kunlar', 'feedbacks': 'javoblar',
            'dont_write_html_tags': '"&lt; &gt;" belgilarini kiriting taqiqlanadi.',
            'all_users': 'barcha', 'buyers': 'xaridorlar', 'sellers': 'sotuvchilar', 'delete': 'O‘chirish',
            'by_dealership': 'avtosalon', 'by_seller': 'shaxsiy shaxs', 'close': 'Yashirish', 'surname_name_patronymic': 'F.I.Sh.: ', 'add': 'Qo‘shish',
            'successfully': 'Muvaffaqiyatli', 'tech_support_entity': '👨🏻‍💻Yordamchi xodim: {SUPPORT_NUMBER}\n',
           'supports_pattern': f'''{' ' * 25 + '───────────────'}\n<blockquote>{'{0}'}</blockquote>\n{' ' * 25 + '───────────────'}''',
               'send_phone_number': 'Raqam yuboring'
               }
''''''


faq = '''
<b>Texnik yordam:</b>
Kontaktlar asosiy menyu orqali [Yordam] tugmasi yordamida mavjud
'''
money_valute = '$'


max_price_len = 20
max_contact_info_len = 100
block_user_reason_text_len = {'max': 256, 'min': 3}

LEXICON_UZ = {
    'buyer_unban': {
        'message_text': 'Xaridor hisobingiz muvaffaqiyatli qulfdan chiqarildi. Biz bilan xarid qilishda davom eting!',
        'buttons': {'close_unblock_notification:buyer': 'Bildirishnomani yashirish', 'width': 1}},

    'seller_unban': {
        'message_text': 'Sotuvchi hisobingiz muvaffaqiyatli blokdan chiqarildi. Biz bilan savdo qilishda davom eting!',
        'buttons': {'close_unblock_notification:seller': 'Bildirishnomani yashirish', 'width': 1}},

            'callback_spam_detected': 'Tugmani bosishning zararli intensivligi aniqlandi.\n{time} soniyadan keyin bot bilan ishlashni davom ettirishingiz mumkin.',
            'spam_detected': 'Sizdan xabar jo‘natishning zararli intensivligi aniqlandi.\nSiz {time} soniyadan so‘ng chatga qayta yozishingiz mumkin bo‘ladi.',
            'spam_passed': 'Chat bloklandi.\nSiz bot bilan muloqotni davom ettirishingiz mumkin.',
            'address_was_not_found': 'Manzil topilmadi',
            'cant_buy_yourself': "Siz mahsulotni o'zingizdan sotib olmaysiz",
            'simultaneous_announcements_was_over': 'Siz bir vaqtning oʻzida chop etilgan reklamalar chegarasidan oshib ketishga harakat qildingiz Sizda allaqachon {advert_count} ta {advert_count} ta reklama bor',
            'you_are_blocked_alert': 'Siz bu faoliyatda bloklanibsiz',
            'sepp': '—',
            'tariff_non_actuallity': 'Tarif sotib olishingiz kerak!',
            'awaiting_process': 'Kuting',
            'new_recommended_offer_startswith': 'Yangi taklif kelib tushdi:',
            'make_choose_brand': 'Markani tanlang:',
            'buyer_havent_recommendated_offers': "Tavsiya etilgan e'lonlar ro'yxati bo'sh!",
            'active_offers_non_exists': 'Faol takliflar ro‘yxati bo‘sh.',
            "buyer_haven't_cached_requests": 'So‘nggi ko‘rilganlar tarixi bo‘sh.',
            'incoming_address_caption': "Ko'rsatilgan manzil:\n",
            'address': 'Manzil',
            'waiting_request_process': "So'rovingiz qayta ishlanmoqda. Taxminiy kutish vaqti: {time} {seconds}",
            'cached_requests_for_buyer_message_text': {
                'message_text': "Siz tasdiqlamagan takliflarni ko'rish\n"},
            'active_offers_for_buyer_message_text': {
                'message_text': 'Faol takliflarni ko‘rish\n'},
            'recommended_offers_for_buyer_message_text' : {
                'message_text': "Tavsiya etilgan takliflarni ko'rish\n"},
            'backward_from_buyer_offers': {'buyer_requests': '◂ Orqaga ▸'},
            'output_inline_brands_pagination': {'inline_buttons_pagination:-': '←', 'page_count': '[C/M]', 'inline_buttons_pagination:+': '→'},
            'confirm_from_buyer': {'separator': '=' * 40, 'non_data_more': "Ko'rsatish uchun ma'lumot yo'q"},
            'start_registration': 'Ro‘yxatdan o‘ting!',
            'unexpected_behavior': 'Kutilmagan xatti-harakat',
            'car_was_withdrawn_from_sale': 'Avtomobil sotuvdan olingan',
            'car_search_parameters_incactive': "Qidiruv parametrlari endi faol emas. Iltimos, yangilang.",
            'seller_dont_exists': 'Sotuvchi endi faol emas',
            'search_parameter_invalid': 'Bu parametr dolzarb emas',
            'order_was_created': "Siz javob berdingiz! Endi e'londa sotuvchining aloqa ma'lumotlari ko'rsatilgan,\nShuningdek, sizning takliflaringiz ro'yxati to'ldirildi!",
            'too_late': 'Siz kech qoldingiz',
            'success_notification': 'Qabul qilindi',
            'seller_lose_self_tariff_notification': {'message_text': "Siz o'z tarifingizni uzaytira olmadingiz!\nSizning savdo faoliyatingiz tarixi o'chirildi.\nBizda sotishni davom ettirish uchun yangi tarifni rasmiylashtiring!",
'buttons': {'tariff_extension': 'Tariflar katalogi ✅', 'close_seller_notification_by_redis:delete_tariff': 'Bildirishnomani yashirish.', 'width': 1}},
'seller_without_tariff_notification': {'message_text': "Sizning tarifingiz sarflandi,\n24 soat o'tgach sizning tovarlar katalogingiz va javoblar tarixingiz tozalanadi, buni oldini olish uchun\nsiz yana bir tarif sotib olishingiz kerak!",
'buttons': {'tariff_extension': 'Tarifni uzaytirish ✅', 'close_seller_notification_by_redis:lose_tariff': 'Bildirishnomani yashirish.', 'width': 1}},
'user_in_system': {'message_text': 'Siz tizimdasiz'},
'choose_language': {'message_text': 'Tilingizni tanlang\nВыберите ваш язык', 'language_uz': '🇺🇿 Uzb',
'language_ru': "🇷🇺 Rus", 'width': 2},
'hello_text': {'message_text': "<b>Salom <i>{user_name}</i></b>!\nBizning ilovamizda siz o'z avtomobilingizni sotishingiz yoki xarid qilishingiz mumkin.\nQuyidagilardan birini tanlang 👇🏼", 'start_sell': 'Sotish 👨🏻‍💼',
'start_buy': '👨🏻‍💻 Xarid qilish', 'width': 2},
'write_full_name': {'message_text': 'FIOingizni kiriting', 'backward:user_registration': '◂ Orqaga ▸', 'width': 1},
'write_full_name(exists)': 'Bu ism allaqachon ro‘yxatdan o‘tgan\nboshqa kutilmoqda',
'write_full_name(novalid)': f'Noto‘g‘ri kirish, 2-3 harfli so‘zlar, probel bilan ajratilgan\nUzunligi {max_contact_info_len} belgilargacha bo‘lishi kerak.',
'write_phone_number': {'message_text': 'Telefon raqamingizni kiriting:',
'backward:user_registration_number': '◂ Orqaga ▸', 'width': 1},
'write_phone_number(novalid)': f"<b>Telefon raqami noto‘g‘ri kiritilgan</b>\nRaqamingizni to‘g‘riligini tekshiring\nFaqat raqamlar, bo‘sh joylar va + belgisini qabul qiladi.\nBelgilarning maksimal soni bilan: {max_phone_number_len}.\nRaqamning mumkin bo'lgan hududlari: O'zbekiston yoki Rossiya.",
'write_phone_number(exists)': '<b>Telefon raqami noto‘g‘ri kiritilgan!</b>\nU allaqachon ro‘yxatdan o‘tgan\nboshqa kutilmoqda',
    'write_phone_number(banned)': 'Ushbu telefon raqami xaridorlar maydonchasida bloklangan\nIltimos, yangi raqam kiriting:',
    # 'most_answers': {'message_text': 'Tez-tez so‘raladigan savollarga javoblar', 'in_main': 'Menyuda', 'width': 1},
    'main_menu': {'message_text': '<b>Xaridor menyusi</b> 👨🏻‍💻\nSizning harakatingizni tanlang:',
                  'buyer_requests': 'Takliflar 📋', 'car_search': '🚘 Avto izlash',
                  'faq': 'Ko‘rsatmalar 💬', 'support': '🌐 Yordam', 'backward:set_language': '◂ Orqaga ▸ ', 'width': 2},
    'buyer_requests': {'message_text': '<b>Takliflar ro‘yxati:</b>',
                       'buttons': {'buyer_cached_offers': '🚫 Tasdiqlanmagan ({non_confirmed})',
                                   'buyer_active_offers': '✅ Tasdiqlangan ({confirmed})',
                                   'buyers_recommended_offers': '🔥 Yangi ({new})', 'return_main_menu': 'Menyuga',
                                   'width': 1}},
    'f_a_q': {
        'message_text': f'Tez-tez so‘raladigan savollarga javoblar: \n\nBotda sotib olish-sotish tizimi bilan tanishish uchun quyidagi tugmalarni tanlang.\n{faq}',
        'seller_faq': 'Sotish 👨🏻‍💼', 'buyer_faq': '👨🏻‍💻 Xarid qilish',
        'return_main_menu': '◂ Orqaga ▸', 'width': 2},
    'tech_support': {'message_text': 'Harakatingizni tanlang:', 'write_to_support': 'Yozing 💬',
                     'call_to_support': 'Qo‘ng‘iroq qiling 📱', 'width': 2, 'return_main_menu': '◂ Orqaga ▸'},
    'write_to_support': {'message_text': "Biz bilan telegram orqali bog'lanishingiz mumkin:", 'backward:support': '◂ Orqaga ▸', 'width': 1},
    'call_to_support': {
        'message_text': 'Bizga quyidagi raqamlarga qo‘ng‘iroq qilib murojaat qilishingiz mumkin:\n',
        'backward:support': '◂ Orqaga ▸', 'width': 1},

    'search_car': {'message_text': 'Avtomobil turlarini tanlang:', 'choose_state_1': 'Yangi',
                   'choose_state_2': 'Ishlatilgan',
                   'return_main_menu': '◂ Orqaga ▸', 'width': 2},
    'cars_not_found': {'message_text': 'Afsuski, ushbu turdagi avtomobillar vitrinada yo‘q.',
                       'backward:choose_car_category': '◂ Orqaga ▸', 'return_main_menu': '🏡 Menyuga 🏡', 'width': 1},

    'search_configuration': {'message_text': 'Qidiruvingizni sozlang', 'start_configuration_search': 'Boshlash',
                             'backward': '◂ Orqaga ▸', 'width': 1},
    'footer_for_output_active_offers': {'viewed_status': 'Sotuvchi tomonidan ko‘rilgan holati: ',
                                        'status_true': 'Ko‘rildi ✅', 'status_false': 'Ko‘rilmagan ❌'},
    'active_offer_caption': '<b>Faol taklif:</b>',
    'chosen_configuration': {
        'message_text': {'phone_number': '\nMobil telefon: ',
                         'your_configs': '<b>Sizning so‘rovingiz bo‘yicha takliflar:</b>',
                         'from_seller': '<b>Sotuvchidan: </b>\n<i>{seller_name}</i>',
                         'from_dealership': '<b>Avtosalondan: </b>\n<i>{dealership_name}</i>\nManzili: <i>{dealership_address}</i>',
                         'car_state': 'Holati: <i>X</i>',
                         'engine_type': 'Dvigatel turi: <i>X</i>',
                         'model': 'Model: <i>X</i>',
                         'brand': 'Marka: <i>X</i>', 'complectation': 'To‘plam: <i>X</i>',
                         'cost': f'<blockquote><b>Narxi: <i>X {money_valute}</i></b></blockquote>',
                         'mileage': 'Yurgan masofasi: <i>X</i>', 'year': 'Yili: <i>X</i>',
                         'color': 'Rangi: <i>X</i>'}, 'buyer_car_pagination:-': '←', 'buyer_car_pagination:+': '→',
        'confirm_buy_settings:': '✓ Tasdiqlash ✓', 'buy_search_price_filter': "♻️ Narx bo'yicha filtrlash ♻",
        'backward_in_carpooling': '⚙️ O‘zgartirish ⚙️', 'return_main_menu': '🏡 Menyuga 🏡', 'width': (2, 1, 1, 1)},

    'confirm_buy_configuration': {
        'message_text': 'Siz muvaffaqiyatli so‘rov qoldirdingiz!\nTasdiqlash haqida xabar olasiz.',
        'return_main_menu': '🏡 Menyuga 🏡', 'width': 1},
    'buy_configuration_error': {'message_text': 'Siz allaqachon bunday so‘rov qoldirgansiz.',
                                'return_main_menu': '🏡 Menyuga 🏡', 'width': 1},
    'user_non_registration': {'message_text': 'Xato. Sizning hisobingiz ro‘yxatdan o‘tmagan\n/start tugmasini bosing'},

    'notification_from_seller_by_buyer_buttons': {'my_sell_feedbacks:': 'Mening sotish bo‘yicha fikrlarimni ko‘rish',
                                                  'close_seller_notification:': 'Xabarni yashirish', 'width': 1},
'confirm_from_seller': {'message_text': {'feedback_header': '<b>Fikr №{feedback_number}</b>', 'from_user': 'Foydalanuvchi <i>{from_user}</i>', 'tendered': '<i>№{advert_number}</i> raqamli so‘rovga javob yozdi:',
'contacts': '<b>Kontaktlar:</b>\n<i>{name}</i>\n{phone}', 'separator': ' ' *10 + '—' * 5}, 'confirm_button': 'Tasdiqlash ✅'},
'backward_name': '◂ Orqaga ▸',
"seller_haven't_this_car": 'Sizda bunday avtomobil sotilmaydi',
'separator': '='*40,

'who_is_seller': {'message_text': 'Quyidagi punktlarni tanlang:', 'i_am_private_person': 'Shaxsiy shaxs 👨🏻', 'i_am_car_dealership': 'Avtosalon 🚘', 'backward:set_language': '◂ Orqaga ▸', 'width': 2},
'write_full_seller_name': {'message_text': 'F.I.O. ni yozing', 'backward:seller_registration_seller_person_name': '◂ Orqaga ▸', 'width': 1},
'write_full_seller_name(novalid)': {
    'message_text': f'Noto‘g‘ri kiritish, qabul qilinadi 2-3 harfli so‘zlar, bo‘sh joy bilan ajratilgan\nUzunligi {max_contact_info_len} belgigacha.',
    'backward:seller_registration_seller_person_name': '◂ Orqaga ▸', 'width': 2},
'write_full_seller_name(exists)': {'message_text': 'Bu ism allaqachon ro‘yxatdan o‘tgan\nBoshqa ism kutmoqda', 'backward:seller_registration_seller_person_name': '◂ Orqaga ▸', 'width': 1},

'write_dealership_name': {'message_text': 'Avtosalon nomini kiriting:', 'backward:seller_registration_dealership_name': '◂ Orqaga ▸', 'width': 1},
'write_dealership_name(novalid)': f'Avtosalon nomi {max_contact_info_len} belgidan kam bo‘lishi kerak\nva faqat harflar va raqamlardan iborat bo‘lishi kerak:',
'write_dealership_name(exists)': 'Bu nom allaqachon ro‘yxatdan o‘tgan\nboshqa nom kutilmoqda',

'write_seller_phone_number': {'message_text': 'Telefon raqamingizni kiriting:',
                       'backward:seller_registration_number': '◂ Orqaga ▸', 'width': 1},
'write_seller_phone_number(novalid)': f"<b>Telefon raqami noto‘g‘ri kiritilgan.</b>Iltimos, raqamingiz toʻgʻriligini tekshiring\nFaqat raqamlar, boʻshliqlar va '+' belgisi qabul qilinadi.\nMaksimal belgilar soni: {max_phone_number_len}.\nRaqamning mumkin bo'lgan hududlari: O'zbekiston yoki Rossiya.",
'write_seller_phone_number(exists)': '<b>Telefon raqami noto‘g‘ri kiritilgan!</b>\nU allaqachon ro‘yxatdan o‘tgan\nboshqa raqam kutilmoqda',
'write_seller_phone_number(banned)': '<b>Ushbu telefon raqami sotuvchilar platformasida bloklangan</b>\nIltimos, yangi raqam kiriting:',

'write_dealership_address': {'message_text': 'Avtosalon manzilini kiriting\nYoki geolokatsiyangizni yuboring\n(chatning chap tomonidagi skrepka belgisini bosing)', 'backward:seller_registration_dealership_address': '◂ Orqaga ▸', 'width': 1},
'write_dealership_address(novalid)': {'message_text': f'Xato\nAvtosalon manzili harflarni o‘z ichiga olishi kerak\nva {max_contact_info_len} belgidan kam bo‘lishi kerak', 'backward:seller_registration_dealership_address': '◂ Orqaga ▸', 'width': 1},

'checking_seller_entered_data': {'message_text': '<b>Kiritilgan ma’lumotlar to‘g‘rimi?</b>\n(ma’lumotni qayta yozish uchun maydonni bosing)', 'rewrite_seller_name': '', 'rewrite_seller_number': '', 'rewrite_dealership_address': '', 'confirm_registration_from_seller': 'Tasdiqlash ✅', 'width': 1},
'confirm_registration_from_seller': {'message_text': 'Ro‘yxatdan o‘tish tugallandi\nMa’muriyat tomonidan tasdiqlash xabari kutib turing.', 'start_sell': 'Sotuvchi menyusi 👨🏻‍💼', 'width': 1},
'try_again_seller_registration': {'message_text': 'Xato.\nBatafsil ma’lumot olish uchun ro‘yxatdan o‘tish jarayonini qayta o‘tib chiqing.', 'return_to_start_seller_registration': 'Ro‘yxatdan qayta o‘tish', 'width': 1},

'confirm_seller_profile_notification': {'message_text': '✅ Muaffaqiyatli, sotuvchi profilini tasdiqlandi!',
'buttons': {'seller_main_menu': '<b>Sotuvchi menyusiga</b> 👨🏻‍💼', 'close_seller_notification_by_redis:seller': captions_uz['close'], 'width': 1}},

'seller_main_menu': {'message_text': 'Sotuvchi menyusi 👨🏻‍💼\nHarakatingizni tanlang:', 'seller_pofile': 'Profil 📱', 'seller_requests': '📋 Arizalar', 'support': 'Yordam 🌐', 'faq': '💬 Ko‘rsatmalar', 'backward:set_language': '◂ Orqaga ▸', 'width': 2},

'confirm_new_seller_registration_from_admin_button': {'confirm_from_admin': 'Tasdiqlash ✅', 'callback_startswith': 'confirm_new_seller_registration_from:'},

'seller_waiting_registration_confirm': {'start_text_legal': '<b>Avtosalon ro‘yxatdan o‘tish so‘rovi:</b>\n{username}\nManzili:\n{address}\n', 'start_text_natural': '<b>Xususiy sotuvchi ro‘yxatdan o‘tish so‘rovi:</b>\n{username}\n',
'legal_body_header': '─' * 8 + '\n<blockquote>Avtosalon nomi: <i>{dealership_name}</i>\n',
'natural_body_header': '─' * 8 + '\n<blockquote>Ism: <i>{name}</i>\nFamiliya: <i>{surname}</i>\nOtasining ismi: <i>{patronymic}</i>\n',
'body': 'Telefon raqami: {phone_number}</blockquote>\n' + '─' * 8},

'success_seller_registration_notice': {'message_text': 'Siz tizimda ro‘yxatdan o‘tdingiz', 'return_main_menu': 'Sotuvchi menyusiga 👨🏻‍💼', 'width': 1},

'seller_faq': {'message_text': '''
\n<b>Sotuv:</b>\n
<b>Ro'yxatdan o'tgandan so'ng siz:
Tarifni rasmiylashtirishingiz mumkin javoblarni olish uchun:</b>
<blockquote><i>[Sotuvchi menyusi] - [Profil] - [Tarifni rasmiylashtirish]</i></blockquote>

<b>Avto e'lonini yaratish:</b>
<blockquote><i>[Sotuvchi menyusi] - [Arizalar] - [E'lon yaratish]</i></blockquote>

<b>Yaratilgan arizalar ko'rsatiladi:</b><blockquote><i>[Sotuvchi menyusi] - [Arizalar] - [Mening e'lonlarim]</i></blockquote>

<b>Mijoz sizning avtongizga javob berganda</b>
<i>Sizga bot bilan chatda xabar keladi, shuningdek, xaridorning kontaktlari bilan javob bo'limida:</i><blockquote><i>[Sotuvchi menyusi] - [Arizalar] - [Javoblar]</i></blockquote>

<b>Arizalar bilan ishlash.</b>
<b>Amalga oshmagan bitimni o'chirish:</b>
<blockquote><i>[Ko'rilgan javoblar] - [Bitim amalga oshmadi]</i></blockquote>

<b>Tovarni o'chirish:</b><i>Javoblar bo'limida:</i>
<blockquote><i>[Javoblar] - [Sotuvdan olib tashlash]</i></blockquote>
<i>E'lonlar bo'limida</i>:
<blockquote><i>[Arizalar] - [Mening e'lonlarim] - [Sotuvdan olib tashlash]</i></blockquote>
'''
, 'faq': '◂ Orqaga ▸', 'return_main_menu': '🏡 Menyuga 🏡', 'width': 1},
'buyer_faq': {'message_text': '''
<b>Xarid:</b>

<b>Siz bizning telegram botimizda xohlagan avtomobilingizni sotib olishingiz mumkin</b>

<b>Sizga mos keladigan avtomobillarga javob bering.</b>
<i>Avtomashinalarni qidirish bot bilan amalga oshiriladigan harakatlar zanjiri orqali sodir bo'ladi:</i>
<blockquote><i>[Xaridor menyusi] - [Avtomobil qidirish]</i></blockquote>
<i>Avtomobillarni qidirishda siz so'rov bo'yicha ro'yxat olish uchun avtomobilning xohlagan parametrlarini ko'rsatishingiz mumkin</i>

<b>Avtomobil tavsiyalari paydo bo'ladi:</b>
<i>Sotuvchi siz tanlagan avtomobil parametrlarini yuklaganidan so'ng</i>
<blockquote><i>[Xaridor menyusi] - [Takliflar] - [Tavsiyalar]</i></blockquote>
<i>Shuningdek, avval ko'rilgan avtomobil tarixiga asoslanib.</i>

<b>Tasdiqlanmagan e'lonlar:
Bo'lim o'tadi:</b>
<blockquote><i>[Xaridor menyusi] - [Takliflar] - [Tasdiqlanmagan]</i></blockquote>
<i>E'lonlar u yerda qoladi:
• Sizning tomoningizdan javob berilgunga qadar
• Birinchi ko'rishdan 7 kun o'tgach.</i>

<b>Sizning javoblaringiz ko'rsatiladi:
Sotuvchidan javob ko'rish holati va kontaktlar bilan:</b>
<blockquote><i>[Xaridor menyusi] - [Takliflar] - [Tasdiqlangan]</i></blockquote>

''', 'faq': '◂ Orqaga ▸', 'return_main_menu': '🏡 Menyuga 🏡', 'width': 1},

'seller_requests': {'message_text': '<b>Arizalar bilan ishlash bo‘limi</b>\nHarakatingizni tanlang:', 'create_new_seller_request': '📨 E’lon yaratish', 'my_sell_requests': '💰 Mening e’lonlarim', 'my_sell_feedbacks': '🔸 Javoblar', 'return_main_menu': 'Menyuga', 'width': 1},

'confirm_load_config_from_seller_button': {'confirm_load_config_from_seller': '✓ Tasdiqlash ✓', 'edit_boot_car_data': '⚙️ O‘zgartirish ⚙️', 'return_main_menu': '🏡 Menyuga 🏡',
                                           'width': 1},
'seller_load_notification_button': {'return_main_menu': '🏡 Menyuga 🏡'},

'message_not_digit': f'<b>Miqdor faqat bitta raqamdan iborat boʻlishi kerak, uzunligi {max_price_len} tagacha</b>',
'message_not_photo': 'Fotografiyani biriktiring\n(chatning chap tomonidagi skrepka belgisini bosing)\nTelegramda yuborishda siqilishni bekor qilmang',

'seller_start_delete_request': {'message_text': 'O‘chiriladigan arizaning raqamini kiriting', 'buttons': {'backward:seller_start_delete_request': '◂ Orqaga ▸', 'width': 1}},

'incorrect_input_removed_car_id': 'Ariza raqamini noto‘g‘ri kiritdingiz.\nRaqamni "◂ Orqaga ▸" tugmasi orqali tekshiring va qayta kiriting.',
'confirm_delete_request': {'message_text': 'Ushbu avtomobilni o‘chirishni xohlaysizmi?', 'confirm_delete': 'Tasdiqlash ✅', 'backward:seller_delete_request': '◂ Orqaga ▸', 'width': 1},

'seller___my_feedbacks': {'message_text': 'Mening javoblarim', 'buttons': {'new_feedbacks': '✓ Yangi ✓', 'viewed_feedbacks': '👁 Ko‘rib chiqilgan 👁', 'backward:seller__my_feedbacks': '◂ Orqaga ▸', 'width': 2}},
'return_main_menu_button': {'return_main_menu': '🏡 Menyuga 🏡'},
  "buyer_price_filter_review": {
    "message_text": {
      "default": "<b>Narxni saralash:</b>\n",
      "selected_caption": "Tanlangan:\n",
      "min_caption": "{price} dan\n",
      "max_caption": "{price} gacha\n"
    },
    "buttons": {
      "buyer_cost_filter:from": "Dan",
      "buyer_cost_filter:before": "Gacha",
      "set_buyer_cost_filter": "Filtrlarni qo'llash",
      "remove_buyer_cost_filter": "Filtrlarni bekor qilish",
      "width": 2
    }
  },
  "buyer_price_filter_start_input": {
    "message_text": "<b>Narx filtri mumkin bo'lgan diapazoni:</b>\n<blockquote>Dan <i>{min_cost}</i>\nGacha <i>{max_cost}</i></blockquote>\n<b>E'lonlarni filtrlash uchun {default_side_name} summani kiriting:</b>",
    "buttons": {
      "backward:input_request_b_cost_filter": "Orqaga",
      "width": 1
    }
  },
  "buyer_price_filter_input_confirmation": {
    "message_text": "<b>E'lonlarni filtrlashda narx diapazonini qo'shish\n{from_or_before}: {cost}</b>",
    "buttons": {
      "confirm_add_buyer_price_filter_part": "Tasdiqlash",
      "rewrite_buyer_price_filter": "Qayta kiriting",
      "cancel_buyer_price_filter": "Bekor qilish",
      "width": 1
    }
  },
  "reset_current_range_side_buttons": {
    "reset_current_range_side": "Tozalash"
  },
  'cost_filter_non_actiallity': 'Joriy reklamalar bitta narxga ega.\nBunday holatda filtrlash foydasiz.',
  "price_incorrect": f"<b>Narx faqat bitta sonni o'z ichiga olishi kerak (to {max_price_len} raqamgacha)</b>\n' $ ' belgisi bilan kiritish mumkin",
  "price_not_in_range": "<b>Kiritilgan narx joriy tanlov doirasidan tashqarida.</b>",
  "nominative_case_cost_side_from": "Minimal",
  "nominative_case_cost_side_before": "Maksimal",
  "accusative_case_lower_caption_side_before": "maksimal",
  "accusative_case_lower_caption_side_from": "minimal",
  "from_caption": "Dan",
  "before_caption": "Gacha",
  "incorrect_nearest_price": "<b>Sizning filtringiz bironta ham e'lonni tanlamadi.\nSizning diapazoningizga eng yaqin narx:\n{nearest_price}</b>",
  "filter_made_null_list": ""
    ,
    'retry_now_allert': 'Yana urinib ko‘ring',
    'user_havent_permision': 'Sizda huquq yo‘q',
    'seller_without_tariff': 'Sizda hisobda javoblar yo‘q',
    'seller_tarriff_expired': 'Sizning tarifingiz eskirgan',
    'non_actiallity': 'Dolzarb emas',
    'successfully': 'Muvaffaqiyatli',
    'seller_does_have_this_car': 'Sizda bunday mashina sotilmaydi',
    'convertation_sub_string': '~',
    'uzbekistan_valute': 'X sum',
    'other_caption': 'Boshqa',
    'color_caption': 'Rang'

}


lexicon_uz = {
    'make_empty_field': 'Oʻtkazib yuborish',
    'free_cost': 'bepul',
    'residual_simultaneous_announcements': "\n📗 Mavjud faol reklama joylari: <i>{}</i>",
    'simultaneous_announcements': '\n📗 Faol reklamalar chegarasi: <i>{}</i>',
    'incorrect_price_$': '<b>Narxda bittadan ortiq “$” belgisi bo‘lmasligi kerak</b>',
    'infinity_feedbacks_caption': 'cheksiz',
    'offer': '<b>Ilova <i>№{offer_number}</i></b>',
    'backward_in_carpooling': '◂ Orqaga ▸',
    'choose_engine_type_text': 'Dvigatel turini tanlang',
    'choose_brand_text': 'Avtomobil markasini tanlang',
    'choose_model_text': 'Avtomobil modelini tanlang',
    'choose_complectation_text': 'Komplektatsiyani tanlang',
    'choose_year_text': 'Ishlab chiqarilgan yilni tanlang',
    'choose_mileage_text': 'Yurgan masofani tanlang',
    'choose_color_text': 'Rangni tanlang',
    'seller_sure_delete_car_ask_text': 'Vitrinadan mashinani olib tashlashni istaysizmi №{number} ?',
    'seller_does_have_active_requests_alert': 'Sizda faol so‘rovlaringiz yo‘q',
    'seller_does_have_active_car_by_brand': 'Bu marka dolzarb emas.',
    'matched_advert': 'Sizning katalogingizda allaqachon shu kabi e‘lon mavjud, qayta joylashtira olmaysiz!',
    'select_brand_message_text': '<b>Avtomobil markasini tanlang</b>',
    'input_new_price': 'Yangi narxni kiriting.\nHozirgi narx: {current_price}',
    'input_new_price_incorrect_message_text': f'<b>Iltimos, bitta raqamni kiriting, uzunligi {max_price_len} tagacha.</b>',
    'input_new_price_car_dont_exists': 'Afsuski, avtomobil savdodan olingan.',
    'succes_rewrite_price': 'Narx muvaffaqiyatli o‘zgartirildi',
    'commodity_output_block': '''───────────────
<blockquote>Holati: <i>{state}</i>
Dvigatel turi: <i>{engine_type}</i>
Marka: <i>{brand_name}</i>
Model: <i>{model_name}</i>
Komplektatsiya: <i>{complectation}</i>
Ishlab chiqarilgan yili: <i>{year_of_release}</i>
Yurgan masofa: <i>{mileage}</i>
Rang: <i>{color}</i></blockquote>
───────────────''',
    'output_car_request_header': 'Ariza <i>№{request_number}</i>',
    'commodity_state': 'Holati: <i>{state}</i>',
    'commodity_brand': 'Marka: <i>{brand}</i>',
    'commodity_model': 'Model: <i>{model}</i>',
    'commodity_complectation': 'Komplektatsiya: <i>{complectation}</i>',
    'commodity_year_of_realise': 'Ishlab chiqarilgan yili: <i>{year_of_release}</i>',
    'commodity_mileage': 'Yurgan masofa: <i>{mileage}</i>',
    'commodity_color': 'Rang: <i>{color}</i>',
    'commodity_price': '<b>Narxi: <i>{price}</i></b>',
    'pages_were_end': 'Sahifalar tugadi',
    'new_feedbacks_not_found': 'Sizda yangi murojaatlar paydo bo‘lmagan',
    'viewed_feedbacks_not_found': 'Sizda ko‘rilgan murojaatlar yo‘q',
    'did_you_sure_to_delete_feedback_ask': 'Murojaatni o‘chirishga ishonchingiz komilmi №{feedback_number} ?',
    'success_delete': 'O‘chirildi',
    'profile_header': '<b>Sotuvchi profili</b>\n\n',
    'dealership_prefix': '<b>Yuridik shaxs</b> 🤵🏻‍♂️',
    'seller_prefix': '<b>Jismoniy shaxs</b> 👨🏻‍💼\n',
    'dealership_name_prefix': '<b>Avtosalon nomi:</b> <i>{dealership_name}</i>',
    'dealership_address_prefix': '<b>Avtosalon manzili:</b> <i>{dealership_address}</i>',
    'seller_name_prefix': '<b>Sizning ismingiz:</b> <i>{seller_name}</i>',
    'phonenumber_prefix': '<b>Telefon raqami:</b> {phone_number}',
    'tariff_block': '<blockquote>💰 Tarif: <i>{tariff_name}</i>\n🕰 Obuna tugashiga qadar: <i>{days_remaining} Kun</i>\n🔸 Murojaatlar: <i>{feedbacks_remaining}</i>{simultaneous_announcements_caption}{cost_caption}</blockquote>',
    'tariff_out_date_prefix': '<blockquote>🕰 Obuna tugashiga qadar: <i>{days_remaining} Kun</i></blockquote>',
    'residual_feedback_prefix': '<blockquote>🔸 Qolgan murojaatlar: <i>{feedbacks_remaining}</i></blockquote>',
    'tariff_expired': 'Sizning tarifingiz tugagan',
    'tariff_selection_not_found_message_text': 'Tariflar topilmadi',
    'tariff_selection_message_text': 'Mavjud barcha tariflar',
    'selected_tariff_preview_header': '<b>Tarif haqida ma‘lumot:</b>',
    'tariff_name': '<blockquote>🪪 <b>Nomi: <i>{tariff_name}</i></b></blockquote>',
    'tariff_price': '\n💰 <b>Narxi: <i>{tariff_price}</i></b>',
    'tariff_duration_time': '<blockquote>🕰 Amal qilish muddati: <i>{tariff_duration} kun</i></b></blockquote>',
    'tariff_feedback_amount': '<blockquote>🔸 Murojaatlar limiti: <i>{tariff_feedback_limit}</i></b></blockquote>',
    'choice_payment_system_message_text': 'To‘lov tizimini tanlang',
    'create_invoice_in_progress_notification': 'Ishlanmoqda',
    'create_invoice_title': 'Tarifni rasmiylashtirish',
    'create_invoice_description': 'Xaridorlarning {feedbacks_amount} ta murojaatiga obuna.\nDavomiyligi {subscription_days} kun.',
    'create_invoice_load_price_label': 'Tarif narxi',
    'payment_operation_error_text': 'To‘lovda xatolik, 15 daqiqalik tanaffusga rioya qilgan holda qayta urinib ko‘ring',
    'payment_operation_success_text': 'Muvaffaqiyatli!',
    'payment_operation_cancel_button': '🚫 Bekor qilish 🚫',
    'tariff_extension_button': 'Tarifni uzaytirish ✅',
    'tariff_store_button': 'Tariflar katalogi 🎫',
    'confirm': 'Tasdiqlash ✅',
    'delete': 'O‘chirish',
    'rewrite_price_by_seller': 'Narxni o‘zgartirish',
    'withdrawn': 'Savdodan olib tashlash',
    'deal_fell_through': 'Bitim amalga oshmadi',
    'page_view_separator': 'Sahifa: ',
    'tariff_prefix': '<blockquote>💰 Tarif: <i>X</i></blockquote>',
    'tarif_expired': '<blockquote>Sizning tarifingiz tugagan</blockquote>',
    'start_choose_payment_method': 'To‘lov usulini tanlang',
    'to_offers': 'Ilovalar uchun'
}




