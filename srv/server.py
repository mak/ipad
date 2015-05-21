import zmq
import threading,Queue

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
    last_hashes=[]
    while True:
        msg = Q.get()
        print msg
        
        if msg['hash'] in last_hashes: continue
        last_hashes.append(msg['hash'])
        del msg['hash']
        out_sock.send_json(msg)

        if len(last_hashes) > 500:
            last_hashes = last_hashes[-500:]
ts = threading.Thread(target=sender)
ts.start()

while True:
    try:
        ev = dict(poller.poll(500))
    except zmq.ZMQError as e:
        print '0MQ exc: %s'%`e`
        break
    
    if in_sock in ev:
        msg = in_sock.recv_json()
        Q.put(msg)
