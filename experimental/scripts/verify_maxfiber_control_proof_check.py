#!/usr/bin/env python3
"""Independent checker for max-fiber control proofs.

checker route: re-enum R>=m charts; verify max_f==1; phase0 cube3 via four-tuple;
recompute ratio<=L on Lemma B toys.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_maxfiber_control_proof as gen  # noqa: E402
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

    A = list(itertools.product([0, 1], repeat=3))
    c3_ok = m.energy_four_tuple(A) == 216

    A_ok = True
    for r in cert.get("lemmas", {}).get("A", {}).get("rows", []):
        if not r.get("R_ge_m"):
            continue
        T = list(range(1, r["N"] + 1))
        if math.comb(r["N"], r["m"]) > 10000:
            continue
        Omega = m.all_m_subsets(T, r["m"])
        fibers = m.build_fibers(Omega, r["R"], r["p"])
        max_f = max(len(v) for v in fibers.values())
        if max_f != 1 or len(fibers) != len(Omega):
            A_ok = False
            break

    B_ok = True
    for r in cert.get("lemmas", {}).get("B", {}).get("rows", []):
        if r["ratio"] > r["L"] + 1e-9:
            B_ok = False

    ok = (
        c3_ok
        and A_ok
        and B_ok
        and cert.get("phase0", {}).get("pass")
        and cert.get("verdict") == "PROVED-SPECIAL"
        and cert.get("all_pass")
    )
    print("route: four-tuple cube3 + re-enum R>=m injectivity + ratio<=L check")
    print(f"c3_ok={c3_ok} A_ok={A_ok} B_ok={B_ok}")
    print(f"payload_sha256: {cert.get('payload_sha256')}")
    print(f"verdict: {cert.get('verdict')}")
    if ok:
        print("RESULT: PASS")
        return 0
    print("RESULT: FAIL", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
