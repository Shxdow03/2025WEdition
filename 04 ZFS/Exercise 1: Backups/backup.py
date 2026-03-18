import sys
import os
import subprocess
from datetime import datetime

_retentionArg = sys.argv[1:] or [5]
_folderArg = sys.argv[2:] or ["zpool_for-saving/save-me"]
_backupArg = sys.argv[3:] or ["zpool_for-backups/backups"]

try:
    _retentionCount = int(_retentionArg[0])
except ValueError:
    print("Given Argument wasn't a number, defaulting to 5.")
    _retentionCount = 5

_folderToBeSaved = _folderArg[0]
_backupFolder = _backupArg[0]

if not os.path.exists(os.path.join("/"+_folderToBeSaved)):
    raise ValueError(
        f"Source {_folderToBeSaved} doesn't exist.\n"
        f"Please create the pool/dataset before attempting a backup."
    )

if not os.path.exists(os.path.join("/"+_backupFolder)):
    raise ValueError(
        f"Destination {_backupFolder} doesn't exist.\n"
        f"Please create the pool/dataset before attempting a backup."
    )

def get_retention_count():
    return _retentionCount

def get_folder_to_save():
    return _folderToBeSaved

def get_backup_folder():
    return _backupFolder

def run_shell_command(command):
    commandResult = subprocess.run(command, shell=True, text=True, capture_output=True)
    if commandResult.returncode != 0:
        raise RuntimeError(f"There was a problem when executing {command}: {commandResult.stderr}")
    return commandResult.stdout

def create_snapshot(dataset, timestamp):
    try:
        snapshotName = f"{dataset}@{timestamp}"
        run_shell_command(f"zfs snapshot {snapshotName}")
    except RuntimeError:
        print(f"Creation of snapshot has failed!")
    return snapshotName

def transfer_snapshot(snap, pred, dataset):
    try:
        if pred:
            transfer = f"zfs send -i {pred} {snap} | zfs recv -F {dataset}"
        else:
            transfer = f"zfs send {snap} | zfs recv -F {dataset}"
        run_shell_command(transfer)
    except RuntimeError as err:
        print(f"Send-Receive Operation has failed: {err}")

def get_all_snapshots(dataset):
    try:
        snapshots = run_shell_command(f"zfs list -H -t snapshot -s creation -o name {dataset}")
        snapshotList = snapshots.strip().splitlines()
    except RuntimeError as err:
        print(f"An error occured while listing the snapshots: {err}")
        snapshotList = []
    return snapshotList

def delete_snapshot_overflow(dataset, retention):
    try:
        snapshotList = get_all_snapshots(dataset)
        diff = len(snapshotList) - retention
        if diff > 0:
            for i in range(diff):
                snapshotToRemove = snapshotList.pop(0)
                print(f"Deleting: {snapshotToRemove}")
                run_shell_command(f"zfs destroy {snapshotToRemove}")
    except Exception as err:
        print(f"Deletion of snapshot overflow has failed: {err}")

def main():
    """
    Usage: python3 backup.py 5 zpool_for-saving/save-me zpool_for-backups/backups
    retention: Number of copies/snapshots to keep in the backup destination after script execution
    source: pool/dataset to take a snapshot and send it to the backup destination
    destination: pool/dataset to receive the snapshot
    """
    src = get_folder_to_save()
    dest = get_backup_folder()
    startTime = datetime.now()
    print("\n"+"-"*20)
    print(f"Starting Backup at: {startTime.strftime("%Y-%m-%dT%H:%M:%S")}")
    print(f"Source Folder: {src}")
    print(f"Destination Folder: {dest}")
    predecessor = None
    src_snapshots = get_all_snapshots(src)
    if len(src_snapshots) > 0:
        predecessor = src_snapshots[-1]

    snapshot = create_snapshot(src, startTime.strftime("%Y-%m-%dT%H:%M:%S"))
    transfer_snapshot(snapshot, predecessor, dest)

    retentionCount = get_retention_count()

    delete_snapshot_overflow(dest, retentionCount)

    # Keeping one snapshot in Source Dataset for incremental approach
    delete_snapshot_overflow(src, 1)

    endTime = datetime.now()
    print(f"Finished Backup at: {endTime.strftime("%Y-%m-%dT%H:%M:%S")}")
    print(f"Time elapsed: {endTime-startTime} Seconds")
    print("-"*20)
    print("Remaining Snapshots:")
    print(f"{"\n".join(get_all_snapshots(dest))}")
    print(f"{"\n".join(get_all_snapshots(src))}")

if __name__ == "__main__":
    main()