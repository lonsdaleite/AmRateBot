import traceback
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import BotBlocked
import bot.config as bot_config
import log
# from db import dml_actions

# user_dict = {}

# Bot initialization
bot = Bot(token=bot_config.BOT_TG_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
all_rates = []


async def print_log(user, message, state, command_dict=None):
    tg_id = message.from_user.id
    text = "No text"
    if message.text is not None:
        text = message.text
    elif message.caption is not None:
        text = message.caption

    user_state = str(await state.get_state())

    if user is None:
        log.logger.info("Unknown user found:\nID: " + str(tg_id))
        if message.from_user.username is not None:
            log.logger.info("UserName: " + message.from_user.username)
        return
    elif command_dict is not None and text[1:] in command_dict or text == '/start':
        log.logger.info("ID: " + str(tg_id) + ", state: " + user_state + ", message: " + text)
    elif command_dict is not None and text in list(command_dict.values()):
        log.logger.info("ID: " + str(tg_id) + ", state: " + user_state + ", message: " + text)
    else:
        log.logger.info("ID: " + str(tg_id) + ", state: " + user_state + ", message: text")

    log.logger.debug("ID: " + str(tg_id) + ", state: " + user_state + ", message: " + text)


async def send_message(tg_id, text, reply_markup=None):
    # log.logger.debug("tg_id: " + str(tg_id), ", message:\n" + text)
    try:
        if bot_config.DEBUG_TG_ID is not None:
            await bot.send_message(bot_config.DEBUG_TG_ID, "Message to " + str(tg_id) + "\n" + text,
                                   reply_markup=reply_markup)
        else:
            await bot.send_message(tg_id, text, reply_markup=reply_markup)
    except BotBlocked:
        log.logger.warn("Bot blocked for user: " + str(tg_id))
    except:
        log.logger.debug("Can not send a message to: " + str(tg_id))
        traceback.print_exc() 
