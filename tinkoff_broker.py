from bs4 import BeautifulSoup
import requests
import re
from rate import add_rate


def add_tinkoff_broker(url="https://www.tinkoff.ru/invest/currencies/", all_rates=None, fee=0.00025):
    page = requests.get(url)
    usdrub_rate = None
    eurrub_rate = None
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, "lxml")
        # print(soup)

        usdrub = soup.find_all("a", {'href': re.compile('.*USDRUB.*')})[0]
        usdrub = usdrub.findNext("span", {'class': re.compile('.*money.*')})
        usdrub_rate = re.sub("[^0-9.]", "", usdrub.text.replace(",", "."))

        eurrub = soup.find_all("a", {'href': re.compile('.*EURRUB.*')})[0]
        eurrub = eurrub.findNext("span", {'class': re.compile('.*money.*')})
        eurrub_rate = re.sub("[^0-9.]", "", eurrub.text.replace(",", "."))
    else:
        print("ERROR: Tinkoff broker status code: " + str(page.status_code))

    if usdrub_rate is not None and eurrub_rate is not None:
        add_rate(all_rates, "rur", "tinkoff", "usd", "tinkoff", "broker", float(usdrub_rate) * (1 + fee), "from")
        add_rate(all_rates, "rur", "tinkoff", "eur", "tinkoff", "broker", float(eurrub_rate) * (1 + fee), "from")
    else:
        print("ERROR: Can not add Tinkoff broker rates")
