import prettytable as pt
from prettytable import ALL

CURRENCIES = {"": "", "rur": "RUB", "usd": "USD", "eur": "EUR", "amd": "AMD"}
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

BOLD = '\033[1m'
END = '\033[0m'


def format_rates(rates, print_=False):
    table = pt.PrettyTable(['From', 'To', 'Method', 'Rate'], hrules=ALL)
    table.align['From'] = 'l'
    table.align['To'] = 'l'
    table.align['Method'] = 'l'
    table.align['Rate'] = 'l'

    has_total = False
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

        begin = ""
        end = ""
        if format_method == "Total":
            table.add_row(["", "", "", ""])
            has_total = True
            begin = BOLD
            end = END

        table.add_row([format_from_currency + "\n" + format_from_type,
                       format_to_currency + "\n" + format_to_type,
                       format_method, format_value])

    if has_total:
        table.set_cell_style(font_weight="bold", rows=[len(rates)])

    if print_:
        print(table)
    return table
