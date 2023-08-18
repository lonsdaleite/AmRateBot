from rate import add_rate
import log
from rate_sources.tinkoff_broker import get_currency


def add_raiffeisen(url="https://www.tinkoff.ru/invest/currencies/", all_rates=None, fee=0.019, method="broker"):
    usdrub_rate = get_currency(url + "USDRUB")
    eurrub_rate = get_currency(url + "EURRUB")
    # print(usdrub_rate, eurrub_rate)

    if usdrub_rate is not None and eurrub_rate is not None:
        add_rate(all_rates, "rur", "bank", "ru", "raif", "usd", "bank", "ru", "raif", method,
                 float(usdrub_rate) * (1 + fee), "from")
        add_rate(all_rates, "rur", "bank", "ru", "raif", "eur", "bank", "ru", "raif", method,
                 float(eurrub_rate) * (1 + fee), "from")
    else:
        log.logger.error("Can not add Raiffeisen rates")
