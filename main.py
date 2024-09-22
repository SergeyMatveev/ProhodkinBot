# main.py

import logging
import os
from datetime import datetime, timezone
import time

from telegram.ext import ApplicationBuilder
from buy_handler import buy_conv_handler
from config import BOT_TOKEN
from help_handler import help_conv_handler
from other_handlers import start_handler, error_handler, qr_code_handler
from utils import make_backup_handler


def setup_logging():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    log_time = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = os.path.join(log_dir, f"{log_time}.log")

    class UTCFormatter(logging.Formatter):
        converter = time.gmtime

    formatter = UTCFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger()
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    logger.info("Logging setup complete.")


def main() -> None:
    setup_logging()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(start_handler)

    app.add_handler(buy_conv_handler)
    app.add_handler(help_conv_handler)
    app.add_handler(qr_code_handler)
    app.add_handler(make_backup_handler)

    app.add_error_handler(error_handler)

    app.run_polling()


if __name__ == '__main__':
    main()

