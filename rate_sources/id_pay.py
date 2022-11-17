from rate import add_rate
import log


def add_id_pay(all_rates, fee=0.009):
    if all_rates is None or len(all_rates) == 0:
        log.logger.error("Can not get ID Pay rate, all_rates is empty")
        return
    rate_added = False
    for rate in all_rates:
        if rate["from_currency"] == "rur" \
                and rate["from_type"] == "bank" \
                and rate["from_country"] == "am" \
                and rate["from_bank"] == "aydi-bank" \
                and rate["to_currency"] == "amd" \
                and rate["to_type"] == "bank" \
                and rate["to_country"] == "am" \
                and rate["to_bank"] == "aydi-bank" \
                and rate["method"] == "convert":
            add_rate(all_rates, "rur", "bank", "ru", "", "amd", "bank", "am", "", "idpay",
                     rate["value_from"] * (1 + fee), "from")
            rate_added = True
            break
    if not rate_added:
        log.logger.error("Can not get ID Pay rate, all_rates doesn't have ID Bank rate")
