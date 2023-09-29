import requests
import json
from aiogram import Bot, types, Dispatcher, executor
from dotenv import load_dotenv
import os

load_dotenv()

bot = Bot(os.getenv('API_KEY_TELE'))
dp = Dispatcher(bot=bot)

main_trello_end_point = os.getenv('URL')
trello_key = os.getenv('API_KEY')
trello_token = os.getenv('TOKEN')
application_list_id = os.getenv('ID')

first_run = True


@dp.message_handler(commands=['start'])
async def proccess_start_command(msg: types.Message):
    global first_run
    if first_run:
        await msg.answer(f"Добро пожаловать {msg.from_user.first_name}")
        await msg.answer(f"Это - FasTask\n"
                         f"При помощи этого бота вы можете обращаться в технический отдел!")
        first_run = False


def create_trello_card(card_name, card_desc):
    create_card_end_point = main_trello_end_point + 'cards'
    jsonObject = {"key": trello_key,
                  "token": trello_token,
                  "idList": application_list_id,
                  "name": f"Отдел {card_name}",
                  "desc": card_desc}

    new_card = requests.post(create_card_end_point, json=jsonObject)

    print(json.loads(new_card.text))


@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)
    await msg.reply("Запрос отправлен\n"
                    "в течении 30 минут заявка будет принято")
    print(create_trello_card(msg.text, 'Hello'))


if __name__ == "__main__":
    executor.start_polling(dp)
