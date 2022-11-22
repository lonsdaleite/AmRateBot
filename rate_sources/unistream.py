import json
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from rate import add_rate
import log


def add_unistream(
        url="https://online.unistream.ru/card2cash/calculate?payout_type=cash&destination=ARM&amount=&currency="
            "&accepted_currency=RUB&profile=unistream",
            all_rates=None):
    for currency in ["RUB", "AMD", "USD", "EUR"]:
        try:
            amount = 1000
            if currency == "RUB":
                amount = 100000
            full_url = url.replace("&currency=", "&currency=" + currency).replace("&amount=", "&amount=" + str(amount))
            hdr = {'User-Agent': 'Mozilla/5.0'}
            req = Request(full_url, headers=hdr)
            page = urlopen(req)
            soup = BeautifulSoup(page, "lxml")
            # print(soup)

            json_str = soup.find_all("p")[0].text
            # print(json_str)
            json_parsed = json.loads(json_str)
            rate_value = json_parsed["fees"][0]["rate"]
            fee_value = json_parsed["fees"][0]["acceptedTotalFee"]
            input_value = json_parsed["fees"][0]["acceptedAmount"]
            final_rate_value = rate_value / (1 + fee_value / (input_value - fee_value))
            # print(final_rate_value)

            to_currency = currency.lower()
            if to_currency == "rub":
                to_currency = "rur"

            add_rate(all_rates, "rur", "bank", "ru", "", to_currency, "cash", "am", "", "unistream", final_rate_value, "to")
        except Exception as e:
            log.logger.error("Can not get Unistream rate for " + currency)
            log.logger.error(e)
