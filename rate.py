from datetime import datetime
import log


def create_rate(from_currency, from_type, from_country, from_bank,
                to_currency, to_type, to_country, to_bank,
                method, value, value_type):
    if from_type not in ["cash", "bank"]:
        log.logger.error("from_type can be only cash or bank")
        return None
    if to_type not in ["cash", "bank"]:
        log.logger.error("to_type can be only cash or bank")
        return None
    if from_country not in ["ru", "am"]:
        log.logger.error("from_country can be only ru or am")
        return None
    if to_country not in ["ru", "am"]:
        log.logger.error("to_country can be only ru or am")
        return None
    if from_bank is None:
        from_bank = ""
    if to_bank is None:
        to_bank = ""

    if value_type == "from":
        value_from = value
        value_to = 1 / value
    else:
        value_from = 1 / value
        value_to = value
    return {
        "from_currency": from_currency,
        "from_type": from_type,
        "from_country": from_country,
        "from_bank": from_bank,
        "to_currency": to_currency,
        "to_type": to_type,
        "to_country": to_country,
        "to_bank": to_bank,
        "method": method,
        "value_from": value_from,
        "value_to": value_to,
        "update_ts": datetime.now()
    }


def add_rate(rates,
             from_currency, from_type, from_country, from_bank,
             to_currency, to_type, to_country, to_bank,
             method, value, value_type):
    if from_bank is None:
        from_bank = ""
    if to_bank is None:
        to_bank = ""
    new_rate = create_rate(from_currency, from_type, from_country, from_bank,
                           to_currency, to_type, to_country, to_bank,
                           method, value, value_type)
    for num, rate in enumerate(rates):
        if rate["from_currency"] == from_currency \
                and rate["from_type"] == from_type \
                and rate["from_country"] == from_country \
                and rate["from_bank"] == from_bank \
                and rate["to_currency"] == to_currency \
                and rate["to_type"] == to_type \
                and rate["to_country"] == to_country \
                and rate["to_bank"] == to_bank \
                and rate["method"] == method:
            rate[num] = new_rate
            return
    rates.append(new_rate)


def format_rate(rate, lens, print_=False):
    formatted_rate = "{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(
        (rate["from_currency"] + ",").ljust(lens[0] + 2),
        (rate["from_type"] + ",").ljust(4 + 2),
        (rate["from_country"] + ",").ljust(2 + 2),
        rate["from_bank"].ljust(lens[1] + 1),
        "-> ",
        (rate["to_currency"] + ",").ljust(lens[2] + 2),
        (rate["to_type"] + ",").ljust(4 + 2),
        (rate["to_country"] + ",").ljust(2 + 2),
        rate["to_bank"].ljust(lens[3] + 1),
        ("(" + rate["method"]).ljust(lens[4] + 2),
        (rate["from_currency"] + ":").ljust(lens[5] + 2),
        (str(round(rate['value_from'], 5)) + ",").ljust(lens[6] + 2),
        (rate["to_currency"] + ":").ljust(lens[7] + 2),
        str(round(rate['value_to'], 5)) + ")"
    )
    if print_:
        print(formatted_rate)
    return formatted_rate


def get_lens(rates):
    return [max([len(x["from_currency"]) for x in rates]),
            max([len(x["from_bank"]) for x in rates]),
            max([len(x["to_currency"]) for x in rates]),
            max([len(x["to_bank"]) for x in rates]),
            max([len(x["method"]) for x in rates]),
            max([len(x["from_currency"]) for x in rates]),
            max([len(str(round(x['value_from'], 5))) for x in rates]),
            max([len(x["to_currency"]) for x in rates]),
            max([len(str(round(x['value_to'], 5))) for x in rates])]


def format_rates(rates, lens=None, print_=False):
    formatted_rates = ""
    if lens is None:
        lens = get_lens(rates)
    for rate in rates:
        formatted_rates += format_rate(rate, lens, print_=False) + '\n'
    if print_:
        print(formatted_rates)
    return formatted_rates


