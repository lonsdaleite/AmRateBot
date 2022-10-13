import random

from bs4 import BeautifulSoup
import requests
import time
from rate import add_rate


def add_mir(url="https://mironline.ru/support/list/kursy_mir/", all_rates=None):
    page = requests.get(url)
    # print(page.status_code)
    result = None
    try_num = 0
    while result is None:
        if try_num > 0:
            print("WARN: Can not get MIR rate, retrying")
            time.sleep(random.uniform(5, 10))
        try_num += 1
        if try_num > 5:
            print("ERROR: Can not get MIR rate")
            break
        if page.status_code == 200:
            soup = BeautifulSoup(page.text, "lxml")
            # print(soup)

            rates = soup.find_all("tr")
            for rate in rates:
                currency = rate.findNext("p")
                if currency.text.strip() == "Армянский драм":
                    value = currency.findNext("p")
                    result = float(value.text.strip().replace(",", "."))
                    add_rate(all_rates, "rur", "tinkoff", "amd", "cash", "atm", result, "to")
                    break
        else:
            print("Warn: MIR status code: " + str(page.status_code))
            continue
