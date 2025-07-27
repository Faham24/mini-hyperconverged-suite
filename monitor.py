import os
import time
import subprocess
import logging

# Setup logging
logging.basicConfig(
    filename='logs/monitor.log',
    filemode='a',  # Append logs to the same file
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Define the simulated nodes
nodes = ["node1", "node2", "node3"]

while True:
    for node in nodes:
        health_file = os.path.join(node, "health.txt")

        if not os.path.exists(health_file):
            msg = f"[{node}] ❌ Health file not found!"
            print(msg)
            logging.error(msg)
            continue

        with open(health_file, "r") as f:
            status = f.read().strip()

        if status == "UP":
            msg = f"[{node}] ✅ Service is healthy."
            print(msg)
            logging.info(msg)
        else:
            msg = f"[{node}] ⚠ Service is DOWN. Attempting auto-heal..."
            print(msg)
            logging.warning(msg)

            try:
                subprocess.Popen(["python3", "fake_service.py"], cwd=node)
                heal_msg = f"[{node}] 🔄 Auto-heal triggered."
                print(heal_msg)
                logging.info(heal_msg)
            except Exception as e:
                error_msg = f"[{node}] ❌ Auto-heal failed: {e}"
                print(error_msg)
                logging.error(error_msg)

    print("-" * 50)
    time.sleep(5)  # Check every 5 seconds
