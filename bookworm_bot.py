from telegram.ext import (
    Application
)
from telegram import (
    Bot,
    Update,
    
)

import json
import logging
import os

from handlers.report_user_handler import report_user_handler
from handlers.start_handler import start_handler
from handlers.edit_text_handler import edit_text_handler
from handlers.new_user_handler import new_user_handler
from handlers.error_handler import error_handler


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
TG_TOKEN = os.environ.get("BOT_TOKEN")


async def handler(event, context) -> dict:
    application = (Application
                   .builder()
                   .token(TG_TOKEN)
                   .pool_timeout(100)
                   .connect_timeout(100)
                   .connection_pool_size(1000)
                   .build())
    
    application.add_handler(start_handler)
    application.add_handler(new_user_handler)
    application.add_handler(edit_text_handler)
    application.add_handler(report_user_handler)
    application.add_error_handler(error_handler)

    await application.initialize()

    logger.info("Application fetched user data")
    logger.info(application.user_data)

    if update_raw := event.get("body"):
        upd = Update.de_json(json.loads(update_raw), application.bot)
        logger.info(json.loads(update_raw))
        
        await application.process_update(upd)

    else:
        logger.error(event)
        return {'statusCode': 400, 'body': 'Something is wrong'}
    
    await application.shutdown()

    return {'statusCode': 200, 'body': 'Hello World!'}