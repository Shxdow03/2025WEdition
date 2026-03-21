import threading
import subprocess
from datetime import datetime

def run_shell_command(command):
    commandResult = subprocess.run(command, shell=True, text=True, capture_output=True)
    if commandResult.returncode != 0:
        raise RuntimeError(f"There was a problem when executing {command}: {commandResult.stderr}")
    return commandResult.stdout

def get_blocks(path):
    numStartBlocks = run_shell_command(f"cat {path} | grep -a ': START' | wc -l")
    numEndBlocks = run_shell_command(f"cat {path} | grep -a ': END' | wc -l")
    print(f"Number of Start Blocks: {numStartBlocks.strip()}")
    print(f"Number of End Blocks: {numEndBlocks.strip()}")

def run(t1, t2, dataset, snap, path):
    startTime = datetime.now()
    print("-" * 20)
    print(f"Starting Execution at: {startTime.strftime("%Y-%m-%dT%H:%M:%S")}")
    t1 = threading.Thread(target=t1, daemon=True)
    t2 = threading.Thread(target=t2)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
    endTime = datetime.now()
    print(f"Finished Execution at: {endTime.strftime("%Y-%m-%dT%H:%M:%S")}")
    print(f"Time elapsed: {endTime - startTime} Seconds")
    print(f"Before rollback with {dataset}@{snap}")
    print("-" * 20)
    get_blocks(path)
    print("-"*20)
    print("Rolling back with taken snapshot!")
    run_shell_command(f"zfs rollback {dataset}@{snap}")
    print(f"After rollback with {dataset}@{snap}:")
    print("-" * 20)
    get_blocks(path)
    print("-" * 20)
    run_shell_command(f"zfs destroy {dataset}@{snap}")