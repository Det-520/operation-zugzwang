"""Check that scenario/data/assets.csv matches the force tables in the team packets.

Usage: python3 tools/check_assets.py
Exits non-zero if IDs differ between the packets and the CSV, or if a CSV row
is missing an asset name, role, or limitation, or if a split counter's `parts`
count doesn't match its list of zones (Z8;Z10).
"""

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKETS = {
    "REDFOR": ROOT / "scenario" / "redfor-packet.md",
    "BLUEFOR": ROOT / "scenario" / "bluefor-packet.md",
}
CSV_PATH = ROOT / "scenario" / "data" / "assets.csv"
ROW_ID = re.compile(r"^\|\s*([RB]-\d{2})\s*\|", re.MULTILINE)
REQUIRED = ("asset", "role", "limitation")


def main() -> int:
    problems = []

    packet_ids = {}
    for side, path in PACKETS.items():
        for asset_id in ROW_ID.findall(path.read_text(encoding="utf-8")):
            packet_ids[asset_id] = side

    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    csv_ids = {}
    for row in rows:
        asset_id = row["id"]
        if asset_id in csv_ids:
            problems.append(f"{asset_id}: duplicate row in CSV")
        csv_ids[asset_id] = row["side"]
        for field in REQUIRED:
            if not row[field].strip():
                problems.append(f"{asset_id}: empty '{field}' in CSV")
        parts = row.get("parts", "").strip()
        if parts and (not parts.isdigit() or int(parts) < 2):
            problems.append(f"{asset_id}: 'parts' must be blank or 2 or more, not '{parts}'")
        elif row.get("part_asset", "").strip() and not parts:
            problems.append(f"{asset_id}: 'part_asset' is set but 'parts' is blank")
        elif ";" in row["zone"] and len(row["zone"].split(";")) != int(parts or 1):
            problems.append(f"{asset_id}: {len(row['zone'].split(';'))} zones listed but parts is '{parts or 1}'")

    for asset_id in sorted(packet_ids.keys() - csv_ids.keys()):
        problems.append(f"{asset_id}: in {packet_ids[asset_id]} packet but not in CSV")
    for asset_id in sorted(csv_ids.keys() - packet_ids.keys()):
        problems.append(f"{asset_id}: in CSV but not in any packet")
    for asset_id in sorted(packet_ids.keys() & csv_ids.keys()):
        if packet_ids[asset_id] != csv_ids[asset_id]:
            problems.append(f"{asset_id}: side is {csv_ids[asset_id]} in CSV but {packet_ids[asset_id]} in packet")

    if problems:
        print("\n".join(problems))
        return 1
    print(f"OK: {len(csv_ids)} assets match across packets and CSV.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
