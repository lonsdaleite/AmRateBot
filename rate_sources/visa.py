import time

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import json
import log
from rate import add_rate
import datetime


def get_json_rate(dt, url, from_curr, to_curr, fee):
    try:
        hdr = {'User-Agent': 'Mozilla/5.0'}
        url += "&fee=" + str(fee) + "&utcConvertedDate=" + dt + "&exchangedate=" + dt + "&fromCurr=" + from_curr + "&toCurr=" + to_curr + ""
        # print(url)
        req = Request(url, headers=hdr)
        page = urlopen(req)
        soup = BeautifulSoup(page, "lxml")
        # print(soup)

        return soup.text
    except Exception as e:
        log.logger.error(e)
        log.logger.error("Can not get Visa rates")
        return None


def add_day(dt_str, days):
    dt = datetime.datetime.strptime(dt_str, "%m%%2F%d%%2F%Y")
    dt += datetime.timedelta(days=days)
    return dt.strftime("%m%%2F%d%%2F%Y")


def add_visa(url="https://usa.visa.com/cmsapi/fx/rates?amount=1", from_curr="AMD", to_curr="RSD",
             fee=0.5, bank="ardshinbank", bank_cash_fee=0.015, all_rates=None):
    dt = datetime.datetime.now().strftime("%m%%2F%d%%2F%Y")
    dt_min = add_day(dt, -10)
    full_rate = get_json_rate(dt, url, from_curr, to_curr, fee)
    # print(full_rate)

    while full_rate is None and dt > dt_min:
        dt = add_day(dt, -1)
        time.sleep(0.5)
        full_rate = get_json_rate(dt, url, from_curr, to_curr, fee)

    if full_rate is not None:
        rate = json.loads(full_rate)

        amd_rsd_rate = float(rate["fxRateWithAdditionalFee"])

        # Country am is a workaround
        add_rate(all_rates, from_curr.lower(), "bank", "am", bank, to_curr.lower(), "pos", "am", "", "pos",
                 amd_rsd_rate, "from")
        if bank_cash_fee is not None:
            add_rate(all_rates, from_curr.lower(), "bank", "am", bank, to_curr.lower(), "cash", "am", "", "atm",
                     amd_rsd_rate * (1 + bank_cash_fee), "from")
    else:
        log.logger.error("Can not add Visa rates")
