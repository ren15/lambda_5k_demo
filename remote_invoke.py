import sys
import time
import json
import aiohttp
import asyncio

from aws_lambda_url import url


async def invoke_lambda(url, data):
    async with aiohttp.ClientSession() as session:
        headers = {"Content-Type": "application/json"}
        while True:
            try:
                async with session.post(url, data=data, headers=headers) as resp:
                    return (await resp.json())["ans"]
            except Exception as e:
                print(e)
                continue


async def send_loop(payload, n):
    threads = payload["args"]["threads"]
    finished = 0
    tasks = []

    while finished < n:
        run_threads = min(n - finished, threads)
        if run_threads < threads:
            payload["args"]["threads"] = run_threads
        data = json.dumps(payload)
        tasks.append(asyncio.ensure_future(invoke_lambda(url, data)))
        finished += run_threads

    ans_list = await asyncio.gather(*tasks)

    ans = sum([i[0] for i in ans_list])
    metadata_list = [i[1] for i in ans_list]
    from local_invoke import print_cpuinfo

    print_cpuinfo(metadata_list)

    return ans


if __name__ == "__main__":
    t1 = time.time()

    payload = {
        "args": {
            "x": float(sys.argv[1]),
            "threads": 6,
        }
    }

    n = int(sys.argv[2])

    print(payload, f"n: {n}")
    with open("compute.py", "r") as f:
        code = f.read()
    payload["code"] = code

    ans = asyncio.run(send_loop(payload, n))
    print("ans: ", ans)

    print("Spent time: ", time.time() - t1)
