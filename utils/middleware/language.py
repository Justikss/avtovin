import importlib
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, CallbackQuery

from utils.lexicon_utils.Lexicon import LEXICON, ADVERT_LEXICON, STATISTIC_LEXICON, ADVERT_PARAMETERS_LEXICON, \
    CATALOG_LEXICON, ADMIN_LEXICON, statistic_captions, catalog_captions, captions as first_captions, class_lexicon, \
    LexiconSellerRequests, LexiconSellerProfile, LexiconTariffSelection, LexiconChoicePaymentSystem, \
    LexiconCreateInvoice, LexiconSelectedTariffPreview, LexiconPaymentOperation, LastButtonsInCarpooling, \
    ChooseEngineType, ChooseBrand, ChooseColor, ChooseMileage, ChooseYearOfRelease, ChooseComplectation, ChooseModel
from utils.lexicon_utils.admin_lexicon.admin_catalog_lexicon import catalog_mini_lexicon, \
    AdminReviewCatalogChooseCarBrand
from utils.lexicon_utils.admin_lexicon.admin_lexicon import captions as second_captions, admin_class_mini_lexicon, \
    NaturalList, ChooseTariff, TariffNonExistsPlug, AllTariffsOutput, SelectTariff
from utils.lexicon_utils.admin_lexicon.advert_parameters_lexicon import advert_params_class_lexicon, \
    advert_params_captions, AdvertParametersChooseState
from utils.lexicon_utils.admin_lexicon.bot_statistics_lexicon import statistic_class_lexicon, TopTenDisplay, \
    SelectCustomParamsProcess
from utils.lexicon_utils.commodity_loader import commodity_loader_lexicon, LexiconCommodityLoader, BaseBootButtons


class LanguageMiddleware(BaseMiddleware):
    def __init__(self):
        config_module = importlib.import_module('config_data.config')
        self.lexicon_objects = [ADMIN_LEXICON, CATALOG_LEXICON, ADVERT_PARAMETERS_LEXICON, STATISTIC_LEXICON,
                           ADVERT_LEXICON, LEXICON, config_module.DEFAULT_COMMANDS, config_module.header_message_text,
                           config_module.faq, config_module.faq_seller, config_module.faq_buyer,
                           commodity_loader_lexicon, catalog_mini_lexicon, admin_class_mini_lexicon, first_captions,
                           second_captions,
                           advert_params_captions,
                           advert_params_class_lexicon,
                           statistic_class_lexicon,
                           catalog_captions,
                           statistic_captions,
                           class_lexicon]
        self.lexicon_objects_to_classes = {
            class_lexicon: [LexiconSellerRequests, LexiconSellerProfile, LexiconTariffSelection,
                            LexiconSelectedTariffPreview, LexiconChoicePaymentSystem, LexiconCreateInvoice,
                            LexiconPaymentOperation, LastButtonsInCarpooling, ChooseEngineType, ChooseBrand,
                            ChooseModel, ChooseComplectation, ChooseYearOfRelease, ChooseMileage, ChooseColor],

            (commodity_loader_lexicon): [BaseBootButtons, LexiconCommodityLoader],

            (catalog_mini_lexicon): [AdminReviewCatalogChooseCarBrand],

            (admin_class_mini_lexicon, second_captions): [NaturalList, TariffNonExistsPlug, AllTariffsOutput,
                                                          SelectTariff, ChooseTariff],
            (advert_params_class_lexicon): [AdvertParametersChooseState],

            (statistic_class_lexicon): [SelectCustomParamsProcess, TopTenDisplay]
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

        if isinstance(event, CallbackQuery) and event.data.startswith('language_') and len(event.data) == 11:

            redis_value = event.data.split('_')
            if len(redis_value) >= 1:
                if redis_value[0] == 'language':
                    redis_value = redis_value[1]
                    await redis_module.redis_data.set_data(key=redis_key, value=redis_value)
                    language = redis_value

        if not language:
            ic()
            language = await redis_module.redis_data.get_data(key=f'{redis_key}')
        ic(language)
        if language:

            for lexicon in self.lexicon_objects:
                ic(lexicon.language)
                if lexicon.language != language:
                    await lexicon.set_language(language)
                    ic()
                    ic(lexicon.language)
                    await self.reinit_instances(lexicon)

        return await handler(event, data)

    async def reinit_instances(self, key):
        for keys, related_classes in self.lexicon_objects_to_classes.items():
            for lexicon_model in keys:
                if key == lexicon_model:
                    for related_class in related_classes:
                        related_class.__init__()
