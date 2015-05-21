import zmq

ctx = zmq.Context()
out_sock = ctx.socket(zmq.PUB)
out_sock.bind('tcp://*:1338')

in_sock = ctx.socket(zmq.SUB)
in_sock.setsockopt(zmq.SUBSCRIBE,'')
in_sock.bind('tcp://*:1337')

poller = zmq.Poller()
poller.register(in_sock,zmq.POLLIN)

while True:
    try:
        ev = dict(poller.poll(500))
    except zmq.ZMQError as e:
        print '0MQ exc: %s'%`e`
        break
    
    if in_sock in ev:
        msg = in_sock.recv_json()
        print msg
        print in_sock.getsockopt(zmq.IDENTITY)
        out_sock.send_json(msg)
