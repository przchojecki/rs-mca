#!/usr/bin/env python3
"""Verify the order-two source-facet and interpolation packet."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
from collections import Counter
from itertools import combinations
from pathlib import Path
from typing import Any, Callable

if not __debug__:
    raise RuntimeError("verifier refuses optimized Python execution")


class VerificationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


EXPERIMENTAL = Path(__file__).resolve().parents[1]
REPO_ROOT = EXPERIMENTAL.parent
CERTIFICATE = (
    EXPERIMENTAL
    / "data/certificates/kb-mca-v4-m2-r4-order2-source-facet-interpolation-v1"
    / "kb_mca_v4_m2_r4_order2_source_facet_interpolation_v1.json"
)

ROUTER_PARENT = {
    "commit": "d4063dcd9c56835c3916ef792e263ea720a4d397",
    "certificate_path": "experimental/data/certificates/kb-mca-v4-m2-v4-outer-recurrence-router-v1/kb_mca_v4_m2_v4_outer_recurrence_router_v1.json",
    "certificate_blob_oid": "50d17f218bfa7d3acb211c946db0c025b9a98944",
    "certificate_payload_sha256": "fe8141810501fd7b3762a378210609177185972ec706bf9ac943fa398bd82d39",
    "terminal": "M2_V4_STABILIZERS_OUTER_RECURRENCE_AND_SOURCE_PARITY",
}
SOURCE_FACET = {
    "commit": "44542e91e459364a521870ed2ebde7f6fe5055bf",
    "theorem_path": "experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/proof/pole_disjoint_conic_facet_collinearity_reduction.md",
    "theorem_blob_oid": "356ff4b47d0bb429d11ea10382762a6e95b5ce24",
    "certificate_path": "experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/pole_disjoint_conic_facet_collinearity_certificate.json",
    "certificate_blob_oid": "91643b5b9020f52764a77cfbc8aa6279ce2d5ef8",
    "certificate_payload_sha256": "396697687aa5baf19d8114b20858d4500b119c078f5f128b6c0e207ec8ff50bb",
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def payload_hash(value: dict[str, Any]) -> str:
    unhashed = copy.deepcopy(value)
    unhashed.pop("payload_sha256", None)
    return hashlib.sha256(canonical_json(unhashed).encode()).hexdigest()


def reject_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise VerificationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def parse_json(text: str, label: str) -> dict[str, Any]:
    try:
        value = json.loads(text, object_pairs_hook=reject_duplicates)
    except (json.JSONDecodeError, VerificationError) as error:
        raise VerificationError(f"cannot parse {label}: {error}") from error
    require(isinstance(value, dict), f"{label} is not an object")
    return value


def git_output(*args: str) -> str:
    try:
        result = subprocess.run(
            ["git", *args], cwd=REPO_ROOT, check=True, capture_output=True, text=True
        )
    except subprocess.CalledProcessError as error:
        raise VerificationError(error.stderr.strip()) from error
    return result.stdout.strip()


def load_pinned(record: dict[str, str]) -> dict[str, Any]:
    path = record["certificate_path"]
    require(
        git_output("rev-parse", f"{record['commit']}:{path}")
        == record["certificate_blob_oid"],
        f"parent blob {path}",
    )
    data = parse_json(git_output("show", f"{record['commit']}:{path}"), path)
    require(data.get("payload_sha256") == record["certificate_payload_sha256"],
            f"parent payload {path}")
    require(payload_hash(data) == data.get("payload_sha256"), f"parent seal {path}")
    return data


def verify_parents() -> None:
    router = load_pinned(ROUTER_PARENT)
    require(
        router["statement"]["terminal"] == ROUTER_PARENT["terminal"],
        "router terminal",
    )
    rows = router["v4_stabilizer_replay"]["rows"]
    require(
        {"r": 4, "delta": 2, "stabilizer": "one_of_three_C2"} in rows,
        "order-two row",
    )

    require(
        git_output("rev-parse", f"{SOURCE_FACET['commit']}:{SOURCE_FACET['theorem_path']}")
        == SOURCE_FACET["theorem_blob_oid"],
        "source theorem blob",
    )
    source = load_pinned(SOURCE_FACET)
    statuses = source["theorem_status"]
    require(statuses["q6_s6_source_label_near_coincidence_9_25"] == "PROVED",
            "Corollary 9.25")
    require(statuses["q6_s6_source_facet_deck_9_27"] == "PROVED",
            "Corollary 9.27")
    require(
        source["outgoing_conjugate_ledger"]["q6_s6_source_facet_common_size"] == 5,
        "common-five size",
    )


def edge(a: int, b: int) -> frozenset[int]:
    return frozenset((a, b))


def coordinate_replay() -> dict[str, Any]:
    invariant = set(range(6))
    complement = set(range(6, 12))
    bar = {
        0: 1, 1: 0, 2: 3, 3: 2, 4: 5, 5: 4,
        6: 7, 7: 6, 8: 9, 9: 8, 10: 11, 11: 10,
    }

    k_orbits = [
        (edge(6, 8), edge(7, 9)),
        (edge(6, 10), edge(7, 11)),
        (edge(6, 11), edge(7, 10)),
        (edge(8, 10), edge(9, 11)),
        (edge(8, 11), edge(9, 10)),
    ]
    eta_orbit = (edge(0, 2), edge(1, 3))
    records = [
        (6, 2, (8, 10), (edge(0, 4), edge(1, 5))),
        (7, 3, (9, 11), (edge(0, 5), edge(1, 4))),
        (8, 0, (10, 11), (edge(2, 4), edge(3, 5))),
        (9, 1, (6, 7), (edge(2, 5), edge(3, 4))),
        (10, 4, (6, 7), (edge(0, 6), edge(1, 7))),
        (11, 5, (8, 9), (edge(2, 8), edge(3, 9))),
    ]
    all_orbits = k_orbits + [eta_orbit] + [record[3] for record in records]
    for first, second in all_orbits:
        require(frozenset(bar[x] for x in first) == second, "bar orbit")

    stars = [value for pair in all_orbits for value in pair]
    require(len(stars) == len(set(stars)) == 24, "distinct stars")
    categories = Counter()
    for value in stars:
        if value <= invariant:
            categories["I-I"] += 1
        elif value <= complement:
            categories["J-J"] += 1
        else:
            categories["I-J"] += 1
    require(categories == Counter({"I-I": 10, "J-J": 10, "I-J": 4}),
            "category census")

    degrees = Counter(vertex for value in stars for vertex in value)
    require([degrees[i] for i in range(12)] == [4] * 12, "source degrees")
    defect = sum(weight * (weight - 1) // 2
                 for weight in Counter(stars).values())
    require(defect == 0, "fixture defect")

    k_degrees = Counter(
        vertex for pair in k_orbits for value in pair for vertex in value
    )
    require(sorted(k_degrees[j] for j in complement) == [3, 3, 3, 3, 4, 4],
            "fixture K profile")

    left_degrees = Counter()
    for right, omitted, neighbors, pair in records:
        require(right not in neighbors, "diagonal-free pole graph")
        for neighbor in neighbors:
            left_degrees[neighbor] += 1
        common = invariant - {omitted}
        first, second = pair
        if first <= invariant:
            require(first <= common and second <= common, "common facet")
        else:
            require(len(first & complement) == len(second & complement) == 1,
                    "one exchange")
            require(next(iter(first & complement)) == neighbors[0], "first exchange")
            require(next(iter(second & complement)) == neighbors[1], "second exchange")
    require([left_degrees[j] for j in complement] == [2] * 6, "pole degrees")
    colored = sum(2 for *_, pair in records if not pair[0] <= invariant)
    require(colored == 4, "component colors")

    profiles = [
        [[4, 4], [4, 4], [2, 2]],
        [[4, 4], [3, 3], [3, 3]],
    ]
    return {
        "category_census": dict(categories),
        "exhaustive_K_pair_degree_profiles": profiles,
        "fixture_aligned_L_equals_I": True,
        "fixture_stars": [sorted(value) for value in stars],
        "source_degrees": [degrees[i] for i in range(12)],
        "pole_left_degrees": [left_degrees[j] for j in complement],
        "component_colored_edges": colored,
        "defect": defect,
    }


def inverse(value: int, prime: int) -> int:
    return pow(value % prime, prime - 2, prime)


def interpolation_replay() -> dict[str, Any]:
    prime = 101
    labels = list(range(12))
    weights = []
    for i, value in enumerate(labels):
        denominator = 1
        for j, other in enumerate(labels):
            if i != j:
                denominator = denominator * (value - other) % prime
        weights.append(inverse(denominator, prime))
    parity = [
        [weights[i] * pow(labels[i], degree, prime) % prime for i in range(12)]
        for degree in range(7)
    ]
    coefficients = [
        [(7 * a + 11 * b + 3 * a * b + 5) % prime for b in range(5)]
        for a in range(5)
    ]
    scales = [(13 * p + 9) % prime or 1 for p in range(12)]
    fibers = []
    for p, value in enumerate(labels):
        fibers.append([
            sum(coefficients[a][b] * pow(value, b, prime) for b in range(5))
            * inverse(scales[p], prime) % prime
            for a in range(5)
        ])
    matrix = [
        [check[p] * fibers[p][a] % prime for p in range(12)]
        for a in range(5)
        for check in parity
    ]
    residual = [
        sum(row[p] * scales[p] for p in range(12)) % prime
        for row in matrix
    ]
    require(len(matrix) == 35 and all(len(row) == 12 for row in matrix),
            "interpolation dimensions")
    require(residual == [0] * 35 and all(scales), "full-support replay")
    return {
        "field": prime,
        "parity_rows": 7,
        "quartic_coefficients": 5,
        "matrix_rows": 35,
        "matrix_columns": 12,
        "kernel_full_support": True,
        "kernel_residual": residual,
        "matrix_sha256": hashlib.sha256(canonical_json(matrix).encode()).hexdigest(),
    }


def expected_certificate() -> dict[str, Any]:
    data = {
        "schema": "kb-mca-v4-m2-r4-order2-source-facet-interpolation-v1",
        "parents": {
            "router": ROUTER_PARENT,
            "source_facet": SOURCE_FACET,
        },
        "coordinate_orientation": {
            "preserving_lift": "(T,X)->(tau(T),b(X))",
            "individual_star_equivariance": True,
            "involution_preserves_I_and_J": True,
            "replay": coordinate_replay(),
            "route_fence": "facet, degree, color, involution, and defect ledgers admit an aligned abstract survivor",
        },
        "diagonal_orientation": {
            "individual_star_equivariance_claimed": False,
            "whole_fiber_transport": "[R_bar(p)]=[tau^*R_p]",
            "global_divisor": "product_p R_p is proportional to A^4",
            "interpolation_equivalence": "full-support kernel iff bidegree-at-most-(4,4) biform interpolant",
            "replay": interpolation_replay(),
        },
        "conclusion": {
            "order_two_type_deleted": False,
            "coordinate_orientation_deleted": False,
            "diagonal_orientation_deleted": False,
            "k3_status": "OPEN",
            "koalabear_row_status": "OPEN",
            "terminal": "M2_R4_ORDER_TWO_SOURCE_FACET_AND_DIAGONAL_INTERPOLATION_INTERFACES",
        },
        "nonclaims": [
            "no algebraic realization of the aligned coordinate fixture",
            "no universal coordinate coefficient or diagonal kernel failure",
            "no deletion of any order-two subgroup or the trivial m2 type",
            "no carrier, data, explaining-polynomial, slope owner, or payment",
            "no K3, KoalaBear row, endpoint, or Prize close",
        ],
    }
    data["payload_sha256"] = payload_hash(data)
    return data


def verify_data(data: dict[str, Any]) -> None:
    require(payload_hash(data) == data.get("payload_sha256"), "certificate seal")
    require(data == expected_certificate(), "certificate content")


def tamper_selftest(data: dict[str, Any]) -> int:
    mutations: list[Callable[[dict[str, Any]], None]] = [
        lambda x: x["coordinate_orientation"].__setitem__(
            "involution_preserves_I_and_J", False),
        lambda x: x["coordinate_orientation"]["replay"]["category_census"].__setitem__(
            "I-J", 5),
        lambda x: x["coordinate_orientation"]["replay"].__setitem__("defect", 1),
        lambda x: x["coordinate_orientation"]["replay"].__setitem__(
            "component_colored_edges", 5),
        lambda x: x["coordinate_orientation"]["replay"].__setitem__(
            "fixture_aligned_L_equals_I", False),
        lambda x: x["coordinate_orientation"].__setitem__("route_fence", "deletion"),
        lambda x: x["diagonal_orientation"].__setitem__(
            "individual_star_equivariance_claimed", True),
        lambda x: x["diagonal_orientation"].__setitem__(
            "global_divisor", "product is A^3"),
        lambda x: x["diagonal_orientation"]["replay"].__setitem__("matrix_rows", 34),
        lambda x: x["diagonal_orientation"]["replay"].__setitem__(
            "kernel_full_support", False),
        lambda x: x["diagonal_orientation"]["replay"].__setitem__(
            "matrix_sha256", "0" * 64),
        lambda x: x["conclusion"].__setitem__("order_two_type_deleted", True),
        lambda x: x["conclusion"].__setitem__("coordinate_orientation_deleted", True),
        lambda x: x["conclusion"].__setitem__("k3_status", "CLOSED"),
        lambda x: x["conclusion"].__setitem__("koalabear_row_status", "CLOSED"),
        lambda x: x["parents"]["router"].__setitem__(
            "certificate_payload_sha256", "0" * 64),
        lambda x: x.__setitem__("payload_sha256", "0" * 64),
    ]
    rejected = 0
    for mutation in mutations:
        hostile = copy.deepcopy(data)
        mutation(hostile)
        try:
            verify_data(hostile)
        except VerificationError:
            rejected += 1
    require(rejected == len(mutations), "tamper self-test")
    return rejected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    verify_parents()
    expected = expected_certificate()
    if args.write:
        CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE.write_text(json.dumps(expected, indent=2, sort_keys=True) + "\n")
    if args.check or not args.write:
        require(CERTIFICATE.is_file(), "missing certificate")
        data = parse_json(CERTIFICATE.read_text(), str(CERTIFICATE))
        verify_data(data)
    else:
        data = expected
    rejected = tamper_selftest(data) if args.tamper_selftest else 0
    print(
        "KB_MCA_V4_M2_R4_ORDER2_SOURCE_FACET_INTERPOLATION_PASS "
        f"coordinate_defect={data['coordinate_orientation']['replay']['defect']} "
        f"matrix={data['diagonal_orientation']['replay']['matrix_rows']}x"
        f"{data['diagonal_orientation']['replay']['matrix_columns']} "
        f"tamper_rejected={rejected}"
    )


if __name__ == "__main__":
    main()
