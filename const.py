from collections import OrderedDict

ALL_CURRENCIES = OrderedDict({
    "rur": "₽",
    "usd": "$",
    "eur": "€",
    "amd": "֏"
})
LIST_CURRENCIES = list(ALL_CURRENCIES.keys())

CONVERT_CASH = OrderedDict({"cash": "Наличные"})

CONVERT_RU_BANKS = OrderedDict({
    "": "Любой банк РФ",
    "tinkoff": "Tinkoff",
    "raif": "Raiffeisen"
})
LIST_RU_BANKS = list(CONVERT_RU_BANKS.keys())

CONVERT_AM_BANKS = OrderedDict({
    "": "Любой банк РА",
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
    "yunibank": "Unibank"
})
LIST_AM_BANKS = list(CONVERT_AM_BANKS.keys())

ALL_BANKS = OrderedDict()
ALL_BANKS.update(CONVERT_AM_BANKS)
ALL_BANKS.update(CONVERT_RU_BANKS)
ALL_BANKS[""] = "Любой банк"
LIST_ALL_BANKS = list(ALL_BANKS.keys())

DEFAULT_EXCLUDE_BANKS = [x for x in ALL_BANKS if x != ""]

ALL_METHODS = OrderedDict({
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
})

DEFAULT_EXCLUDE_METHODS = ["broker"]
