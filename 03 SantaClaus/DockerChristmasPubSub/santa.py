import zmq
import time

context = zmq.Context()

pull = context.socket(zmq.PULL)
pull.bind("tcp://*:2222")

pub = context.socket(zmq.PUB)
pub.bind("tcp://*:2223")

reindeers = []
elves = []

while True:
    msg = pull.recv_json()

    if msg["type"] == "reindeer":
        reindeers.append(msg["id"])
        print(f"Number of reindeers that have arrived from the south pole: {len(reindeers)}/9")

        if len(reindeers) == 9:
            print(f"All reindeers arrived, preparing sleigh for reindeers: {reindeers}")
            time.sleep(1)
            pub.send_json({"action": "reindeer_go", "reindeers": reindeers})
            reindeers = []
            #time.sleep(random.randint(5,8))

    elif msg["type"] == "elf":
        if len(reindeers) == 9:
            print("Elves have to wait because all reindeers have arrived.")
            continue
        elves.append(msg["id"])
        print(f"Number of elves that request help: {len(elves)}/3")

        if len(elves) == 3:
            print(f"Helping elves: {elves}")
            time.sleep(1)
            pub.send_json({"action": "elves_help", "elves": elves})
            elves = []
            #time.sleep(random.randint(5,8))