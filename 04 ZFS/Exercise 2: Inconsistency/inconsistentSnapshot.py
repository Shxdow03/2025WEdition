import subprocess
import time
import os
import random
from common import run_shell_command, run

_DATASET = "zpool_for-saving/save-me"
_FILE_PATH = f"/{_DATASET}/inconsistency.bin"
_SNAPSHOT_NAME = "inconsistency"

_BLOCK_SIZE = 1024 * 1024
_iterations = 200

def write_file():
    with open(_FILE_PATH, "wb") as f:
        for i in range(_iterations):
            f.write(f"\nBlock {i+1}: START\n".encode())
            data = os.urandom(_BLOCK_SIZE)
            time.sleep(0.01)
            f.write(data)
            time.sleep(0.01)
            f.write(f"\nBlock {i + 1}: END\n".encode())
            time.sleep(0.01)

def take_snapshot():
    time.sleep(random.uniform(1, 5))
    try:
        run_shell_command(f"zfs snapshot {_DATASET}@{_SNAPSHOT_NAME}")
        print("Finished Snapshot!")
    except subprocess.CalledProcessError:
        print(f"Snapshot {_DATASET}@{_SNAPSHOT_NAME} already exists")

def main():
    run(write_file, take_snapshot, _DATASET, _SNAPSHOT_NAME, _FILE_PATH)

if __name__ == "__main__":
    main()