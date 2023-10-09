import requests
import json
from aiogram import Bot, types, Dispatcher, executor
from aiogram.types import ReplyKeyboardMarkup
from dotenv import load_dotenv
import os

load_dotenv()

main_trello_end_point = os.getenv('URL')
trello_key = os.getenv('API_KEY')
trello_token = os.getenv('TOKEN')
application_list_id = os.getenv('ID')
bot = Bot(os.getenv('API_KEY_TELE'))
dp = Dispatcher(bot=bot)

main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add('ℹ️Инструкция')


@dp.message_handler(commands=['start'])
async def process_start_command(msg: types.Message):
    await bot.forward_message(-1001792269419, msg.from_user.id, msg.message_id, msg.from_user.first_name)
    text_salam = """
👋Добро пожаловать!🎉
                
🤖Этот бот поможет вам обратиться в технический отдел.👨‍💻
                
❓Чтобы обратиться в технический отдел, просто задайте свой вопрос или проблему.💡
                
📨Бот передаст ваше сообщение сотруднику технического отдел.⏳
                
                
ℹ️ Инструкция ⬇️
                
Пример запроса:
                
Технический отдел, Иванов Иван, Проблема с компьютером
                
Внимание:
                
Отправляйте запросы в формате: [отдел] [фамилия] [имя] [проблема] 📝
                
Не отправляйте стикеры, голосовые сообщения и другие медиафайлы 🔇
                """
    bot_picture = open("botpic.jpg", 'rb')
    await msg.answer_photo(photo=bot_picture, caption=text_salam, reply_markup=main)


@dp.message_handler(text='ℹ️Инструкция')
async def cmd_instructions(msg: types.Message):
    logo = open('Rule.jpg', 'rb')
    info_text = """
Пример запроса:
                
Технический отдел, Иванов Иван, Проблема с компьютером
                
Внимание:
                
Отправляйте запросы в формате: [отдел] [фамилия] [имя] [проблема] 📝
                
❌
                
Не отправляйте стикеры, голосовые сообщения и другие медиафайлы 🔇
                
❌
                """
    await msg.answer_photo(photo=logo, caption=info_text)


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
    await bot.forward_message(-1001792269419, msg.from_user.id, msg.message_id, msg.from_user.first_name)
    print(msg.text.split(' '))
    await bot.send_video(msg.chat.id, open('Gifask.gif', 'rb'),
                         caption="🤖Ваша заявка будет обработана в течение 15 минут!!!🤖")
    list_accept = []
    for i in msg.text.split():
        list_accept.append(i)

    print(list_accept[0:2], list_accept[2::])
    print(create_trello_card(' '.join(list_accept[0:2]), ' '.join(list_accept[2::])))


if __name__ == "__main__":
    executor.start_polling(dp)
