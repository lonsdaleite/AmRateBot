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


def get_best_convert(rates, from_currency, from_type, to_currency, to_type, allow_uncertainty=0, steps=[], print_result=False):
    # print(steps)
    if len(steps) > 10:
        return [], None
    best_steps_list = []
    best_rate_list = []
    for rate in rates:
        if rate["from_currency"] == from_currency and rate["from_type"] == from_type:
            stop = False
            for step in steps:
                if rate["to_currency"] == step["from_currency"] and rate["to_type"] == step["from_type"]:
                    stop = True
                    break
            if stop:
                continue
            new_steps = steps.copy()
            new_steps.append(rate)
            if rate["to_currency"] == to_currency and rate["to_type"] == to_type:
                new_best_steps = new_steps
                new_best_rate = 1
                for step in new_best_steps:
                    new_best_rate *= step["value_from"]
                # print_format(new_best_steps, new_best_rate)
            else:
                # if from_currency == "amd" and from_currency == "cash":
                #     print("!!!!!!")
                #     for step in new_steps:
                #         print(step)
                #     print()
                new_best_steps, new_best_rate = \
                    get_best_convert(rates, rate["to_currency"], rate["to_type"], to_currency, to_type, steps=new_steps)

            if new_best_rate is not None:
                best_steps_list.append(new_best_steps)
                best_rate_list.append(new_best_rate)
    best_rate = None
    best_steps = None
    for num, rate in enumerate(best_rate_list):
        # for step in best_steps_list[num]:
        #     print(step)
        # print(rate)
        # print()
        if rate is not None and (best_rate is None or best_rate > rate):
            best_rate = rate
            best_steps = best_steps_list[num]

    if len(steps) == 0:
        if allow_uncertainty > 0:
            second_best_rate = best_rate
            second_best_steps = best_steps
            for num, rate in enumerate(best_rate_list):
                if rate is not None \
                        and rate < best_rate * (1 + allow_uncertainty) \
                        and len(best_steps_list[num]) < len(second_best_steps):
                    second_best_rate = rate
                    second_best_steps = best_steps_list[num]
                    print("!!!!", rate)
            best_rate = second_best_rate
            best_steps = second_best_steps
        if print_result:
            print(from_currency + ", " + from_type + " -> " + to_currency + ", " + to_type)
            for print_step in best_steps:
                print(print_step)
            print(from_currency + ": " + str(best_rate) + ", " + to_currency + ": " + str(1 / best_rate))
            print()

    return best_steps, best_rate
