import yfinance
import pandas as pd
import bs4
import requests
import time


def get_stocks(count: int):

    headers = {
        "user-agent": "curl/7.55.1",
        "referer": "https://finance.yahoo.com/",
    }
    url = "https://finance.yahoo.com/most-active?offset=0&count={}".format(count)
    res = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    for td in soup.find_all("td", {"aria-label": "Symbol"}):
        for link in td.find_all("a", {"data-test": "quoteLink"}):
            symbol = str(link.next)
            yield symbol


def get_prices(symbol):

    ticker = yfinance.Ticker(symbol)
    tradingday_list = [
        i.strftime("%Y-%m-%d")
        for i in ticker.history(interval="1d", start="2022-01-01").index.to_list()
    ][-20:]

    data_list = []
    for i in range(len(tradingday_list) - 1):
        start = tradingday_list[i]
        end = tradingday_list[i + 1]
        data = ticker.history(start=start, end=end, interval="1m")
        data_list.append(data)
    data = pd.concat(data_list)

    midprice = (data["High"] + data["Low"]) / 2
    vwap = (midprice * data["Volume"]).sum() / data["Volume"].sum()

    size_mb = data.memory_usage(index=True).sum() / 1024**2

    return symbol, vwap, size_mb


def run():
    tickers = list(get_stocks(5))

    ts = time.time()
    ans_list = []
    for ticker in tickers:
        ans_list.append(get_prices(ticker))

    max_value = max(ans_list, key=lambda x: x[1])
    print(max_value)
    print(f"Time taken: {time.time() - ts}")


if __name__ == "__main__":
    run()
