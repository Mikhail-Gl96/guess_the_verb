import logging
import json
import os
from dotenv import load_dotenv

from google.cloud import dialogflow
from google.api_core import exceptions
# google.api_core.exceptions.InvalidArgument

from MyLogger import TelegramLogsHandler, create_my_logger


dialogflow_logger = create_my_logger(name=__name__, level=logging.INFO)


def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=texts,
                                      language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(request={'session': session,
                                                     'query_input': query_input})

    query_info = response.query_result
    log_msg = f'Query text: {query_info.query_text}; ' \
        f'Detected intent: {query_info.intent.display_name} (confidence: {query_info.intent_detection_confidence}); ' \
        f'Fulfillment text: {query_info.fulfillment_text}\n'
    dialogflow_logger.debug(log_msg)

    return None if query_info.intent.is_fallback else query_info.fulfillment_text


def upload_intent(filepath, project_id):
    with open(filepath, encoding='utf-8') as json_file:
        intents = json.load(json_file)

        intents_client = dialogflow.IntentsClient()
        agents_client = dialogflow.AgentsClient()
        parent = agents_client.agent_path(project_id)

        for intent_name in intents.keys():
            questions = intents[intent_name]['questions']
            answer = intents[intent_name]['answer']

            intent = create_dict_for_intent(name=intent_name,
                                            messages=[answer],
                                            training_parts=questions)
            try:
                response = intents_client.create_intent(request={'parent': parent,
                                                                 'intent': intent})
                dialogflow_logger.debug('Intent created: {}'.format(response))
            except exceptions.InvalidArgument as e:
                # google.api_core.exceptions.InvalidArgument
                intent_exists = e.message.count(f"Intent with the display name '{intent_name}' already exists.")
                if not intent_exists:
                    raise e
                dialogflow_logger.error('error: {}'.format(e))

        parent = agents_client.common_project_path(project_id)
        response = agents_client.train_agent(request={'parent': parent})
        dialogflow_logger.debug('Intents trained: {}'.format(response))


def create_dict_for_intent(name, messages, training_parts):
    training_phrases = [{"parts": [{"text": part}]} for part in training_parts]
    messages_phrases = [{"text": {"text": [message]}} for message in messages]
    answer = {
        "display_name": name,
        "messages": messages_phrases,
        "training_phrases": training_phrases
    }
    return answer


if __name__ == '__main__':
    load_dotenv()
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    GOOGLE_APPLICATION_PROJECT_ID = os.getenv("GOOGLE_APPLICATION_PROJECT_ID")

    # start this file if you want to upload new intents
    path = os.path.join('intents', 'intents.json')
    try:
        upload_intent(filepath=path, project_id=GOOGLE_APPLICATION_PROJECT_ID)
    except Exception as e:
        dialogflow_logger.error('error: {}'.format(e))

