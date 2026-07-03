#!/usr/bin/env python3
"""Certify the A407/A408 residual-design exact rows and A407 budget gate.

This is a narrow, high-agreement M1/M2 support-wise LD_sw certificate.  It
packages only the A=408 and A=407 rows proved by the A409
saturated-triple/high-neighbor/moment method and deliberately stops at A=406,
where the same method fails.

The verifier checks:
  * the residual-design moment inequalities for A=408 and A=407;
  * the first failure diagnostics at A=406 for this exact method;
  * the exact-budget prime p=27168*2^120+1 with Lucas primality witness 11;
  * the A407 safe / A406 unsafe 2^-128 finite-slope gate;
  * generated JSON/report/site-row artifacts byte-for-byte under --check.
"""
from __future__ import annotations

import argparse
import json
from math import comb, gcd
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

N = 512
K = 256
R = N - K
PERIOD = 1536  # lcm(512,3), sufficient for balanced degrees and floor(m/3).
EPS_EXP = 128
P_MULT = 27168
P = P_MULT * (2**120) + 1
PRIME_FACTORS_P_MINUS_1 = {2: 125, 3: 1, 283: 1}
LUCAS_WITNESS = 11
BUDGET = 106
AUTHOR = "Codex audit"
ROOT = Path(__file__).resolve().parents[2]
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "m1-a407-a408-residual-design-threshold-v1"
CERT_PATH = CERT_DIR / "m1_a407_a408_residual_design_threshold_v1.json"
WITNESS_PATH = CERT_DIR / "tangent_witness_A408_A407_A406_v1.json"
CERT_README_PATH = CERT_DIR / "README.md"
REPORT_PATH = ROOT / "experimental" / "notes" / "certificate_scanner" / "outputs" / "m1_a407_a408_residual_design_threshold_v1.report.md"
FRONTIER_ENTRY_PATH = ROOT / "site" / "data" / "frontier_prime_a406_a407_adjacent_gate.entry.json"
UPDATES_ENTRY_PATH = ROOT / "site" / "data" / "updates_m1_a407_a408_residual_design_threshold.entry.json"


def choose(n: int, k: int) -> int:
    if k < 0 or n < k:
        return 0
    return comb(n, k)


def phi(m: int, d: int) -> int:
    return choose(d, 2) * (m - d) + 2 * choose(d, 3)


def phi_second_difference(m: int, d: int) -> int:
    """Return phi(d+2)-2phi(d+1)+phi(d) for the third-moment kernel."""
    return phi(m, d + 2) - 2 * phi(m, d + 1) + phi(m, d)


def check_phi_convexity_formula(m: int) -> bool:
    """Check the exact discrete-convexity identity on the full degree domain."""
    return all(phi_second_difference(m, d) == m - d - 2 and phi_second_difference(m, d) >= 0 for d in range(0, m - 1))


def balanced_lower(j: int, m: int) -> Tuple[int, int, int]:
    total = j * m
    q, s = divmod(total, N)
    return (N - s) * phi(m, q) + s * phi(m, q + 1), q, s


def balanced_minimizer_certificate(j: int, m: int) -> Dict[str, object]:
    """Certificate that the balanced degrees minimize the separable kernel.

    For fixed m and total degree j*m, the third-moment lower bound is the
    minimum of sum_x phi_m(d_x).  The kernel is discretely convex because
    phi_m(d+2)-2phi_m(d+1)+phi_m(d)=m-d-2 >= 0 for 0 <= d <= m-2.  Hence the
    exchange argument forces minimizers to have degrees differing by at most 1.
    """
    total = j * m
    q, s = divmod(total, N)
    return {
        "m": m,
        "total_degree": total,
        "balanced_low_degree": q,
        "balanced_high_degree": q + 1,
        "balanced_high_count": s,
        "balanced_low_count": N - s,
        "kernel_second_difference_formula": "phi_m(d+2)-2*phi_m(d+1)+phi_m(d)=m-d-2",
        "kernel_convexity_domain": "0 <= d <= m-2",
        "kernel_convexity_formula_checked_for_this_m": check_phi_convexity_formula(m),
        "exchange_conclusion": "For fixed total degree, the minimum is attained by degrees q and q+1.",
    }


