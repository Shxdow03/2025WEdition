import threading
import subprocess
import time
import os
import sys
from datetime import datetime

_diskArg = sys.argv[1:] or ["/dev/sdd"]
_DISK = _diskArg[0]
_replaceDiskArg = sys.argv[2:] or ["/dev/sdg"]
_REPLACE_DISK = _replaceDiskArg[0]
_datasetArg = sys.argv[3:] or ["zpool_raidz/raid"]
_DATASET = _datasetArg[0]
_FILE_PATH_CRASH = f"/{_DATASET}/raidz_crash.bin"
_FILE_PATH = f"/{_DATASET}/raidz_no_crash.bin"
_BLOCK_SIZE_READ = 1024 * 512
_BLOCK_SIZE_WRITE = 1024 * 1024
_iterations = 200

def run_shell_command(command):
    commandResult = subprocess.run(command, shell=True, text=True, capture_output=True)
    if commandResult.returncode != 0:
        raise RuntimeError(f"There was a problem when executing {command}: {commandResult.stderr}")
    return commandResult.stdout

if not os.path.exists(run_shell_command(f"zfs get mountpoint {_DATASET} -H -o value").strip()):
    raise ValueError(
        f"{_DATASET} doesn't exist.\n"
        f"Please create the pool/dataset before attempting to interact with a file."
    )

if not os.path.exists(_DISK):
    raise ValueError(
        f"{_DISK} doesn't exist.\n"
        f"Please create the disk and use it in the raidz-setup used for the experiment."
    )

if not os.path.exists(_REPLACE_DISK):
    raise ValueError(
        f"{_REPLACE_DISK} doesn't exist.\n"
        f"Please create the disk and DON'T use it in the raidz-setup used for the experiment."
    )

def get_blocks(path):
    numStartBlocks = run_shell_command(f"cat {path} | grep -a ': START' | wc -l")
    numEndBlocks = run_shell_command(f"cat {path} | grep -a ': END' | wc -l")
    print(f"Number of Start Blocks: {numStartBlocks.strip()}")
    print(f"Number of End Blocks: {numEndBlocks.strip()}")

def write_file(path):
    with open(path, "wb") as f:
        print("Start Writing...")
        for i in range(_iterations):
            f.write(f"\nBlock {i+1}: START\n".encode())
            data = os.urandom(_BLOCK_SIZE_WRITE)
            f.write(data)
            f.write(f"\nBlock {i + 1}: END\n".encode())
            time.sleep(0.01)
        print("Finish Writing...")
    get_blocks(path)

def read_file(path):
    startBlockCount = 0
    endBlockCount = 0
    with open(path, "rb") as f:
        print("Start Reading...")
        while True:
            data = f.read(_BLOCK_SIZE_READ)
            if b": START" in data:
                startBlockCount += 1
            if b": END" in data:
                endBlockCount += 1
            time.sleep(0.01)
            if not data:
                break
        print("Finish Reading...")
    print(f"Number of Start Blocks: {startBlockCount}")
    print(f"Number of End Blocks: {endBlockCount}")


def crash_disk(disk):
    time.sleep(2)
    run_shell_command(f"zpool offline {_DATASET.split("/")[0]} {disk}")
    print(f"Disk {disk} crashed!")

def run_crash(target1, target2, disk):
    t1 = threading.Thread(target=target1, daemon=True, args=(_FILE_PATH_CRASH,))
    t2 = threading.Thread(target=target2, args=(disk,))
    startTime = datetime.now()
    print("-"*20)
    print(f"Starting at: {startTime.strftime("%Y-%m-%dT%H:%M:%S")}")
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    endTime = datetime.now()
    print(f"Ending at: {endTime.strftime("%Y-%m-%dT%H:%M:%S")}")
    print(f"Elapsed time: {endTime - startTime} seconds")
    print("-"*20)

def run_no_crash(target1):
    t1 = threading.Thread(target=target1, daemon=True, args=(_FILE_PATH,))
    startTime = datetime.now()
    print("-"*20)
    print(f"Starting at: {startTime.strftime("%Y-%m-%dT%H:%M:%S")}")
    t1.start()
    time.sleep(2)
    t1.join()
    endTime = datetime.now()
    print(f"Ending at: {endTime.strftime("%Y-%m-%dT%H:%M:%S")}")
    print(f"Elapsed time: {endTime - startTime} seconds")
    print("-"*20)

def main():
    """
    Usage: python3 raidz.py /dev/sdd /dev/sdg pool/zpool_for-saving/save-me
    disk: disk to initially "crash"
    replace disk: disk to use for initial "resilvering"
    dataset: pool/dataset
    """
    raid_disks = run_shell_command("zdb -C zpool_raidz | grep '/dev/'").rstrip().split("\n")
    abort = True
    for disk in raid_disks:
        if _DISK in disk.split("'")[1]:
            abort = False
    if abort:
        raise ValueError(
            f"{_DISK} is not part of the raidz setup for pool {_DATASET.split("/")[0]}"
        )
    print("-"*20)
    print("Running crash while Write simulation...")
    run_crash(write_file, crash_disk, _DISK)
    time.sleep(3)
    print(f"Replacing offline disk {_DISK} with unused disk {_REPLACE_DISK}")
    run_shell_command(f"zpool replace {_DATASET.split("/")[0]} {_DISK} {_REPLACE_DISK}")
    time.sleep(5)
    print("Running crash while Read simulation...")
    run_crash(read_file, crash_disk, _REPLACE_DISK)
    time.sleep(3)
    print(f"Replacing offline disk {_REPLACE_DISK} with unused disk {_DISK}")
    run_shell_command(f"zpool replace {_DATASET.split("/")[0]} {_REPLACE_DISK} {_DISK}")
    time.sleep(5)
    print("-" * 20)
    print("Running no crash while Write simulation...")
    run_no_crash(write_file)
    print("Running no crash while Read simulation...")
    run_no_crash(read_file)

if __name__ == "__main__":
    main()