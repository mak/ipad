
import cmd
import zmq
import json
import threading,Queue

import multiprocessing as m
from copy import deepcopy

from db import store_change,start_db

ctx = zmq.Context()
out_sock = ctx.socket(zmq.PUB)
out_sock.bind('tcp://*:1338')

in_sock = ctx.socket(zmq.SUB)
in_sock.setsockopt(zmq.SUBSCRIBE,'')
in_sock.bind('tcp://*:1337')

poller = zmq.Poller()
poller.register(in_sock,zmq.POLLIN)
Q = Queue.Queue()

def sender():
    start_db()
    last_hashes=[]
    while True:
        msg = Q.get()
        if msg=='quit': break
        print msg

        if msg['hash'] in last_hashes: continue
        last_hashes.append(msg['hash'])

        m = deepcopy(msg)
        if not store_change(m):
            continue
        
        del msg['hash']
        ssid = hex(msg['ssid']).lstrip('0x')
        del msg['ssid']

        print [ssid,json.dumps(msg)]
        out_sock.send_multipart([ssid,json.dumps(msg)])
        print 'sended'
        if len(last_hashes) > 500:
            last_hashes = last_hashes[-500:]
ts = threading.Thread(target=sender)
ts.start()

cmd_t=m.Process(target=cmd.run_server)
cmd_t.start()

try:
    while True:
        try:
            ev = dict(poller.poll(500))
        except zmq.ZMQError as e:
            print '0MQ exc: %s'%`e`
            break
    
        if in_sock in ev:
            msg = in_sock.recv_json()
            Q.put(msg)
except KeyboardInterrupt:
    print 'cc-break'
    Q.put('quit')
    cmd_t.terminate()
    
