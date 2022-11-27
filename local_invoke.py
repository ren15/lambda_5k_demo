import time
import sys

from compute import multi


def invoke_local(payload, n):
    threads = payload["args"]["threads"]
    finished = 0
    ans = 0
    metadata_list = []
    while finished < n:
        run_threads = min(n - finished, threads)
        if run_threads < threads:
            payload = payload.copy()
            payload["args"]["threads"] = run_threads
        ret, metadata = multi(**payload["args"])
        ans += ret
        metadata_list.append(metadata)

        finished += run_threads
    print("ans: ", ans)
    print_cpuinfo(metadata_list)


def print_cpuinfo(metadata_list):
    cpuinfo_count = {}
    for i in metadata_list:
        if i["cpuinfo"] not in cpuinfo_count:
            cpuinfo_count[i["cpuinfo"]] = 1
        else:
            cpuinfo_count[i["cpuinfo"]] += 1
    print(cpuinfo_count)


if __name__ == "__main__":
    t1 = time.time()

    n = int(sys.argv[2])
    payload = {"args": {"x": float(sys.argv[1]), "threads": int(sys.argv[3])}}

    print(payload, f"n: {n}")
    invoke_local(payload, n)

    print("Spent time: ", time.time() - t1)
