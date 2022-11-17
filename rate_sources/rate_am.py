from bs4 import BeautifulSoup
import requests
import re
from rate import add_rate
import log


def add_rate_am(url="https://rate.am/en/armenian-dram-exchange-rates/banks/", convert_type="cash", all_rates=None):
    page = requests.get(url + convert_type)
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, "lxml")

        banks = soup.find_all("tr", {'id': re.compile('.*-.*')})
        for bank in banks:
            bank_name = bank.findNext("img").get("alt").lower()
            if convert_type == "cash":
                rate_type = "cash"
                method = bank_name
                bank_name = ""
            else:
                # Just for now
                if bank_name not in ["yunibank", "aydi-bank"]:
                    continue
                rate_type = "bank"
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
                    add_rate(all_rates,
                             tmp_rate[0], rate_type, "am", bank_name,
                             tmp_rate[1], rate_type, "am", bank_name,
                             method, float(pos.text), tmp_rate[2])
    else:
        log.logger.error("rate.am status code: " + str(page.status_code))
