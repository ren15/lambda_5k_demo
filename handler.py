import json
import sys


def lambda_handler(event, context):
    body = json.loads(event["body"])
    code = body["code"]
    with open("/tmp/compute.py", "w") as f:
        f.write(code)

    sys.path.append("/tmp")
    from compute import multi

    try:
        x = multi(**body["args"])
        ans = {"ans": x}
        return {"statusCode": 200, "body": json.dumps(ans)}
    except Exception as e:
        print(e)
        return {"statusCode": 400}
