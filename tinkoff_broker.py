from bs4 import BeautifulSoup
import requests
from urllib.request import Request, urlopen
import re
from rate import add_rate


def get_currency(url):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(url, headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, "lxml")

    tmp_result = soup.find_all("div", {'class': re.compile('.*priceText.*')})[0]
    tmp_result = tmp_result.findNext("span", {'class': re.compile('.*money.*')})
    rate = re.sub("[^0-9.]", "", tmp_result.text.replace(",", "."))
    return rate


def add_tinkoff_broker(url="https://www.tinkoff.ru/invest/currencies/", all_rates=None, fee=0.003):
    usdrub_rate = get_currency(url + "USDRUB")
    eurrub_rate = get_currency(url + "EURRUB")
    # print(usdrub_rate, eurrub_rate)

    if usdrub_rate is not None and eurrub_rate is not None:
        add_rate(all_rates, "rur", "tinkoff", "usd", "tinkoff", "broker", float(usdrub_rate) * (1 + fee), "from")
        add_rate(all_rates, "rur", "tinkoff", "eur", "tinkoff", "broker", float(eurrub_rate) * (1 + fee), "from")
    else:
        print("ERROR: Can not add Tinkoff broker rates")
