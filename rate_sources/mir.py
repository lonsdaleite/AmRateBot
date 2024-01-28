import random
import time
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from rate import add_rate
import log
import io
import re
from PyPDF2 import PdfReader


def add_mir(url="https://privetmir.ru/upload/FX_rate_Mir/FX_rate_Mir.pdf", all_rates=None):
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
            # Read the PDF file with io.BytesIO
            file = io.BytesIO(page.read())
            pdf = PdfReader(file)

            # Get number of pages in the PDF
            num_pages = len(pdf.pages)

            # Iterate through each page and print the content
            for page in range(num_pages):
                text = pdf.pages[page].extract_text()
                if "Армянский драм" in text:
                    # print(text)
                    result = float(re.sub(r"[^\\0]*Армянский драм ([0-9]*),([0-9]*)[^◕]+", "\\1.\\2", text))
                    add_rate(all_rates, "rur", "bank", "ru", "", "amd", "cash", "am", "", "atm", result, "from")
                    # print(result)
                    break
    except Exception as e:
        log.logger.error(e)
        log.logger.error("Can not get MIR rates")
