from bs4 import BeautifulSoup
import requests
from rate import add_rate
import log


def add_sas(url="https://www.sas.am/en/appfood/personal/calculator/", all_rates=None):
    try:
        page = requests.get(url)
        if page.status_code == 200:
            soup = BeautifulSoup(page.text, "lxml")
            # print(soup)

            rates = soup.find_all("div", class_="exchange-table__row")
            total = 0
            for rate in rates:
                pos = rate.findNext("span", class_="exchange-table__cell-content")
                if pos.text in ["USD", "EUR", "RUR"]:
                    total += 1
                    currency = pos.text.lower()
                    pos = pos.findNext("span", class_="exchange-table__cell-content")
                    add_rate(all_rates, currency, "cash", "am", "", "amd", "cash", "am", "", "sas", float(pos.text), "to")
                    pos = pos.findNext("span", class_="exchange-table__cell-content")
                    add_rate(all_rates, "amd", "cash", "am", "", currency, "cash", "am", "", "sas", float(pos.text), "from")
                if total == 3:
                    break
        else:
            log.logger.error("SAS status code: " + str(page.status_code))
    except Exception as e:
        log.logger.error(e)
        log.logger.error("Can not get SAS rates")
