from rate import add_rate
from rate_sources.id_pay import add_id_pay
from rate_sources.rate_am import add_rate_am
from rate_sources.sas import add_sas
from rate_sources.mir import add_mir
from rate_sources.tinkoff_broker import add_tinkoff_broker
from rate_sources.unistream import add_unistream


def add_const_rates(all_rates=None):
    if all_rates is None:
        all_rates = []

    add_rate(all_rates, "rur", "tinkoff", "rur", "yunibank", "transfer", 1, "from")
    add_rate(all_rates, "usd", "tinkoff", "usd", "yunibank", "swift", 1.005, "from")
    add_rate(all_rates, "eur", "tinkoff", "eur", "yunibank", "swift", 1.005, "from")
    add_rate(all_rates, "rur", "yunibank", "rur", "cash", "bank", 1.02, "from")
    add_rate(all_rates, "usd", "yunibank", "usd", "cash", "bank", 1.02, "from")
    add_rate(all_rates, "eur", "yunibank", "eur", "cash", "bank", 1.02, "from")
    add_rate(all_rates, "amd", "yunibank", "amd", "cash", "atm", 1, "from")
    add_rate(all_rates, "amd", "cash", "amd", "yunibank", "bank", 1, "from")
    add_rate(all_rates, "usd", "cash", "usd", "yunibank", "bank", 1, "from")
    add_rate(all_rates, "eur", "cash", "eur", "yunibank", "bank", 1, "from")
    add_rate(all_rates, "rur", "cash", "rur", "yunibank", "bank", 1.02, "from")
    add_rate(all_rates, "rur", "yunibank", "rur", "tinkoff", "transfer", 1.002, "from")

    return all_rates


def add_all_rates(all_rates=None):
    if all_rates is None:
        all_rates = []

    add_sas(all_rates=all_rates)
    add_mir(all_rates=all_rates)
    add_tinkoff_broker(all_rates=all_rates)
    add_unistream(all_rates=all_rates)
    add_rate_am(convert_type="cash", all_rates=all_rates)
    add_rate_am(convert_type="non-cash", all_rates=all_rates)
    add_id_pay(all_rates)

    add_const_rates(all_rates=all_rates)

    return all_rates
