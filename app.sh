#!/bin/bash

if [[ -z "${DOMINO_NODE_IP}" ]]; then
    python app/main.py
else
    python /mnt/code/app/main.py
fi