import sys
import time
import json
import aiohttp
import asyncio

from aws_lambda_url import url

from fetch_stock import get_stocks, reduce_fn, filter_fn


async def invoke_lambda(url, data):
    async with aiohttp.ClientSession() as session:
        headers = {"Content-Type": "application/json"}
        while True:
            try:
                async with session.post(url, data=data, headers=headers) as resp:
                    return (await resp.json())["ans"]
            except Exception as e:
                print(e)
                break


async def send_loop(code_str, n):
    stock_list = get_stocks(n)

    tasks = []

    for symbol in stock_list:
        payload = {
            "code": code_str,
            "args": {"symbol": symbol},
        }
        data = json.dumps(payload)
        tasks.append(asyncio.ensure_future(invoke_lambda(url, data)))

    ans_list = await asyncio.gather(*tasks)
    filtered = list(filter(filter_fn, ans_list))
    ret = reduce_fn(filtered)
    print("ans: ", ret)


if __name__ == "__main__":
    t1 = time.time()

    n = int(sys.argv[1])

    print(f"stock num: {n}")
    with open("fetch_stock.py", "r") as f:
        code_str = f.read()

    asyncio.run(send_loop(code_str, n))

    print("Spent time: ", time.time() - t1)
