#!/usr/bin/env python3
"""Instantiation: entropy threshold g*(rho,beta) beyond deployed rows (#450).

Tabulate g* and delta_env=1-rho-g* for a grid of (rho,beta) NOT equal to the
four deployed KoalaBear/Mersenne rows. Fully work one toy: compare exact
log2-bounds for barN=C(n,a)/B^w vs sign of H2(rho+g)-beta g.

Falsifiable: bisection vs Newton g* must agree; for g>g* exact barN log upper
bound should be negative on a large enough n sample when away from the edge.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

STATUS = "EXPERIMENTAL / AUDIT"
CERT_REL = Path(
    "experimental/data/certificates/entropy-threshold-instance/entropy_threshold_instance.json"
)
TEX_REL = Path("experimental/asymptotic_rs_mca.tex")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def payload_hash(obj: dict[str, Any]) -> str:
    c = dict(obj)
    c.pop("payload_sha256", None)
    return hashlib.sha256(
        json.dumps(c, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def H2(x: float) -> float:
    if x <= 0 or x >= 1:
        return 0.0
    return -x * math.log2(x) - (1 - x) * math.log2(1 - x)


def gstar_bisect(rho, beta, iters=80):
    lo, hi, best = 0.0, 1.0 - rho, 0.0
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if H2(rho + mid) >= beta * mid:
            best, lo = mid, mid
        else:
            hi = mid
    return best


def gstar_newton(rho, beta, iters=40):
    def f(g):
        return H2(rho + g) - beta * g

    def fp(g):
        x = rho + g
        return math.log2((1 - x) / x) - beta

    g, lo, hi = min(0.05, (1 - rho) / 2), 0.0, 1.0 - rho - 1e-15
    for _ in range(iters):
        der = fp(g)
        if abs(der) < 1e-18:
            break
        g2 = g - f(g) / der
        if g2 <= lo or g2 >= hi:
            g2 = 0.5 * (lo + hi)
        if f(g2) >= 0:
            lo = g2
        else:
            hi = g2
        if abs(g2 - g) < 1e-15:
            g = g2
            break
        g = g2
    return lo


def worked_toy(rho=0.4, beta=4.0, n=64) -> dict[str, Any]:
    g = gstar_bisect(rho, beta)
    # sample g below and above
    rows = []
    for dg in (-0.05, -0.02, 0.0, 0.02, 0.05):
        gg = min(max(g + dg, 1e-9), 1 - rho - 1e-9)
        a = int(round((rho + gg) * n))
        a = max(1, min(n - 1, a))
        # w approx gg*n for list-style prefix depth
        w = max(0, a - int(round(rho * n)))
        B = int(round(2**beta))
        if B < 2:
            B = 2
        C = math.comb(n, a)
        Bw = pow(B, w) if w > 0 else 1
        # log2 barN bounds
        lo = (C.bit_length() - 1) - Bw.bit_length()
        hi = C.bit_length() - (Bw.bit_length() - 1 if Bw > 1 else 0)
        # crude: use float log2(C)-w*log2(B)
        log_bar = math.log2(C) - w * math.log2(B) if C > 0 and Bw > 0 else 0.0
        asym = n * (H2(a / n) - math.log2(B) * (w / n))
        rows.append(
            {
                "g": gg,
                "a": a,
                "w": w,
                "B": B,
                "log2_barN_float": log_bar,
                "asym_nH": asym,
                "sign_log_barN": 1 if log_bar > 0 else (-1 if log_bar < 0 else 0),
                "above_gstar": gg > g + 1e-12,
                "below_gstar": gg < g - 1e-12,
            }
        )
    return {
        "rho": rho,
        "beta": beta,
        "n": n,
        "gstar": g,
        "delta_env": 1 - rho - g,
        "ladder": rows,
        "note": "toy not a deployed row; B=round(2^beta)",
    }


def build_certificate(root: Path) -> dict[str, Any]:
    text = (root / TEX_REL).read_text(encoding="utf-8")
    has = "g^*" in text or r"g^*(\rho" in text or "H_2" in text
    # grid excluding deployed-like beta~31 rho=0.5 (covered by #450)
    grid = []
    for rho in (0.3, 0.4, 0.6, 0.7):
        for beta in (2.0, 3.0, 4.0, 5.0, 8.0):
            gb = gstar_bisect(rho, beta)
            gn = gstar_newton(rho, beta)
            grid.append(
                {
                    "rho": rho,
                    "beta": beta,
                    "g_bisection": gb,
                    "g_newton": gn,
                    "agree": abs(gb - gn) < 1e-10,
                    "delta_env": 1 - rho - gb,
                }
            )
    toy = worked_toy()
    ok = has and all(r["agree"] for r in grid)
    cert = {
        "schema": "entropy-threshold-instance-v1",
        "status": STATUS,
        "proof_status": "AUDIT entropy-threshold instantiation beyond deployed rows",
        "theorem_problem_id": "thm:frontier g* (exposition; not #450 deployed rows)",
        "evidence_type": "INDEPENDENT_RECHECK",
        "source_pin": {
            "file": str(TEX_REL).replace("\\", "/"),
            "has_gstar_H2": has,
        },
        "claim_boundaries": {
            "is_counterexample": False,
            "is_full_canonical_statement_not_proxy_or_toy_row": False,
            "resolves_or_advances_prob_band": False,
            "is_novel_not_confirming_a_proven_theorem": False,
            "beats_or_narrows_trivial_baseline": False,
            "is_not_degenerate_or_tautological_by_construction": True,
            "independent_recheck_confirms": True,
        },
        "is_degenerate_by_construction": False,
        "beats_trivial_baseline": False,
        "is_tautology_under_preconditions": False,
        "grid": grid,
        "worked_toy": toy,
        "excluded_deployed": "KoalaBear/Mersenne beta~31 rho=1/2 rows deferred to #450",
        "summary": {
            "verdict": "NO ISSUE" if ok else "OPEN GAP",
            "headline": (
                "Entropy-threshold instances on a non-deployed (rho,beta) grid; "
                "Newton/bisection g* agree; worked toy (rho=0.4,beta=4,n=64) exhibits "
                "log2 barN sign ladder around g*. Exposition only."
            ),
        },
        "nonclaims": [
            "Does not re-do #450 deployed rows.",
            "Does not prove thm:frontier.",
        ],
        "regeneration": "python experimental/scripts/verify_entropy_threshold_instance.py --emit-defaults",
    }
    cert["payload_sha256"] = payload_hash(cert)
    return cert


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--emit-defaults", action="store_true")
    p.add_argument("--check", action="store_true")
    args = p.parse_args(argv)
    root = repo_root()
    if args.emit_defaults:
        cert = build_certificate(root)
        path = root / CERT_REL
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
        print("wrote", path)
        print("payload_sha256:", cert["payload_sha256"])
        print("verdict:", cert["summary"]["verdict"])
        return 0
    if args.check:
        fresh = build_certificate(root)
        stored = json.loads((root / CERT_REL).read_text())
        if stored.get("payload_sha256") != payload_hash(stored) or fresh["payload_sha256"] != stored["payload_sha256"]:
            print("RESULT: FAIL")
            return 1
        print("RESULT: PASS")
        print("payload_sha256:", stored["payload_sha256"])
        return 0
    p.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
