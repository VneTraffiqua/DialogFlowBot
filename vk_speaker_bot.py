import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from environs import Env
import random
from utils import detect_intent_texts


if __name__ == '__main__':
    env = Env()
    env.read_env()
    vk_token = env.str('VK_TOKEN')

    project_id = env.str('PROJECT_ID')
    session_id = env.str('DIALOGFLOW_TOKEN')
    language_code = 'ru-RU'

    vk_session = vk_api.VkApi(token=vk_token)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            message = detect_intent_texts(
                project_id, session_id, event.text, language_code
            )
            if message:
                vk.messages.send(
                    user_id=event.user_id,
                    message=message,
                    random_id=random.randint(1, 1000)
                )
