import requests
import json
from config.config import main_trello_end_point, trello_key, trello_token, application_list_id

# Функция для создания карточки в Trello
def create_trello_card(card_name, card_desc):
    try:
        create_card_end_point = main_trello_end_point + 'cards'
        json_object = {
            "key": trello_key,
            "token": trello_token,
            "idList": application_list_id,
            "name": card_name,
            "desc": card_desc
        }

        # Отправка запроса на создание карточки
        new_card = requests.post(create_card_end_point, json=json_object)
        return json.loads(new_card.text)
    except Exception as e:
        print(f"Ошибка при создании карточки в Trello: {e}")
