import random
import time
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from rate import add_rate
import log


def add_mir(url="https://mironline.ru/support/list/kursy_mir/", all_rates=None):
    try:
        # page = requests.get(url)
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(url, headers=hdr)
        page = urlopen(req)
        # print(page.status_code)
        result = None
        try_num = 0
        while result is None:
            if try_num > 0:
                log.logger.warn("Can not get MIR rate, retrying")
                time.sleep(random.uniform(5, 10))
            try_num += 1
            if try_num > 5:
                log.logger.error("Can not get MIR rate")
                break
            soup = BeautifulSoup(page, "lxml")
            # print(soup)
            rates = soup.find_all("tr")
            if len(rates) == 0:
                continue

            for rate in rates:
                currency = rate.findNext("p")
                if currency.text.strip() == "Армянский драм":
                    value = currency.findNext("p")
                    result = float(value.text.strip().replace(",", "."))
                    add_rate(all_rates, "rur", "bank", "ru", "", "amd", "cash", "am", "", "atm", result, "to")
                    break
    except Exception as e:
        log.logger.error(e)
        log.logger.error("Can not get MIR rates")
