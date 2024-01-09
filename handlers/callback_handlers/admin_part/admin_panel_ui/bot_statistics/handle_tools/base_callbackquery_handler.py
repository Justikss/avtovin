from handlers.callback_handlers.admin_part.admin_panel_ui.bot_statistics.handle_tools.statistic_manager import \
    StatisticManager
from utils.oop_handlers_engineering.update_handlers.base_objects.base_callback_query_handler import \
    BaseCallbackQueryHandler

class BaseStatisticCallbackHandler(BaseCallbackQueryHandler):
    statistic_manager = StatisticManager