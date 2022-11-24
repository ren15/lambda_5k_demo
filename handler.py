import json
import os
import time
from multiprocessing import Process, Pipe

def f(x,iter_mul,conn):
    cnt = 0
    N = 30000000 * iter_mul
    while cnt < N:
        cnt+=1
    conn.send(x)
    conn.close()

def multi(input_x,iter_mul,threads):
    processes = []
    parent_connections = []

    for _ in range(threads):            
        parent_conn, child_conn = Pipe()
        parent_connections.append(parent_conn)
        process = Process(target=f, args=(input_x, iter_mul,child_conn))
        processes.append(process)

    _ = [process.start() for process in processes]
    _ = [process.join() for process in processes]

    ans = sum([parent_conn.recv() for parent_conn in parent_connections])

    return ans

def lambda_handler(event, context):
    body = json.loads(event['body'])
    x = multi(body['input_x'],body['iter_mul'],body['threads'])
    ans = {'x':x}
    return {
        'statusCode': 200,
        'body': json.dumps(ans)
    }