def finite_differences(vals: List[int]) -> List[int]:
    if len(vals) != 4:
        raise ValueError("need four values")
    return [
        vals[0],
        vals[1] - vals[0],
        vals[2] - 2 * vals[1] + vals[0],
        vals[3] - 3 * vals[2] + 3 * vals[1] - vals[0],
    ]


def row_parameters(A: int) -> Dict[str, int]:
    j = N - A
    pair_trigger = 3 * j - R
    return {
        "A": A,
        "j": j,
        "tau": K + j,
        "target_j_plus_1": j + 1,
        "pair_trigger": pair_trigger,
        "pair_cap_no_paid_exit": pair_trigger - 1,
        "compact_T_paid_cap": R - j,
    }


def classify_compact_nonexiting_triples(j: int) -> List[Dict[str, int | List[int]]]:
    """Enumerate three-complement Venn types surviving pair and triple paid exits."""
    pair_cap = 3 * j - R - 1
    compact_t_paid_cap = R - j
    if pair_cap < 0:
        return []
    out: List[Dict[str, int | List[int]]] = []
    for q in range(min(j, pair_cap) + 1):
        max_pair_only = pair_cap - q
        for a12 in range(max_pair_only + 1):
            for a13 in range(max_pair_only + 1):
                if a12 + a13 + q > j:
                    continue
                for a23 in range(max_pair_only + 1):
                    if a12 + a23 + q > j or a13 + a23 + q > j:
                        continue
                    p12, p13, p23 = a12 + q, a13 + q, a23 + q
                    pair_sum = p12 + p13 + p23
                    union = 3 * j - pair_sum + q
                    t2 = pair_sum - 2 * q
                    if union <= R and t2 >= compact_t_paid_cap + 1:
                        out.append(
                            {
                                "q": q,
                                "pair_intersections": [p12, p13, p23],
                                "sorted_pair_intersections": sorted([p12, p13, p23]),
                                "union": union,
                                "t2": t2,
                                "delta": 3 * j - union,
                            }
                        )
    return out


def unique_type_tuples(types: Iterable[Dict[str, int | List[int]]]) -> List[Tuple[int, Tuple[int, int, int], int, int, int]]:
    return sorted(
        {
            (
                int(t["q"]),
                tuple(int(x) for x in t["sorted_pair_intersections"]),
                int(t["union"]),
                int(t["t2"]),
                int(t["delta"]),
            )
            for t in types
        }
    )


def first_degree_violation(j: int, high_threshold: int, q_max: int) -> Optional[Dict[str, int]]:
    """Find the first high-neighbor degree impossible inside one j-set."""
    for d in range(1, j + 2):
        lower = d * high_threshold - choose(d, 2) * q_max
        if lower > j:
            return {"first_forbidden_degree_plus_one": d, "union_lower_bound": lower}
    return None


def residue_proof(
    j: int,
    pair_cap: int,
    sat_delta_cap: int,
    max_degree: int,
    threshold_m: int,
) -> Tuple[bool, Dict[str, object]]:
    triangle_factor = choose(max_degree, 2)

    def saturated_triple_bound(m: int) -> int:
        return (m * triangle_factor) // 3

    def upper(m: int) -> int:
        return pair_cap * choose(m, 3) + (sat_delta_cap - pair_cap) * saturated_triple_bound(m)

    min_record: Optional[Dict[str, object]] = None
    failing: Optional[Dict[str, object]] = None
    sample_records: List[Dict[str, object]] = []
    for residue in range(PERIOD):
        t0 = 0 if residue >= threshold_m else 1
        ms = [PERIOD * (t0 + s) + residue for s in range(4)]
        values = [balanced_lower(j, m)[0] - upper(m) for m in ms]
        diffs = finite_differences(values)
        record = {"residue": residue, "t0": t0, "m0": ms[0], "values": values, "diffs": diffs}
        if values[0] <= 0 or any(d < 0 for d in diffs[1:]):
            failing = record
            break
        if min_record is None or values[0] < int(min_record["margin"]):
            min_record = {"residue": residue, "t0": t0, "m0": ms[0], "margin": values[0], "diffs": diffs}
        if residue in (0, threshold_m, PERIOD - 1):
            sample_records.append(record)

    if failing is not None:
        return False, {"failing_residue": failing}

    first_lower, first_q, first_rem = balanced_lower(j, threshold_m)
    first_upper = upper(threshold_m)
    prev_m = threshold_m - 1
    prev_lower, prev_q, prev_rem = balanced_lower(j, prev_m)
    prev_upper = upper(prev_m)
    return True, {
        "period": PERIOD,
        "threshold_m": threshold_m,
        "no_paid_residual_bound": threshold_m - 1,
        "first_forbidden": {
            "m": threshold_m,
            "balanced_lower": first_lower,
            "upper": first_upper,
            "margin": first_lower - first_upper,
            "balanced_q": first_q,
            "balanced_remainder": first_rem,
            "balanced_minimizer_certificate": balanced_minimizer_certificate(j, threshold_m),
        },
        "previous_m": {
            "m": prev_m,
            "balanced_lower": prev_lower,
            "upper": prev_upper,
            "margin": prev_lower - prev_upper,
            "balanced_q": prev_q,
            "balanced_remainder": prev_rem,
            "balanced_minimizer_certificate": balanced_minimizer_certificate(j, prev_m),
        },
        "min_residue_start_record": min_record,
        "sample_residue_records": sample_records,
    }


