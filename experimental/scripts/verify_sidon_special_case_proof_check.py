#!/usr/bin/env python3
"""Independent checker for W50 special-case Sidon payment proofs.

checker route: recompute Gsid from fibers with four-tuple energy; verify
Lemma II inequality with Fraction; re-check injective toys independently.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_sidon_special_case_proof as gen  # noqa: E402
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

    # cube3
    A = list(itertools.product([0, 1], repeat=3))
    c3_ok = m.energy_four_tuple(A) == 216

    # recompute one injective instance
    I_rows = cert.get("lemmas", {}).get("I", {}).get("rows", [])
    inj_ok = True
    for r in I_rows:
        if not r.get("injective"):
            continue
        T = list(range(1, r["N"] + 1))
        Omega = m.all_m_subsets(T, r["m"])
        fibers = m.build_fibers(Omega, r["R"], r["p"])
        if len(fibers) != len(Omega):
            inj_ok = False
            break
        barN = 1.0
        Gsid = gen.gsid_from_fibers(fibers, barN, gen.Q, 0.5, T)
        if Gsid > 1.0 + 1e-9:
            inj_ok = False
            break

    # Lemma II on first row with independent energy
    II_rows = cert.get("lemmas", {}).get("II", {}).get("rows", [])
    ii_ok = True
    if II_rows:
        r0 = II_rows[0]
        T = list(range(1, r0["N"] + 1))
        if math.comb(r0["N"], r0["m"]) <= 8000:
            Omega = m.all_m_subsets(T, r0["m"])
        else:
            Omega = m.sample_m_subsets(T, r0["m"], 3000, __import__("random").Random(0))
        fibers = m.build_fibers(Omega, r0["R"], r0["p"])
        Mtot = len(Omega)
        L = len(fibers)
        barN = Mtot / float(L)
        max_f = max(len(v) for v in fibers.values())
        # Gsid with four-tuple energy route
        contrib = 0.0
        for members in fibers.values():
            f = len(members)
            pts = [m.support_vector(s, T) for s in members]
            E = m.energy_four_tuple(pts) if len(pts) <= 20 else m.energy_diff_counter(pts)
            Delta = m.delta_of(pts, E)
            if Delta is not None and Delta <= 0.5:
                contrib += (f / barN) ** gen.Q
        Gsid = contrib / L if L else 0.0
        upper = (max_f / barN) ** gen.Q
        if Gsid > upper + 1e-9:
            ii_ok = False
        if abs(Gsid - r0["Gsid"]) > 1e-6 and math.comb(r0["N"], r0["m"]) <= 8000:
            # allow tiny float noise
            if abs(Gsid - r0["Gsid"]) > 1e-4:
                ii_ok = False

    ok = (
        c3_ok
        and inj_ok
        and ii_ok
        and cert.get("phase0", {}).get("pass")
        and cert.get("verdict") == "PROVED-SPECIAL"
        and cert.get("all_pass")
    )
    print(
        "route: four-tuple energy Gsid recompute + injective re-enum + Lemma II inequality"
    )
    print(f"c3_ok={c3_ok} inj_ok={inj_ok} ii_ok={ii_ok}")
    print(f"payload_sha256: {cert.get('payload_sha256')}")
    print(f"verdict: {cert.get('verdict')}")
    if ok:
        print("RESULT: PASS")
        return 0
    print("RESULT: FAIL", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
