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
main.add('Информация').add('Инструкция')

main_trello_end_point = os.getenv('URL')
trello_key = os.getenv('API_KEY')
trello_token = os.getenv('TOKEN')
application_list_id = os.getenv('ID')

first_run = True


@dp.message_handler(commands=['start'])
async def process_start_command(msg: types.Message):
    global first_run
    if first_run:
        await msg.answer(f"Добро пожаловать {msg.from_user.first_name}", reply_markup=main)
        await msg.answer('При помощи этого бота вы можете обращаться в технический отдел!')
        first_run = False


@dp.message_handler(text='Информация')
async def cmd_instructions(msg: types.Message):
    logo = open('logo.png', 'rb')
    await msg.answer_photo(photo=logo, caption='hello')


@dp.message_handler(text='Инструкция')
async def cmd_info(msg: types.Message):
    await msg.answer("Пример как писать запрос ⤵\n"
                     "Отдел продаж, сотрудник Лев Яшин, нет подключение к сети\n"
                     "--------------------------------------------------------------------------------")


def create_trello_card(card_name, card_desc):
    create_card_end_point = main_trello_end_point + 'cards'
    json_object = {"key": trello_key,
                   "token": trello_token,
                   "idList": application_list_id,
                   "name": card_name,
                   "desc": card_desc}

    new_card = requests.post(create_card_end_point, json=json_object)
    return json.loads(new_card.text)


@dp.message_handler()
async def echo_message(msg: types.Message):
    print(msg.text.split(' '))
    await msg.reply("Запрос отправлен\n"
                    "в течении 30 минут заявка будет принято")
    list_accept = []
    for i in msg.text.split():
        list_accept.append(i)
    print(list_accept[0:2], list_accept[2::])
    print(create_trello_card(' '.join(list_accept[0:2]), ' '.join(list_accept[2::])))


if __name__ == "__main__":
    executor.start_polling(dp)
