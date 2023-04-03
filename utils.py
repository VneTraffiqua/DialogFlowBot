from google.cloud import dialogflow
from environs import Env


def detect_intent_texts(project_id, session_id, text, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""


    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(
        text=text, language_code=language_code
    )

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response.query_result.fulfillment_text


if __name__ == '__main__':
    env = Env()
    env.read_env()
    project_id = env.str('PROJECT_ID')
    session_id = env.str('DIALOGFLOW_TOKEN')
    texts = ['хала']
    language_code = 'ru-RU'

    detect_intent_texts(project_id, session_id, texts, language_code)