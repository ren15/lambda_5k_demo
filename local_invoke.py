import time
import sys
import concurrent.futures

from fetch_stock import get_stocks, get_prices, reduce_fn, filter_fn


def multi(stock_list, threads):
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        future_list = []
        for stock in stock_list:
            future = executor.submit(get_prices, stock)
            future_list.append(future)
    return [i.result() for i in future_list]


def invoke_local(stock_list, threads):
    ans_list = multi(stock_list, threads)
    filtered = list(filter(filter_fn, ans_list))
    ret = reduce_fn(filtered)
    print("ans: ", ret)


if __name__ == "__main__":
    t1 = time.time()

    n = int(sys.argv[1])
    threads = int(sys.argv[2])
    print(f"stock num: {n},threads: {threads}")

    stock_list = list(get_stocks(n))
    invoke_local(stock_list, threads)

    print("Spent time: ", time.time() - t1)
