import traceback
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import BotBlocked
import bot.config as bot_config
import log
import bot.user as us

user_dict = {}

# Bot initialization
bot = Bot(token=bot_config.BOT_TG_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
all_rates = []


async def print_log(user, message, state, callback: types.CallbackQuery = None, command_dict=None):
    tg_id = message.from_user.id
    text = "No text"
    if callback is not None:
        text = callback.data
    elif message.text is not None:
        text = message.text
    elif message.caption is not None:
        text = message.caption

    user_state = ""
    if state is not None:
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


async def send_message(tg_id, text, parse_mode=None, reply_markup=None, disable_web_page_preview=True):
    # log.logger.debug("tg_id: " + str(tg_id), ", message:\n" + text)
    try:
        if bot_config.DEBUG_TG_ID is not None:
            await bot.send_message(bot_config.DEBUG_TG_ID, "Message to " + str(tg_id) + "\n" + text,
                                   parse_mode=parse_mode,
                                   reply_markup=reply_markup,
                                   disable_web_page_preview=disable_web_page_preview)
        else:
            await bot.send_message(tg_id, text, parse_mode=parse_mode, reply_markup=reply_markup,
                                   disable_web_page_preview=disable_web_page_preview)
    except BotBlocked:
        log.logger.warn("Bot blocked for user: " + str(tg_id))
    except:
        log.logger.debug("Can not send a message to: " + str(tg_id))
        traceback.print_exc()


def get_user(message=None, tg_id=None, user_id=None):
    if message is None and tg_id is None and user_id is None:
        return None

    if message is not None:
        tg_id = message.from_user.id

    user = None

    if tg_id is not None and tg_id in user_dict:
        user = user_dict[tg_id]
        if not user.check():
            user.refresh()
    elif tg_id is None:
        for tg_id_tmp, user_tmp in user_dict.items():
            if user_id is not None and user_tmp.user_id == user_id:
                user = user_tmp
                if not user.check():
                    user.refresh()
                    break

    if user is None:
        # If tg_id not in dict, create User instance
        user = us.User(user_id, tg_id)
        if user.user_id is None:
            return None
        user_dict[tg_id] = user

    return user
