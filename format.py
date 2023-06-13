import prettytable as pt
from prettytable import ALL
from const import ALL_CURRENCIES, ALL_BANKS, ALL_METHODS, CONVERT_AM_BANKS, CONVERT_RU_BANKS


def format_rates(rates, result_format="wide", print_=False):
    if result_format == "wide":
        table = pt.PrettyTable()
    else:
        table = pt.PrettyTable(hrules=ALL)
    table.header = False
    table.align = 'l'
    if result_format == "wide":
        table.add_row(['#', 'Из', 'В', 'Метод', 'Курс'])
    else:
        table.add_row(['#', 'Из\nМетод', 'В\nКурс'])

    for rate_num, rate in enumerate(rates):
        format_from_currency = ALL_CURRENCIES[rate["from_currency"]]
        format_to_currency = ALL_CURRENCIES[rate["to_currency"]]
        if rate["from_country"] == "am":
            format_from_bank = CONVERT_AM_BANKS[rate["from_bank"]]
        else:
            format_from_bank = CONVERT_RU_BANKS[rate["from_bank"]]
        if rate["to_country"] == "am":
            format_to_bank = CONVERT_AM_BANKS[rate["to_bank"]]
        else:
            format_to_bank = CONVERT_RU_BANKS[rate["to_bank"]]
        if rate["method"] in ALL_METHODS:
            format_method = ALL_METHODS[rate["method"]]
        else:
            format_method = ALL_BANKS[rate["method"]]
        if rate["value_from"] == "-" or rate["value_to"] == "-":
            format_value = "-"
        elif rate["value_from"] >= rate["value_to"] or rate["from_currency"] == "rur" and rate["to_currency"] == "rsd":
            format_value = str(f'{rate["value_from"]:.2f}') + " " + format_from_currency
        else:
            format_value = str(f'{rate["value_to"]:.2f}') + " " + format_to_currency
        if rate["from_type"] == "cash":
            format_from_type = "Cash"
        else:
            format_from_type = format_from_bank
        if rate["to_type"] == "cash":
            format_to_type = "Cash"
        elif rate["to_type"] == "pos":
            format_to_type = "POS"
        else:
            format_to_type = format_to_bank

        format_num = str(rate_num + 1)
        if format_method == "Total":
            format_num = "Σ"

        if result_format == "wide":
            table.add_row([format_num,
                           format_from_type + " " + format_from_currency,
                           format_to_type + " " + format_to_currency,
                           format_method, format_value])
        else:
            table.add_row([format_num,
                           format_from_type + " " + format_from_currency + "\n" + format_method,
                           format_to_type + " " + format_to_currency + "\n" + format_value])

    if print_:
        print(table)
    return table
