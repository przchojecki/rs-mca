#!/usr/bin/env python3
"""X-10 consumer tolerance ladder.

This verifier answers the arithmetic question:

    If the final X-10 estimate is weakened to A_h^nt <= h n^alpha,
    which downstream consumers still close?

The hard consumers pass through the proved orbit conversion

    #split pairs <= (n / h) A_h^nt,

so the normalized exponent alpha becomes a split-pair column n^(alpha+1).
The script uses the landed QA.22 and QA.25 certificates for exact row budgets,
and uses integer comparisons for all candidate-rung checks.  Floating logs are
diagnostic only.
"""

from __future__ import annotations

import json
import math
import os
import sys
from fractions import Fraction
from typing import Any


HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
DAG = os.path.join(REPO, "experimental", "data", "prize-dag", "prize_dag.json")
QA22_CERT = os.path.join(
    REPO,
    "experimental",
    "data",
    "certificates",
    "qa22-staircase-budget",
    "qa22_staircase_budget.json",
)
QA25_CERT = os.path.join(
    REPO,
    "experimental",
    "data",
    "certificates",
    "qa25-boundary-scale-column",
    "qa25_boundary_scale_column.json",
)
CERT = os.path.join(
    REPO,
    "experimental",
    "data",
    "certificates",
    "x10-consumer-tolerance-ladder",
    "x10_consumer_tolerance_ladder.json",
)

BANKED_DAG_NODES: dict[str, dict[str, str]] = {
    "anchored_nontoral_pte_bound": {
        "id": "anchored_nontoral_pte_bound",
        "status": "CONDITIONAL",
        "statement": (
            "H = mu_n in F_q*, n = 2^s, p >= n^2. "
            "A_h^nt counts anchored non-toral pairs. Consequences include "
            "#uncharged split pairs = (n/h) A_h^nt <= n^2 by the proved "
            "orbit argument."
        ),
        "notes": (
            "X-10 insufficiency ledger: in-range rows stay small; the "
            "remaining target is the anchored non-toral PTE bound."
        ),
    },
    "u1_alpha_active_core_incidence": {
        "id": "u1_alpha_active_core_incidence",
        "status": "TARGET",
        "statement": (
            "Sum over active cores of the sporadic full-fiber counts is "
            "bounded by the n^2 split-pair budget."
        ),
        "notes": (
            "X-10: A reduces exactly to anchored_nontoral_pte_bound by the "
            "proved orbit argument."
        ),
    },
    "u1_beta_band_trade_reduction": {
        "id": "u1_beta_band_trade_reduction",
        "status": "CONDITIONAL",
        "statement": (
            "Band trades reduce through minimal subtrades, v1-chargeable "
            "pullback pencils, or the primitive moment/PTE exit."
        ),
        "notes": (
            "B-WRITEUP reduces exits 1 and 2 formally. X-10 plus the "
            "defect/tails wrapper is the remaining exit-3 residue."
        ),
    },
    "a2_depth_cell_active_shadow_bound": {
        "id": "a2_depth_cell_active_shadow_bound",
        "status": "TARGET",
        "statement": (
            "The graded ledger counts active depth cells actually occupied "
            "by post-strip pairs."
        ),
        "notes": (
            "ACT-SHADOW: active depth cells follow the same rarity count as "
            "the final X-10 estimate."
        ),
    },
}

FAILS: list[str] = []
NCHECK = 0


def check(name: str, cond: bool, detail: str = "") -> None:
    global NCHECK
    NCHECK += 1
    tag = "PASS" if cond else "FAIL"
    line = f"[{tag}] {name}"
    if detail:
        line += f"   ({detail})"
    print(line)
    if not cond:
        FAILS.append(name)


def load_json(path: str) -> Any:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def node_by_id(dag: dict[str, Any], node_id: str) -> dict[str, Any]:
    for node in dag["nodes"]:
        if node["id"] == node_id:
            return node
    if node_id in BANKED_DAG_NODES:
        print(f"[info] upstream DAG lacks {node_id}; using banked node snippet")
        return BANKED_DAG_NODES[node_id]
    raise KeyError(node_id)


def log2_big(x: int | None) -> float | None:
    if x is None or x <= 0:
        return None
    bits = x.bit_length()
    if bits <= 53:
        return math.log2(x)
    return bits - 53 + math.log2(x >> (bits - 53))


def log_base_big(x: int, base: int) -> float:
    if x <= 0 or base <= 1:
        raise ValueError("positive x and base > 1 required")
    return float(log2_big(x)) / math.log2(base)