def get_all_convert(rates,
                    from_currency, from_type, from_country, from_bank,
                    to_currency, to_type, to_country, to_bank,
                    exclude_methods=None,
                    exclude_banks=None,
                    all_steps_list=None,
                    all_price_list=None,
                    current_steps=None):
    if exclude_methods is None:
        exclude_methods = []
    if exclude_banks is None:
        exclude_banks = []
    if current_steps is None:
        current_steps = []
    if all_price_list is None:
        all_price_list = []
    if all_steps_list is None:
        all_steps_list = []
    if len(current_steps) > 10:
        return None, None

    for rate in rates:
        if rate["method"] in exclude_methods \
                or rate["from_bank"] in exclude_banks \
                or rate["to_bank"] in exclude_banks:
            continue
        if rate["from_currency"] == from_currency \
                and rate["from_type"] == from_type \
                and rate["from_country"] == from_country \
                and (rate["from_bank"] == "" or from_bank == "" or rate["from_bank"] == from_bank):
            if rate["to_currency"] != to_currency \
                    or rate["to_type"] != to_type \
                    or rate["to_country"] != to_country \
                    or (rate["to_bank"] != "" and to_bank != "" and rate["to_bank"] != to_bank):
                recursion = False
                for step in current_steps:
                    if rate["to_currency"] == step["from_currency"] \
                            and rate["to_type"] == step["from_type"] \
                            and rate["to_country"] == step["from_country"] \
                            and (rate["to_bank"] == "" or step["from_bank"] == ""
                                 or rate["to_bank"] == step["from_bank"]):
                        recursion = True
                        break
                if recursion:
                    continue
            new_current_steps = current_steps.copy()
            new_current_steps.append(rate)
            if rate["to_currency"] == to_currency \
                    and rate["to_type"] == to_type \
                    and rate["to_country"] == to_country \
                    and (rate["to_bank"] == "" or to_bank == "" or rate["to_bank"] == to_bank):
                new_price = 1
                for step in new_current_steps:
                    new_price *= step["value_from"]
                all_steps_list.append(new_current_steps)
                all_price_list.append(new_price)
            else:
                get_all_convert(rates,
                                rate["to_currency"], rate["to_type"], rate["to_country"], rate["to_bank"],
                                to_currency, to_type, to_country, to_bank,
                                exclude_methods=exclude_methods,
                                exclude_banks=exclude_banks,
                                all_steps_list=all_steps_list,
                                all_price_list=all_price_list,
                                current_steps=new_current_steps)
    return all_price_list, all_steps_list


def get_best_convert(rates,
                     from_currency, from_type, from_country, from_bank,
                     to_currency, to_type, to_country, to_bank,
                     allow_uncertainty=0,
                     exclude_methods=None,
                     exclude_banks=None,
                     print_=False):
    all_price_list, all_steps_list = get_all_convert(rates,
                                                     from_currency, from_type, from_country, from_bank,
                                                     to_currency, to_type, to_country, to_bank,
                                                     exclude_methods=exclude_methods, exclude_banks=exclude_banks)

    best_price = None
    best_steps = None
    for num, price in enumerate(all_price_list):
        if best_price is None or best_price > price:
            best_price = price
            best_steps = all_steps_list[num]
    if allow_uncertainty > 0:
        second_best_price = best_price
        second_best_steps = best_steps
        for num, price in enumerate(all_price_list):
            if price < best_price * (1 + allow_uncertainty) \
                    and len(all_steps_list[num]) < len(second_best_steps):
                second_best_price = price
                second_best_steps = all_steps_list[num]
        best_price = second_best_price
        best_steps = second_best_steps
    result = ""
    if best_price is not None:
        head = create_rate(from_currency, from_type, from_country, from_bank,
                           to_currency, to_type, to_country, to_bank,
                           "", best_price, "from")
        lens = get_lens(best_steps)
        result += format_rate(head, lens, print_=False) + '\n'
        result += "All steps:\n"
        result += format_rates(best_steps, lens, print_=False)

    if print_:
        print(result)

    return result

# def find_arbitrage(rates, print_=False):
#     pairs = set([(rate["from_currency"], rate["from_type"]) for rate in rates])
#     result = ""
#     for pair in pairs:
#         price, steps = get_best_convert(rates, pair[0], pair[1], pair[0], pair[1], print_=False)
#         if price is not None and price < 1:
#             result += "Arbitrage found!\n"
#             result += get_best_convert(rates, pair[0], pair[1], pair[0], pair[1], print_=True) + "\n"
#     if print_:
#         print(result)
#     return result
