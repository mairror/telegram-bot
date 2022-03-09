import json
import traceback

import requests
from config.settings import SLACK_WEBHOOK_URI
from telegram import Update
from telegram.ext import CallbackContext
from utils.logging import telegram_bot


def error_handler(update: object, context: CallbackContext) -> None:
    """
    Name: error_handler
    Description:
        Manage any error from the dispatcher logging it and send it to the developer chat id.
    Inputs:
        :update: type(Update): update handler object.
        :context: type(CallbackContext).
    Outputs:
        None
    """
    telegram_bot.error(
        msg="Exception while handling an update:", exc_info=context.error
    )

    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb_string = "".join(tb_list)

    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = f"""
<!here>
An exception was raised while handling an update:\n
*UPDATE JSON DATA*
```
{json.dumps(update_str, indent=2, ensure_ascii=False)}
```
*TRACEBACK*
```
{tb_string}
```
"""

    data = {
        "blocks": [{"type": "section", "text": {"type": "mrkdwn", "text": message}}]
    }

    headers = {"Content-type": "application/json"}

    requests.post(SLACK_WEBHOOK_URI, data=json.dumps(data), headers=headers)
