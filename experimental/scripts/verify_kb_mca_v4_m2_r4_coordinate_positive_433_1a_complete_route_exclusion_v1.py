#!/usr/bin/env python3
"""Fail-closed verifier: positive 433-1a -> O0b complete route exclusion.

Self-contained scope: replays the census arithmetic (orbit partition,
disjointness, row arity, totals), cross-checks the canonical certificate
JSON, and checks the note's ledger and nonclaim sentences.  The per-cell
exclusion proofs are NOT re-verified here; they are pinned by node id to
the canonical DAG (https://github.com/AllenGrahamHart/rs-mca-prize-dag),
where the aggregate node's own verifier was replayed PASS at audit.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NAME = "kb_mca_v4_m2_r4_coordinate_positive_433_1a_complete_route_exclusion_v1"
NOTE = ROOT / "experimental" / "notes" / "frontier-adjacent" / f"{NAME}.md"
CERT = (ROOT / "experimental" / "data" / "certificates"
        / "kb-mca-v4-m2-r4-coordinate-positive-433-1a-complete-route-exclusion-v1"
        / f"{NAME}.json")

EXPECTED_PARTITION = [
    ((0,), 4, 1), ((1, 2), 8, 2), ((3, 6), 8, 1), ((4, 7), 8, 1),
    ((5, 8), 8, 1), ((9, 10), 8, 1), ((11,), 4, 1), ((12, 13), 8, 1),
    ((14,), 4, 1),
]


def require(condition, message):
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def main():
    cert = json.loads(CERT.read_text())
    partition = [(tuple(row["orbit"]), row["rows"], row["representatives"])
                 for row in cert["orbit_partition"]]
    require(partition == EXPECTED_PARTITION, "certificate orbit partition")

    cells = [cell for orbit, _, _ in partition for cell in orbit]
    require(sorted(cells) == list(range(15)), "cells 0..14 covered exactly once")
    require(len(cells) == len(set(cells)), "orbit disjointness")
    require(sum(rows for _, rows, _ in partition) == 60 == cert["total_raw_rows"],
            "raw-row total 60")
    require(sum(reps for _, _, reps in partition) == 10
            == cert["total_representatives"], "representative total 10")
    require(cert["signed_lanes"] == 2, "exactly two signed lanes")
    for orbit, rows, reps in partition:
        require(rows == 4 * len(orbit), f"row arity 4*|orbit| at {orbit}")
        require(reps == (2 if orbit == (1, 2) else 1),
                f"representative count at {orbit}")

    pins = cert["pinned_nodes"]
    require(len(pins["orbit_exclusions"]) == 9, "nine orbit-exclusion pins")
    require(len(set(pins["orbit_exclusions"])) == 9, "pins distinct")
    for node in ([pins["aggregate"], pins["signed_edge_atlas"],
                  pins["common_row_quotient"]] + pins["orbit_exclusions"]):
        require(re.fullmatch(r"[a-z0-9_]+", node), f"pin id shape: {node}")
        require(node.startswith("rate_half_kb_m2_r4_coordinate_positive_433_1a"),
                f"pin lane: {node}")

    prov = cert["provenance"]
    require(re.fullmatch(r"[0-9a-f]{8,40}", prov["final_integration_commit"]),
            "integration commit pin")
    counts = prov["route_count_by_wave"]
    require(counts["wave38"] == 13 and counts["wave41_representatives"] == 0,
            "route count 13 -> 0")

    note = NOTE.read_text()
    for marker in (
        "(KBPCR-1)", "(KBPCR-2)", "total   60.",
        "closes **one coordinate route only**",
        "Formal orbit representatives are not algebraic survivors",
        "target elimination is not source-system elimination",
        prov["final_integration_commit"],
    ):
        require(marker in note, f"note marker: {marker!r}")
    for node in pins["orbit_exclusions"]:
        cell_tag = node.split("433_1a_")[1].split("_")[0]
        require(cell_tag.startswith("cell"), f"pin cell tag: {node}")
    require(cert["nonclaim"].startswith("Closes one coordinate route only"),
            "nonclaim present")

    print("positive 433-1a complete route exclusion: census + certificate "
          "+ note ledger verified (per-cell proofs pinned to canonical DAG)")


if __name__ == "__main__":
    main()
