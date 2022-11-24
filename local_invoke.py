import time

from handler import multi


def local_invoke(payload,n):
    ans = sum([multi(payload['input_x'],payload['sleep_time']) for _ in range(n)])
    print("ans: ",ans)

if __name__ == "__main__":
    t1 = time.time()

    payload = {"input_x": 1, "sleep_time": 1}
    n = 5
    print(payload,n)
    local_invoke(payload,n)
    print("spent time: ", time.time() - t1)