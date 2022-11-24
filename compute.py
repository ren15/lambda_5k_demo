from multiprocessing import Process, Pipe


def f(x, conn):
    cnt = 0
    while cnt < 30000000:
        cnt += 1
    conn.send(x)
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

    return sum([parent_conn.recv() for parent_conn in parent_connections])
