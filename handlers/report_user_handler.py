import logging
from telegram.ext import (
    CallbackContext, 
    CommandHandler,
    filters
)
from telegram import (
    Update,
)
from telegram.constants import ParseMode
import arrow

from common.config import BAN_TRESHOLD, DTTM_FORMAT, REPORTS_TABLE
from datasource.db_controller import reports_to_user, YDataBase


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


async def report_user(update: Update, context: CallbackContext) -> None:
    message = None
    original_message = update.effective_message.reply_to_message
    reporter_user_id = update.effective_message.from_user.id

    admins = await update.effective_chat.get_administrators()
    admins_user_id = [admin.user.id for admin in admins]

    if original_message:
        suspected_user = original_message.from_user
        if suspected_user.id in admins_user_id:
            return None
        
        chat_id = update.effective_chat.id

        db = YDataBase(db_name='reports')
        reports = reports_to_user(chat_id=chat_id, user_id=suspected_user.id, cursor=db)
        is_new_report = not any([
            report['chat_id']==chat_id and report['reporter_id']==reporter_user_id 
            for report in reports
        ])

        if is_new_report:
            db.insert_row(
                new_row=dict(
                    chat_id=chat_id,
                    suspected_user_id=suspected_user.id,
                    reporter_id=reporter_user_id,
                    dttm=arrow.now().format(DTTM_FORMAT)
                ),
                table_name=REPORTS_TABLE
            )

            if len(reports) + 1 >= BAN_TRESHOLD:
                message = f"Пользователь {suspected_user.full_name} удалён из чата"
                await original_message.delete()
                await update.effective_chat.ban_member(
                    user_id=suspected_user.id,
                    revoke_messages=True
                )

            else:
                message = f"Поступила жалоба на пользователя {suspected_user.full_name}"

        logger.info(message)
        if message:
            logger.info(update.effective_message.reply_to_message)
            await update.effective_chat.send_message(
                message,
                parse_mode=ParseMode.HTML,
                message_thread_id=439,
                # message_thread_id=update.effective_message.reply_to_message.message_thread_id
            )
            

report_user_handler = CommandHandler(
    command=['report'],
    filters=filters.REPLY,
    callback=report_user,
)