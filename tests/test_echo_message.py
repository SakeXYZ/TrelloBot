import sys
import os
import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from handlers.message_handler import echo_message
import pytest
from aiogram import types


@pytest.mark.asyncio
async def test_echo_message():
    msg = types.Message(
        message_id=1,
        from_user=types.User(id=123, is_bot=False, first_name='TestUser'),
        chat=types.Chat(id=1, type='private'),
        date=int(datetime.datetime.now().timestamp()),  # Заменил None на актуальную дату
        text='Hello'
    )
    response = await echo_message(msg)
    assert response is None
