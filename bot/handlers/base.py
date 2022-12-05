from aiogram import types
from aiogram.dispatcher import FSMContext

import bot.common
import bot.user_state
from bot import bot_reply_markup
from bot.db import dml_actions

main_command_dict = dict(
    convert='Новая конвертация',
    settings='Настройки',
    help='Информация')


async def handle_start(message: types.Message, state: FSMContext):
    await state.finish()
    await handle_welcome(message, state)


async def handle_welcome(message: types.Message, state: FSMContext):
    user = await validate(message, state)
    if user is None:
        return

    msg = "Привет!\n" \
          + "Я бот, который подскажет лучшие способы обмена валюты в Армении!\n" \
          + "Вот список команд, которые я понимаю:\n"
    for k, v in main_command_dict.items():
        msg += "/{} : {}\n".format(k, v)
    msg += "А также ты можешь воспользоваться кнопками ниже ⬇️"
    await bot.common.send_message(message.from_user.id, msg, reply_markup=bot_reply_markup.dict_menu(main_command_dict))


async def handle_help(message: types.Message, state: FSMContext):
    user = await validate(message, state)
    if user is None:
        return

    msg = "Привет!\n" \
          "Я бот, который подскажет лучшие способы обмена валюты в Армении!\n\n" \
          "Курсы обновляются раз в 20 минут и берутся со следующих сайтов:\n" \
          "Все банки Армении и IDPay: https://rate.am/en/:\n" \
          "SAS: https://www.sas.am/en/appfood/personal/calculator/\n" \
          "Unistream: https://online.unistream.ru/\n" \
          "Tinkoff Инвестиции: https://www.tinkoff.ru/invest/currencies/\n" \
          "В случае проблем с отдельным сайтами, " \
          "некоторые курсы могут обновляться с дополнительной задержкой.\n\n" \
          "В настройках можно выбрать банки РФ и РА, включить поддержку покупки валюты на бирже, " \
          "установить установить допустимую погрешность в расчетах, а также изменить формат отображаемых " \
          "конвертаций."

    await bot.common.send_message(message.from_user.id, msg,
                                  reply_markup=bot_reply_markup.dict_menu(main_command_dict))


# Main message preparation and validation
# All the handlers call it first
# If user accepted the conversation, returns a User object
# Else returns None
async def validate(message: types.Message, state):
    user = bot.common.get_user(message=message)
    await bot.common.print_log(user, message, state)

    if user is None:
        await request_user_accept(message, state)
        return None

    # current_state = await state.get_state()
    #
    # if not user.check() and current_state is None:
    #     await request_settings(message, state)
    #     return None

    return user


async def request_user_accept(message: types.Message, state):
    tg_id = message.from_user.id

    msg = "Привет! Я бот, который помогает получить лучшие курсы конвертации валют в Армении!\n" \
          "Нажимай на кнопку 'Давай начнем!'"
    await bot.common.send_message(tg_id, msg, reply_markup=bot_reply_markup.user_accept())
    await state.set_state(bot.user_state.InitialState.waiting_for_accept)


async def handle_action_user_accept(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id

    if message.text == "Давай начнем!":
        user = bot.common.get_user(message=message)
        if user is None:
            dml_actions.add_user(tg_id=tg_id)
            bot.common.get_user(message=message)
        else:
            user.update_user_info(user.user_id, tg_id=tg_id)

        await state.finish()

        user = await validate(message, state)
        if user is not None:
            await handle_welcome(message, state)


async def handle_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    user = await validate(message, state)
    if user is None:
        return

    await bot.common.send_message(user.tg_id, "Перехожу в главное меню",
                                  reply_markup=bot_reply_markup.dict_menu(main_command_dict))
