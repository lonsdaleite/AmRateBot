from bs4 import BeautifulSoup
import requests
import re
from rate import add_rate


def add_rate_am(url="https://rate.am/en/armenian-dram-exchange-rates/banks/", convert_type="cash", all_rates=None):
    page = requests.get(url + convert_type)
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, "lxml")

        banks = soup.find_all("tr", {'id': re.compile('.*-.*')})
        for bank in banks:
            name = bank.findNext("img").get("alt").lower()
            rate_type = convert_type
            method = name
            if convert_type != "cash":
                # Just for now
                if name != "yunibank":
                    continue
                rate_type = name
                method = "convert"
            pos = bank.findNext("td", class_="date")
            for tmp_rate in [
                ["usd", "amd", "to"],
                ["amd", "usd", "from"],
                ["eur", "amd", "to"],
                ["amd", "eur", "from"],
                ["rur", "amd", "to"],
                ["amd", "rur", "from"]
            ]:
                pos = pos.findNext("td")
                if pos.text is not None and pos.text != "":
                    add_rate(all_rates, tmp_rate[0], rate_type, tmp_rate[1], rate_type, method,
                             float(pos.text), tmp_rate[2])
    else:
        print("ERROR: rate.am status code: " + str(page.status_code))
