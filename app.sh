#!/bin/bash

if [[ -n "${!DOMINO_NODE_IP}" ]]; then
    # torchrun --n_proc_per_node 1 /mnt/src/main.py
    python /mnt/src/main.py
else
    python src/main.py
fi