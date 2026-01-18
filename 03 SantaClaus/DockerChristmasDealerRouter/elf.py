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
        print(f"Elf with id {eID} needs help", flush=True)
        dealer.send_multipart([b"", json.dumps({"type": "elf", "id": eID}).encode()])
        sent = True
    msg = dealer.recv_multipart()
    msg = json.loads(msg[0].decode())
    if msg.get("action", "") == "elves_help" and eID in msg.get("id", ""):
        dealer.send_multipart([b"", json.dumps({"type": "ackElf", "id": eID, "seqElf": msg.get("seqElf", "")}).encode()])
        time.sleep(5)
        sent = False
        continue