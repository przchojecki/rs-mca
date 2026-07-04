#!/usr/bin/env python3
"""W4 direct-column rewiring verifier.

This is a proof-packet verifier, not a new search.  It checks the exact
integer room and the consumer wiring for the W4 statement:

    If the terminal post-strip primitive PTE residue is supplied as one
    row-wise split-pair column R(row) <= n^3, then U1's primitive column and
    B exit 3 consume that same column directly in the compiler budget.

The script deliberately does not prove the terminal residue estimate.  It only
verifies that the old local n^2 consumer bottleneck is a routing artifact once
the residue is counted in compiler-column currency.
"""

from __future__ import annotations

import json
import math
import os
import sys
from typing import Any


HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
DAG = os.path.join(
    REPO,
    "experimental",
    "data",
    "certificates",
    "w4-direct-column-rewiring",
    "prize_dag_w4_fixture.json",
)
QA25_CERT = os.path.join(
    REPO,
    "experimental",
    "data",
    "certificates",
    "qa25-boundary-scale-column",
    "qa25_boundary_scale_column.json",
)
X10_CERT = os.path.join(
    REPO,
    "experimental",
    "data",
    "certificates",
    "x10-consumer-tolerance-ladder",
    "x10_consumer_tolerance_ladder.json",
)
B_CERT = os.path.join(
    REPO,
    "experimental",
    "data",
    "certificates",
    "b-writeup-band-reduction",
    "b_writeup_band_reduction.json",
)
CERT = os.path.join(
    REPO,
    "experimental",
    "data",
    "certificates",
    "w4-direct-column-rewiring",
    "w4_direct_column_rewiring.json",
)

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
    raise KeyError(node_id)


def log2_big(x: int) -> float:
    if x <= 0:
        raise ValueError("positive integer required")
    bits = x.bit_length()
    if bits <= 53:
        return math.log2(x)
    return bits - 53 + math.log2(x >> (bits - 53))


def build_certificate() -> dict[str, Any]:
    dag = load_json(DAG)
    qa25 = load_json(QA25_CERT)
    x10 = load_json(X10_CERT)
    b_cert = load_json(B_CERT)

    active = node_by_id(dag, "active_core_count_bound")
    pte = node_by_id(dag, "anchored_nontoral_pte_bound")
    u1 = node_by_id(dag, "u1_pullback_dichotomy")
    alpha = node_by_id(dag, "u1_alpha_active_core_incidence")
    beta = node_by_id(dag, "u1_beta_band_trade_reduction")

    check("active-core node carries the L3 n^3 target", "(L3) #uncharged split pairs <= n^3" in active["statement"])
    check("active-core node records W4 as the L3 sufficiency gate", "W4" in active["statement"])
    check("anchored PTE node records W4 as proved", "W4 PROVED" in pte.get("notes", ""))
    check("U1 remains conditional, not overclaimed", u1["status"] == "CONDITIONAL", u1["status"])
    check("A consumer reduces to anchored PTE", "anchored_nontoral_pte_bound" in alpha.get("notes", ""))
    check("B consumer exit 3 reduces to X-10", "exit 3 is EXACTLY the X-10 residue" in beta.get("notes", ""))
    check("B source certificate names the same residue", b_cert["named_residue"].startswith("anchored_nontoral_pte_bound"))
    check("X10 source certificate has alpha=2 row-room conclusion", x10["min_compiler_alpha_max_numeric"] >= 2.0)
    check(
        "X10 exact rows all fit alpha=2",
        all(row["candidate_alpha_fits_exact"]["alpha_2"] for row in x10["compiler_room_rows"]),
    )

    row_room = []
    for row in qa25["rows"]:
        n = int(row["n"])
        bstar = int(row["B_star"])
        repaired = int(row["repaired_budget_total"])
        room = bstar - repaired
        n3 = n**3
        rid = f"{row['label']} {row['rate']}"
        max_columns = room // n3
        check(f"{rid}: repaired budget is ok", bool(row["repaired_budget_ok"]))
        check(f"{rid}: one direct n^3 column fits", n3 <= room)
        check(f"{rid}: two direct n^3 columns fit", 2 * n3 <= room)
        row_room.append(
            {
                "row": rid,
                "n": n,
                "B_star": bstar,
                "repaired_budget_total": repaired,
                "remaining_room": room,
                "direct_column_n3": n3,
                "max_full_n3_columns_in_remaining_room": max_columns,
                "log2_remaining_room": log2_big(room),
                "log2_n3": log2_big(n3),
            }
        )

    residue_id = "post_strip_primitive_pte_split_pair_column"
    consumers = [
        {
            "consumer": "U1 primitive star/PTE column",
            "old_local_budget": "n^2 post-dictionary star trades per row",
            "new_route": "assign every primitive survivor to the direct compiler column",
            "residue_column_id": residue_id,
        },
        {
            "consumer": "B exit 3 primitive moment/PTE residue",
            "old_local_budget": "n^2 non-v1 band trades",
            "new_route": "assign exit-3 survivors to the same direct compiler column",
            "residue_column_id": residue_id,
        },
    ]
    check("U1 and B exit 3 share one residue column", len({c["residue_column_id"] for c in consumers}) == 1)
    check(
        "row room would even tolerate accidental two-column accounting",
        all(row["max_full_n3_columns_in_remaining_room"] >= 2 for row in row_room),
    )

    return {
        "task": "W4 direct-column rewiring",
        "node": "w4_direct_column_rewiring",
        "status": "PROVED: consumer rewiring only; terminal residue estimate remains open",
        "conditional_theorem": (
            "If the terminal fully stripped primitive PTE residue is supplied in "
            "row-wise split-pair currency as R(row) <= n^3, then U1's primitive "
            "column and B exit 3 consume R directly as one compiler column."
        ),
        "not_claimed": [
            "This packet does not prove active_core_count_bound.",
            "This packet does not prove anchored_nontoral_pte_bound.",
            "The n^3 residue must already include the full paid strip or have tails paid separately.",
        ],
        "tail_currency_condition": (
            "A core-only estimate followed by an uncharged polynomial tail multiplier "
            "is not accepted by W4; the terminal proof must deliver the final row-wise "
            "post-strip split-pair count."
        ),
        "residue_column_id": residue_id,
        "consumers": consumers,
        "row_room": row_room,
        "checks": NCHECK,
        "sources": {
            "dag": (
                "experimental/data/certificates/w4-direct-column-rewiring/"
                "prize_dag_w4_fixture.json"
            ),
            "qa25": "experimental/data/certificates/qa25-boundary-scale-column/qa25_boundary_scale_column.json",
            "x10": "experimental/data/certificates/x10-consumer-tolerance-ladder/x10_consumer_tolerance_ladder.json",
            "b_writeup": "experimental/data/certificates/b-writeup-band-reduction/b_writeup_band_reduction.json",
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
                "conditional_theorem": cert["conditional_theorem"],
                "min_full_n3_columns": min(
                    row["max_full_n3_columns_in_remaining_room"] for row in cert["row_room"]
                ),
                "status": cert["status"],
            },
            indent=2,
            sort_keys=True,
        )
    )

    if FAILS:
        print("\nFAIL:")
        for name in FAILS:
            print(f"  - {name}")
        print("\nrecomputed summary:")
        print(json.dumps(cert, indent=2, sort_keys=True))
        return 1

    print(f"\nPASS: {NCHECK} W4 direct-column checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
