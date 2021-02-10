import os
import logging

from dialogflow_funcs import detect_intent_texts

from dotenv import load_dotenv

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

from MyLogger import TelegramLogsHandler, create_my_logger


telegram_logger = create_my_logger(name=__name__, level=logging.INFO)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
    telegram_logger.debug(f'/start command activated by {update.effective_chat.id}')


def answer_on_intent(update, context):
    answer = detect_intent_texts(project_id=GOOGLE_APPLICATION_PROJECT_ID,
                                 session_id=update.effective_chat.id,
                                 texts=update.message.text,
                                 language_code="ru-RU")
    if answer:
        context.bot.send_message(chat_id=update.effective_chat.id, text=answer)


if __name__ == '__main__':
    telegram_logger.info(f'Start telegram bot')

    load_dotenv()

    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    GOOGLE_APPLICATION_PROJECT_ID = os.getenv("GOOGLE_APPLICATION_PROJECT_ID")

    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    telegram_logger.addHandler(TelegramLogsHandler(tg_bot=updater.bot, chat_id=TELEGRAM_CHAT_ID))

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    echo_handler = MessageHandler(Filters.text & (~Filters.command), answer_on_intent)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()

