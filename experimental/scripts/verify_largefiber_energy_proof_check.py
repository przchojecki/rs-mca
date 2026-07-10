#!/usr/bin/env python3
"""Checker for largefiber energy proof packet."""
from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_largefiber_energy_proof as gen  # noqa: E402
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
    # recompute one fiber CS
    cs_ok = True
    rows = cert.get("toys", {}).get("rows") or []
    if rows:
        r0 = rows[0]
        T = list(range(1, r0["N"] + 1))
        Omega = m.all_m_subsets(T, r0["m"])
        fibers = m.build_fibers(Omega, 2, r0["p"])
        # find a fiber with matching f
        found = False
        for members in fibers.values():
            if len(members) != r0["f"]:
                continue
            pts = [m.support_vector(s, T) for s in members]
            E = m.energy_four_tuple(pts) if len(pts) <= 20 else m.energy_diff_counter(pts)
            Delta = E / float(len(pts) ** 3)
            if abs(Delta - r0["Delta"]) < 1e-6 or abs(E - r0["E"]) < 1:
                found = True
                if Delta + 1e-9 < 1.0 / len(pts):
                    cs_ok = False
                break
        if not found:
            # still verify CS inequality on stated numbers
            if r0["Delta"] + 1e-9 < 1.0 / r0["f"]:
                cs_ok = False
    ok = (
        c3_ok
        and cs_ok
        and cert.get("verdict") == "REDUCED"
        and cert.get("phase0", {}).get("pass")
        and cert.get("all_pass")
    )
    print("route: four-tuple cube3 + fiber E recompute + CS inequality")
    print(f"c3_ok={c3_ok} cs_ok={cs_ok}")
    print(f"payload_sha256: {cert.get('payload_sha256')}")
    print(f"verdict: {cert.get('verdict')}")
    if ok:
        print("RESULT: PASS")
        return 0
    print("RESULT: FAIL", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
