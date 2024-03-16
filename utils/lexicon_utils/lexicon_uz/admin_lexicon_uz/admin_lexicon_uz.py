import importlib


# config_module = importlib.import_module('config_data.config')

block_user_reason_text_len = {'max': 256, 'min': 3}
max_contact_info_len = 100
max_feedbacks_len = 18
max_price_len = 20

return_main_menu_uz = {'return_main_menu': 'Menyuga'}
captions_uz = {'backward': '◂ Orqaga ▸', 'was_selected': 'Siz tanladingiz', 'cancel': 'Bekor qilish', 'confirm': 'Tasdiqlash',
            'sales': 'sotishlar', 'purchases': 'xaridlar', 'any': 'har doim', 'day': 'kun', 'week': 'hafta',
            'month': 'oy', 'year': 'yil', 'days': 'kunlar', 'feedbacks': 'javoblar',
            'dont_write_html_tags': '"&lt; &gt;" belgilarini kiriting taqiqlanadi.',
            'all_users': 'barcha', 'buyers': 'xaridorlar', 'sellers': 'sotuvchilar', 'delete': 'O‘chirish',
            'by_dealership': 'avtosalon', 'by_seller': 'shaxsiy shaxs', 'close': 'Yashirish', 'surname_name_patronymic': 'F.I.Sh.: ', 'add': 'Qo‘shish',
            'successfully': 'Muvaffaqiyatli'
            }
low_sep = '────────'


