import logging
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext import Filters, CallbackContext
from environs import Env
from utils import detect_intent_texts

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Здравствуйте, {user.mention_markdown_v2()}\!',
        # reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def bot_answer(update: Update, context: CallbackContext) -> None:
    env = Env()
    env.read_env()
    text = update.message.text
    project_id = env.str('PROJECT_ID')
    session_id = env.str('DIALOGFLOW_TOKEN')
    language_code = 'ru-RU'
    update.message.reply_text(
        detect_intent_texts(project_id, session_id, text, language_code)
    )


def main() -> None:
    env = Env()
    env.read_env()
    tg_token = env.str('TG_TOKEN')

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
        MessageHandler(Filters.text & ~Filters.command, bot_answer())
    )

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
