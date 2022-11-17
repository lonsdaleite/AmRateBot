from add_rates import add_all_rates
from rate import get_best_convert, format_rates

all_rates = add_all_rates()
# print(all_rates)
format_rates(all_rates, print_=True)
uncertainty = 0.003

get_best_convert(all_rates, "rur", "cash", "am", "",        "eur", "cash", "am", "",         allow_uncertainty=uncertainty, print_=True)
get_best_convert(all_rates, "rur", "bank", "ru", "tinkoff", "eur", "cash", "am", "",         allow_uncertainty=uncertainty, print_=True)
get_best_convert(all_rates, "rur", "bank", "ru", "tinkoff", "eur", "bank", "am", "yunibank", allow_uncertainty=uncertainty, print_=True)

get_best_convert(all_rates, "rur", "cash", "am", "",        "usd", "cash", "am", "",         allow_uncertainty=uncertainty, print_=True)
get_best_convert(all_rates, "rur", "bank", "ru", "tinkoff", "usd", "cash", "am", "",         allow_uncertainty=uncertainty, print_=True)
get_best_convert(all_rates, "rur", "bank", "ru", "tinkoff", "usd", "bank", "am", "yunibank", allow_uncertainty=uncertainty, print_=True)

get_best_convert(all_rates, "rur", "cash", "am", "",        "amd", "cash", "am", "",         allow_uncertainty=uncertainty, print_=True)
get_best_convert(all_rates, "rur", "bank", "ru", "tinkoff", "amd", "cash", "am", "",         allow_uncertainty=uncertainty, print_=True)
get_best_convert(all_rates, "rur", "bank", "ru", "tinkoff", "amd", "bank", "am", "yunibank", allow_uncertainty=uncertainty, print_=True)

get_best_convert(all_rates, "rur", "bank", "ru", "tinkoff", "amd", "cash", "am", "",         allow_uncertainty=uncertainty, print_=True, exclude_methods="broker")

# find_arbitrage(all_rates, print_=True)
