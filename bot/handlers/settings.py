from aiogram import types
from aiogram.dispatcher import FSMContext
import re
import bot.common
from bot import user_state, bot_reply_markup
from bot.handlers.base import validate

settings_dict = dict(
    # exclude_banks='Исключить банки',
    # exclude_methods='Исключить методы конвертации',
    message_format='Формат сообщения',
    uncertainty='Погрешность',
    cancel='Главное меню')
message_format_dict = dict(mobile='Мобильный', full='Полноразмерный', back='Назад')


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


async def handle_set_uncertainty(message: types.Message, state: FSMContext):
    user = await validate(message, state)
    if user is None:
        return

    msg = "Введите допустимую погрешность при поиске оптимальной конвертации. " \
          "Это нужно, чтобы искать более простые пути конвертации при минимальной разнице в курсе.\n" \
          "Формат xx.xx%. Например, 0.5%\n" \
          "Текущая погрешность: " + str(user.uncertainty * 100) + "%"
    await state.set_state(user_state.InitialState.waiting_for_set_uncertainty)
    await bot.common.send_message(user.tg_id, msg, reply_markup=bot_reply_markup.back())


async def handle_action_set_uncertainty(message: types.Message, state: FSMContext):
    user = await validate(message, state)
    if user is None:
        return

    text = message.text
    if text == "Назад":
        msg = "ОК"
        await state.set_state(user_state.InitialState.waiting_for_settings)
        await bot.common.send_message(user.tg_id, msg, reply_markup=bot_reply_markup.dict_menu(settings_dict, 2))
    elif re.match("^[0-9]+%$", text) or re.match("^[0-9]+\\.[0-9]+%$", text):
        user.uncertainty = float(text[:-1]) / 100
        msg = "Погрешность " + text + " установлена!"
        await state.set_state(user_state.InitialState.waiting_for_settings)
        await bot.common.send_message(user.tg_id, msg, reply_markup=bot_reply_markup.dict_menu(settings_dict, 2))
    else:
        msg = "Некорректный формат"
        await bot.common.send_message(user.tg_id, msg)
