#!/usr/bin/env python3
"""Verify the degree-60 decomposition source-fiber adapter.

This verifier certifies the exact integer profile compiler, source/active
accounting, binary source-pencil interface, challenge-field descent,
degree-five deletion, degree-thirty refinement, the canonical degree-twelve
pencil, the conditional carrier gate, source-object bindings, replay hashes,
and mutation resistance.  It does not replace the homogeneous divisor proofs
or the inherited actual-component theorem.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import subprocess
from pathlib import Path
from typing import Any, Callable


if not __debug__:
    raise RuntimeError("verifier refuses optimized Python execution")


class VerificationError(RuntimeError):
    """Raised when a certificate condition fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
CERTIFICATE = (
    ROOT
    / "data"
    / "certificates"
    / "kb-mca-v4-degree60-decomposition-source-fiber-adapter-v1"
    / "kb_mca_v4_degree60_decomposition_source_fiber_adapter_v1.json"
)
PARENT_CERTIFICATE = (
    ROOT
    / "data"
    / "certificates"
    / "kb-mca-v4-degree60-primitive-subdegree4-route-cut-v1"
    / "kb_mca_v4_degree60_primitive_subdegree4_route_cut_v1.json"
)

ENDPOINT_DEGREE = 60
POLE_ORDER = 5
ACTIVE_POINTS = 60
SOURCE_POINTS = 12
P = 2_130_706_433
Q = P**6
DOMAIN_SIZE = 1 << 21
EXPECTED_PARENT_HEAD = "59c4449ca0f5cee929dd39fc7b5ae8b0a33877f4"
EXPECTED_PARENT_PATH = (
    "experimental/data/certificates/"
    "kb-mca-v4-degree60-primitive-subdegree4-route-cut-v1/"
    "kb_mca_v4_degree60_primitive_subdegree4_route_cut_v1.json"
)
EXPECTED_PARENT_BLOB = "7e8a79db97dc56125f25d9a190c3b0c3adca158a"
EXPECTED_PARENT_PAYLOAD = (
    "21a8ca7800745c2c94876d48473801e84f4d9c8f9e6ce5b53e8b8bd66b699962"
)
EXPECTED_IMPORTED_TERMINAL = (
    "ROUTED_TO_GEOMETRIC_FUNCTIONAL_DECOMPOSITION_ADAPTER"
)
STATUS = (
    "PROVED_SOURCE_FIBER_ADAPTER_DEGREE5_DELETION_"
    "DEGREE30_REFINEMENT_ROW_OPEN"
)
EXPECTED_NONCLAIMS = [
    (
        "no identification of the endpoint parameter line with the "
        "evaluation carrier domain"
    ),
    "no full-domain fold proved for inner degree 2",
    "no full-domain fold proved for inner degree 4",
    "no actual-producer deletion for inner degrees 3,6,10,12",
    (
        "no deletion of the inner-degree-30 producer beyond its exact "
        "refinement to inner degree 6"
    ),
    "no received-data descent",
    "no explaining-polynomial descent",
    "no slope-projection descent",
    "no chronology-valid quotient payment",
    "no u=2 closure",
    "no u=3 theorem",
    "no cap-68 theorem",
    "no ledger movement",
    "no KoalaBear row closure",
]


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def payload_hash(value: dict[str, Any]) -> str:
    unhashed = dict(value)
    unhashed.pop("payload_sha256", None)
    return hashlib.sha256(canonical_json(unhashed).encode()).hexdigest()


def reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise VerificationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=reject_duplicate_pairs,
    )


