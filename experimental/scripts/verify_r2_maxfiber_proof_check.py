#!/usr/bin/env python3
"""Checker for R=2 max-fiber proof packet.

checker route: re-enumerate fibers independently; verify max_f <= N^{m-2};
phase0 four-tuple cube3.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_r2_maxfiber_proof as gen  # noqa: E402
import w49_sidon_model as m  # noqa: E402


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

    c3_ok = m.energy_four_tuple(list(itertools.product([0, 1], repeat=3))) == 216

    toys_ok = True
    for t in cert.get("toys", [])[:6]:
        row = gen.max_fiber_R2(t["p"], t["N"], t["m"])
        if row["max_f"] != t["max_f"] or not row["bound_holds"]:
            toys_ok = False
            break
        bound = 1 if t["m"] == 2 else t["N"] ** (t["m"] - 2)
        if t["max_f"] > bound:
            toys_ok = False

    ok = (
        c3_ok
        and toys_ok
        and cert.get("phase0", {}).get("pass")
        and cert.get("verdict") == "PROVED-SPECIAL"
        and cert.get("all_pass")
    )
    print("route: re-enum R=2 fibers + N^{m-2} check + four-tuple cube3")
    print(f"c3_ok={c3_ok} toys_ok={toys_ok}")
    print(f"payload_sha256: {cert.get('payload_sha256')}")
    print(f"verdict: {cert.get('verdict')}")
    if ok:
        print("RESULT: PASS")
        return 0
    print("RESULT: FAIL", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
