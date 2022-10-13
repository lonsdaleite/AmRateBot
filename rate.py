def create_rate(from_currency, from_type, to_currency, to_type, method, value, value_type):
    if value_type == "from":
        value_from = value
        value_to = 1 / value
    else:
        value_from = 1 / value
        value_to = value
    return {
        "from_currency": from_currency,
        "from_type": from_type,
        "to_currency": to_currency,
        "to_type": to_type,
        "method": method,
        "value_from": value_from,
        "value_to": value_to
    }


def add_rate(rates, from_currency, from_type, to_currency, to_type, method, value, value_type):
    rates.append(create_rate(from_currency, from_type, to_currency, to_type, method, value, value_type))


def print_rate(rate, lens):
    print("{}{}{}{}{}{}{}{}{}{}".format(
        (rate["from_currency"] + ",").ljust(lens[0] + 2),
        rate["from_type"].ljust(lens[1] + 1),
        "-> ",
        (rate["to_currency"] + ",").ljust(lens[2] + 2),
        rate["to_type"].ljust(lens[3] + 1),
        ("(" + rate["method"]).ljust(lens[4] + 2),
        (rate["from_currency"] + ":").ljust(lens[5] + 2),
        (str(round(rate['value_from'], 5)) + ",").ljust(lens[6] + 2),
        (rate["to_currency"] + ":").ljust(lens[7] + 2),
        str(round(rate['value_to'], 5)) + ")"
    ))


def get_lens(rates):
    return [max([len(x["from_currency"]) for x in rates]),
            max([len(x["from_type"]) for x in rates]),
            max([len(x["to_currency"]) for x in rates]),
            max([len(x["to_type"]) for x in rates]),
            max([len(x["method"]) for x in rates]),
            max([len(x["from_currency"]) for x in rates]),
            max([len(str(round(x['value_from'], 5))) for x in rates]),
            max([len(x["to_currency"]) for x in rates]),
            max([len(str(round(x['value_to'], 5))) for x in rates])]


def print_rates(rates, lens=None):
    if lens is None:
        lens = get_lens(rates)
    for rate in rates:
        print_rate(rate, lens)


def get_all_convert(rates, from_currency, from_type, to_currency, to_type,
                    all_steps_list=None,
                    all_price_list=None,
                    current_steps=None):
    if current_steps is None:
        current_steps = []
    if all_price_list is None:
        all_price_list = []
    if all_steps_list is None:
        all_steps_list = []
    if len(current_steps) > 10:
        return None, None

    for rate in rates:
        if rate["from_currency"] == from_currency and rate["from_type"] == from_type:
            recursion = False
            for step in current_steps:
                if rate["to_currency"] == step["from_currency"] and rate["to_type"] == step["from_type"]:
                    recursion = True
                    break
            if recursion:
                continue
            new_current_steps = current_steps.copy()
            new_current_steps.append(rate)
            if rate["to_currency"] == to_currency and rate["to_type"] == to_type:
                new_price = 1
                for step in new_current_steps:
                    new_price *= step["value_from"]
                all_steps_list.append(new_current_steps)
                all_price_list.append(new_price)
            else:
                get_all_convert(rates, rate["to_currency"], rate["to_type"], to_currency, to_type,
                                all_steps_list=all_steps_list,
                                all_price_list=all_price_list,
                                current_steps=new_current_steps)
    return all_price_list, all_steps_list


def get_best_convert(rates, from_currency, from_type, to_currency, to_type,
                     allow_uncertainty=0,
                     print_result=False):
    all_price_list, all_steps_list = get_all_convert(rates, from_currency, from_type, to_currency, to_type)

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
    if print_result:
        head = create_rate(from_currency, from_type, to_currency, to_type, "", best_price, "from")
        lens = get_lens(best_steps)
        print_rate(head, lens)
        print("All steps:")
        print_rates(best_steps, lens)
        print()

    return best_price, best_steps
