#!/bin/bash
# autoheal.sh
NODE=$1
echo "[Auto-Heal] Restarting service in $NODE"
pkill -f "$NODE/fake_service.py"
python3 "$NODE/fake_service.py" &
