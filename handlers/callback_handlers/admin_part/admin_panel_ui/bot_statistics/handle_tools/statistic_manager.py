import importlib
from copy import copy

from database.data_requests.statistic_requests.advert_feedbacks_requests import AdvertFeedbackRequester
from database.tables.statistic_tables.period_seller_statistic import calculate_stats
from handlers.callback_handlers.admin_part.admin_panel_ui.user_actions.actions_admin_to_user.check_seller_statistic.seller_statistic_output import \
    get_period_string
from handlers.utils.create_advert_configuration_block import create_advert_configuration_block

from states.admin_part_states.statistics_states import StatisticsStates


Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

class EmptyField:
    name = Lexicon_module.catalog_captions['empty']
    id = 0

class StatisticManager:
    calculate_statistics = calculate_stats
    ident_period_string = get_period_string
    states = StatisticsStates
    database_requests = AdvertFeedbackRequester
    empty_button_field = EmptyField
    car_params_card_pattern = create_advert_configuration_block

    @staticmethod
    async def statistic_lexicon():
        Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')
        return Lexicon_module.STATISTIC_LEXICON