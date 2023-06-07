import time

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import json
import log
from rate import add_rate
import datetime


def get_json_rate(dt, url):
    try:
        hdr = {'User-Agent': 'Mozilla/5.0'}
        url += dt + ".json"
        req = Request(url, headers=hdr)
        page = urlopen(req)
        soup = BeautifulSoup(page, "lxml")
        # print(soup)

        return soup.text
    except Exception as e:
        log.logger.error(e)
        log.logger.error("Can not get UnionPay rates")
        return None


def add_day(dt_str, days):
    dt = datetime.datetime.strptime(dt_str, "%Y%m%d")
    dt += datetime.timedelta(days=days)
    return dt.strftime("%Y%m%d")


def add_unionpay(url="https://www.unionpayintl.com/upload/jfimg/", trans_cur="RSD", base_cur="USD", all_rates=None):
    dt = datetime.datetime.now().strftime("%Y%m%d")
    dt_min = add_day(dt, -10)
    full_rate = get_json_rate(dt, url)

    while full_rate is None and dt > dt_min:
        dt = add_day(dt, -1)
        time.sleep(0.5)
        full_rate = get_json_rate(dt, url)

    if full_rate is not None:
        full_rate_json = json.loads(full_rate)

        for rate in full_rate_json["exchangeRateJson"]:
            if rate["transCur"] == trans_cur and rate["baseCur"] == base_cur:
                # Country am is a workaround
                add_rate(all_rates, "usd", "bank", "ru", "tinkoff", "rsd", "pos", "am", "", "pos",
                         float(rate["rateData"]), "from")
                add_rate(all_rates, "usd", "bank", "ru", "tinkoff", "rsd", "cash", "am", "", "atm",
                         float(rate["rateData"]), "from")
                break
    else:
        log.logger.error("Can not add UnionPay rates")

