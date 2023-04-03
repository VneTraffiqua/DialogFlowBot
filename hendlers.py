import logging
import telegram


class LogsHandler(logging.Handler):
    def __init__(self, tg_token, tg_chat_id):
        super().__init__()
        self.tg_chat_id = tg_chat_id
        self.tg_token = tg_token
        self.bot_logger = telegram.Bot(token=self.tg_token)

    def emit(self, record) -> None:
        log_entry = self.format(record)
        self.bot_logger.send_message(chat_id=self.tg_chat_id, text=log_entry)
