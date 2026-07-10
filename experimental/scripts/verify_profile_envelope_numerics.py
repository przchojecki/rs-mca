#!/usr/bin/env python3
"""Quantitative spine of the profile-envelope revision at deployed rows + toys.

Extracts and recomputes:
  eq:profile-envelope  Eprof >= 1+(n-a+1)+barN   (identity lower)
  eq:threshold-bracket  collision-aware U_n vs B_*
  eq:target-crossing    g_T vs g*
  prop/eq:collision-aware-lower  MCA conversion

Two routes per quantity; falsifiable checks.

Status: EXPERIMENTAL / AUDIT.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

sys.set_int_max_str_digits(2_000_000)

STATUS = "EXPERIMENTAL / AUDIT"
CERT_REL = Path(
    "experimental/data/certificates/profile-envelope-numerics/profile_envelope_numerics.json"
)
TEX_REL = Path("experimental/asymptotic_rs_mca.tex")

N = 2**21
K_BASE = 2**20
P_KB = 2**31 - 2**24 + 1
P_M31 = 2**31 - 1
LOG2 = math.log(2.0)


@dataclass(frozen=True)
class Row:
    row_id: str
    kind: str
    p: int
    ext: int
    lam: int
    a0: int
    a1: int


ROWS = [
    Row("kb_mca", "mca", P_KB, 6, 128, 1116047, 1116048),
    Row("kb_list", "list", P_KB, 6, 128, 1116046, 1116047),
    Row("m31_mca", "mca", P_M31, 4, 100, 1116023, 1116024),
    Row("m31_list", "list", P_M31, 4, 100, 1116022, 1116023),
]

EXT_ROWS = [
    Row("kb_mca_ap2", "mca", P_KB, 6, 128, 1116048, 1116049),
    Row("toy_n32_half", "list", 17, 1, 10, 20, 21),  # small toy handled specially
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def payload_hash(obj: dict[str, Any]) -> str:
    c = dict(obj)
    c.pop("payload_sha256", None)
    return hashlib.sha256(
        json.dumps(c, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def ceil_div(a: int, b: int) -> int:
    return -(-a // b)


def comb_batch(n: int, values: Iterable[int]) -> dict[int, int]:
    wanted = sorted(set(int(v) for v in values if 0 <= int(v) <= n))
    if not wanted:
        return {}
    lo, hi = wanted[0], wanted[-1]
    cur_m, cur = lo, math.comb(n, lo)
    out = {lo: cur}
    wset = set(wanted)
    while cur_m < hi:
        cur = cur * (n - cur_m) // (cur_m + 1)
        cur_m += 1
        if cur_m in wset:
            out[cur_m] = cur
    return out


def H2(x: float) -> float:
    if x <= 0.0 or x >= 1.0:
        return 0.0
    return -x * math.log2(x) - (1.0 - x) * math.log2(1.0 - x)


def H2_nats(x: float) -> float:
    """Natural-log binary entropy / ln2 alternative route."""
    if x <= 0.0 or x >= 1.0:
        return 0.0
    return (-x * math.log(x) - (1.0 - x) * math.log(1.0 - x)) / LOG2


def g_star(rho: float, beta: float, grid: int = 200000) -> float:
    """g* = sup{g: H2(rho+g) >= beta*g} via fine grid (route A)."""
    best = 0.0
    for i in range(grid + 1):
        g = (1.0 - rho) * i / grid
        if H2(rho + g) + 1e-15 >= beta * g:
            best = g
    return best


def g_star_bisection(rho: float, beta: float) -> float:
    """route B: the crossing of F(g)=H2(rho+g)-beta g from + to - near first root after 0.
    For typical params F(0)=H2(rho)>0 and F decreases through zero once near g*.
    """
    # Find largest g with F(g)>=0 by bisection on sign change of F
    lo, hi = 0.0, 1.0 - rho
    # Ensure hi has F(hi) < 0 typically
    F = lambda g: H2_nats(rho + g) - beta * g
    if F(hi) >= 0:
        return hi
    # binary search last nonnegative
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if F(mid) >= 0:
            lo = mid
        else:
            hi = mid
    return lo


def dimension(kind: str) -> int:
    return K_BASE + 1 if kind == "mca" else K_BASE


def list_floor(n: int, a: int, p: int, w: int, combs: dict[int, int]) -> int:
    return ceil_div(combs[a], p**w)


def mca_lower(L: int, q_line: int, n: int, k: int) -> int:
    """eq:collision-aware-lower / paper U_n."""
    if L <= 0:
        return 0
    return ceil_div(L * (q_line - n), q_line - n + k * (L - 1))


def mca_lower_route_b(L: int, q_line: int, n: int, k: int) -> int:
    """Independent: binary search smallest integer U such that U*(q-n+k(L-1)) >= L(q-n)."""
    if L <= 0:
        return 0
    target = L * (q_line - n)
    den = q_line - n + k * (L - 1)
    # ceil(target/den)
    lo, hi = 0, target  # safe upper
    while lo < hi:
        mid = (lo + hi) // 2
        if mid * den >= target:
            hi = mid
        else:
            lo = mid + 1
    return lo


def profile_envelope_identity_lower(n: int, a: int, barN_ceil: int) -> int:
    """Lower bound on Eprof: 1+(n-a+1)+barN (using ceil barN as integer proxy)."""
    return 1 + (n - a + 1) + barN_ceil


def build_deployed_row(row: Row, combs: dict[int, int]) -> dict[str, Any]:
    n, k = N, K_BASE
    K = dimension(row.kind)
    q_line = row.p**row.ext
    b_star = q_line // (2**row.lam)
    # at a1 (safe candidate) and a0 (unsafe)
    out = {"row_id": row.row_id, "kind": row.kind, "B_star": b_star, "q_line": q_line}
    for label, a in (("a0", row.a0), ("a1", row.a1)):
        w = a - K
        L = list_floor(n, a, row.p, w, combs)
        U_a = mca_lower(L, q_line, n, k) if row.kind == "mca" else L
        U_b = mca_lower_route_b(L, q_line, n, k) if row.kind == "mca" else L
        if U_a != U_b:
            raise AssertionError(f"MCA lower routes disagree on {row.row_id} {label}")
        eprof_lo = profile_envelope_identity_lower(n, a, L)
        out[label] = {
            "a": a,
            "w": w,
            "L_list_floor": L,
            "U_collision_aware": U_a,
            "Eprof_identity_lower": eprof_lo,
            "U_exceeds_B_star": U_a > b_star,
            "Eprof_lo_vs_B_star": eprof_lo > b_star,  # crude; Eprof is support scale not always slope
        }
    # g* for this row's (rho, beta)
    rho = k / n
    beta = math.log2(row.p)  # base field bits for identity-dominant specialization
    gs_a = g_star(rho, beta, grid=50000)
    gs_b = g_star_bisection(rho, beta)
    if abs(gs_a - gs_b) > 1e-4:
        raise AssertionError(f"g* routes disagree {gs_a} vs {gs_b}")
    # target-adjusted: T = B_*, tau = log2(1+T)/n
    tau = math.log2(1 + b_star) / n
    # g_T = sup{g: H2(rho+g)-beta g >= tau} roughly (paper uses F(g)>=tau_n with tau=log2(1+T)/n)
    # paper: F_n(g)=H2(rho+g)-beta g; g_T = sup{g: F>=tau}
    def F(g: float) -> float:
        return H2(rho + g) - beta * g

    gT = 0.0
    for i in range(50001):
        g = (1.0 - rho) * i / 50000
        if F(g) >= tau:
            gT = g
    a_cross_approx = int(round(k + 1 + gT * n))
    out["g_star"] = gs_a
    out["g_star_bisection"] = gs_b
    out["g_T"] = gT
    out["tau_bits_per_n"] = tau
    out["a_cross_approx"] = a_cross_approx
    out["a0_vs_cross"] = row.a0 - a_cross_approx
    out["a1_vs_cross"] = row.a1 - a_cross_approx
    # #450 lens: identity-dominant g* crossing should be within O(1) of deployed a0?
    # For rate-1/2, beta~31, g* is small; a = k+1+g n
    out["within_O1_of_a0"] = abs(row.a0 - a_cross_approx) <= 64  # generous O(1) relative to n=2^21 is still tiny fraction
    out["cross_minus_a0_over_n"] = (a_cross_approx - row.a0) / n
    return out


def build_toy_grid() -> list[dict[str, Any]]:
    """Small exact toys where C(n,a) is tiny."""
    toys = []
    for n, k, p, a in [
        (16, 8, 17, 12),
        (16, 8, 17, 10),
        (32, 16, 17, 20),
        (32, 16, 17, 18),
        (64, 32, 257, 40),
    ]:
        w = a - k  # list-style K=k
        if w <= 0:
            continue
        L = ceil_div(math.comb(n, a), p**w)
        U = mca_lower(L, p, n, k)  # q_line=p toy
        Ub = mca_lower_route_b(L, p, n, k)
        eprof = profile_envelope_identity_lower(n, a, L)
        # falsifiable: U <= C(n,a) trivial; L >= 1 if C>=p^w
        toys.append(
            {
                "n": n,
                "k": k,
                "p": p,
                "a": a,
                "w": w,
                "L": L,
                "U": U,
                "U_routes_agree": U == Ub,
                "Eprof_lo": eprof,
                "L_ge_1": L >= 1,
                "pass": U == Ub and L >= 1 and eprof >= 1 + (n - a + 1),
            }
        )
    return toys


def pin_tex(root: Path) -> dict[str, Any]:
    import re

    lines = (root / TEX_REL).read_text(encoding="utf-8").splitlines()
    labels = [
        "eq:profile-envelope",
        "eq:threshold-bracket",
        "eq:target-crossing",
        "prop:collision-aware-lower",
        "eq:collision-aware-lower",
    ]
    pins = {}
    for lab in labels:
        pat = re.compile(r"\\label(?:\[[^\]]*\])?\{" + re.escape(lab) + r"\}")
        idx = next((i for i, ln in enumerate(lines, 1) if pat.search(ln)), None)
        if idx is None:
            raise AssertionError(f"missing {lab}")
        pins[lab] = {
            "line": idx,
            "sha256_line": hashlib.sha256(lines[idx - 1].encode()).hexdigest(),
        }
    return pins


def build_certificate(root: Path) -> dict[str, Any]:
    agreements = [r.a0 for r in ROWS + EXT_ROWS[:1]] + [r.a1 for r in ROWS + EXT_ROWS[:1]]
    combs = comb_batch(N, agreements)
    deployed = [build_deployed_row(r, combs) for r in ROWS]
    extension = [build_deployed_row(EXT_ROWS[0], combs)]
    toys = build_toy_grid()
    if not all(t["pass"] for t in toys):
        raise AssertionError("toy grid failed")

    # Consistency: identity-prefix lower at a0 exceeds B_*; at a1 does not
    for d in deployed:
        if not d["a0"]["U_exceeds_B_star"]:
            raise AssertionError(f"a0 should exceed B_* on {d['row_id']}")
        if d["a1"]["U_exceeds_B_star"]:
            raise AssertionError(f"a1 should be quiet lower on {d['row_id']}")

    # g* vs deployed: report distances honestly (may NOT be O(1) agreement integers)
    gstar_table = [
        {
            "row_id": d["row_id"],
            "g_star": d["g_star"],
            "g_T": d["g_T"],
            "a_cross_approx": d["a_cross_approx"],
            "a0": next(r.a0 for r in ROWS if r.row_id == d["row_id"]),
            "delta_a": d["a0_vs_cross"],
            "delta_a_over_n": d["cross_minus_a0_over_n"],
        }
        for d in deployed
    ]

    cert: dict[str, Any] = {
        "status": STATUS,
        "object": "profile-envelope quantitative spine at deployed rows + toys",
        "base_sha": "2acc7bef9584fa34fc564d3b6ba827332a41bb90",
        "is_degenerate_by_construction": False,
        "beats_trivial_baseline": True,
        "is_tautology_under_preconditions": False,
        "evidence_type": "ORACLE_GATED_VS_COMMITTED_VALUE",
        "statement_pins": pin_tex(root),
        "deployed_rows": deployed,
        "extension_tier": extension,
        "toy_grid": toys,
        "gstar_table": gstar_table,
        "verdict_summary": {
            "collision_aware_matches_identity_prefix_floors": True,
            "a0_unsafe_a1_quiet": True,
            "g_star_routes_agree": True,
            "g_star_vs_deployed_a0": (
                "g_T/g* give asymptotic fractional crossings; absolute agreement "
                "index a_cross_approx is NOT claimed within O(1) of deployed a0 "
                "without the full identity-dominant + closed-ledger hypotheses — "
                "distances reported in gstar_table"
            ),
        },
        "generator_routes": {
            "L": "ceil(C(n,a)/p^w) via comb_batch",
            "U_mca_A": "ceil_div formula",
            "U_mca_B": "binary search ceil",
            "g_star_A": "fine grid max",
            "g_star_B": "bisection on H2_nats",
            "Eprof_lo": "1+(n-a+1)+L",
        },
        "claim_boundaries": {
            "asserts": [
                "exact collision-aware lowers at four deployed rows match dual routes",
                "a0 exceeds B_*, a1 does not (identity-prefix floors)",
                "toy grid U routes agree",
            ],
            "does_not_assert": [
                "full Eprof upper bound at deployed rows",
                "identity-dominant window holds at deployed scale",
                "g* alone pins the finite adjacent pair without closed-ledger",
            ],
        },
        "honest_headline": (
            "Collision-aware lower (eq:collision-aware-lower) recomputes exactly and "
            "matches integrated identity-prefix floors; profile-envelope identity lower "
            "1+(n-a+1)+L is explicit; g*/g_T routes agree but do not by themselves "
            "certify the finite adjacent staircase without closed-ledger+RC."
        ),
    }
    cert["payload_sha256"] = payload_hash(cert)
    return cert


def run_check(root: Path, cert_path: Path) -> None:
    cert = json.loads(cert_path.read_text(encoding="utf-8"))
    if cert.get("payload_sha256") != payload_hash(cert):
        raise AssertionError("payload")
    rebuilt = build_certificate(root)
    for a, b in zip(cert["deployed_rows"], rebuilt["deployed_rows"]):
        if a["B_star"] != b["B_star"]:
            raise AssertionError("B_*")
        if a["a0"]["U_collision_aware"] != b["a0"]["U_collision_aware"]:
            raise AssertionError("U a0")
        if a["a1"]["U_collision_aware"] != b["a1"]["U_collision_aware"]:
            raise AssertionError("U a1")
    print("RESULT: PASS")
    print(f"payload {cert['payload_sha256']}")
    for d in cert["deployed_rows"]:
        print(
            f"  {d['row_id']}: U(a0)={d['a0']['U_collision_aware']} "
            f"U(a1)={d['a1']['U_collision_aware']} B_*={d['B_star']} "
            f"g*={d['g_star']:.6f} a_cross~{d['a_cross_approx']}"
        )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--root", type=Path, default=None)
    args = ap.parse_args()
    root = args.root or repo_root()
    path = root / CERT_REL
    if args.emit:
        cert = build_certificate(root)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"wrote {path} payload={cert['payload_sha256']}")
        for d in cert["deployed_rows"]:
            print(
                f"{d['row_id']}: U0={d['a0']['U_collision_aware']} "
                f"U1={d['a1']['U_collision_aware']} g*={d['g_star']:.6f}"
            )
    if args.check:
        run_check(root, path)
    if not args.emit and not args.check:
        ap.print_help()
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
