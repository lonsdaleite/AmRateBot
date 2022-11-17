from rate import add_rate


def add_id_pay(all_rates, fee=0.009):
    if all_rates is None or len(all_rates) == 0:
        print("ERROR: Can not get ID Pay rate, all_rates is empty")
        return
    rate_added = False
    for rate in all_rates:
        if rate["from_currency"] == "rur" \
                and rate["to_currency"] == "amd" \
                and rate["from_type"] == "aydi-bank" \
                and rate["to_type"] == "aydi-bank" \
                and rate["method"] == "convert":
            add_rate(all_rates, "rur", "tinkoff", "amd", "yunibank", "idpay", rate["value_from"] * (1 + fee), "from")
            rate_added = True
            break
    if not rate_added:
        print("ERROR: Can not get ID Pay rate, all_rates doesn't have ID Bank rate")
