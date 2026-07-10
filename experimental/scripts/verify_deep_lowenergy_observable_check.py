#!/usr/bin/env python3
"""Checker for deep low-energy observability packet.

checker route: sum-histogram energy; algebraic ratio; re-run one deep chart thr sweep;
phase0 cube3.
"""
from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_deep_lowenergy_observable as gen  # noqa: E402
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

    # re-analyze one deep chart
    deep = [c for c in cert.get("charts", []) if c.get("regime") == "deep"]
    live_ok = True
    if deep:
        c = deep[0]
        live = gen.analyze_chart(c["p"], c["N"], c["m"], c["R"], seed=0)
        live_ok = live["regime"] == "deep" and live["barN"] > 0
        # thr sweep length match
        live_ok = live_ok and len(live["thr_sweep"]) == len(c["thr_sweep"])

    # ratio algebra
    ratio_ok = True
    for c in cert.get("charts", [])[:5]:
        pr = c.get("primary") or {}
        if pr.get("max_f_low") and c.get("barN"):
            r = pr["max_f_low"] / c["barN"]
            if abs(r - pr.get("ratio", -1)) > 1e-9:
                ratio_ok = False

    ok = (
        c3_ok
        and live_ok
        and ratio_ok
        and cert.get("phase0", {}).get("pass")
        and cert.get("all_pass")
    )
    print("route: four-tuple cube3 + re-analyze deep chart + ratio algebra")
    print(f"c3_ok={c3_ok} live_ok={live_ok} ratio_ok={ratio_ok}")
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