ADMIN_LEXICON_uz = {
    'branch_is_exists': "Tanlangan xususiyatlar kombinatsiyasi joriy holat uchun allaqachon mavjud.\n'Yangi + ishlatilgan' da mumkin.",
    'choose_user_block_category': {'message_text': '<b>Foydalanuvchi turini tanlang:</b>', 'buttons': {
        'user_block_status:true': 'Bloklashda', 'user_block_status:false': 'Faol',
        **return_main_menu_uz,
        'width': 2
    }},

    'banned_user_endswith': {'message_text': low_sep + '\n<blockquote><b>Zablokirovan</b> <i>{date}</i>\n <b>soat</b> <i>{time}</i> da\n<b>Sabab:</b> <i>{reason}</i></blockquote>',
    'buttons': {'unblock_user': 'Razblokirovat'
    }},
    'unban_confirmation': {'message_text': '<b>Tasdiqlang razblokirovku </b>\n<i>{user_entity}</i>',
    'buttons': {'confirm_unban': captions_uz['confirm'],
    'admin_backward:unban_confirmation': captions_uz['backward'],
    'width': 1}},
    'banned_users_caption_parent_case:true': '<i>Bloklangan</i>',
    'banned_users_caption_parent_case:false': '<i>Faol</i>',
    'banned_users_caption:true': '<i>Bloklangan</i>',
    'banned_users_caption:false': '<i>Faol</i>',
    'inputted_user_not_is_admin': 'Kiritilgan foydalanuvchi administrator emas',
    'user_has_not_been_blocked': 'Foydalanuvchi bloklanmagan',
    'inputted_admin_is_exists': "Belgilangan administrator allaqachon o'z lavozimida",
    'user_id_not_found': "Foydalanuvchi topilmadi. Ehtimol, u hech qachon botda ro'yxatdan o'tmagan.",
    'admin_help': {'message_text': '''<b>Atamalar:</b>
Qizil admin - Eng yuqori darajali administrator.

Qizil adminlarga mavjud buyruqlar:

/add @username - <i>Admin qo'shish.</i>

/radd @username - <i>Qizil admin qo'shish.</i>

/del @username - <i>Adminni olib tashlash (Hatto qizil bo'lsa ham).</i>

/rdel @username - <i>Qizil adminni pasaytirish - oddiyga</i>

Har qanday adminlarga mavjud buyruqlar:

/unban s @username - <i>Sotuvchini blokdan chiqarish</i>
/unban b @username - <i>Xaridorni blokdan chiqarish</i>
/unban @username - <i>Xaridorni ham, sotuvchini ham blokdan chiqaring</i>

/alist - <i>Adminlar ro'yxati</i>''', 'buttons': {'check_banned_persons': "Foydalanuvchilar ro'yxati",
                                                  'return_main_menu': 'Menyuga qaytish', 'width': 1}},
    'close_admin_list': 'Menyuda',
    'admin_list_header': 'Administratorlar:\nFoydalanuvchi nomi   Qizil holat',
    'admin_list_part': '\n{username} | {red_status}',
    'successfully': 'Muvaffaqiyatli',
    'unsuccessfully': 'Muvaffaqiyatsiz',
    'admin_not_is_red': 'Siz qizil administrator emassiz',
    'admin_panel_button_caption': '🔑 Admin Paneli',
    'user_havent_admin_permission': 'Siz administrator emassiz',
    'users_category_non_exists': 'Foydalanuvchilar ushbu kategoriyasi topilmadi.',
    'user_non_active': 'Ushbu foydalanuvchi faol emas',
    'success_set_tariff': 'Tarif muvaffaqiyatli berildi!',
    'failed_set_tariff': 'Tarif berilmadi, foydalanuvchi topilmadi.',
    'tariff_was_reset': 'Tarif muvaffaqiyatli nolga tushirildi!',
    'action_non_actuality': 'Harakat dolzarb emas',
    'user_block_success': 'Foydalanuvchi bloklandi!',
    'information_was_updated': 'Ma’lumot yangilandi!',
    'success_input_tariff_data': 'Muvaffaqiyatli!\nTarif {tariff_name} - muvaffaqiyatli qo‘shildi!',
    'unsuccessfully_add_tariff': 'Tarif qo‘shib bo‘lmadi.',
    'tariff_has_bindings': 'Ushbu tarifni o‘chirib bo‘lmaydi, chunki u foydalanuvchilarda faol',
    'tariff_was_successfully_removed': 'Tarif muvaffaqiyatli o‘chirildi!',
    'tariff_was_inactive': 'Ushbu tarif faol emas edi!',
    'successfully_edit_action': 'Muvaffaqiyatli tahrirlandi!',
'incorrect_input_block_reason': f'''<b>Sizning sababingiz {block_user_reason_text_len['min']} dan {block_user_reason_text_len['max']} gacha belgilarni o‘z ichiga olishi kerak, jumladan!</b>\nHozirgi uzunlik (bo‘sh joylarsiz):\n''',

'start_admin_panel': {'message_text': '<b>Admin paneliga xush kelibsiz.</b>\nHarakatingizni tanlang:',
                      'buttons': {'admin_button_bot_statistics': 'Statistika 📈', 'admin_button_users': '👨🏻‍💻 Foydalanuvchilar',
                                  'admin_button_tariffs': 'Tariflar 💳', 'admin_button_contacts': '📝 Kontaktlar',
                                  'admin_button_catalog': 'Katalog 🗂', 'admin_button_advert': '🗞 Reklama',
                                  'admin_backward:admin_main_menu': 'Chiqish',
                                  'width': 2}},

'select_user_category': {'message_text': '<b>{block_state} foydalanuvchilar toifasini tanlang:</b>',
                         'buttons': {'buyer_category_actions': 'Xaridorlar 👨🏻‍💻',
                                     'seller_category_actions': '👨🏻‍💼 Sotuvchilar',
                                    'admin_backward:choose_user_entity': captions_uz['backward'],
                                     **return_main_menu_uz,
                                     'width': 2}},

'select_seller_category': {'message_text': '<b>{block_state} sotuvchilar toifasini tanlang:</b>',
                           'buttons': {'legal_seller_actions': 'Salonlar 🚘', 'natural_seller_actions': '👨🏻‍💼 Shaxsiy shaxslar',
                                       'admin_backward:choose_seller_category': '◂ Orqaga ▸',
                                       'width': 2}},

'review_seller_card': {'message_header': "<b>Sotuvchi haqida ma'lumot:</b>",
                       'buttons': {'tariff_actions_by_admin': 'Tarif', 'user_block_action_by_admin': 'Bloklov',
                                   'select_seller_statistic_period': 'Statistika',
                                   'admin_backward:user_profile_review': captions_uz['backward'],
                                   **return_main_menu_uz, 'width': 2}},

'review_buyer_card': {'message_text': '<b>Xaridorni ko‘rib chiqish:</b>\n<blockquote>F.I.Sh.: {full_name}\nTelefon raqami: {phone_number}</blockquote>',
                      'buttons': {'user_block_action_by_admin': 'Bloklov',
                                  'admin_backward:user_profile_review': captions_uz['backward'],
                                  **return_main_menu_uz, 'width': 1}},

'reset_tariff_confirm_request': {'message_text': '\nSiz rostdan ham sotuvchi tarifini nolga tushirmoqchimisiz ?',
                                 'buttons': {'confirm_reset_seller_tariff_action': 'Tasdiqlash',
                                             'admin_backward:reset_seller_tariff': captions_uz['cancel'],
                                             'width': 1}},
'final_decision_ban_user': {'message_text': '<b>Bloklovni amalga oshirish:</b>\n{user_entity}\n<b>Sababi:</b>\n{reason}',
                            'confirm_block_user_by_admin': captions_uz['confirm'],
                            'admin_backward:final_confirm_block_user': captions_uz['backward'],
                            'admin_backward:review_result_profile_protocol': captions_uz['cancel'],
                            'width': 1},

'user_ban_notification': {
    'message_text': 'DIQQAT!\nSizning {activity} botimizdagi faoliyatingiz quyidagi sababga ko‘ra abadiy bloklangan: {reason}',
'buttons': {'close_ban_notification': captions_uz['close'], 'width': 1}},
    'input_name_to_search_process':  {'message_text': "<b>{block_state} foydalanuvchining to'liq ismini kiriting:</b>",
                                     'buttons': {'admin_backward:input_name_to_search': captions_uz['backward'],
                                                 'width': 1}},

    'input_name_to_search_process(novalid)': f'''<b>Noto'g'ri kirish FIO!</b>\nIsm {'{block_state}'} foydalanuvchi ikki uch so'z shaklida "FIO" bo'lishi kerak va o'z ichiga {max_contact_info_len} harfdan ortiq bo'lmagan bo'lishi kerak.'''
,
    'input_name_to_search_process(novalid)dealership': f'<b>Noto‘g‘ri kiritish!</b>\nAvtosalon nomi {max_contact_info_len} belgidan kam bo‘lishi kerak\nva faqat harflar va raqamlardan iborat bo‘lishi kerak: ',
    'input_name_to_search_process(non_exists)': '<b>Ushbu nomdagi {block_state} foydalanuvchi topilmadi</b>',

    'rewrite_tariff_sub_text': '<b>Tarifni tahrirlash</b>\n',
    'add_tariff_sub_text': "<b>Tarif qo'shish</b>\n",
    'input_tariff_cost': {'message_text': "Narxni ko'rsating:",
                          'buttons': {'admin_backward:input_tariff_cost': captions_uz['backward'], 'width': 1}},
    'input_tariff_cost(incorrect)': f"<b>Narx bitta raqamdan iborat bo‘lishi kerak ({max_price_len} ta raqamgacha)</b>\n' $ ' belgisini kiriting mumkin",

    'input_tariff_feedbacks': {'message_text': "Javoblar sonini ko‘rsating:",
                               'buttons': {'admin_backward:input_tariff_feedbacks': captions_uz['backward'], 'width': 1}},
    'input_tariff_feedbacks(incorrect)': f"<b>Javoblar soni faqat butun son sifatida kiritilishi kerak, uzunligi 0 dan {max_feedbacks_len} gacha.</b>",

    'input_tariff_time_duration': {
        'message_text': "Vaqtni kiriting\nFormatda: yillar:oylar:kunlar\nMisol (6 oy va 15 kun): 0:6:15",
        'buttons': {'admin_backward:input_tariff_duration_time': captions_uz['backward'],
                    'width': 1}},
    'input_tariff_time_duration(incorrect)': "<b>Tarifning amal qilish muddati ijobiy va asosli bo'lishi kerak va quyidagi formatda butun sonlar sifatida kiritilishi kerak: yillar:oylar:kunlar</b>",

    'input_tariff_name': {'message_text': '<b>Ismni istalgan formatda kiriting:</b>',
                          'buttons': {'admin_backward:input_tariff_name': captions_uz['backward'], 'width': 1}},
    'input_tariff_name(match)': f'''<b>Ushbu nom boshqa tarifda mavjud\nBoshqa nom kiriting:</b>''',
    'input_tariff_name(len)': f'''<b>Siz maksimal sarlavha uzunligidan oshib ketdingiz - {max_contact_info_len}.</b>\nBoshqa nom kiriting:''',

    'tariff_view_buttons': {'edit_tariff_by_admin': 'Tahrirlash', 'delete_tariff_by_admin': captions_uz['delete'],
                            'admin_backward:check_tariff_info': captions_uz['backward'], 'width': 2},

    'tariff_delete_confirm_action': {'message_text': '<b>Tarifni o‘chirishni tasdiqlash:</b>',
                                     'buttons': {'confirm_delete_tariff_by_admin': captions_uz['delete'],
                                                 'admin_backward:confirm_delete_tariff_action': 'Bekor qilish',
                                                 'width': 1}},

    'start_tariff_edit_action': {'message_text': '<b>Tahrirlash uchun maydonni tanlang:</b>',
                                 'buttons': ('edit_tariff_name', 'edit_tariff_duration_time',
    'edit_tariff_feedbacks_residual', 'edit_tariff_cost',
    {'admin_backward:edit_tariff': captions_uz['backward'],
    'confirm_tariff_edit': captions_uz['confirm'],
    'width': 1})}

                                             }
