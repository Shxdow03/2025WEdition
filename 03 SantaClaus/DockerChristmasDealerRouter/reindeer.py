import random
import zmq
import socket
import time
import json

context = zmq.Context()
rID = socket.gethostname()
dealer = context.socket(zmq.DEALER)
dealer.connect("tcp://santa:2222")

sent = False

while True:
    if not sent:
        print(f"Reindeer with id {rID} arrived from the south pole.", flush=True)
        dealer.send_multipart([b"",json.dumps({"type": "reindeer", "id": rID}).encode()])
        sent = True
    msg = dealer.recv_multipart()
    msg = json.loads(msg[0].decode())
    if msg["action"] == "reindeer_go" and rID in msg.get("id", ""):
        dealer.send_multipart([b"",json.dumps({"type": "ackReindeer", "id": rID, "seqReindeer": msg.get("seqReindeer", "")}).encode()])
        time.sleep(5)
        sent = False
        continue
