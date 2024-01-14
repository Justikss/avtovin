import importlib

from utils.lexicon_utils.lexicon_uz.admin_lexicon_uz.admin_lexicon_uz import admin_class_mini_lexicon_uz
from utils.safe_dict_class import SafeDict

config_module = importlib.import_module('config_data.config')
admin_lexicon_uz_module = importlib.import_module('utils.lexicon_utils.lexicon_uz.admin_lexicon_uz.admin_lexicon_uz')
# block_user_reason_text_len = config_module.get('block_user_reason_text_len')
# block_user_reason_text_len = config_module.get('block_user_reason_text_len')

return_main_menu = {'return_main_menu': 'В меню'}
_captions = {'backward': '◂ Назад ▸', 'was_selected': 'Вы выбрали', 'cancel': 'Отменить', 'confirm': 'Подтвердить',
            'sales': 'продажам', 'purchases': 'покупкам', 'any': 'всё время', 'day': 'день', 'week': 'неделю',
            'month': 'месяц', 'year': 'год', 'days': 'дней', 'feedbacks': 'откликов',
            'dont_write_html_tags': 'Запрещён ввод знаков "&lt; &gt;".',
            'all_users': 'всех', 'buyers': 'покупателей', 'sellers': 'продавцов', 'delete': 'Удалить',
            'by_dealership': 'автосалона',
            'by_seller': 'частного лица', 'close': 'Скрыть', 'surname_name_patronymic': 'ФИО: ', 'add': 'Добавить',
            'successfully': 'Успешно'
            }



