import time
import random
import os

status_file = os.path.join(os.path.dirname(__file__), "health.txt")
while True:
    # Randomly simulate a crash
    if random.random() < 0.05:
        with open(status_file, "w") as f:
            f.write("DOWN")
        break

    with open(status_file, "w") as f:
        f.write("UP")
    time.sleep(2)