# lambda_5k_demo

In `aws_lambda_url.py`

```python
url = "https://${YOUR_LAMBDA}.lambda-url.${YOUR_REGION}.on.aws/"
```

```bash
python local_invoke.py 1 1 1
python local_invoke.py 1 4 4
python local_invoke.py 1 20 4
python local_invoke.py 1 20 8

python remote_invoke.py 1 20
python remote_invoke.py 1 50
python remote_invoke.py 1 5000
python remote_invoke.py 1.1 5000
```