from rate import add_rate
from rate_sources.id_pay import add_id_pay
from rate_sources.raiffeisen_broker import add_raiffeisen_broker
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

    add_rate(all_rates, "amd", "bank", "am", "",           "amd", "pos",  "am", "",         "pos",      1,     "from")
    add_rate(all_rates, "amd", "bank", "ru", "tinkoff",    "amd", "pos",  "am", "",         "pos",      1,     "from")
    add_rate(all_rates, "rur", "bank", "ru", "",           "rur", "bank", "ru", "",         "transfer", 1,     "from")
    add_rate(all_rates, "rur", "bank", "ru", "",           "rur", "bank", "am", "",         "transfer", 1,     "from", instant=False)
    add_rate(all_rates, "amd", "bank", "am", "",           "amd", "bank", "am", "",         "transfer", 1,     "from", instant=False)
    # add_rate(all_rates, "usd", "bank", "ru", "tinkoff",    "usd", "bank", "am", "",         "swift",    1.01,  "from", instant=False)
    # add_rate(all_rates, "eur", "bank", "ru", "tinkoff",    "eur", "bank", "am", "",         "swift",    1.01,  "from", instant=False)
    add_rate(all_rates, "usd", "bank", "ru", "raif",       "usd", "bank", "am", "",         "swift",    1.02,  "from", instant=False)
    add_rate(all_rates, "eur", "bank", "ru", "raif",       "eur", "bank", "am", "",         "swift",    1.02,  "from", instant=False)
    add_rate(all_rates, "rur", "bank", "am", "yunibank",   "rur", "cash", "am", "",         "bank",     1.02,  "from", instant=False)
    add_rate(all_rates, "usd", "bank", "am", "yunibank",   "usd", "cash", "am", "",         "bank",     1.02,  "from", instant=False)
    add_rate(all_rates, "eur", "bank", "am", "yunibank",   "eur", "cash", "am", "",         "bank",     1.02,  "from", instant=False)
    add_rate(all_rates, "amd", "bank", "am", "",           "amd", "cash", "am", "",         "atm",      1,     "from")
    add_rate(all_rates, "amd", "cash", "am", "",           "amd", "bank", "am", "",         "atm",      1,     "from")
    add_rate(all_rates, "usd", "cash", "am", "",           "usd", "bank", "am", "yunibank", "bank",     1,     "from", instant=False)
    add_rate(all_rates, "eur", "cash", "am", "",           "eur", "bank", "am", "yunibank", "bank",     1,     "from", instant=False)
    add_rate(all_rates, "rur", "cash", "am", "",           "rur", "bank", "am", "yunibank", "bank",     1.02,  "from", instant=False)
    add_rate(all_rates, "rur", "bank", "am", "yunibank",   "rur", "bank", "ru", "",         "transfer", 1.002, "from", instant=False)

    return all_rates


def add_all_rates(all_rates=None):
    log.logger.debug("Adding rates...")
    if all_rates is None:
        all_rates = []

    add_sas(all_rates=all_rates)
    add_mir(all_rates=all_rates)
    add_tinkoff_broker(all_rates=all_rates)
    add_tinkoff_card(all_rates=all_rates)
    add_raiffeisen_broker(all_rates=all_rates)
    add_unistream(all_rates=all_rates)
    add_rate_am(convert_type="cash", all_rates=all_rates)
    add_rate_am(convert_type="non-cash", all_rates=all_rates)
    add_id_pay(all_rates)
    add_unionpay(all_rates=all_rates)
    add_visa(fee=0.5, bank="ardshinbank", from_curr="AMD", to_curr="RSD", bank_cash_fee=0.015, all_rates=all_rates)
    add_visa(fee=0.5, bank="ardshinbank", from_curr="EUR", to_curr="RSD", bank_cash_fee=0.015, all_rates=all_rates)
    add_visa(fee=2, bank="yunibank", from_curr="AMD", to_curr="RSD", bank_cash_fee=0.013, all_rates=all_rates)
    add_visa(fee=2, bank="yunibank", from_curr="EUR", to_curr="RSD", bank_cash_fee=None, all_rates=all_rates)

    add_const_rates(all_rates=all_rates)

    log.logger.debug("Rates added")

    return all_rates
