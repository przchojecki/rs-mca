#!/usr/bin/env python3
"""Verify the M31 rank-seven shallow master-denominator cut.

The packet has two exact, source-bound consequences.

1.  The lcm/master-denominator normalization forces every proper fixed-G
    slice of a zero-anchored rank-seven shallow family into a rank-at-most-six
    ordinary RS list.  The only slice that can retain rank seven is G=P.
2.  A convex-reciprocal refinement of the codimension-one dual pays the 26
    additional union sizes 354973..354998.

The packet does not aggregate different G-slices, close rank seven, touch
rank at least eight, or move a Grande Finale v4 ledger atom.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from fractions import Fraction
from math import comb
from pathlib import Path
from typing import Any, Iterable


FIELD_PRIME = 2**31 - 1
N = 2**21
K = 2**20
A = 1_116_023
R = N - A
W = A - K
B_STAR = 2**24 - 1
DEEP_CAP = 1_001_282
SHALLOW_SIZE = B_STAR - DEEP_CAP
SHALLOW_TARGET = SHALLOW_SIZE - 1
S_MAX = 366_886

RANK = 7
Q_PROFILE = W + 1
D6_MIN = N - K + 6
T0_TURN = 1_177_354

OLD_RESIDUAL_MIN = 72_428
OLD_RESIDUAL_MAX = 354_998
NEW_HARMONIC_MIN = 354_973
NEW_RESIDUAL_MAX = NEW_HARMONIC_MIN - 1
PURE_FIXED_G_CUTOFF = 328_678
LOW_MIXED_END = 72_859

SCHEMA_ID = "m31-rank7-shallow-master-denominator-cut-summary-v1"
THEOREM_ID = "M31_RANK7_SHALLOW_MASTER_DENOMINATOR_CUT_V1"
ARCHITECTURE_ID = "M31_BASE_FIELD_BOUNDARY_RANK7_MASTER_DENOMINATOR_V1"
STATUS = "PROVED_MASTER_NORMALIZATION_FIXED_G_AND_HARMONIC_FLANK_ROW_OPEN"
PARENT_PAYLOAD = (
    "914ee52fa6c4df6697268ca36d825f01361cad4a6a9d6d1c3f0edd822f379cd8"
)


class VerificationError(RuntimeError):
    """Raised when an exact certificate condition fails."""


CHECKS = 0


def require(condition: bool, label: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise VerificationError(label)


def product(values: Iterable[int]) -> int:
    result = 1
    for value in values:
        result *= value
    return result


def falling(value: int, length: int) -> int:
    require(length >= 0, "falling length nonnegative")
    require(value >= length, "falling argument large enough")
    return product(value - offset for offset in range(length))


def floor_fraction(value: Fraction) -> int:
    return value.numerator // value.denominator


def fraction_record(value: Fraction) -> dict[str, int]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "floor": floor_fraction(value),
    }


def affine_slice_cap(rank: int, degree: int) -> int:
    """Affine-span cap for RS(E0, degree-W) at agreement degree."""
    require(0 <= rank <= degree - W, "slice rank within message dimension")
    require(W + 1 <= degree <= R, "legal fixed-G degree")
    return comb(R - degree + W + rank, rank) // comb(W + rank, rank)


def full_slice_cap(union_size: int) -> int:
    require(W + RANK <= union_size <= R, "legal full-G rank-seven degree")
    return affine_slice_cap(RANK, union_size)


def affine_fiber_cap(dimension: int) -> int:
    require(0 <= dimension <= RANK - 1, "affine fiber dimension")
    return comb((N - K) + dimension, dimension) // comb(
        W + dimension, dimension
    )


def raw_q6_cap(union_size: int, fiber_dimension: int) -> int:
    require(OLD_RESIDUAL_MIN <= union_size <= OLD_RESIDUAL_MAX, "q6 union")
    require(1 <= fiber_dimension <= RANK - 2, "q6 fiber dimension")
    fixed = SHALLOW_SIZE * union_size * product(
        W + index for index in range(fiber_dimension + 1, RANK - 1)
    )
    numerator = affine_fiber_cap(fiber_dimension) * falling(
        R + union_size, RANK - fiber_dimension
    )
    return numerator // fixed - (W + RANK - 1)


def q6_envelope(union_size: int) -> tuple[int, int, int]:
    raw_cap, winner = min(
        (raw_q6_cap(union_size, dimension), dimension)
        for dimension in range(1, RANK - 1)
    )
    strict_cap = union_size - W - RANK
    require(strict_cap >= 0, "strict generalized-weight cap")
    return min(raw_cap, strict_cap), winner, raw_cap


def pi_profile(d6: int, layer_mismatch: int) -> int:
    require(d6 >= D6_MIN, "legal d6")
    require(layer_mismatch >= 0, "layer mismatch nonnegative")
    return (d6 - R + layer_mismatch) * product(
        W + index + layer_mismatch for index in range(1, 6)
    )


def old_support_term(d6: int) -> Fraction:
    return Fraction(falling(d6, 6), pi_profile(d6, 0))


def old_layer_term(d6: int, union_size: int) -> Fraction:
    layer = R + union_size - d6
    require(layer >= 1, "strict support layer")
    return Fraction(
        falling(d6, 7),
        Q_PROFILE * pi_profile(d6, layer),
    )


def harmonic_layer_term(d6: int, union_size: int) -> Fraction:
    """The improved second resource after reciprocal-convex interpolation."""
    layer = R + union_size - d6
    require(1 <= layer <= Q_PROFILE, "harmonic layer range")
    constant = R + union_size - Q_PROFILE - 6
    require(constant > 0, "harmonic numerator positive")
    return Fraction(
        falling(d6, 6) * constant,
        Q_PROFILE * pi_profile(d6, layer),
    )


def old_region_majorant(union_size: int, d6_max: int) -> tuple[str, Fraction]:
    """Safe predecessor majorant on a truncated d6 interval."""
    require(D6_MIN <= d6_max < R + union_size, "old region d6 interval")
    low_endpoint = min(T0_TURN, d6_max)
    candidates = [
        (
            "OLD_LOW_PIECE",
            old_support_term(D6_MIN)
            + old_layer_term(low_endpoint, union_size),
        )
    ]
    if d6_max >= T0_TURN:
        candidates.append(
            (
                "OLD_HIGH_ENDPOINT",
                old_support_term(d6_max)
                + old_layer_term(d6_max, union_size),
            )
        )
    return max(candidates, key=lambda item: item[1])


def harmonic_region_majorant(
    union_size: int, d6_min: int, d6_max: int
) -> tuple[str, Fraction]:
    """Safe majorant where e=R+g-d6 is at most Q_PROFILE."""
    require(D6_MIN <= d6_min <= d6_max, "harmonic d6 interval")
    require(
        1 <= R + union_size - d6_max <= Q_PROFILE,
        "harmonic endpoint layer",
    )
    require(
        1 <= R + union_size - d6_min <= Q_PROFILE,
        "harmonic initial layer",
    )

    candidates: list[tuple[str, Fraction]] = []
    if d6_min <= T0_TURN:
        low_endpoint = min(T0_TURN, d6_max)
        candidates.append(
            (
                "HARMONIC_LOW_PIECE",
                old_support_term(d6_min)
                + harmonic_layer_term(low_endpoint, union_size),
            )
        )
    high_start = max(d6_min, T0_TURN)
    if high_start <= d6_max:
        candidates.append(
            (
                "HARMONIC_HIGH_ENDPOINT",
                old_support_term(d6_max)
                + harmonic_layer_term(d6_max, union_size),
            )
        )
    require(bool(candidates), "harmonic candidates nonempty")
    return max(candidates, key=lambda item: item[1])


def refined_profile_majorant(union_size: int) -> dict[str, Any]:
    q6_cap, winner, raw_cap = q6_envelope(union_size)
    d6_max = D6_MIN + q6_cap
    require(d6_max < R + union_size, "strict d6<d7")

    # e<=Q exactly when d6>=R+g-Q.  Keep the predecessor dual on e>Q
    # and use the harmonic dual only on the eligible endpoint interval.
    first_harmonic_d6 = R + union_size - Q_PROFILE
    candidates: list[tuple[str, Fraction]] = []
    old_max = min(d6_max, first_harmonic_d6 - 1)
    if old_max >= D6_MIN:
        candidates.append(old_region_majorant(union_size, old_max))
    harmonic_min = max(D6_MIN, first_harmonic_d6)
    if harmonic_min <= d6_max:
        candidates.append(
            harmonic_region_majorant(union_size, harmonic_min, d6_max)
        )
    require(bool(candidates), "refined profile candidates nonempty")
    owner, bound = max(candidates, key=lambda item: item[1])
    return {
        "q6_cap": q6_cap,
        "q6_winner": winner,
        "q6_raw_cap": raw_cap,
        "d6_max": d6_max,
        "minimum_layer": R + union_size - d6_max,
        "first_harmonic_d6": first_harmonic_d6,
        "owner": owner,
        "bound": bound,
        "component_floors": {
            candidate_owner: floor_fraction(candidate_bound)
            for candidate_owner, candidate_bound in candidates
        },
    }


def harmonic_dual_controls() -> dict[str, Any]:
    """Exact small controls for the reciprocal-convex dual identity."""
    cases = 0
    minimum_margin: Fraction | None = None
    for a_values in ((1,), (1, 3), (2, 4, 7), (3, 5, 8, 11)):
        for e in range(1, 7):
            for Q in range(e, 9):
                p0 = product(a_values)
                pe = product(a + e for a in a_values)
                x = Fraction(1, e * p0) - Fraction(Q - e, e * Q * pe)
                y = Fraction(1, Q * pe)
                require(x >= 0 and y > 0, "harmonic dual weights nonnegative")
                for b in range(e + 1):
                    pb = product(a + b for a in a_values)
                    lhs = (
                        x * (e - b) * pb
                        + y * (Q - e + b) * pb
                    )
                    chord = pb * (
                        Fraction(e - b, e * p0)
                        + Fraction(b, e * pe)
                    )
                    require(lhs == chord, "harmonic dual algebra identity")
                    require(lhs >= 1, "reciprocal-convex dual feasibility")
                    margin = lhs - 1
                    minimum_margin = (
                        margin
                        if minimum_margin is None
                        else min(minimum_margin, margin)
                    )
                    cases += 1
    require(cases == 524, "harmonic control case count")
    require(minimum_margin == 0, "harmonic endpoint equality control")
    return {
        "identity": (
            "x(e-b)P(b)+y(Q-e+b)P(b)="
            "P(b)((e-b)/(eP(0))+b/(eP(e)))"
        ),
        "convex_function": "1/P(z)",
        "dual_weights": {
            "x": "1/(eP(0))-(Q-e)/(eQP(e))",
            "y": "1/(QP(e))",
        },
        "closed_bound": (
            "d_fall_j/P(0)+d_fall_j*(d-j-Q+e)/(QP(e))"
        ),
        "exact_control_cases": cases,
    }


def fixed_g_slice_scan() -> dict[str, Any]:
    small_caps = {
        str(message_dimension): affine_slice_cap(
            message_dimension, W + message_dimension
        )
        for message_dimension in range(1, 6)
    }
    require(
        small_caps
        == {
            "1": 14,
            "2": 211,
            "3": 3_077,
            "4": 44_769,
            "5": 651_202,
        },
        "small fixed-G slice caps",
    )

    degree_six = W + 6
    proper_max = affine_slice_cap(6, degree_six)
    require(proper_max == 9_471_941, "proper fixed-G slice maximum")
    require(proper_max < SHALLOW_SIZE, "proper slice below shallow source")

    before = full_slice_cap(PURE_FIXED_G_CUTOFF - 1)
    at = full_slice_cap(PURE_FIXED_G_CUTOFF)
    require(before == 15_776_081, "full-slice last unresolved cap")
    require(at == 15_775_927, "full-slice first excluded cap")
    require(before > SHALLOW_TARGET, "full-slice adjacent failure")
    require(at <= SHALLOW_TARGET, "full-slice threshold payment")

    forced_proper_mass = {
        str(union_size): SHALLOW_SIZE - full_slice_cap(union_size)
        for union_size in (
            PURE_FIXED_G_CUTOFF,
            340_000,
            350_000,
            NEW_RESIDUAL_MAX,
            OLD_RESIDUAL_MAX,
        )
    }
    require(
        forced_proper_mass
        == {
            "328678": 6,
            "340000": 1_656_948,
            "350000": 2_994_067,
            "354972": 3_617_436,
            "354998": 3_620_626,
        },
        "forced proper-slice mass records",
    )

    return {
        "master_map": "P=lcm_i(G_i), Q_i=P/G_i, f_i=Q_i*b_i",
        "rank_identity": "span(c_i)=(A0/P)*span(f_i)",
        "agreement_identity": (
            "gcd(P*L0,P*H0-f_i)=Q_i*H_i; degree=g+s_i"
        ),
        "exact_union_gate": "no common zero of span(f_i) on Z(P)",
        "proper_slice_rank_cap": 6,
        "proper_slice_formula": (
            "B_k(m)=floor(binomial(R-m+w+k,k)/binomial(w+k,k))"
        ),
        "small_message_dimension_caps": small_caps,
        "proper_slice_maximum": proper_max,
        "proper_slice_gap": SHALLOW_SIZE - proper_max,
        "proper_slice_maximum_degree": degree_six,
        "full_slice_threshold": PURE_FIXED_G_CUTOFF,
        "full_slice_threshold_records": {
            str(PURE_FIXED_G_CUTOFF - 1): before,
            str(PURE_FIXED_G_CUTOFF): at,
        },
        "pure_fixed_g_excluded_range": [PURE_FIXED_G_CUTOFF, R],
        "forced_proper_mass": forced_proper_mass,
    }


def harmonic_flank_scan() -> dict[str, Any]:
    records: dict[str, Any] = {}
    paid: list[int] = []
    maximum_old_component = -1

    for union_size in range(NEW_RESIDUAL_MAX, OLD_RESIDUAL_MAX + 1):
        result = refined_profile_majorant(union_size)
        bound_floor = floor_fraction(result["bound"])
        maximum_old_component = max(
            maximum_old_component,
            max(
                value
                for owner, value in result["component_floors"].items()
                if owner.startswith("OLD_")
            ),
        )
        if bound_floor <= SHALLOW_TARGET:
            paid.append(union_size)
        if union_size in (
            NEW_RESIDUAL_MAX,
            NEW_HARMONIC_MIN,
            OLD_RESIDUAL_MAX,
        ):
            records[str(union_size)] = {
                "q6_cap": result["q6_cap"],
                "d6_max": result["d6_max"],
                "minimum_layer": result["minimum_layer"],
                "owner": result["owner"],
                "bound": fraction_record(result["bound"]),
                "component_floors": result["component_floors"],
            }

    require(
        paid == list(range(NEW_HARMONIC_MIN, OLD_RESIDUAL_MAX + 1)),
        "exact new harmonic paid interval",
    )
    require(
        records[str(NEW_RESIDUAL_MAX)]["bound"]["floor"] == 15_776_055,
        "adjacent harmonic failure",
    )
    require(
        records[str(NEW_HARMONIC_MIN)]["bound"]["floor"] == 15_775_843,
        "first harmonic payment",
    )
    require(
        records[str(OLD_RESIDUAL_MAX)]["bound"]["floor"] == 15_768_132,
        "last predecessor-residual harmonic cap",
    )
    require(maximum_old_component == 15_332_341, "old-region maximum")

    return {
        "new_paid_range": [NEW_HARMONIC_MIN, OLD_RESIDUAL_MAX],
        "new_paid_union_count": OLD_RESIDUAL_MAX - NEW_HARMONIC_MIN + 1,
        "adjacent_failure_excess": (
            records[str(NEW_RESIDUAL_MAX)]["bound"]["floor"]
            - SHALLOW_TARGET
        ),
        "first_payment_margin": (
            SHALLOW_TARGET
            - records[str(NEW_HARMONIC_MIN)]["bound"]["floor"]
        ),
        "last_payment_margin": (
            SHALLOW_TARGET
            - records[str(OLD_RESIDUAL_MAX)]["bound"]["floor"]
        ),
        "maximum_old_region_floor": maximum_old_component,
        "threshold_records": records,
    }


def residual_partition() -> dict[str, Any]:
    require(
        NEW_RESIDUAL_MAX - OLD_RESIDUAL_MIN + 1 == 282_545,
        "new residual count",
    )
    return {
        "old_rank7_union_range": [OLD_RESIDUAL_MIN, OLD_RESIDUAL_MAX],
        "new_rank7_union_range": [OLD_RESIDUAL_MIN, NEW_RESIDUAL_MAX],
        "new_rank7_union_count": NEW_RESIDUAL_MAX - OLD_RESIDUAL_MIN + 1,
        "first_match_types": [
            {
                "union_range": [OLD_RESIDUAL_MIN, LOW_MIXED_END],
                "possible_type": "MIXED_G_ONLY",
                "source": "predecessor fixed-G endpoint owners",
            },
            {
                "union_range": [LOW_MIXED_END + 1, PURE_FIXED_G_CUTOFF - 1],
                "possible_type": "PURE_FIXED_G_OR_MIXED_G",
                "source": "unresolved ordinary-RS middle",
            },
            {
                "union_range": [PURE_FIXED_G_CUTOFF, NEW_RESIDUAL_MAX],
                "possible_type": "MIXED_G_ONLY",
                "source": "master-denominator proper-slice rank drop",
            },
        ],
        "terminal": "UNPAID_RANK7_MIXED_G_FIXED_SYNDROME_INCIDENCE",
    }


def canonical_json(value: Any, *, pretty: bool = False) -> bytes:
    text = json.dumps(
        value,
        sort_keys=True,
        indent=2 if pretty else None,
        separators=None if pretty else (",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )
    return (text + "\n").encode("ascii")


def payload_sha256(payload: dict[str, Any]) -> str:
    unsigned = copy.deepcopy(payload)
    unsigned.pop("payload_sha256", None)
    return hashlib.sha256(canonical_json(unsigned)).hexdigest()


def deep_exact(actual: Any, expected: Any, path: str = "payload") -> None:
    require(type(actual) is type(expected), f"{path}: exact type")
    if isinstance(expected, dict):
        require(set(actual) == set(expected), f"{path}: exact keys")
        for key in expected:
            deep_exact(actual[key], expected[key], f"{path}.{key}")
    elif isinstance(expected, list):
        require(len(actual) == len(expected), f"{path}: exact length")
        for index, (left, right) in enumerate(zip(actual, expected, strict=True)):
            deep_exact(left, right, f"{path}[{index}]")
    else:
        require(actual == expected, f"{path}: exact value")


def build_summary() -> dict[str, Any]:
    global CHECKS
    CHECKS = 0
    require((R, W) == (981_129, 67_447), "deployed radius and excess")
    require(SHALLOW_SIZE == 15_775_933, "shallow source size")
    require(D6_MIN == 1_048_582, "rank-seven d6 floor")

    fixed_g = fixed_g_slice_scan()
    harmonic_lemma = harmonic_dual_controls()
    harmonic = harmonic_flank_scan()
    residual = residual_partition()

    summary: dict[str, Any] = {
        "schema": SCHEMA_ID,
        "theorem_id": THEOREM_ID,
        "architecture": ARCHITECTURE_ID,
        "status": STATUS,
        "parent_payload_sha256": PARENT_PAYLOAD,
        "row": {
            "field_prime": FIELD_PRIME,
            "n": N,
            "K": K,
            "agreement": A,
            "R": R,
            "w": W,
            "B_star": B_STAR,
            "deep_cap": DEEP_CAP,
            "shallow_size": SHALLOW_SIZE,
            "shallow_target": SHALLOW_TARGET,
            "maximum_excess": S_MAX,
            "rank": RANK,
        },
        "fixed_g_slice_cut": fixed_g,
        "harmonic_dual_lemma": harmonic_lemma,
        "harmonic_flank": harmonic,
        "residual_partition": residual,
        "impact": {
            "rank7_union_values_removed": 26,
            "pure_fixed_g_union_values_removed": 26_321,
            "rank7_closed": False,
            "rank8_and_above_closed": False,
            "row_closed": False,
            "ledger_movement": 0,
            "official_endpoint_movement": 0,
        },
        "nonclaims": [
            "Caps on distinct fixed-G slices are not summed.",
            "A mixed-G rank-seven family is not excluded.",
            "No rank-at-least-eight family is excluded.",
            "No Grande Finale v4 atom or official endpoint is moved.",
        ],
    }
    summary["checks"] = CHECKS + 2
    summary["payload_sha256"] = payload_sha256(summary)
    require(summary["payload_sha256"] == payload_sha256(summary), "payload seal")
    require(summary["checks"] == CHECKS + 1, "check counter sealed")
    return summary


def tamper_selftest() -> dict[str, Any]:
    expected = build_summary()
    paths_and_values = [
        (("row", "shallow_size"), SHALLOW_SIZE + 1),
        (("fixed_g_slice_cut", "proper_slice_rank_cap"), 7),
        (("fixed_g_slice_cut", "proper_slice_maximum"), 9_471_942),
        (("fixed_g_slice_cut", "full_slice_threshold"), 328_677),
        (
            (
                "fixed_g_slice_cut",
                "full_slice_threshold_records",
                "328678",
            ),
            15_775_928,
        ),
        (("harmonic_flank", "new_paid_range"), [354_972, 354_998]),
        (("harmonic_flank", "new_paid_union_count"), 27),
        (("harmonic_flank", "first_payment_margin"), 88),
        (
            (
                "harmonic_flank",
                "threshold_records",
                "354972",
                "bound",
                "floor",
            ),
            15_776_054,
        ),
        (("residual_partition", "new_rank7_union_range"), [72_428, 354_973]),
        (("residual_partition", "new_rank7_union_count"), 282_546),
        (("impact", "rank7_closed"), True),
        (("impact", "ledger_movement"), 1),
        (("parent_payload_sha256",), "0" * 64),
    ]
    detected = 0
    for path, value in paths_and_values:
        mutant = copy.deepcopy(expected)
        cursor: Any = mutant
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = value
        try:
            deep_exact(mutant, expected)
        except VerificationError:
            detected += 1
        else:
            raise VerificationError(f"mutation escaped: {'.'.join(path)}")
    require(detected == len(paths_and_values), "all primary mutations detected")
    return {
        "schema": "m31-rank7-master-denominator-primary-tamper-v1",
        "mutations": len(paths_and_values),
        "detected": detected,
        "all_detected": True,
        "base_payload_sha256": expected["payload_sha256"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    try:
        summary = tamper_selftest() if args.tamper_selftest else build_summary()
        encoded = canonical_json(summary, pretty=args.pretty)
        if args.output is not None:
            args.output.write_bytes(encoded)
        if not args.check or args.output is None:
            sys.stdout.buffer.write(encoded)
        return 0
    except (VerificationError, AssertionError, ValueError) as exc:
        print(f"[FAIL] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
