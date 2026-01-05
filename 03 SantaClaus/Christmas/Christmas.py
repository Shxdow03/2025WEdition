from threading import *
import time

semElves = Semaphore(1)
semSanta = Semaphore(0)
semReindeers = Semaphore(0)
mutex = Semaphore(1)

class ChristmasSync:
    def __init__(self):
        self.elves = 0
        self.reindeers = 0

    def get_elves(self):
        return self.elves

    def set_elves(self, elves_count):
        self.elves = elves_count

    def get_reindeers(self):
        return self.reindeers

    def set_reindeers(self, reindeers_count):
        self.reindeers = reindeers_count

def prepare_sleigh():
    print("All 9 Reindeers have assembled. Sleigh is being prepared.\n")

def get_hitched():
    print("Reindeer is getting hitched ...")

def help_elves():
    print("Helping elves ...\n")

def get_help(elves):
    print(f"Number of elves that request help: {elves}\n")

def run_santa(c):
    while True:
        semSanta.acquire()
        mutex.acquire()
        print(f"Current number of elves: {c.get_elves()}")
        print(f"Current number of reindeers: {c.get_reindeers()}")
        if (c.get_reindeers() >= 9):
            prepare_sleigh()
            semReindeers.release(9)
            c.set_reindeers(c.get_reindeers()-9)
            time.sleep(5)
        elif (c.get_elves() >= 3):
            help_elves()
            time.sleep(5)
        mutex.release()


def run_elves(c):
    while True:
        semElves.acquire()
        mutex.acquire()
        c.set_elves(c.get_elves()+1)
        if (c.get_elves() >= 3):
            semSanta.release()
        else:
            semElves.release()
        mutex.release()
        get_help(elves=c.get_elves())
        time.sleep(1)
        mutex.acquire()
        c.set_elves(c.get_elves()-1)
        print("Succesfully helped one elf!")
        if (c.get_elves() == 0):
            semElves.release()
        mutex.release()


def run_reindeers(c):
    while True:
        mutex.acquire()
        c.set_reindeers(c.get_reindeers()+1)
        time.sleep(0.1)
        print(f"Number of reindeers that have arrived from the south pole: {c.get_reindeers()}")
        if (c.get_reindeers() == 9):
            semSanta.release()
        mutex.release()
        semReindeers.acquire()
        get_hitched()
        time.sleep(1)


def main():
    Christmas = ChristmasSync()
    t1 = Thread(target=run_santa, args=(Christmas,))
    t2_list = []
    t3_list = []
    t1.start()
    for i in range(11):
        t2_list.append(Thread(target=run_elves, args=(Christmas,)))
    for i in range(9):
        t3_list.append(Thread(target=run_reindeers, args=(Christmas,)))
    for i in t2_list:
        i.start()
    for i in t3_list:
        i.start()
    t1.join()

if __name__ == "__main__":
    main()
