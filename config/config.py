import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

load_dotenv()

# Получение значений переменных окружения
main_trello_end_point = os.getenv('URL')
trello_key = os.getenv('API_KEY')
trello_token = os.getenv('TOKEN')
application_list_id = os.getenv('ID')

# Инициализация бота и диспетчера
bot = Bot(os.getenv('API_KEY_TELE'))
dp = Dispatcher(bot=bot)

# ID чата для пересылки сообщений
feedback_chat_id = -1001792269419
