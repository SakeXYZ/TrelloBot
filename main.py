import requests
import json
from aiogram import Bot, types, Dispatcher, executor
from aiogram.types import ReplyKeyboardMarkup
from dotenv import load_dotenv
import os

load_dotenv()
# Получение значений переменных окружения из файла .env
main_trello_end_point = os.getenv('URL')
trello_key = os.getenv('API_KEY')
trello_token = os.getenv('TOKEN')
application_list_id = os.getenv('ID')

# Инициализация бота и диспетчера
bot = Bot(os.getenv('API_KEY_TELE'))
dp = Dispatcher(bot=bot)

# Создание клавиатуры с кнопкой "Инструкция"
main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add('ℹ️Инструкция')

try:
    # Обработчик команды /start
    @dp.message_handler(commands=['start'])
    async def process_start_command(msg: types.Message):
        # Пересылка сообщения пользователя в групповой чат
        feedback = -1001792269419
        await bot.forward_message(feedback, msg.from_user.id, msg.message_id, msg.from_user.first_name)
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
        bot_picture = open("img/bot_pic.jpg", 'rb')
        await msg.answer_photo(photo=bot_picture, caption=text_salam, reply_markup=main)
except Exception as startErr:
    # Обработка ошибки, если возникает проблема при выполнении команды /start
    print(f'Ошибка при попытке запустить бота: Ошибка: {startErr}')

try:
    # Обработчик нажатия кнопки "ℹ️Инструкция"
    @dp.message_handler(text='ℹ️Инструкция')
    async def cmd_instructions(msg: types.Message):
        logo = open('img/Rule.jpg', 'rb')
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
except Exception as InfoErr:
    # Обработка ошибки, если возникает проблема при нажатии кнопки "Инструкция"
    print(f"Ошибка {InfoErr} при нажатии кнопки 'Инструкция' ")

try:
    # Функция для создания карточки Trello
    def create_trello_card(card_name, card_desc):
        create_card_end_point = main_trello_end_point + 'cards'
        json_object = {"key": trello_key,
                       "token": trello_token,
                       "idList": application_list_id,
                       "name": card_name,
                       "desc": card_desc}

        # Отправка запроса на создание карточки в Trello
        new_card = requests.post(create_card_end_point, json=json_object)
        return json.loads(new_card.text)
except Exception as SendToTrelloErr:
    # Обработка ошибки, если возникает проблема при отправке запроса в Trello
    print(f"Ошибка {SendToTrelloErr} при отправке запроса в Trello")

try:
    # Обработчик всех остальных сообщений от пользователя
    @dp.message_handler()
    async def echo_message(msg: types.Message):
        # Пересылка сообщения пользователя в групповой чат
        await bot.forward_message(-1001792269419, msg.from_user.id, msg.message_id, msg.from_user.first_name)
        print(msg.text.split(' '))
        # Отправка видео и уведомления о времени обработки заявки
        await bot.send_video(msg.chat.id, open('img/Gif_ask.gif', 'rb'),
                             caption="🤖Ваша заявка будет обработана в течение 15 минут!!!🤖")
        list_accept = []
        for i in msg.text.split():
            list_accept.append(i)

        print(list_accept[0:2], list_accept[2::])
        # Создание карточки Trello на основе текста сообщения пользователя
        print(create_trello_card(' '.join(list_accept[0:2]), ' '.join(list_accept[2::])))
except Exception as WriteRequestsErr:
    print(f"Ошибка {WriteRequestsErr} при отправке на обработке")

if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp)
