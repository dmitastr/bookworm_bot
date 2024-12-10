import logging
from telegram.ext import (
    CallbackContext, 
    CommandHandler,
)
from telegram import (
    Update,
)
from telegram.constants import ParseMode
import arrow

from common.config import GREETINGS_TABLE, MESSAGE_HIST_TABLE
from common.null_safety_utils import get_list_elements

from datasource.db_controller import YDataBase


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

HELP_MESSAGE = ('Привет! Это бот для настройки приветственного сообщения в чате. \n' +
'Если ты пишешь первый раз, пришли @dmastr свой ID (кликабельно)=<code>{user_id}</code> \n\n' +
'Отправь /edit_greeting чтобы изменить текст приветствия'
)


async def show_help_message(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    await update.effective_chat.send_message(
        HELP_MESSAGE.format(user_id=user_id),
        parse_mode=ParseMode.HTML
    )
            

start_handler = CommandHandler(
    ['start', 'help'],
    show_help_message,
)