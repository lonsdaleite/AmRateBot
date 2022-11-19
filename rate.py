import copy
from datetime import datetime
import log
from format import format_rates


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
    if len(current_steps) > 7:
        return None, None

    # Copy rates for removing already used steps
    rates_copy = copy.copy(rates)
    rate_num = 0
    while rate_num < len(rates_copy):
        rate = rates_copy[rate_num]

        # Remove excluded rates and continue
        if rate["method"] in exclude_methods \
                or rate["from_bank"] in exclude_banks \
                or rate["to_bank"] in exclude_banks:
            rates_copy.pop(rate_num)
            continue

        # If the next step matches
        if rate["from_currency"] == from_currency \
                and rate["from_type"] == from_type \
                and rate["from_country"] == from_country \
                and (rate["from_bank"] == "" or from_bank == "" or rate["from_bank"] == from_bank):

            # Checking steps recursion
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
                    rate_num += 1
                    continue

            # Copy current_steps for the next iteration and append the next step
            new_current_steps = copy.copy(current_steps)
            new_current_steps.append(rate)
            rates_copy.pop(rate_num)

            # Update bank info for rates with bank == ""
            if len(new_current_steps) == 1:
                if from_bank != "" and new_current_steps[-1]["from_bank"] == "":
                    tmp_step_1 = copy.copy(new_current_steps[-1])
                    tmp_step_1["from_bank"] = from_bank
                    new_current_steps[-1] = tmp_step_1
            else:
                if new_current_steps[-2]["to_bank"] != "" and new_current_steps[-1]["from_bank"] == "":
                    tmp_step_1 = copy.copy(new_current_steps[-1])
                    tmp_step_1["from_bank"] = new_current_steps[-2]["to_bank"]
                    new_current_steps[-1] = tmp_step_1
                elif new_current_steps[-2]["to_bank"] == "" and new_current_steps[-1]["from_bank"] != "":
                    tmp_step_2 = copy.copy(new_current_steps[-2])
                    tmp_step_2["to_bank"] = new_current_steps[-1]["from_bank"]
                    new_current_steps[-2] = tmp_step_2

            # If it is the final step
            if rate["to_currency"] == to_currency \
                    and rate["to_type"] == to_type \
                    and rate["to_country"] == to_country \
                    and (rate["to_bank"] == "" or to_bank == "" or rate["to_bank"] == to_bank):
                new_price = 1
                for step in new_current_steps:
                    new_price *= step["value_from"]

                # Update bank info for rates with bank == ""
                if to_bank != "" and new_current_steps[-1]["to_bank"] == "":
                    tmp_step_1 = copy.copy(new_current_steps[-1])
                    tmp_step_1["to_bank"] = to_bank
                    new_current_steps[-1] = tmp_step_1

                all_steps_list.append(new_current_steps)
                all_price_list.append(new_price)
            else:  # If it is not the final step
                get_all_convert(rates_copy,
                                rate["to_currency"], rate["to_type"], rate["to_country"], rate["to_bank"],
                                to_currency, to_type, to_country, to_bank,
                                exclude_methods=exclude_methods,
                                exclude_banks=exclude_banks,
                                all_steps_list=all_steps_list,
                                all_price_list=all_price_list,
                                current_steps=new_current_steps)
        else:  # If the next step doesn't match
            rate_num += 1

    return all_price_list, all_steps_list


def get_best_convert(rates,
                     from_currency, from_type, from_country, from_bank,
                     to_currency, to_type, to_country, to_bank,
                     allow_uncertainty=0,
                     exclude_methods=None,
                     exclude_banks=None,
                     print_=False):

    # debug_start_all = timer()

    all_price_list, all_steps_list = get_all_convert(rates,
                                                     from_currency, from_type, from_country, from_bank,
                                                     to_currency, to_type, to_country, to_bank,
                                                     exclude_methods=exclude_methods, exclude_banks=exclude_banks)

    # debug_end_all = timer()
    # log.logger.debug("get_all_convert time: " + str(debug_end_all - debug_start_all))

    # Find the best steps and price
    best_price = None
    best_steps = None
    for num, price in enumerate(all_price_list):
        if best_price is None or best_price > price:
            best_price = price
            best_steps = all_steps_list[num]

    # Find shorter steps with almost the same price
    if allow_uncertainty >= 0:
        second_best_price = best_price
        second_best_steps = best_steps
        for num, price in enumerate(all_price_list):
            if price <= best_price * (1 + allow_uncertainty) \
                    and len(all_steps_list[num]) < len(second_best_steps):
                second_best_price = price
                second_best_steps = all_steps_list[num]
        best_price = second_best_price
        best_steps = second_best_steps

    # Format output
    result = ""
    if best_price is not None:
        head = create_rate(from_currency, from_type, from_country, from_bank,
                           to_currency, to_type, to_country, to_bank,
                           "total", best_price, "from")
        result = format_rates([head] + best_steps, print_=False)

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
