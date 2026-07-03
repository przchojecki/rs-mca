#!/usr/bin/env python3
"""Verify the E23 A=425 second-pin unsafe fallback packet.

This is a row-level support-wise MCA/LD_sw certificate for the budget-prime row

    p = 22275*2^120 + 1,  n = 512,  k = 256.

It proves the E23 decision question on the unsafe side:

    LD_sw(RS[F_p,D,256],425) > floor((p-1)/2^128) = 87.

The proof is the certified lower-witness fallback: an explicit received line has
88 finite slopes, each explained on a support of size 425, while the direction
word is not separately degree-<256 explainable on that support.  The script also
records the direct two-core exact-attempt arithmetic one grid step below the
A=426 row: the large-core branch has upper bound 88, but the low-pair packing
branch only gives 7781, so this packet does not claim exact LD_sw(C,425)=88.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
CERT_DIR = ROOT / "experimental/data/certificates/a425-second-pin-unsafe"
CERT_PATH = CERT_DIR / "a425_second_pin_unsafe.json"

SCHEMA_VERSION = "a425-second-pin-unsafe-v1"
TWO_128 = 1 << 128

N = 512
K = 256
A_UNSAFE = 425
A_CONTEXT_SAFE = 426

P = 22275 * (1 << 120) + 1
P_MINUS_1_FACTORS = {2: 120, 3: 4, 5: 2, 11: 1}
PRIMITIVE_ROOT_WITNESS = 13
DOMAIN_GENERATOR = pow(PRIMITIVE_ROOT_WITNESS, (P - 1) // N, P)

BUDGET_FLOOR = (P - 1) // TWO_128
TANGENT_LOWER_A425 = N + 1 - A_UNSAFE
TANGENT_LOWER_A426 = N + 1 - A_CONTEXT_SAFE


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def render(obj: Any) -> str:
    return json.dumps(obj, indent=2, sort_keys=True) + "\n"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_json(obj: Any) -> str:
    return sha256_bytes(canonical_json(obj).encode("utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def verify_small_prime(q: int) -> None:
    require(q >= 2, f"not prime: {q}")
    d = 2
    while d * d <= q:
        require(q % d != 0, f"not prime: {q}")
        d += 1


def verify_lucas_prime(n: int, factors: dict[int, int], witness: int) -> None:
    product = 1
    for q, exp in factors.items():
        verify_small_prime(q)
        product *= q**exp
    require(product == n - 1, "factorization does not multiply to p-1")
    require(pow(witness, n - 1, n) == 1, "Lucas witness fails Fermat check")
    for q in factors:
        require(
            pow(witness, (n - 1) // q, n) != 1,
            f"Lucas witness has order dividing (p-1)/{q}",
        )


def verify_domain_generator() -> None:
    require(P % N == 1, "p is not 1 modulo 512")
    require(pow(DOMAIN_GENERATOR, N, P) == 1, "domain generator is not 512-torsion")
    require(
        pow(DOMAIN_GENERATOR, N // 2, P) != 1,
        "domain generator has order dividing 256",
    )


def domain_elements() -> list[int]:
    verify_domain_generator()
    elems = [1]
    for _ in range(1, N):
        elems.append((elems[-1] * DOMAIN_GENERATOR) % P)
    require(len(set(elems)) == N, "domain elements are not distinct")
    require((elems[-1] * DOMAIN_GENERATOR) % P == 1, "domain cycle does not close")
    return elems


def budget_prime_record() -> dict[str, Any]:
    verify_lucas_prime(P, P_MINUS_1_FACTORS, PRIMITIVE_ROOT_WITNESS)
    require(BUDGET_FLOOR == 87, "budget floor should be 87")
    require(P // TWO_128 == BUDGET_FLOOR, "p and p-1 budget floors differ")
    return {
        "p": P,
        "p_minus_1_factorization": {str(q): exp for q, exp in P_MINUS_1_FACTORS.items()},
        "lucas_primitive_root_witness": PRIMITIVE_ROOT_WITNESS,
        "p_is_prime_by_lucas": True,
        "target_security_bits": 128,
        "floor_p_minus_1_over_2_128": BUDGET_FLOOR,
        "floor_p_over_2_128": P // TWO_128,
        "remainder_p_minus_1_mod_2_128": (P - 1) % TWO_128,
        "comparison_budget": "87",
    }


def tangent_lower_witness(agreement: int) -> dict[str, Any]:
    require(K + 1 <= agreement <= N, "agreement outside tangent-witness range")
    elems = domain_elements()
    core_size = agreement - 1
    outside_count = N - core_size
    require(outside_count == N + 1 - agreement, "outside count mismatch")

    slopes = list(range(outside_count))
    f_values = [0] * N
    g_values = [0] * N
    for i, index in enumerate(range(core_size, N)):
        f_values[index] = (-i) % P
        g_values[index] = 1

    records = []
    for i, index in enumerate(range(core_size, N)):
        slope = slopes[i]
        support = list(range(core_size)) + [index]
        require(len(support) == agreement, "support size mismatch")
        require(len(set(support)) == agreement, "support indices repeat")
        for support_index in support:
            value = (f_values[support_index] + slope * g_values[support_index]) % P
            require(value == 0, "zero codeword does not explain this slope")
        require(g_values[index] == 1, "direction word is not one at moving coordinate")
        records.append(
            {
                "slope": slope,
                "moving_coordinate_index": index,
                "moving_domain_element": elems[index],
                "support_size": agreement,
                "explaining_codeword": "zero polynomial",
                "noncontained_reason": (
                    f"g has {core_size} zero coordinates on the support and value "
                    "1 at the moving coordinate, so no degree-<256 polynomial can "
                    "agree with g there"
                ),
            }
        )

    require(len(slopes) == len(set(slopes)), "slopes are not distinct")
    require(len(records) == N + 1 - agreement, "record count mismatch")
    return {
        "agreement": agreement,
        "support_threshold": agreement,
        "core_size": core_size,
        "outside_count": outside_count,
        "bad_finite_slope_count": len(slopes),
        "LD_sw_lower_bound": len(slopes),
        "field": {
            "p": P,
            "domain_generator": DOMAIN_GENERATOR,
            "domain_hash_sha256": sha256_json(elems),
        },
        "line_definition": {
            "received_words_are_coordinate_values_on_D": True,
            "core_indices": {"start": 0, "stop_inclusive": core_size - 1, "count": core_size},
            "outside_indices": {"start": core_size, "stop_inclusive": N - 1, "count": outside_count},
            "f_values_rule": (
                f"f=0 on indices < {core_size}; f=-i on index {core_size}+i "
                f"for i=0..{outside_count - 1}"
            ),
            "g_values_rule": f"g=0 on indices < {core_size}; g=1 on indices >= {core_size}",
            "f_values_hash_sha256": sha256_json(f_values),
            "g_values_hash_sha256": sha256_json(g_values),
        },
        "bad_slope_encodings": slopes,
        "bad_slope_hash_sha256": sha256_json(slopes),
        "support_record_hash_sha256": sha256_json(records),
        "records": records,
        "checks": {
            "all_slope_values_are_distinct": True,
            "each_support_has_requested_size": True,
            "zero_codeword_explains_each_line_word_on_its_support": True,
            "direction_word_noncontained_on_each_support": True,
        },
    }


def core_bound_rows(agreement: int) -> list[dict[str, int]]:
    threshold = N + K - agreement
    rows = []
    for common_core_size in range(threshold, N + 1):
        outside = N - common_core_size
        required_per_slope = max(1, agreement - common_core_size)
        rows.append(
            {
                "common_core_size": common_core_size,
                "outside_coordinates": outside,
                "outside_required_per_slope": required_per_slope,
                "bound": outside // required_per_slope,
            }
        )
    return rows


def two_core_attempt_record() -> dict[str, Any]:
    agreement = A_UNSAFE
    complement_size = N - agreement
    pair_core_threshold = N + K - agreement
    low_pair_support_intersection_max = pair_core_threshold - 1
    complement_intersection_max = (
        low_pair_support_intersection_max - N + 2 * complement_size
    )
    packing_subsets_size = complement_intersection_max + 1
    low_pair_bound = math.comb(N, packing_subsets_size) // math.comb(
        complement_size, packing_subsets_size
    )
    rows = core_bound_rows(agreement)
    best = max(rows, key=lambda row: row["bound"])
    tangent_lower = N + 1 - agreement

    require(complement_size == 87, "A=425 complement size mismatch")
    require(pair_core_threshold == 343, "A=425 pair-core threshold mismatch")
    require(complement_intersection_max == 4, "A=425 low-pair intersection mismatch")
    require(low_pair_bound == 7781, "A=425 low-pair packing bound mismatch")
    require(best["bound"] == tangent_lower, "large-core branch should max at tangent count")
    require(best["common_core_size"] == agreement - 1, "large-core argmax mismatch")

    return {
        "status": "AUDIT_EXACT_UPPER_NOT_CLOSED_BY_CHEAP_TWO_CORE_PACKING",
        "agreement": agreement,
        "complement_size": complement_size,
        "pair_core_threshold": {
            "formula": "n+k-A",
            "value": pair_core_threshold,
            "meaning": (
                "a pair intersection this large gives at least k common zeros "
                "for every third residual branch"
            ),
        },
        "case_1_no_large_pair_core": {
            "support_pair_intersection_at_most": low_pair_support_intersection_max,
            "complement_pair_intersection_at_most": complement_intersection_max,
            "packing_subsets_size": packing_subsets_size,
            "packing_bound_formula": "floor(binomial(512,5)/binomial(87,5))",
            "packing_bound": low_pair_bound,
            "binomial_512_5": math.comb(N, packing_subsets_size),
            "binomial_87_5": math.comb(complement_size, packing_subsets_size),
            "closes_against_88": low_pair_bound <= tangent_lower,
        },
        "case_2_large_pair_core": {
            "bound_formula": "floor((n-c)/max(1,A-c)) for c=|common code-line support|",
            "max_bound": best["bound"],
            "max_attained_at_common_core_size": best["common_core_size"],
            "core_bound_rows_hash_sha256": sha256_json(rows),
            "core_bound_rows": rows,
        },
        "exact_upper_status": {
            "claimed_exact_LD_sw_A425": False,
            "large_core_branch_upper_bound": best["bound"],
            "low_pair_branch_upper_bound": low_pair_bound,
            "direct_two_core_attempt_closes": False,
            "reason": "the low-pair packing branch gives 7781, not 88",
        },
    }


def build_certificate() -> dict[str, Any]:
    budget = budget_prime_record()
    a425_witness = tangent_lower_witness(A_UNSAFE)
    two_core = two_core_attempt_record()

    require(TANGENT_LOWER_A425 == 88, "A=425 tangent lower should be 88")
    require(TANGENT_LOWER_A426 == 87, "A=426 tangent lower should be 87")
    require(a425_witness["LD_sw_lower_bound"] == 88, "witness count mismatch")
    require(a425_witness["LD_sw_lower_bound"] > budget["floor_p_minus_1_over_2_128"], "unsafe comparison failed")

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "CERTIFIED_UNSAFE_FALLBACK / EXACT_A425_UPPER_OPEN",
        "evidence_id": "E23",
        "target_node": "second_pin_a426",
        "question": "is LD_sw(RS[F_p,D,256],425) > 87 at the budget-prime row?",
        "row": {
            "code": "RS[F_p,D,256]",
            "n": N,
            "k": K,
            "domain_size": N,
            "domain": "multiplicative subgroup generated by domain_generator",
            "field": "F_p",
        },
        "budget_prime": budget,
        "domain": {
            "domain_generator": DOMAIN_GENERATOR,
            "generator_order": N,
            "domain_hash_sha256": a425_witness["field"]["domain_hash_sha256"],
            "checks": {
                "p_congruent_1_mod_512": P % N == 1,
                "generator_512_torsion": pow(DOMAIN_GENERATOR, N, P) == 1,
                "generator_not_256_torsion": pow(DOMAIN_GENERATOR, N // 2, P) != 1,
            },
        },
        "a426_context": {
            "agreement": A_CONTEXT_SAFE,
            "tangent_lower_bound": TANGENT_LOWER_A426,
            "budget_floor": BUDGET_FLOOR,
            "context_only": (
                "A=426 exact upper is the adjacent row handled by the two-core "
                "packet; this E23 packet only certifies the A=425 unsafe side."
            ),
        },
        "a425_lower_witness": a425_witness,
        "a425_two_core_exact_attempt": two_core,
        "verdict": {
            "LD_sw_lower_bound_A425": a425_witness["LD_sw_lower_bound"],
            "budget_floor": BUDGET_FLOOR,
            "comparison": "88 > 87",
            "finite_slope_support_wise_mca_status": "UNSAFE_BY_CERTIFIED_LOWER_WITNESS",
            "exact_evaluation_status": "not proved by this packet",
        },
        "nonclaims": [
            "does not prove LD_sw(RS[F_p,D,256],425)=88",
            "does not close the A=425 low-pair exact upper branch",
            "does not reprove the adjacent A=426 exact upper certificate",
            "does not address infinite/projective-slope conventions",
        ],
    }


def check_certificate(path: Path) -> None:
    actual = path.read_text(encoding="utf-8")
    expected = render(build_certificate())
    if actual != expected:
        raise AssertionError(f"certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    verdict = certificate["verdict"]
    exact = certificate["a425_two_core_exact_attempt"]["exact_upper_status"]
    print("E23 A=425 second-pin unsafe packet")
    print(f"prime budget: floor((p-1)/2^128) = {verdict['budget_floor']}")
    print(
        "A=425 lower witness: LD_sw >= "
        f"{verdict['LD_sw_lower_bound_A425']} ({verdict['comparison']})"
    )
    print(f"status: {verdict['finite_slope_support_wise_mca_status']}")
    print(
        "exact attempt: large-core <= {large_core_branch_upper_bound}, "
        "low-pair <= {low_pair_branch_upper_bound}; closes={direct_two_core_attempt_closes}".format(
            **exact
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write",
        nargs="?",
        const=CERT_PATH,
        type=Path,
        help="write deterministic certificate JSON, optionally to PATH",
    )
    parser.add_argument(
        "--check",
        nargs="?",
        const=CERT_PATH,
        type=Path,
        help="check deterministic certificate JSON, optionally at PATH",
    )
    parser.add_argument("--json", action="store_true", help="print certificate JSON")
    args = parser.parse_args()

    certificate = build_certificate()
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(render(certificate), encoding="utf-8")
    if args.check:
        check_certificate(args.check)
    if args.json:
        print(render(certificate), end="")
        return
    print_summary(certificate)


if __name__ == "__main__":
    main()
