#!/usr/bin/env python3
"""Checker for atlas exhaustiveness hunt."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import atlas_secant_model as model  # noqa: E402
import verify_atlas_exhaustiveness_hunt as gen  # noqa: E402


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    root = gen.repo_root()
    path = root / gen.CERT
    if not path.is_file():
        print("RESULT: FAIL missing cert", file=sys.stderr)
        return 1
    cert = json.loads(path.read_text(encoding="utf-8"))
    # re-run one small instance dual routes
    live = model.analyze_instance(7, 5, 2, 3, n_lines=20, seed=1)
    live_ok = live["routes_agree_all"] and live["missing_full_atlas"] == 0
    # restricted can miss
    rest_ok = cert.get("summary", {}).get("restricted_atlas_shows_missing") is True
    pins_ok = cert.get("pins_ok") is True
    ok = live_ok and rest_ok and pins_ok and cert.get("all_pass")
    print("route: re-run p=7 n=5 dual bad-slope routes + restricted-missing flag")
    print(f"live_ok={live_ok} rest_ok={rest_ok} pins_ok={pins_ok}")
    print(f"payload_sha256: {cert.get('payload_sha256')}")
    print(f"verdict: {cert.get('verdict')}")
    if ok:
        print("RESULT: PASS")
        return 0
    print("RESULT: FAIL", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
