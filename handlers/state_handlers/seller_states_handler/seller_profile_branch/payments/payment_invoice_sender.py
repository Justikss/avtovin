from aiogram.types import Message, CallbackQuery, LabeledPrice
from aiogram.fsm.context import FSMContext
import importlib

from utils.Lexicon import LexiconCreateInvoice


async def send_invoice_offer(request: CallbackQuery, state: FSMContext):
    tarif_request_module = importlib.import_module('database.data_requests.tariff_requests')

    memory_storage = await state.get_data()
    tariff_id = memory_storage['current_tariff_id']
    tariff_model = tarif_request_module.TarifRequester.get_by_id(tariff_id=tariff_id)
    if tariff_model:        
        
        currency = 'UZS'
        title = LexiconCreateInvoice.title + tariff_model.name
        sub_description = LexiconCreateInvoice.description.split('-')
        sub_description = sub_description[2], sub_description[5] = \
                    tariff_model.feedback_amount, tariff_model.duration_time
        description = ''.join(sub_description)

        request_timeout=60

        invoice_message = await request.message.bot.send_invoice(chat_id=request.message.chat.id,
        currency=currency, title=title, description=description, need_name=True, provider_token='398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065',
                        request_timeout=request_timeout, prices=[LabeledPrice(label=LexiconCreateInvoice.load_price_label, amount=int(tariff_model.price))])
        
    else:
        #отправить на шаг назад
        pass

        
    