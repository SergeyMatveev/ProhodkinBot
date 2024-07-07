import logging
import os
import re

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters

from config import PRODUCTION_CHAT_ID, ORDERS_FILE, ORDER_CHAT_ID
from messages import START_MESSAGE, STOP_MESSAGE, QR_CODE_ERROR_MESSAGE1, QR_CODE_ERROR_MESSAGE2, \
    QR_CODE_ORDER_NOT_FOUND_MESSAGE, QR_CODE_THANK_YOU_MESSAGE
from utils import load_orders, save_photo, ORDERS_DIR, send_photo


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    logging.info(f"User {user.username}, UserID {user.id} has entered start process.")
    await update.message.reply_text(START_MESSAGE)


async def stop_all(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logging.info(f"Stopping process for user {update.message.from_user.username}, UserID {update.message.from_user.id}")
    context.user_data.clear()
    await update.message.reply_text(STOP_MESSAGE)
    return ConversationHandler.END


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    try:
        logging.error(msg="Exception while handling an update:", exc_info=context.error)
    except Exception as e:
        logging.error("Error in error handler: %s", e)


start_handler = CommandHandler('start', start)


async def handle_qr_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(msg=f"Used handle_qr_code step 0")
    if str(update.message.chat_id) != str(PRODUCTION_CHAT_ID):
        logging.info(msg=f"Used handle_qr_code step 1")
        return

    if not update.message.photo or not update.message.caption:
        logging.info(msg="Used handle_qr_code step 2")
        await update.message.reply_text(QR_CODE_ERROR_MESSAGE1)
        return

    order_number_match = re.search(r'\b\d+\b', update.message.caption)
    if not order_number_match:
        logging.info(msg="Used handle_qr_code step 3")
        await update.message.reply_text(QR_CODE_ERROR_MESSAGE2)
        return

    order_number = int(order_number_match.group())
    orders = load_orders(ORDERS_FILE)

    for order in orders:
        if order['order_number'] == order_number:
            chat_id = order['chat_id']
            photo_file = await save_photo(order_number, update, context, step="_qrcode")
            order_dir = os.path.join(ORDERS_DIR, f'Order{order_number}')
            photo_file = os.path.join(order_dir, 'photo_step_qrcode.jpg')

            await update.message.reply_text(f"Заказ №{order_number} выполнен.")

            caption = f"Вот ваш QR-код для заказа №{order_number}."
            await send_photo(update, context, chat_id, photo_file, caption)

            # Send QR code to ORDER_CHAT_ID
            caption_order = f"Куаркод для заказа номер {order_number}"
            await send_photo(update, context, ORDER_CHAT_ID, photo_file, caption_order)

            # Additional message to the user
            await context.bot.send_message(chat_id=chat_id, text=QR_CODE_THANK_YOU_MESSAGE)
            return

    # If the order was not found in the list, send a message to PRODUCTION_CHAT_ID
    await update.message.reply_text(QR_CODE_ORDER_NOT_FOUND_MESSAGE)

qr_code_handler = MessageHandler(filters.PHOTO, handle_qr_code)
