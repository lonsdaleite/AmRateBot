from rate import add_rate
from rate_sources.gpb_broker import add_gpb_broker
from rate_sources.id_pay import add_id_pay
from rate_sources.raiffeisen import add_raiffeisen
from rate_sources.rate_am import add_rate_am
from rate_sources.sas import add_sas
from rate_sources.mir import add_mir
from rate_sources.tinkoff_broker import add_tinkoff_broker
from rate_sources.tinkoff_card import add_tinkoff_card
from rate_sources.unionpay import add_unionpay
from rate_sources.unistream import add_unistream
import log
from rate_sources.visa import add_visa


def add_const_rates(all_rates=None):
    if all_rates is None:
        all_rates = []

    # AM - AM
    add_rate(all_rates, "amd", "bank", "am", "",           "amd", "bank", "am", "",         "transfer", 1,     "from", instant=False)
    add_rate(all_rates, "amd", "bank", "am", "",           "amd", "pos",  "am", "",         "pos",      1,     "from")
    add_rate(all_rates, "rur", "bank", "am", "yunibank",   "rur", "cash", "am", "",         "bank",     1.02,  "from", instant=False)
    add_rate(all_rates, "usd", "bank", "am", "yunibank",   "usd", "cash", "am", "",         "bank",     1.02,  "from", instant=False)
    add_rate(all_rates, "eur", "bank", "am", "yunibank",   "eur", "cash", "am", "",         "bank",     1.02,  "from", instant=False)
    add_rate(all_rates, "amd", "bank", "am", "",           "amd", "cash", "am", "",         "atm",      1,     "from")
    add_rate(all_rates, "amd", "cash", "am", "",           "amd", "bank", "am", "",         "atm",      1,     "from")
    add_rate(all_rates, "usd", "cash", "am", "",           "usd", "bank", "am", "yunibank", "bank",     1,     "from", instant=False)
    add_rate(all_rates, "eur", "cash", "am", "",           "eur", "bank", "am", "yunibank", "bank",     1,     "from", instant=False)
    add_rate(all_rates, "rur", "cash", "am", "",           "rur", "bank", "am", "yunibank", "bank",     1.02,  "from", instant=False)

    # RU - RU
    add_rate(all_rates, "rur", "bank", "ru", "",           "rur", "bank", "ru", "",         "transfer", 1,     "from")
    add_rate(all_rates, "cny", "bank", "ru", "tinkoff",    "cny", "bank", "ru", "gpb",      "swift",    1,     "from")

    # RU - AM
    add_rate(all_rates, "amd", "bank", "ru", "tinkoff",    "amd", "pos",  "am", "",         "pos",      1,      "from")
    add_rate(all_rates, "rur", "bank", "ru", "",           "rur", "bank", "am", "",         "transfer", 1,      "from", instant=False)

    # AM - RU
    add_rate(all_rates, "rur", "bank", "am", "yunibank",   "rur", "bank", "ru", "",         "transfer", 1.002, "from", instant=False)

    # RS - RS
    add_rate(all_rates, "rsd", "bank", "rs", "", "rsd", "bank", "rs", "",        "transfer", 1, "from", instant=False)
    add_rate(all_rates, "rsd", "bank", "rs", "", "rsd", "pos",  "rs", "",        "pos",      1, "from")
    add_rate(all_rates, "rsd", "bank", "rs", "", "rsd", "cash", "rs", "",        "atm",      1, "from")
    add_rate(all_rates, "rsd", "cash", "rs", "", "rsd", "bank", "rs", "",        "atm",      1, "from")
    add_rate(all_rates, "eur", "cash", "rs", "", "eur", "bank", "rs", "alta",    "bank",     1, "from", instant=False)
    add_rate(all_rates, "eur", "cash", "rs", "", "eur", "bank", "rs", "raif-rs", "bank",     1, "from", instant=False)
    add_rate(all_rates, "eur", "bank", "rs", "", "eur", "cash", "rs", "alta",    "bank",     1, "from", instant=False)
    add_rate(all_rates, "eur", "bank", "rs", "", "eur", "cash", "rs", "raif-rs", "bank",     1, "from", instant=False)
    #### TEST ####
    add_rate(all_rates, "eur", "bank", "rs", "alta", "rsd", "bank", "rs", "alta", "bank", 116.6325, "to")
    add_rate(all_rates, "rsd", "bank", "rs", "alta", "eur", "bank", "rs", "alta", "bank", 117.7461, "from")
    add_rate(all_rates, "eur", "cash", "rs", "",     "rsd", "cash", "rs", "",     "convert", 117, "to")
    add_rate(all_rates, "rsd", "cash", "rs", "",     "eur", "cash", "rs", "",     "convert", 117.3, "from")

    # RU - RS
    add_rate(all_rates, "eur", "bank", "ru", "raif", "eur", "bank", "rs", "alta",    "swift", 1.015 * 1.002, "from", instant=False)
    add_rate(all_rates, "eur", "bank", "ru", "raif", "eur", "bank", "rs", "raif-rs", "swift", 1.015, "from", instant=False)

    # AM - RS
    add_rate(all_rates, "eur", "bank", "am", "ardshinbank", "eur", "bank", "rs", "alta",    "swift", 1.02 * 1.002,  "from", instant=False)
    add_rate(all_rates, "eur", "bank", "am", "ardshinbank", "eur", "bank", "rs", "raif-rs", "swift", 1.02 * 1.002,  "from", instant=False)
    add_rate(all_rates, "eur", "bank", "am", "yunibank",    "eur", "bank", "rs", "alta",    "swift", 1.002 * 1.002, "from", instant=False)
    add_rate(all_rates, "eur", "bank", "am", "yunibank",    "eur", "bank", "rs", "raif-rs", "swift", 1.002 * 1.002, "from", instant=False)

    return all_rates


def add_all_rates(all_rates=None):
    log.logger.debug("Adding rates...")
    if all_rates is None:
        all_rates = []

    add_sas(all_rates=all_rates)
    # add_mir(all_rates=all_rates)
    add_tinkoff_broker(all_rates=all_rates)
    add_tinkoff_card(all_rates=all_rates)
    add_gpb_broker(all_rates=all_rates)
    add_raiffeisen(all_rates=all_rates, fee=0.019, method="broker")
    add_raiffeisen(all_rates=all_rates, fee=0.01, method="convert")
    add_unistream(all_rates=all_rates)
    add_rate_am(convert_type="cash", all_rates=all_rates)
    add_rate_am(convert_type="non-cash", all_rates=all_rates)
    add_id_pay(all_rates)
    add_unionpay(all_rates=all_rates)
    add_visa(all_rates=all_rates)

    add_const_rates(all_rates=all_rates)

    log.logger.debug("Rates added")

    return all_rates
