import vk_api
import logging
from vk_api.longpoll import VkLongPoll, VkEventType
from environs import Env
import random
from hendlers import LogsHandler
from df_connector import detect_intent_texts
from vk_api.exceptions import VkRequestsPoolException, ApiHttpError, AuthError, ApiError


logger = logging.getLogger(__name__)


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    env = Env()
    env.read_env()
    tg_logger_token = env.str('TELEGRAM_LOGGER_TOKEN')
    tg_chat_id = env.str('TG_CHAT_ID')
    vk_token = env.str('VK_TOKEN')
    project_id = env.str('PROJECT_ID')
    session_id = env.str('DIALOGFLOW_TOKEN')
    language_code = 'ru-RU'
    try:
        logger.setLevel(logging.DEBUG)
        logger.addHandler(LogsHandler(tg_logger_token, tg_chat_id))
        logger.debug('Бот запущен')

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
    except VkRequestsPoolException as err:
        logger.debug('Бот упал с ошибкой')
        logger.exception(err)

    except AuthError as err:
        logger.debug('Бот упал с ошибкой')
        logger.exception(err)

    except ApiHttpError as err:
        logger.debug('Бот упал с ошибкой')
        logger.exception(err)

    except ApiError as err:
        logger.debug('Бот упал с ошибкой')
        logger.exception(err)

