from aiogram import types
from aiogram.types import ReplyKeyboardMarkup
from config.config import dp, bot, feedback_chat_id

# Создание клавиатуры с кнопкой "Инструкция"
main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add('ℹ️Инструкция')

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


@dp.message_handler(commands=['start'])
async def process_start_command(msg: types.Message):
    try:
        # Пересылка сообщения пользователя в групповой чат
        await bot.forward_message(feedback_chat_id, msg.from_user.id, msg.message_id)

        text_salam = """
        👋Добро пожаловать!🎉

        🤖Этот бот поможет вам обратиться в технический отдел.👨‍💻

        ❓Чтобы обратиться в технический отдел, просто задайте свой вопрос или проблему.💡

        ℹ️ Инструкция ⬇️

        Пример запроса:

        Технический отдел, Иванов Иван, Проблема с компьютером

        Не отправляйте стикеры, голосовые сообщения и другие медиафайлы 🔇
        """
        bot_picture = open("img/bot_pic.jpg", 'rb')
        await msg.answer_photo(photo=bot_picture, caption=text_salam, reply_markup=main)
    except Exception as startErr:
        print(f'Ошибка при выполнении команды /start: {startErr}')
