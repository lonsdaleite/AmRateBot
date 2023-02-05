from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified

import bot.common
import const
from bot import bot_reply_markup
from bot.handlers.base import validate, main_command_dict
from format import format_rates
from rate import get_best_convert, create_rate


async def handle_convert(message: types.Message, state: FSMContext):
    user = await validate(message, state)
    if user is None:
        return

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
                           allow_uncertainty=user.uncertainty,
                           result_format=user.message_format,
                           exclude_methods=user.exclude_methods + ["broker"],
                           exclude_banks=user.exclude_banks,
                           print_=False)
    await bot.common.send_message(message.from_user.id, f"<pre>{msg}</pre>",
                                  parse_mode=types.ParseMode.HTML,
                                  reply_markup=bot_reply_markup.inline_convert(
                                      from_currency, from_type, from_country, from_bank,
                                      to_currency, to_type, to_country, to_bank, False, False))

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
    online_only = bool(int(data.split("#")[9]))
    broker = bool(int(data.split("#")[10]))
    return from_currency, from_type, from_country, from_bank, to_currency, to_type, to_country, to_bank, online_only, broker


async def update_message(message, text,
                         from_currency, from_type, from_country, from_bank,
                         to_currency, to_type, to_country, to_bank, online_only, broker):
    try:
        await message.edit_text(
            f"<pre>{text}</pre>",
            parse_mode=types.ParseMode.HTML,
            reply_markup=bot_reply_markup.inline_convert(
                from_currency, from_type, from_country, from_bank,
                to_currency, to_type, to_country, to_bank,
                online_only, broker))
    except MessageNotModified:
        pass
        # log.logger.trace("Message not modified")

    # log.logger.debug(from_currency + " " + from_type + " " + from_country + " " + from_bank + " " +
    #                  to_currency + " " + to_type + " " + to_country + " " + to_bank)


async def callback_update_convert(callback: types.CallbackQuery):
    user = bot.common.get_user(tg_id=callback.from_user.id)

    from_currency, from_type, from_country, from_bank, to_currency, to_type, to_country, to_bank, online_only, broker = \
        parse_callback_data(callback.data)

    # callback_data_suffix = "#" + from_currency + "#" + from_type + "#" + from_country + "#" + from_bank + \
    #                        "#" + to_currency + "#" + to_type + "#" + to_bank + "#" + to_bank
    # log.logger.debug(callback_data_suffix)

    extra_exclude_methods = []
    if online_only:
        extra_exclude_methods += ["atm", "bank"]
    if not broker:
        extra_exclude_methods += ["broker"]
    prev_msg = callback.message.text
    msg = get_best_convert(bot.common.all_rates,
                           from_currency, from_type, from_country, from_bank,
                           to_currency, to_type, to_country, to_bank,
                           allow_uncertainty=user.uncertainty,
                           result_format=user.message_format,
                           exclude_methods=user.exclude_methods + extra_exclude_methods,
                           exclude_banks=user.exclude_banks,
                           print_=False)

    # log.logger.debug(msg)
    if msg == "" or msg is None:
        total = create_rate(from_currency, from_type, from_country, from_bank,
                            to_currency, to_type, to_country, to_bank,
                            "total", 0, "from")
        msg = format_rates([total], result_format=user.message_format, print_=False)

    if prev_msg != msg:
        await update_message(callback.message, msg,
                             from_currency, from_type, from_country, from_bank,
                             to_currency, to_type, to_country, to_bank, online_only, broker)

    await callback.answer()
    # log.logger.debug("Convert updated")


def next_currency(currency):
    new_currency = currency
    for num, curr in enumerate(const.LIST_CURRENCIES):
        if currency == curr:
            if num == len(const.LIST_CURRENCIES) - 1:
                new_currency = const.LIST_CURRENCIES[0]
            else:
                new_currency = const.LIST_CURRENCIES[num + 1]
            break
    return new_currency


async def callback_update_from_currency(callback: types.CallbackQuery):
    from_currency, from_type, from_country, from_bank, to_currency, to_type, to_country, to_bank, online_only, broker = \
        parse_callback_data(callback.data)

    from_currency = next_currency(from_currency)

    msg = callback.message.text
    await update_message(callback.message, msg,
                         from_currency, from_type, from_country, from_bank,
                         to_currency, to_type, to_country, to_bank, online_only, broker)

    await callback.answer()


async def callback_update_to_currency(callback: types.CallbackQuery):
    from_currency, from_type, from_country, from_bank, to_currency, to_type, to_country, to_bank, online_only, broker = \
        parse_callback_data(callback.data)

    to_currency = next_currency(to_currency)

    msg = callback.message.text
    await update_message(callback.message, msg,
                         from_currency, from_type, from_country, from_bank,
                         to_currency, to_type, to_country, to_bank, online_only, broker)

    await callback.answer()


