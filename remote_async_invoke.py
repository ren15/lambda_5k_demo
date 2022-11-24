import json
import aiohttp
import asyncio

from aws_lambda_url import url


async def main():
    payload = {"input_x": 1.1, "sleep_time": 1}
    async with aiohttp.ClientSession() as session:
        headers = {"Content-Type": "application/json"}
        async with session.post(url,data=json.dumps(payload), headers=headers) as resp:
            rsp = await resp.json()
            print(rsp)

asyncio.run(main())
