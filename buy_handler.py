import asyncio
import json
import os

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters

from config import ORDER_CHAT_ID, PRODUCTION_CHAT_ID, ORDERS_DIR
from other_handlers import stop_all
from messages import (
    START_BUY_MESSAGE,
    ERROR_MESSAGE,
    STEP1_MESSAGE,
    STEP2_MESSAGE,
    STEP3_MESSAGE,
    STEP4_MESSAGE,
    STEP4_INSTRUCTION_MESSAGE,
    STEP5_ERROR_MESSAGE,
    ORDER_SAVED_MESSAGE,
    STEP6_MESSAGE,
    STEP6_ERROR_MESSAGE,
    ORDER_ACCEPTED_MESSAGE,
    PRODUCTION_ORDER_CAPTION
)

from utils import (
    initialize_order,
    save_photo,
    save_order_data,
    log_user_step,
    send_order_details,
    send_photo, handle_photo_sending
)

# Define steps
BUY_STEP1, BUY_STEP2, BUY_STEP3, BUY_STEP4, BUY_STEP5, BUY_STEP6 = range(6)


async def start_buy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.message.chat_id
    username = update.message.from_user.username
    user_id = update.message.from_user.id

    if initialize_order(context, chat_id, username, user_id):
        await update.message.reply_text(START_BUY_MESSAGE)
        return BUY_STEP1
    else:
        await update.message.reply_text(ERROR_MESSAGE)
        return ConversationHandler.END


async def buy_step1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await log_user_step(update, context, BUY_STEP1)
    context.user_data['name'] = update.message.text
    await update.message.reply_text(STEP1_MESSAGE)
    return BUY_STEP2


async def buy_step2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await log_user_step(update, context, BUY_STEP2)
    context.user_data['date'] = update.message.text
    await update.message.reply_text(STEP2_MESSAGE)
    return BUY_STEP3


async def buy_step3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await log_user_step(update, context, BUY_STEP3)
    context.user_data['contact'] = update.message.text
    await update.message.reply_text(STEP3_MESSAGE)
    return BUY_STEP4


async def buy_step4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await log_user_step(update, context, BUY_STEP4)
    context.user_data['airport'] = update.message.text

    order_number = context.user_data['order_number']

    # Сохранение текстовых данных заказа в JSON файл
    await save_order_data(order_number, context)

    order_number = context.user_data['order_number']
    await send_order_details(context, order_number, ORDER_CHAT_ID)

    await update.message.reply_text(STEP4_MESSAGE)
    with open('help.jpg', 'rb') as photo:
        await context.bot.send_photo(chat_id=update.message.chat_id, photo=photo, caption=STEP4_INSTRUCTION_MESSAGE)

    return BUY_STEP5


async def buy_step5(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if not update.message.photo:
        if update.message.document:
            await update.message.reply_text(STEP5_ERROR_MESSAGE)
            return BUY_STEP5
    if not update.message.photo:
        await update.message.reply_text(STEP5_ERROR_MESSAGE)
        return BUY_STEP5

    await log_user_step(update, context, BUY_STEP5)
    order_number = context.user_data['order_number']

    photo_file = await save_photo(order_number, update, context, step=5, photo_number=1)
    await handle_photo_sending(update, context, order_number, step=5, photo_file=photo_file, photo_number=1)

    await update.message.reply_text(
        ORDER_SAVED_MESSAGE.format(
            order_number=order_number,
            name=context.user_data['name'],
            airport=context.user_data['airport'],
            date=context.user_data['date']
        )
    )

    await update.message.reply_text(STEP6_MESSAGE)
    return BUY_STEP6


async def buy_step6(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if not update.message.photo:
        if update.message.document:
            await update.message.reply_text(STEP6_ERROR_MESSAGE)
            return BUY_STEP6
    if not update.message.photo:
        await update.message.reply_text(STEP6_ERROR_MESSAGE)
        return BUY_STEP6

    order_number = context.user_data['order_number']
    photo_file = await save_photo(order_number, update, context, step=6, photo_number=2)
    await handle_photo_sending(update, context, order_number, step=6, photo_file=photo_file, photo_number=2)

    await update.message.reply_text(
        ORDER_ACCEPTED_MESSAGE.format(order_number=order_number)
    )

    # Запуск асинхронной задачи для отправки в PRODUCTION_CHAT_ID через 3 минуты
    context.application.create_task(
        schedule_send_order_details(context, order_number, update, context.user_data['photo_step5'])
    )

    return ConversationHandler.END


async def schedule_send_order_details(context: ContextTypes.DEFAULT_TYPE, order_number: int, update: Update,
                                      photo: str) -> None:
    await asyncio.sleep(180)
    await send_order_details(context, order_number, PRODUCTION_CHAT_ID)

    caption = PRODUCTION_ORDER_CAPTION.format(order_number=order_number)
    await send_photo(update, context, PRODUCTION_CHAT_ID, photo, caption)


buy_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('buy', start_buy)],
    states={
        BUY_STEP1: [MessageHandler(filters.TEXT & ~filters.COMMAND, buy_step1)],
        BUY_STEP2: [MessageHandler(filters.TEXT & ~filters.COMMAND, buy_step2)],
        BUY_STEP3: [MessageHandler(filters.TEXT & ~filters.COMMAND, buy_step3)],
        BUY_STEP4: [MessageHandler(filters.TEXT & ~filters.COMMAND, buy_step4)],
        BUY_STEP5: [MessageHandler(filters.PHOTO | filters.Document.ALL | filters.TEXT & ~filters.COMMAND, buy_step5)],
        BUY_STEP6: [MessageHandler(filters.PHOTO | filters.Document.ALL | filters.TEXT & ~filters.COMMAND, buy_step6)]
    },
    fallbacks=[CommandHandler('stop', stop_all)]
)
