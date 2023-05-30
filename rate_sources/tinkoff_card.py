from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import json
import log
from rate import add_rate


def get_json_rate(url, from_currency, to_currency):
    try:
        hdr = {'User-Agent': 'Mozilla/5.0'}
        url += "?from=" + from_currency + "&to=" + to_currency
        req = Request(url, headers=hdr)
        page = urlopen(req)
        soup = BeautifulSoup(page, "lxml")
        # print(soup)

        return soup.text
    except Exception as e:
        log.logger.error(e)
        log.logger.error("Can not get Tinkoff broker rates")


def add_tinkoff_card(url="https://api.tinkoff.ru/v1/currency_rates", all_rates=None):
    rubamd_rate = get_json_rate(url, "RUB", "AMD")
    # print(rubamd_rate)

    if rubamd_rate is not None:
        rubamd_rate_json = json.loads(rubamd_rate)

        for rate in rubamd_rate_json["payload"]["rates"]:
            if rate["category"] == "DebitCardsTransfers":
                add_rate(all_rates, "rur", "bank", "ru", "tinkoff", "amd", "bank", "ru", "tinkoff", "convert",
                         float(rate["buy"]), "to")
                add_rate(all_rates, "amd", "bank", "ru", "tinkoff", "rur", "bank", "ru", "tinkoff", "convert",
                         float(rate["sell"]), "from")
            elif rate["category"] == "DebitCardsOperations":
                add_rate(all_rates, "rur", "bank", "ru", "tinkoff", "amd", "pos", "am", "", "pos",
                         float(rate["buy"]), "to")
    else:
        log.logger.error("Can not add Tinkoff card rates")
