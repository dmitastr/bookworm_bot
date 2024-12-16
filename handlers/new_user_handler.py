import logging
from telegram.ext import (
    CallbackContext, 
    ChatMemberHandler,
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

GREET_TEMPLATE = '@{username} {full_name}, привет! Актуальная информация в закрепе'


async def greet_new_user(update: Update, context: CallbackContext) -> None:
    db = YDataBase()
    chat_id = update.effective_chat.id
    status = update.chat_member.new_chat_member.status

    greet_messages = db.get_fields_equal(
        field_filter=dict(chat_id=[chat_id], is_active=[1]), 
        table_name=GREETINGS_TABLE
    )
    greet_message = get_list_elements(greet_messages)

    logger.info(update.chat_member)

    if status == 'member' and greet_message:
        message = greet_message.get('message', GREET_TEMPLATE) 
        is_temporary = greet_message.get('is_temporary', 0) 
        full_name = update.chat_member.new_chat_member.user.full_name
        username = update.chat_member.new_chat_member.user.username
        
        if username:
            username = '@' + username
        else:
            username = full_name

        sent_message = await update.effective_chat.send_message(
            message.format(
                username=username,
                full_name=full_name
            ),
            parse_mode=ParseMode.HTML
        )
        
        if is_temporary:
            db.insert_row(
                new_row=dict(
                    chat_id=chat_id, 
                    message_id=sent_message.message_id, 
                    timestamp=int(arrow.utcnow().timestamp),
                    is_deleted=False
                ),
                table_name=MESSAGE_HIST_TABLE
            )

            


new_user_handler = ChatMemberHandler(
    greet_new_user,
    chat_member_types=ChatMemberHandler.ANY_CHAT_MEMBER
)