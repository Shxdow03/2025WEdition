import random
import zmq
import time
import socket
import json

context = zmq.Context()

dealer = context.socket(zmq.DEALER)
eID = socket.gethostname()
dealer.connect("tcp://santa:2222")

sent = False

while True:
    if not sent:
        print(f"Elf with id {eID} needs help")
        dealer.send_multipart([b"", json.dumps({"type": "elf", "id": eID}).encode()])
        sent = True
    msg = dealer.recv_multipart()
    msg = json.loads(msg[0].decode())
    time.sleep(0.1)
    if msg["action"] == "elves_help" and eID in msg.get("id", ""):
        print(f"Helping elf with id {eID}")
        time.sleep(random.randint(3, 5))
        sent = False
        continue