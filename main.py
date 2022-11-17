from add_rates import add_all_rates
from rate import get_best_convert, format_rates

all_rates = add_all_rates()
# print(all_rates)
format_rates(all_rates, print_=True)
uncertainty = 0.003

converts = [["rur", "cash", "am", "",        "eur", "cash", "am", "",         None],
            ["rur", "bank", "ru", "tinkoff", "eur", "cash", "am", "",         None],
            ["rur", "bank", "ru", "tinkoff", "eur", "bank", "am", "yunibank", None],
            ["rur", "cash", "am", "",        "usd", "cash", "am", "",         None],
            ["rur", "bank", "ru", "tinkoff", "usd", "cash", "am", "",         None],
            ["rur", "bank", "ru", "tinkoff", "usd", "bank", "am", "yunibank", None],
            ["rur", "cash", "am", "",        "amd", "cash", "am", "",         None],
            ["rur", "bank", "ru", "tinkoff", "amd", "cash", "am", "",         None],
            ["rur", "bank", "ru", "tinkoff", "amd", "bank", "am", "yunibank", None],
            ["rur", "bank", "ru", "tinkoff", "amd", "cash", "am", "",         ["broker"]]]

for conv in converts:
    get_best_convert(all_rates, conv[0], conv[1], conv[2], conv[3], conv[4], conv[5], conv[6], conv[7],
                     allow_uncertainty=uncertainty, print_=True, exclude_methods=conv[8])

# find_arbitrage(all_rates, print_=True)
