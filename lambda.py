import os
import time
from multiprocessing import Process, Pipe


def f(x,sleep_time,conn):
    start_time = time.time()
    cnt = 0
    while time.time() - start_time <sleep_time:
        cnt+=1
    conn.send(x)
    conn.close()

def multi(input_x,sleep_time):
    processes = []
    parent_connections = []

    for _ in range(os.cpu_count()):            
        parent_conn, child_conn = Pipe()
        parent_connections.append(parent_conn)
        process = Process(target=f, args=(input_x, sleep_time,child_conn))
        processes.append(process)

    _ = [process.start() for process in processes]
    _ = [process.join() for process in processes]

    ans = sum([parent_conn.recv() for parent_conn in parent_connections])

    return ans


if __name__ == '__main__':
    x = multi(1.1,1)
    print(x)
        

