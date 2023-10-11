#!/bin/bash

if [[ -z "${DOMINO_NODE_IP}" ]]; then
    pip install ./llama --quiet
    python src/main.py
else
    pip install /mnt/code/llama --user --quiet
    # torchrun --n_proc_per_node 1 /mnt/src/main.py
    python /mnt/code/src/main.py
fi