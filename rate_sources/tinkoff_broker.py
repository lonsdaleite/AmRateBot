from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import log
from rate import add_rate


def get_currency(url):
    try:
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(url, headers=hdr)
        page = urlopen(req)
        soup = BeautifulSoup(page, "lxml")
        # print(soup)

        tmp_result = soup.find_all("div", {'class': re.compile('.*priceText.*')})[0]
        # log.logger.debug(tmp_result)
        tmp_result = tmp_result.findNext("span", {'class': re.compile('.*money.*')})
        # log.logger.debug(tmp_result)
        rate = re.sub("[^0-9.]", "", tmp_result.text.replace(",", "."))
        # log.logger.debug(rate)
        return rate
    except Exception as e:
        log.logger.error(e)
        log.logger.error("Can not get Tinkoff broker rates")


def add_tinkoff_broker(url="https://www.tinkoff.ru/invest/currencies/", all_rates=None, fee=0.004):
    usdrub_rate = get_currency(url + "USDRUB")
    eurrub_rate = get_currency(url + "EURRUB")
    # print(usdrub_rate, eurrub_rate)

    if usdrub_rate is not None and eurrub_rate is not None:
        add_rate(all_rates, "rur", "bank", "ru", "tinkoff", "usd", "bank", "ru", "tinkoff", "broker",
                 float(usdrub_rate) * (1 + fee), "from")
        add_rate(all_rates, "rur", "bank", "ru", "tinkoff", "eur", "bank", "ru", "tinkoff", "broker",
                 float(eurrub_rate) * (1 + fee), "from")
    else:
        log.logger.error("Can not add Tinkoff broker rates")
