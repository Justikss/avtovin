# import pytest
# from aiogram.types import Message, Chat, User
# from aiogram.fsm.context import FSMContext
# from unittest.mock import AsyncMock, MagicMock
#
# from handlers.custom_filters.correct_number import CheckInputNumber
#
#
# # Создаем моки для необходимых объектов
# @pytest.fixture
# def mock_message():
#     return Message(chat=Chat(id=1234, type='private'), text="", from_user=User(id=123))
#
# @pytest.fixture
# def mock_state():
#     state = FSMContext(None, None, None)
#     state.get_state = AsyncMock(return_value='CarDealerShipRegistrationStates')
#     return state
#
# @pytest.mark.asyncio
# @pytest.mark.parametrize("input_text,expected", [
#     ("+71234567890", {'input_number': '+7-123-456-78-90'}),
#     ("81234567890", {'input_number': '+7-123-456-78-90'}),
#     ("+9981234567", {'input_number': '+998-12-345-67'}),
#     ("9981234567", {'input_number': '+998-12-345-67'}),
#     ("912345678", {'input_number': '9-123-45-67-8'}),
# ])
# async def test_check_input_number_valid(mock_message, mock_state, input_text, expected):
#     filter = CheckInputNumber()
#     mock_message.text = input_text
#     result = await filter(mock_message, mock_state)
#     assert result == expected
#
# @pytest.mark.asyncio
# @pytest.mark.parametrize("input_text", [
#     "123456",
#     "+123456789012",
#     "abcdefghij",
#     "81234567890123456789",
#     "+71234567890123456789",
#     "99999999999999999999",
#     "+71234567890+71234567890",
#     "+7123456789071234567890",
#     "+71234567890 71234567890",
#     "+7123456789081234567890",
#     "+71234567890 81234567890",
# ])
# async def test_check_input_number_invalid(mock_message, mock_state, input_text):
#     filter = CheckInputNumber()
#     mock_message.text = input_text
#     result = await filter(mock_message, mock_state)
#     assert not result
