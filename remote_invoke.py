import time
import json
import aiohttp
import asyncio
import sys

from aws_lambda_url import url

async def invoke_lambda(url, payload):
    async with aiohttp.ClientSession() as session:
        headers = {"Content-Type": "application/json"}
        data = json.dumps(payload)
        while True:
            try:
                async with session.post(url,data=data, headers=headers) as resp:
                    return (await resp.json())['x']
            except:
                continue


async def send_loop(payload,n):
    threads = 6
    finished = 0
    tasks = []

    while finished < n:
        run_threads = min(n-finished,threads)
        if run_threads < threads:
            payload= payload.copy()
            payload['threads'] = run_threads
        tasks.append(asyncio.ensure_future(invoke_lambda(url, payload)))
        finished += run_threads
    ans = sum(await asyncio.gather(*tasks))
    print("ans: ",ans)

if __name__ == "__main__":
    t1 = time.time()

    payload = {"input_x": float(sys.argv[1]), "iter_mul": float(sys.argv[2]),"threads":6}

    n= int(sys.argv[3])

    print(payload,f"n: {n}")

    asyncio.run(send_loop(payload,n))

    print("Spent time: ", time.time() - t1)