def next_union_type(country, type_, bank, online_only, user):
    list_ru_banks_exclude = [x for x in const.LIST_RU_BANKS if x not in user.exclude_banks]
    list_am_banks_exclude = [x for x in const.LIST_AM_BANKS if x not in user.exclude_banks]

    new_type = type_
    new_bank = bank
    new_country = country
    if type_ == "cash":
        new_type = "bank"
        new_bank = list_ru_banks_exclude[0]
        new_country = "ru"
    elif country == "ru":
        for num, bank_tmp in enumerate(list_ru_banks_exclude):
            if bank == bank_tmp:
                if num == len(list_ru_banks_exclude) - 1:
                    new_bank = list_am_banks_exclude[0]
                    new_country = "am"
                else:
                    new_bank = list_ru_banks_exclude[num + 1]
                break
    else:
        for num, bank_tmp in enumerate(list_am_banks_exclude):
            if bank == bank_tmp:
                if num == len(list_am_banks_exclude) - 1:
                    if online_only:
                        new_type = "bank"
                        new_bank = list_ru_banks_exclude[0]
                        new_country = "ru"
                    else:
                        new_bank = ""
                        new_type = "cash"
                        new_country = "am"
                else:
                    new_bank = list_am_banks_exclude[num + 1]
                break
    return new_country, new_type, new_bank


async def callback_update_from_union_type(callback: types.CallbackQuery):
    user = bot.common.get_user(tg_id=callback.from_user.id)
    from_currency, from_type, from_country, from_bank, to_currency, to_type, to_country, to_bank, online_only, broker = \
        parse_callback_data(callback.data)

    from_country, from_type, from_bank = next_union_type(from_country, from_type, from_bank, online_only, user)

    msg = callback.message.text
    await update_message(callback.message, msg,
                         from_currency, from_type, from_country, from_bank,
                         to_currency, to_type, to_country, to_bank, online_only, broker)

    await callback.answer()


async def callback_update_to_union_type(callback: types.CallbackQuery):
    user = bot.common.get_user(tg_id=callback.from_user.id)
    from_currency, from_type, from_country, from_bank, to_currency, to_type, to_country, to_bank, online_only, broker = \
        parse_callback_data(callback.data)

    to_country, to_type, to_bank = next_union_type(to_country, to_type, to_bank, online_only, user)

    msg = callback.message.text
    await update_message(callback.message, msg,
                         from_currency, from_type, from_country, from_bank,
                         to_currency, to_type, to_country, to_bank, online_only, broker)

    await callback.answer()


async def callback_update_online_only(callback: types.CallbackQuery):
    user = bot.common.get_user(tg_id=callback.from_user.id)
    from_currency, from_type, from_country, from_bank, to_currency, to_type, to_country, to_bank, online_only, broker = \
        parse_callback_data(callback.data)

    if online_only:
        online_only = False
    else:
        online_only = True
        if from_type == "cash":
            from_country, from_type, from_bank = next_union_type(from_country, from_type, from_bank, online_only, user)
        if to_type == "cash":
            to_country, to_type, to_bank = next_union_type(to_country, to_type, to_bank, online_only, user)

    msg = callback.message.text
    await update_message(callback.message, msg,
                         from_currency, from_type, from_country, from_bank,
                         to_currency, to_type, to_country, to_bank, online_only, broker)

    await callback.answer()


async def callback_update_broker(callback: types.CallbackQuery):
    from_currency, from_type, from_country, from_bank, to_currency, to_type, to_country, to_bank, online_only, broker = \
        parse_callback_data(callback.data)

    if broker:
        broker = False
    else:
        broker = True

    msg = callback.message.text
    await update_message(callback.message, msg,
                         from_currency, from_type, from_country, from_bank,
                         to_currency, to_type, to_country, to_bank, online_only, broker)

    await callback.answer()


async def handle_convert_all(message: types.Message, state: FSMContext):
    user = await validate(message, state)
    if user is None:
        return

    converts = [["rur", "cash", "am", "", "eur", "cash", "am", "", []],
                ["rur", "bank", "ru", "tinkoff", "eur", "cash", "am", "", []],
                ["rur", "bank", "ru", "tinkoff", "eur", "bank", "am", "yunibank", []],
                ["rur", "cash", "am", "", "usd", "cash", "am", "", []],
                ["rur", "bank", "ru", "tinkoff", "usd", "cash", "am", "", []],
                ["rur", "bank", "ru", "tinkoff", "usd", "bank", "am", "yunibank", []],
                ["rur", "cash", "am", "", "amd", "cash", "am", "", []],
                ["rur", "bank", "ru", "tinkoff", "amd", "cash", "am", "", []],
                ["rur", "bank", "ru", "tinkoff", "amd", "bank", "am", "yunibank", []],
                ["rur", "bank", "ru", "tinkoff", "amd", "cash", "am", "", ["broker"]]]

    for conv in converts:
        msg = get_best_convert(bot.common.all_rates,
                               conv[0], conv[1], conv[2], conv[3], conv[4], conv[5], conv[6], conv[7],
                               allow_uncertainty=user.uncertainty, result_format=user.message_format, print_=False,
                               exclude_methods=conv[8] + user.exclude_methods, exclude_banks=user.exclude_banks)
        await bot.common.send_message(message.from_user.id, f"<pre>{msg}</pre>",
                                      parse_mode=types.ParseMode.HTML,
                                      reply_markup=bot_reply_markup.dict_menu(main_command_dict))
