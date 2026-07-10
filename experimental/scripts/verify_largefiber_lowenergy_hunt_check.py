#!/usr/bin/env python3
"""Checker for largefiber-lowenergy hunt.

checker route: four-tuple energy on extremal; re-run one linear chart; phase0 cube3.
"""
from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_largefiber_lowenergy_hunt as gen  # noqa: E402
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

    live_ok = True
    lin = [
        c
        for c in (cert.get("charts_sample") or cert.get("charts") or [])
        if c.get("linear_density") and c.get("Omega_mode") == "all"
    ]
    if lin:
        c = lin[0]
        live = gen.analyze_linear(c["p"], c["N"], c["density"], seed=0, max_omega=4000)
        live_ok = live.get("max_f") == c.get("max_f") and abs(
            (live.get("largest_fiber_Delta") or 0) - (c.get("largest_fiber_Delta") or 0)
        ) < 1e-9

    # Delta identity E/f^3 on a frontier point
    delta_ok = True
    for c in lin[:3]:
        for pt in (c.get("frontier_top10") or [])[:2]:
            if pt.get("f") and pt.get("E") is not None and pt.get("Delta") is not None:
                if abs(pt["E"] / (pt["f"] ** 3) - pt["Delta"]) > 1e-9:
                    delta_ok = False

    ok = c3_ok and live_ok and delta_ok and cert.get("phase0", {}).get("pass") and cert.get("all_pass")
    print("route: four-tuple cube3 + re-run linear chart + Delta=E/f^3 check")
    print(f"c3_ok={c3_ok} live_ok={live_ok} delta_ok={delta_ok}")
    print(f"payload_sha256: {cert.get('payload_sha256')}")
    print(f"verdict: {cert.get('verdict')}")
    print(f"summary: {cert.get('summary')}")
    if ok:
        print("RESULT: PASS")
        return 0
    print("RESULT: FAIL", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
