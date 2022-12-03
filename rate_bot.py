import re
from aiogram.utils.exceptions import MessageNotModified
from aiogram import executor, types
from aiogram.dispatcher import FSMContext
import bot.common
import format
import log
from bot import bot_reply_markup, update_rates, user_state
from bot.db import dml_actions, sql_init
from add_rates import add_all_rates
from rate import get_best_convert

main_command_dict = dict(
    convert='Новая конвертация',
    settings='Настройки',
    help='Помощь с командами')

settings_dict = dict(exclude_banks='Исключить банки',
                     exclude_methods='Исключить методы конвертации',
                     message_format='Формат сообщения',
                     cancel='Главное меню')

message_format_dict = dict(mobile='Мобильный', full='Полноразмерный', cancel='Назад')


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

    msg = "Привет! Я бот, который помогает получить лучшие курсы конвертации валют в Армении! Начнем?"
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


async def handle_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    user = await validate(message, state)
    if user is None:
        return

    response_dict = main_command_dict
    await bot.common.send_message(user.tg_id, "Перехожу в главное меню",
                                  reply_markup=bot_reply_markup.dict_menu(response_dict))


async def handle_rate(message: types.Message, state: FSMContext):
    user = await validate(message, state)
    if user is None:
        return
    for rate in bot.common.all_rates:
        await bot.common.send_message(message.from_user.id, rate,
                                      reply_markup=bot_reply_markup.dict_menu(main_command_dict))


async def handle_convert(message: types.Message, state: FSMContext):
    user = await validate(message, state)
    if user is None:
        return

    uncertainty = 0.000

    from_currency = "rur"
    from_type = "cash"
    from_country = "am"
    from_bank = ""
    to_currency = "amd"
    to_type = "cash"
    to_country = "am"
    to_bank = ""
    msg = get_best_convert(bot.common.all_rates,
                           from_currency, from_type, from_country, from_bank,
                           to_currency, to_type, to_country, to_bank,
                           allow_uncertainty=uncertainty,
                           result_format=user.message_format,
                           exclude_methods=user.exclude_methods,
                           exclude_banks=user.exclude_banks,
                           print_=False)
    await bot.common.send_message(message.from_user.id, f"<pre>{msg}</pre>",
                                  parse_mode=types.ParseMode.HTML,
                                  reply_markup=bot_reply_markup.inline_convert(
                                      from_currency, from_type, from_country, from_bank,
                                      to_currency, to_type, to_country, to_bank))

    await bot.common.send_message(message.from_user.id,
                                  "Нажимайте на кнопки под сообщением, чтобы изменить параметры конвертации")


def parse_callback_data(data):
    from_currency = data.split("#")[1]
    from_type = data.split("#")[2]
    from_country = data.split("#")[3]
    from_bank = data.split("#")[4]
    to_currency = data.split("#")[5]
    to_type = data.split("#")[6]
    to_country = data.split("#")[7]
    to_bank = data.split("#")[8]
    return from_currency, from_type, from_country, from_bank, to_currency, to_type, to_country, to_bank


async def update_message(message, text,
                         from_currency, from_type, from_country, from_bank,
                         to_currency, to_type, to_country, to_bank):
    try:
        await message.edit_text(
            f"<pre>{text}</pre>",
            parse_mode=types.ParseMode.HTML,
            reply_markup=bot_reply_markup.inline_convert(
                from_currency, from_type, from_country, from_bank,
                to_currency, to_type, to_country, to_bank))
    except MessageNotModified:
        log.logger.debug("Message not modified")

    log.logger.debug(from_currency + " " + from_type + " " + from_country + " " + from_bank + " " +
                     to_currency + " " + to_type + " " + to_country + " " + to_bank)


