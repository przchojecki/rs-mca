#!/usr/bin/env python3
"""Append the A407 public threshold row fragments to site/data JSON arrays.

Run from the repository root after the certificate generator has written:
  site/data/frontier_prime_a406_a407_adjacent_gate.entry.json
  site/data/updates_m1_a407_a408_residual_design_threshold.entry.json

The script is idempotent by entry id/href and refuses to overwrite unrelated
site data. It is intentionally separate from the theorem verifier so reviewers
can inspect the public-row object before modifying the live site arrays.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[2]
FRONTIER_JSON = ROOT / "site" / "data" / "frontier.json"
UPDATES_JSON = ROOT / "site" / "data" / "updates.json"
FRONTIER_ENTRY = ROOT / "site" / "data" / "frontier_prime_a406_a407_adjacent_gate.entry.json"
UPDATES_ENTRY = ROOT / "site" / "data" / "updates_m1_a407_a408_residual_design_threshold.entry.json"


def load_array(path: Path) -> List[Dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise TypeError(f"expected JSON array at {path}")
    return data


Schema = Dict[str, Tuple[type, ...]]


def require_schema(entry: Dict[str, Any], schema: Schema, path: Path) -> None:
    missing = [key for key in schema if key not in entry]
    if missing:
        raise KeyError(f"{path} missing required keys: {', '.join(missing)}")
    bad_types = []
    for key, expected in schema.items():
        value = entry[key]
        if not isinstance(value, expected):
            expected_names = " or ".join(t.__name__ for t in expected)
            bad_types.append(f"{key}: expected {expected_names}, got {type(value).__name__}")
    if bad_types:
        raise TypeError(f"{path} has invalid field types: {'; '.join(bad_types)}")


def load_entry(path: Path, schema: Schema) -> Dict[str, Any]:
    entry = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(entry, dict):
        raise TypeError(f"expected JSON object at {path}")
    require_schema(entry, schema, path)
    return entry


def append_unique(array_path: Path, entry_path: Path, key: str, schema: Schema, write: bool) -> bool:
    arr = load_array(array_path)
    entry = load_entry(entry_path, schema)
    if any(item.get(key) == entry.get(key) for item in arr):
        return False
    arr.append(entry)
    if write:
        array_path.write_text(json.dumps(arr, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="modify site/data/frontier.json and updates.json")
    args = parser.parse_args()
    frontier_schema: Schema = {
        "id": (str,),
        "title": (str,),
        "short": (str,),
        "row": (str,),
        "n": (int,),
        "k": (int,),
        "rho": (int, float),
        "agreement": (int,),
        "badSlopes": (str,),
        "q": (str,),
        "status": (str,),
        "tag": (str,),
        "label": (str,),
        "radiusLabel": (str,),
        "proof": (str,),
        "nonclaims": (str,),
        "links": (list,),
        "authors": (str,),
    }
    updates_schema: Schema = {
        "date": (str,),
        "status": (str,),
        "author": (str,),
        "title": (str,),
        "summary": (str,),
        "impact": (str,),
        "href": (str,),
    }
    f_added = append_unique(FRONTIER_JSON, FRONTIER_ENTRY, "id", frontier_schema, args.write)
    u_added = append_unique(UPDATES_JSON, UPDATES_ENTRY, "href", updates_schema, args.write)
    print(json.dumps({"frontier_added": f_added, "updates_added": u_added, "write": args.write}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
