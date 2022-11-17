from rate import add_rate
from rate_sources.id_pay import add_id_pay
from rate_sources.raiffeisen_broker import add_raiffeisen_broker
from rate_sources.rate_am import add_rate_am
from rate_sources.sas import add_sas
from rate_sources.mir import add_mir
from rate_sources.tinkoff_broker import add_tinkoff_broker
from rate_sources.unistream import add_unistream


def add_const_rates(all_rates=None):
    if all_rates is None:
        all_rates = []

    add_rate(all_rates, "rur", "bank", "ru", "",           "rur", "bank", "ru", "",         "transfer", 1,     "from")
    add_rate(all_rates, "rur", "bank", "ru", "",           "rur", "bank", "am", "",         "transfer", 1,     "from")
    add_rate(all_rates, "usd", "bank", "ru", "tinkoff",    "usd", "bank", "am", "",         "swift",    1.005, "from")
    add_rate(all_rates, "eur", "bank", "ru", "tinkoff",    "eur", "bank", "am", "",         "swift",    1.005, "from")
    add_rate(all_rates, "usd", "bank", "ru", "raiffeisen", "usd", "bank", "am", "",         "swift",    1.03,  "from")
    add_rate(all_rates, "eur", "bank", "ru", "raiffeisen", "eur", "bank", "am", "",         "swift",    1.03,  "from")
    add_rate(all_rates, "rur", "bank", "am", "yunibank",   "rur", "cash", "am", "",         "bank",     1.02,  "from")
    add_rate(all_rates, "usd", "bank", "am", "yunibank",   "usd", "cash", "am", "",         "bank",     1.02,  "from")
    add_rate(all_rates, "eur", "bank", "am", "yunibank",   "eur", "cash", "am", "",         "bank",     1.02,  "from")
    add_rate(all_rates, "amd", "bank", "am", "yunibank",   "amd", "cash", "am", "",         "atm",      1,     "from")
    add_rate(all_rates, "amd", "cash", "am", "",           "amd", "bank", "am", "yunibank", "bank",     1,     "from")
    add_rate(all_rates, "usd", "cash", "am", "",           "usd", "bank", "am", "yunibank", "bank",     1,     "from")
    add_rate(all_rates, "eur", "cash", "am", "",           "eur", "bank", "am", "yunibank", "bank",     1,     "from")
    add_rate(all_rates, "rur", "cash", "am", "",           "rur", "bank", "am", "yunibank", "bank",     1.02,  "from")
    add_rate(all_rates, "rur", "bank", "am", "yunibank",   "rur", "bank", "ru", "",         "transfer", 1.002, "from")

    return all_rates


def add_all_rates(all_rates=None):
    if all_rates is None:
        all_rates = []

    add_sas(all_rates=all_rates)
    add_mir(all_rates=all_rates)
    add_tinkoff_broker(all_rates=all_rates)
    add_raiffeisen_broker(all_rates=all_rates)
    add_unistream(all_rates=all_rates)
    add_rate_am(convert_type="cash", all_rates=all_rates)
    add_rate_am(convert_type="non-cash", all_rates=all_rates)
    add_id_pay(all_rates)

    add_const_rates(all_rates=all_rates)

    return all_rates
