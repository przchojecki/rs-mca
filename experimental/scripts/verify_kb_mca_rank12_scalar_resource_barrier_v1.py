#!/usr/bin/env python3
"""Exact scalar-resource barrier for the post-#1174 rank-twelve row.

This verifier optimizes the strongest coordinate-incidence conclusion that
uses only:

* the number N of post-near selected records;
* the nonuniform truncated-margin resource sum(theta_gamma) <= C_11(R);
* theta_gamma = min(d + 1, raw_margin_gamma);
* pair noncontainment, which forces raw_margin_gamma >= 1; and
* the first-moment identity |S_gamma cap H_gamma| = m - raw_margin_gamma.

It does not claim that the extremal histogram is Reed--Solomon realizable.
Its conclusion is a certificate-class route cut: scalar margin accounting
plus one-coordinate averaging cannot force the rank-ten child required by
the repaired rank-eleven induction.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from fractions import Fraction
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULT_PATH = (
    ROOT
    / "experimental/data/certificates/kb-mca-rank12-scalar-gluing-route-v1/result.json"
)

R = 1_048_576
D = 67_472
BUDGET = 274_980_728_111_395_087
NEAR = 2 * D
UNSAFE = BUDGET - NEAR + 1
S = 11
K = R
DOMAIN_LENGTH = R + K
M = D + K
TARGET_CHILD = 248_706_399_341_288_370
BASE_FIELD = 2_130_706_433
LINE_FIELD_ORDER = BASE_FIELD**6


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(f"Reject: {message}")


def falling(x: int, length: int) -> int:
    value = 1
    for i in range(length):
        value *= x - i
    return value


def rising(x: int, length: int) -> int:
    value = 1
    for i in range(length):
        value *= x + i
    return value


def margin_resource() -> int:
    endpoints = (
        Fraction(falling(R + K, S + 1), (D + K) * rising(D + 1, S - 1)),
        Fraction(falling(R + S, S + 1), rising(D + 1, S)),
    )
    value = max(endpoints)
    return value.numerator // value.denominator


def payload_hash(result: dict[str, int | str | bool]) -> str:
    unsigned = dict(result)
    unsigned.pop("payload_sha256", None)
    canonical = json.dumps(unsigned, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode()).hexdigest()


def solve() -> dict[str, int | str | bool]:
    resource = margin_resource()

    # Start every record at theta=1 and raw margin 1.  Promoting a record to
    # theta=d+1 costs d extra units and may reduce its guaranteed core from
    # m-1 to zero.  This is more efficient than spending a unit on any
    # unpromoted record, which reduces the guaranteed core by only one.
    promoted = min(UNSAFE, (resource - UNSAFE) // D)
    remainder = resource - (UNSAFE + promoted * D)
    unpromoted = UNSAFE - promoted

    require(0 <= remainder < D, "resource remainder outside [0,d)")
    require(0 < promoted < UNSAFE, "capped-record count outside range")
    require(unpromoted > 0, "no unpromoted record")

    minimum_core_incidence = unpromoted * (M - 1) - remainder
    forced_heavy_coordinate = (
        minimum_core_incidence + DOMAIN_LENGTH - 1
    ) // DOMAIN_LENGTH
    shortfall = TARGET_CHILD - forced_heavy_coordinate
    fantasy_full_support_incidence_average = (
        UNSAFE * M + DOMAIN_LENGTH - 1
    ) // DOMAIN_LENGTH
    fantasy_full_support_incidence_shortfall = (
        TARGET_CHILD - fantasy_full_support_incidence_average
    )
    require(
        fantasy_full_support_incidence_average < TARGET_CHILD,
        "full selected-support incidence unexpectedly pays child",
    )

    # The actual-line gluing quotient has a rank-zero branch.  In that
    # branch, raw-low records all use the same global pair and inject through
    # distinct nonempty exception coordinates outside a core of size at
    # least m.  If L0 is their count, the remaining records each cost d+1
    # units.  The exact upper envelope is increasing in L0, so L0=n-m is
    # optimal.
    gluing_rank_zero_low = DOMAIN_LENGTH - M
    gluing_rank_zero_high = (
        resource - gluing_rank_zero_low
    ) // (D + 1)
    gluing_rank_zero_cap = gluing_rank_zero_low + gluing_rank_zero_high
    gluing_rank_zero_slack = TARGET_CHILD - gluing_rank_zero_cap
    require(
        gluing_rank_zero_cap == 49_106_899_082_787_469,
        "gluing rank-zero exact cap drift",
    )
    require(
        gluing_rank_zero_cap < TARGET_CHILD,
        "gluing rank-zero branch does not fit child target",
    )
    require(
        all(
            l0 + (resource - l0) // (D + 1) <= gluing_rank_zero_cap
            for l0 in (0, 1, gluing_rank_zero_low - 1, gluing_rank_zero_low)
        ),
        "gluing rank-zero endpoint is not maximal",
    )

    # Add the strongest currently proved scalar pair constraints at margin
    # one.  A fixed pair owns at most n-(m-1)=R-d+1 singleton-exception
    # records, while interleaving bounds the number of distinct pair types by
    # Q_11(1).  The extremal histogram still fits by a wide margin.
    fixed_pair_capacity = R - D + 1
    margin_one_records = unpromoted - 1
    pair_types_needed = (
        margin_one_records + fixed_pair_capacity - 1
    ) // fixed_pair_capacity
    pair_type_cap = comb(R + S, S) // comb(D - 1 + S, S)
    require(pair_type_cap**2 < LINE_FIELD_ORDER, "sub-square field guard fails")
    require(
        pair_types_needed <= pair_type_cap,
        "abstract margin-one pair types exceed interleaving cap",
    )

    # The explicit abstract histogram attains every scalar constraint:
    # promoted records have theta=d+1 and raw margin m; one record has
    # theta=1+remainder; all other records have theta=1.
    histogram_resource = (
        promoted * (D + 1)
        + (1 + remainder)
        + (unpromoted - 1)
    )
    histogram_core = (
        0
        + (M - 1 - remainder)
        + (unpromoted - 1) * (M - 1)
    )
    require(histogram_resource == resource, "histogram resource mismatch")
    require(histogram_core == minimum_core_incidence, "histogram core mismatch")
    require(
        forced_heavy_coordinate < TARGET_CHILD,
        "scalar first moment unexpectedly pays child",
    )

    result: dict[str, int | str | bool] = {
        "schema": "kb-mca-rank12-scalar-resource-barrier-v1",
        "counting_unit": "distinct_affine_slopes_on_one_actual_received_line",
        "R": R,
        "d": D,
        "n": DOMAIN_LENGTH,
        "m": M,
        "post_near_unsafe_load": UNSAFE,
        "rank_ten_child_target": TARGET_CHILD,
        "C_11_R": resource,
        "promoted_cap_records": promoted,
        "unpromoted_records": unpromoted,
        "residual_resource": remainder,
        "minimum_abstract_core_incidence": minimum_core_incidence,
        "largest_coordinate_forced_by_first_moment": forced_heavy_coordinate,
        "child_target_shortfall": shortfall,
        "fantasy_every_record_full_support_incidence_average": (
            fantasy_full_support_incidence_average
        ),
        "fantasy_full_support_incidence_child_shortfall": (
            fantasy_full_support_incidence_shortfall
        ),
        "gluing_rank_zero_raw_low_cap": gluing_rank_zero_low,
        "gluing_rank_zero_raw_high_cap": gluing_rank_zero_high,
        "gluing_rank_zero_total_cap": gluing_rank_zero_cap,
        "gluing_rank_zero_child_target_slack": gluing_rank_zero_slack,
        "fixed_pair_singleton_capacity": fixed_pair_capacity,
        "margin_one_records": margin_one_records,
        "pair_types_needed_for_margin_one_records": pair_types_needed,
        "interleaved_pair_type_cap_Q_11_1": pair_type_cap,
        "pair_type_capacity_slack": pair_type_cap - pair_types_needed,
        "line_field_order": LINE_FIELD_ORDER,
        "sub_square_guard": True,
        "scalar_resource_first_moment_pays_rank12": False,
        "scalar_resource_barrier_proved": True,
        "gluing_rank_zero_paid": True,
        "gluing_rank_one_paid": False,
        "gluing_rank_two_paid": False,
        "affine_error_rank12_paid": False,
        "koalabear_closed": False,
        "abstract_histogram_claimed_rs_realizable": False,
        "active_v4_ledger_movement": 0,
    }
    result["payload_sha256"] = payload_hash(result)
    return result


def validate_result(result: dict[str, int | str | bool]) -> None:
    require(result.get("schema") == "kb-mca-rank12-scalar-resource-barrier-v1", "schema drift")
    require(result.get("counting_unit") == "distinct_affine_slopes_on_one_actual_received_line", "counting unit drift")
    require(result.get("payload_sha256") == payload_hash(result), "payload hash mismatch")
    require(result.get("n") == result.get("R", 0) + result.get("R", 0), "domain-length identity fails")
    require(result.get("m") == result.get("R", 0) + result.get("d", 0), "agreement identity fails")
    require(result.get("post_near_unsafe_load") == BUDGET - 2 * D + 1, "unsafe-load identity fails")
    require(result.get("C_11_R") == margin_resource(), "margin resource drift")
    require(
        result.get("largest_coordinate_forced_by_first_moment")
        + result.get("child_target_shortfall")
        == result.get("rank_ten_child_target"),
        "first-moment target identity fails",
    )
    require(
        result.get("gluing_rank_zero_total_cap")
        + result.get("gluing_rank_zero_child_target_slack")
        == result.get("rank_ten_child_target"),
        "gluing target identity fails",
    )
    require(result.get("scalar_resource_barrier_proved") is True, "barrier claim drift")
    require(result.get("gluing_rank_zero_paid") is True, "rank-zero claim drift")
    require(result.get("gluing_rank_one_paid") is False, "rank-one nonclaim drift")
    require(result.get("gluing_rank_two_paid") is False, "rank-two nonclaim drift")
    require(result.get("affine_error_rank12_paid") is False, "rank-twelve nonclaim drift")
    require(result.get("active_v4_ledger_movement") == 0, "ledger movement drift")
    require(result.get("koalabear_closed") is False, "KoalaBear nonclaim drift")
    require(result == solve(), "canonical result mismatch")


def hostile_mutations(result: dict[str, int | str | bool]) -> int:
    expected = {
        "C_11_R": 3_313_389_801_746_721_900_417,
        "promoted_cap_records": 49_103_551_414_195_675,
        "residual_resource": 56_673,
        "minimum_abstract_core_incidence": 252_089_545_421_228_709_377_370,
        "largest_coordinate_forced_by_first_moment": 120_205_662_451_376_300,
        "child_target_shortfall": 128_500_736_889_912_070,
        "fantasy_every_record_full_support_incidence_average": 146_337_362_121_160_346,
        "fantasy_full_support_incidence_child_shortfall": 102_369_037_220_128_024,
        "gluing_rank_zero_raw_low_cap": 981_104,
        "gluing_rank_zero_raw_high_cap": 49_106_899_081_806_365,
        "gluing_rank_zero_total_cap": 49_106_899_082_787_469,
        "gluing_rank_zero_child_target_slack": 199_599_500_258_500_901,
        "fixed_pair_singleton_capacity": 981_105,
        "margin_one_records": 225_877_176_697_064_468,
        "pair_types_needed_for_margin_one_records": 230_227_321_946,
        "interleaved_pair_type_cap_Q_11_1": 12_761_830_235_484,
        "pair_type_capacity_slack": 12_531_602_913_538,
    }
    for key, value in expected.items():
        require(result[key] == value, f"exact value mismatch: {key}")

    mutations = [
        ("C_11_R", result["C_11_R"] - 1),
        ("promoted_cap_records", result["promoted_cap_records"] - 1),
        (
            "largest_coordinate_forced_by_first_moment",
            result["largest_coordinate_forced_by_first_moment"] - 1,
        ),
        (
            "pair_types_needed_for_margin_one_records",
            result["pair_types_needed_for_margin_one_records"] - 1,
        ),
        ("sub_square_guard", False),
        (
            "fantasy_every_record_full_support_incidence_average",
            result["rank_ten_child_target"],
        ),
        ("abstract_histogram_claimed_rs_realizable", True),
        ("gluing_rank_zero_paid", False),
    ]
    caught = 0
    for field, bad in mutations:
        mutant = copy.deepcopy(result)
        mutant[field] = bad
        mutant["payload_sha256"] = payload_hash(mutant)
        try:
            validate_result(mutant)
        except ValueError:
            caught += 1
    require(caught == len(mutations), "hostile mutation escaped")
    return caught


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()

    result = solve()
    validate_result(result)
    caught = hostile_mutations(result)
    if args.write_result:
        RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
        RESULT_PATH.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
        print(f"WROTE {RESULT_PATH}")
    elif args.json:
        print(json.dumps(result, sort_keys=True, indent=2))
    else:
        print("KB_MCA_RANK12_SCALAR_RESOURCE_BARRIER_PASS")
        print(f"C_11_R={result['C_11_R']}")
        print(
            "forced_heavy_coordinate="
            f"{result['largest_coordinate_forced_by_first_moment']}"
        )
        print(f"child_target_shortfall={result['child_target_shortfall']}")
        print(f"gluing_rank_zero_cap={result['gluing_rank_zero_total_cap']}")
        print(f"mutations={caught}/{caught}")


if __name__ == "__main__":
    main()
