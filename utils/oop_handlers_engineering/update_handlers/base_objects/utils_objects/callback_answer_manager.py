from aiogram.types import CallbackQuery


class CallbackAnswerManager:
    def __init__(self, request):
        self.request = request

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if isinstance(self.request, CallbackQuery):
            await self.request.answer()