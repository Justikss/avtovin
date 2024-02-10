from aiogram.types import CallbackQuery, LabeledPrice
from aiogram.fsm.context import FSMContext
import importlib

from states.tariffs_to_seller import ChoiceTariffForSellerStates


Lexicon_module = importlib.import_module('utils.lexicon_utils.Lexicon')

async def send_invoice_offer(request: CallbackQuery, state: FSMContext):
    await request.answer(Lexicon_module\
                         .LexiconCreateInvoice.in_progress_notification)
    return

    tarif_request_module = importlib.import_module('database.data_requests.tariff_requests')
    await state.set_state(ChoiceTariffForSellerStates.make_payment)
    memory_storage = await state.get_data()
    tariff_id = memory_storage['current_tariff_id']
    tariff_model = tarif_request_module.TarifRequester.get_by_id(tariff_id=tariff_id)
    if tariff_model:        
        
        currency = 'UZS'
        title = Lexicon_module\
                    .LexiconCreateInvoice.title + tariff_model.name
        sub_description = Lexicon_module\
            .LexiconCreateInvoice.description.split('-')
        sub_description[1], sub_description[3] = \
                    str(tariff_model.feedback_amount), str(tariff_model.duration_time)

        description = ''.join(sub_description)

        request_timeout=60

        invoice_message = await request.message.bot.send_invoice(chat_id=request.message.chat.id,
        currency=currency, title=title, description=description, need_name=True, provider_token='398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065',
                        request_timeout=request_timeout, prices=[LabeledPrice(label=Lexicon_module\
                                                                              .LexiconCreateInvoice.load_price_label, amount=10000)], payload=request.data)
        
    else:
        #отправить на шаг назад
        pass

        
