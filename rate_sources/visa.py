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


def get_visa_rate(url="https://usa.visa.com/cmsapi/fx/rates?amount=1", from_curr="AMD", to_curr="RSD",
                  convert_fee=0.5):
    dt = datetime.datetime.now().strftime("%m%%2F%d%%2F%Y")
    dt_min = add_day(dt, -10)
    full_rate = get_json_rate(dt, url, from_curr, to_curr, convert_fee)
    # print(full_rate)

    while full_rate is None and dt > dt_min:
        dt = add_day(dt, -1)
        time.sleep(0.5)
        full_rate = get_json_rate(dt, url, from_curr, to_curr, convert_fee)

    rate_with_fee = None
    if full_rate is not None:
        rate = json.loads(full_rate)
        rate_with_fee = float(rate["fxRateWithAdditionalFee"])
    else:
        log.logger.error("Can not get Visa rates")
    return rate_with_fee

def add_visa(all_rates=None):
    # ArdshinBank
    ardshin_convert_fee = 0.5
    ardshin_cash_fee = 0.015
    ardshin_c2c_fee = 0.01

    ardshin_amd_rsd_rate = get_visa_rate(convert_fee=ardshin_convert_fee, from_curr="AMD", to_curr="RSD")
    ardshin_eur_rsd_rate = get_visa_rate(convert_fee=ardshin_convert_fee, from_curr="EUR", to_curr="RSD")
    ardshin_amd_eur_rate = get_visa_rate(convert_fee=ardshin_convert_fee, from_curr="AMD", to_curr="EUR")

    add_rate(all_rates, "amd", "bank", "am", "ardshinbank", "rsd", "pos", "rs", "", "pos", ardshin_amd_rsd_rate, "from")
    add_rate(all_rates, "eur", "bank", "am", "ardshinbank", "rsd", "pos", "rs", "", "pos", ardshin_eur_rsd_rate, "from")

    add_rate(all_rates, "amd", "bank", "am", "ardshinbank", "rsd", "cash", "rs", "", "atm",
             ardshin_amd_rsd_rate * (1 + ardshin_cash_fee), "from")
    add_rate(all_rates, "eur", "bank", "am", "ardshinbank", "rsd", "cash", "rs", "", "atm",
             ardshin_eur_rsd_rate * (1 + ardshin_cash_fee), "from")

    add_rate(all_rates, "amd", "bank", "am", "ardshinbank", "eur", "bank", "rs", "", "c2c",
             ardshin_amd_eur_rate * (1 + ardshin_c2c_fee), "from")

    # Unibank
    unibank_convert_fee = 2
    unibank_cash_fee = 0.013

    unibank_amd_rsd_rate = get_visa_rate(convert_fee=unibank_convert_fee, from_curr="AMD", to_curr="RSD")
    unibank_usd_rsd_rate = get_visa_rate(convert_fee=unibank_convert_fee, from_curr="USD", to_curr="RSD")

    add_rate(all_rates, "amd", "bank", "am", "yunibank", "rsd", "pos", "rs", "", "pos", unibank_amd_rsd_rate, "from")
    add_rate(all_rates, "usd", "bank", "am", "yunibank", "rsd", "pos", "rs", "", "pos", unibank_usd_rsd_rate, "from")

    add_rate(all_rates, "amd", "bank", "am", "yunibank", "rsd", "cash", "rs", "", "atm",
             unibank_amd_rsd_rate * (1 + unibank_cash_fee), "from")
    add_rate(all_rates, "usd", "bank", "am", "yunibank", "rsd", "cash", "rs", "", "atm",
             unibank_usd_rsd_rate * (1 + unibank_cash_fee), "from")
