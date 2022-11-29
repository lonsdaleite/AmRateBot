import prettytable as pt
from prettytable import ALL

CURRENCIES = {
    "": "",
    "rur": "₽",
    "usd": "$",
    "eur": "€",
    "amd": "֏"
}
BANKS = {
    "": "",
    "acba-bank": "Acba Bank",
    "ameriabank": "Ameriabank",
    "araratbank": "AraratBank",
    "arcakhbank": "Artsakhbank",
    "ardshinbank": "Ardshinbank",
    "armsvisbank": "ArmSwissBank",
    "aydi-bank": "IDBank",
    "biblos-bank-armenia": "Byblos",
    "evocabank": "Evocabank",
    "eychesbisi-bank": "HSBC",
    "fast-bank": "Fast Bank",
    "haybiznesbank": "ArmBusinessBank",
    "hayekonombank": "AEB",
    "inekobank": "Inecobank",
    "konvers-bank": "Converse Bank",
    "mellat-bank": "Mellat Bank",
    "vtbhayastan-bank": "VTB",
    "yunibank": "Unibank",
    "tinkoff": "Tinkoff",
    "raiffeisen": "Raiffeisen"
}
METHODS = {
    "": "",
    "atm": "ATM",
    "bank": "Bank",
    "broker": "Broker",
    "convert": "Convert",
    "idpay": "IDpay",
    "sas": "SAS",
    "swift": "Swift",
    "total": "Total",
    "transfer": "Transfer",
    "unistream": "Unistream"
}


def format_rates(rates, result_format="wide", print_=False):
    if result_format == "wide":
        table = pt.PrettyTable()
    else:
        table = pt.PrettyTable(hrules=ALL)
    table.header = False
    table.align = 'l'
    if result_format == "wide":
        table.add_row(['#', 'From', 'Method', 'To', 'Rate'])
    else:
        table.add_row(['#', 'From\nMethod', 'To\nRate'])

    for rate_num, rate in enumerate(rates):
        format_from_currency = CURRENCIES[rate["from_currency"]]
        format_to_currency = CURRENCIES[rate["to_currency"]]
        format_from_bank = BANKS[rate["from_bank"]]
        format_to_bank = BANKS[rate["to_bank"]]
        if rate["method"] in METHODS:
            format_method = METHODS[rate["method"]]
        else:
            format_method = BANKS[rate["method"]]
        if rate["value_from"] >= rate["value_to"]:
            format_value = str(f'{rate["value_from"]:.2f}') + " " + format_from_currency
        else:
            format_value = str(f'{rate["value_to"]:.2f}') + " " + format_to_currency
        if rate["from_type"] == "cash":
            format_from_type = "Cash"
        else:
            format_from_type = format_from_bank
        if rate["to_type"] == "cash":
            format_to_type = "Cash"
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
