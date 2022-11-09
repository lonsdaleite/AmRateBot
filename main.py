from add_rates import add_all_rates
from rate import get_best_convert, format_rates

all_rates = add_all_rates()
format_rates(all_rates, print_=True)
uncertainty = 0.000

get_best_convert(all_rates, "rur", "cash",    "eur", "cash",     allow_uncertainty=uncertainty, print_=True)
get_best_convert(all_rates, "rur", "tinkoff", "eur", "cash",     allow_uncertainty=uncertainty, print_=True)
get_best_convert(all_rates, "rur", "tinkoff", "eur", "yunibank", allow_uncertainty=uncertainty, print_=True)

get_best_convert(all_rates, "rur", "cash",    "usd", "cash",     allow_uncertainty=uncertainty, print_=True)
get_best_convert(all_rates, "rur", "tinkoff", "usd", "cash",     allow_uncertainty=uncertainty, print_=True)
get_best_convert(all_rates, "rur", "tinkoff", "usd", "yunibank", allow_uncertainty=uncertainty, print_=True)

get_best_convert(all_rates, "rur", "cash",    "amd", "cash",     allow_uncertainty=uncertainty, print_=True)
get_best_convert(all_rates, "rur", "tinkoff", "amd", "cash",     allow_uncertainty=uncertainty, print_=True)
get_best_convert(all_rates, "rur", "tinkoff", "amd", "yunibank", allow_uncertainty=uncertainty, print_=True)

# get_best_convert(all_rates, "usd", "yunibank", "amd", "yunibank", allow_uncertainty=uncertainty, print_=True)
# get_best_convert(all_rates, "usd", "yunibank", "amd", "cash",     allow_uncertainty=uncertainty, print_=True)
# get_best_convert(all_rates, "usd", "yunibank", "eur", "yunibank", allow_uncertainty=uncertainty, print_=True)
# get_best_convert(all_rates, "usd", "yunibank", "eur", "cash",     allow_uncertainty=uncertainty, print_=True)

# get_best_convert(all_rates, "rur", "cash",    "eur", "cash",     allow_uncertainty=uncertainty, print_=True, exclude_methods=["swift"])
# get_best_convert(all_rates, "rur", "tinkoff", "eur", "cash",     allow_uncertainty=uncertainty, print_=True, exclude_methods=["swift"])
# get_best_convert(all_rates, "rur", "tinkoff", "eur", "yunibank", allow_uncertainty=uncertainty, print_=True, exclude_methods=["swift"])
#
# get_best_convert(all_rates, "rur", "cash",    "usd", "cash",     allow_uncertainty=uncertainty, print_=True, exclude_methods=["swift"])
# get_best_convert(all_rates, "rur", "tinkoff", "usd", "cash",     allow_uncertainty=uncertainty, print_=True, exclude_methods=["swift"])
# get_best_convert(all_rates, "rur", "tinkoff", "usd", "yunibank", allow_uncertainty=uncertainty, print_=True, exclude_methods=["swift"])
#
# get_best_convert(all_rates, "rur", "cash",    "amd", "cash",     allow_uncertainty=uncertainty, print_=True, exclude_methods=["swift"])
# get_best_convert(all_rates, "rur", "tinkoff", "amd", "cash",     allow_uncertainty=uncertainty, print_=True, exclude_methods=["swift", "unistream"])
# get_best_convert(all_rates, "rur", "tinkoff", "amd", "yunibank", allow_uncertainty=uncertainty, print_=True, exclude_methods=["swift", "unistream"])

# find_arbitrage(all_rates, print_=True)
