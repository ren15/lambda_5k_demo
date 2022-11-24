import requests
import json

from aws_lambda_url import url


def invoke_lambda(url, payload):
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    return response.json()

if __name__ == "__main__":
    payload = {"input_x": 1.1, "sleep_time": 1}
    response = invoke_lambda(url, payload)
    print(response)