def find_moment_threshold(j: int, pair_cap: int, sat_delta_cap: int, max_degree: int, max_threshold: int) -> Tuple[Optional[int], Optional[Dict[str, object]]]:
    for threshold_m in range(1, max_threshold + 1):
        ok, proof = residue_proof(j, pair_cap, sat_delta_cap, max_degree, threshold_m)
        if ok:
            return threshold_m, proof
    return None, None


def analyze_row(A: int, max_threshold: int = 256) -> Dict[str, object]:
    params = row_parameters(A)
    j = params["j"]
    pair_trigger = params["pair_trigger"]
    pair_cap = params["pair_cap_no_paid_exit"]
    target = params["target_j_plus_1"]
    labelled_types = classify_compact_nonexiting_triples(j)
    unique_types = unique_type_tuples(labelled_types)
    row: Dict[str, object] = {
        "parameters": params,
        "saturated_triple_classification": {
            "labelled_type_count": len(labelled_types),
            "unique_type_count": len(unique_types),
        },
    }
    if unique_types:
        high_threshold = min(min(pairs) for _q, pairs, _u, _t2, _delta in unique_types)
        q_max = max(q for q, _pairs, _u, _t2, _delta in unique_types)
        sat_delta_cap = max(delta for _q, _pairs, _u, _t2, delta in unique_types)
        row["saturated_triple_classification"].update(
            {
                "high_edge_threshold": high_threshold,
                "q_max": q_max,
                "sat_delta_cap": sat_delta_cap,
                "min_delta": min(delta for _q, _pairs, _u, _t2, delta in unique_types),
                "sample_unique_types": [
                    {"q": q, "sorted_pair_intersections": list(pairs), "union": union, "t2": t2, "delta": delta}
                    for q, pairs, union, t2, delta in unique_types[:12]
                ],
            }
        )
    else:
        high_threshold = pair_cap
        q_max = 0
        sat_delta_cap = pair_cap
        row["saturated_triple_classification"].update(
            {"high_edge_threshold": None, "q_max": None, "sat_delta_cap": sat_delta_cap, "sample_unique_types": []}
        )

    if unique_types and 2 * high_threshold < pair_trigger:
        row["status"] = "FAIL_HIGH_NEIGHBOR_COMPACTNESS"
        row["failure"] = {"reason": "Two high-neighbor edges no longer force a compact triple.", "check": f"2*{high_threshold} < {pair_trigger}"}
        return row

    degree_violation = first_degree_violation(j, high_threshold, q_max)
    if degree_violation is None:
        row["status"] = "FAIL_HIGH_NEIGHBOR_DEGREE_BOUND"
        row["failure"] = {
            "reason": "The inclusion-exclusion degree argument gives no finite high-neighbor bound.",
            "high_edge_threshold": high_threshold,
            "q_max": q_max,
            "best_three_neighbor_lower_bound": 3 * high_threshold - 3 * q_max,
            "base_set_size_j": j,
        }
        return row

    max_degree = int(degree_violation["first_forbidden_degree_plus_one"]) - 1
    row["high_neighbor_graph"] = {
        "max_degree_bound": max_degree,
        "degree_forbidden_check": degree_violation,
        "triangle_bound": f"floor(m*C({max_degree},2)/3)",
    }
    threshold_m, proof = find_moment_threshold(j, pair_cap, sat_delta_cap, max_degree, max_threshold)
    if threshold_m is None or proof is None:
        row["status"] = "FAIL_MOMENT_THRESHOLD"
        row["failure"] = {"reason": "No finite-difference moment threshold was found.", "max_threshold": max_threshold}
        return row

    no_paid_bound = threshold_m - 1
    row["moment_inequality"] = proof
    row["conclusions"] = {
        "no_paid_residual_size_bound": no_paid_bound,
        "paid_exit_size_bound": target,
        "proves_exact_row_by_tangent_lower": no_paid_bound <= target,
        "LD_sw_exact_if_tangent_lower": target if no_paid_bound <= target else None,
    }
    row["status"] = "PROVES_EXACT_ROW_BY_A409_METHOD" if no_paid_bound <= target else "FAIL_NO_PAID_BOUND_EXCEEDS_TARGET"
    return row