__ADMIN_LEXICON = {
    'admin_panel_button_caption': '🔑 Админ Панель',
    'user_havent_admin_permission': 'Вы не администратор',
    'users_category_non_exists': 'Пользователи данной категории не зарегистрированы.',
    'user_non_active': 'Данный пользователь оказался неактивен',
    'success_set_tariff': 'Тариф успешно выдан!',
    'failed_set_tariff': 'Тариф не был выдан, пользователь не найден.',
    'tariff_was_reset': 'Тариф успешно обнулён!',
    'action_non_actuality': 'Действие неактуально',
    'user_block_success': 'Пользователь заблокирован!',
    'information_was_updated': 'Информация обновлена!',
    'success_input_tariff_data': 'Успешно!\nТариф {tariff_name} - успешно добавлен!',
    'unsuccessfully_add_tariff': 'Не получилось добавить тариф.',
    'tariff_has_bindings': 'Данный тариф нельзя удалить, так как он активен у пользователей',
    'tariff_was_successfully_removed': 'Тариф успешно удалён!',
    'tariff_was_inactive': 'Данный тариф оказался неактивен!',
    'successfully_edit_action': 'Успешно редактировано!',
    'incorrect_input_block_reason': f'''Ваша причина должна содержать от {config_module.block_user_reason_text_len['min']} до {config_module.block_user_reason_text_len['max']} символов, включительно!\nТекущая длина (без учёта пробелов):\n''',

    'start_admin_panel': {'message_text': 'Добро пожаловать в админ панель.\nВыберите ваше действие:',
                          'buttons': {'admin_button_users': 'Пользователи', 'admin_button_tariffs': 'Тарифы',
                                      'admin_button_catalog': 'Каталог', 'admin_button_advert': 'Реклама',
                                      'admin_button_bot_statistics': 'Статистика бота',
                                      'admin_backward:admin_main_menu': 'Выход',
                                      'width': 2}},

    'select_user_category': {'message_text': 'Выберите категорию пользователей:',
                             'buttons': {'buyer_category_actions': 'Покупатели',
                                         'seller_category_actions': 'Продавцы',
                                         **return_main_menu,
                                         'width': 2}},

    'select_seller_category': {'message_text': 'Выберите категорию продавцов:',
                               'buttons': {'legal_seller_actions': 'Салоны', 'natural_seller_actions': 'Частники',
                                           'admin_backward:choose_seller_category': '◂ Назад ▸',
                                           'width': 2}},

    'review_seller_card': {'message_header': 'Просмотр продавца:',
                           'buttons': {'tariff_actions_by_admin': 'Тариф', 'user_block_action_by_admin': 'Блокировка',
                                       'select_seller_statistic_period': 'Статистика',
                                       'admin_backward:user_profile_review': _captions['backward'],
                                       **return_main_menu, 'width': 2}},

    'review_buyer_card': {'message_text': 'Просмотр покупателя:\n<blockquote>ФИО: {full_name}\nТелефонны номер: {phone_number}</blockquote>',
                          'buttons': {'user_block_action_by_admin': 'Блокировка',
                                      'admin_backward:user_profile_review': _captions['backward'],
                                      **return_main_menu, 'width': 1}},

    'reset_tariff_confirm_request': {'message_text': '\nВы действительно хотите обнулить тариф продавца ?',
                                     'buttons': {'confirm_reset_seller_tariff_action': 'Подтвердить',
                                                 'admin_backward:reset_seller_tariff': _captions['cancel'],
                                                 'width': 1}},
    'final_decision_ban_user': {'message_text': 'Произвести блокировку:\n{user_entity}\nПо причине:\n{reason}',
                                'confirm_block_user_by_admin': _captions['confirm'],
                                'admin_backward:final_confirm_block_user': _captions['backward'],
                                'admin_backward:review_result_profile_protocol': _captions['cancel'],
                                'width': 1},

    'user_ban_notification': {
        'message_text': 'ВНИМАНИЕ!\nВаше отношения к {activity} в нашем боте заблокировано навсегда по причине: {reason}',
    'buttons': {'close_ban_notification': _captions['close'], 'width': 1}},

    'input_name_to_search_process': {'message_text': 'Введите имя желаемого пользователя:',
                                     'buttons': {'admin_backward:input_name_to_search': _captions['backward'],
                                                 'width': 1}},

    'input_name_to_search_process(novalid)': 'Некорректный ввод имени!\nИмя пользователя должно содержать 2-3 слова в формате "ФИО" и содержать в себе только буквы',
    'input_name_to_search_process(novalid)dealership': f'Некорректный ввод!\nНазвание автосалона должно быть длинной менее {config_module.max_contact_info_len} символов\nИ состоять только из букв и цифр: ',
    'input_name_to_search_process(non_exists)': 'Пользователя с таким именем - не найдено',

    'input_tariff_cost': {'message_text': 'Укажите стоимость тарифа:',
                          'buttons': {'admin_backward:input_tariff_cost': _captions['backward'], 'width': 1}},
    'input_tariff_cost(incorrect)': 'Стоимость должна состоять только из цифр\nВозможен ввод со знаком " $ "',

    'input_tariff_feedbacks': {'message_text': 'Укажите количество откликов:',
                               'buttons': {'admin_backward:input_tariff_feedbacks': _captions['backward'], 'width': 1}},
    'input_tariff_feedbacks(incorrect)': 'Количество откликов указывается только в целочисленном виде.',

    'input_tariff_time_duration': {
        'message_text': 'Введите продолжительность времени тарифа\nВ формате: лет:месяцев:дней\nПример (6 месяцев и 15 дней): 0:6:15',
        'buttons': {'admin_backward:input_tariff_duration_time': _captions['backward'],
                    'width': 1}},
    'input_tariff_time_duration(incorrect)': 'Продолжительность времени тарифа должна вводиться в целочисленном формате: лет:месяцев:дней',

    'input_tariff_name': {'message_text': 'Укажите название нового тарифа в произвольном формате:',
                          'buttons': {'admin_backward:input_tariff_name': _captions['backward'], 'width': 1}},
    'input_tariff_name(incorrect)': f'''Данное название уже присутствует у другого тарифа\nВведите другое название:''',


    'tariff_view_buttons': {'edit_tariff_by_admin': 'Редактировать', 'delete_tariff_by_admin': _captions['delete'],
                            'admin_backward:check_tariff_info': _captions['backward'], 'width': 2},

    'tariff_delete_confirm_action': {'message_text': 'Подтвердите действие удаления тарифа:',
                                     'buttons': {'confirm_delete_tariff_by_admin': _captions['delete'],
                                                 'admin_backward:confirm_delete_tariff_action': 'Отменить', 'width': 1}},

    'start_tariff_edit_action': {'message_text': 'Выберите поле для редактирования:',
                                 'buttons': ('edit_tariff_name', 'edit_tariff_duration_time',
                                             'edit_tariff_feedbacks_residual', 'edit_tariff_cost',
                                             {'admin_backward:edit_tariff': _captions['backward'],
                                              'confirm_tariff_edit': _captions['confirm'],
                                              'width': 1})}




}
pagination_interface = {'admin_pagination:-': '←', 'page_counter': '[{start}/{end}]', 'admin_pagination:+': '→'}

