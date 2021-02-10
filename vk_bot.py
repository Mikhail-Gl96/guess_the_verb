import random
import os
import logging

from dotenv import load_dotenv

from dialogflow_funcs import detect_intent_texts

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from MyLogger import create_my_logger


vk_logger = create_my_logger(name=__name__, level=logging.INFO)


def answer_on_intent(event, vk_api):
    random_id = random.randint(1, 1000)
    try:
        answer = detect_intent_texts(project_id=GOOGLE_APPLICATION_PROJECT_ID,
                                     session_id=f'{event.user_id}-{random_id}',
                                     texts=event.text,
                                     language_code="ru-RU")
        if answer:
            vk_api.messages.send(
                user_id=event.user_id,
                message=answer,
                random_id=random_id
            )
            vk_logger.debug(f'send to: {event.user_id} msg: {event.text}')
        else:
            vk_logger.debug(f'no intent detected')
    except Exception as e:
        vk_logger.error(f"error: {e}")


if __name__ == '__main__':
    vk_logger.info('Start VK Bot')

    load_dotenv()

    VKONTAKTE_GROUP_TOKEN = os.getenv("VKONTAKTE_GROUP_TOKEN")
    GOOGLE_APPLICATION_PROJECT_ID = os.getenv("GOOGLE_APPLICATION_PROJECT_ID")

    vk_session = vk.VkApi(token=VKONTAKTE_GROUP_TOKEN)
    vk_api = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            vk_logger.debug('Новое сообщение:')
            if event.to_me:
                vk_logger.debug(f'Для меня от: {event.user_id}')
                answer_on_intent(event, vk_api)
            else:
                vk_logger.debug(f'От меня для: {event.user_id}')
            vk_logger.debug(f'Текст: {event.text}')

