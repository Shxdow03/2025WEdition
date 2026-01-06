import random
import zmq
import socket
import time

context = zmq.Context()

push = context.socket(zmq.PUSH)
push.connect("tcp://santa:2222")

sub = context.socket(zmq.SUB)
sub.connect("tcp://santa:2223")
sub.setsockopt_string(zmq.SUBSCRIBE, "")

rID = socket.gethostname()
sent = False

while True:
    if not sent:
        print(f"Reindeer with id {rID} arrived from the south pole.")
        push.send_json({"type": "reindeer", "id": rID})
        sent = True
    msg = sub.recv_json()
    time.sleep(0.1)
    if msg["action"] == "reindeer_go" and rID in msg.get("reindeers", []):
        print(f"Reindeer with {rID} was succesfully hitched.")
        time.sleep(random.randint(5,8))
        sent = False
        continue
