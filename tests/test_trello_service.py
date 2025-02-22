import pytest
from services.trello_service import create_trello_card
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_create_trello_card_success(requests_mock):
    url = "https://api.trello.com/1/cards"
    requests_mock.post(url, json={"id": "test_card_id", "name": "Test Card"})
    response = create_trello_card("Test Card", "Test Description")
    assert response["id"] == "test_card_id"
    assert response["name"] == "Test Card"
