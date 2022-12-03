from aiogram import types
import format


def dict_menu(command_dict, row_width=1):
    markup = types.ReplyKeyboardMarkup(row_width=row_width, resize_keyboard=True)
    markup.add(*list(command_dict.values()))
    return markup


def start():
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button = types.KeyboardButton(text="Старт")
    markup.add(button)
    return markup


def nothing():
    return types.ReplyKeyboardRemove()


def cancel():
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add("Отмена")
    return markup


def user_accept():
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add("Давай начнем!")
    return markup


def inline_convert(from_currency, from_type, from_country, from_bank,
                   to_currency, to_type, to_country, to_bank):
    callback_data_suffix = "#" + from_currency + "#" + from_type + "#" + from_country + "#" + from_bank + \
                           "#" + to_currency + "#" + to_type + "#" + to_country + "#" + to_bank
    from_union_type_text = format.CONVERT_CASH["cash"]
    if from_type != "cash":
        if from_country == "am":
            from_union_type_text = format.CONVERT_AM_BANKS[from_bank]
        else:
            from_union_type_text = format.CONVERT_RU_BANKS[from_bank]

    to_union_type_text = format.CONVERT_CASH["cash"]
    if to_type != "cash":
        if to_country == "am":
            to_union_type_text = format.CONVERT_AM_BANKS[to_bank]
        else:
            to_union_type_text = format.CONVERT_RU_BANKS[to_bank]

    buttons = [
        [
            types.InlineKeyboardButton(text="Из: " + format.ALL_CURRENCIES[from_currency],
                                       callback_data="from_currency" + callback_data_suffix),
            types.InlineKeyboardButton(text="Из: " + from_union_type_text,
                                       callback_data="from_union_type" + callback_data_suffix)
        ],
        [
            types.InlineKeyboardButton(text="В: " + format.ALL_CURRENCIES[to_currency],
                                       callback_data="to_currency" + callback_data_suffix),
            types.InlineKeyboardButton(text="В: " + to_union_type_text,
                                       callback_data="to_union_type" + callback_data_suffix)
        ],
        [types.InlineKeyboardButton(text="Получить конвертацию", callback_data="update" + callback_data_suffix)]
    ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return markup
