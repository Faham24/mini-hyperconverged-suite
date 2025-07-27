# dashboard.py
import time
import os
from rich.table import Table
from rich.console import Console
from rich.live import Live
from datetime import datetime

HEALTH_LOG = "logs/monitor.log"  # adjust path if needed

console = Console()


def parse_health_log(log_path):
    if not os.path.exists(log_path):
        print(f"Log file not found: {log_path}")
        return []

    node_data = {}
    with open(log_path, "r") as file:
        for line in file:
            try:
                # Example line:
                # 2025-07-27 14:11:54,440 - INFO - [node1] ✅ Service is healthy.
                parts = line.strip().split(" - ")
                if len(parts) < 3:
                    continue

                timestamp = parts[0].strip()
                node_part = parts[2].strip()

                node_start = node_part.find("[") + 1
                node_end = node_part.find("]")
                if node_start == 0 or node_end == -1:
                    continue

                node = node_part[node_start:node_end]
                status = "UP" if "✅" in node_part else "DOWN"

                node_data[node] = {
                    "node": node,
                    "status": status,
                    "last_checked": timestamp,
                    "last_heal": "N/A",  # Adjust if you add heal log entries later
                }
            except Exception as e:
                print(f"Error parsing line: {line.strip()}\n{e}")

    return list(node_data.values())


def generate_table(data):
    table = Table(title="🖥️  Hyperconverged CLI Dashboard", style="cyan")

    table.add_column("Node", style="bold")
    table.add_column("Status", style="green")
    table.add_column("Last Checked", style="white")
    table.add_column("Last Heal", style="magenta")

    for details in data:
        node = details.get("node", "N/A")
        status = details.get("status", "Unknown")
        color = "green" if status == "UP" else "red"
        table.add_row(
            node,
            f"[{color}]{status}[/{color}]",
            details.get("last_checked", "N/A"),
            details.get("last_heal", "N/A")
        )

    return table



def main():
    with Live(refresh_per_second=1) as live:
        while True:
            health_data = parse_health_log(HEALTH_LOG)
            table = generate_table(health_data)
            live.update(table)
            time.sleep(3)


if __name__ == "__main__":
    console.print("[bold blue]Starting CLI Dashboard...[/bold blue]")
    main()