def lucas_prime_certificate() -> Dict[str, object]:
    product = 1
    for q, e in PRIME_FACTORS_P_MINUS_1.items():
        product *= q**e
    checks = {}
    for q in sorted(PRIME_FACTORS_P_MINUS_1):
        value = pow(LUCAS_WITNESS, (P - 1) // q, P)
        checks[str(q)] = {"pow": value, "not_one": value != 1, "gcd_minus_one_p": gcd(value - 1, P)}
    fermat = pow(LUCAS_WITNESS, P - 1, P)
    ok = product == P - 1 and fermat == 1 and all(v["not_one"] and v["gcd_minus_one_p"] == 1 for v in checks.values())
    return {
        "p": P,
        "p_expression": "27168*2^120+1",
        "bit_length": P.bit_length(),
        "p_minus_1_factorization": "2^125 * 3 * 283",
        "factorization_product_matches": product == P - 1,
        "lucas_witness": LUCAS_WITNESS,
        "fermat_pow": fermat,
        "prime_factors_checked": checks,
        "lucas_primality_certificate_passes": ok,
        "p_mod_512": P % 512,
        "subgroup_generator_h": pow(LUCAS_WITNESS, (P - 1) // N, P),
        "h_order_512_checks": {
            "h^512_mod_p": pow(pow(LUCAS_WITNESS, (P - 1) // N, P), N, P),
            "h^256_mod_p": pow(pow(LUCAS_WITNESS, (P - 1) // N, P), N // 2, P),
        },
    }


def tangent_witness() -> Dict[str, object]:
    witnesses = []
    for A in [408, 407, 406]:
        j = N - A
        witnesses.append(
            {
                "A": A,
                "j": j,
                "claimed_bad_slopes": j + 1,
                "core_size": A - 1,
                "moving_coordinates": j + 1,
                "construction": "Choose a core C0 of size A-1 and j+1 outside points x_i. On C0 set f=g=0. At x_i set g(x_i)=1 and f(x_i)=-z_i for distinct slopes z_i. Then f+z_i g agrees with the zero codeword on C0 union {x_i}.",
                "noncontainment_check": "On each exact support, g has A-1 >= k zeros and one nonzero value, so g restricted to the support is not a degree-<k RS word.",
            }
        )
    return {"status": "SYMBOLIC_TANGENT_MOVING_ROOT_WITNESS", "field_requirement": "at least 512 distinct domain points and j+1 distinct finite slopes", "witnesses": witnesses}


def frontier_entry() -> Dict[str, object]:
    return {
        "id": "prime-a406-a407-adjacent-gate",
        "title": "Prime-field A406/A407 adjacent threshold row",
        "short": "Residual-design sweep plus the tangent floor pins a new finite-slope gate 19 grid points below the A425/A426 row.",
        "row": "RS[F_p,H,256], p=27168*2^120+1",
        "n": 512,
        "k": 256,
        "rho": 0.5,
        "agreement": 406,
        "badSlopes": "107",
        "q": str(P),
        "status": "proved",
        "tag": "proved",
        "label": "exact finite-slope gate",
        "radiusLabel": "53/256",
        "proof": "The residual-design sweep proves LD_sw(RS[F,D,256],407)=106 and LD_sw(RS[F,D,256],408)=105 for every 512-point RS domain. The moving-root tangent witness gives LD_sw(C,406)>=107. For p=27168*2^120+1, p is prime, p is 1 mod 512, and 106*2^128 < p < 107*2^128, so A=407 is safe and A=406 is the first unsafe closed-grid finite-slope point.",
        "nonclaims": "Finite-slope support-wise MCA / LD_sw only. Not ordinary list decoding, not interleaved-list safety, not protocol soundness, not an exact A406 value, and not based on the false global RNC Fano-line route.",
        "links": [
            {"label": "A407/A408 residual-design threshold note", "href": "https://github.com/przchojecki/rs-mca/blob/main/experimental/notes/m1/m1_a407_a408_residual_design_threshold_v1.md"},
            {"label": "A407/A408 certificate data", "href": "https://github.com/przchojecki/rs-mca/tree/main/experimental/data/certificates/m1-a407-a408-residual-design-threshold-v1"},
            {"label": "Scanner report", "href": "https://github.com/przchojecki/rs-mca/blob/main/experimental/notes/certificate_scanner/outputs/m1_a407_a408_residual_design_threshold_v1.report.md"},
        ],
        "authors": f"residual-design notes / {AUTHOR}",
    }


def updates_entry() -> Dict[str, object]:
    return {
        "date": "2026-07-03",
        "status": "proved threshold row / M1 residual design",
        "author": AUTHOR,
        "title": "A407/A408 residual-design exact rows and budget-106 gate",
        "summary": "The A409 residual-design method proves exact support-wise finite-slope numerators LD_sw(408)=105 and LD_sw(407)=106 for every 512-point rate-half RS domain. For the prime p=27168*2^120+1, this pins a new adjacent finite-slope MCA gate: A=407 is safe and A=406 is unsafe.",
        "impact": "Moves the prime-field rate-1/2 finite-slope MCA gate from A425/A426 down to A406/A407 for a smooth budget-106 prime row; deliberately does not claim A406 exactness or M1 closure.",
        "href": "https://github.com/przchojecki/rs-mca/blob/main/experimental/notes/m1/m1_a407_a408_residual_design_threshold_v1.md",
    }


def build_certificate() -> Dict[str, object]:
    rows = [analyze_row(A) for A in [408, 407, 406]]
    proved_rows = [r for r in rows if str(r["status"]).startswith("PROVES_")]
    prime = lucas_prime_certificate()
    gate = {
        "status": "PROVED_ADJACENT_THRESHOLD_ROW",
        "safe_A": 407,
        "unsafe_A": 406,
        "safe_delta": "105/512",
        "unsafe_delta": "53/256",
        "safe_LD_sw": 106,
        "unsafe_tangent_lower": 107,
        "floor_p_minus_1_over_2^128": (P - 1) // (2**EPS_EXP),
        "floor_p_over_2^128": P // (2**EPS_EXP),
        "safe_strict_check_106_times_2^128_lt_p": 106 * (2**EPS_EXP) < P,
        "unsafe_strict_check_107_times_2^128_gt_p": 107 * (2**EPS_EXP) > P,
        "safe_margin_p_minus_106_2^128": P - 106 * (2**EPS_EXP),
        "unsafe_margin_107_2^128_minus_p": 107 * (2**EPS_EXP) - P,
        "q_gen": str(P),
        "q_line": str(P),
        "q_chal": "not protocol-bound",
    }
    exact_values = {"408": 105, "407": 106}
    return {
        "status": "PROVED_A407_A408_EXACT_AND_A407_PUBLIC_GATE",
        "object": "finite-slope support-wise LD_sw / MCA line-slope numerator",
        "parameters": {"n": N, "k": K, "r": R, "rho": "1/2", "epsilon_target": "2^-128"},
        "theorem": {
            "universal_exact_rows": "For every finite field F and every distinct 512-point RS domain D, LD_sw(RS[F,D,256],408)=105 and LD_sw(RS[F,D,256],407)=106.",
            "public_gate": "For p=27168*2^120+1 and H the order-512 subgroup of F_p^*, A=407 is safe and A=406 is unsafe at the 2^-128 finite-slope support-wise MCA threshold.",
            "proof_dependencies": [
                "Exact-support reduction for support-wise noncontained finite-slope witnesses when A>=k+1, after contained/common-code-line branches are separated.",
                "Per-support uniqueness for noncontained finite slopes.",
                "Moving-root tangent lower witness LD_sw >= n-A+1.",
                "RS uniqueness from k common coordinates in compact triples and common-code-line branches.",
            ],
            "nonclaims": [
                "No A406 exact upper bound is claimed.",
                "No M1 closure is claimed.",
                "No ordinary list-decoding or interleaved-list claim is made.",
                "No protocol q_chal soundness claim is made.",
                "No use is made of the false global RNC Fano-line classification.",
            ],
            "exact_support_reduction": "Uses the repo's support-wise RS/MDS exact-support reduction for A>=k+1: a bad slope may be represented by an exact A-subset witness unless it has already fallen into a contained/common-code-line branch.",
        },
        "prime": prime,
        "gate": gate,
        "exact_values": exact_values,
        "rows": rows,
        "proved_rows_summary": [
            {
                "A": int(r["parameters"]["A"]),
                "j": int(r["parameters"]["j"]),
                "LD_sw_exact": r["conclusions"]["LD_sw_exact_if_tangent_lower"],
                "no_paid_residual_size_bound": r["conclusions"]["no_paid_residual_size_bound"],
                "moment_threshold_m": r["moment_inequality"]["threshold_m"],
            }
            for r in proved_rows
        ],
        "first_failure_of_this_method": rows[-1],
    }


def report(cert: Dict[str, object]) -> str:
    lines = [
        "# M1 A407/A408 residual-design threshold v1",
        "",
        f"Status: `{cert['status']}`.",
        "",
        "This packet proves the two exact rows reached by the A409 saturated-triple/high-neighbor/moment method and uses A407 as an exact-budget public threshold row. It deliberately stops at A406, where this exact method fails.",
        "",
        "## Main theorem",
        "",
        "```text",
        "For every finite field F and every distinct 512-point RS domain D,",
        "LD_sw(RS[F,D,256],408) = 105,",
        "LD_sw(RS[F,D,256],407) = 106.",
        "```",
        "",
        "The matching lower bounds are the moving-root tangent witnesses recorded in the witness JSON. The upper bounds are certified by the residual-design sweep below.",
        "",
        "## Imported proof dependencies",
        "",
        "The proof note states proof sketches for these repo-standard RS/MDS reductions:",
        "",
        "1. Exact-support reduction for support-wise noncontained finite-slope witnesses when `A >= k+1`, after contained/common-code-line branches are separated.",
        "2. Per-support uniqueness for noncontained finite slopes.",
        "3. Moving-root tangent lower witness `LD_sw >= n-A+1`.",
        "4. RS uniqueness from `k` common coordinates in compact triples and common-code-line branches.",
        "",
        "## Public threshold row",
        "",
        "```text",
        f"p = {cert['prime']['p_expression']}",
        f"  = {cert['prime']['p']}",
        "p - 1 = 2^125 * 3 * 283",
        f"Lucas/primitive-root witness = {cert['prime']['lucas_witness']}",
        f"floor((p-1)/2^128) = {cert['gate']['floor_p_minus_1_over_2^128']}",
        "106*2^128 < p < 107*2^128",
        "p == 1 mod 512",
        "```",
        "",
        "Therefore for `C = RS[F_p,H,256]`, with `H` the order-512 subgroup:",
        "",
        "```text",
        "A=407: LD_sw(C,407)=106, safe at delta=105/512.",
        "A=406: LD_sw(C,406)>=107, unsafe at delta=53/256.",
        "```",
        "",
        "This pins the closed-grid finite-slope support-wise MCA gate between A=406 and A=407 for this prime row.",
        "",
        "## Residual-design rows",
        "",
        "| A | j | exact LD_sw | no-paid residual bound | first forbidden m |",
        "|---:|---:|---:|---:|---:|",
    ]
    for row in cert["proved_rows_summary"]:
        lines.append(f"| {row['A']} | {row['j']} | {row['LD_sw_exact']} | {row['no_paid_residual_size_bound']} | {row['moment_threshold_m']} |")
    failure = cert["first_failure_of_this_method"]
    fparams = failure["parameters"]
    lines.extend(
        [
            "",
            "## First failure of this method",
            "",
            "```text",
            f"A={fparams['A']}, j={fparams['j']}",
            f"pair_trigger={fparams['pair_trigger']}",
            f"pair_cap={fparams['pair_cap_no_paid_exit']}",
            f"compact_T_paid_cap={fparams['compact_T_paid_cap']}",
            f"status={failure['status']}",
            f"reason={failure.get('failure',{}).get('reason')}",
            "```",
            "",
            "So this is not an A406 exact theorem and not an M1 closure. The A406 unsafe side used for the public gate is only the tangent lower witness `LD_sw >= 107`.",
            "",
            "## Third-moment minimizer certificate",
            "",
            "For fixed family size `m`, the coordinate-degree kernel is",
            "",
            "```text",
            "phi_m(d) = binom(d,2)(m-d) + 2 binom(d,3).",
            "```",
            "",
            "The verifier records the identity",
            "",
            "```text",
            "phi_m(d+2) - 2 phi_m(d+1) + phi_m(d) = m-d-2 >= 0",
            "```",
            "",
            "for `0 <= d <= m-2`, so the standard exchange argument makes the balanced degree vector the minimum at fixed total degree.",
            "",
            "## Validation",
            "",
            "```bash",
            "python3 -m py_compile experimental/scripts/certify_m1_a407_a408_residual_design_threshold_v1.py",
            "python3 -m py_compile experimental/scripts/apply_m1_a407_a408_site_entries_v1.py",
            "python3 experimental/scripts/certify_m1_a407_a408_residual_design_threshold_v1.py --check",
            "python3 experimental/scripts/certify_m1_a407_a408_residual_design_threshold_v1.py --json",
            "python3 -m json.tool experimental/data/certificates/m1-a407-a408-residual-design-threshold-v1/m1_a407_a408_residual_design_threshold_v1.json",
            "python3 -m json.tool experimental/data/certificates/m1-a407-a408-residual-design-threshold-v1/tangent_witness_A408_A407_A406_v1.json",
            "python3 -m json.tool site/data/frontier_prime_a406_a407_adjacent_gate.entry.json",
            "python3 -m json.tool site/data/updates_m1_a407_a408_residual_design_threshold.entry.json",
            "git diff --check",
            "```",
            "",
            "## Non-claims",
            "",
            "- Finite-slope support-wise MCA / LD_sw only.",
            "- Not ordinary list decoding.",
            "- Not interleaved-list safety.",
            "- Not protocol soundness or query accounting.",
            "- Not an exact A406 upper bound.",
            "- Not a full M1 closure.",
            "- Does not use the false global RNC Fano-line classification.",
        ]
    )
    return "\n".join(lines) + "\n"


def assert_certificate(cert: Dict[str, object]) -> None:
    assert len(cert["theorem"]["proof_dependencies"]) == 4
    assert cert["prime"]["lucas_primality_certificate_passes"] is True
    assert cert["prime"]["p_mod_512"] == 1
    assert P.bit_length() < 256
    assert P < 2**256
    assert cert["prime"]["h_order_512_checks"]["h^512_mod_p"] == 1
    assert cert["prime"]["h_order_512_checks"]["h^256_mod_p"] == P - 1
    assert cert["gate"]["floor_p_minus_1_over_2^128"] == BUDGET
    assert cert["gate"]["safe_strict_check_106_times_2^128_lt_p"] is True
    assert cert["gate"]["unsafe_strict_check_107_times_2^128_gt_p"] is True
    rows_by_A = {r["parameters"]["A"]: r for r in cert["rows"]}
    assert set(rows_by_A) == {408, 407, 406}
    for A, exact, no_paid in [(408, 105, 50), (407, 106, 93)]:
        row = rows_by_A[A]
        assert row["status"] == "PROVES_EXACT_ROW_BY_A409_METHOD"
        assert row["parameters"]["target_j_plus_1"] == exact
        assert row["conclusions"]["LD_sw_exact_if_tangent_lower"] == exact
        assert row["conclusions"]["paid_exit_size_bound"] == exact
        assert row["conclusions"]["no_paid_residual_size_bound"] == no_paid
        assert no_paid < exact
        assert row["high_neighbor_graph"]["max_degree_bound"] == 2
    assert rows_by_A[406]["status"] == "FAIL_HIGH_NEIGHBOR_DEGREE_BOUND"
    for row in (rows_by_A[408], rows_by_A[407]):
        proof = row["moment_inequality"]
        assert proof["first_forbidden"]["balanced_minimizer_certificate"]["kernel_convexity_formula_checked_for_this_m"] is True
        assert proof["previous_m"]["balanced_minimizer_certificate"]["kernel_convexity_formula_checked_for_this_m"] is True


def assert_tangent_witness(witness: Dict[str, object]) -> None:
    by_A = {item["A"]: item for item in witness["witnesses"]}
    assert set(by_A) == {408, 407, 406}
    for A in [408, 407, 406]:
        j = N - A
        assert by_A[A]["j"] == j
        assert by_A[A]["core_size"] == A - 1
        assert by_A[A]["moving_coordinates"] == j + 1
        assert by_A[A]["claimed_bad_slopes"] == j + 1
    assert by_A[408]["claimed_bad_slopes"] == 105
    assert by_A[407]["claimed_bad_slopes"] == 106
    assert by_A[406]["claimed_bad_slopes"] == 107


def cert_readme() -> str:
    return """# A407/A408 residual-design threshold certificate

This directory contains the generated artifacts for the A407/A408 residual-design threshold packet.

## Files

- `m1_a407_a408_residual_design_threshold_v1.json`: machine-readable certificate for the A=408 and A=407 exact `LD_sw` rows, the A=406 first-failure diagnostic for this method, and the exact-budget prime gate.
- `tangent_witness_A408_A407_A406_v1.json`: symbolic moving-root tangent lower witnesses for A=408, A=407, and A=406.

## Regeneration

Run from the repository root:

```bash
python3 experimental/scripts/certify_m1_a407_a408_residual_design_threshold_v1.py --write
python3 experimental/scripts/certify_m1_a407_a408_residual_design_threshold_v1.py --check
```

## Claims

- For every finite field `F` and every distinct 512-point RS domain `D`, `LD_sw(RS[F,D,256],408)=105`.
- For every finite field `F` and every distinct 512-point RS domain `D`, `LD_sw(RS[F,D,256],407)=106`.
- For `p=27168*2^120+1`, the row `RS[F_p,H,256]` has an adjacent finite-slope support-wise MCA gate: A=407 is safe and A=406 is unsafe at `2^-128`.

## Non-claims

- No exact A=406 upper bound is claimed.
- No full M1 closure is claimed.
- No ordinary list-decoding, interleaved-list, protocol soundness, or challenge-field ledger claim is made.
- The candidate site fragments are review artifacts; live `site/data/*.json` arrays should be updated only after review.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    cert = build_certificate()
    witness = tangent_witness()
    assert_certificate(cert)
    assert_tangent_witness(witness)
    f_entry = frontier_entry()
    u_entry = updates_entry()

    cert_bytes = (json.dumps(cert, indent=2, sort_keys=True) + "\n").encode("utf-8")
    witness_bytes = (json.dumps(witness, indent=2, sort_keys=True) + "\n").encode("utf-8")
    cert_readme_bytes = cert_readme().encode("utf-8")
    report_bytes = report(cert).encode("utf-8")
    frontier_bytes = (json.dumps(f_entry, indent=2, sort_keys=True) + "\n").encode("utf-8")
    updates_bytes = (json.dumps(u_entry, indent=2, sort_keys=True) + "\n").encode("utf-8")

    if args.write:
        CERT_DIR.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        FRONTIER_ENTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
        CERT_PATH.write_bytes(cert_bytes)
        WITNESS_PATH.write_bytes(witness_bytes)
        CERT_README_PATH.write_bytes(cert_readme_bytes)
        REPORT_PATH.write_bytes(report_bytes)
        FRONTIER_ENTRY_PATH.write_bytes(frontier_bytes)
        UPDATES_ENTRY_PATH.write_bytes(updates_bytes)
    if args.check:
        expected = {
            CERT_PATH: cert_bytes,
            WITNESS_PATH: witness_bytes,
            CERT_README_PATH: cert_readme_bytes,
            REPORT_PATH: report_bytes,
            FRONTIER_ENTRY_PATH: frontier_bytes,
            UPDATES_ENTRY_PATH: updates_bytes,
        }
        for path, data in expected.items():
            actual = path.read_bytes()
            if actual != data:
                raise AssertionError(f"artifact mismatch: {path}")
    if args.json:
        print(json.dumps(cert, indent=2, sort_keys=True))
    if not (args.write or args.check or args.json):
        print(report(cert))


if __name__ == "__main__":
    main()
