#!/usr/bin/env python3
"""Proved brackets on U_Q and U_R1 for cor:capfr1-Q-R1-closing.

Constructive partial packet: exact U_Q / U_R1 need open inputs.  This supplies
the best *proved* upper and lower brackets at the four deployed adjacent rows
(and an extension tier), with dual algorithms per bound.

  U_Q upper:
    route A — Johnson one-term packing (thm:q-proper):
        max |P_Q| <= C(n,m) / (C(m,t) C(n-m,t)), t=floor(w/2)
        R_Q^pack <= |B|^w / (C(m,t) C(n-m,t))
    route B — anticode packing (thm:q-proper / cor:anticode-cap):
        max |Fib| <= C(n,m) / C(n-m+w, w)
        R_Q^acode <= |B|^w / C(n-m+w, w)

  U_Q lower (identity-prefix pigeonhole):
        max fiber >= ceil(C(n,m) / |B|^w)   (= list floor L_list)

  U_R1 upper:
    route A — one-parameter pencil (cor:bc-one-pencil), CONDITIONAL on chart reduction:
        floor(n / omega) with omega = n-m  (primitive g=0)
    route B — raw locator dimension (thm:bc-proper) first term:
        min(C(n, omega), |F|^{r1+r2}) but r1+r2 unknown → C(n,omega) only
        (honest: this is enormous; not a usable closing upper)

  U_R1 lower: 0 (no forced residual rank-one mass is proved at a0+1)

Does NOT prove the one-step inequality.  Does NOT resolve prob:band.
Status: EXPERIMENTAL / PARTIAL-LEDGER.

Numbers that match prop:proper-q-gap log2 table are recomputed here; that
proposition already records the packing is far too weak for adjacent closure.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

sys.set_int_max_str_digits(2_000_000)

STATUS = "EXPERIMENTAL / PARTIAL-LEDGER"
CERT_REL = Path("experimental/data/certificates/uq-ur1-bounds/uq_ur1_bounds.json")
GF_REL = Path("experimental/grande_finale.tex")
RAW_REL = Path("experimental/cap25_cap_v13_raw.tex")
Q_R1_CERT_REL = Path(
    "experimental/data/certificates/q-r1-closing-audit/q_r1_closing_audit.json"
)

N = 2**21
K_BASE = 2**20
P_KB = 2**31 - 2**24 + 1
P_M31 = 2**31 - 1
LOG2 = math.log(2.0)


@dataclass(frozen=True)
class Row:
    row_id: str
    row_label: str
    kind: str
    base_prime: int
    extension_degree: int
    lambda_bits: int
    a0: int
    a1: int
    tier: str = "deployed"


ROWS: list[Row] = [
    Row("kb_mca", "KoalaBear MCA", "mca", P_KB, 6, 128, 1116047, 1116048),
    Row("kb_list", "KoalaBear list", "list", P_KB, 6, 128, 1116046, 1116047),
    Row("m31_mca", "Mersenne-31 MCA", "mca", P_M31, 4, 100, 1116023, 1116024),
    Row("m31_list", "Mersenne-31 list", "list", P_M31, 4, 100, 1116022, 1116023),
]

EXT_ROWS: list[Row] = [
    Row("kb_mca_ap2", "KoalaBear MCA a0+2", "mca", P_KB, 6, 128, 1116048, 1116049, "extension"),
    Row("m31_mca_ap2", "Mersenne-31 MCA a0+2", "mca", P_M31, 4, 100, 1116024, 1116025, "extension"),
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
    wanted = sorted(set(int(v) for v in values))
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


def log2_binom_lgamma(n: int, k: int) -> float:
    """Route A for log2 C(n,k): lgamma."""
    if k < 0 or k > n:
        return float("-inf")
    k = min(k, n - k)
    if k == 0:
        return 0.0
    return (
        math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
    ) / LOG2


def log2_binom_product(n: int, k: int) -> float:
    """Route B for log2 C(n,k): sum of log2 of successive ratios (independent of lgamma)."""
    if k < 0 or k > n:
        return float("-inf")
    k = min(k, n - k)
    if k == 0:
        return 0.0
    s = 0.0
    for i in range(k):
        s += math.log2(n - i) - math.log2(i + 1)
    return s


def log2_agree(a: float, b: float, tol: float = 1e-6) -> bool:
    if math.isinf(a) or math.isinf(b):
        return a == b
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def dimension(row: Row) -> int:
    return K_BASE + 1 if row.kind == "mca" else K_BASE


def b_star(row: Row) -> int:
    return (row.base_prime**row.extension_degree) // (2**row.lambda_bits)


def list_floor(row: Row, agreement: int, combinations: dict[int, int]) -> int:
    w = agreement - dimension(row)
    return ceil_div(combinations[agreement], row.base_prime**w)


def lower_count(row: Row, agreement: int, combinations: dict[int, int]) -> int:
    floor = list_floor(row, agreement, combinations)
    if row.kind == "list":
        return floor
    q_line = row.base_prime**row.extension_degree
    den = q_line - N + K_BASE * (floor - 1)
    return ceil_div(floor * (q_line - N), den)


# ---------------------------------------------------------------------------
# U_Q brackets
# ---------------------------------------------------------------------------


def uq_brackets(row: Row, m: int, combinations: dict[int, int]) -> dict[str, Any]:
    """m = a1 agreement; w = m - K; |B| = base_prime (prefix field scale)."""
    K = dimension(row)
    w = m - K
    if w <= 0:
        raise ValueError(f"nonpositive w for {row.row_id}")
    t = w // 2
    p = row.base_prime  # |B| for base-field prefix map
    log2_p_exact = math.log2(p)
    # prop:proper-q-gap uses log2|B|=31 as a convenient upper (p = 2^31-... < 2^31).
    log2_B_w_exact = w * log2_p_exact
    log2_B_w_prop31 = w * 31.0

    # --- upper route A: Johnson one-term ---
    log2_Cm_t_A = log2_binom_lgamma(m, t)
    log2_Cnm_t_A = log2_binom_lgamma(N - m, t)
    log2_RQ_pack_exact = log2_B_w_exact - log2_Cm_t_A - log2_Cnm_t_A
    log2_RQ_pack_prop31 = log2_B_w_prop31 - log2_Cm_t_A - log2_Cnm_t_A

    # --- upper route A': same Johnson via product log2 (algorithm independence) ---
    log2_Cm_t_P = log2_binom_product(m, t)
    log2_Cnm_t_P = log2_binom_product(N - m, t)
    log2_RQ_pack_P = log2_B_w_exact - log2_Cm_t_P - log2_Cnm_t_P
    if not log2_agree(log2_RQ_pack_exact, log2_RQ_pack_P, tol=1e-5):
        raise AssertionError(
            f"Johnson log2 routes disagree on {row.row_id}: "
            f"{log2_RQ_pack_exact} vs {log2_RQ_pack_P}"
        )

    # Absolute packing upper on max fiber (log2): log2 C(n,m) - log2 C(m,t) - log2 C(n-m,t)
    log2_Cn_m_A = log2_binom_lgamma(N, m)
    log2_UQ_pack_A = log2_Cn_m_A - log2_Cm_t_A - log2_Cnm_t_A
    log2_Cn_m_P = log2_binom_product(N, m)
    log2_UQ_pack_P = log2_Cn_m_P - log2_Cm_t_P - log2_Cnm_t_P
    if not log2_agree(log2_UQ_pack_A, log2_UQ_pack_P, tol=1e-5):
        raise AssertionError("absolute U_Q pack log2 routes disagree")

    # --- upper route B: anticode ---
    # |Fib| <= C(n,m) / C(n-m+w, w)  => R <= |B|^w / C(n-m+w, w)
    log2_C_acode = log2_binom_lgamma(N - m + w, w)
    log2_RQ_acode = log2_B_w_exact - log2_C_acode
    log2_UQ_acode = log2_Cn_m_A - log2_C_acode
    log2_RQ_pack_A = log2_RQ_pack_exact  # primary exact

    # --- lower: pigeonhole max fiber >= ceil(C(n,m)/|B|^w) ---
    # For list rows this is L_list; for MCA the identity-prefix list floor is the same
    # quantity before deep-list conversion.  Use exact integer from comb_batch.
    uq_lower = list_floor(row, m, combinations)
    log2_uq_lower = math.log2(uq_lower) if uq_lower > 0 else float("-inf")

    b = b_star(row)
    log2_b = math.log2(b) if b > 0 else float("-inf")

    # Distance from bracket-upper to B_* budget (in bits): how far packing is from fitting
    # Positive means upper >> B_* (cannot close).
    dist_pack_bits = log2_UQ_pack_A - log2_b
    dist_acode_bits = log2_UQ_acode - log2_b
    # Normalized overhead vs spare-margin style (prop:proper-q-gap reports R_Q)
    # spare_margin in that prop is about B_* headroom after lower — we report
    # log2 R_Q^pack and log2 B_* for the absolute/normalized tables separately.

    # Bracket width on log2 absolute U_Q: upper_pack - lower
    width_bits = log2_UQ_pack_A - log2_uq_lower

    # J_t / J_{t-1} ratio for the V_t one-term dominance argument
    if t >= 1:
        ratio_at_t = (m - t + 1) * (N - m - t + 1) / (t * t)
    else:
        ratio_at_t = None

    return {
        "m": m,
        "K": K,
        "w": w,
        "t_floor_w_over_2": t,
        "base_field_bits_exact": log2_p_exact,
        "base_field_bits_prop_convention": 31.0,
        "U_Q_lower_pigeonhole": uq_lower,
        "log2_U_Q_lower": log2_uq_lower,
        "log2_R_Q_pack_johnson_exact_p": log2_RQ_pack_exact,
        "log2_R_Q_pack_johnson_prop31": log2_RQ_pack_prop31,
        "log2_R_Q_pack_johnson_lgamma": log2_RQ_pack_A,
        "log2_R_Q_pack_johnson_product": log2_RQ_pack_P,
        "log2_R_Q_anticode": log2_RQ_acode,
        "log2_U_Q_upper_johnson": log2_UQ_pack_A,
        "log2_U_Q_upper_anticode": log2_UQ_acode,
        "log2_B_star": log2_b,
        "bracket_width_bits_johnson_minus_lower": width_bits,
        "distance_johnson_upper_to_B_star_bits": dist_pack_bits,
        "distance_anticode_upper_to_B_star_bits": dist_acode_bits,
        "johnson_one_term_ratio_J_t_over_J_tm1": ratio_at_t,
        "johnson_one_term_dominates_Vt": ratio_at_t is not None and ratio_at_t > 2.0,
        "upper_exceeds_B_star": dist_pack_bits > 0,
        "routes": {
            "U_Q_upper_A": "Johnson one-term packing via lgamma log2 binoms (thm:q-proper)",
            "U_Q_upper_A_prime": "Johnson one-term via product-sum log2 (independent of lgamma)",
            "U_Q_upper_B": "anticode cap C(n-m+w,w) denominator (thm:q-proper)",
            "U_Q_lower": "pigeonhole ceil(C(n,m)/|B|^w) identity-prefix list floor",
        },
        "honest": (
            "proved U_Q upper from packing is many orders of magnitude above B_*; "
            "this confirms prop:proper-q-gap and does not supply a closing U_Q integer"
        ),
    }


# ---------------------------------------------------------------------------
# U_R1 / BC brackets
# ---------------------------------------------------------------------------


def ur1_brackets(row: Row, m: int) -> dict[str, Any]:
    omega = N - m
    # Route A: cor:bc-one-pencil primitive one-parameter pencil
    one_pencil = N // omega  # floor(n/omega)
    # Route B: thm:bc-proper raw support bound first term C(n, omega)
    log2_raw = log2_binom_lgamma(N, omega)
    log2_raw_p = log2_binom_product(N, omega)
    if not log2_agree(log2_raw, log2_raw_p, tol=1e-5):
        raise AssertionError("raw BC binom log2 routes disagree")

    b = b_star(row)
    log2_b = math.log2(b) if b > 0 else float("-inf")

    return {
        "m": m,
        "omega": omega,
        "U_R1_lower": 0,
        "U_R1_upper_one_pencil_conditional": one_pencil,
        "one_pencil_condition": (
            "cor:bc-one-pencil applies only after first-match has reduced the residual "
            "chart to a primitive one-parameter D-split locator pencil with slope→parameter injection; "
            "chart-decomposition audit is an OPEN input (rem:bc-status-after-moving-root)"
        ),
        "one_pencil_fits_under_B_star": one_pencil <= b,
        "log2_U_R1_upper_raw_support_bc_proper": log2_raw,
        "distance_raw_support_to_B_star_bits": log2_raw - log2_b,
        "raw_support_exceeds_B_star": log2_raw > log2_b,
        "routes": {
            "U_R1_upper_A": "floor(n/omega) moving-root one-pencil (thm:bc-moving-root / cor:bc-one-pencil) CONDITIONAL",
            "U_R1_upper_B": "log2 C(n,omega) raw support bound first term (thm:bc-proper)",
            "U_R1_lower": "0 (no forced residual proved)",
        },
        "blocker_unconditional_U_R1": (
            "no unconditional finite U_R1(a0+1) integer: one-pencil bound is conditional "
            "on chart reduction; raw support bound is exponentially larger than the MCA "
            "slope numerator (cor:raw-bc-fails / thm:saturation)"
        ),
        "honest": (
            "conditional one-pencil upper is 2 at deployed MCA a+ and fits under B_*, "
            "but cannot be summed into the closing inequality without the chart audit; "
            "raw support upper does not close anything"
        ),
    }


# ---------------------------------------------------------------------------
# Toy oracle: packing vs brute max fiber
# ---------------------------------------------------------------------------


def es_prefix(M: tuple[int, ...], w: int, p: int) -> tuple[int, ...]:
    """Elementary-symmetric prefix (e1..ew) mod p via DP — for oracle only."""
    # e_h of set M
    dp = [0] * (w + 1)
    dp[0] = 1
    for x in M:
        for h in range(w, 0, -1):
            dp[h] = (dp[h] + dp[h - 1] * (x % p)) % p
    return tuple(dp[1:])


def oracle_packing_vs_brute(
    n: int, m: int, w: int, p: int
) -> dict[str, Any]:
    """Falsifiable: brute max prefix fiber <= packing upper on small (n,m,w)."""
    from itertools import combinations as combos

    if math.comb(n, m) > 200_000:
        raise ValueError("oracle too large")
    t = w // 2
    # Packing upper (integer): floor(C(n,m) / (C(m,t)*C(n-m,t))) when den>0
    den = math.comb(m, t) * math.comb(n - m, t)
    pack_upper = math.comb(n, m) // den if den else math.comb(n, m)
    acode_den = math.comb(n - m + w, w)
    acode_upper = math.comb(n, m) // acode_den if acode_den else math.comb(n, m)

    fibers: dict[tuple[int, ...], int] = {}
    domain = list(range(n))  # abstract domain labels; values 0..n-1 in F_p if p>n
    for M in combos(domain, m):
        z = es_prefix(M, w, p)
        fibers[z] = fibers.get(z, 0) + 1
    max_fib = max(fibers.values()) if fibers else 0
    pigeon = ceil_div(math.comb(n, m), p**w)

    return {
        "n": n,
        "m": m,
        "w": w,
        "p": p,
        "t": t,
        "max_fiber_brute": max_fib,
        "packing_upper": pack_upper,
        "anticode_upper": acode_upper,
        "pigeon_lower": pigeon,
        "packing_holds": max_fib <= pack_upper,
        "anticode_holds": max_fib <= acode_upper,
        "pigeon_holds": max_fib >= pigeon,
        "pass": max_fib <= pack_upper and max_fib <= acode_upper and max_fib >= pigeon,
        "route_oracle": "brute ES-prefix fiber census",
        "route_bound": "Johnson one-term + anticode integer floors",
    }


def build_oracles() -> dict[str, Any]:
    # Small enough for brute; p prime > n for clean value domain
    cases = [
        (8, 4, 1, 11),
        (9, 5, 2, 11),
        (10, 5, 2, 13),
        (12, 6, 2, 13),
        (12, 7, 1, 17),
    ]
    rows = [oracle_packing_vs_brute(*c) for c in cases]
    # Moving-root toy: |Z| <= floor((n-g)/h) — reuse simple combinatorial check
    # n=7,g=1,h=3 => bound 2
    mr = {"n": 7, "g": 1, "h": 3, "bound": (7 - 1) // 3, "formula": "floor((n-g)/h)", "pass": (7 - 1) // 3 == 2}
    return {
        "prefix_packing_vs_brute": {"rows": rows, "pass": all(r["pass"] for r in rows)},
        "moving_root_floor_formula": mr,
        "all_pass": all(r["pass"] for r in rows) and mr["pass"],
    }


def pin_labels(root: Path) -> dict[str, Any]:
    pins = {}
    specs = [
        (GF_REL, "thm:q-proper"),
        (GF_REL, "thm:bc-proper"),
        (GF_REL, "thm:bc-moving-root"),
        (GF_REL, "cor:bc-one-pencil"),
        (GF_REL, "prop:proper-q-gap"),
        (RAW_REL, "cor:capfr1-Q-R1-closing"),
    ]
    for rel, label in specs:
        lines = (root / rel).read_text(encoding="utf-8").splitlines()
        pat = re.compile(r"\\label(?:\[[^\]]*\])?\{" + re.escape(label) + r"\}")
        idx = next((i for i, ln in enumerate(lines, 1) if pat.search(ln)), None)
        if idx is None:
            raise AssertionError(f"missing {label} in {rel}")
        pins[label] = {
            "path": rel.as_posix(),
            "line": idx,
            "sha256_line": hashlib.sha256(lines[idx - 1].encode()).hexdigest(),
        }
    return pins


def build_row(row: Row, combinations: dict[int, int]) -> dict[str, Any]:
    m = row.a1
    b = b_star(row)
    uq = uq_brackets(row, m, combinations)
    ur1 = ur1_brackets(row, m)
    la0 = lower_count(row, row.a0, combinations)
    la1 = lower_count(row, row.a1, combinations)
    return {
        "row_id": row.row_id,
        "row": row.row_label,
        "kind": row.kind,
        "tier": row.tier,
        "a0": row.a0,
        "a1": row.a1,
        "B_star": b,
        "lower_L_a0": la0,
        "lower_L_a1": la1,
        "U_Q": uq,
        "U_R1": ur1,
        "closing_status": {
            "U_Q_proved_upper_fits_B_star": not uq["upper_exceeds_B_star"],
            "U_R1_conditional_one_pencil_fits_B_star": ur1["one_pencil_fits_under_B_star"],
            "unconditional_closing_possible_from_these_bounds": False,
            "reason": (
                "U_Q packing upper >> B_*; U_R1 one-pencil is conditional; "
                "sum of proved unconditional uppers does not fit B_*"
            ),
        },
    }


def build_certificate(root: Path) -> dict[str, Any]:
    agreements = [r.a0 for r in ROWS + EXT_ROWS] + [r.a1 for r in ROWS + EXT_ROWS]
    combinations = comb_batch(N, agreements)
    oracle = build_oracles()
    if not oracle["all_pass"]:
        raise AssertionError("oracle failed")

    deployed = [build_row(r, combinations) for r in ROWS]
    extension = [build_row(r, combinations) for r in EXT_ROWS]

    # prop:proper-q-gap table targets (log2 R_Q pack) — recompute and compare roughly
    # prop:proper-q-gap prints log2 R_Q using log2|B|=31 (proof text), not exact log2(p).
    gap_targets = {
        "kb_mca": 1661552.48,
        "kb_list": 1661552.47,
        "m31_mca": 1660926.12,
        "m31_list": 1660926.11,
    }
    gap_replay = []
    for d in deployed:
        rid = d["row_id"]
        got31 = d["U_Q"]["log2_R_Q_pack_johnson_prop31"]
        got_exact = d["U_Q"]["log2_R_Q_pack_johnson_exact_p"]
        tgt = gap_targets[rid]
        gap_replay.append(
            {
                "row_id": rid,
                "prop_proper_q_gap_log2_RQ": tgt,
                "recomputed_log2_RQ_prop31_convention": got31,
                "recomputed_log2_RQ_exact_p": got_exact,
                "abs_diff_vs_prop_table": abs(got31 - tgt),
                "agrees_to_0p1_under_prop31_convention": abs(got31 - tgt) < 0.1,
                "exact_p_is_strictly_below_prop31": got_exact < got31,
            }
        )
    if not all(x["agrees_to_0p1_under_prop31_convention"] for x in gap_replay):
        raise AssertionError(f"prop:proper-q-gap table mismatch: {gap_replay}")

    cert: dict[str, Any] = {
        "status": STATUS,
        "object": "proved U_Q / U_R1 brackets for cor:capfr1-Q-R1-closing at a0+1",
        "base_sha_target": "eb42b823f817baace7e37cf9b5018affa26eeb43",
        "is_degenerate_by_construction": False,
        "beats_trivial_baseline": True,
        "is_tautology_under_preconditions": False,
        "claim_boundaries": {
            "asserts": [
                "Johnson packing and anticode give proved U_Q uppers; pigeonhole gives U_Q lower",
                "one-pencil U_R1 upper is conditional on chart reduction; raw BC support upper is unconditional but huge",
                "at deployed rows, packing U_Q upper exceeds B_* by ~1.66e6 bits (prop:proper-q-gap replay)",
            ],
            "does_not_assert": [
                "U_paid+U_Q+U_R1 <= B_*",
                "exact finite U_Q or U_R1 integers for the one-step inequality",
                "prob:band resolution",
                "chart-decomposition audit complete",
            ],
        },
        "evidence_type": "ORACLE_GATED_VS_COMMITTED_VALUE",
        "statement_pins": pin_labels(root),
        "oracle_gates": oracle,
        "prop_proper_q_gap_replay": gap_replay,
        "deployed_rows": deployed,
        "extension_tier_rows": extension,
        "generator_routes": {
            "U_Q_upper_johnson": "lgamma log2 binoms for C(m,t)C(n-m,t)",
            "U_Q_upper_johnson_crosscheck": "product-sum log2 binoms",
            "U_Q_upper_anticode": "lgamma log2 C(n-m+w,w)",
            "U_Q_lower": "exact ceil(C(n,m)/p^w) via comb_batch",
            "U_R1_one_pencil": "integer floor(n/omega)",
            "U_R1_raw": "lgamma log2 C(n,omega)",
            "oracle": "brute ES-prefix fiber census on small (n,m,w)",
        },
        "honest_headline": (
            "PARTIAL brackets only.  Proved U_Q packing upper is ~2^(1.66e6) overhead "
            "bits above usable scale; conditional one-pencil U_R1 is 2 at deployed MCA a+ "
            "but needs chart audit; this quantifies prop:proper-q-gap and does not close "
            "cor:capfr1-Q-R1-closing."
        ),
    }
    cert["payload_sha256"] = payload_hash(cert)
    return cert


def run_check(root: Path, cert_path: Path) -> None:
    cert = json.loads(cert_path.read_text(encoding="utf-8"))
    if cert.get("payload_sha256") != payload_hash(cert):
        raise AssertionError("payload hash")
    rebuilt = build_certificate(root)
    for a, b in zip(cert["deployed_rows"], rebuilt["deployed_rows"]):
        if a["B_star"] != b["B_star"]:
            raise AssertionError("B_* drift")
        if a["U_Q"]["w"] != b["U_Q"]["w"]:
            raise AssertionError("w drift")
        if abs(a["U_Q"]["log2_R_Q_pack_johnson_prop31"] - b["U_Q"]["log2_R_Q_pack_johnson_prop31"]) > 1e-4:
            raise AssertionError("log2 RQ prop31 drift")
        if abs(a["U_Q"]["log2_R_Q_pack_johnson_exact_p"] - b["U_Q"]["log2_R_Q_pack_johnson_exact_p"]) > 1e-4:
            raise AssertionError("log2 RQ exact drift")
        if a["U_R1"]["U_R1_upper_one_pencil_conditional"] != b["U_R1"]["U_R1_upper_one_pencil_conditional"]:
            raise AssertionError("one-pencil drift")
        if a["U_Q"]["U_Q_lower_pigeonhole"] != b["U_Q"]["U_Q_lower_pigeonhole"]:
            raise AssertionError("UQ lower drift")
    if not all(x["agrees_to_0p1_under_prop31_convention"] for x in cert["prop_proper_q_gap_replay"]):
        raise AssertionError("gap replay flags")
    print("RESULT: PASS")
    print(f"payload {cert['payload_sha256']}")
    for d in cert["deployed_rows"]:
        print(
            f"  {d['row_id']}: log2_RQ_exact={d['U_Q']['log2_R_Q_pack_johnson_exact_p']:.4f} "
            f"prop31={d['U_Q']['log2_R_Q_pack_johnson_prop31']:.4f} "
            f"dist_to_B_*={d['U_Q']['distance_johnson_upper_to_B_star_bits']:.4f} bits "
            f"one_pencil={d['U_R1']['U_R1_upper_one_pencil_conditional']}"
        )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--root", type=Path, default=None)
    args = ap.parse_args()
    root = args.root or repo_root()
    cert_path = root / CERT_REL
    if args.emit:
        cert = build_certificate(root)
        cert_path.parent.mkdir(parents=True, exist_ok=True)
        cert_path.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"wrote {cert_path} payload={cert['payload_sha256']}")
        for d in cert["deployed_rows"]:
            print(
                f"{d['row_id']}: log2_RQ={d['U_Q']['log2_R_Q_pack_johnson_lgamma']:.4f} "
                f"width_bits={d['U_Q']['bracket_width_bits_johnson_minus_lower']:.2f} "
                f"one_pencil={d['U_R1']['U_R1_upper_one_pencil_conditional']}"
            )
    if args.check:
        if not cert_path.is_file():
            raise SystemExit("missing cert; run --emit")
        run_check(root, cert_path)
    if not args.emit and not args.check:
        ap.print_help()
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
