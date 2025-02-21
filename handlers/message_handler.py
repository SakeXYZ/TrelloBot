from aiogram import types
from config.config import dp, bot, feedback_chat_id
from services.trello_service import create_trello_card


@dp.message_handler()
async def echo_message(msg: types.Message):
    try:
        # Пересылка сообщения пользователя в групповой чат
        await bot.forward_message(feedback_chat_id, msg.from_user.id, msg.message_id)

        # Отправка гифки с уведомлением
        await bot.send_video(msg.chat.id, open('img/Gif_ask.gif', 'rb'),
                             caption="🤖Ваша заявка будет обработана в течение 15 минут!!!🤖")

        # Разбиение текста сообщения на части
        list_accept = msg.text.split()

        # Создание карточки Trello на основе сообщения
        card_name = ' '.join(list_accept[0:2])
        card_desc = ' '.join(list_accept[2::])
        response = create_trello_card(card_name, card_desc)
        print(response)
    except Exception as WriteRequestsErr:
        print(f"Ошибка при обработке сообщения: {WriteRequestsErr}")