safe_dict_module = importlib.import_module('utils.safe_dict_class')
captions = safe_dict_module.SafeDict({'ru': _captions,
                     'uz': admin_lexicon_uz_module.captions_uz})

admin_class_mini_lexicon_ru = {
    'tariff_non_exists_plug_name': 'Тарифов не найдено',
    'all_tariffs_output_message_text': 'Список тарифов:',
    'ban_user_input_reason_dealership': 'автосалона {name}',
    'ban_user_input_reason_seller': 'частного продавца {name}',
    'ban_user_input_reason_buyer': 'покупателя {name}',
    'ban_user_message_text_head': 'Блокировка {entity}:\nВведите вашу причину:',
    'select_tariff_message_text_exists': 'Вы действительно хотите\nобновить тариф на {tariff_name}',
    'select_tariff_message_text_non_exists': 'Вы действительно хотите\nустановить тариф {tariff_name}',
    'select_tariff_message_text_startswith': 'Тариф для {name}:\n',
    'choose_tariff_message_text': 'Тариф для {name}\nВыберите новый тариф:',
    'review_seller_tariff_message_header_legal': 'Тариф салона {name}:',
    'review_seller_tariff_message_header_natural': 'Тариф частного продавца {name}:',
    'tariff_not_exists': '<blockquote>Тариф отсутствует</blockquote>',
    'user_list_message_text': 'Список покупателей:',
    'natural_list_message_text': 'Список частных лиц:',
    'dealership_list_message_text': 'Список салонов:',

    'return_to_user': 'Вернуться к пользователю',
    'set': 'Установить',
    'set_tariff': 'Установить тариф',
    'remove_tariff': 'Обнулить тариф',
    'search_by_name': 'Поиск по имени'
}



# Добавление в узбекский словарь


admin_class_mini_lexicon = SafeDict({'ru': admin_class_mini_lexicon_ru,
                                     'uz': admin_class_mini_lexicon_uz})


class TariffNonExistsPlug:
    def __init__(self):
        self.id = 'None'
        self.name = admin_class_mini_lexicon['tariff_non_exists_plug_name']  # Для русской версии, для узбекской замените на lexicon_uz

class AllTariffsOutput:
    def __init__(self):
        self.message_text = admin_class_mini_lexicon['all_tariffs_output_message_text']
        self.buttons_callback_data = 'admin_select_tariff:'
        self.width = 1
        self.dynamic_buttons = 2
        self.last_buttons = None
        self.backward_command = {'add_tariff_by_admin': captions['add'], **return_main_menu}

class BanUser:
    class InputReason:
        def __init__(self, user_entity, name):
            self.user_entities = {
                    'dealership': admin_class_mini_lexicon['ban_user_input_reason_dealership'],
                    'seller': admin_class_mini_lexicon['ban_user_input_reason_seller'],
                    'buyer': admin_class_mini_lexicon['ban_user_input_reason_buyer']
                }
            self.message_text_head = admin_class_mini_lexicon['ban_user_message_text_head']
            self.width = 1
            self.buttons = {'admin_backward:input_ban_reason': captions['backward'], 'width': self.width}

            self.user_entity = self.user_entities.get(user_entity)

            if self.user_entity:
                self.user_entity = self.user_entity.format(name=name)
                self.message_text = self.message_text_head.format(entity=self.user_entity)
                self.lexicon_part = {'message_text': self.message_text, 'buttons': {**self.buttons}}


class SelectTariff:
    def __init__(self):
        self.message_text = {
        'exists': admin_class_mini_lexicon['select_tariff_message_text_exists'],
        'non_exists': admin_class_mini_lexicon['select_tariff_message_text_non_exists']
        }
        self.message_text_startswith = admin_class_mini_lexicon['select_tariff_message_text_startswith']
        self.last_buttons = {'confirm_set_tariff_to_seller_by_admin': captions['confirm']}
        self.backward_command = {'admin_backward:tariff_to_seller_pre_confirm_moment': captions['cancel']}
        self.width = 1

