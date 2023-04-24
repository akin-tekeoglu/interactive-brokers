import typing
import requests
from bs4 import BeautifulSoup
import csv

FILTER="cap_smallunder,sh_curvol_o1000,sh_price_u10,sh_relvol_o1.5"

def get_finwiz_screening_page(offset: int) -> str:
    response = requests.get(
        "https://finviz.com/screener.ashx",
        params={
            "f": FILTER,
            "r": offset,
        },
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        },
    )
    return response.text


def get_total_ticker_count(html: str) -> int:
    soup = BeautifulSoup(html, "html.parser")
    td = soup.find("td", {"class": "count-text"})
    return int(td.text.replace("Total:", "").replace("#1", "").strip())


def get_tickers(html: str) -> typing.List:
    soup = BeautifulSoup(html, "html.parser")
    tds = soup.select("td.screener-body-table-nw a.screener-link-primary")
    return list(map(lambda td: td.text, tds))


if __name__ == "__main__":
    offset = 1
    first_page = get_finwiz_screening_page(offset)
    count = get_total_ticker_count(first_page)
    offsets = [c * 20 + 1 for c in range(1, count // 20 + 1)]
    tickers = get_tickers(first_page)
    for offset in offsets:
        page = get_finwiz_screening_page(offset)
        tickers.extend(get_tickers(page))
    with open('tickers.csv', 'w') as file:
        writer = csv.writer(file)
        for ticker in tickers:
            writer.writerow(["SYM",ticker,"SMART/AMEX"])