async def callback_update_convert(callback: types.CallbackQuery):
    user = bot.common.get_user(tg_id=callback.from_user.id)

    uncertainty = 0.000

    from_currency, from_type, from_country, from_bank, to_currency, to_type, to_country, to_bank = \
        parse_callback_data(callback.data)

    # callback_data_suffix = "#" + from_currency + "#" + from_type + "#" + from_country + "#" + from_bank + \
    #                        "#" + to_currency + "#" + to_type + "#" + to_bank + "#" + to_bank
    # log.logger.debug(callback_data_suffix)

    msg = get_best_convert(bot.common.all_rates,
                           from_currency, from_type, from_country, from_bank,
                           to_currency, to_type, to_country, to_bank,
                           allow_uncertainty=uncertainty,
                           result_format=user.message_format,
                           exclude_methods=user.exclude_methods,
                           exclude_banks=user.exclude_banks,
                           print_=False)

    # log.logger.debug(msg)

    await update_message(callback.message, msg,
                         from_currency, from_type, from_country, from_bank,
                         to_currency, to_type, to_country, to_bank)

    log.logger.debug("Convert updated")


async def callback_update_from_currency(callback: types.CallbackQuery):
    from_currency, from_type, from_country, from_bank, to_currency, to_type, to_country, to_bank = \
        parse_callback_data(callback.data)

    for num, curr in enumerate(format.LIST_CURRENCIES):
        if from_currency == curr:
            if num == len(format.LIST_CURRENCIES) - 1:
                from_currency = format.LIST_CURRENCIES[0]
            else:
                from_currency = format.LIST_CURRENCIES[num + 1]
            break

    msg = callback.message.text
    await update_message(callback.message, msg,
                         from_currency, from_type, from_country, from_bank,
                         to_currency, to_type, to_country, to_bank)


async def callback_update_to_currency(callback: types.CallbackQuery):
    from_currency, from_type, from_country, from_bank, to_currency, to_type, to_country, to_bank = \
        parse_callback_data(callback.data)

    for num, curr in enumerate(format.LIST_CURRENCIES):
        if to_currency == curr:
            if num == len(format.LIST_CURRENCIES) - 1:
                to_currency = format.LIST_CURRENCIES[0]
            else:
                to_currency = format.LIST_CURRENCIES[num + 1]
            break

    msg = callback.message.text
    await update_message(callback.message, msg,
                         from_currency, from_type, from_country, from_bank,
                         to_currency, to_type, to_country, to_bank)


async def callback_update_from_union_type(callback: types.CallbackQuery):
    from_currency, from_type, from_country, from_bank, to_currency, to_type, to_country, to_bank = \
        parse_callback_data(callback.data)

    if from_type == "cash":
        from_type = "bank"
        from_bank = format.LIST_RU_BANKS[0]
        from_country = "ru"
    elif from_country == "ru":
        for num, bank in enumerate(format.LIST_RU_BANKS):
            if from_bank == bank:
                if num == len(format.LIST_RU_BANKS) - 1:
                    from_bank = format.LIST_AM_BANKS[0]
                    from_country = "am"
                else:
                    from_bank = format.LIST_RU_BANKS[num + 1]
                break
    else:
        for num, bank in enumerate(format.LIST_AM_BANKS):
            if from_bank == bank:
                if num == len(format.LIST_AM_BANKS) - 1:
                    from_bank = ""
                    from_type = "cash"
                    from_country = "am"
                else:
                    from_bank = format.LIST_AM_BANKS[num + 1]
                break

    msg = callback.message.text
    await update_message(callback.message, msg,
                         from_currency, from_type, from_country, from_bank,
                         to_currency, to_type, to_country, to_bank)


async def callback_update_to_union_type(callback: types.CallbackQuery):
    from_currency, from_type, from_country, from_bank, to_currency, to_type, to_country, to_bank = \
        parse_callback_data(callback.data)

    if to_type == "cash":
        to_type = "bank"
        to_bank = format.LIST_RU_BANKS[0]
        to_country = "ru"
    elif to_country == "ru":
        for num, bank in enumerate(format.LIST_RU_BANKS):
            if to_bank == bank:
                if num == len(format.LIST_RU_BANKS) - 1:
                    to_bank = format.LIST_AM_BANKS[0]
                    to_country = "am"
                else:
                    to_bank = format.LIST_RU_BANKS[num + 1]
                break
    else:
        for num, bank in enumerate(format.LIST_AM_BANKS):
            if to_bank == bank:
                if num == len(format.LIST_AM_BANKS) - 1:
                    to_bank = ""
                    to_type = "cash"
                    to_country = "am"
                else:
                    to_bank = format.LIST_AM_BANKS[num + 1]
                break

    msg = callback.message.text
    await update_message(callback.message, msg,
                         from_currency, from_type, from_country, from_bank,
                         to_currency, to_type, to_country, to_bank)


