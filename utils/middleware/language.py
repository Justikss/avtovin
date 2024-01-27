import importlib
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, CallbackQuery
from icecream import ic

from database.tables.car_configurations import attribute_language_manager
from utils.lexicon_utils.Lexicon import LEXICON, ADVERT_LEXICON, STATISTIC_LEXICON, ADVERT_PARAMETERS_LEXICON, \
    CATALOG_LEXICON, ADMIN_LEXICON, statistic_captions, catalog_captions, captions as first_captions, class_lexicon, \
    LexiconSellerRequests, LexiconSellerProfile, LexiconTariffSelection, LexiconChoicePaymentSystem, \
    LexiconCreateInvoice, LexiconSelectedTariffPreview, LexiconPaymentOperation, LastButtonsInCarpooling, \
    ChooseEngineType, ChooseBrand, ChooseColor, ChooseMileage, ChooseYearOfRelease, ChooseComplectation, ChooseModel, \
    BaseOptionalField
from utils.lexicon_utils.admin_lexicon.admin_catalog_lexicon import catalog_mini_lexicon, \
    AdminReviewCatalogChooseCarBrand
from utils.lexicon_utils.admin_lexicon.admin_lexicon import captions as second_captions, admin_class_mini_lexicon, \
    ChooseTariff, TariffNonExistsPlug, AllTariffsOutput
from utils.lexicon_utils.admin_lexicon.advert_parameters_lexicon import advert_params_class_lexicon, \
    advert_parameters_captions
from utils.lexicon_utils.admin_lexicon.bot_statistics_lexicon import statistic_class_lexicon, TopTenDisplay, \
    SelectCustomParamsProcess
from utils.lexicon_utils.admin_lexicon.contacts_lexicon import ADMIN_CONTACTS, OutputTSContacts
from utils.lexicon_utils.commodity_loader import commodity_loader_lexicon, LexiconCommodityLoader, BaseBootButtons

# ic.disable()


class LanguageMiddleware(BaseMiddleware):
    def __init__(self):
        config_module = importlib.import_module('config_data.config')
        self.lexicon_objects = [ADMIN_LEXICON, CATALOG_LEXICON, ADVERT_PARAMETERS_LEXICON, STATISTIC_LEXICON,
                           ADVERT_LEXICON, LEXICON, config_module.DEFAULT_COMMANDS, config_module.header_message_text,
                           config_module.faq, config_module.faq_seller, config_module.faq_buyer,
                           commodity_loader_lexicon, catalog_mini_lexicon, admin_class_mini_lexicon, first_captions,
                           second_captions,
                           advert_parameters_captions,
                           advert_params_class_lexicon,
                           statistic_class_lexicon,
                           catalog_captions,
                           statistic_captions,
                           class_lexicon, attribute_language_manager, ADMIN_CONTACTS]
        self.lexicon_objects_to_classes = {
            (class_lexicon): [LexiconSellerRequests, LexiconSellerProfile, LexiconTariffSelection,
                            LexiconSelectedTariffPreview, LexiconChoicePaymentSystem, LexiconCreateInvoice,
                            LexiconPaymentOperation, LastButtonsInCarpooling, ChooseEngineType, ChooseBrand,
                            ChooseModel, ChooseComplectation, ChooseYearOfRelease, ChooseMileage, ChooseColor,
                              BaseOptionalField],

            (commodity_loader_lexicon): [BaseBootButtons, LexiconCommodityLoader],

            (catalog_mini_lexicon): [AdminReviewCatalogChooseCarBrand],

            (admin_class_mini_lexicon, second_captions): [TariffNonExistsPlug, AllTariffsOutput,
                                                        ChooseTariff],
            # (advert_params_class_lexicon, advert_parameters_captions): [AdvertParametersChooseState],

            (statistic_class_lexicon): [SelectCustomParamsProcess, TopTenDisplay],
            (ADMIN_CONTACTS): [OutputTSContacts]
        }

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        redis_module = importlib.import_module('handlers.default_handlers.start')  # Ленивый импорт
        ic()
        language = None
        redis_key = f'{str(event.from_user.id)}:language'

        # ic(class_lexicon.language, LexiconSelectedTariffPreview.tariff_block)
        if isinstance(event, CallbackQuery) and event.data.startswith('language_') and len(event.data) == 11:
            redis_value = event.data.split('_')
            if len(redis_value) >= 1:
                if redis_value[0] == 'language':
                    redis_value = redis_value[1]
                    await redis_module.redis_data.set_data(key=redis_key, value=redis_value)
                    language = redis_value

        if not language:
            # ic()
            language = await redis_module.redis_data.get_data(key=f'{redis_key}')
        # ic(language)
        if language:

            for lexicon in self.lexicon_objects:
                # ic(lexicon.language)
                if lexicon.language != language:
                    await lexicon.set_language(language)
#                     ic()
#                     ic(lexicon.language)
                    await self.reinit_instances(lexicon)
                # ic(lexicon.__class__.__name__, lexicon.language)

#         ic(class_lexicon.language, LexiconSelectedTariffPreview.tariff_block)

        return await handler(event, data)



    async def reinit_instances(self, key):
        async def reinit_related(equanced_model):
            # ic(index, key == equanced_model, type(key), equanced_model if isinstance(equanced_model, str) else None)
            if key == equanced_model:
                for related_class in related_classes:
                    # ic(related_class.__class__.__name__)
                    related_class.__init__()
#                 ic(key.__dict__, key.language)

        for index, (keys, related_classes) in enumerate(self.lexicon_objects_to_classes.items()):
            # ic(index, len(keys) if isinstance(key, tuple) else None, type(related_classes), len(related_classes))
            # ic()
            if isinstance(keys, tuple):
                for index, lexicon_model in enumerate(keys):
                    await reinit_related(lexicon_model)
            else:
                await reinit_related(keys)


