import logging
import os
import json
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from config import ORDER_CHAT_ID, PRODUCTION_CHAT_ID, ORDERS_DIR


def load_orders(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    else:
        with open(file_path, 'w') as file:
            json.dump([], file)
        return []


def save_orders(file_path, orders):
    with open(file_path, 'w') as file:
        json.dump(orders, file, indent=4)


def create_order_data(context, order_number, start_time, chat_id, username, user_id):
    return {
        "order_number": order_number,
        "chat_id": chat_id,
        "start_time": start_time,
        "username": username,
        "user_id": user_id
    }


def initialize_order(context: ContextTypes.DEFAULT_TYPE, chat_id, username, user_id) -> bool:
    orders = load_orders('orders.txt')
    order_number = len(orders) + 1
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    order_data = create_order_data(context, order_number, start_time, chat_id, username, user_id)

    orders.append(order_data)
    save_orders('orders.txt', orders)

    context.user_data.update(order_data)
    return True


async def save_photo(order_number, update, context, step, photo_number=None):
    order_dir = os.path.join(ORDERS_DIR, f'Order{order_number}')
    os.makedirs(order_dir, exist_ok=True)
    photo_file = os.path.join(order_dir, f'photo_step{step}_{photo_number}.jpg') if photo_number else os.path.join(
        order_dir, f'photo_step{step}.jpg')
    photo = await update.message.photo[-1].get_file()
    await photo.download_to_drive(photo_file)
    return photo_file


async def handle_photo_sending(update, context, order_number, step, photo_file, photo_number=None):
    if step == 5 and photo_number == 1:
        caption = f"Бизнес зал заказа номер {order_number}"
        context.user_data['photo_step5'] = photo_file
    elif step == 6 and photo_number == 2:
        caption = f"Оплата заказа номер {order_number}"
    else:
        caption = f"Непонятное фото из заказа номер {order_number}"

    await send_photo(update, context, ORDER_CHAT_ID, photo_file, caption)


async def send_photo(update, context, chat_id, photo_path, caption):
    with open(photo_path, 'rb') as photo:
        await context.bot.send_photo(chat_id=chat_id, photo=photo, caption=caption)


async def log_user_step(update: Update, context: ContextTypes.DEFAULT_TYPE, step: int):
    user = update.message.from_user
    logging.info(f"Step {step}, User {user.username}, UserID {user.id}, entered: {update.message.text}")


async def send_order_details(context: ContextTypes.DEFAULT_TYPE, order_number: int, chat_id):
    order_file = os.path.join(ORDERS_DIR, f'Order{order_number}', f'order_{order_number}_data.json')

    if os.path.exists(order_file):
        with open(order_file, 'r', encoding='utf-8') as file:
            order_data = json.load(file)

        details = (
            f"Новый заказ номер {order_number}:\n"
            f"Имя: {order_data['Имя']}\n"
            f"Аэропорт: {order_data['Аэропорт']}\n"
            f"Дата: {order_data['Дата']}\n"
        )
        await context.bot.send_message(chat_id=chat_id, text=details)

        if chat_id != PRODUCTION_CHAT_ID:
            user_data = context.user_data
            await context.bot.send_message(chat_id=chat_id,
                                           text=f"Юзернейм: @{user_data['username']}\nКонтакт: {user_data['contact']}\n")
    else:
        await context.bot.send_message(chat_id=chat_id, text=f"Ошибка: данные заказа номер {order_number} не найдены.")


async def send_orders_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logs_directory = 'logs'
    orders_file = 'orders.txt'
    backup_message = "Сохраню бекап файлы на всякий случай"

    # Send backup message
    await context.bot.send_message(chat_id=ORDER_CHAT_ID, text=backup_message)

    # Find the latest log file
    latest_log_file = None
    if os.path.exists(logs_directory):
        log_files = [f for f in os.listdir(logs_directory) if f.endswith('.log')]
        if log_files:
            latest_log_file = max(log_files, key=lambda x: datetime.strptime(x, '%Y-%m-%d_%H-%M-%S.log'))

    # Send the latest log file if it exists
    if latest_log_file:
        latest_log_path = os.path.join(logs_directory, latest_log_file)
        with open(latest_log_path, 'rb') as log_file:
            await context.bot.send_document(chat_id=ORDER_CHAT_ID, document=log_file, filename=latest_log_file)
    else:
        logging.error("No log files found.")

    # Send the orders file if it exists
    if os.path.exists(orders_file):
        with open(orders_file, 'rb') as file:
            await context.bot.send_document(chat_id=ORDER_CHAT_ID, document=file, filename='orders.txt')
    else:
        logging.error("Orders file does not exist.")


make_backup_handler = CommandHandler('make_backup', send_orders_file)


async def save_order_data(order_number, context):
    order_dir = os.path.join(ORDERS_DIR, f'Order{order_number}')
    os.makedirs(order_dir, exist_ok=True)
    order_file = os.path.join(order_dir, f'order_{order_number}_data.json')
    order_data = {
        "Имя": context.user_data.get('name'),
        "Аэропорт": context.user_data.get('airport'),
        "Дата": context.user_data.get('date')
    }
    with open(order_file, 'w', encoding='utf-8') as file:
        json.dump(order_data, file, ensure_ascii=False, indent=4)

