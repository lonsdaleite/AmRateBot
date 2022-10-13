from rate import add_rate, get_best_convert
from rate_am import add_rate_am
from sas import add_sas
from mir import add_mir
from tinkoff_broker import add_tinkoff_broker

all_rates = []
add_sas(all_rates=all_rates)
add_mir(all_rates=all_rates)
add_tinkoff_broker(all_rates=all_rates)
add_rate_am(convert_type="cash", all_rates=all_rates)
add_rate_am(convert_type="non-cash", all_rates=all_rates)
for rate in all_rates:
    print(rate)
print()

# always
add_rate(all_rates, "rur", "tinkoff",  "rur", "cash",     "unistream", 1.017,  "from")
add_rate(all_rates, "rur", "tinkoff",  "rur", "yunibank", "transfer",  1,      "from")
add_rate(all_rates, "usd", "tinkoff",  "usd", "yunibank", "transfer",  1.005,  "from")
add_rate(all_rates, "eur", "tinkoff",  "eur", "yunibank", "transfer",  1.005,  "from")
add_rate(all_rates, "usd", "yunibank", "usd", "cash",     "bank",      1.02,   "from")
add_rate(all_rates, "eur", "yunibank", "eur", "cash",     "bank",      1.02,   "from")
add_rate(all_rates, "rur", "yunibank", "rur", "cash",     "bank",      1.02,   "from")
add_rate(all_rates, "amd", "yunibank", "amd", "cash",     "atm",       1,      "from")
add_rate(all_rates, "amd", "cash",     "amd", "yunibank", "bank",      1,      "from")
add_rate(all_rates, "usd", "cash",     "usd", "yunibank", "bank",      1,      "from")
add_rate(all_rates, "eur", "cash",     "eur", "yunibank", "bank",      1,      "from")

# add_rate(all_rates, "rur", "cash",     "amd", "cash",     "sas",       6.25,   "to")
# add_rate(all_rates, "rur", "tinkoff",  "amd", "cash",     "atm",       6.232,  "to")
# add_rate(all_rates, "usd", "yunibank", "amd", "yunibank", "convert",   400,    "to")
# add_rate(all_rates, "rur", "yunibank", "amd", "yunibank", "convert",   6,      "to")
# add_rate(all_rates, "amd", "cash",     "usd", "cash",     "sas",       413.5,  "from")
# add_rate(all_rates, "usd", "cash",     "amd", "cash",     "sas",       410,    "to")

# add_rate(all_rates, "rur", "tinkoff",  "amd", "cash",     "unistream", 0.16728,  "from") #!
# add_rate(all_rates, "rur", "tinkoff",  "usd", "cash",     "unistream", 67.156, "from") #!
# add_rate(all_rates, "rur", "tinkoff",  "usd", "tinkoff",  "broker",    63.41,  "from")
# add_rate(all_rates, "rur", "cash",     "usd", "cash",     "sas",       64.063, "from")

# get_best_convert(all_rates, "rur", "cash", "amd", "cash", allow_uncertainty=0.005, print_result=True)
# get_best_convert(all_rates, "rur", "tinkoff", "amd", "cash", allow_uncertainty=0.005, print_result=True)
get_best_convert(all_rates, "rur", "tinkoff", "amd", "yunibank", allow_uncertainty=0.006, print_result=True)
# get_best_convert(all_rates, "rur", "tinkoff", "usd", "cash", allow_uncertainty=0.005, print_result=True)
# get_best_convert(all_rates, "rur", "tinkoff", "eur", "cash", allow_uncertainty=0.005, print_result=True)
