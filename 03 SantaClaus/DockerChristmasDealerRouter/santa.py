import zmq
import time
import json

context = zmq.Context()

router = context.socket(zmq.ROUTER)
router.bind("tcp://*:2222")

reindeers = []
elves = []

while True:
    id_, empty, msg = router.recv_multipart()
    msg = json.loads(msg.decode())

    if msg["type"] == "reindeer":
        reindeers.append((id_, msg["id"]))
        print(f"Number of reindeers that have arrived from the south pole: {len(reindeers)}/9")

        if len(reindeers) == 9:
            print(f"All reindeers arrived, preparing sleigh for reindeers: {reindeers}")
            time.sleep(1)
            for reindeer in reindeers:
                router.send_multipart([reindeer[0], json.dumps({"action": "reindeer_go", "id": reindeer[1]}).encode()])
            reindeers = []

    elif msg["type"] == "elf":
        if len(reindeers) == 9:
            print("Elves have to wait because all reindeers have arrived.")
            continue
        elves.append((id_, msg["id"]))
        print(f"Number of elves that request help: {len(elves)}/3")

        if len(elves) == 3:
            print(f"Helping elves: {elves}")
            time.sleep(1)
            for elf in elves:
                router.send_multipart([elf[0], json.dumps({"action": "elves_help", "id": elf[1]}).encode()])
            elves = []
