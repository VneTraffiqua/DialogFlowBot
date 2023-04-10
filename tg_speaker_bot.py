import logging
from telegram import Update, ForceReply, error
from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext import Filters, CallbackContext
from environs import Env
from df_connector import detect_intent_texts
from hendlers import LogsHandler


logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Здравствуйте, {user.mention_markdown_v2()}\!',
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text(
        'Вас приветствует, бот поддержки онлайн-издательства "Игра глаголов".'
        '«Игра глаголов» – крупное онлайн-издательство, '
        'помогающее продвигать авторские блоги и публиковать книги.'
        'Вы можете задать любой, интересующий вас вопрос в чате=)'
    )


def bot_answer(update: Update, context: CallbackContext, project_id) -> None:
    text = update.message.text
    print(update.message.chat_id)
    language_code = 'ru-RU'
    message = detect_intent_texts(
        project_id,
        f"tg-{update.message.chat_id}",
        text,
        language_code
    ).fulfillment_text
    update.message.reply_text(message)


def main() -> None:
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    env = Env()
    env.read_env()
    tg_token = env.str('TG_TOKEN')
    project_id = env.str('PROJECT_ID')
    tg_logger_token = env.str('TELEGRAM_LOGGER_TOKEN')
    tg_chat_id = env.str('TG_CHAT_ID')

    try:
        logger.setLevel(logging.DEBUG)
        logger.addHandler(LogsHandler(tg_logger_token, tg_chat_id))
        logger.debug('Бот запущен')
        """Start the bot."""
        # Create the Updater and pass it your bot's token.
        updater = Updater(tg_token)

        # Get the dispatcher to register handlers
        dispatcher = updater.dispatcher

        # on different commands - answer in Telegram
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CommandHandler("help", help_command))

        # on non command i.e message - answer DF in the message on Telegram
        dispatcher.add_handler(
            MessageHandler(
                Filters.text & ~Filters.command,
                lambda update, context: bot_answer(
                    update, context, project_id
                )
            )
        )

        # Start the Bot
        updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        updater.idle()
    except (error.BadRequest, error.NetworkError) as err:
        logger.debug('Ошибка соединения')
        logger.exception(err)

    except error.TelegramError as err:
        logger.debug('Бот упал с ошибкой')
        logger.exception(err)

    except error.InvalidToken as err:
        logger.debug('Неверный токен')
        logger.exception(err)


if __name__ == '__main__':
    main()
