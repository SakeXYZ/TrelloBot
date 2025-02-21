from aiogram import executor
from config.config import dp
import handlers.start_handler
import handlers.message_handler

if __name__ == "__main__":
    executor.start_polling(dp)
