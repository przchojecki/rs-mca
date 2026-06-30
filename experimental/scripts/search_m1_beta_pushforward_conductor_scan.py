#!/usr/bin/env python3
"""(BETA_2) conductor-growth probe for the M1 good beta-pushforward.

The conditional import (BETA_2) (m1_kummer_weil_import_contract.md) asserts that
the rank-two good beta-pushforward trace has bounded conductor:

    | sum_{(a,beta,r) in Y_G(F_p)} psi(a) phi(beta) chi(d_UV) |  <=  C_beta(e) p,

so the per-prime conductor ratio max_{psi,phi != 1} |G_{psi,phi}| / p should stay
bounded by C_beta(e) as p -> infinity at fixed quotient order e.  The existing
finite audit (verify_m1_beta_pushforward_spectral_audit.py) only checks fixed
(p,e) rows up to p=127.  This script reuses that audit's validated
`good_pushforward_matrix` (the e x e label matrix G_e, an O(p^2) build) and
`spectral_stats` (the 2D DFT giving max|G_{psi,phi}|), and scans FIXED e over a
much larger p range, watching whether the conductor ratio stays bounded (no
counterexample to (BETA_2)) or grows with p (which would refute it).

Two ratios are tracked per (p,e):
  * beta2_ratio     = max_{psi any, phi != 1} |G_{psi,phi}| / p  (pointwise (BETA_2));
  * two_sided_ratio = max_{psi != 1, phi != 1} |G_{psi,phi}| / p (the centered
                      M1 block consumed by the quotient-conic ledger, (BETA_2^avg)).

Status: EXPERIMENTAL / AUDIT (finite numerical evidence, not a proof of (BETA_2)).
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from experimental.scripts.verify_m1_beta_pushforward_spectral_audit import (  # noqa: E402
    good_pushforward_matrix,
    spectral_stats,
)

STATUS = "EXPERIMENTAL"
THEOREM_ID = "M1 (BETA_2) beta-pushforward conductor (m1_kummer_weil_import_contract.md, m1_beta_pushforward_spectral_audit.md)"
OBJECT = "max_{psi,phi!=1} |G_{psi,phi}| / p for the good beta-pushforward, fixed e, growing p"

# audit rows reproduced for validation: (p,e) -> (two_sided/p, beta2/p) from EXPECTED_ROWS.
# The (181,18) and (97,24) anchors are the round-2 fresh quotient orders e=18,24
# (fast small-p representatives; their large-p sample peaks live in the note).
AUDIT_DATAPOINTS = {
    (43, 6): (3.0697674419, 3.2558139535),
    (61, 12): (3.7704918033, 5.0163934426),
    (73, 12): (3.3972602740, 5.5068493151),
    (109, 12): (3.9816513761, 5.6717827398),
    (181, 18): (3.1817736563, 3.7679558011),
    (97, 24): (2.4147368394, 3.6118420031),
}


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def conductor_ratios(p: int, e: int):
    """(two_sided_ratio, beta2_ratio, point_count) for the good beta-pushforward."""
    matrix, point_count = good_pushforward_matrix(p, e)
    _, _, max_two_sided, max_beta2, _ = spectral_stats(matrix)
    return max_two_sided / p, max_beta2 / p, point_count


def scan_fixed_e(e: int, p_min: int, p_max: int, out_path: Path | None = None,
                 verbose: bool = False) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    peak_b2 = 0.0
    peak_ts = 0.0
    for p in range(max(7, p_min), p_max + 1):
        if not is_prime(p) or (p - 1) % e != 0:
            continue
        t = time.monotonic()
        ts, b2, pc = conductor_ratios(p, e)
        peak_b2 = max(peak_b2, b2)
        peak_ts = max(peak_ts, ts)
        rows.append({"p": p, "points": pc, "beta2_ratio": round(b2, 8),
                     "two_sided_ratio": round(ts, 8), "sec": round(time.monotonic() - t, 1)})
        if verbose:
            print(f"e={e} p={p:5d} beta2/p={b2:.6f} two_sided/p={ts:.6f} "
                  f"(peak beta2={peak_b2:.6f}, two_sided={peak_ts:.6f})", flush=True)
        if out_path is not None:
            out_path.write_text(json.dumps(
                {"e": e, "p_min": p_min, "p_max": p_max, "rows": rows,
                 "peak_beta2_ratio": round(peak_b2, 8),
                 "peak_two_sided_ratio": round(peak_ts, 8)}, indent=2), encoding="utf-8")
    return {"e": e, "p_min": p_min, "p_max": p_max,
            "case_count": len(rows),
            "peak_beta2_ratio": round(peak_b2, 8),
            "peak_two_sided_ratio": round(peak_ts, 8),
            "argmax_beta2_p": max(rows, key=lambda r: r["beta2_ratio"])["p"] if rows else None,
            "argmax_two_sided_p": max(rows, key=lambda r: r["two_sided_ratio"])["p"] if rows else None,
            "rows": rows}


def build_certificate() -> Dict[str, Any]:
    # (1) reproduce audit datapoints from the imported functions
    reproduced = {}
    all_ok = True
    for (p, e), (exp_ts, exp_b2) in AUDIT_DATAPOINTS.items():
        ts, b2, pc = conductor_ratios(p, e)
        ok = abs(ts - exp_ts) < 1e-6 and abs(b2 - exp_b2) < 1e-6
        all_ok = all_ok and ok
        reproduced[f"p{p}_e{e}"] = {
            "points": pc, "two_sided_ratio": round(ts, 10), "beta2_ratio": round(b2, 10),
            "expected_two_sided": exp_ts, "expected_beta2": exp_b2, "ok": ok,
        }
    # (2) a small deterministic extended trend (e=6, p<=151) as a reproducibility anchor
    trend = scan_fixed_e(6, 7, 151)
    return {
        "status": STATUS,
        "theorem_id": THEOREM_ID,
        "object": OBJECT,
        "method": "reuse good_pushforward_matrix + spectral_stats (validated audit), scan fixed e over growing p",
        "audit_datapoints_reproduced": reproduced,
        "all_audit_datapoints_ok": all_ok,
        "extended_trend_e6_p151": {
            "case_count": trend["case_count"],
            "peak_beta2_ratio": trend["peak_beta2_ratio"],
            "peak_two_sided_ratio": trend["peak_two_sided_ratio"],
        },
    }


def render(cert: Dict[str, Any]) -> str:
    return json.dumps(cert, indent=2, sort_keys=True) + "\n"


def selftest() -> bool:
    ts, b2, pc = conductor_ratios(43, 6)
    ok = pc == 1568 and abs(ts - 3.0697674419) < 1e-6 and abs(b2 - 3.2558139535) < 1e-6
    print(f"[selftest] (43,6) points={pc} two_sided/p={round(ts,10)} beta2/p={round(b2,10)} -> {'OK' if ok else 'FAIL'}")
    return ok


def main() -> int:
    ap = argparse.ArgumentParser(description="(BETA_2) beta-pushforward conductor scan.")
    ap.add_argument("--certificate", action="store_true")
    ap.add_argument("--output", type=Path)
    ap.add_argument("--check", type=Path)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--scan", action="store_true")
    ap.add_argument("--e", type=int, default=6)
    ap.add_argument("--p-min", type=int, default=7)
    ap.add_argument("--p-max", type=int, default=300)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return 0 if selftest() else 1
    if args.check is not None:
        if args.check.read_text(encoding="utf-8") != render(build_certificate()):
            raise SystemExit(f"certificate mismatch: {args.check}")
        print(f"certificate matches: {args.check}")
        return 0
    if args.certificate or args.output is not None:
        cert = build_certificate()
        rendered = render(cert)
        if args.output is not None:
            args.output.write_text(rendered, encoding="utf-8")
        print(rendered, end="")
        return 0 if cert["all_audit_datapoints_ok"] else 1

    res = scan_fixed_e(args.e, args.p_min, args.p_max, verbose=not args.json)
    if args.json:
        print(json.dumps(res, indent=2, sort_keys=True))
    else:
        print(f"e={args.e} p<= {args.p_max}: cases={res['case_count']} "
              f"peak_beta2/p={res['peak_beta2_ratio']} (p={res['argmax_beta2_p']}) "
              f"peak_two_sided/p={res['peak_two_sided_ratio']} (p={res['argmax_two_sided_p']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
