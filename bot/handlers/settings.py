from aiogram import types
from aiogram.dispatcher import FSMContext
import re
import bot.common
import const
from bot import user_state, bot_reply_markup
from bot.handlers.base import validate

settings_dict = dict(
    banks='Список банков',
    # broker='Настройки биржи',
    message_format='Формат сообщения',
    cancel='Главное меню')
message_format_dict = dict(mobile='Мобильный', full='Полноразмерный', back='Назад')


async def handle_settings(message: types.Message, state: FSMContext):
    user = await validate(message, state)
    if user is None:
        return

    await state.set_state(user_state.InitialState.waiting_for_settings)
    msg = "Установи нужные параметры!"
    await bot.common.send_message(user.tg_id, msg, reply_markup=bot_reply_markup.dict_menu(settings_dict, 1))


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
        await bot.common.send_message(user.tg_id, msg, reply_markup=bot_reply_markup.dict_menu(settings_dict, 1))
    else:
        await handle_set_message_format(message, state)


def parse_banks_callback_suffix(callback_data):
    data_toggle = callback_data.split("#")
    include_banks = []
    for num in range(1, len(data_toggle)):
        if data_toggle[num] == "1":
            include_banks.append(const.SETTINGS_ALL_BANKS[num])
    return include_banks


async def handle_set_banks(message: types.Message, state: FSMContext):
    user = await validate(message, state)
    if user is None:
        return

    msg = "Выбери банки, карты которых у тебя есть"
    await bot.common.send_message(user.tg_id, msg, reply_markup=bot_reply_markup.inline_banks(user.include_banks))


async def callback_update_bank_button(callback: types.CallbackQuery):
    user = await validate(callback=callback)
    if user is None:
        return

    include_banks = parse_banks_callback_suffix(callback.data)
    bank = callback.data.split("#")[0].split("_")[1]
    if bank in include_banks:
        include_banks.remove(bank)
    else:
        include_banks.append(bank)

    await callback.message.edit_text(
        callback.message.text,
        reply_markup=bot_reply_markup.inline_banks(include_banks))
    await callback.answer()


async def callback_update_include_banks(callback: types.CallbackQuery):
    user = await validate(callback=callback)
    if user is None:
        return

    include_banks = parse_banks_callback_suffix(callback.data)
    user.update_user_info(include_banks=include_banks)
    await callback.message.edit_text(
        "Информация о банках обновлена",
        reply_markup=None)
    await callback.answer()
