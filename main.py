import requests
import json
from aiogram import Bot, types, Dispatcher, executor
from aiogram.types import ReplyKeyboardMarkup
from dotenv import load_dotenv
import os

load_dotenv()

bot = Bot(os.getenv('API_KEY_TELE'))
dp = Dispatcher(bot=bot)

main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add('Инструкция').add('Информация')

main_trello_end_point = os.getenv('URL')
trello_key = os.getenv('API_KEY')
trello_token = os.getenv('TOKEN')
application_list_id = os.getenv('ID')

first_run = True


@dp.message_handler(commands=['start'])
async def proccess_start_command(msg: types.Message):
    global first_run
    if first_run:
        await msg.answer_sticker('CAACAgIAAxkBAAIBkmUW1PN9u5EcHxrORjqbxEy9NkPyAAKHAAOYv4ANyUnTtWS5aKUwBA')
        await msg.answer(f"Добро пожаловать {msg.from_user.first_name}")
        await msg.answer(f"Это - FasTask\n"
                         f"При помощи этого бота вы можете обращаться в технический отдел!",
                         reply_markup=main)
        first_run = False


@dp.message_handler(text='Инструкция')
async def cmd_instraction(msg: types.Message):
    await msg.answer_sticker('CAACAgIAAxkBAAIBm2UW1SYLvP95u3HazXA5a7-Vo2lMAAKDAAOYv4ANM11_M-RpKzkwBA')
    await msg.answer("Как правильно писать запрос\n"
                     "ПРИМЕР: Продаж Проблема с интернетом\n"
                     "Вывод: Отдел Продаж\n"
                     "Описание: Проблема с интернетом")


@dp.message_handler(text='Информация')
async def cmd_info(msg: types.Message):
    await msg.answer_sticker('CAACAgIAAxkBAAIBm2UW1SYLvP95u3HazXA5a7-Vo2lMAAKDAAOYv4ANM11_M-RpKzkwBA')
    await msg.answer("Как правильно писать запрос\n"
                     "ПРИМЕР: Продаж Проблема с интернетом\n"
                     "Вывод: Отдел Продаж\n"
                     "Описание: Проблема с интернетом")


def create_trello_card(card_name, card_desc):
    create_card_end_point = main_trello_end_point + 'cards'
    jsonObject = {"key": trello_key,
                  "token": trello_token,
                  "idList": application_list_id,
                  "name": card_name,
                  "desc": card_desc}

    new_card = requests.post(create_card_end_point, json=jsonObject)

    print(json.loads(new_card.text))


@dp.message_handler()
async def echo_message(msg: types.Message):
    print(msg.text.split(' '))
    photo_send = open('12415.jpg', 'rb')
    await msg.answer_sticker('CAACAgIAAxkBAAIBs2UW1Y7Bj1LLBm2yh0RS7sYg5bcwAAKNAAOYv4ANvb8zl4t9VZkwBA')
    await msg.reply("Запрос отправлен\n"
                    "в течении 30 минут заявка будет принято")
    strSplit = msg.text
    listAccept = []
    strSplit = strSplit.split()
    for i in msg.text.split():
        listAccept.append(i)
    print(listAccept[0:2], listAccept[2::])
    print(create_trello_card(' '.join(listAccept[0:2]), ' '.join(listAccept[2::])))


if __name__ == "__main__":
    executor.start_polling(dp)
