import time
import sys

from compute import multi


def invoke_local(payload, n):
    threads = payload["args"]["threads"]
    finished = 0
    ans = 0
    while finished < n:
        run_threads = min(n - finished, threads)
        if run_threads < threads:
            payload = payload.copy()
            payload["args"]["threads"] = run_threads
        ans += multi(**payload["args"])
        finished += run_threads
    print("ans: ", ans)


if __name__ == "__main__":
    t1 = time.time()

    n = int(sys.argv[2])
    payload = {"args": {"x": float(sys.argv[1]), "threads": int(sys.argv[3])}}

    print(payload, f"n: {n}")
    invoke_local(payload, n)

    print("Spent time: ", time.time() - t1)
