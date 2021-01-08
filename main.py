import os
import logging


from dotenv import load_dotenv

from MyLogger import create_my_logger


if __name__ == '__main__':
    main_logger = create_my_logger(name=__name__, level=logging.INFO)
    main_logger.info('Start Bot')

    load_dotenv()
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    from telegram_bot import updater
    from vk_bot import longpoll