def git_output(*arguments: str) -> str:
    try:
        result = subprocess.run(
            ["git", *arguments],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        raise VerificationError(
            "git object binding failed: " + " ".join(arguments)
        ) from error
    return result.stdout.strip()


def is_prime_trial(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def proper_divisors(value: int) -> list[int]:
    return [
        candidate
        for candidate in range(2, value)
        if value % candidate == 0
    ]


def terminal(inner_degree: int, full_domain_divides: bool) -> str:
    if inner_degree == 5:
        return (
            "DELETED_CHALLENGE_FIELD_FIFTH_POWER_"
            "FIBER_CONTRADICTION"
        )
    if inner_degree == 30:
        return "ROUTED_TO_INNER_DEGREE_6_BY_FIFTH_POWER_EXTRACTION"
    if inner_degree == 12:
        return (
            "CANONICAL_PENCIL_MEMBERSHIP_TEST_OPEN_"
            "SAME_DEGREE_CARRIER_FOLD_INCOMPATIBLE"
        )
    if full_domain_divides:
        return (
            "CONDITIONAL_CARRIER_CARDINALITY_COMPATIBLE_"
            "PARAMETER_TO_CARRIER_BRIDGE_OPEN"
        )
    return (
        f"SAME_DEGREE_CARRIER_FOLD_{inner_degree}_"
        "CARDINALITY_INCOMPATIBLE_BRIDGE_OR_DELETION_OPEN"
    )


def derived_profiles() -> tuple[list[dict[str, Any]], list[int]]:
    profiles: list[dict[str, Any]] = []
    rejected_degrees: set[int] = set()
    for inner_degree in proper_divisors(ENDPOINT_DEGREE):
        outer_degree = ENDPOINT_DEGREE // inner_degree
        admitted_for_degree = False
        for simple_outer_poles in range(outer_degree + 1):
            remaining_pole_degree = outer_degree - simple_outer_poles
            if remaining_pole_degree % POLE_ORDER:
                continue
            order_five_outer_poles = remaining_pole_degree // POLE_ORDER
            if simple_outer_poles and inner_degree % POLE_ORDER:
                continue
            forced_ramification = (
                simple_outer_poles
                * (POLE_ORDER - 1)
                * inner_degree
                // POLE_ORDER
            )
            rh_budget = 2 * inner_degree - 2
            if forced_ramification > rh_budget:
                continue
            admitted_for_degree = True
            complete_source_points = (
                order_five_outer_poles * inner_degree
            )
            exceptional_source_points = (
                simple_outer_poles * inner_degree // POLE_ORDER
            )
            source_partition_count = math.factorial(SOURCE_POINTS) // (
                math.factorial(inner_degree)
                ** order_five_outer_poles
                * math.factorial(order_five_outer_poles)
                * (
                    math.factorial(inner_degree // POLE_ORDER)
                    ** simple_outer_poles
                )
                * math.factorial(simple_outer_poles)
            )
            divides = DOMAIN_SIZE % inner_degree == 0
            profiles.append(
                {
                    "inner_degree": inner_degree,
                    "outer_degree": outer_degree,
                    "order_five_outer_poles": order_five_outer_poles,
                    "simple_outer_poles": simple_outer_poles,
                    "active_fibers": outer_degree,
                    "active_points": outer_degree * inner_degree,
                    "complete_source_fibers": order_five_outer_poles,
                    "complete_source_points": complete_source_points,
                    "exceptional_source_fibers": simple_outer_poles,
                    "exceptional_source_points": exceptional_source_points,
                    "forced_ramification": forced_ramification,
                    "riemann_hurwitz_budget": rh_budget,
                    "riemann_hurwitz_slack": (
                        rh_budget - forced_ramification
                    ),
                    "divides_full_domain_cardinality": divides,
                    "source_partition_count": source_partition_count,
                    "terminal": terminal(inner_degree, divides),
                }
            )
        if not admitted_for_degree:
            rejected_degrees.add(inner_degree)
    return profiles, sorted(rejected_degrees)


EXPECTED_DIVISOR_ADAPTER = {
    "homogeneous_no_cancellation": True,
    "active_outer_zeros_simple": True,
    "active_inner_ramification_indices": [1],
    "active_fiber_count_formula": "n=60/m",
    "active_fiber_size_formula": "m",
    "active_factorization": (
        "V_act is proportional to product_n Z_nu(H0,H1), with squarefree "
        "pairwise-coprime degree-m factors"
    ),
    "outer_pole_orders": [1, 5],
    "order_five_outer_pole_inner_ramification_indices": [1],
    "order_five_outer_pole_source_fiber_size_formula": "m",
    "simple_outer_pole_inner_ramification_indices": [5],
    "simple_outer_pole_source_fiber_size_formula": "m/5",
    "source_factorization": (
        "A is proportional to product_a L_i(H0,H1) times product_b R_j, "
        "where M_j(H0,H1)=c_j R_j^5"
    ),
    "outer_pole_degree_equation": "5a+b=n",
    "forced_ramification_formula": "4bm/5",
    "riemann_hurwitz_budget_formula": "2m-2",
    "source_point_count_formula": "am+b(m/5)=12",
    "locator_level_only": True,
    "received_data_descent_proved": False,
    "explaining_polynomial_descent_proved": False,
    "slope_projection_descent_proved": False,
}

EXPECTED_BINDINGS = [
    {
        "binding_id": "KB_DECOMPOSITION_ADAPTER::source_geometry",
        "commit": "44542e91e459364a521870ed2ebde7f6fe5055bf",
        "path": (
            "experimental/notes/frontier-adjacent/"
            "kb_mca_v4_equality_wall_geometry_v1/proof/"
            "pole_disjoint_conic_facet_collinearity_reduction.md"
        ),
        "blob_oid": "356ff4b47d0bb429d11ea10382762a6e95b5ce24",
        "role": (
            "degree-60 endpoint parameter line, K-rational active/source "
            "locators, and actual component descent"
        ),
    },
    {
        "binding_id": "KB_DECOMPOSITION_ADAPTER::foundation_domain",
        "commit": EXPECTED_PARENT_HEAD,
        "path": "tex/cs25_cap_v13_2.tex",
        "blob_oid": "5ceff5dbc4b1ac4cef53eae7eada32046e4bafeb",
        "role": "deployed p, D subgroup of F_p^x, and |D|=2^21",
    },
    {
        "binding_id": "KB_DECOMPOSITION_ADAPTER::active_v4_owner",
        "commit": EXPECTED_PARENT_HEAD,
        "path": "experimental/grande_finale.tex",
        "blob_oid": "6b21d6ea937a8a9f85fc7ade6032d73efd4c7222",
        "role": "complete-fiber owner and quotient-remainder semantic contract",
    },
    {
        "binding_id": "KB_DECOMPOSITION_ADAPTER::workboard",
        "commit": EXPECTED_PARENT_HEAD,
        "path": "agents.md",
        "blob_oid": "b0411aaa46462e38a77bf6146171d683813dbd76",
        "role": "K3 source-bound decomposition adapter target",
    },
]


def check_statement(statement: dict[str, Any]) -> None:
    expected = {
        "row": "KoalaBear MCA at 2^-128",
        "agreement": 1_116_048,
        "B_star": "274980728111395087",
        "object": "MCA",
        "deployed_prime": P,
        "challenge_field": "F_{p^6}",
        "challenge_field_cardinality": str(Q),
        "deployed_domain_cardinality": DOMAIN_SIZE,
        "deployed_domain_structure": (
            "order-2^21 multiplicative subgroup of F_p^x"
        ),
        "endpoint_degree": ENDPOINT_DEGREE,
        "active_root_count": ACTIVE_POINTS,
        "active_roots_squarefree": True,
        "active_roots_are_challenge_field_parameter_values": True,
        "source_root_count": SOURCE_POINTS,
        "source_roots_are_challenge_field_parameter_values": True,
        "source_pole_order": POLE_ORDER,
        "active_source_disjoint": True,
        "endpoint_parameter_line_identified_with_carrier_domain": False,
        "decomposition_scope": (
            "every geometric decomposition f=F composed with h forced by "
            "the residual actual Q=6,s=6,u=2 component theorem"
        ),
    }
    require(statement == expected, "statement")


def check_parent(parent: dict[str, Any]) -> None:
    require(
        set(parent)
        == {
            "head_commit",
            "certificate_path",
            "certificate_blob_oid",
            "certificate_payload_sha256",
            "imported_terminal",
        },
        "parent schema",
    )
    require(parent["head_commit"] == EXPECTED_PARENT_HEAD, "parent head")
    require(
        parent["certificate_path"] == EXPECTED_PARENT_PATH,
        "parent certificate path",
    )
    require(
        parent["certificate_blob_oid"] == EXPECTED_PARENT_BLOB,
        "parent certificate blob",
    )
    require(
        parent["certificate_payload_sha256"] == EXPECTED_PARENT_PAYLOAD,
        "parent payload",
    )
    require(
        parent["imported_terminal"] == EXPECTED_IMPORTED_TERMINAL,
        "parent terminal",
    )
    require(
        git_output("cat-file", "-t", parent["head_commit"]) == "commit",
        "parent commit object",
    )
    require(
        git_output(
            "rev-parse",
            parent["head_commit"] + ":" + parent["certificate_path"],
        )
        == parent["certificate_blob_oid"],
        "parent head/path/blob",
    )
    parent_data = load_json(PARENT_CERTIFICATE)
    require(
        parent_data["payload_sha256"] == payload_hash(parent_data),
        "parent canonical payload",
    )
    require(
        parent_data["payload_sha256"]
        == parent["certificate_payload_sha256"],
        "parent local payload binding",
    )
    require(
        parent_data["conclusion"]["terminal"] == parent["imported_terminal"],
        "parent imported terminal replay",
    )


def check_profiles(data: dict[str, Any]) -> None:
    profiles, excluded = derived_profiles()
    require(data["profiles"] == profiles, "profile compiler")
    require(
        [row["inner_degree"] for row in profiles]
        == [2, 3, 4, 5, 6, 10, 12, 30],
        "profile degree list",
    )
    require(
        [row["source_partition_count"] for row in profiles]
        == [10395, 15400, 5775, 8316, 462, 66, 1, 462],
        "source partition counts",
    )
    require(excluded == [15, 20], "derived excluded degrees")
    require(
        data["excluded_profile_degrees"] == excluded,
        "certificate excluded degrees",
    )
    for row in profiles:
        require(
            5 * row["order_five_outer_poles"]
            + row["simple_outer_poles"]
            == row["outer_degree"],
            "outer pole degree",
        )
        require(row["active_points"] == ACTIVE_POINTS, "active accounting")
        require(
            row["complete_source_points"]
            + row["exceptional_source_points"]
            == SOURCE_POINTS,
            "source accounting",
        )
        require(
            row["forced_ramification"] + row["riemann_hurwitz_slack"]
            == row["riemann_hurwitz_budget"],
            "RH accounting",
        )


def check_conditional_carrier(domain: dict[str, Any]) -> None:
    expected = {
        "endpoint_variable": "challenge-field parameter T",
        "carrier_variable": "evaluation coordinate X",
        "endpoint_parameter_line_identified_with_carrier_domain": False,
        "same_record_parameter_to_carrier_bridge_proved": False,
        "carrier_domain_cardinality": DOMAIN_SIZE,
        "carrier_domain_prime_factorization": "2^21",
        "conditional_statement": (
            "if h is transported to a same-degree complete m-fold map on "
            "D, then m divides |D|"
        ),
        "same_degree_cardinality_compatible_inner_degrees": [2, 4],
        "same_degree_cardinality_incompatible_inner_degrees": [
            3, 5, 6, 10, 12, 30
        ],
        "actual_producer_deletion_implied": False,
        "carrier_owner_implied": False,
        "open_semantic_gates": [
            "parameter_to_carrier_same_record_transport",
            "declared_polynomial_or_retained_fold_form",
            "complete_fibers_on_the_entire_evaluation_domain",
            "received_data_descent",
            "explaining_polynomial_descent",
            "slope_projection_descent",
            "chronology_valid_same_record_owner",
        ],
    }
    require(domain == expected, "conditional carrier compatibility")
    profiles, _ = derived_profiles()
    require(
        [
            row["inner_degree"]
            for row in profiles
            if row["divides_full_domain_cardinality"]
        ]
        == [2, 4],
        "conditional carrier divisibility",
    )


def check_degree_five(gate: dict[str, Any]) -> None:
    expected = {
        "profile_inner_degree": 5,
        "simple_outer_poles": 2,
        "totally_ramified_points": 2,
        "totally_ramified_points_in_challenge_field": True,
        "ramification_index": 5,
        "forced_ramification": 8,
        "riemann_hurwitz_budget": 8,
        "riemann_hurwitz_saturated": True,
        "right_component_K_descent": (
            "ratio of two reduced split active-fiber locators"
        ),
        "K_rational_normal_form": (
            "K-source-and-target-conjugate to c z^5"
        ),
        "active_fiber_points_in_K": 5,
        "active_fiber_reduced": True,
        "p_mod_5": 3,
        "q": str(Q),
        "q_mod_5": 4,
        "gcd_5_q_minus_1": 1,
        "fifth_power_map_on_K_is_bijective": True,
        "reduced_five_point_K_fiber_possible": False,
        "actual_producer_empty": True,
    }
    require(gate == expected, "degree-five gate")
    require(is_prime_trial(P), "deployed prime")
    require(P % 5 == 3, "deployed prime mod five")
    require(Q == int(gate["q"]), "challenge field cardinality")
    require(Q % 5 == 4, "challenge field mod five")
    require(math.gcd(5, Q - 1) == 1, "fifth-power bijectivity")
    inverse = pow(5, -1, Q - 1)
    require((5 * inverse) % (Q - 1) == 1, "fifth-root exponent")


def check_degree_thirty(gate: dict[str, Any]) -> None:
    expected = {
        "profile_inner_degree": 30,
        "simple_outer_poles": 2,
        "exceptional_source_points_per_fiber": 6,
        "exceptional_ramification_index": 5,
        "pullback_divisors": (
            "h^*[0]=5R_0 and h^*[infinity]=5R_infinity after target "
            "normalization"
        ),
        "reduced_divisor_degrees": [6, 6],
        "fifth_power_extraction": (
            "h=p_5 composed with r up to target scaling"
        ),
        "power_map_degree": 5,
        "refined_inner_degree": 6,
        "terminal": (
            "ROUTED_TO_INNER_DEGREE_6_BY_FIFTH_POWER_EXTRACTION"
        ),
        "actual_degree_six_producer_deleted": False,
    }
    require(gate == expected, "degree-thirty refinement")
    require(5 * gate["refined_inner_degree"] == 30, "30 to 6 refinement")


def check_pencil_equivalence(gate: dict[str, Any]) -> None:
    expected = {
        "source_partition": (
            "a blocks S_i of size m and b blocks R_j of size m/5"
        ),
        "pencil_dimension": 2,
        "pencil_forms_degree": "m",
        "pencil_coprime": True,
        "complete_source_condition": "A_{S_i} belongs to W",
        "exceptional_source_condition": "A_{R_j}^5 belongs to W",
        "active_condition": "V_act belongs to Sym^n(W)",
        "outer_denominator": (
            "Q=product_i ell_i^5 times product_j mu_j"
        ),
        "outer_denominator_degree_identity": "5a+b=n",
        "composition_reconstruction": (
            "f=(P/Q) composed with [H0:H1]"
        ),
        "self_correspondence_factor": (
            "H0(T)H1(W)-H1(T)H0(W) divides "
            "numerator(f(T)-f(W))"
        ),
        "equivalence_proved": True,
        "carrier_owner_implied": False,
    }
    require(gate == expected, "binary source-pencil equivalence")


def check_right_component_descent(gate: dict[str, Any]) -> None:
    expected = {
        "challenge_field": "K=F_{p^6}",
        "input": (
            "two distinct reduced active fibers whose points are "
            "individually K-rational"
        ),
        "construction": (
            "h_0=L_0/L_infinity is a K-rational target transform of h"
        ),
        "outer_map_descent": (
            "F_0 is fixed by Gal(Kbar/K) because substitution Y to "
            "h_0(T) is injective"
        ),
        "right_component_defined_over_K_up_to_target_PGL2": True,
        "outer_component_defined_over_K_after_same_transform": True,
        "carrier_domain_action_implied": False,
    }
    require(gate == expected, "challenge-field right-component descent")


def check_degree_twelve(gate: dict[str, Any]) -> None:
    expected = {
        "profile_inner_degree": 12,
        "source_partition_count": 1,
        "source_pencil_form": "W=<A,N>",
        "leading_outer_coefficient_normalized_to_one_over_K": True,
        "residue_equation": "N_0^5=V_act mod A",
        "split_residue_algebra": "K[T]/(A) is isomorphic to K^12",
        "fifth_power_on_residue_algebra_bijective": True,
        "normalized_residue_candidate_unique": True,
        "all_degree_twelve_lifts": "N=N_0+cA",
        "pencil_independent_of_lift": True,
        "terminal_membership_test": (
            "V_act in span_K{A^5,A^4N_0,A^3N_0^2,A^2N_0^3,"
            "AN_0^4,N_0^5}"
        ),
        "producer_deleted_unconditionally": False,
        "carrier_owner_implied": False,
    }
    require(gate == expected, "degree-twelve canonical pencil")
    require(math.gcd(5, Q - 1) == 1, "degree-twelve fifth-power gate")


def check_degree_two(gate: dict[str, Any]) -> None:
    expected = {
        "profile_inner_degree": 2,
        "deck_involution_defined_over_K": True,
        "deck_involution_defined_over_F_p_proved": False,
        "deck_action_on_carrier_D_proved": False,
        "conditional_prime_field_stabilizer_theorem": (
            "gamma(D)=D implies gamma(x)=kappa x or kappa/x with "
            "kappa in D"
        ),
        "conditional_involution_types": [
            "POWER_PAIR_x_to_minus_x",
            "RECIPROCAL_PAIR_x_to_kappa_over_x",
        ],
        "reciprocal_uniformity_condition": "kappa in D minus D^2",
        "parameter_to_carrier_same_record_bridge_open": True,
        "received_data_descent_proved": False,
        "slope_projection_descent_proved": False,
    }
    require(gate == expected, "degree-two parameter/carrier gate")
    require(DOMAIN_SIZE < P, "carrier stabilizer binomial gate")
    require(P > DOMAIN_SIZE, "intermediate binomial coefficients nonzero")


def check_bindings(bindings: list[dict[str, Any]]) -> None:
    require(bindings == EXPECTED_BINDINGS, "source bindings")
    for binding in bindings:
        require(
            git_output("cat-file", "-t", binding["commit"]) == "commit",
            "binding commit object",
        )
        require(
            git_output(
                "rev-parse",
                binding["commit"] + ":" + binding["path"],
            )
            == binding["blob_oid"],
            "binding commit/path/blob",
        )


def check_replays(replays: dict[str, Any]) -> None:
    expected_paths = {
        "sage": (
            "experimental/scripts/"
            "verify_kb_mca_v4_degree60_decomposition_source_fiber_"
            "adapter_v1.sage"
        ),
        "wolfram": (
            "experimental/scripts/"
            "verify_kb_mca_v4_degree60_decomposition_source_fiber_"
            "adapter_v1.wl"
        ),
    }
    require(set(replays) == set(expected_paths), "replay names")
    for name, path_string in expected_paths.items():
        require(
            set(replays[name]) == {"path", "sha256"},
            f"{name} replay schema",
        )
        require(replays[name]["path"] == path_string, f"{name} replay path")
        path = REPO_ROOT / path_string
        require(path.is_file(), f"{name} replay exists")
        require(
            replays[name]["sha256"]
            == hashlib.sha256(path.read_bytes()).hexdigest(),
            f"{name} replay hash",
        )


def check_conclusion(conclusion: dict[str, Any]) -> None:
    expected = {
        "profile_count": 8,
        "deleted_inner_degrees": [5],
        "conditional_same_degree_carrier_compatible": [2, 4],
        "direct_producer_exclusion_open": [3, 6, 10, 12],
        "canonical_single_pencil_test_open": [12],
        "refined_to_earlier_inner_degree": [{"from": 30, "to": 6}],
        "u2_branch_closed": False,
        "u3_authorized": False,
        "parameter_to_carrier_same_record_bridge_proved": False,
        "row_closed": False,
        "ledger_movement": 0,
        "status": STATUS,
        "next_maximal_attack": (
            "run the exact binary source-pencil compiler for m=2,3,4,6,10 "
            "and the canonical membership test for m=12, then require a "
            "same-record parameter-to-carrier/data/slope bridge for every "
            "survivor"
        ),
    }
    require(conclusion == expected, "conclusion")


def check(data: dict[str, Any]) -> None:
    require(
        set(data)
        == {
            "schema",
            "payload_sha256",
            "statement",
            "parent_stack",
            "divisor_adapter",
            "profiles",
            "excluded_profile_degrees",
            "binary_source_pencil_equivalence",
            "challenge_field_right_component_descent",
            "conditional_carrier_compatibility",
            "degree_five_deletion",
            "degree_thirty_refinement",
            "degree_twelve_canonical_pencil",
            "degree_two_parameter_carrier_gate",
            "source_bindings",
            "independent_replays",
            "conclusion",
            "nonclaims",
        },
        "top-level schema",
    )
    require(
        data["schema"]
        == "kb-mca-v4-degree60-decomposition-source-fiber-adapter-v1",
        "schema",
    )
    require(data["payload_sha256"] == payload_hash(data), "payload hash")
    check_statement(data["statement"])
    check_parent(data["parent_stack"])
    require(
        data["divisor_adapter"] == EXPECTED_DIVISOR_ADAPTER,
        "divisor adapter",
    )
    check_profiles(data)
    check_pencil_equivalence(data["binary_source_pencil_equivalence"])
    check_right_component_descent(
        data["challenge_field_right_component_descent"]
    )
    check_conditional_carrier(data["conditional_carrier_compatibility"])
    check_degree_five(data["degree_five_deletion"])
    check_degree_thirty(data["degree_thirty_refinement"])
    check_degree_twelve(data["degree_twelve_canonical_pencil"])
    check_degree_two(data["degree_two_parameter_carrier_gate"])
    check_bindings(data["source_bindings"])
    check_replays(data["independent_replays"])
    check_conclusion(data["conclusion"])
    require(data["nonclaims"] == EXPECTED_NONCLAIMS, "nonclaims")


def mutations(data: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    result: list[tuple[str, dict[str, Any]]] = []

    def add(name: str, mutate: Callable[[dict[str, Any]], None]) -> None:
        forged = copy.deepcopy(data)
        mutate(forged)
        forged["payload_sha256"] = payload_hash(forged)
        result.append((name, forged))

    statement_keys = [
        "agreement",
        "B_star",
        "deployed_prime",
        "challenge_field",
        "challenge_field_cardinality",
        "deployed_domain_cardinality",
        "endpoint_degree",
        "active_root_count",
        "active_roots_squarefree",
        "active_roots_are_challenge_field_parameter_values",
        "source_root_count",
        "source_roots_are_challenge_field_parameter_values",
        "source_pole_order",
        "active_source_disjoint",
        "endpoint_parameter_line_identified_with_carrier_domain",
        "decomposition_scope",
    ]
    for key in statement_keys:
        add(
            f"statement {key}",
            lambda d, key=key: d["statement"].update({key: "forged"}),
        )

    parent_keys = [
        "head_commit",
        "certificate_path",
        "certificate_blob_oid",
        "certificate_payload_sha256",
        "imported_terminal",
    ]
    for key in parent_keys:
        add(
            f"parent {key}",
            lambda d, key=key: d["parent_stack"].update({key: "forged"}),
        )

    adapter_keys = [
        "homogeneous_no_cancellation",
        "active_outer_zeros_simple",
        "outer_pole_orders",
        "source_factorization",
        "locator_level_only",
        "received_data_descent_proved",
        "explaining_polynomial_descent_proved",
        "slope_projection_descent_proved",
    ]
    for key in adapter_keys:
        add(
            f"adapter {key}",
            lambda d, key=key: d["divisor_adapter"].update({key: "forged"}),
        )

    for index in range(8):
        add(
            f"profile {index} degree",
            lambda d, index=index: d["profiles"][index].update(
                inner_degree=1
            ),
        )
        add(
            f"profile {index} terminal",
            lambda d, index=index: d["profiles"][index].update(
                terminal="PAID"
            ),
        )
        add(
            f"profile {index} partition count",
            lambda d, index=index: d["profiles"][index].update(
                source_partition_count=(
                    d["profiles"][index]["source_partition_count"] + 1
                )
            ),
        )

    add("profile removed", lambda d: d["profiles"].pop())
    add(
        "excluded profile",
        lambda d: d.update(excluded_profile_degrees=[20]),
    )
    add(
        "conditional carrier eligible",
        lambda d: d["conditional_carrier_compatibility"].update(
            same_degree_cardinality_compatible_inner_degrees=[2, 3, 4]
        ),
    )
    add(
        "conditional carrier false bridge",
        lambda d: d["conditional_carrier_compatibility"].update(
            same_record_parameter_to_carrier_bridge_proved=True
        ),
    )
    add(
        "conditional carrier gate removed",
        lambda d: d["conditional_carrier_compatibility"][
            "open_semantic_gates"
        ].pop(),
    )
    add(
        "pencil active condition",
        lambda d: d["binary_source_pencil_equivalence"].update(
            active_condition="forged"
        ),
    )
    add(
        "pencil false owner",
        lambda d: d["binary_source_pencil_equivalence"].update(
            carrier_owner_implied=True
        ),
    )
    add(
        "right component false carrier",
        lambda d: d["challenge_field_right_component_descent"].update(
            carrier_domain_action_implied=True
        ),
    )
    add(
        "degree5 RH",
        lambda d: d["degree_five_deletion"].update(
            riemann_hurwitz_saturated=False
        ),
    )
    add(
        "degree5 field cardinality",
        lambda d: d["degree_five_deletion"].update(
            q=str(Q + 1)
        ),
    )
    add(
        "degree5 fifth-power gate",
        lambda d: d["degree_five_deletion"].update(
            fifth_power_map_on_K_is_bijective=False
        ),
    )
    add(
        "degree5 producer",
        lambda d: d["degree_five_deletion"].update(
            actual_producer_empty=False
        ),
    )
    add(
        "degree30 target",
        lambda d: d["degree_thirty_refinement"].update(
            refined_inner_degree=10
        ),
    )
    add(
        "degree30 false deletion",
        lambda d: d["degree_thirty_refinement"].update(
            actual_degree_six_producer_deleted=True
        ),
    )
    add(
        "degree12 residue",
        lambda d: d["degree_twelve_canonical_pencil"].update(
            residue_equation="forged"
        ),
    )
    add(
        "degree12 false deletion",
        lambda d: d["degree_twelve_canonical_pencil"].update(
            producer_deleted_unconditionally=True
        ),
    )
    add(
        "degree2 false prime-field descent",
        lambda d: d["degree_two_parameter_carrier_gate"].update(
            deck_involution_defined_over_F_p_proved=True
        ),
    )
    add(
        "degree2 false carrier action",
        lambda d: d["degree_two_parameter_carrier_gate"].update(
            deck_action_on_carrier_D_proved=True
        ),
    )
    for index in range(len(EXPECTED_BINDINGS)):
        add(
            f"binding {index}",
            lambda d, index=index: d["source_bindings"][index].update(
                blob_oid="0" * 40
            ),
        )
    add(
        "sage hash",
        lambda d: d["independent_replays"]["sage"].update(
            sha256="0" * 64
        ),
    )
    add(
        "wolfram hash",
        lambda d: d["independent_replays"]["wolfram"].update(
            sha256="0" * 64
        ),
    )
    conclusion_keys = [
        "profile_count",
        "deleted_inner_degrees",
        "conditional_same_degree_carrier_compatible",
        "direct_producer_exclusion_open",
        "canonical_single_pencil_test_open",
        "refined_to_earlier_inner_degree",
        "u2_branch_closed",
        "u3_authorized",
        "parameter_to_carrier_same_record_bridge_proved",
        "row_closed",
        "ledger_movement",
        "status",
        "next_maximal_attack",
    ]
    for key in conclusion_keys:
        add(
            f"conclusion {key}",
            lambda d, key=key: d["conclusion"].update({key: "forged"}),
        )
    add("nonclaim removed", lambda d: d["nonclaims"].pop())
    add("schema", lambda d: d.update(schema="forged"))
    add("unknown top-level claim", lambda d: d.update(row_closed=True))
    add(
        "unknown parent claim",
        lambda d: d["parent_stack"].update(row_closed=True),
    )
    add(
        "unknown replay claim",
        lambda d: d["independent_replays"]["sage"].update(
            symbolic_proof=True
        ),
    )

    forged_hash = copy.deepcopy(data)
    forged_hash["payload_sha256"] = "0" * 64
    result.append(("payload hash", forged_hash))
    return result


def tamper_selftest(data: dict[str, Any]) -> int:
    forged_cases = mutations(data)
    rejected = 0
    for name, forged in forged_cases:
        try:
            check(forged)
        except (VerificationError, KeyError, TypeError, ValueError):
            rejected += 1
        else:
            raise VerificationError(f"mutation accepted: {name}")
    require(rejected == len(forged_cases), "all mutations rejected")

    try:
        json.loads(
            '{"a":1,"a":2}',
            object_pairs_hook=reject_duplicate_pairs,
        )
    except VerificationError:
        pass
    else:
        raise VerificationError("duplicate JSON key accepted")
    return rejected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    arguments = parser.parse_args()
    require(
        arguments.check or arguments.tamper_selftest,
        "choose a verification mode",
    )

    data = load_json(CERTIFICATE)
    check(data)
    mutation_count = 0
    if arguments.tamper_selftest:
        mutation_count = tamper_selftest(data)

    print("status=" + STATUS)
    print("decomposition_profiles=8")
    print("deleted_inner_degrees=[5]")
    print("degree30_refined_to_inner_degree=6")
    print("conditional_same_degree_carrier_compatible=[2,4]")
    print("degree12_canonical_source_pencil_count=1")
    print("direct_producer_exclusion_open=[3,6,10,12]")
    if arguments.tamper_selftest:
        print(
            f"tamper_mutations_rejected={mutation_count}/{mutation_count}"
        )
        print("duplicate_json_keys=REJECTED")
    print("ledger_movement=0")
    print("payload_sha256=" + data["payload_sha256"])


if __name__ == "__main__":
    main()
