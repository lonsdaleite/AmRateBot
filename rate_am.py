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
            pos = pos.findNext("td")
            add_rate(all_rates, "usd", rate_type, "amd", rate_type, method, float(pos.text), "to")
            pos = pos.findNext("td")
            add_rate(all_rates, "amd", rate_type, "usd", rate_type, method, float(pos.text), "from")
            pos = pos.findNext("td")
            add_rate(all_rates, "eur", rate_type, "amd", rate_type, method, float(pos.text), "to")
            pos = pos.findNext("td")
            add_rate(all_rates, "amd", rate_type, "eur", rate_type, method, float(pos.text), "from")
            pos = pos.findNext("td")
            add_rate(all_rates, "rur", rate_type, "amd", rate_type, method, float(pos.text), "to")
            pos = pos.findNext("td")
            add_rate(all_rates, "amd", rate_type, "rur", rate_type, method, float(pos.text), "from")
    else:
        print("ERROR: rate.am status code: " + str(page.status_code))
