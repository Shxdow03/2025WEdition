import threading
import subprocess
import time
import os
import sys
import random
from common import run_shell_command, run

_datasetArg = sys.argv[1:] or ["zpool_for-saving/save-me"]
_DATASET = _datasetArg[0]
_FILE_PATH = f"/{_DATASET}/fullConsistency.bin"
_SNAPSHOT_NAME = "fullConsistency"
_BLOCK_SIZE = 1024 * 1024
_iterations = 200

if not os.path.exists(os.path.join("/"+_DATASET)):
    raise ValueError(
        f"{_DATASET} doesn't exist.\n"
        f"Please create the pool/dataset before attempting a snapshot."
    )

lock = threading.Lock()

def write_file():
    with open(_FILE_PATH, "wb") as f:
        with lock:
            for i in range(_iterations):
                f.write(f"\nBlock {i+1}: START\n".encode())
                data = os.urandom(_BLOCK_SIZE)
                time.sleep(0.01)
                f.write(data)
                time.sleep(0.01)
                f.write(f"\nBlock {i + 1}: END\n".encode())
                time.sleep(0.01)
            f.flush()
            os.fsync(f.fileno())

def take_snapshot():
    try:
        time.sleep(random.uniform(1, 5))
        with lock:
            run_shell_command(f"zfs snapshot {_DATASET}@{_SNAPSHOT_NAME}")
            print("Finished Snapshot!")
    except subprocess.CalledProcessError:
        print(f"Snapshot {_DATASET}@{_SNAPSHOT_NAME} already exists")

def main():
    run(write_file, take_snapshot, _DATASET, _SNAPSHOT_NAME, _FILE_PATH)

if __name__ == "__main__":
    main()
