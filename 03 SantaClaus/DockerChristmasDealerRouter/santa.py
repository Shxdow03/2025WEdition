import zmq
import time
import json
from collections import deque

context = zmq.Context()

router = context.socket(zmq.ROUTER)
router.bind("tcp://*:2222")

reindeers = deque()
elves = deque()
seq = 0
processingReindeers = False
processingElves = False
ackReindeer = 0
ackElf = 0

def nextSeq():
    global seq
    seq += 1
    return seq

while True:
    id_, empty, msg = router.recv_multipart()
    msg = json.loads(msg.decode())

    if msg["type"] == "reindeer":
        reindeers.append((id_, msg["id"]))
        print(f"Number of reindeers that have arrived from the south pole: {len(reindeers)}/9 (Reindeer: {msg["id"]})")
    elif msg["type"] == "elf":
        elves.append((id_, msg["id"]))
        print(f"Number of elves that request help: {len(elves)}/3 (Elf: {msg["id"]})")
    elif msg["type"] == "ackReindeer":
        ackReindeer += 1
        print(f"{msg.get("seqReindeer", "")} Reindeer with {msg.get("id", "")} was succesfully hitched.")
    elif msg["type"] == "ackElf":
        ackElf += 1
        print(f"{msg.get("seqElf")}: Helping elf with id {msg.get("id", "")}")

    if not processingReindeers and len(reindeers) >= 9:
        processingReindeers = True
        ackReindeer = 0
        print(f"All reindeers arrived, preparing sleigh for reindeers: {list(reindeers)[:9]}")
        for _ in range(9):
            _id, rID = reindeers.popleft()
            router.send_multipart([_id, json.dumps({"action": "reindeer_go", "id": rID, "seqReindeer": nextSeq()}).encode()])

    if processingReindeers and ackReindeer >= 9:
        processingReindeers = False
        print("Finished christmas days. Reindeers can return to the south pole.")

    if not processingReindeers and not processingElves and len(elves) >= 3:
        processingElves = True
        ackElf = 0
        print(f"Helping elves: {list(elves)[:3]}")
        for _ in range(3):
            _id, eID = elves.popleft()
            router.send_multipart([_id, json.dumps({"action": "elves_help", "id": eID, "seqElf": nextSeq()}).encode()])

    if not processingReindeers and processingElves and ackElf >= 3:
        processingElves = False
        print("Finished helping the elves")
