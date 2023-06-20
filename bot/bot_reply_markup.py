from aiogram import types
import const


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


def back():
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add("Назад")
    return markup


def user_accept():
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add("Давай начнем!")
    return markup


def inline_convert(from_currency, from_type, from_country, from_bank,
                   to_currency, to_type, to_country, to_bank, online_only, broker, result_num=0, instant_num=0):
    online_str = str(int(online_only))
    broker_str = str(int(broker))
    callback_data_suffix = "#" + from_currency + "#" + from_type + "#" + from_country + \
                           "#" + const.ALL_BANKS_NAME_TO_ID[from_bank] + \
                           "#" + to_currency + "#" + to_type + "#" + to_country + \
                           "#" + const.ALL_BANKS_NAME_TO_ID[to_bank] + \
                           "#" + online_str + "#" + broker_str + "#" + str(result_num) + "#" + str(instant_num)
    from_union_type_text = const.CONVERT_CASH["cash"]
    if from_type != "cash":
        if from_country == "am":
            from_union_type_text = const.CONVERT_AM_BANKS[from_bank]
        else:
            from_union_type_text = const.CONVERT_RU_BANKS[from_bank]

    if to_type == "cash":
        to_union_type_text = const.CONVERT_CASH["cash"]
    elif to_type == "pos":
        to_union_type_text = const.CONVERT_POS["pos"]
    else:
        if to_country == "am":
            to_union_type_text = const.CONVERT_AM_BANKS[to_bank]
        else:
            to_union_type_text = const.CONVERT_RU_BANKS[to_bank]

    if online_only:
        online_suffix = " ✅"
    else:
        online_suffix = " ❌"

    if broker:
        broker_suffix = " ✅"
    else:
        broker_suffix = " ❌"

    if instant_num == 1:
        instant_suffix = " ✅"
    else:
        instant_suffix = " ❌"

    buttons = [
        [
            types.InlineKeyboardButton(text="Из: " + const.ALL_CURRENCIES[from_currency],
                                       callback_data="c_from_curr" + callback_data_suffix),
            types.InlineKeyboardButton(text="Из: " + from_union_type_text,
                                       callback_data="c_from_union_t" + callback_data_suffix)
        ],
        [
            types.InlineKeyboardButton(text="В: " + const.ALL_CURRENCIES[to_currency],
                                       callback_data="c_to_curr" + callback_data_suffix),
            types.InlineKeyboardButton(text="В: " + to_union_type_text,
                                       callback_data="c_to_union_t" + callback_data_suffix)
        ],
        [
            types.InlineKeyboardButton(text="Только онлайн" + online_suffix,
                                       callback_data="c_online" + callback_data_suffix),
            types.InlineKeyboardButton(text="Быстро" + instant_suffix,
                                       callback_data="c_instant" + callback_data_suffix)],
        [types.InlineKeyboardButton(text="Биржа" + broker_suffix,
                                       callback_data="c_broker" + callback_data_suffix)],
        [types.InlineKeyboardButton(text="Лучшая конвертация", callback_data="c_update" + callback_data_suffix)],
        [types.InlineKeyboardButton(text="<-", callback_data="c_prev" + callback_data_suffix),
         types.InlineKeyboardButton(text="->", callback_data="c_next" + callback_data_suffix)]
    ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return markup


def create_banks_callback_suffix(include_banks):
    suffix = ""
    for num in range(1, len(const.SETTINGS_ALL_BANKS)):
        if const.SETTINGS_ALL_BANKS[num] not in include_banks:
            suffix += "#0"
        else:
            suffix += "#1"
    return suffix


def inline_banks(include_banks):
    callback_data_suffix = create_banks_callback_suffix(include_banks)
    buttons = []
    for num in range(1, len(const.SETTINGS_ALL_BANKS)):
        bank_key = const.SETTINGS_ALL_BANKS[num]
        bank = const.ALL_BANKS[bank_key]
        if bank_key not in include_banks:
            bank += " ❌"
        else:
            bank += " ✅"
        if bank_key in const.LIST_RU_BANKS:
            bank = "Россия: " + bank
        elif bank_key in const.LIST_AM_BANKS:
            bank = "Армения: " + bank
        elif bank_key in const.LIST_RS_BANKS:
            bank = "Сербия: " + bank
        buttons.append([types.InlineKeyboardButton(text=bank,
                                                   callback_data="bb_" + bank_key + callback_data_suffix)])
    buttons.append([types.InlineKeyboardButton(text="Обновить информацию",
                                               callback_data="ub_" + callback_data_suffix)])
    markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return markup