captions_uz = {'backward': '◂ Orqaga ▸', 'was_selected': 'Siz tanladingiz', 'cancel': 'Bekor qilish', 'confirm': 'Tasdiqlash',
            'sales': 'sotishlar', 'purchases': 'xaridlar', 'any': 'har doim', 'day': 'kun', 'week': 'hafta',
            'month': 'oy', 'year': 'yil', 'days': 'kunlar', 'feedbacks': 'javoblar',
            'dont_write_html_tags': '"&lt; &gt;" belgilarini kiriting taqiqlanadi.',
            'all_users': 'barcha', 'buyers': 'xaridorlar', 'sellers': 'sotuvchilar', 'delete': 'O‘chirish',
            'by_dealership': 'avtosalon', 'by_seller': 'shaxsiy shaxs', 'close': 'Yashirish', 'surname_name_patronymic': 'F.I.Sh.: ', 'add': 'Qo‘shish',
            'successfully': 'Muvaffaqiyatli'
            }

admin_class_mini_lexicon_uz = {
    'search_by_dealership_name_caption': "Ism bo'yicha qidirish",
    'tariff_non_exists_plug_name': 'Tariflar topilmadi',
    'all_tariffs_output_message_text': '<b>Tariflar ro‘yxati:</b>',
    'ban_user_input_reason_dealership': 'avtosalon {name}',
    'ban_user_input_reason_seller': 'xususiy sotuvchi {name}',
    'ban_user_input_reason_buyer': 'xaridor {name}',
    'ban_user_message_text_head': '<b>Bloklash {entity}:</b>\nSababingizni kiriting:',
    'select_tariff_message_text_exists': 'Haqiqatan ham tarifni yangilamoqchimisiz {tariff_name}',
    'select_tariff_message_text_non_exists': 'Haqiqatan ham tarifni o‘rnatmoqchimisiz <b>{tariff_name}</b>',
    'select_tariff_message_text_startswith': '<b>{name} uchun tarif:</b>\n',
    'choose_tariff_message_text': '<b>{name} uchun tarif</b>\nYangi tarifni tanlang:',
    'review_seller_tariff_message_header_legal': '<b>Salon tarifi {name}:</b>',
    'review_seller_tariff_message_header_natural': '<b>Xususiy sotuvchi tarifi {name}:</b>',
    'tariff_not_exists': '<blockquote>Tarif mavjud emas</blockquote>',
    'user_list_message_text': "<b>{block_status} xaridorlar ro'yxati:</b>",
    'natural_list_message_text': "<b>{block_status} shaxslar ro'yxati:</b>",
    'dealership_list_message_text': "<b>{block_status} salonlar ro'yxati:</b>",
    'return_to_user': "Foydalanuvchiga qaytish",
    'set': "O'rnatish",
    'set_tariff': "Tarifni belgilash",
    'remove_tariff': "Tarifni tiklash",
    'search_by_name': "To'liq ism bo'yicha qidiring",
    'return_main_menu': 'Menyuda'
}