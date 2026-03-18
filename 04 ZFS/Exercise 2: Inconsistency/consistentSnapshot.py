import threading
import subprocess
import time
import os
import random
from common import run_shell_command, run

_DATASET = "zpool_for-saving/save-me"
_FILE_PATH = f"/{_DATASET}/consistency.bin"
_SNAPSHOT_NAME = "consistency"

_BLOCK_SIZE = 1024 * 1024
_iterations = 200

write_event = threading.Event()
snapshot_event = threading.Event()
write_event.set()

def write_file():
    with open(_FILE_PATH, "wb") as f:
        for i in range(_iterations):
            write_event.wait()
            f.write(f"\nBlock {i+1}: START\n".encode())
            data = os.urandom(_BLOCK_SIZE)
            time.sleep(0.01)
            f.write(data)
            time.sleep(0.01)
            f.write(f"\nBlock {i + 1}: END\n".encode())
            f.flush()
            os.fsync(f.fileno())
            time.sleep(0.01)
            snapshot_event.set()


def take_snapshot():
    try:
        time.sleep(random.uniform(1, 5))

        write_event.clear()
        snapshot_event.wait()
        snapshot_event.clear()

        run_shell_command(f"zfs snapshot {_DATASET}@{_SNAPSHOT_NAME}")
        print("Finished Snapshot!")
        write_event.set()
    except subprocess.CalledProcessError:
        print(f"Snapshot {_DATASET}@{_SNAPSHOT_NAME} already exists")

def main():
    run(write_file, take_snapshot, _DATASET, _SNAPSHOT_NAME, _FILE_PATH)

if __name__ == "__main__":
    main()