class ChooseTariff:
    def __init__(self):
        self.buttons_callback_data = 'select_tariff_for_seller_by_admin:'
        self.message_text = admin_class_mini_lexicon['choose_tariff_message_text']  # Или lexicon_uz для узбекской версии
        self.dynamic_buttons = 2
        self.width = 2
        self.backward_command = {'admin_backward:choose_tariff_for_seller': captions['backward'],
                                'admin_backward:review_seller_tariff': admin_class_mini_lexicon['return_to_user']}
        self.last_buttons = None
        self.tariff_review_buttons = {'activate_tariff_by_admin_for_seller': admin_class_mini_lexicon['set'],
                                'admin_backward:tariff_for_seller_review': captions['backward'], 'width': 1}

class ReviewSellerTariff:
    def __init__(self, tariff_exists):
        self.message_header = {
            'legal': admin_class_mini_lexicon['review_seller_tariff_message_header_legal'],
            'natural': admin_class_mini_lexicon['review_seller_tariff_message_header_natural']
        }
        self.set_tariff_button = {'set_seller_tariff_by_admin': captions['set_tariff']}
        self.remove_tariff_buttons = {'reset_seller_tariff_by_admin': captions['remove_tariff']}
        self.backward_buttons = {'admin_backward:review_seller_tariff': captions['backward']}
        self.tariff_not_exists = admin_class_mini_lexicon['tariff_not_exists']

        if tariff_exists:
            self.width = 2
            self.buttons = {**self.set_tariff_button, **self.remove_tariff_buttons, **self.backward_buttons,
                            'width': self.width}
        else:
            self.width = 1
            self.buttons = {**self.set_tariff_button, **self.backward_buttons, 'width': self.width}

class UserList:
    def __init__(self, user_status):
        self.buttons_callback_data = 'user_select_action:'
        self.search_by_name_button_caption = captions['search_by_name']
        self.search_by_name_callback_data_startswith = 'from_admin_search_by_name'
        self.backward_command = {'admin_backward:user_list_to_admin': captions['backward'], **return_main_menu}
        self.message_text = admin_class_mini_lexicon['user_list_message_text']
        self.width = 1
        self.dynamic_buttons = 2
        self.search_by_name_button = {f'{self.search_by_name_callback_data_startswith}{user_status}': self.search_by_name_button_caption}
        self.last_buttons = {**self.search_by_name_button}

class SellerList(UserList):
    buttons_callback_data = 'seller_select_action:'
    backward_command = {'admin_backward:seller_list_to_admin': captions['backward']}

class NaturalList:
    def __init__(self):
        self.message_text = admin_class_mini_lexicon['natural_list_message_text']

NaturalList = NaturalList()
TariffNonExistsPlug = TariffNonExistsPlug()
AllTariffsOutput = AllTariffsOutput()
SelectTariff = SelectTariff()
ChooseTariff = ChooseTariff()

class DealershipList:
    def __init__(self, seller_status):
        self.message_text = admin_class_mini_lexicon['dealership_list_message_text']
        self.message_text = NaturalList.message_text if seller_status == 'natural' \
            else self.message_text





''''''
# class TariffNonExistsPlug:
#     id = 'None'
#     name = 'Тарифов не найдено'
#
# class AllTariffsOutput:
#     message_text = 'Список тарифов:'
#     buttons_callback_data = 'admin_select_tariff:'
#     width = 1
#     dynamic_buttons = 2
#     last_buttons = None
#     backward_command = {'add_tariff_by_admin': 'Добавить', **return_main_menu}
#
# class BanUser:
#     class InputReason:
#         user_entities = {'dealership': 'автосалона {name}', 'seller': 'частного продавца {name}',
#                          'buyer': 'покупателя {name}'}
#
#         message_text_head = 'Блокировка {entity}:\nВведите вашу причину:'
#         width = 1
#         buttons = {'admin_backward:input_ban_reason': _captions['backward'], 'width': width}
#
#         def __init__(self, user_entity, name):
#             self.buttons = self.buttons
#
#             self.user_entity = self.user_entities.get(user_entity)
#
#             if self.user_entity:
#                 self.user_entity = self.user_entity.format(name=name)
#                 self.message_text = self.message_text_head.format(entity=self.user_entity)
#                 self.lexicon_part = {'message_text': self.message_text, 'buttons': {**self.buttons}}
#
# class SelectTariff:
#     message_text = {'exists': 'Вы действительно хотите\nобновить тариф на {tariff_name}', 'non_exists': 'Вы действительно хотите\nустановить тариф {tariff_name}'}
#     message_text_startswith = 'Тариф для {name}:\n'
#     last_buttons = {'confirm_set_tariff_to_seller_by_admin': 'Подтвердить'}
#     backward_command = {'admin_backward:tariff_to_seller_pre_confirm_moment': _captions['cancel']}
#     width = 1
#
#     def __init__(self, tariff_exists, tariff_name, seller_name):
#         self.message_text_startswith = self.message_text_startswith.format(name=seller_name)
#         self.message_text = self.message_text['exists'] if tariff_exists else self.message_text['non_exists']
#         self.message_text = self.message_text_startswith + self.message_text.format(tariff_name=tariff_name)
#         self.last_buttons = self.last_buttons
#         self.backward_command = self.backward_command
#         self.width = self.width
#         self.lexicon_part = {'message_text': self.message_text, 'buttons': {**self.last_buttons,
#                                                                             **self.backward_command,
#                                                                             'width': self.width
#                                                                             }
#                              }

