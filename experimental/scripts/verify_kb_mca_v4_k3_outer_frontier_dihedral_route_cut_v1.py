#!/usr/bin/env python3
"""Verify the KoalaBear K3 outer-frontier synthesis and dihedral route cut.

The packet is deliberately fail-closed.  It proves an exact finite frontier,
checks that the live active-v4 four-cell partition already exists, proves a
conditional any-69 implication, and gives a deployed-carrier counterexample
to treating recurrent quadratic folds as automatic strict progress.  It does
not manufacture the missing semantic adapter or resolve either final m=2
transverse type.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import subprocess
import sys
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
    / "data/certificates/"
    "kb-mca-v4-k3-outer-frontier-dihedral-route-cut-v1/"
    "kb_mca_v4_k3_outer_frontier_dihedral_route_cut_v1.json"
)
BASE_HEAD = "c2edcfa5cbfb8a41e7dea04ae1b34325c90ed5dc"
HISTORICAL_PROVENANCE_HEAD = "ceb6611e7f6aa713fe4a2d7c6d48ca67daaae365"
GRANDE_FINALE_PATH = "experimental/grande_finale.tex"
GRANDE_FINALE_BLOB_AT_BASE = "6b21d6ea937a8a9f85fc7ade6032d73efd4c7222"
TANGENT_VERIFIER = (
    EXPERIMENTAL / "scripts/verify_kb_mca_v4_tangent_source_adapter_v1.py"
)

SOURCES = {
    "source_pencil": {
        "path": (
            "experimental/data/certificates/"
            "kb-mca-v4-degree60-source-pencil-rank-compiler-v1/"
            "kb_mca_v4_degree60_source_pencil_rank_compiler_v1.json"
        ),
        "payload_sha256": (
            "6d4bc83e40e491f02f7d265b021628ffb7d52b1978c0655f83e5a9d3e0a9f4bb"
        ),
        "blob_oid": "5c16c7884b349d7e474b8dfc1267ab357ef0d477",
    },
    "m12_close": {
        "path": (
            "experimental/data/certificates/"
            "kb-mca-v4-m12-diagonal-socle-degree5-close-v1/"
            "kb_mca_v4_m12_diagonal_socle_degree5_close_v1.json"
        ),
        "payload_sha256": (
            "456b51c78e837c8a27ffda0b43409c63c88128b254be320723728868db096e6f"
        ),
        "blob_oid": "9e1bd3d89dac6409f148dc134fda46d3bf644c11",
    },
    "m10_router": {
        "path": (
            "experimental/data/certificates/"
            "kb-mca-v4-m10-scott-strip-lower-degree-router-v1/"
            "kb_mca_v4_m10_scott_strip_lower_degree_router_v1.json"
        ),
        "payload_sha256": (
            "66117d7ba207a66606fc4ae4770a2b314b3510066be7af734b4e579d028ce1d1"
        ),
        "blob_oid": "6e49093fdb9d9e55b45c55265eb3cc0c0e65e8c9",
    },
    "m6_router": {
        "path": (
            "experimental/data/certificates/"
            "kb-mca-v4-m6-scott-cartesian-degree2-router-v1/"
            "kb_mca_v4_m6_scott_cartesian_degree2_router_v1.json"
        ),
        "payload_sha256": (
            "b34e096730f3d93644c283f95d65f622100d6868e9882ed2b901fa109b3d6116"
        ),
        "blob_oid": "af5fd87a5c28f3b021fc05971a665e6d92f978af",
    },
    "m4_close": {
        "path": (
            "experimental/data/certificates/"
            "kb-mca-v4-m4-adjacency-genus-exclusion-v1/"
            "kb_mca_v4_m4_adjacency_genus_exclusion_v1.json"
        ),
        "payload_sha256": (
            "a0bc909a9e05c097440d318f5fe7aed052387507723fc1f3337172d3e5db7428"
        ),
        "blob_oid": "a0b2c8ec260da35ffdefa5a29c7aa5496af5cc79",
    },
    "m3_router": {
        "path": (
            "experimental/data/certificates/"
            "kb-mca-v4-m3-primitive-outer-degree2-router-v1/"
            "kb_mca_v4_m3_primitive_outer_degree2_router_v1.json"
        ),
        "payload_sha256": (
            "0f7c0134c723875d66dd19d96f9c68c7299079b5560e63780910afc6d86f21d4"
        ),
        "blob_oid": "24f406d8bdb72d8562c91b28890eae59befd6d91",
    },
    "m2_full_v4_close": {
        "path": (
            "experimental/data/certificates/"
            "kb-mca-v4-m2-r2-dihedral-degree3-source-facet-exclusion-v1/"
            "kb_mca_v4_m2_r2_dihedral_degree3_source_facet_exclusion_v1.json"
        ),
        "payload_sha256": (
            "f48a46f22bc15098f5fc566e6f009d76afa4751c4fd4b4b8edaf481e619c5a01"
        ),
        "blob_oid": "75fce13ee5cee43dc2d74565505641adf114f6f2",
    },
    "m2_live_interface": {
        "path": (
            "experimental/data/certificates/"
            "kb-mca-v4-m2-u2-universal-source-facet-census-v1/"
            "kb_mca_v4_m2_u2_universal_source_facet_census_v1.json"
        ),
        "payload_sha256": (
            "8f768cfded349dc3dd40cf6214ffe980c69ff18ae2d8c209e63b4307767429d2"
        ),
        "blob_oid": "844b7885620bf10fe19336f3acd7866cf1d9a204",
    },
    "active_v4_manifest": {
        "path": (
            "experimental/data/certificates/"
            "kb-mca-v4-tangent-source-adapter-v1/manifest.json"
        ),
        "payload_sha256": (
            "ffd1e427f53db3d2dbfd13e69a05d173d2f2aa1f03c152aead73fcc821094acb"
        ),
        "blob_oid": "c29987f43f7526aacbbf4c238ee6887687876879",
    },
    "active_v4_row": {
        "path": (
            "experimental/data/certificates/"
            "kb-mca-v4-tangent-source-adapter-v1/row_manifest.json"
        ),
        "payload_sha256": (
            "36e9d69aaf6deeb4fe123358e8bb8d5bbbdcb40c9315b4316f0c6a1189a270e1"
        ),
        "blob_oid": "15731acc39a4cc38d8175fd09535b149490f8551",
    },
}

EXPECTED_HISTORY = [
    ("source_pencil", 26, [2, 3, 4, 6, 10, 12]),
    ("m12_closed", 22, [2, 3, 4, 6, 10]),
    ("m10_routed", 18, [2, 3, 4, 6]),
    ("m6_routed", 12, [2, 3, 4]),
    ("m4_closed", 8, [2, 3]),
    ("m3_routed", 3, [2]),
    ("m2_full_v4_closed", 2, [2]),
]
EXPECTED_RESIDUAL = [[2, 4, 2], [2, 8, 1]]
EXPECTED_OWNER_ORDER = [
    "SOURCE_COORDINATE_TANGENT_IMAGE",
    "ACTIVE_V4_BOUNDARY_PREFIX_Q",
    "ACTIVE_V4_BALANCED_CORE",
    "UNPAID_V4_COMPLEMENT",
]
SAME_RECORD_KEY = [
    "received_line_id",
    "slope_coordinates",
    "graph_record_id",
    "evaluation_support_id",
    "received_data_id",
    "explaining_polynomial_id",
    "source_map_class_id",
    "active_v4_owner_index",
]
REQUIRED_ADAPTER_GATES = [
    "transverse_terminal_to_active_cell_mapping",
    "semantic_complete_selector",
    "strict_descent_69_class_transport_or_exact_reselection",
    "full_same_record_owner_descent",
]
PACKET_FILES = {
    "note": (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_k3_outer_frontier_dihedral_route_cut_v1.md"
    ),
    "python_verifier": (
        "experimental/scripts/"
        "verify_kb_mca_v4_k3_outer_frontier_dihedral_route_cut_v1.py"
    ),
    "sage_replay": (
        "experimental/scripts/"
        "verify_kb_mca_v4_k3_outer_frontier_dihedral_route_cut_v1.sage"
    ),
    "wolfram_replay": (
        "experimental/scripts/"
        "verify_kb_mca_v4_k3_outer_frontier_dihedral_route_cut_v1.wl"
    ),
    "readme": (
        "experimental/data/certificates/"
        "kb-mca-v4-k3-outer-frontier-dihedral-route-cut-v1/README.md"
    ),
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def payload_hash(value: dict[str, Any]) -> str:
    unhashed = copy.deepcopy(value)
    unhashed.pop("payload_sha256", None)
    return hashlib.sha256(canonical_json(unhashed).encode()).hexdigest()


def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
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
    require(isinstance(value, dict), f"{label}: expected JSON object")
    return value


def git_output(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


Polynomial = dict[tuple[int, int], int]


def poly_add(left: Polynomial, right: Polynomial, modulus: int) -> Polynomial:
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = (result.get(monomial, 0) + coefficient) % modulus
        if result[monomial] == 0:
            del result[monomial]
    return result


def poly_scale(value: Polynomial, scalar: int, modulus: int) -> Polynomial:
    return {
        monomial: (scalar * coefficient) % modulus
        for monomial, coefficient in value.items()
        if (scalar * coefficient) % modulus
    }


def poly_multiply(
    left: Polynomial, right: Polynomial, modulus: int
) -> Polynomial:
    result: Polynomial = {}
    for (left_t, left_x), left_coefficient in left.items():
        for (right_t, right_x), right_coefficient in right.items():
            monomial = (left_t + right_t, left_x + right_x)
            result[monomial] = (
                result.get(monomial, 0)
                + left_coefficient * right_coefficient
            ) % modulus
            if result[monomial] == 0:
                del result[monomial]
    return result


def replay_tangent_verifier() -> None:
    """Fail closed unless the repaired tangent packet passes in both modes."""

    for optimized in (False, True):
        command = [sys.executable]
        if optimized:
            command.append("-O")
        command.extend([str(TANGENT_VERIFIER), "--check"])
        result = subprocess.run(
            command,
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        mode = "optimized" if optimized else "normal"
        require(
            result.returncode == 0,
            f"tangent verifier {mode} replay: "
            f"{result.stdout.strip()} {result.stderr.strip()}",
        )


def is_prime_64(n: int) -> bool:
    if n < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for prime in small:
        if n % prime == 0:
            return n == prime
    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2
    for base in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if base % n == 0:
            continue
        value = pow(base, d, n)
        if value in (1, n - 1):
            continue
        for _ in range(s - 1):
            value = value * value % n
            if value == n - 1:
                break
        else:
            return False
    return True


def load_sources() -> dict[str, dict[str, Any]]:
    require(
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", BASE_HEAD, "HEAD"],
            cwd=REPO_ROOT,
        ).returncode
        == 0,
        "the packet must remain stacked on the exact #1132 head",
    )
    require(
        git_output("rev-parse", f"{BASE_HEAD}:{GRANDE_FINALE_PATH}")
        == GRANDE_FINALE_BLOB_AT_BASE,
        "exact-base grande_finale.tex blob pin",
    )
    loaded = {}
    for key, binding in SOURCES.items():
        path = REPO_ROOT / binding["path"]
        data = parse_json(path.read_text(), binding["path"])
        require(
            data.get("payload_sha256") == binding["payload_sha256"],
            f"{key}: payload pin",
        )
        require(
            payload_hash(data) == binding["payload_sha256"],
            f"{key}: canonical payload seal",
        )
        require(
            git_output("rev-parse", f"{BASE_HEAD}:{binding['path']}")
            == binding["blob_oid"],
            f"{key}: base blob pin",
        )
        loaded[key] = data
    return loaded


def source_states(source: dict[str, Any]) -> set[tuple[int, int, int]]:
    states = {
        (row["m"], pair[0], pair[1])
        for row in source["transverse_outer_terminal"]["rows"]
        for pair in row["r_delta"]
    }
    require(len(states) == 26, "source frontier cardinality")
    require(all(delta * r == 4 * m for m, r, delta in states), "delta*r=4m")
    return states


def derive_frontier(
    sources: dict[str, dict[str, Any]]
) -> tuple[list[dict[str, Any]], list[list[int]]]:
    frontier = source_states(sources["source_pencil"])
    history = [
        {
            "stage": "source_pencil",
            "count": len(frontier),
            "live_inner_degrees": sorted({state[0] for state in frontier}),
        }
    ]

    require(sources["m12_close"]["conclusion"]["m12_closed"], "m12 close")
    frontier = {state for state in frontier if state[0] != 12}
    history.append(
        {
            "stage": "m12_closed",
            "count": len(frontier),
            "live_inner_degrees": sorted({state[0] for state in frontier}),
        }
    )

    require(sources["m10_router"]["conclusion"]["m10_routed"], "m10 route")
    frontier = {state for state in frontier if state[0] != 10}
    history.append(
        {
            "stage": "m10_routed",
            "count": len(frontier),
            "live_inner_degrees": sorted({state[0] for state in frontier}),
        }
    )

    require(sources["m6_router"]["conclusion"]["m6_routed"], "m6 route")
    frontier = {state for state in frontier if state[0] != 6}
    history.append(
        {
            "stage": "m6_routed",
            "count": len(frontier),
            "live_inner_degrees": sorted({state[0] for state in frontier}),
        }
    )

    require(
        sources["m4_close"]["conclusion"]["m4_transverse_row_empty"],
        "m4 close",
    )
    frontier = {state for state in frontier if state[0] != 4}
    history.append(
        {
            "stage": "m4_closed",
            "count": len(frontier),
            "live_inner_degrees": sorted({state[0] for state in frontier}),
        }
    )

    require(
        sources["m3_router"]["conclusion"]["m3_independent_type_count"] == 0,
        "m3 route",
    )
    frontier = {state for state in frontier if state[0] != 3}
    history.append(
        {
            "stage": "m3_routed",
            "count": len(frontier),
            "live_inner_degrees": sorted({state[0] for state in frontier}),
        }
    )

    require(
        sources["m2_full_v4_close"]["conclusion"]["full_v4_type_deleted"],
        "full-V4 m2 close",
    )
    frontier.remove((2, 2, 4))
    history.append(
        {
            "stage": "m2_full_v4_closed",
            "count": len(frontier),
            "live_inner_degrees": sorted({state[0] for state in frontier}),
        }
    )
    residual = [list(state) for state in sorted(frontier)]
    require(residual == EXPECTED_RESIDUAL, "exact residual types")
    return history, residual


def derive_live_partition(
    sources: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    manifest = sources["active_v4_manifest"]
    row = sources["active_v4_row"]
    partition = row["partition"]
    stages = partition["chronology_stages"]
    owner_order = [stage["owner_id"] for stage in stages]
    atom_order = [stage["atom_id"] for stage in stages]
    require(owner_order == EXPECTED_OWNER_ORDER, "live four-cell owner order")
    require(atom_order == ["U_paid", "U_Q", "U_BC", "U_new"], "atom order")
    require(partition["owner_order"] == owner_order, "partition owner order")
    require(partition["atom_order"] == atom_order, "partition atom order")
    require(all(stage["predicate_available"] for stage in stages), "predicates")
    require(partition["first_match"], "first-match partition")
    require(partition["first_match_disjoint"], "disjoint partition")
    require(partition["witness_exhaustive"], "witness exhaustive partition")
    require(partition["same_partition_for_all_atoms"], "single partition")
    require(
        manifest["architecture_id"] == row["architecture_id"],
        "active architecture binding",
    )
    require(
        manifest["partition_sha256"] == partition["partition_sha256"],
        "active partition digest binding",
    )
    row_sha256 = hashlib.sha256(
        (REPO_ROOT / SOURCES["active_v4_row"]["path"]).read_bytes()
    ).hexdigest()
    require(
        manifest["row_manifest_binding"]["sha256"] == row_sha256,
        "manifest raw row hash binding",
    )
    return {
        "architecture_id": manifest["architecture_id"],
        "manifest_payload_sha256": manifest["payload_sha256"],
        "row_payload_sha256": row["payload_sha256"],
        "partition_sha256": partition["partition_sha256"],
        "owner_order": owner_order,
        "atom_order": atom_order,
        "live_four_cell_partition_present": True,
        "live_four_cell_partition_first_match_disjoint": True,
        "live_four_cell_partition_witness_exhaustive": True,
        "transverse_terminal_to_active_cell_mapping_proved": False,
    }


def derive_route_cut() -> dict[str, Any]:
    p = 2_130_706_433
    n = 2**21
    half = n // 2
    primitive_root = 3
    require(is_prime_64(p), "deployed field prime")
    require(p - 1 == 127 * 2**24, "p-1 factorization")
    a = pow(primitive_root, (p - 1) // n, p)
    require(a == 1_213_133_211, "deployed carrier generator")
    require(pow(a, n, p) == 1, "a^N=1")
    require(pow(a, half, p) == p - 1, "a^(N/2)=-1")
    require(math.gcd(2, n) == 2, "fixed-point congruence divisor")
    require(1 % 2 == 1 and 3 % 2 == 1, "odd reflection exponents")

    # Derive q_c(T)-q_c(x)=((T-x)(T*x-c))/(T*x) coefficientwise in
    # F_p[T,x], then combine it with the exact order and fixed-point gates.
    t: Polynomial = {(1, 0): 1}
    x: Polynomial = {(0, 1): 1}
    tx = poly_multiply(t, x, p)
    t_minus_x = poly_add(t, poly_scale(x, -1, p), p)
    quotient_fibres = []
    for name, exponent, coefficient_label in (
        ("q1", 1, "a"),
        ("q2", 3, "a^3"),
    ):
        c = pow(a, exponent, p)
        constant_c: Polynomial = {(0, 0): c}
        tx_minus_c = poly_add(
            tx, poly_scale(constant_c, -1, p), p
        )
        factored_numerator = poly_multiply(t_minus_x, tx_minus_c, p)
        direct_numerator = poly_add(
            poly_add(
                poly_multiply(poly_multiply(t, t, p), x, p),
                poly_scale(poly_multiply(t, poly_multiply(x, x, p), p),
                           -1, p),
                p,
            ),
            poly_add(
                poly_scale(t, -c, p),
                poly_scale(x, c, p),
                p,
            ),
            p,
        )
        require(
            direct_numerator == factored_numerator,
            f"{name} fibre-difference identity",
        )
        require(c != 0, f"{name} nonzero coefficient")
        require(pow(c, n, p) == 1, f"{name} coefficient lies in D")
        require(
            exponent % math.gcd(2, n) != 0,
            f"{name} involution is fixed-point-free on D",
        )
        quotient_fibres.append(
            {
                "name": name,
                "involution": f"x |-> {coefficient_label}/x",
                "coefficient": coefficient_label,
                "coefficient_value": c,
                "formula": f"{name}(x)=x+{coefficient_label}/x",
                "fibre_difference_formula": (
                    f"{name}(T)-{name}(x)="
                    f"((T-x)(T*x-{coefficient_label}))/(T*x)"
                ),
                "rational_map_degree": 2,
                "preserves_D": True,
                "complete_D_fibre_formula": (
                    f"{name}^(-1)({name}(x))={{x,"
                    f"{coefficient_label}/x}} for x in D"
                ),
                "D_fibre_complete": True,
                "D_fibre_reduced": True,
                "D_fibre_cardinality": 2,
            }
        )

    rotation_order = n // math.gcd(n, 2)
    generated_group_order = 2 * rotation_order
    require(rotation_order == 2**20, "rotation order")
    require(generated_group_order == n, "dihedral group order")
    require(pow(a, 2 * half, p) == 1, "rotation invariance exponent")
    require(pow(a, half, p) == pow(a, 3 * half, p) == p - 1,
            "reflection invariance exponents")
    require((p - 1) % n == 0, "all N-th roots lie in the base field")
    require(math.gcd(p, n) == 1, "x^N-1 is separable")

    # D supplies N distinct roots of x^N-1 and that polynomial has degree N,
    # so it is the complete zero set.  Separability follows from
    # gcd(N,p)=1; the two pole orders follow from the numerator value at zero
    # and the numerator/denominator degree difference at infinity.
    zero_fibre = {
        "equation": "u^(-1)(0)=D",
        "defining_polynomial": "x^N-1",
        "cardinality": n,
        "fibre_degree": n,
        "complete": True,
        "reduced": True,
        "separability": "N divides p-1 and p does not divide N",
        "pole_support": ["0", "infinity"],
        "pole_orders": {"0": half, "infinity": half},
        "pole_divisor_degree": n,
    }
    require(
        zero_fibre["pole_orders"]["0"]
        + zero_fibre["pole_orders"]["infinity"]
        == zero_fibre["fibre_degree"],
        "u pole divisor degree",
    )

    return {
        "field_prime": p,
        "field_prime_verified": True,
        "carrier_subgroup": "D=<a>",
        "carrier_order": n,
        "primitive_root_seed": primitive_root,
        "carrier_generator": a,
        "carrier_generator_order": n,
        "tau1": "x |-> a/x",
        "tau2": "x |-> a^3/x",
        "tau1_fixed_point_free_on_D": True,
        "tau2_fixed_point_free_on_D": True,
        "fixed_point_congruences": ["2k=1 mod N", "2k=3 mod N"],
        "quadratic_quotient_fibres": quotient_fibres,
        "rotation": "tau2*tau1: x |-> a^2*x",
        "rotation_order": rotation_order,
        "generated_group": "DIHEDRAL",
        "generated_group_order": generated_group_order,
        "common_invariant": "u=x^(N/2)-x^(-N/2)",
        "common_invariant_rational_map_degree": n,
        "common_invariant_value_on_D": 0,
        "common_invariant_zero_fibre": zero_fibre,
        "fixed_field_intersection": "F_p(x)^<tau1> INTERSECT F_p(x)^<tau2> = F_p(u)",
        "fixed_field_intersection_degree": n,
        "fixed_field_intersection_proved": True,
        "bounded_degree_four_progress_forced": False,
        "useful_nonconstant_quotient_on_D_forced": False,
        "actual_received_line_record_constructed": False,
        "scope": "CARRIER_PRESERVATION_INFERENCE_COUNTEREXAMPLE_ONLY",
    }


def derive_live_arithmetic() -> dict[str, Any]:
    p = 2_130_706_433
    b_star = 274_980_728_111_395_087
    tangent_paid = 981_104
    return {
        "field_prime": p,
        "B_star": b_star,
        "active_U_paid_tangent": tangent_paid,
        "active_reserve_after_tangent": b_star - tangent_paid,
        "source_map_cap68_live_charge_derived": False,
        "ledger_movement": 0,
    }


def derive_historical_calibration() -> dict[str, Any]:
    p = 2_130_706_433
    outer_multiplier = 1_894_736
    cap68 = (67 * p + 68) * outer_multiplier
    cap69 = (68 * p + 69) * outer_multiplier
    require(cap68 == 270_487_454_459_300_144, "historical cap68 calibration")
    require(cap69 == 274_524_580_645_231_568, "historical cap69 calibration")
    return {
        "source_commit": HISTORICAL_PROVENANCE_HEAD,
        "source_payload_sha256": (
            "afa673d57ed84c240560aae9e40ae72a33a115c5638fd4bad0b23859e2520ecb"
        ),
        "authority": False,
        "live_charge_derived": False,
        "role": "OFF_BRANCH_NON_LOAD_BEARING_PROVENANCE_ONLY",
        "field_prime": p,
        "outer_multiplier": outer_multiplier,
        "support_multiplier": outer_multiplier,
        "historical_cap68_calibration": cap68,
        "historical_cap69_calibration": cap69,
    }


def validate_packet(
    packet: dict[str, Any],
    sources: dict[str, dict[str, Any]],
    *,
    check_seal: bool = True,
) -> None:
    require(
        packet["schema"]
        == "kb-mca-v4-k3-outer-frontier-dihedral-route-cut-v1",
        "schema",
    )
    if check_seal:
        require(
            packet["payload_sha256"] == payload_hash(packet),
            "packet canonical payload seal",
        )
    require(packet["base_repository"]["head"] == BASE_HEAD, "base head")
    require(packet["base_repository"]["stacked_on_pr"] == 1132, "base PR")
    require(packet["statement"]["ledger_movement"] == 0, "ledger movement")
    require(packet["statement"]["workboard_item"] == "K3", "workboard item")

    bindings = packet["source_bindings"]
    require(len(bindings) == len(SOURCES), "all source bindings present")
    require(
        [binding["binding_id"] for binding in bindings] == list(SOURCES),
        "source binding order",
    )
    for binding in bindings:
        expected = SOURCES[binding["binding_id"]]
        require(binding["path"] == expected["path"], "source path pin")
        require(
            binding["payload_sha256"] == expected["payload_sha256"],
            f"{binding['binding_id']}: packet payload pin",
        )
        require(
            binding["blob_oid_at_base"] == expected["blob_oid"],
            f"{binding['binding_id']}: packet blob pin",
        )

    packet_files = packet["packet_files"]
    require(
        [item["file_id"] for item in packet_files] == list(PACKET_FILES),
        "packet file order",
    )
    for item in packet_files:
        expected_path = PACKET_FILES[item["file_id"]]
        require(item["path"] == expected_path, "packet file path")
        actual = hashlib.sha256((REPO_ROOT / expected_path).read_bytes()).hexdigest()
        require(item["sha256"] == actual, f"{item['file_id']}: packet file hash")

    repair = packet["active_v4_repair"]
    require(
        repair["predecessor_manifest_payload_sha256"]
        == "536b08f23e552b2cb4fb226d74d42d54750118dae2efe619ff6e67d69d0370bf",
        "predecessor manifest payload seam",
    )
    require(
        repair["predecessor_row_payload_sha256"]
        == "a05d8caf2b772c9c5cc7e7683631c9db7f5b3f2ba4cf8f436f6d3b16f4bdc189",
        "predecessor row payload seam",
    )
    require(
        repair["predecessor_grande_finale_blob_oid"]
        == "8a5d9791900ca9eed773feba146b92ad296704ce",
        "predecessor active-v4 blob seam",
    )
    require(
        repair["current_grande_finale_blob_oid"]
        == GRANDE_FINALE_BLOB_AT_BASE,
        "current active-v4 blob seam",
    )
    require(
        repair["current_grande_finale_blob_gate"]
        == "git rev-parse BASE_HEAD:experimental/grande_finale.tex",
        "current active-v4 direct blob gate",
    )
    require(
        repair["repaired_manifest_payload_sha256"]
        == SOURCES["active_v4_manifest"]["payload_sha256"],
        "repaired manifest payload",
    )
    require(
        repair["repaired_row_payload_sha256"]
        == SOURCES["active_v4_row"]["payload_sha256"],
        "repaired row payload",
    )
    require(repair["tangent_verifier_passes"], "tangent verifier replay")
    require(
        repair["tangent_verifier_normal_passes"],
        "tangent verifier normal replay",
    )
    require(
        repair["tangent_verifier_optimized_passes"],
        "tangent verifier optimized replay",
    )

    history, residual = derive_frontier(sources)
    require(
        packet["frontier_synthesis"]["history"] == history,
        "frontier history",
    )
    require(
        packet["frontier_synthesis"]["residual_types"] == residual,
        "residual types",
    )
    require(
        packet["frontier_synthesis"]["degree_identity"] == "delta*r=4*m",
        "degree identity",
    )

    live = derive_live_partition(sources)
    require(packet["active_v4_partition"] == live, "live partition derivation")
    require(live["live_four_cell_partition_present"], "live partition present")
    require(
        not live["transverse_terminal_to_active_cell_mapping_proved"],
        "geometric-to-active mapping must fail closed",
    )

    route = packet["strict_route_compiler"]
    require(
        route["rank"] == {"closed": 0, "m2": 1, "m3": 2, "m6": 2, "m10": 3},
        "route rank",
    )
    rank = route["rank"]
    for source, target in route["strict_edges"]:
        require(rank[target] < rank[source], f"strict route {source}->{target}")
    require(not route["m2_self_recurrence_is_strict"], "m2 recurrence guard")

    conditional = packet["conditional_any69"]
    require(
        conditional["required_adapter_gates"] == REQUIRED_ADAPTER_GATES,
        "adapter gates",
    )
    require(
        conditional["same_record_key"] == SAME_RECORD_KEY,
        "same-record key",
    )
    require(
        conditional["current_gate_values"]
        == {gate: False for gate in REQUIRED_ADAPTER_GATES},
        "current gate values",
    )
    require(conditional["currently_resolved_types"] == [], "resolved types")
    require(not conditional["cap68_currently_proved"], "current cap68")
    require(
        conditional["cap68_if_all_gates_and_types_close"],
        "conditional cap68 implication",
    )
    require(
        conditional["statement_status"] == "CONDITIONAL_ONLY",
        "conditional status",
    )

    require(packet["deployed_dihedral_route_cut"] == derive_route_cut(),
            "dihedral route cut")
    require(
        packet["live_arithmetic"] == derive_live_arithmetic(),
        "live exact arithmetic",
    )
    require(
        packet["historical_abstract_calibration"]
        == derive_historical_calibration(),
        "historical non-load-bearing calibration",
    )
    require(
        packet["historical_provenance"]["commit"]
        == HISTORICAL_PROVENANCE_HEAD,
        "historical provenance commit",
    )
    require(
        not packet["historical_provenance"]["authority"],
        "historical artifact is not authority",
    )
    require(
        packet["proof_status"]["verdict"]
        == "YELLOW_ROUTE_CUT_GLOBAL_K3_OPEN",
        "verdict",
    )
    require(
        "q1 and q2 have complete reduced two-point fibres on D"
        in packet["proof_status"]["proved"],
        "quadratic-fibre proof status",
    )
    require(
        "u^(-1)(0)=D is a complete reduced degree-N fibre"
        in packet["proof_status"]["proved"],
        "zero-fibre proof status",
    )
    require(not packet["proof_status"]["global_K3_closed"], "K3 remains open")
    require(not packet["proof_status"]["KoalaBear_row_closed"], "row remains open")


def mutation_cases() -> list[tuple[str, Callable[[dict[str, Any]], None]]]:
    cases: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        (
            "base_head",
            lambda x: x["base_repository"].__setitem__("head", "0" * 40),
        ),
        (
            "frontier_count",
            lambda x: x["frontier_synthesis"]["history"][-1].__setitem__(
                "count", 1
            ),
        ),
        (
            "residual_type",
            lambda x: x["frontier_synthesis"]["residual_types"].pop(),
        ),
        (
            "route_rank",
            lambda x: x["strict_route_compiler"]["rank"].__setitem__("m2", 2),
        ),
        (
            "m2_self_route",
            lambda x: x["strict_route_compiler"].__setitem__(
                "m2_self_recurrence_is_strict", True
            ),
        ),
        (
            "field_prime",
            lambda x: x["deployed_dihedral_route_cut"].__setitem__(
                "field_prime", 2_130_706_431
            ),
        ),
        (
            "carrier_generator",
            lambda x: x["deployed_dihedral_route_cut"].__setitem__(
                "carrier_generator", 1_213_133_210
            ),
        ),
        (
            "tau1_fixed_point",
            lambda x: x["deployed_dihedral_route_cut"].__setitem__(
                "tau1_fixed_point_free_on_D", False
            ),
        ),
        (
            "fixed_field",
            lambda x: x["deployed_dihedral_route_cut"].__setitem__(
                "fixed_field_intersection_proved", False
            ),
        ),
        (
            "q1_formula",
            lambda x: x["deployed_dihedral_route_cut"][
                "quadratic_quotient_fibres"
            ][0].__setitem__("formula", "q1(x)=x"),
        ),
        (
            "q1_name",
            lambda x: x["deployed_dihedral_route_cut"][
                "quadratic_quotient_fibres"
            ][0].__setitem__("name", "false"),
        ),
        (
            "q1_involution",
            lambda x: x["deployed_dihedral_route_cut"][
                "quadratic_quotient_fibres"
            ][0].__setitem__("involution", "false"),
        ),
        (
            "q1_coefficient_label",
            lambda x: x["deployed_dihedral_route_cut"][
                "quadratic_quotient_fibres"
            ][0].__setitem__("coefficient", "false"),
        ),
        (
            "q1_coefficient",
            lambda x: x["deployed_dihedral_route_cut"][
                "quadratic_quotient_fibres"
            ][0].__setitem__("coefficient_value", 1),
        ),
        (
            "q1_fibre_difference_formula",
            lambda x: x["deployed_dihedral_route_cut"][
                "quadratic_quotient_fibres"
            ][0].__setitem__("fibre_difference_formula", "false"),
        ),
        (
            "q1_degree",
            lambda x: x["deployed_dihedral_route_cut"][
                "quadratic_quotient_fibres"
            ][0].__setitem__("rational_map_degree", 1),
        ),
        (
            "q1_preserves_D",
            lambda x: x["deployed_dihedral_route_cut"][
                "quadratic_quotient_fibres"
            ][0].__setitem__("preserves_D", False),
        ),
        (
            "q1_complete_fibre_formula",
            lambda x: x["deployed_dihedral_route_cut"][
                "quadratic_quotient_fibres"
            ][0].__setitem__("complete_D_fibre_formula", "false"),
        ),
        (
            "q1_fibre_complete",
            lambda x: x["deployed_dihedral_route_cut"][
                "quadratic_quotient_fibres"
            ][0].__setitem__("D_fibre_complete", False),
        ),
        (
            "q1_fibre_reduced",
            lambda x: x["deployed_dihedral_route_cut"][
                "quadratic_quotient_fibres"
            ][0].__setitem__("D_fibre_reduced", False),
        ),
        (
            "q1_fibre_cardinality",
            lambda x: x["deployed_dihedral_route_cut"][
                "quadratic_quotient_fibres"
            ][0].__setitem__("D_fibre_cardinality", 1),
        ),
        (
            "q2_formula",
            lambda x: x["deployed_dihedral_route_cut"][
                "quadratic_quotient_fibres"
            ][1].__setitem__("formula", "q2(x)=x"),
        ),
        (
            "q2_name",
            lambda x: x["deployed_dihedral_route_cut"][
                "quadratic_quotient_fibres"
            ][1].__setitem__("name", "false"),
        ),
        (
            "q2_involution",
            lambda x: x["deployed_dihedral_route_cut"][
                "quadratic_quotient_fibres"
            ][1].__setitem__("involution", "false"),
        ),
        (
            "q2_coefficient_label",
            lambda x: x["deployed_dihedral_route_cut"][
                "quadratic_quotient_fibres"
            ][1].__setitem__("coefficient", "false"),
        ),
        (
            "q2_coefficient",
            lambda x: x["deployed_dihedral_route_cut"][
                "quadratic_quotient_fibres"
            ][1].__setitem__("coefficient_value", 1),
        ),
        (
            "q2_fibre_difference_formula",
            lambda x: x["deployed_dihedral_route_cut"][
                "quadratic_quotient_fibres"
            ][1].__setitem__("fibre_difference_formula", "false"),
        ),
        (
            "q2_degree",
            lambda x: x["deployed_dihedral_route_cut"][
                "quadratic_quotient_fibres"
            ][1].__setitem__("rational_map_degree", 1),
        ),
        (
            "q2_preserves_D",
            lambda x: x["deployed_dihedral_route_cut"][
                "quadratic_quotient_fibres"
            ][1].__setitem__("preserves_D", False),
        ),
        (
            "q2_complete_fibre_formula",
            lambda x: x["deployed_dihedral_route_cut"][
                "quadratic_quotient_fibres"
            ][1].__setitem__("complete_D_fibre_formula", "false"),
        ),
        (
            "q2_fibre_complete",
            lambda x: x["deployed_dihedral_route_cut"][
                "quadratic_quotient_fibres"
            ][1].__setitem__("D_fibre_complete", False),
        ),
        (
            "q2_fibre_reduced",
            lambda x: x["deployed_dihedral_route_cut"][
                "quadratic_quotient_fibres"
            ][1].__setitem__("D_fibre_reduced", False),
        ),
        (
            "q2_fibre_cardinality",
            lambda x: x["deployed_dihedral_route_cut"][
                "quadratic_quotient_fibres"
            ][1].__setitem__("D_fibre_cardinality", 1),
        ),
        (
            "u_zero_fibre_equation",
            lambda x: x["deployed_dihedral_route_cut"][
                "common_invariant_zero_fibre"
            ].__setitem__("equation", "false"),
        ),
        (
            "u_zero_fibre_polynomial",
            lambda x: x["deployed_dihedral_route_cut"][
                "common_invariant_zero_fibre"
            ].__setitem__("defining_polynomial", "x-1"),
        ),
        (
            "u_zero_fibre_cardinality",
            lambda x: x["deployed_dihedral_route_cut"][
                "common_invariant_zero_fibre"
            ].__setitem__("cardinality", 1),
        ),
        (
            "u_zero_fibre_degree",
            lambda x: x["deployed_dihedral_route_cut"][
                "common_invariant_zero_fibre"
            ].__setitem__("fibre_degree", 1),
        ),
        (
            "u_zero_fibre_complete",
            lambda x: x["deployed_dihedral_route_cut"][
                "common_invariant_zero_fibre"
            ].__setitem__("complete", False),
        ),
        (
            "u_zero_fibre_reduced",
            lambda x: x["deployed_dihedral_route_cut"][
                "common_invariant_zero_fibre"
            ].__setitem__("reduced", False),
        ),
        (
            "u_zero_fibre_separability",
            lambda x: x["deployed_dihedral_route_cut"][
                "common_invariant_zero_fibre"
            ].__setitem__("separability", "false"),
        ),
        (
            "u_pole_support",
            lambda x: x["deployed_dihedral_route_cut"][
                "common_invariant_zero_fibre"
            ].__setitem__("pole_support", ["0"]),
        ),
        (
            "u_zero_pole_order",
            lambda x: x["deployed_dihedral_route_cut"][
                "common_invariant_zero_fibre"
            ]["pole_orders"].__setitem__("0", 1),
        ),
        (
            "u_infinity_pole_order",
            lambda x: x["deployed_dihedral_route_cut"][
                "common_invariant_zero_fibre"
            ]["pole_orders"].__setitem__("infinity", 1),
        ),
        (
            "u_pole_divisor_degree",
            lambda x: x["deployed_dihedral_route_cut"][
                "common_invariant_zero_fibre"
            ].__setitem__("pole_divisor_degree", 1),
        ),
        (
            "quadratic_fibre_proof_status",
            lambda x: x["proof_status"]["proved"].remove(
                "q1 and q2 have complete reduced two-point fibres on D"
            ),
        ),
        (
            "zero_fibre_proof_status",
            lambda x: x["proof_status"]["proved"].remove(
                "u^(-1)(0)=D is a complete reduced degree-N fibre"
            ),
        ),
        (
            "live_partition",
            lambda x: x["active_v4_partition"].__setitem__(
                "live_four_cell_partition_present", False
            ),
        ),
        (
            "resolved_type",
            lambda x: x["conditional_any69"]["currently_resolved_types"].append(
                [2, 4, 2]
            ),
        ),
        (
            "invented_gate",
            lambda x: x["conditional_any69"]["current_gate_values"].__setitem__(
                "semantic_complete_selector", True
            ),
        ),
        (
            "invented_cap",
            lambda x: x["conditional_any69"].__setitem__(
                "cap68_currently_proved", True
            ),
        ),
        (
            "ledger_movement",
            lambda x: x["live_arithmetic"].__setitem__("ledger_movement", 1),
        ),
        (
            "historical_authority",
            lambda x: x["historical_provenance"].__setitem__("authority", True),
        ),
        (
            "packet_file_hash",
            lambda x: x["packet_files"][0].__setitem__("sha256", "0" * 64),
        ),
        (
            "active_v4_repair_blob",
            lambda x: x["active_v4_repair"].__setitem__(
                "current_grande_finale_blob_oid", "0" * 40
            ),
        ),
        (
            "active_v4_repair_blob_gate",
            lambda x: x["active_v4_repair"].__setitem__(
                "current_grande_finale_blob_gate", "false"
            ),
        ),
        (
            "tangent_normal_replay",
            lambda x: x["active_v4_repair"].__setitem__(
                "tangent_verifier_normal_passes", False
            ),
        ),
        (
            "tangent_optimized_replay",
            lambda x: x["active_v4_repair"].__setitem__(
                "tangent_verifier_optimized_passes", False
            ),
        ),
    ]
    for index, binding_id in enumerate(SOURCES):
        cases.append(
            (
                f"payload_pin_{binding_id}",
                lambda x, i=index: x["source_bindings"][i].__setitem__(
                    "payload_sha256", "0" * 64
                ),
            )
        )
    return cases


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument("--emit-derived", action="store_true")
    args = parser.parse_args()

    replay_tangent_verifier()
    sources = load_sources()
    packet = parse_json(CERTIFICATE.read_text(), str(CERTIFICATE))
    validate_packet(packet, sources)

    rejected = 0
    if args.tamper_selftest:
        for name, mutate in mutation_cases():
            damaged = copy.deepcopy(packet)
            mutate(damaged)
            damaged["payload_sha256"] = payload_hash(damaged)
            try:
                validate_packet(damaged, sources)
            except VerificationError:
                rejected += 1
            else:
                raise VerificationError(f"mutation accepted: {name}")
        require(rejected == len(mutation_cases()), "mutation count")

    if args.emit_derived:
        print(
            json.dumps(
                {
                    "frontier_synthesis": {
                        "history": derive_frontier(sources)[0],
                        "residual_types": derive_frontier(sources)[1],
                    },
                    "active_v4_partition": derive_live_partition(sources),
                    "deployed_dihedral_route_cut": derive_route_cut(),
                    "live_arithmetic": derive_live_arithmetic(),
                    "historical_abstract_calibration": (
                        derive_historical_calibration()
                    ),
                },
                indent=2,
                sort_keys=True,
            )
        )
    else:
        print(
            "PASS "
            "frontier=26>22>18>12>8>3>2 "
            "residual=[[2,4,2],[2,8,1]] "
            "live_partition=FOUR_CELL_PRESENT "
            "dihedral_order=2097152 "
            "quadratic_fibres=COMPLETE_REDUCED_2 "
            "u_zero_fibre=COMPLETE_REDUCED_2097152 "
            "terminal=UNPAID_TWO_TRANSVERSE_TYPES_AND_SEMANTIC_ADAPTER "
            f"tamper_rejected={rejected}"
        )


if __name__ == "__main__":
    main()
