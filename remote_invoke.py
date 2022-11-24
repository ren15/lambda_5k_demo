import time
import json
import aiohttp
import asyncio

from aws_lambda_url import url

async def invoke_lambda(url, payload):
    async with aiohttp.ClientSession() as session:
        headers = {"Content-Type": "application/json"}
        async with session.post(url,data=json.dumps(payload), headers=headers) as resp:
            return (await resp.json())['x']

async def main(payload,n):
    async with aiohttp.ClientSession() as _session:
        tasks = [asyncio.ensure_future(invoke_lambda(url, payload)) for _ in range(n)]
        ans = sum(await asyncio.gather(*tasks))
        print("core used: ",ans)

if __name__ == "__main__":
    t1 = time.time()

    payload = {"input_x": 1, "sleep_time": 1}
    n = 300
    print(payload,n)
    asyncio.run(main(payload,n))
    print("spent time: ", time.time() - t1)

