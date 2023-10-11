#!/bin/bash

if [[ -z "${DOMINO_NODE_IP}" ]]; then
    python src/main.py
else
    # torchrun --n_proc_per_node 1 /mnt/src/main.py
    python /mnt/code/src/main.py
fi