def add_rate(rates, from_currency, from_type, to_currency, to_type, method, value, value_type):
    if value_type == "from":
        value_from = value
        value_to = 1 / value
    else:
        value_from = 1 / value
        value_to = value
    rates.append({
        "from_currency": from_currency,
        "from_type": from_type,
        "to_currency": to_currency,
        "to_type": to_type,
        "method": method,
        "value_from": value_from,
        "value_to": value_to
    })


def print_rate(rate):
    new_rate = rate.copy()
    new_rate['value_from'] = round(new_rate['value_from'], 5)
    new_rate['value_to'] = round(new_rate['value_to'], 5)
    print(new_rate)


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
        print(from_currency + ", " + from_type + " -> " + to_currency + ", " + to_type)
        for print_step in best_steps:
            print_rate(print_step)
        print(from_currency + ": " + str(round(best_price, 5)) + ", " +
              to_currency + ": " + str(round(1 / best_price, 5)))
        print()

    return best_price, best_steps
