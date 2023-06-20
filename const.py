from collections import OrderedDict

ALL_CURRENCIES = OrderedDict({
    "rur": "₽",
    "usd": "$",
    "eur": "€",
    "amd": "֏",
    "rsd": "RSD"
})
LIST_CURRENCIES = list(ALL_CURRENCIES.keys())

CONVERT_CASH = OrderedDict({"cash": "Наличные"})
CONVERT_POS = OrderedDict({"pos": "Оплата"})

# Add new banks to the end only! You can ignore "" bank
CONVERT_RU_BANKS = OrderedDict({
    "tinkoff": "Tinkoff",
    "raif": "Raiffeisen",
    "": "Банк РФ"
})
LIST_RU_BANKS = list(CONVERT_RU_BANKS.keys())

RU_BANKS_ID_TO_NAME = {}
RU_BANKS_NAME_TO_ID = {}
num = 0
for bank_name in LIST_RU_BANKS:
    if bank_name == "":
        continue
    num += 1
    bank_id = "R" + str(num)
    RU_BANKS_ID_TO_NAME[bank_id] = bank_name
    RU_BANKS_NAME_TO_ID[bank_name] = bank_id

# Add new banks to the end only! You can ignore "" bank
CONVERT_AM_BANKS = OrderedDict({
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
    "": "Банк РА"
})
LIST_AM_BANKS = list(CONVERT_AM_BANKS.keys())

AM_BANKS_ID_TO_NAME = {}
AM_BANKS_NAME_TO_ID = {}
num = 0
for bank_name in LIST_AM_BANKS:
    if bank_name == "":
        continue
    num += 1
    bank_id = "A" + str(num)
    AM_BANKS_ID_TO_NAME[bank_id] = bank_name
    AM_BANKS_NAME_TO_ID[bank_name] = bank_id

# Add new banks to the end only! You can ignore "" bank
CONVERT_RS_BANKS = OrderedDict({
    "alta": "Alta",
    "raif-rs": "Raiffeisen SRB",
    "": "Банк РС"
})
LIST_RS_BANKS = list(CONVERT_RS_BANKS.keys())

RS_BANKS_ID_TO_NAME = {}
RS_BANKS_NAME_TO_ID = {}
num = 0
for bank_name in LIST_RS_BANKS:
    if bank_name == "":
        continue
    num += 1
    bank_id = "S" + str(num)
    RS_BANKS_ID_TO_NAME[bank_id] = bank_name
    RS_BANKS_NAME_TO_ID[bank_name] = bank_id

ALL_BANKS = OrderedDict()
ALL_BANKS[""] = "Банк"
ALL_BANKS.update(CONVERT_AM_BANKS)
ALL_BANKS.update(CONVERT_RU_BANKS)
ALL_BANKS.update(CONVERT_RS_BANKS)
LIST_ALL_BANKS = list(ALL_BANKS.keys())

EXCLUDE_BANKS_LIST = ["biblos-bank-armenia", "eychesbisi-bank", "fast-bank", "haybiznesbank", "hayekonombank", "mellat-bank"]
SETTINGS_ALL_BANKS = [x for x in LIST_ALL_BANKS if x not in EXCLUDE_BANKS_LIST]

ALL_BANKS_ID_TO_NAME = {"0": ""}
ALL_BANKS_ID_TO_NAME.update(RU_BANKS_ID_TO_NAME)
ALL_BANKS_ID_TO_NAME.update(AM_BANKS_ID_TO_NAME)
ALL_BANKS_ID_TO_NAME.update(RS_BANKS_ID_TO_NAME)

ALL_BANKS_NAME_TO_ID = {"": "0"}
ALL_BANKS_NAME_TO_ID.update(RU_BANKS_NAME_TO_ID)
ALL_BANKS_NAME_TO_ID.update(AM_BANKS_NAME_TO_ID)
ALL_BANKS_NAME_TO_ID.update(RS_BANKS_NAME_TO_ID)

ALL_METHODS = OrderedDict({
    "": "",
    "atm": "ATM",
    "bank": "Банк",
    "broker": "Биржа",
    "convert": "Обмен",
    "idpay": "IDpay",
    "sas": "SAS",
    "swift": "Swift",
    "total": "Итого",
    "transfer": "Перевод",
    "unistream": "Unistream",
    "pos": "Оплата"
})
