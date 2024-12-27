import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='bot.log'
)


# Функция для логирования событий
def log_user_action(update: Update, context, action: str):
    user = update.effective_user
    username = user.username if user.username else user.first_name
    message = update.message.text if update.message else 'No message'
    logging.info(f"User: {username}, Action: {action}, Message: {message}")


async def common_response(update: Update, context):
    log_user_action(update, context, "Command or message received")
    await update.message.reply_text(
        "Бот остановлен до завтра, так как закончились проходки. Попробуйте оформить проходку в другой день.")


def main():
    app = ApplicationBuilder().token('7299154862:AAGVpkJgTVVooGVUR_4-DJxlc2NekyT5sX0').build()

    start_handler = CommandHandler('start', common_response)
    buy_handler = CommandHandler('buy', common_response)
    stop_handler = CommandHandler('stop', common_response)
    help_handler = CommandHandler('help', common_response)
    message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, common_response)

    app.add_handler(start_handler)
    app.add_handler(buy_handler)
    app.add_handler(stop_handler)
    app.add_handler(help_handler)
    app.add_handler(message_handler)

    app.run_polling()


if __name__ == '__main__':
    main()