# class ChooseTariff:
#     buttons_callback_data = 'select_tariff_for_seller_by_admin:'
#     message_text = 'Тариф для {name}\nВыберите новый тариф:'
#     dynamic_buttons = 2
#     width = 2
#     backward_command = {'admin_backward:choose_tariff_for_seller': _captions['backward'],
#                     'admin_backward:review_seller_tariff': 'Вернуться к пользователю'}
#     last_buttons = None
#     tariff_review_buttons = {'activate_tariff_by_admin_for_seller': 'Установить',
#                              'admin_backward:tariff_for_seller_review': 'Назад', 'width': 1}
#
# class ReviewSellerTariff:
#     message_header = {'legal': 'Тариф салона {name}:',
#                                                 'natural': 'Тариф частного продавца {name}:'}
#     set_tariff_button = {'set_seller_tariff_by_admin': 'Установить тариф'}
#     remove_tariff_buttons = {'reset_seller_tariff_by_admin': 'Обнулить тариф'}
#     backward_buttons = {'admin_backward:review_seller_tariff': _captions['backward']}
#     tariff_not_exists = '<blockquote>Тариф отсутствует</blockquote>'
#
#     def __init__(self, tariff_exists):
#         self.message_header = self.message_header
#         self.tariff_not_exists = self.tariff_not_exists
#         if tariff_exists:
#             self.width = 2
#             self.buttons = {**self.set_tariff_button, **self.remove_tariff_buttons, **self.backward_buttons,
#                             'width': self.width}
#         else:
#             self.width = 1
#             self.buttons = {**self.set_tariff_button, **self.backward_buttons, 'width': self.width}
#
# class UserList:
#     buttons_callback_data = 'user_select_action:'
#     search_by_name_button_caption = 'Поиск по имени'
#     search_by_name_callback_data_startswith = 'from_admin_search_by_name'
#     backward_command = {'admin_backward:user_list_to_admin': _captions['backward'], **return_main_menu}
#     message_text = 'Список покупателей:'
#     width = 1
#     dynamic_buttons = 2
#     def __init__(self, user_status):
#         self.dynamic_buttons = self.dynamic_buttons
#         self.buttons_callback_data = self.buttons_callback_data
#         self.search_by_name_button_caption = self.search_by_name_button_caption
#         self.search_by_name_callback_data_startswith = self.search_by_name_callback_data_startswith
#         self.backward_command = self.backward_command
#         self.message_text = self.message_text
#         self.search_by_name_button = \
#             {f'{self.search_by_name_callback_data_startswith}_{user_status}': self.search_by_name_button_caption}
#         self.last_buttons = {**self.search_by_name_button}
#         self.width = self.width
#
#
# class SellerList(UserList):
#     buttons_callback_data = 'seller_select_action:'
#     backward_command = {'admin_backward:seller_list_to_admin': 'Назад'}
#
#     class NaturalList:
#         message_text = 'Список частных лиц:'
#
#     class DealershipList:
#         message_text = 'Список салонов:'
#
#     def __init__(self, seller_status):
#         super().__init__(seller_status)
#         self.message_text = self.NaturalList.message_text if seller_status == 'natural' \
#                                                             else self.DealershipList.message_text

# def get_captions():

    # return captions

# captions = get_captions()