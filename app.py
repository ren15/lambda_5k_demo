import json
import sys

import yfinance
import pandas as pd
import bs4
import requests


def handler(event, context):
    body = json.loads(event["body"])
    code = body["code"]
    with open("/tmp/fetch_stock.py", "w") as f:
        f.write(code)

    sys.path.append("/tmp")
    from fetch_stock import get_prices

    try:
        msg = {"ans": get_prices(**body["args"])}
        return {"statusCode": 200, "body": json.dumps(msg)}
    except Exception as e:
        print(e)
        return {"statusCode": 400}
