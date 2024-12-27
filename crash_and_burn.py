import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# Chat IDs to exclude
PRODUCTION_CHAT_ID = '-1002191030126'
ORDER_CHAT_ID = '-1002000757373'

# Logging configuration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='bot.log'
)

# Function to log user actions
def log_user_action(update: Update, context, action: str):
    user = update.effective_user
    username = user.username if user.username else user.first_name
    message = update.message.text if update.message else 'No message'
    logging.info(f"User: {username}, Action: {action}, Message: {message}")

# Common response function
async def common_response(update: Update, context):
    if str(update.effective_chat.id) in [PRODUCTION_CHAT_ID, ORDER_CHAT_ID]:
        return  # Do not respond in excluded chats

    log_user_action(update, context, "Command or message received")
    await update.message.reply_text(
        "Бот остановлен до завтра, так как закончились проходки. Попробуйте оформить проходку в другой день.")

# Function to send the log file as backup
async def make_backup(update: Update, context):
    if str(update.effective_chat.id) == ORDER_CHAT_ID:
        try:
            with open('bot.log', 'rb') as log_file:
                await context.bot.send_document(chat_id=ORDER_CHAT_ID, document=log_file, caption="Backup log file")
            log_user_action(update, context, "Backup log sent")
        except Exception as e:
            logging.error(f"Error sending backup: {e}")
            await update.message.reply_text("Failed to send backup.")

# Main function
def main():
    app = ApplicationBuilder().token('7299154862:AAGVpkJgTVVooGVUR_4-DJxlc2NekyT5sX0').build()

    # Handlers
    start_handler = CommandHandler('start', common_response)
    buy_handler = CommandHandler('buy', common_response)
    stop_handler = CommandHandler('stop', common_response)
    help_handler = CommandHandler('help', common_response)
    message_handler = MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        common_response
    )
    backup_handler = CommandHandler('make_backup', make_backup)

    # Add handlers to the application
    app.add_handler(start_handler)
    app.add_handler(buy_handler)
    app.add_handler(stop_handler)
    app.add_handler(help_handler)
    app.add_handler(message_handler)
    app.add_handler(backup_handler)

    app.run_polling()

if __name__ == '__main__':
    main()
