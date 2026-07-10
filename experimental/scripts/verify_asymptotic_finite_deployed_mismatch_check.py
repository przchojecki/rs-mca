#!/usr/bin/env python3
"""Independent checker for asymptotic-vs-finite deployed mismatch audit.

Re-verifies the committed certificate WITHOUT importing the generator.
g* is recomputed by a DIFFERENT numeric route (Newton on
f(g)=H2(rho+g)-beta*g, with regula-falsi fallback), not binary bisection.
Also re-checks a0-a* distances, eps_max, and re-scans asymptotic_rs_mca.tex
for pinned quotes via fresh string search.

Usage:
  python experimental/scripts/verify_asymptotic_finite_deployed_mismatch_check.py --check
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

CERT_REL = Path(
    "experimental/data/certificates/asymptotic-finite-mismatch/"
    "asymptotic_finite_deployed_mismatch.json"
)
PAPER_REL = Path("experimental/asymptotic_rs_mca.tex")

N = 2**21
K_BASE = 2**20
RHO = 0.5
P_KB = 2**31 - 2**24 + 1
P_M31 = 2**31 - 1

# Hard-coded row table (must match cert; not imported from generator).
ROWS: list[dict[str, Any]] = [
    {
        "row_id": "kb_mca",
        "kind": "mca",
        "base_prime": P_KB,
        "a0": 1116047,
        "a1": 1116048,
        "printed_fail_margin_bits": 22.1969,
        "lambda_bits": 128,
    },
    {
        "row_id": "kb_list",
        "kind": "list",
        "base_prime": P_KB,
        "a0": 1116046,
        "a1": 1116047,
        "printed_fail_margin_bits": 22.0109,
        "lambda_bits": 128,
    },
    {
        "row_id": "m31_mca",
        "kind": "mca",
        "base_prime": P_M31,
        "a0": 1116023,
        "a1": 1116024,
        "printed_fail_margin_bits": 3.2589,
        "lambda_bits": 100,
    },
    {
        "row_id": "m31_list",
        "kind": "list",
        "base_prime": P_M31,
        "a0": 1116022,
        "a1": 1116023,
        "printed_fail_margin_bits": 3.0730,
        "lambda_bits": 100,
    },
]

# Absolute tolerances: cert floats are double precision; a* is ~1e6 scale.
TOL_G = 1e-10
TOL_A = 1e-6
TOL_EPS = 1e-15
TOL_RES = 1e-12


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def H2(x: float) -> float:
    if x <= 0.0 or x >= 1.0:
        return 0.0
    return -x * math.log2(x) - (1.0 - x) * math.log2(1.0 - x)


def H2_prime(x: float) -> float:
    """d/dx H2(x) = log2((1-x)/x)."""
    if x <= 0.0 or x >= 1.0:
        return float("nan")
    return math.log2((1.0 - x) / x)


def gstar_newton(rho: float, beta: float, iters: int = 60) -> float:
    """Root of f(g)=H2(rho+g)-beta*g via Newton (NOT bisection).

    Falls back to regula falsi on a bracket if Newton leaves the interval.
    """
    # f(0)=H2(rho)>0 for rho in (0,1); find upper where f becomes negative.
    def f(g: float) -> float:
        return H2(rho + g) - beta * g

    def fp(g: float) -> float:
        return H2_prime(rho + g) - beta

    hi = 1.0 - rho - 1e-12
    if f(0.0) < 0:
        return 0.0
    # Expand until f(hi)<=0 or hit boundary
    probe = min(0.05, hi)
    while f(probe) > 0 and probe < hi:
        probe = min(hi, probe * 1.5 + 1e-3)
    if f(probe) > 0:
        # entire interval positive: g* = 1-rho
        return hi
    lo, hi = 0.0, probe
    g = 0.03  # Newton start near the expected crossing for beta~31, rho=1/2
    for _ in range(iters):
        val = f(g)
        der = fp(g)
        if abs(der) < 1e-18:
            break
        g_new = g - val / der
        if g_new <= lo or g_new >= hi:
            # regula falsi step inside bracket
            flo, fhi = f(lo), f(hi)
            if abs(fhi - flo) < 1e-18:
                break
            g_new = (lo * fhi - hi * flo) / (fhi - flo)
        if f(g_new) >= 0:
            lo = g_new
        else:
            hi = g_new
        if abs(g_new - g) < 1e-15:
            g = g_new
            break
        g = g_new
    # Return the largest point with f>=0 in the final bracket (sup definition)
    if f(g) >= 0:
        return g
    return lo


def near(a: float, b: float, tol: float) -> bool:
    return abs(a - b) <= tol


def paper_scan(root: Path) -> list[str]:
    """Fresh independent quote scan (string contains), no generator import."""
    text = (root / PAPER_REL).read_text(encoding="utf-8")
    needles = [
        r"\label{thm:frontier}",
        r"g^*(\rho,\beta)=\sup\{g\in[0,1-\rho]:H_2(\rho+g)\ge \beta g\}",
        r"\log_2\barN_{n,a_n}",
        "This is an asymptotic theorem.  It intentionally absorbs",
        "those constants are not supplied by the asymptotic argument alone",
        r"\log_2(1/\eps_n)=O(n)",
    ]
    missing = [n for n in needles if n not in text]
    return missing


def check() -> None:
    root = repo_root()
    cert_path = root / CERT_REL
    if not cert_path.is_file():
        raise AssertionError(f"missing cert {CERT_REL}")
    cert = json.loads(cert_path.read_text(encoding="utf-8"))

    # Structural gates
    if cert.get("summary", {}).get("verdict_overall") != "NO ISSUE":
        raise AssertionError("verdict_overall is not NO ISSUE")
    if not cert.get("paper_quote_gate", {}).get("all_ok", False):
        raise AssertionError("paper_quote_gate.all_ok is false")
    efr = cert["entropy_frontier_rows"]
    if efr.get("n") != N or efr.get("rho") != RHO:
        raise AssertionError("n/rho mismatch")
    if not efr.get("all_a0_within_3_of_a_star"):
        raise AssertionError("all_a0_within_3_of_a_star is false")

    by_id = {r["row_id"]: r for r in efr["rows"]}
    if set(by_id) != {r["row_id"] for r in ROWS}:
        raise AssertionError(f"row-id set mismatch: {sorted(by_id)}")

    errors: list[str] = []
    for spec in ROWS:
        rid = spec["row_id"]
        rec = by_id[rid]
        beta = math.log2(spec["base_prime"])
        g = gstar_newton(RHO, beta)
        a_star = (RHO + g) * N
        delta_env = 1.0 - RHO - g
        a0 = spec["a0"]
        dist = a0 - a_star
        eps_max = spec["printed_fail_margin_bits"] / N
        residual = H2(RHO + g) - beta * g

        # Cross-check vs cert (independent recompute)
        if not near(g, rec["g_star"], TOL_G):
            errors.append(f"{rid}: g* cert={rec['g_star']} check={g}")
        if not near(a_star, rec["a_star"], TOL_A):
            errors.append(f"{rid}: a* cert={rec['a_star']} check={a_star}")
        if not near(delta_env, rec["delta_env"], TOL_G):
            errors.append(f"{rid}: delta_env cert={rec['delta_env']} check={delta_env}")
        if not near(dist, rec["a0_minus_a_star"], TOL_A):
            errors.append(f"{rid}: a0-a* cert={rec['a0_minus_a_star']} check={dist}")
        if abs(dist) > 3.0 + 1e-9:
            errors.append(f"{rid}: |a0-a*|={abs(dist)} > 3")
        if not near(eps_max, rec["exp_on_overhead_eps_max_bits_per_symbol"], TOL_EPS):
            errors.append(
                f"{rid}: eps_max cert={rec['exp_on_overhead_eps_max_bits_per_symbol']} check={eps_max}"
            )
        if abs(residual) > TOL_RES:
            errors.append(f"{rid}: |H2(rho+g*)-beta g*|={residual} > {TOL_RES}")
        if rec["a0"] != a0 or rec["a1"] != spec["a1"]:
            errors.append(f"{rid}: a0/a1 mismatch")
        if rec["base_prime"] != spec["base_prime"]:
            errors.append(f"{rid}: base_prime mismatch")
        if rec["kind"] != spec["kind"]:
            errors.append(f"{rid}: kind mismatch")
        if rec["lambda_bits"] != spec["lambda_bits"]:
            errors.append(f"{rid}: lambda_bits mismatch")
        if not rec.get("prize_log_eps_compatible_with_O_n", False):
            errors.append(f"{rid}: prize O(n) flag false")

    missing = paper_scan(root)
    if missing:
        errors.append(f"paper quote scan missing: {missing}")

    # Attack verdicts all NO ISSUE
    for atk in cert.get("attacks", []):
        if atk.get("verdict") != "NO ISSUE":
            errors.append(f"attack not NO ISSUE: {atk.get('failure_mode')}")

    if errors:
        print("RESULT: FAIL")
        for e in errors:
            print(" -", e)
        raise SystemExit(1)

    print("RESULT: PASS")
    print("route: Newton/regula-falsi g* (independent of generator bisection)")
    print("rows_checked:", len(ROWS))
    print("all_a0_within_3_of_a_star: True")
    print("paper_quotes_missing: 0")
    print("verdict_overall: NO ISSUE")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true")
    args = p.parse_args(argv)
    if args.check:
        try:
            check()
            return 0
        except AssertionError as exc:
            print("RESULT: FAIL")
            print(" -", exc)
            return 1
    p.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
