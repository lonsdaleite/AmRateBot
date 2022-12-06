import log
from add_rates import add_all_rates
from rate import get_best_convert
from format import format_rates

all_rates = add_all_rates()
format_rates(all_rates, result_format="wide", print_=True)
uncertainty = 0.000
exclude_methods = []
exclude_banks = ["acba-bank", "ameriabank", "araratbank", "arcakhbank", "ardshinbank", "armsvisbank",
                 "aydi-bank", "biblos-bank-armenia", "evocabank", "eychesbisi-bank", "fast-bank", "haybiznesbank",
                 "hayekonombank", "inekobank", "konvers-bank", "mellat-bank", "vtbhayastan-bank"]

converts = [["rur", "cash", "am", "",        "eur", "cash", "am", "",         [],         []],
            ["rur", "bank", "ru", "tinkoff", "eur", "cash", "am", "",         [],         []],
            ["rur", "bank", "ru", "tinkoff", "eur", "bank", "am", "yunibank", [],         []],
            ["rur", "cash", "am", "",        "usd", "cash", "am", "",         [],         []],
            ["rur", "bank", "ru", "tinkoff", "usd", "cash", "am", "",         [],         []],
            ["rur", "bank", "ru", "tinkoff", "usd", "bank", "am", "yunibank", [],         []],
            ["rur", "cash", "am", "",        "amd", "cash", "am", "",         [],         []],
            ["rur", "bank", "ru", "tinkoff", "amd", "cash", "am", "",         [],         []],
            ["rur", "bank", "ru", "tinkoff", "amd", "bank", "am", "yunibank", [],         []],
            ["rur", "bank", "ru", "tinkoff", "amd", "bank", "am", "yunibank", ["atm"],    []],
            ["rur", "bank", "ru", "tinkoff", "amd", "cash", "am", "",         ["broker"], []]]

for conv in converts:
    get_best_convert(all_rates, conv[0], conv[1], conv[2], conv[3], conv[4], conv[5], conv[6], conv[7],
                     allow_uncertainty=uncertainty, result_format="wide", print_=True,
                     exclude_methods=exclude_methods + conv[8],
                     exclude_banks=exclude_banks + conv[9])

log.logger.debug("Done")

# find_arbitrage(all_rates, print_=True)
