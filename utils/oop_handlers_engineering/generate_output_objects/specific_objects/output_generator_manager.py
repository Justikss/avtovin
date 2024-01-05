from utils.oop_handlers_engineering.generate_output_objects.specific_objects.base_admin_pagination import \
    AdminPaginationInit
from utils.oop_handlers_engineering.generate_output_objects.specific_objects.base_inline_pagination import \
    InlinePaginationInit
from utils.oop_handlers_engineering.generate_output_objects.specific_objects.base_travel_editor import \
    TravelMessageEditorInit

class MenuGenerator:
    travel_editor = TravelMessageEditorInit
    inline_pagination = InlinePaginationInit
    admin_simple_pagination = AdminPaginationInit