import time
import sys

from handler import multi


def local_invoke(payload,n,threads):
    finished = 0
    ans = 0
    while finished < n:
        run_threads = min(n-finished,threads)
        ans+=multi(payload['input_x'],payload['iter_mul'],run_threads)
        finished += run_threads
    print("ans: ",ans)

if __name__ == "__main__":
    t1 = time.time()

    payload = {"input_x": float(sys.argv[1]), "iter_mul": int(sys.argv[2])}
    n,threads = int(sys.argv[3]),int(sys.argv[4])
    print(payload,f"n: {n}, threads: {threads}")
    local_invoke(payload,n,threads)

    print("Spent time: ", time.time() - t1)