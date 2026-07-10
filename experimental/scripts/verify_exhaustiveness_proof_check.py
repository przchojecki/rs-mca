#!/usr/bin/env python3
"""Checker for exhaustiveness proof packet."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import atlas_secant_model as model  # noqa: E402
import verify_exhaustiveness_proof as gen  # noqa: E402


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
    # t=1 instance
    t1 = model.analyze_instance(11, 6, 3, 5, n_lines=15, seed=2)
    t1_ok = t1["t"] == 1 and t1["missing_full_atlas"] == 0 and t1["routes_agree_all"]
    # restricted fails for some t>=2 (e.g. p=5 n=4 a=2)
    t2 = model.analyze_instance(5, 4, 2, 2, n_lines=20, seed=2)
    rest_ok = t2["t"] >= 2 and t2["missing_restricted_atlas"] > 0
    ok = (
        t1_ok
        and rest_ok
        and cert.get("verdict") == "PROVED-SPECIAL"
        and cert.get("all_pass")
    )
    print("route: t=1 full exhaustive + t>=2 restricted non-exhaustive dual routes")
    print(f"t1_ok={t1_ok} rest_ok={rest_ok}")
    print(f"payload_sha256: {cert.get('payload_sha256')}")
    print(f"verdict: {cert.get('verdict')}")
    if ok:
        print("RESULT: PASS")
        return 0
    print("RESULT: FAIL", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
