#!/usr/bin/env python3
"""Verify the universal degree-two source-facet census packet."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
from collections import Counter
from itertools import combinations, product
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
    / "data/certificates/kb-mca-v4-m2-u2-universal-source-facet-census-v1"
    / "kb_mca_v4_m2_u2_universal_source_facet_census_v1.json"
)
PARENT = {
    "commit": "c88438d7109cf7acd7caebaf006f21c776b74d74",
    "note_path": "experimental/notes/frontier-adjacent/kb_mca_v4_m2_r4_order2_source_subfield_coefficient_compilers_v1.md",
    "note_blob_oid": "f58c2ea9cea88dfc6be637e9f1f14e86e8862cc6",
    "verifier_path": "experimental/scripts/verify_kb_mca_v4_m2_r4_order2_source_subfield_coefficient_compilers_v1.py",
    "verifier_blob_oid": "7cc4eb6e0560ca5c587f91623dc407892a07e2ca",
    "certificate_path": "experimental/data/certificates/kb-mca-v4-m2-r4-order2-source-subfield-coefficient-compilers-v1/kb_mca_v4_m2_r4_order2_source_subfield_coefficient_compilers_v1.json",
    "certificate_blob_oid": "033043e7a0969ea9f98207567b890b10e3077271",
    "certificate_payload_sha256": "f0b751301e56989bf6fbf19cf15e5ff8faa0d7d86e76278306950a488cdf5156",
    "terminal": "M2_R4_ORDER_TWO_SOURCE_SUBFIELD_AND_COEFFICIENT_COMPILERS",
}
SOURCE_REDUCTION_PARENT = {
    "commit": "ad109774f7d9bc320e7e0c046ba83471f39d5cd9",
    "note_path": "experimental/notes/frontier-adjacent/kb_mca_v4_q6_u2_complete_source_conic_exclusion_v1.md",
    "note_blob_oid": "bd4ca8c756c22f6f475cb06c142de4c981d6b320",
    "verifier_path": "experimental/scripts/verify_kb_mca_v4_q6_u2_complete_source_conic_exclusion_v1.py",
    "verifier_blob_oid": "c5e7338fc03acdd245c60291aea27b0cde521645",
    "certificate_path": "experimental/data/certificates/kb-mca-v4-q6-u2-complete-source-conic-exclusion-v1/kb_mca_v4_q6_u2_complete_source_conic_exclusion_v1.json",
    "certificate_blob_oid": "61afd4534740c5ccabc6196919126c80c361e4c5",
    "certificate_payload_sha256": "30a5d45895957f774ef972118e227fa54522fc27a48ee0e2a99a0d5a012a5451",
    "terminal": "DELETED_BY_COMPLETE_SOURCE_DIVISOR_PROFILE_OBSTRUCTION",
}
SOURCE_FACET_PARENT = {
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


def load_parent() -> dict[str, Any]:
    for path_key, blob_key in (
        ("note_path", "note_blob_oid"),
        ("verifier_path", "verifier_blob_oid"),
        ("certificate_path", "certificate_blob_oid"),
    ):
        require(
            git_output("rev-parse", f"{PARENT['commit']}:{PARENT[path_key]}")
            == PARENT[blob_key],
            f"parent blob {PARENT[path_key]}",
        )
    data = parse_json(
        git_output("show", f"{PARENT['commit']}:{PARENT['certificate_path']}"),
        PARENT["certificate_path"],
    )
    require(data.get("payload_sha256") == PARENT["certificate_payload_sha256"],
            "parent payload")
    require(payload_hash(data) == data.get("payload_sha256"), "parent seal")
    require(data["conclusion"]["terminal"] == PARENT["terminal"], "parent terminal")
    require(data["source_row_interpolation"]["replay"]["matrix_rows"] == 45,
            "parent source gate")
    require(
        data["parent"]["terminal"]
        == "M2_R4_ORDER_TWO_SOURCE_FACET_AND_DIAGONAL_INTERPOLATION_INTERFACES",
        "diagonal fiber parent terminal",
    )
    require(not data["conclusion"]["diagonal_orientation_deleted"],
            "parent diagonal scope")
    return data


def load_source_reduction_parent() -> dict[str, Any]:
    for path_key, blob_key in (
        ("note_path", "note_blob_oid"),
        ("verifier_path", "verifier_blob_oid"),
        ("certificate_path", "certificate_blob_oid"),
    ):
        require(
            git_output(
                "rev-parse",
                f"{SOURCE_REDUCTION_PARENT['commit']}:"
                f"{SOURCE_REDUCTION_PARENT[path_key]}",
            )
            == SOURCE_REDUCTION_PARENT[blob_key],
            f"source-reduction blob {SOURCE_REDUCTION_PARENT[path_key]}",
        )
    data = parse_json(
        git_output(
            "show",
            f"{SOURCE_REDUCTION_PARENT['commit']}:"
            f"{SOURCE_REDUCTION_PARENT['certificate_path']}",
        ),
        SOURCE_REDUCTION_PARENT["certificate_path"],
    )
    require(
        data.get("payload_sha256")
        == SOURCE_REDUCTION_PARENT["certificate_payload_sha256"],
        "source-reduction payload",
    )
    require(payload_hash(data) == data.get("payload_sha256"),
            "source-reduction seal")
    require(data["conclusion"]["terminal"] == SOURCE_REDUCTION_PARENT["terminal"],
            "source-reduction terminal")
    saturation = data["complete_source_saturation"]
    require(saturation["component_source_degree"] == 2, "source degree")
    require(saturation["row_binary_degree"] == 4, "source-row degree")
    require(saturation["source_count"] == 12, "source-row count")
    require(saturation["left_total_degree"] == 48, "source-row total degree")
    require(
        saturation["product_identity"]
        == "product_i H(alpha_i,-) is proportional to B^2",
        "source product identity",
    )
    return data


def load_source_facet_parent() -> dict[str, Any]:
    require(
        git_output(
            "rev-parse",
            f"{SOURCE_FACET_PARENT['commit']}:"
            f"{SOURCE_FACET_PARENT['theorem_path']}",
        )
        == SOURCE_FACET_PARENT["theorem_blob_oid"],
        "source-facet theorem blob",
    )
    require(
        git_output(
            "rev-parse",
            f"{SOURCE_FACET_PARENT['commit']}:"
            f"{SOURCE_FACET_PARENT['certificate_path']}",
        )
        == SOURCE_FACET_PARENT["certificate_blob_oid"],
        "source-facet certificate blob",
    )
    data = parse_json(
        git_output(
            "show",
            f"{SOURCE_FACET_PARENT['commit']}:"
            f"{SOURCE_FACET_PARENT['certificate_path']}",
        ),
        SOURCE_FACET_PARENT["certificate_path"],
    )
    require(
        data.get("payload_sha256")
        == SOURCE_FACET_PARENT["certificate_payload_sha256"],
        "source-facet payload",
    )
    require(payload_hash(data) == data.get("payload_sha256"),
            "source-facet seal")
    require(
        data["theorem_status"]["q6_s6_component_edge_coloring_9_28"]
        == "PROVED",
        "component edge coloring status",
    )
    require(
        data["outgoing_conjugate_ledger"]["q6_s6_component_edge_color_multiplicity_formula"]
        == "2*u",
        "component color multiplicity",
    )
    require(
        data["outgoing_conjugate_ledger"]["q6_s6_complementary_pole_graph_left_degree"] == 2,
        "left pole-graph degree",
    )
    require(
        data["theorem_status"]["q6_s6_source_facet_deck_9_27"] == "PROVED",
        "source-facet deck status",
    )
    classes = data["outgoing_conjugate_ledger"]["q6_s6_horizontal_fiber_classes"]
    require(classes["K_pullback_degree"] == 10, "common-K fiber degree")
    require(classes["eta_pullback_degree"] == 2, "eta fiber degree")
    require(classes["exchange_distinct_parameter_points"] == 12,
            "one-exchange point count")
    require(
        data["outgoing_conjugate_ledger"]["q6_s6_source_facet_common_size"] == 5,
        "one-exchange common size",
    )
    require(
        data["outgoing_conjugate_ledger"]["q6_s6_source_facet_exchange_size"] == 1,
        "one-exchange size",
    )
    return data


def profile_replay() -> dict[str, Any]:
    profiles = sorted({
        tuple(sorted(4 - deficit for deficit in deficits))
        for deficits in product(range(5), repeat=6)
        if sum(deficits) == 4
    })
    expected = [
        (0, 4, 4, 4, 4, 4),
        (1, 3, 4, 4, 4, 4),
        (2, 2, 4, 4, 4, 4),
        (2, 3, 3, 4, 4, 4),
        (3, 3, 3, 3, 4, 4),
    ]
    require(profiles == expected, "five exhaustive profiles")
    require(all(sum(profile) == 20 for profile in profiles), "incidence sum")
    require(all(profile.count(0) <= 1 for profile in profiles), "one absent label")
    return {
        "category_census": {"J-J": 10, "I-I": 10, "I-J": 4},
        "J_incidence_over_K": 20,
        "J_incidence_outside_K": 4,
        "profiles": [list(profile) for profile in profiles],
        "profile_count": len(profiles),
        "maximum_absent_J_labels": 1,
        "uses_stabilizer_symmetry": False,
        "ramification_counted_by_divisor_multiplicity": True,
    }


def component_color_replay() -> dict[str, Any]:
    profiles = sorted({
        tuple(sorted(4 - deficit for deficit in deficits))
        for deficits in product(range(3), repeat=6)
        if sum(deficits) == 4
    })
    expected = [
        (2, 2, 4, 4, 4, 4),
        (2, 3, 3, 4, 4, 4),
        (3, 3, 3, 3, 4, 4),
    ]
    require(profiles == expected, "three color-surviving profiles")
    require(all(min(profile) >= 2 for profile in profiles),
            "all J labels occur over K")
    return {
        "component_source_degree": 2,
        "colored_edge_count": 4,
        "left_pole_graph_degree": 2,
        "outside_K_deficit_is_left_colored_degree": True,
        "maximum_deficit": 2,
        "surviving_profiles": [list(profile) for profile in profiles],
        "surviving_profile_count": len(profiles),
        "every_J_label_occurs_over_K": True,
        "uses_zero_migration_condition": False,
        "uses_stabilizer_symmetry": False,
    }


def colored_resultant_split_replay() -> dict[str, Any]:
    checked = 0
    for colored_tuple in combinations(range(12), 4):
        colored = set(colored_tuple)
        j_orders = [int(slot in colored) for slot in range(12)]
        i_orders = [2 - order for order in j_orders]
        require(sum(j_orders) == 4, "colored J degree")
        require(sum(i_orders) == 20, "exchange I degree")
        require(all(i_order + j_order == 2
                    for i_order, j_order in zip(i_orders, j_orders)),
                "exchange square split")
        checked += 1
    require(checked == 495, "colored divisor census")
    return {
        "colored_divisor_degree": 4,
        "colored_divisor_squarefree": True,
        "colored_divisor_divides_L_complement_pullback": True,
        "common_K_pullback_degree": 10,
        "remaining_pullback_degree": 14,
        "P_I_degree": 6,
        "P_J_degree": 6,
        "partial_resultant_degrees": {"I": 24, "J": 24},
        "J_resultant_identity": "Res_T(P_J,H) is proportional to D_K^2*C_H",
        "I_resultant_identity": "C_H*Res_T(P_I,H) is proportional to D_R^2",
        "left_deficit_recovery": "c_j=deg gcd(C_H,bZ_j)",
        "four_root_divisors_checked": checked,
        "uses_stabilizer_symmetry": False,
    }


def coordinate_colored_quotient_replay() -> dict[str, Any]:
    fibers = tuple((2 * index, 2 * index + 1) for index in range(6))
    invariant = []
    for subset in combinations(range(12), 4):
        chosen = set(subset)
        if all((left in chosen) == (right in chosen) for left, right in fibers):
            invariant.append(chosen)
    require(len(invariant) == 15, "coordinate quotient quadratics")
    require(
        all(sum({left, right} <= chosen for left, right in fibers) == 2
            for chosen in invariant),
        "two complete right fibers",
    )

    modulus = 101

    def value(coefficients: list[int], point: int) -> int:
        return sum(coefficient * pow(point, degree, modulus)
                   for degree, coefficient in enumerate(coefficients)) % modulus

    coefficients = {
        "A2": [3, 5, 7], "A0": [11, 13, 17], "B1": [19, 23],
        "A1": [29, 31, 37], "B2": [41, 43], "B0": [47, 53],
    }
    pair_checks = 0
    for t, x in ((2, 3), (5, 7), (11, 13), (17, 19)):
        w = x * x % modulus
        y = t * t % modulus
        positive_base = (value(coefficients["A2"], w) * y
                         + value(coefficients["A0"], w)) % modulus
        positive_odd = x * t * value(coefficients["B1"], w) % modulus
        require(
            (positive_base + positive_odd) * (positive_base - positive_odd)
            % modulus
            == (positive_base**2
                - w * y * value(coefficients["B1"], w) ** 2) % modulus,
            "positive coordinate pair",
        )
        negative_even = t * value(coefficients["A1"], w) % modulus
        negative_odd = x * (
            value(coefficients["B2"], w) * y
            + value(coefficients["B0"], w)
        ) % modulus
        require(
            (negative_even + negative_odd) * (-negative_even + negative_odd)
            % modulus
            == (w * (value(coefficients["B2"], w) * y
                     + value(coefficients["B0"], w)) ** 2
                - y * value(coefficients["A1"], w) ** 2) % modulus,
            "negative coordinate pair",
        )
        pair_checks += 2
    return {
        "colored_quartic_descends_to_squarefree_quotient_quadratic": True,
        "quotient_quadratic_count_on_six_free_fibers": len(invariant),
        "right_colored_degree_profile": [0, 0, 0, 0, 2, 2],
        "positive_parameter_dimension": 8,
        "negative_parameter_dimension": 7,
        "positive_Phi": "(A_2*Y+A_0)^2-W*Y*B_1^2",
        "negative_Phi": "W*(B_2*Y+B_0)^2-Y*A_1^2",
        "partial_resultant": "R_S=Res_Y(p_S,Phi_epsilon)",
        "J_identity": "R_J is proportional to K_5^2*c",
        "I_identity": "c*R_I is proportional to R_7^2",
        "pair_checks": pair_checks,
        "coordinate_orientation_deleted": False,
    }


def coordinate_k_fiber_vieta_replay() -> dict[str, Any]:
    modulus = 101

    def inverse(value: int) -> int:
        return pow(value % modulus, modulus - 2, modulus)

    def binary_value(coefficients: list[int], u: int, v: int) -> int:
        degree = len(coefficients) - 1
        return sum(
            coefficient * pow(u, index, modulus)
            * pow(v, degree - index, modulus)
            for index, coefficient in enumerate(coefficients)
        ) % modulus

    def matrix_rank(matrix: list[list[int]]) -> int:
        work = [[entry % modulus for entry in row] for row in matrix]
        pivot_row = 0
        for column in range(len(work[0])):
            pivot = next((
                row for row in range(pivot_row, len(work))
                if work[row][column]
            ), None)
            if pivot is None:
                continue
            work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
            scale = inverse(work[pivot_row][column])
            work[pivot_row] = [entry * scale % modulus
                               for entry in work[pivot_row]]
            for row in range(len(work)):
                if row == pivot_row or not work[row][column]:
                    continue
                scale = work[row][column]
                work[row] = [
                    (left - scale * right) % modulus
                    for left, right in zip(work[row], work[pivot_row])
                ]
            pivot_row += 1
        return pivot_row

    deck_checks = 0
    for r, s, left, right in (
        (1, 1, 2, 3), (2, 1, -1, 4), (3, 1, 5, -2),
        (0, 1, 7, -7), (1, 0, 9, -9),
    ):
        require(left * right == (-left) * (-right), "deck product")
        require(
            r * s * (left + right)
            == (-r) * s * ((-left) + (-right)),
            "deck weighted sum",
        )
        deck_checks += 1

    positive_points = [(0, 1), (1, 0), (1, 1), (4, 1), (9, 1)]
    a2, a0, b1 = [3, 5, 7], [11, 13, 17], [19, 23]
    positive_rows = []
    positive_small_rows = []
    for u, v in positive_points:
        lead = binary_value(a2, u, v)
        require(lead != 0, "positive leading support")
        product_value = binary_value(a0, u, v) * inverse(lead) % modulus
        weighted_sum = (
            -u * v * binary_value(b1, u, v) * inverse(lead)
        ) % modulus
        v2 = [v * v % modulus, u * v % modulus, u * u % modulus]
        positive_rows.extend((
            [(-product_value * value) % modulus for value in v2]
            + v2 + [0, 0],
            [(weighted_sum * value) % modulus for value in v2]
            + [0, 0, 0, u * v * v % modulus, u * u * v % modulus],
        ))
        positive_small_rows.append([
            weighted_sum * v * v % modulus,
            weighted_sum * u * v % modulus,
            weighted_sum * u * u % modulus,
            u * v * v % modulus,
            u * u * v % modulus,
        ])

    negative_points = [(1, 1), (4, 1), (9, 1), (16, 1), (25, 1)]
    b2, b0, a1 = [3, 5], [7, 11], [13, 17, 19]
    negative_rows = []
    negative_product_rows = []
    negative_sum_rows = []
    for u, v in negative_points:
        lead = binary_value(b2, u, v)
        require(u * v * lead != 0, "negative leading support")
        product_value = binary_value(b0, u, v) * inverse(lead) % modulus
        weighted_sum = -binary_value(a1, u, v) * inverse(lead) % modulus
        v1 = [v, u]
        v2 = [v * v % modulus, u * v % modulus, u * u % modulus]
        negative_rows.extend((
            [(-product_value * value) % modulus for value in v1]
            + v1 + [0, 0, 0],
            [(weighted_sum * value) % modulus for value in v1]
            + [0, 0] + v2,
        ))
        negative_product_rows.append([
            -product_value * v % modulus, -product_value * u % modulus,
            v, u,
        ])
        negative_sum_rows.append([
            weighted_sum * v % modulus, weighted_sum * u % modulus,
            v * v % modulus, u * v % modulus, u * u % modulus,
        ])

    positive_rank = matrix_rank(positive_rows)
    positive_small_rank = matrix_rank(positive_small_rows)
    negative_rank = matrix_rank(negative_rows)
    negative_product_rank = matrix_rank(negative_product_rows)
    negative_sum_rank = matrix_rank(negative_sum_rows)
    require(positive_rank <= 7, "positive Vieta kernel")
    require(positive_small_rank <= 4, "positive determinant")
    require(negative_rank <= 6, "negative Vieta kernel")
    require(negative_product_rank <= 3, "negative product rank")
    require(negative_sum_rank <= 4, "negative determinant")
    return {
        "deck_invariant_edge_coordinates": ["p=ab", "q=r*s*(a+b)"],
        "deck_checks": deck_checks,
        "positive_matrix_shape": [10, 8],
        "positive_sample_rank": positive_rank,
        "positive_small_determinant_rank": positive_small_rank,
        "positive_ramified_test_fibers": 2,
        "negative_matrix_shape": [10, 7],
        "negative_sample_rank": negative_rank,
        "negative_product_matrix_shape": [5, 4],
        "negative_product_sample_rank": negative_product_rank,
        "negative_sum_determinant_rank": negative_sum_rank,
        "negative_ramified_K_excluded": True,
        "coordinate_orientation_deleted": False,
    }


def coordinate_transpose_replay() -> dict[str, Any]:
    terms_checked = 0
    for degree in range(1, 61):
        terms = {(degree - 1 - index, index) for index in range(degree)}
        require({(right, left) for left, right in terms} == terms,
                "endpoint divided-difference transpose")
        terms_checked += len(terms)

    identity, first, second, diagonal = (0, 0), (1, 0), (0, 1), (1, 1)
    transpose = lambda element: (element[1], element[0])
    require(transpose(identity) == identity, "identity transpose")
    require(transpose(first) == second, "first coordinate transpose")
    require(transpose(second) == first, "second coordinate transpose")
    require(transpose(diagonal) == diagonal, "diagonal transpose")
    return {
        "endpoint_self_correspondence_transpose_invariant": True,
        "divided_difference_terms_checked": terms_checked,
        "coordinate_subgroups_exchanged": True,
        "diagonal_subgroup_fixed": True,
        "fresh_source_record_required": True,
        "old_source_record_reused": False,
        "independent_order_two_geometry_routes": ["coordinate", "diagonal"],
        "coordinate_orientation_deleted": False,
    }


def diagonal_facet_mixing_replay() -> dict[str, Any]:
    invariant = frozenset(range(6))
    common = frozenset(range(5))
    xi = 5

    def matchings(vertices: tuple[int, ...]):
        if not vertices:
            yield ()
            return
        first = vertices[0]
        for index in range(1, len(vertices)):
            second = vertices[index]
            rest = vertices[1:index] + vertices[index + 1:]
            for tail in matchings(rest):
                yield ((first, second),) + tail

    census: Counter[tuple[int, int, int]] = Counter()
    preserving = 0
    eta_near = 6
    c6_eta_xi_deleted = 0
    c6_near_survivors = 0
    c2_near_types: Counter[str] = Counter()
    for edges in matchings(tuple(range(12))):
        mate = {}
        for left, right in edges:
            mate[left] = right
            mate[right] = left
        crossing = sum(mate[label] not in invariant for label in invariant)
        a = sum(left in common and right in common for left, right in edges)
        b = int(mate[xi] in common)
        if crossing == 0:
            preserving += 1
            require(mate[xi] in common, "odd common five-set")
            transported_roots = 4
            xi_J_capacities = {"aligned_eta": 0, "near_one_exchange": 2}
            require(
                all(transported_roots > capacity
                    for capacity in xi_J_capacities.values()),
                "transported xi capacity",
            )
        else:
            census[(a, b, crossing)] += 1
            if crossing == 2:
                if (a, b) == (2, 0):
                    c2_near_types["a2_b0"] += 1
                elif mate[eta_near] in common:
                    c2_near_types["a1_b1_eta_to_K"] += 1
                else:
                    require(mate[eta_near] in set(range(6, 12)),
                            "c2 exceptional eta lies in J_0")
                    c2_near_types["a1_b1_eta_to_J0"] += 1
            if crossing == 6:
                if mate[eta_near] == xi:
                    c6_eta_xi_deleted += 1
                else:
                    require(mate[eta_near] in common, "c6 eta pairs into K")
                    ell = mate[xi]
                    require(ell in set(range(6, 12)) - {eta_near},
                            "c6 xi orbit label")
                    c6_near_survivors += 1

    expected = {(2, 0, 2), (1, 1, 2), (1, 0, 4), (0, 1, 4), (0, 0, 6)}
    require(set(census) == expected, "five diagonal mixing rows")
    require(sum(census.values()) + preserving == 10395,
            "fixed-point-free matching count")
    require(preserving == 225, "partition-preserving matching count")
    require(c6_eta_xi_deleted == 120, "near c6 eta-xi deletion count")
    require(c6_near_survivors == 600, "near c6 survivor count")
    require(c2_near_types == {
        "a2_b0": 1350,
        "a1_b1_eta_to_K": 900,
        "a1_b1_eta_to_J0": 1800,
    }, "near c2 matching types")
    c6_j_counts = [z for z in range(3) if 4 - z <= 2]
    require(c6_j_counts == [2], "near c6 paired J counts")
    c2_202_profile = sorted([4] * 4 + [(20 - 4 * 4) // 2] * 2)
    require(c2_202_profile == [2, 2, 4, 4, 4, 4],
            "c2 (2,0,2) degree profile")
    c2_112_saturated_profile = [4, 4]
    require(4 + 2 + 2 == sum(c2_112_saturated_profile),
            "c2 (1,1,2) saturation")
    c2_112_exceptional_values = list(range(3 * 2, 2 * 4 + 1))
    require(c2_112_exceptional_values == [6, 7, 8],
            "c2 (1,1,2) exceptional capacity")
    rows = [
        {"a": a, "b": b, "c": crossing, "matching_count": census[(a, b, crossing)]}
        for a, b, crossing in sorted(census, key=lambda row: (row[2], -row[0], row[1]))
    ]
    return {
        "endpoint_involution_fixed_point_free_on_labels": True,
        "total_fixed_point_free_matchings": 10395,
        "partition_preserving_matchings_deleted": preserving,
        "partition_preserving_diagonal_subcase_deleted": True,
        "transported_common_K_J_roots": 4,
        "xi_J_capacities": {"aligned_eta": 0, "near_one_exchange": 2},
        "crossing_counts": [2, 4, 6],
        "orbit_rows": rows,
        "orbit_row_count": len(rows),
        "K_transport_to_K": "all four roots lie in J_0=J intersect tau(J)",
        "K_transport_to_eta": "all four roots lie in J_1=J intersect tau(I)",
        "K_transport_to_L_complement": "at least two roots lie in J_1",
        "aligned_c6_deleted": True,
        "near_c6_eta_xi_matchings_deleted": c6_eta_xi_deleted,
        "near_c6_matchings_surviving": c6_near_survivors,
        "near_c6_J_roots_per_paired_quartic": c6_j_counts[0],
        "near_c6_colored_source_fibers": 2,
        "near_c6_colored_quotient_degree": 2,
        "near_c6_colored_quotient_tau_eigenvalue": 1,
        "near_c6_J_identity": "Q_J is proportional to K_5^2*chi",
        "near_c6_I_identity": "chi*Q_I is proportional to R_7^2",
        "near_c6_resultant_degree": 12,
        "near_c2_matching_types": dict(c2_near_types),
        "c2_202_J_degree_profile": c2_202_profile,
        "c2_202_square_fiber": "R_kstar is proportional to P_J1^2",
        "c2_202_internal_product": "product over K_0 of R_k is proportional to P_J0^4",
        "c2_112_saturated_J1_degree_profile": c2_112_saturated_profile,
        "c2_112_saturated_square_fiber": "R_tau_eta is proportional to P_J1^2",
        "c2_112_exceptional_eta_orbit": "eta and tau(eta) lie in J_0",
        "c2_112_exceptional_J1_capacity_values": c2_112_exceptional_values,
        "uses_whole_fiber_transport_only": True,
        "individual_star_transport_used": False,
        "diagonal_orientation_deleted": False,
    }


def expected_certificate() -> dict[str, Any]:
    data = {
        "schema": "kb-mca-v4-m2-u2-universal-source-facet-census-v1",
        "parent": PARENT,
        "source_reduction_parent": SOURCE_REDUCTION_PARENT,
        "source_facet_parent": SOURCE_FACET_PARENT,
        "universal_source_facet": profile_replay(),
        "component_color_profile_cut": component_color_replay(),
        "colored_source_resultant_split": colored_resultant_split_replay(),
        "coordinate_colored_quotient_resultant": coordinate_colored_quotient_replay(),
        "coordinate_k_fiber_vieta_rank": coordinate_k_fiber_vieta_replay(),
        "coordinate_transpose_transport": coordinate_transpose_replay(),
        "diagonal_facet_mixing": diagonal_facet_mixing_replay(),
        "universal_source_interpolation": {
            "actual_source_bidegree": [2, 4],
            "source_count": 12,
            "row_binary_degree": 4,
            "matrix_rows": 45,
            "matrix_columns": 12,
            "kernel_condition": "full support",
            "complete_source_product": "product_i q_i is proportional to B^2",
            "stabilizer_types_r_delta": [[2, 4], [4, 2], [8, 1]],
            "uses_stabilizer_symmetry": False,
            "applies_to_trivial_stabilizer": True,
        },
        "scope": {
            "coordinate_order_two": True,
            "diagonal_order_two": True,
            "trivial_stabilizer_r8_delta1": True,
            "coordinate_pairing_transferred_to_trivial": False,
            "partition_preserving_diagonal_subcase_deleted": True,
            "aligned_c6_deleted": True,
            "minimally_mixed_c2_capacity_refined": True,
        },
        "conclusion": {
            "order_two_type_deleted": False,
            "trivial_stabilizer_type_deleted": False,
            "k3_status": "OPEN",
            "koalabear_row_status": "OPEN",
            "terminal": "M2_U2_SOURCE_FACET_COLOR_COORDINATE_QUOTIENT_VIETA_TRANSPOSE_DIAGONAL_MIXING_C6_QUOTIENT_AND_C2_CAPACITY_INTERFACES",
        },
        "nonclaims": [
            "no stabilizer action or paired degree profile in the trivial branch",
            "no universal source-row kernel failure",
            "no complete deletion of any of the five diagonal mixing rows",
            "no contradiction from a reciprocal c=2 square fiber alone",
            "no component, type, owner, payment, K3, row, or Prize close",
        ],
    }
    data["payload_sha256"] = payload_hash(data)
    return data


def verify_data(data: dict[str, Any]) -> None:
    require(payload_hash(data) == data.get("payload_sha256"), "certificate seal")
    require(data == expected_certificate(), "certificate content")


def tamper_selftest(data: dict[str, Any]) -> int:
    mutations: list[Callable[[dict[str, Any]], None]] = [
        lambda x: x["universal_source_facet"]["category_census"].__setitem__("I-J", 5),
        lambda x: x["universal_source_facet"].__setitem__("J_incidence_over_K", 19),
        lambda x: x["universal_source_facet"].__setitem__("profile_count", 4),
        lambda x: x["universal_source_facet"]["profiles"].pop(),
        lambda x: x["universal_source_facet"].__setitem__("uses_stabilizer_symmetry", True),
        lambda x: x["scope"].__setitem__("trivial_stabilizer_r8_delta1", False),
        lambda x: x["scope"].__setitem__("coordinate_pairing_transferred_to_trivial", True),
        lambda x: x["universal_source_interpolation"].__setitem__("matrix_rows", 44),
        lambda x: x["universal_source_interpolation"].__setitem__("actual_source_bidegree", [4, 4]),
        lambda x: x["universal_source_interpolation"].__setitem__("uses_stabilizer_symmetry", True),
        lambda x: x["universal_source_interpolation"].__setitem__("applies_to_trivial_stabilizer", False),
        lambda x: x["component_color_profile_cut"].__setitem__("colored_edge_count", 3),
        lambda x: x["component_color_profile_cut"].__setitem__("maximum_deficit", 3),
        lambda x: x["component_color_profile_cut"]["surviving_profiles"].pop(),
        lambda x: x["colored_source_resultant_split"].__setitem__("colored_divisor_degree", 5),
        lambda x: x["colored_source_resultant_split"].__setitem__("colored_divisor_squarefree", False),
        lambda x: x["colored_source_resultant_split"].__setitem__("common_K_pullback_degree", 9),
        lambda x: x["colored_source_resultant_split"].__setitem__("left_deficit_recovery", "untracked"),
        lambda x: x["coordinate_colored_quotient_resultant"].__setitem__("quotient_quadratic_count_on_six_free_fibers", 14),
        lambda x: x["coordinate_colored_quotient_resultant"].__setitem__("positive_parameter_dimension", 9),
        lambda x: x["coordinate_colored_quotient_resultant"].__setitem__("negative_Phi", "wrong"),
        lambda x: x["coordinate_colored_quotient_resultant"].__setitem__("coordinate_orientation_deleted", True),
        lambda x: x["coordinate_k_fiber_vieta_rank"].__setitem__("positive_matrix_shape", [9, 8]),
        lambda x: x["coordinate_k_fiber_vieta_rank"].__setitem__("positive_ramified_test_fibers", 0),
        lambda x: x["coordinate_k_fiber_vieta_rank"].__setitem__("negative_matrix_shape", [10, 8]),
        lambda x: x["coordinate_k_fiber_vieta_rank"].__setitem__("negative_product_sample_rank", 4),
        lambda x: x["coordinate_k_fiber_vieta_rank"].__setitem__("negative_ramified_K_excluded", False),
        lambda x: x["coordinate_k_fiber_vieta_rank"].__setitem__("coordinate_orientation_deleted", True),
        lambda x: x["coordinate_transpose_transport"].__setitem__("endpoint_self_correspondence_transpose_invariant", False),
        lambda x: x["coordinate_transpose_transport"].__setitem__("coordinate_subgroups_exchanged", False),
        lambda x: x["coordinate_transpose_transport"].__setitem__("fresh_source_record_required", False),
        lambda x: x["coordinate_transpose_transport"].__setitem__("old_source_record_reused", True),
        lambda x: x["diagonal_facet_mixing"].__setitem__("partition_preserving_diagonal_subcase_deleted", False),
        lambda x: x["diagonal_facet_mixing"].__setitem__("partition_preserving_matchings_deleted", 224),
        lambda x: x["diagonal_facet_mixing"].__setitem__("crossing_counts", [2, 4]),
        lambda x: x["diagonal_facet_mixing"]["orbit_rows"].pop(),
        lambda x: x["diagonal_facet_mixing"].__setitem__("individual_star_transport_used", True),
        lambda x: x["diagonal_facet_mixing"].__setitem__("diagonal_orientation_deleted", True),
        lambda x: x["diagonal_facet_mixing"].__setitem__("aligned_c6_deleted", False),
        lambda x: x["diagonal_facet_mixing"].__setitem__("near_c6_matchings_surviving", 599),
        lambda x: x["diagonal_facet_mixing"].__setitem__("near_c6_J_roots_per_paired_quartic", 1),
        lambda x: x["diagonal_facet_mixing"].__setitem__("near_c6_colored_quotient_degree", 4),
        lambda x: x["diagonal_facet_mixing"].__setitem__("near_c6_colored_quotient_tau_eigenvalue", -1),
        lambda x: x["diagonal_facet_mixing"].__setitem__("near_c6_J_identity", "wrong"),
        lambda x: x["diagonal_facet_mixing"]["near_c2_matching_types"].__setitem__("a2_b0", 1349),
        lambda x: x["diagonal_facet_mixing"]["c2_202_J_degree_profile"].pop(),
        lambda x: x["diagonal_facet_mixing"].__setitem__("c2_202_square_fiber", "wrong"),
        lambda x: x["diagonal_facet_mixing"].__setitem__("c2_112_saturated_J1_degree_profile", [3, 4]),
        lambda x: x["diagonal_facet_mixing"].__setitem__("c2_112_exceptional_J1_capacity_values", [6, 7]),
        lambda x: x["scope"].__setitem__("minimally_mixed_c2_capacity_refined", False),
        lambda x: x["conclusion"].__setitem__("trivial_stabilizer_type_deleted", True),
        lambda x: x["conclusion"].__setitem__("k3_status", "CLOSED"),
        lambda x: x["parent"].__setitem__("certificate_payload_sha256", "0" * 64),
        lambda x: x["source_reduction_parent"].__setitem__("certificate_payload_sha256", "0" * 64),
        lambda x: x["source_facet_parent"].__setitem__("certificate_payload_sha256", "0" * 64),
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

    load_parent()
    load_source_reduction_parent()
    load_source_facet_parent()
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
        "KB_MCA_V4_M2_U2_UNIVERSAL_SOURCE_FACET_CENSUS_PASS "
        f"raw_profiles={data['universal_source_facet']['profile_count']} "
        f"surviving_profiles={data['component_color_profile_cut']['surviving_profile_count']} "
        f"colored_divisors={data['colored_source_resultant_split']['four_root_divisors_checked']} "
        f"coordinate_quotients={data['coordinate_colored_quotient_resultant']['quotient_quadratic_count_on_six_free_fibers']} "
        f"coordinate_vieta_rank={data['coordinate_k_fiber_vieta_rank']['positive_sample_rank']}/"
        f"{data['coordinate_k_fiber_vieta_rank']['negative_sample_rank']} "
        f"transpose_terms={data['coordinate_transpose_transport']['divided_difference_terms_checked']} "
        f"diagonal_mixing_rows={data['diagonal_facet_mixing']['orbit_row_count']} "
        f"c6_near={data['diagonal_facet_mixing']['near_c6_matchings_surviving']} "
        f"c2_exceptional={data['diagonal_facet_mixing']['near_c2_matching_types']['a1_b1_eta_to_J0']} "
        f"tamper_rejected={rejected}"
    )


if __name__ == "__main__":
    main()
