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
    print()


def get_all_convert(rates, from_currency, from_type, to_currency, to_type,
                    exclude_methods=None,
                    all_steps_list=None,
                    all_price_list=None,
                    current_steps=None):
    if exclude_methods is None:
        exclude_methods = []
    if current_steps is None:
        current_steps = []
    if all_price_list is None:
        all_price_list = []
    if all_steps_list is None:
        all_steps_list = []
    if len(current_steps) > 10:
        return None, None

    for rate in rates:
        if rate["method"] in exclude_methods:
            continue
        if rate["from_currency"] == from_currency and rate["from_type"] == from_type:
            if rate["to_currency"] != to_currency or rate["to_type"] != to_type:
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
                                exclude_methods=exclude_methods,
                                all_steps_list=all_steps_list,
                                all_price_list=all_price_list,
                                current_steps=new_current_steps)
    return all_price_list, all_steps_list


def get_best_convert(rates, from_currency, from_type, to_currency, to_type,
                     allow_uncertainty=0,
                     print_result=False,
                     exclude_methods=None):
    all_price_list, all_steps_list = get_all_convert(rates, from_currency, from_type, to_currency, to_type,
                                                     exclude_methods=exclude_methods)

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
    if print_result and best_price is not None:
        head = create_rate(from_currency, from_type, to_currency, to_type, "", best_price, "from")
        lens = get_lens(best_steps)
        print_rate(head, lens)
        print("All steps:")
        print_rates(best_steps, lens)

    return best_price, best_steps


def find_arbitrage(rates):
    pairs = set([(rate["from_currency"], rate["from_type"]) for rate in rates])
    for pair in pairs:
        price, steps = get_best_convert(rates, pair[0], pair[1], pair[0], pair[1], print_result=False)
        if price is not None and price < 1:
            print("Arbitrage found!")
            get_best_convert(rates, pair[0], pair[1], pair[0], pair[1], print_result=True)
