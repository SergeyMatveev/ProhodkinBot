import logging
from telegram import Update
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, filters, ContextTypes

from buy_handler import stop_all
from config import ORDER_CHAT_ID, PRODUCTION_CHAT_ID
from messages import START_HELP_MESSAGE, SUPPLIER_MESSAGE_TEMPLATE, SUPPORT_MESSAGE_TEMPLATE, CONFIRMATION_MESSAGE

# Define stage after start
HELP_STEP1 = 1


async def log_user_step(update: Update, context: ContextTypes.DEFAULT_TYPE, step: int):
    user = update.message.from_user
    logging.info(f"Help Step {step}: User {user.username} ({user.id}) entered: {update.message.text}")


async def start_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(START_HELP_MESSAGE)
    return HELP_STEP1


async def help_step1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await log_user_step(update, context, HELP_STEP1)
    context.user_data['issue'] = update.message.text

    # Check if the message is from the PRODUCTION_CHAT_ID
    if str(update.message.chat_id) == PRODUCTION_CHAT_ID:
        text = SUPPLIER_MESSAGE_TEMPLATE.format(username=update.message.from_user.username,
                                                user_id=update.message.from_user.id, issue=context.user_data['issue'])
    else:
        text = SUPPORT_MESSAGE_TEMPLATE.format(username=update.message.from_user.username,
                                               user_id=update.message.from_user.id, issue=context.user_data['issue'])

    # Send the message to ORDER_CHAT_ID
    await context.bot.send_message(
        chat_id=ORDER_CHAT_ID,
        text=text
    )

    await update.message.reply_text(CONFIRMATION_MESSAGE)
    return ConversationHandler.END


help_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('help', start_help)],
    states={
        HELP_STEP1: [MessageHandler(filters.TEXT & ~filters.COMMAND, help_step1)],
    },
    fallbacks=[CommandHandler('stop', stop_all)],
)
