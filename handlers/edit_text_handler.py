import logging
from telegram.ext import (
    CallbackContext, 
    CommandHandler,
)
from telegram import (
    Update,
)
from telegram.constants import ParseMode

from common.config import DEV_USER_ID, GREETINGS_TABLE, PERMISSIONS_TABLE
from datasource.db_controller import YDataBase


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

HELP_MESSAGE = ('Отправьте новый текст приветствия вместе с командой /edit_greeting. '
              + 'В нём можно использовать переменные {full_name} - полное имя пользователя и {username} - его ник.'
              + '\n\nПример (нажми чтобы скопировать)\n<code>/edit_greeting Это новый текст приветствия, {username}</code>'
)


async def edit_greetings_text(update: Update, context: CallbackContext) -> None:
    db = YDataBase()
    user_id = update.effective_user.id

    permissions = db.get_fields_equal(field_filter={'user_id': [user_id]}, table_name=PERMISSIONS_TABLE)
    logger.info(update)
    args = context.args

    if args:
        if user_id == DEV_USER_ID:
            chat_id = int(args[0]) 
            new_text = ' '.join(args[1:])
            
        elif permissions:
            chat_id = int(permissions[0]['chat_id']) 
            new_text = ' '.join(args)

        db.insert_row(dict(chat_id=chat_id, message=new_text), table_name=GREETINGS_TABLE)
        await update.effective_chat.send_message('Текст успешно обновлён')

    else:
        if user_id == DEV_USER_ID:
            chat_id_available = db.get_fields_equal(table_name=GREETINGS_TABLE)
            chat_id_available = [
                f"<code>{row['chat_id']}</code> {row['chat_name']}"
                for row in chat_id_available
            ]
            await update.effective_chat.send_message(
                'Доступные чаты для текста\n\n' + '\n'.join(chat_id_available), 
                parse_mode=ParseMode.HTML
            )            
            
        elif permissions:
            await update.effective_chat.send_message(HELP_MESSAGE, parse_mode=ParseMode.HTML)


edit_text_handler = CommandHandler(
    'edit_greeting',
    edit_greetings_text,
)
