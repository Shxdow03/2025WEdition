import random
import zmq
import time
import socket

context = zmq.Context()

push = context.socket(zmq.PUSH)
push.connect("tcp://santa:2222")

sub = context.socket(zmq.SUB)
sub.connect("tcp://santa:2223")
sub.setsockopt_string(zmq.SUBSCRIBE, "")

eID = socket.gethostname()
sent = False

while True:
    if not sent:
        print(f"Elf with id {eID} needs help")
        push.send_json({"type": "elf", "id": eID})
        sent = True
    msg = sub.recv_json()
    time.sleep(0.1)
    if msg["action"] == "elves_help" and eID in msg.get("elves", []):
        print(f"Helping elf with id {eID}")
        time.sleep(random.randint(5,8))
        sent = False
        continue