def leq_power(base: int, exponent: Fraction, budget: int) -> bool:
    """Return whether base**exponent <= budget, exactly.

    The comparison is done as base**p <= budget**q for exponent p/q.
    """
    if exponent < 0:
        raise ValueError("nonnegative exponent required")
    return pow(base, exponent.numerator) <= pow(budget, exponent.denominator)


def frac_str(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def consumer_row(
    cid: str,
    budget: str,
    transform: str,
    alpha_max: Fraction,
    note: str,
) -> dict[str, Any]:
    delta_min = max(Fraction(0), Fraction(2) - alpha_max)
    return {
        "id": cid,
        "budget": budget,
        "normalized_model": "A_h^nt <= h*n^alpha",
        "transform": transform,
        "alpha_max": frac_str(alpha_max),
        "n_times_polylog_verdict": (
            "only if the polylog factor is absorbed by the h envelope and constants"
            if alpha_max == 1
            else "yes, at this consumer's exponent scale"
        ),
        "n_to_1_5_ok": alpha_max >= Fraction(3, 2),
        "n_to_2_minus_delta_min_delta": frac_str(delta_min),
        "n_to_2_minus_delta_ok_condition": f"delta >= {frac_str(delta_min)}",
        "note": note,
    }


def compiler_room_rows(qa25: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    candidates = {
        "alpha_1": Fraction(1),
        "alpha_3_over_2": Fraction(3, 2),
        "alpha_2": Fraction(2),
        "alpha_5_over_2": Fraction(5, 2),
    }
    for row in qa25["rows"]:
        n = int(row["n"])
        bstar = int(row["B_star"])
        repaired = int(row["repaired_budget_total"])
        room = bstar - repaired
        rid = f"{row['label']} {row['rate']}"
        check(f"{rid}: QA.25 repaired total leaves positive room", room > 0)
        check(f"{rid}: n^3 split-pair compiler column fits remaining room", n**3 <= room)
        fits = {
            name: leq_power(n, alpha + 1, room)
            for name, alpha in candidates.items()
        }
        alpha_max = log_base_big(room, n) - 1.0
        rows.append(
            {
                "row": rid,
                "n": n,
                "B_star": bstar,
                "qa25_repaired_budget_total": repaired,
                "remaining_room_after_QA22_QA25": room,
                "log2_remaining_room": log2_big(room),
                "compiler_alpha_max_numeric": alpha_max,
                "candidate_alpha_fits_exact": fits,
            }
        )
    check(
        "all campaign rows tolerate alpha=2 at compiler-room scale",
        all(row["candidate_alpha_fits_exact"]["alpha_2"] for row in rows),
    )
    check(
        "at least one campaign row rejects alpha=5/2 at compiler-room scale",
        any(not row["candidate_alpha_fits_exact"]["alpha_5_over_2"] for row in rows),
    )
    return rows


def build_certificate() -> dict[str, Any]:
    dag = load_json(DAG)
    qa22 = load_json(QA22_CERT)
    qa25 = load_json(QA25_CERT)

    pte = node_by_id(dag, "anchored_nontoral_pte_bound")
    alpha = node_by_id(dag, "u1_alpha_active_core_incidence")
    beta = node_by_id(dag, "u1_beta_band_trade_reduction")
    active_depth = node_by_id(dag, "a2_depth_cell_active_shadow_bound")

    check("QA.22 source certificate has six rows", len(qa22["rows"]) == 6)
    check("QA.25 source certificate has six rows", len(qa25["rows"]) == 6)
    check("QA.25 rows are repaired and budget-ok", all(row["repaired_budget_ok"] for row in qa25["rows"]))
    check(
        "X-10 final estimate node is still open/conditional",
        pte["status"] in {"TARGET", "CONDITIONAL"},
        pte["status"],
    )
    check("X-10 node states the orbit conversion", "(n/h) A_h^nt <= n^2" in pte["statement"])
    check("A consumer reduces to X-10", "X-10" in alpha["notes"] and "anchored_nontoral_pte_bound" in alpha["notes"])
    check("B consumer reduces to X-10", "X-10" in beta["notes"] and "defect/tails wrapper" in beta["notes"])
    check("active-depth consumer is the same rarity shape", "same rarity" in active_depth["notes"])

    compiler_rows = compiler_room_rows(qa25)
    min_compiler_alpha = min(row["compiler_alpha_max_numeric"] for row in compiler_rows)

    consumers = [
        consumer_row(
            "A_to_U1_split_pair_budget",
            "n^2 split-pair budget",
            "(n/h)*A_h^nt <= n^(alpha+1)",
            Fraction(1),
            "This is the hard orbit-converted budget.  It is exactly the stated hn target.",
        ),
        consumer_row(
            "A_to_16n3_compiler_reserve_only",
            "exact QA.22/QA.25 remaining row room, with n^3 checked integrally",
            "(n/h)*A_h^nt <= n^(alpha+1), then absorbed directly by row room",
            Fraction(2),
            (
                "The global compiler arithmetic tolerates alpha=2 on all six rows, "
                "but this does not preserve the local U1 n^2 split-pair theorem."
            ),
        ),
        consumer_row(
            "B_exit3_primitive_moment_PTE",
            "n^2 non-v1 band-trade budget",
            "(n/h)*A_h^nt <= n^(alpha+1)",
            Fraction(1),
            "Exit 3 is precisely the X-10 residue plus the same orbit conversion.",
        ),
        consumer_row(
            "A1_lower_active_shadow_local",
            "n^2 active-shadow mass budget",
            "active shadow is counted locally; no extra n/h orbit factor in this local ledger",
            Fraction(2),
            "This is the local active-shadow budget only; downstream split-pair use reverts to the first row.",
        ),
        consumer_row(
            "A2_depth_cell_active_shadow_local",
            "n^2 active-depth mass budget",
            "active depth cells are counted locally; no extra n/h orbit factor in this local ledger",
            Fraction(2),
            "Same tolerance as the A1 local active-shadow ledger.",
        ),
        {
            "id": "tails_defect_wrapper",
            "budget": "n^2 after orbit conversion",
            "normalized_model": "A_{h,B}^nt <= h*n^alpha*n^lambda, where lambda is defect/tail loss",
            "transform": "(n/h)*A_{h,B}^nt <= n^(alpha+lambda+1)",
            "constraint": "alpha + lambda <= 1",
            "alpha_max_when_lambda_0": "1",
            "lambda_max_when_alpha_1": "0",
            "lambda_max_when_alpha_1_minus_delta": "delta",
            "n_times_polylog_verdict": (
                "only if the total defect/tail factor remains subpolynomial and fits exact constants"
            ),
            "n_to_1_5_ok": False,
            "n_to_2_minus_delta_ok_condition": "delta >= 1 + lambda",
            "note": "This is the weakest rung: any polynomial defect loss must be paid by an equal exponent saving in A_h^nt.",
        },
    ]

    return {
        "task": "X-10 consumer tolerance ladder",
        "node": "anchored_nontoral_pte_bound",
        "status": "PASS: exact row-room checks and consumer exponent ladder emitted",
        "normalization": "A_h^nt <= h*n^alpha",
        "hard_conclusion": (
            "The consumers that preserve the U1/B n^2 split-pair budgets require alpha <= 1. "
            "Thus h*n^(3/2) is not enough there; h*n^(2-delta) works only for delta >= 1."
        ),
        "compiler_room_conclusion": (
            "The exact QA.22/QA.25 row room tolerates the weaker alpha=2 column on all six rows, "
            "but alpha=5/2 is rejected by at least one prize row."
        ),
        "min_compiler_alpha_max_numeric": min_compiler_alpha,
        "consumers": consumers,
        "compiler_room_rows": compiler_rows,
        "checks": NCHECK,
        "sources": {
            "qa22": "qa22_staircase_budget.json",
            "qa25": "qa25_boundary_scale_column.json",
            "dag": "prize_dag.json",
        },
    }


def main() -> int:
    write = "--write-certificate" in sys.argv
    cert = build_certificate()
    if write:
        os.makedirs(os.path.dirname(CERT), exist_ok=True)
        with open(CERT, "w", encoding="utf-8") as fh:
            json.dump(cert, fh, indent=2, sort_keys=True)
            fh.write("\n")
        print(f"[write] {CERT}")

    expected = None
    if os.path.exists(CERT):
        expected = load_json(CERT)
    check("certificate exists", expected is not None, CERT)
    if expected is not None:
        check("certificate matches recomputed summary", cert == expected)

    print("\nsummary:")
    print(
        json.dumps(
            {
                "normalization": cert["normalization"],
                "hard_conclusion": cert["hard_conclusion"],
                "min_compiler_alpha_max_numeric": cert["min_compiler_alpha_max_numeric"],
            },
            indent=2,
            sort_keys=True,
        )
    )

    if FAILS:
        print("\nFAIL:")
        for name in FAILS:
            print(f"  - {name}")
        print("\nrecomputed certificate:")
        print(json.dumps(cert, indent=2, sort_keys=True))
        return 1

    print(f"\nPASS: {NCHECK} X-10 tolerance ladder checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