async def handle_convert_all(message: types.Message, state: FSMContext):
    user = await validate(message, state)
    if user is None:
        return

    uncertainty = 0.003

    converts = [["rur", "cash", "am", "", "eur", "cash", "am", "", None],
                ["rur", "bank", "ru", "tinkoff", "eur", "cash", "am", "", None],
                ["rur", "bank", "ru", "tinkoff", "eur", "bank", "am", "yunibank", None],
                ["rur", "cash", "am", "", "usd", "cash", "am", "", None],
                ["rur", "bank", "ru", "tinkoff", "usd", "cash", "am", "", None],
                ["rur", "bank", "ru", "tinkoff", "usd", "bank", "am", "yunibank", None],
                ["rur", "cash", "am", "", "amd", "cash", "am", "", None],
                ["rur", "bank", "ru", "tinkoff", "amd", "cash", "am", "", None],
                ["rur", "bank", "ru", "tinkoff", "amd", "bank", "am", "yunibank", None],
                ["rur", "bank", "ru", "tinkoff", "amd", "cash", "am", "", ["broker"]]]

    for conv in converts:
        msg = get_best_convert(bot.common.all_rates,
                               conv[0], conv[1], conv[2], conv[3], conv[4], conv[5], conv[6], conv[7],
                               allow_uncertainty=uncertainty, result_format=user.message_format, print_=False,
                               exclude_methods=conv[8])
        await bot.common.send_message(message.from_user.id, f"<pre>{msg}</pre>",
                                      parse_mode=types.ParseMode.HTML,
                                      reply_markup=bot_reply_markup.dict_menu(main_command_dict))


def register_handlers_main():
    add_all_rates(bot.common.all_rates)
    bot.common.dp.register_message_handler(handle_start, commands=['start', 'help'], state='*')
    bot.common.dp.register_message_handler(handle_cancel,
                                           text=['/cancel', 'Отмена', 'Главное меню'],
                                           state='*')
    bot.common.dp.register_message_handler(handle_action_user_accept, state=user_state.InitialState.waiting_for_accept)
    bot.common.dp.register_message_handler(handle_set_message_format, text=['/message_format',
                                                                            settings_dict['message_format']],
                                           state=[user_state.InitialState.waiting_for_settings])
    bot.common.dp.register_message_handler(handle_action_set_message_format,
                                           state=[user_state.InitialState.waiting_for_set_message_format])
    bot.common.dp.register_message_handler(handle_settings, text=['/settings', main_command_dict['settings']])
    # bot.common.dp.register_message_handler(handle_rate, text=['/rate', main_command_dict['rate']])
    bot.common.dp.register_message_handler(handle_convert_all, text=['/convert_all'])  # Hidden method
    bot.common.dp.register_message_handler(handle_convert, text=['/convert', main_command_dict['convert']])
    bot.common.dp.register_message_handler(handle_welcome)

    bot.common.dp.register_callback_query_handler(callback_update_convert, regexp=re.compile(r"update.*"))
    bot.common.dp.register_callback_query_handler(callback_update_from_currency,
                                                  regexp=re.compile(r"from_currency.*"))
    bot.common.dp.register_callback_query_handler(callback_update_to_currency,
                                                  regexp=re.compile(r"to_currency.*"))
    bot.common.dp.register_callback_query_handler(callback_update_from_union_type,
                                                  regexp=re.compile(r"from_union_type.*"))
    bot.common.dp.register_callback_query_handler(callback_update_to_union_type,
                                                  regexp=re.compile(r"to_union_type.*"))


sql_init.run_scripts()

register_handlers_main()
executor.start_polling(bot.common.dp, skip_updates=False, on_startup=update_rates.run)
