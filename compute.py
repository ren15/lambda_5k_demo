from multiprocessing import Process, Pipe


def f_inner(x):
    cnt = 0
    while cnt < 32 * 1000 * 1000:
        cnt += 1
    return x


def f(x, conn):
    conn.send(f_inner(x))
    conn.close()


def multi(x, threads):
    processes = []
    parent_connections = []

    for _ in range(threads):
        parent_conn, child_conn = Pipe()
        parent_connections.append(parent_conn)
        process = Process(target=f, args=(x, child_conn))
        processes.append(process)

    [p.start() for p in processes]
    [p.join() for p in processes]

    metadata = {
        "cpuinfo": get_cpuinfo(),
    }

    return sum([parent_conn.recv() for parent_conn in parent_connections]), metadata


def get_cpuinfo():
    try:
        with open("/proc/cpuinfo") as f:
            cpuinfo = f.read()
        model_name = (
            cpuinfo.split("model name")[1].split(": ")[1].split("\n")[0].strip()
        )
        flags = cpuinfo.split("flags")[1].split(": ")[1].split("\n")[0].strip()
        return f"{model_name}"
    except Exception as e:
        print(e)
        return "Unknown"
