#!/usr/bin/bash

mkdir -p /benchmark/zfs
mkdir -p /benchmark/ext4

# Ext4 Benchmarks
fio --name=seqwrite --rw=write --bs=1MB --size=2G --runtime=30 --directory=/mnt/ext4bench/ --output=/benchmark/ext4/ext4_seqwrite.txt
fio --name=seqread --rw=read --bs=1MB --size=2G --runtime=30 --directory=/mnt/ext4bench/ --output=/benchmark/ext4/ext4_seqread.txt
fio --name=randread --rw=randread --bs=1MB --size=2G --runtime=30 --directory=/mnt/ext4bench/ --output=/benchmark/ext4/ext4_randread.txt
fio --name=randwrite --rw=randwrite --bs=1MB --size=2G --runtime=30 --directory=/mnt/ext4bench/ --output=/benchmark/ext4/ext4_randwrite.txt
fio --name=randrw --rw=randrw --bs=1MB --size=2G --runtime=30 --buffer_compress_percentage=60 --directory=/mnt/ext4bench/ --output=/benchmark/ext4/ext4_randrw_compr60.txt
fio --name=readwrite --rw=readwrite --bs=1MB --size=2G --runtime=30 --buffer_compress_percentage=60 --directory=/mnt/ext4bench/ --output=/benchmark/ext4/ext4_readwrite_compr60.txt
fio --name=randrw --rw=randrw --bs=1MB --size=2G --runtime=30 --directory=/mnt/ext4bench/ --output=/benchmark/ext4/ext4_randrw.txt
fio --name=readwrite --rw=readwrite --bs=1MB --size=2G --runtime=30 --directory=/mnt/ext4bench/ --output=/benchmark/ext4/ext4_readwrite.txt

# ZFS Benchmarks
fio --name=seqwrite --rw=write --bs=1MB --size=2G --runtime=30 --directory=/zpool_benchmark/benchmark --output=/benchmark/zfs/zfs_seqwrite.txt
fio --name=seqread --rw=read --bs=1MB --size=2G --runtime=30 --directory=/zpool_benchmark/benchmark --output=/benchmark/zfs/zfs_seqread.txt
fio --name=randread --rw=randread --bs=1MB --size=2G --runtime=30 --directory=/zpool_benchmark/benchmark --output=/benchmark/zfs/zfs_randread.txt
fio --name=randwrite --rw=randwrite --bs=1MB --size=2G --runtime=30 --directory=/zpool_benchmark/benchmark --output=/benchmark/zfs/zfs_randwrite.txt
fio --name=readwrite --rw=readwrite --bs=1MB --size=2G --runtime=30 --buffer_compress_percentage=60 --directory=/zpool_benchmark/benchmark/ --output=/benchmark/zfs/zfs_readwrite_compr60.txt
fio --name=randrw --rw=randrw --bs=1MB --size=2G --runtime=30 --buffer_compress_percentage=60 --directory=/zpool_benchmark/benchmark/ --output=/benchmark/zfs/zfs_randrw_compr60.txt
fio --name=readwrite --rw=readwrite --bs=1MB --size=2G --runtime=30 --directory=/zpool_benchmark/benchmark/ --output=/benchmark/zfs/zfs_readwrite.txt
fio --name=randrw --rw=randrw --bs=1MB --size=2G --runtime=30 --directory=/zpool_benchmark/benchmark/ --output=/benchmark/zfs/zfs_randrw.txt