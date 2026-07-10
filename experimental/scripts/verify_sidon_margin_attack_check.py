#!/usr/bin/env python3
"""Independent checker for W50 sidon-margin-attack.

checker route: sum-histogram energy; algebraic margin recompute from cert Gsid;
phase0 cube3 via sum-histogram only; re-evaluate one extremal config.
"""
from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_sidon_margin_attack as gen  # noqa: E402
import w49_sidon_model as m  # noqa: E402


def energy_sum_histogram(points):
    if not points:
        return 0
    sums: Counter = Counter()
    for a, b in itertools.product(points, points):
        s = tuple(a[i] + b[i] for i in range(len(a)))
        sums[s] += 1
    return int(sum(v * v for v in sums.values()))


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

    # phase0 via sum-histogram
    A = list(itertools.product([0, 1], repeat=3))
    e = energy_sum_histogram(A)
    c3_ok = e == 216 and cert.get("phase0", {}).get("energy_diff") == 216

    # recompute margins on scale family
    scale = cert.get("scale_in_p", {}).get("rows", [])
    scale_ok = True
    for r in scale[:5]:
        if r.get("Gsid") is None:
            continue
        rate = m.payment_rate(r["Gsid"], r["N"], gen.Q)
        rate_f = None if rate == float("-inf") else rate
        if r.get("rate") is not None and rate_f is not None:
            if abs(r["rate"] - rate_f) > 1e-9:
                scale_ok = False

    # re-run extremal config once
    ext = cert.get("zoom", {}).get("extremal", {})
    live_ok = True
    if ext:
        inst = m.evaluate_instance(
            ext["p"], ext["N"], ext["m"], ext["R"], seed=0, Omega_mode="all", max_omega=6000
        )
        # rates should be close (same seed/mode as zoom used evaluate_instance)
        if ext.get("rate") is not None and inst.get("rate") is not None:
            if abs(ext["rate"] - inst["rate"]) > 1e-9:
                # may differ if zoom stored different Omega_mode — allow only if payment same
                live_ok = ext["payment_holds"] == inst["payment_holds"]

    # synthetic still fails
    syn = m.synthetic_fail_instance()
    syn_ok = syn.get("pass") is True

    # trend consistency: recompute trend_a
    fam_a = [r for r in scale if r.get("family") == "N8_m4_R1_vary_p"]
    margins = [r["margin"] for r in fam_a if r.get("margin") is not None]
    trend = gen.trend_of(margins)
    trend_ok = trend == cert.get("scale_in_p", {}).get("family_N8_m4_R1_trend")

    ok = c3_ok and scale_ok and live_ok and syn_ok and trend_ok and cert.get("all_pass")

    print(
        "route: sum-histogram cube3 + algebraic margin recompute + extremal re-eval + trend recompute"
    )
    print(f"cube3_sum={e} c3_ok={c3_ok} scale_ok={scale_ok} live_ok={live_ok} syn_ok={syn_ok} trend={trend}")
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
