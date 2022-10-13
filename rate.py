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


def get_best_convert(rates, from_currency, from_type, to_currency, to_type,
                     all_steps_list=None,
                     all_rate_list=None,
                     current_steps=None,
                     allow_uncertainty=0,
                     print_result=False):
    # print(current_steps)
    if current_steps is None:
        current_steps = []
    if all_rate_list is None:
        all_rate_list = []
    if all_steps_list is None:
        all_steps_list = []
    if len(current_steps) > 10:
        return None, None
    for rate in rates:
        if rate["from_currency"] == from_currency and rate["from_type"] == from_type:
            stop = False
            for step in current_steps:
                if rate["to_currency"] == step["from_currency"] and rate["to_type"] == step["from_type"]:
                    stop = True
                    break
            if stop:
                continue
            new_current_steps = current_steps.copy()
            new_current_steps.append(rate)
            if rate["to_currency"] == to_currency and rate["to_type"] == to_type:
                new_rate = 1
                for step in new_current_steps:
                    new_rate *= step["value_from"]
                all_steps_list.append(new_current_steps)
                all_rate_list.append(new_rate)
                # print_format(new_steps, new_rate)
            else:
                get_best_convert(rates, rate["to_currency"], rate["to_type"], to_currency, to_type,
                                 all_steps_list=all_steps_list,
                                 all_rate_list=all_rate_list,
                                 current_steps=new_current_steps)

    if len(current_steps) == 0:
        best_rate = None
        best_steps = None
        for num, rate in enumerate(all_rate_list):
            if best_rate is None or best_rate > rate:
                best_rate = rate
                best_steps = all_steps_list[num]
        if allow_uncertainty > 0:
            second_best_rate = best_rate
            second_best_steps = best_steps
            for num, rate in enumerate(all_rate_list):
                if rate < best_rate * (1 + allow_uncertainty) \
                        and len(all_steps_list[num]) < len(second_best_steps):
                    second_best_rate = rate
                    second_best_steps = all_steps_list[num]
                    # print("!!!!", rate)
            best_rate = second_best_rate
            best_steps = second_best_steps
        if print_result:
            print(from_currency + ", " + from_type + " -> " + to_currency + ", " + to_type)
            for print_step in best_steps:
                print(print_step)
            print(from_currency + ": " + str(best_rate) + ", " + to_currency + ": " + str(1 / best_rate))
            print()

        return best_steps, best_rate
    else:
        return None, None
