#!/usr/bin/env python3
"""Reconstruct one K'=79..82 frontier and complete pairwise-atlas reroute."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import tarfile
from pathlib import Path


ARCHIVES = list(Path(".").glob("*.tar.gz"))
ROOT = Path("repo") if ARCHIVES else Path(__file__).resolve().parents[2]
if ARCHIVES:
    with tarfile.open(ARCHIVES[0], "r:gz") as archive:
        archive.extractall(ROOT, filter="data")
PRIMARY_PATH = ROOT / "experimental/scripts/verify_kb_mca_rank11_full_carrier_atlas_k79_k82_k83_wall_v1.py"
OLD_FULL_PATH = ROOT / "experimental/scripts/verify_kb_mca_rank11_full_carrier_atlas_k74_k78_v1_full.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PRIMARY = load_module("rank11_k79_k83_primary_for_full", PRIMARY_PATH)
OLD_FULL = load_module("rank11_k74_k78_full_replay_core", OLD_FULL_PATH)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--row", type=int, choices=range(79, 83), required=True)
    args = parser.parse_args()
    raw = PRIMARY.MANIFEST.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == PRIMARY.MANIFEST_SHA256
    data = json.loads(raw)
    PRIMARY.validate(data)
    print(json.dumps(
        OLD_FULL.reconstruct(args.row, data["rows"][str(args.row)]),
        sort_keys=True,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
