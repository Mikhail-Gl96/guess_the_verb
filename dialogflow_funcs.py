import logging
import json
import os
from dotenv import load_dotenv

from google.cloud import dialogflow

from MyLogger import TelegramLogsHandler, create_my_logger


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

    log_msg = 'Query text: {}'.format(response.query_result.query_text) + \
              '; Detected intent: {} (confidence: {})'.format(
                  response.query_result.intent.display_name,
                  response.query_result.intent_detection_confidence) + \
              '; Fulfillment text: {}\n'.format(response.query_result.fulfillment_text)
    dialogflow_logger.debug(log_msg)

    if response.query_result.intent.is_fallback:
        return None
    else:
        return response.query_result.fulfillment_text


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
            except Exception as e:
                dialogflow_logger.error('error: {}'.format(e))
        try:
            parent = agents_client.common_project_path(project_id)
            response = agents_client.train_agent(request={'parent': parent})
            dialogflow_logger.debug('Intents trained: {}'.format(response))
        except Exception as e:
            dialogflow_logger.error('error: {}'.format(e))


def create_dict_for_intent(name, messages, training_parts):
    training_phrases = []
    for part in training_parts:
        part_form = {
            "parts": [{
                "text": part
            }]
        }
        training_phrases.append(part_form)

    messages_phrases = []
    for message in messages:
        message_form = {
            "text": {
                "text": [message]
            }
        }
        messages_phrases.append(message_form)

    answer = {
        "display_name": name,
        "messages": messages_phrases,
        "training_phrases": training_phrases
    }
    return answer


dialogflow_logger = create_my_logger(name=__name__, level=logging.INFO)


if __name__ == '__main__':
    load_dotenv()
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    GOOGLE_APPLICATION_PROJECT_ID = os.getenv("GOOGLE_APPLICATION_PROJECT_ID")

    # start this file if you want to upload new intents
    path = os.path.join('intents', 'intents.json')
    upload_intent(filepath=path, project_id=GOOGLE_APPLICATION_PROJECT_ID)


