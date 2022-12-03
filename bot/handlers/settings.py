from aiogram import types
from aiogram.dispatcher import FSMContext

import bot.common
from bot import user_state, bot_reply_markup
from bot.handlers.base import validate
from bot.commands import settings_dict, message_format_dict


async def handle_settings(message: types.Message, state: FSMContext):
    user = await validate(message, state)
    if user is None:
        return

    await state.set_state(user_state.InitialState.waiting_for_settings)
    msg = "Установи нужные параметры!"
    await bot.common.send_message(user.tg_id, msg, reply_markup=bot_reply_markup.dict_menu(settings_dict, 2))


async def handle_set_message_format(message: types.Message, state: FSMContext):
    user = await validate(message, state)
    if user is None:
        return

    msg = "Выбери формат сообщений для отображения. Мобильный или полноразмерный"
    await state.set_state(user_state.InitialState.waiting_for_set_message_format)
    await bot.common.send_message(user.tg_id, msg, reply_markup=bot_reply_markup.dict_menu(message_format_dict, 1))


async def handle_action_set_message_format(message: types.Message, state: FSMContext):
    user = await validate(message, state)
    if user is None:
        return

    if message.text in ("Мобильный", "Полноразмерный", "Назад"):
        if message.text == "Мобильный":
            user.update_user_info(message_format="short")
        elif message.text == "Полноразмерный":
            user.update_user_info(message_format="wide")
        await state.set_state(user_state.InitialState.waiting_for_settings)
        msg = "ОК!"
        await bot.common.send_message(user.tg_id, msg, reply_markup=bot_reply_markup.dict_menu(settings_dict, 2))
    else:
        await handle_set_message_format(message, state)
