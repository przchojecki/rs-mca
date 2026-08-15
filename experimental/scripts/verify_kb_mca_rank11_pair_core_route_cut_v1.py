#!/usr/bin/env python3
"""Exact certificate for the KoalaBear rank-11 pair/core route cut.

The unconditional ceiling uses only the printed support-local high theorem,
the cumulative interleaved pair caps, and fixed-pair core deficiency.  The
smaller coupled ceiling is explicitly conditional on the new pointwise
ordered-basis corollary ``sum(theta_gamma) <= C_s``.  Neither ceiling pays
rank eleven.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from fractions import Fraction
from math import comb, prod
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "experimental/data/certificates/kb-mca-rank11-pair-core-route-cut-v1/manifest.json"
PARENT = "491ccdf53d54846f5a013b808960645275c64ed3"
UPSTREAM_MAIN = "93fba1be3f3299b0ba4708d88715377bbb656e45"
PACKET_FILES = [
    "agents.md",
    "experimental/agents-log.md",
    "experimental/grande_finale.tex",
    "experimental/notes/thresholds/kb_mca_rank11_pair_core_route_cut_v1.md",
    "experimental/data/certificates/kb-mca-rank11-pair-core-route-cut-v1/README.md",
    "experimental/scripts/verify_kb_mca_rank11_pair_core_route_cut_v1.py",
    "experimental/scripts/verify_kb_mca_rank11_pair_core_route_cut_v1.sage",
    "experimental/campaigns/kb-mca-rank11-pair-core-post-1167/campaign.json",
    "experimental/campaigns/kb-mca-rank11-pair-core-post-1167/00_contract.md",
    "experimental/campaigns/kb-mca-rank11-pair-core-post-1167/01_frontier_map.md",
    "experimental/campaigns/kb-mca-rank11-pair-core-post-1167/02_controls.md",
    "experimental/campaigns/kb-mca-rank11-pair-core-post-1167/03_idea_ledger.csv",
    "experimental/campaigns/kb-mca-rank11-pair-core-post-1167/04_dependency_ledger.csv",
    "experimental/campaigns/kb-mca-rank11-pair-core-post-1167/05_claim_registry.csv",
    "experimental/campaigns/kb-mca-rank11-pair-core-post-1167/06_review_registry.csv",
    "experimental/campaigns/kb-mca-rank11-pair-core-post-1167/07_review_status.csv",
    "experimental/campaigns/kb-mca-rank11-pair-core-post-1167/proofs/nonuniform_theta_pair_route_cut.md",
    "experimental/campaigns/kb-mca-rank11-pair-core-post-1167/threads/barrier_adversary.md",
    "experimental/campaigns/kb-mca-rank11-pair-core-post-1167/controls/gf7_parallel_star.sage",
    "experimental/campaigns/kb-mca-rank11-pair-core-post-1167/reviews/literature_sweep.md",
    "experimental/campaigns/kb-mca-rank11-pair-core-post-1167/reviews/wolfram_replay.md",
]
ROW = {
    "p": 2130706433,
    "extension_degree": 6,
    "n": 2097152,
    "K": 1048576,
    "m": 1116048,
    "w": 67472,
    "near": 134944,
    "budget": 274980728111395087,
}
EXPLANATION_DIMENSION = 10


class Reject(ValueError):
    pass


def require(value: bool, message: str) -> None:
    if not value:
        raise Reject(message)


def falling(x: int, length: int) -> int:
    return prod(x - index for index in range(length))


def rising(x: int, length: int) -> int:
    return prod(x + index for index in range(length))


def ceil_div(numerator: int, denominator: int) -> int:
    return -(-numerator // denominator)


def theta_resource(rank: int) -> int:
    """Floor of the largest ordered-basis resource through ``rank``.

    For a rank-j affine family the two endpoint constants before division by
    a margin threshold are the displayed falling/rising factorial ratios.
    Rank zero contributes n.  Taking the maximum through rank s also supplies
    the high-subfamily cap for every possible affine subrank.
    """

    n, K, m, w = (ROW[key] for key in ("n", "K", "m", "w"))
    values = [Fraction(n)]
    for subrank in range(1, rank + 1):
        values.extend(
            [
                Fraction(
                    falling(n, subrank + 1),
                    m * rising(w + 1, subrank - 1),
                ),
                Fraction(
                    falling(n - K + subrank, subrank + 1),
                    rising(w + 1, subrank),
                ),
            ]
        )
    value = max(values)
    return value.numerator // value.denominator


def high_cap(rank: int, threshold: int) -> int:
    require(1 <= threshold <= ROW["w"] + 1, "legal high threshold")
    # floor(max_j C_j/threshold) = floor(floor(max_j C_j)/threshold).
    return theta_resource(rank) // threshold


def pair_cap(rank: int, deficiency: int) -> int:
    """Cumulative number of pairs with core deficiency at most delta."""

    n, K, w = (ROW[key] for key in ("n", "K", "w"))
    require(1 <= deficiency < w, "legal core deficiency")
    return comb(n - K + rank, rank) // comb(w - deficiency + rank, rank)


def pair_multiplicity(deficiency: int) -> int:
    """Sharp disjoint-exception multiplicity for one fixed selected pair."""

    require(deficiency >= 1, "positive deficiency")
    return (ROW["n"] - ROW["m"] + deficiency) // deficiency


def pair_weight_capacity(cutoff: int, deficiency: int) -> int:
    require(1 <= deficiency <= cutoff, "weighted deficiency range")
    return pair_multiplicity(deficiency) * (cutoff + 1 - deficiency)


def max_compatible_deficiency(cutoff: int, forced_weight: int) -> int:
    """Largest j whose sharp parallel capacity can carry forced_weight."""

    low, high = 1, cutoff + 1
    while low < high:
        middle = (low + high) // 2
        if pair_weight_capacity(cutoff, middle) >= forced_weight:
            low = middle + 1
        else:
            high = middle
    return low - 1


def fixed_pair_optima(rank: int, resource: int) -> dict[str, Any]:
    field_size = ROW["p"] ** ROW["extension_degree"]
    post_near_excess = ROW["budget"] - ROW["near"] + 1
    by_weight: dict[str, int] | None = None
    by_records: dict[str, int] | None = None
    legal_cutoffs = 0
    last_legal = 0
    for cutoff in range(1, ROW["w"]):
        pairs = pair_cap(rank, cutoff)
        if pairs * pairs >= field_size:
            continue
        legal_cutoffs += 1
        last_legal = cutoff
        low_weight = max(0, (cutoff + 1) * post_near_excess - resource)
        weight = ceil_div(low_weight, pairs)
        records = ceil_div(weight, cutoff)
        item = {
            "cutoff": cutoff,
            "pair_cap": pairs,
            "forced_pair_weight": weight,
            "forced_records": records,
            "max_compatible_deficiency": max_compatible_deficiency(cutoff, weight),
        }
        if by_weight is None or (weight, -cutoff) > (
            by_weight["forced_pair_weight"],
            -by_weight["cutoff"],
        ):
            by_weight = item
        if by_records is None or (records, -cutoff) > (
            by_records["forced_records"],
            -by_records["cutoff"],
        ):
            by_records = item
    require(by_weight is not None and by_records is not None, "nonempty pair scan")
    return {
        "legal_cutoffs": legal_cutoffs,
        "last_legal_cutoff": last_legal,
        "maximum_forced_weight": by_weight,
        "maximum_forced_records": by_records,
    }


def core_lp_optima(rank: int, resource: int) -> dict[str, Any]:
    """Scan the unconditional and sum-theta-conditional core ceilings."""

    field_size = ROW["p"] ** ROW["extension_degree"]
    previous_pairs = 0
    unconditional_low = 0
    conditional_low = 0
    conditional_resource = 0
    unconditional_best: dict[str, int] | None = None
    conditional_best: dict[str, int] | None = None
    unconditional_multiplicity = 0
    conditional_first = 0
    conditional_last = 0
    conditional_multiplicity = 0

    for cutoff in range(1, ROW["w"]):
        current_pairs = pair_cap(rank, cutoff)
        new_pair_types = current_pairs - previous_pairs
        slots = new_pair_types * pair_multiplicity(cutoff)

        # Current-theorem LP: Abel/greedy sum over every available pair type.
        unconditional_low += slots

        # Conditional LP: a type-delta record costs at least delta units of
        # the new global sum-theta resource.  Lower delta is always more
        # efficient than a high record of cost cutoff+1.
        selected = min(slots, (resource - conditional_resource) // cutoff)
        conditional_low += selected
        conditional_resource += cutoff * selected

        if current_pairs * current_pairs < field_size:
            high = high_cap(rank, cutoff + 1)
            unconditional = {
                "cutoff": cutoff,
                "pair_cap": current_pairs,
                "high_records": high,
                "low_records": unconditional_low,
                "total": ROW["near"] + high + unconditional_low,
            }
            unconditional["signed_slack"] = ROW["budget"] - unconditional["total"]
            if (
                unconditional_best is None
                or unconditional["total"] < unconditional_best["total"]
            ):
                unconditional_best = unconditional
                unconditional_multiplicity = 1
            elif unconditional["total"] == unconditional_best["total"]:
                unconditional_multiplicity += 1

            conditional_high = (resource - conditional_resource) // (cutoff + 1)
            conditional = {
                "cutoff": cutoff,
                "pair_cap": current_pairs,
                "low_records": conditional_low,
                "low_theta_used": conditional_resource,
                "high_records": conditional_high,
                "total": ROW["near"] + conditional_low + conditional_high,
            }
            conditional["signed_slack"] = ROW["budget"] - conditional["total"]
            if conditional_best is None or conditional["total"] < conditional_best["total"]:
                conditional_best = conditional
                conditional_first = cutoff
                conditional_last = cutoff
                conditional_multiplicity = 1
            elif conditional["total"] == conditional_best["total"]:
                conditional_last = cutoff
                conditional_multiplicity += 1

        previous_pairs = current_pairs

    require(
        unconditional_best is not None and conditional_best is not None,
        "nonempty core LP scan",
    )
    unconditional_best["optimum_multiplicity"] = unconditional_multiplicity
    conditional_best["first_optimal_cutoff"] = conditional_first
    conditional_best["last_optimal_cutoff"] = conditional_last
    conditional_best["optimum_multiplicity"] = conditional_multiplicity
    return {
        "unconditional_current_theorems": unconditional_best,
        "conditional_on_pointwise_theta_sum": conditional_best,
    }


def abstract_singleton_packing(rank: int, resource: int) -> dict[str, Any]:
    """Exact certificate-class packing; not claimed RS-realizable."""

    pairs = pair_cap(rank, 1)
    records_per_pair = pair_multiplicity(1)
    slopes = pairs * records_per_pair
    total = ROW["near"] + slopes
    field_size = ROW["p"] ** ROW["extension_degree"]
    require(slopes <= resource, "packing respects sum-theta resource")
    require(slopes < field_size, "packing respects affine slope supply")
    require(pairs * pairs < field_size, "packing respects sub-square guard")
    return {
        "status": "ABSTRACT_CERTIFICATE_CLASS_PACKING_NOT_RS_REALIZABILITY",
        "deficiency": 1,
        "local_margin": 1,
        "pair_types": pairs,
        "records_per_pair": records_per_pair,
        "post_near_records": slopes,
        "total_with_near": total,
        "excess_over_budget": total - ROW["budget"],
        "theta_resource_used": slopes,
    }


def build() -> dict[str, Any]:
    rank = EXPLANATION_DIMENSION
    resource = theta_resource(rank)
    fixed = fixed_pair_optima(rank, resource)
    core = core_lp_optima(rank, resource)
    packing = abstract_singleton_packing(rank, resource)

    require(resource == 106618568137036225644, "theta resource")
    require(
        fixed["maximum_forced_weight"]
        == {
            "cutoff": 6486,
            "pair_cap": 2255946383610,
            "forced_pair_weight": 743449148,
            "forced_records": 114624,
            "max_compatible_deficiency": 8,
        },
        "fixed-pair weight optimum",
    )
    require(
        fixed["maximum_forced_records"]
        == {
            "cutoff": 1795,
            "pair_cap": 1075288922022,
            "forced_pair_weight": 360132809,
            "forced_records": 200632,
            "max_compatible_deficiency": 4,
        },
        "fixed-pair record optimum",
    )
    require(fixed["last_legal_cutoff"] == 65810, "last sub-square cutoff")

    unconditional = core["unconditional_current_theorems"]
    require(
        unconditional
        == {
            "cutoff": 19737,
            "pair_cap": 26130774875308,
            "high_records": 5401690553097387,
            "low_records": 808527428378681053,
            "total": 813929118931913384,
            "signed_slack": -538948390820518297,
            "optimum_multiplicity": 1,
        },
        "unconditional core LP optimum",
    )

    conditional = core["conditional_on_pointwise_theta_sum"]
    require(
        conditional
        == {
            "cutoff": 26033,
            "pair_cap": 107486241601454,
            "low_records": 811957734614064312,
            "low_theta_used": 106597778100457375003,
            "high_records": 798572504373,
            "total": 811958533186703629,
            "signed_slack": -536977805075308542,
            "first_optimal_cutoff": 26033,
            "last_optimal_cutoff": 65810,
            "optimum_multiplicity": 39778,
        },
        "conditional coupled core LP optimum",
    )

    require(
        packing["post_near_records"] == 805771548351717555,
        "abstract singleton packing",
    )
    return {
        "schema": "kb-mca-rank11-pair-core-route-cut-v1",
        "parent": PARENT,
        "row": ROW,
        "explanation_dimension": rank,
        "theta_resource": resource,
        "fixed_pair_concentration": fixed,
        "core_deficiency_lp": core,
        "abstract_singleton_packing": packing,
        "dependency_boundary": {
            "unconditional_current_theorems": [
                "support-local high-margin cap",
                "sub-square common-support interleaving collapse",
                "fixed-pair disjoint exception sets",
            ],
            "conditional_new_corollary": "sum_gamma theta_gamma <= C_10",
        },
        "claims": {
            "rank11_paid": False,
            "active_v4_ledger_movement": 0,
            "KoalaBear_closed": False,
            "route_cut": "NEEDS_CROSS_PAIR_COLLISION_OR_OWNER_THEOREM",
        },
        "provenance": {
            "repository": "przchojecki/rs-mca",
            "upstream_main_at_refresh": UPSTREAM_MAIN,
            "exact_pr1167_parent": PARENT,
            "exa_sources_reviewed": 55,
            "load_bearing_external_lemma": False,
            "wolfram_exact_replay": True,
        },
        "packet_files": PACKET_FILES,
        "packet_file_sha256": {
            path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
            for path in PACKET_FILES
        },
    }


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def payload(value: dict[str, Any]) -> str:
    unsigned = copy.deepcopy(value)
    unsigned.pop("payload_sha256", None)
    return hashlib.sha256(canonical(unsigned)).hexdigest()


def validate(value: dict[str, Any], expected: dict[str, Any]) -> None:
    require(value == expected, "canonical certificate")
    require(value["payload_sha256"] == payload(value), "payload hash")


def tamper_selftest(expected: dict[str, Any]) -> int:
    mutations = [
        lambda item: item["core_deficiency_lp"]["unconditional_current_theorems"].__setitem__(
            "total", 813929118931913383
        ),
        lambda item: item["core_deficiency_lp"]["conditional_on_pointwise_theta_sum"].__setitem__(
            "total", 811958533186703628
        ),
        lambda item: item["fixed_pair_concentration"]["maximum_forced_weight"].__setitem__(
            "max_compatible_deficiency", 9
        ),
        lambda item: item["abstract_singleton_packing"].__setitem__(
            "status", "RS_REALIZABLE"
        ),
        lambda item: item["claims"].__setitem__("rank11_paid", True),
        lambda item: item["row"].__setitem__("extension_degree", 1),
    ]
    caught = 0
    for mutate in mutations:
        changed = copy.deepcopy(expected)
        mutate(changed)
        changed["payload_sha256"] = payload(changed)
        try:
            validate(changed, expected)
        except Reject:
            caught += 1
    require(caught == len(mutations), "all hostile mutations caught")
    return caught


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    expected = build()
    expected["payload_sha256"] = payload(expected)
    if args.write:
        MANIFEST.parent.mkdir(parents=True, exist_ok=True)
        MANIFEST.write_text(json.dumps(expected, indent=2) + "\n")
        print(f"WROTE {MANIFEST}")
        return
    actual = json.loads(MANIFEST.read_text())
    validate(actual, expected)
    if args.tamper_selftest:
        caught = tamper_selftest(expected)
        print(f"KB_MCA_RANK11_PAIR_CORE_ROUTE_CUT_TAMPER_PASS mutations={caught}/6")
        return
    if args.json:
        print(json.dumps(expected, sort_keys=True))
        return
    unconditional = expected["core_deficiency_lp"]["unconditional_current_theorems"]
    conditional = expected["core_deficiency_lp"]["conditional_on_pointwise_theta_sum"]
    print(
        "KB_MCA_RANK11_PAIR_CORE_ROUTE_CUT_PASS "
        f"unconditional={unconditional['total']} "
        f"conditional={conditional['total']} "
        f"conditional_over={-conditional['signed_slack']}"
    )


if __name__ == "__main__":
    main()
