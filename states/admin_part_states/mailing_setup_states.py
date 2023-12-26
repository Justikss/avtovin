from aiogram.filters.state import StatesGroup, State

class MailingStates(StatesGroup):
    choosing_recipients = State()  # Выбор получателей рассылки
    entering_text = State()  # Ввод текста рассылки
    uploading_media = State()  # Загрузка медиа для рассылки
    entering_date_time = State()  # Ввод даты и времени рассылки
    confirmation = State()  # Подтверждение деталей рассылки