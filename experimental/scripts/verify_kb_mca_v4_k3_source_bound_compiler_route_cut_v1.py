#!/usr/bin/env python3
"""Verify the exact K3 source-bound compiler route-cut packet.

This packet deliberately fails closed.  It imports the proved raw
``433-1b -> O0a`` exclusion, reconstructs the thirteen-route raw workboard
and the exact local orientation censuses, and then checks that no
raw-system result is substituted for a distinct-affine-slope payment.  The
first missing implication is the declared active ``m=2,r=4`` residual-slice
parameter-to-carrier bridge.  Membership in that slice and reduction of all
``Z_BC`` to it are not asserted.  Consequently none of U_remaining,
U_positive, U_sourcecover, U_K3, U_K3_allocation, or the signed slack is
assigned a value.

The executable proves exact arithmetic, combinatorial censuses, source
bindings, and fail-closed composition contracts.  The mathematical transport
invariants are stated and proved in the companion note; this script replays
their finite data.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable, Iterable


sys.set_int_max_str_digits(2_500_000)

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = "rs-mca-kb-v4-k3-source-bound-compiler-route-cut-v1"
STATUS = "PROVED_FAIL_CLOSED_K3_ROUTE_CUT_WITH_STALE_UPSTREAM_SOURCE_GATE"
TERMINAL = "UNPAID_PARAMETER_TO_CARRIER_AND_LABELS_TO_SLOPES"
ARCHITECTURE = "GRANDE_FINALE_V4_KB_MCA_TANGENT_SOURCE_ADAPTER_V1"
PARTITION_SHA256 = "4fade91abc408264989babcff6f8f9bbd80bcec52545a5db15ac376bf17d88fc"
UNIT = "DISTINCT_BAD_FINITE_SLOPES_PER_RECEIVED_LINE"
QUANTIFIER = "UNIFORM_OVER_ALL_ADMISSIBLE_RECEIVED_LINES"
ACTIVE_SLICE = "DECLARED_ACTIVE_V4_BALANCED_CORE_M2_R4_RESIDUAL_SLICE"
EXPECTED_ACTIVE_V4_BLOB = "8a5d9791900ca9eed773feba146b92ad296704ce"
OBSERVED_ACTIVE_V4_BLOB = "6b21d6ea937a8a9f85fc7ade6032d73efd4c7222"
EXPECTED_STEERING_BLOB = "30d8b9f1b4caa3c7504fe3d24fc7ce8da84de434"
OBSERVED_PR1152_STEERING_BLOB = "75a01e4b6cfc17c34112a47bd51294519ebc687c"
TRANSPORT_CLASS_ID = (
    "DECLARED_NATURAL_RECORD_ROLE_GAUGE_AND_TYPED_INCIDENCE_RELABELINGS"
)
TRANSPORT_GENERATORS = (
    "TARGET_VERTEX_GAUGE_APPLIED_UNIFORMLY_TO_PARALLEL_RECORDS",
    "INTERCHANGE_OF_THE_TWO_PARALLEL_BC_RECORDS",
    "SWAP_OF_B_AND_C_ROLES",
    "SOURCE_ROOT_SIGN_OR_DECK_RELABELINGS_DECLARED_BY_THE_PINNED_ATLASES",
    "TYPED_OUTSIDE_ROLE_PERMUTATIONS_PRESERVING_DISPLAYED_INCIDENCE_DATA",
)

P = 2_130_706_433
N = 2_097_152
K = 1_048_576
AGREEMENT = 1_116_048
B_STAR = 274_980_728_111_395_087
U_PAID = 981_104
JOINT_UNPAID_RESERVE = B_STAR - U_PAID

PUBLIC_DAG_COMMIT = "48a7de3c2d0d092b1899b1bb18d62bb4bf8861ce"
RAW_DAG_COMMIT = "8df0903391a228eed6e24398fca9d40d72d546cf"
PR1152_HEAD = "ed4877cce5f227f33311fa93f5ff5e5f4150ae63"
PR1155_HEAD = "1cf13bb4058da19c5108bf79472394a598217bca"

CERT_REL = Path(
    "experimental/data/certificates/"
    "kb-mca-v4-k3-source-bound-compiler-route-cut-v1/manifest.json"
)
ROW_REL = Path(
    "experimental/data/certificates/"
    "kb-mca-v4-tangent-source-adapter-v1/row_manifest.json"
)
TANGENT_REL = Path(
    "experimental/data/certificates/"
    "kb-mca-v4-tangent-source-adapter-v1/manifest.json"
)
RAW_REL = Path(
    "experimental/data/certificates/"
    "kb-mca-v4-433-1b-raw-workboard-close-v1/"
    "kb_mca_v4_433_1b_raw_workboard_close_v1.json"
)
RAW_VERIFY_REL = Path(
    "experimental/data/certificates/"
    "kb-mca-v4-433-1b-raw-workboard-close-v1/verify.py"
)
ACTIVE_V4_REL = Path("experimental/grande_finale.tex")

LOCAL_BINDINGS = {
    str(ROW_REL): "574c6fd6d3a993260e2dc947235a92a56189e4197c069c3ff24b962944dda5c1",
    str(TANGENT_REL): "943f62b5ebf5e5bc638067a7b47a3b7f7cb1d53a7d2b647b2178b764a976b964",
    str(RAW_REL): "289f542e2e8420fca4c04ad66cf01e763d82a63cf86686bf496cb8228ac750d6",
    str(RAW_VERIFY_REL): "a6cc773757339c5adf1c2004a33ebe96a2dfc6ec4d2e58e457ff7f849d465668",
    str(ACTIVE_V4_REL): "336ba3c9a6d9483d0eab74677d6224aae23adf15d84891c6099f6d2f45cf226d",
}

PUBLIC_DAG_BINDINGS = {
    "background/nodes/rate_half_kb_decomposition_source_pencil_compiler/statement.md":
        "54b2879737b8d9f381678e35f18460ed51f092a7c2ab808aea9bf6ea9454b776",
    "background/nodes/rate_half_kb_source_pencil_rank_transverse_compiler/statement.md":
        "0c1756ccf94e7b4503bf7b9aa5a39cebf16abaf1a200ec9496dd8bcf6b6f664f",
    "background/nodes/rate_half_kb_m2_r4_coordinate_positive_residual_loop_workboard/statement.md":
        "fdfe52363a1b143279e426080c8a7cf9dd79623f21f1f69f371b6794d15fef7a",
    "background/nodes/rate_half_kb_m2_r4_coordinate_positive_remaining_route_payment/statement.md":
        "b2d6c15247f6b0a4b4fbae70615a7266205ffb96c9cf0914a655fbe9c10a6a27",
    "background/nodes/rate_half_kb_m2_r4_k3_orientation_assembly/statement.md":
        "52ada0417abf74fc4709bc635520ed3064d67cf7c9fbd017dc6a45f474e7ff1e",
    "background/nodes/rate_half_kb_m2_r4_k3_allocation_inequality/statement.md":
        "dd41d5e3075e8eb3e75ad792bddaeb28b5615b50d66202c5a83078a789008d1b",
    "background/nodes/rate_half_kb_m2_r4_diagonal_source_subfield_dichotomy/statement.md":
        "8c56c6b461949bb1ec34703233cf4e952179b9248899dbb39ee2c76c4f04e11b",
    "background/nodes/rate_half_kb_m2_r4_diagonal_facet_mixing_obstruction/statement.md":
        "4ed39ffaaf859355bcd6406a9bc83aeb7a1aeb334da5f3d78e59a791118052ff",
    "background/nodes/rate_half_kb_m2_r4_coordinate_positive_433_1b_o0a_signed_edge_atlas/statement.md":
        "62ea6520db4f1a0144e343ff80efe1adf85121738b163ac20a2be805a87fe204",
    "background/nodes/rate_half_kb_m2_r4_coordinate_positive_433_1b_o0b_signed_edge_atlas/statement.md":
        "1e62ce887dbe2ebb57e8219536454af8683142dee820997a71f070a79ac637fc",
    "background/nodes/rate_half_kb_m2_r4_coordinate_positive_433_1b_o0b_residual_owner_partition/statement.md":
        "a01d451b19f2c09987a5b88102edb1a39eb6e2402fe8530bce996494a7fdcaac",
    "notes/codex_briefs/WAVE57_K3_ROUND30_HANDOFF_20260810.md":
        "53a137f13db20ca21102910a44a0d4b24f4ae97203b883f52d76dc2c92bdbdbc",
    "notes/codex_briefs/URGENT_M1_SCOPE_HAZARD_20260810.md":
        "d2513e03b3f2ec3b8d44c30798273e67b83cf36063d9fcce385d3fab310d8888",
    "notes/pilots_20260810/k3_orientation_assembly/replay_orientation_images.py":
        "c99d76452860e995f89a2bb691748890be5ca78a9214c56671895bfa2129fe5a",
    "notes/pilots_20260810/k3_splitbc_transport/label_orbits.py":
        "3146e60b7f28817f914862e7b141fc34ac5953408558772359b1d6d75cb1317e",
}

PR1155_BINDINGS = {
    "experimental/data/certificates/kb-mca-v4-433-1b-cell11-signed-pair-route-cut-v1/raw.json":
        "74c2a601542b12cf236aa60519e486a361fbe3326dca62455e460da6ce710e76",
    "experimental/scripts/verify_kb_mca_v4_433_1b_cell11_signed_pair_route_cut_v1.py":
        "ae0450c34c6d5776bc2f2af2898f9dfb5076b3ade4711b278df9a2d8fae9567d",
    "experimental/notes/thresholds/kb_mca_v4_433_1b_cell11_signed_pair_route_cut_v1.md":
        "1b91a9e3a6f6ce4f1acb67df0afe0ac8cc75aa94f7ffea0e5298a6a05be1870d",
}

COMMON = {
    "442-0a": {"defect": 2, "loops": 0},
    "442-1b": {"defect": 1, "loops": 1},
    "433-0": {"defect": 0, "loops": 0},
    "433-1a": {"defect": 3, "loops": 1},
    "433-1b": {"defect": 1, "loops": 1},
}
OUTSIDE = {
    "O0a": {"defect": 2, "loops": 0},
    "O0b": {"defect": 0, "loops": 0},
    "O1a": {"defect": 5, "loops": 1},
    "O1b": {"defect": 1, "loops": 1},
    "O1c": {"defect": 3, "loops": 1},
    "O1d": {"defect": 1, "loops": 1},
}
CLOSED_ROUTES = {("433-1a", "O0b"), ("433-1b", "O0a")}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in out, f"duplicate JSON key: {key}")
        out[key] = value
    return out


def reject_noninteger(token: str) -> Any:
    raise AssertionError(f"noninteger/nonstandard JSON number: {token}")


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(),
        object_pairs_hook=strict_object,
        parse_float=reject_noninteger,
        parse_constant=reject_noninteger,
    )
    require(isinstance(value, dict), f"JSON root is not an object: {path}")
    return value


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def payload_digest(value: dict[str, Any]) -> str:
    payload = copy.deepcopy(value)
    payload.pop("payload_sha256", None)
    return hashlib.sha256(canonical_bytes(payload)).hexdigest()


def seal(value: dict[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(value)
    value["payload_sha256"] = payload_digest(value)
    return value


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob(root: Path, commit: str, path: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(root), "show", f"{commit}:{path}"],
        check=True,
        stdout=subprocess.PIPE,
    ).stdout


def git_blob_id(root: Path, commit: str, path: str) -> str:
    return subprocess.run(
        ["git", "-C", str(root), "rev-parse", f"{commit}:{path}"],
        check=True,
        stdout=subprocess.PIPE,
        text=True,
    ).stdout.strip()


def verify_blob_bindings(root: Path, commit: str, bindings: dict[str, str]) -> int:
    for path, expected in bindings.items():
        got = hashlib.sha256(git_blob(root, commit, path)).hexdigest()
        require(got == expected, f"source digest mismatch: {path}")
    return len(bindings)


def derive_routes() -> list[dict[str, Any]]:
    routes: list[dict[str, Any]] = []
    for common in sorted(COMMON):
        for outside in sorted(OUTSIDE):
            c = COMMON[common]
            o = OUTSIDE[outside]
            if c["defect"] + o["defect"] > 3:
                continue
            if c["loops"] > 0 and o["loops"] > 0:
                continue
            closed = (common, outside) in CLOSED_ROUTES
            routes.append(
                {
                    "route": f"{common} -> {outside}",
                    "common": common,
                    "outside": outside,
                    "total_defect": c["defect"] + o["defect"],
                    "common_loops": c["loops"],
                    "outside_loops": o["loops"],
                    "status": "PROVED_EMPTY_RAW_SYSTEMS" if closed else "TARGET_RAW_WORKBOARD_ROUTE_NO_SLOPE_PAYMENT",
                    "surviving_raw_systems": 0 if closed else None,
                    "distinct_affine_slope_payment": None,
                }
            )
    return routes


def fpf_involutions(labels: tuple[int, ...]) -> Iterable[dict[int, int]]:
    if not labels:
        yield {}
        return
    head, rest = labels[0], labels[1:]
    for index, partner in enumerate(rest):
        tail = rest[:index] + rest[index + 1 :]
        for sub in fpf_involutions(tail):
            tau = dict(sub)
            tau[head] = partner
            tau[partner] = head
            yield tau


def diagonal_involution_census() -> dict[str, Any]:
    labels = tuple(range(12))
    I = set(range(6))
    J = set(range(6, 12))
    K0 = set(range(5))
    xi = 5
    rows: dict[tuple[int, int, int], int] = {}
    total = 0
    deleted = 0
    for tau in fpf_involutions(labels):
        total += 1
        tau_i = {tau[x] for x in I}
        if tau_i == I:
            deleted += 1
            continue
        tau_j = {tau[x] for x in J}
        c = len(I & tau_j)
        require(c == len(J & tau_i), "diagonal crossing count")
        a = sum(1 for k in K0 if tau[k] in K0 and tau[k] > k)
        b = int(tau[xi] in K0)
        rows[(a, b, c)] = rows.get((a, b, c), 0) + 1
    return {
        "all_fixed_point_free_involutions": total,
        "partition_preserving_deleted": deleted,
        "live_total": total - deleted,
        "rows": [
            {"a": key[0], "b": key[1], "c": key[2], "multiplicity": rows[key]}
            for key in sorted(rows)
        ],
    }


def perfect_matchings(items: tuple[int, ...]) -> list[frozenset[frozenset[int]]]:
    if not items:
        return [frozenset()]
    first = items[0]
    out: list[frozenset[frozenset[int]]] = []
    for index in range(1, len(items)):
        pair = frozenset((first, items[index]))
        rest = items[1:index] + items[index + 1 :]
        for matching in perfect_matchings(rest):
            out.append(matching | {pair})
    return out


Label = tuple[int, frozenset[frozenset[int]]]


def outside_labels() -> list[Label]:
    labels: list[Label] = []
    for missing in range(7):
        rest = tuple(x for x in range(7) if x != missing)
        for matching in perfect_matchings(rest):
            labels.append((missing, matching))
    return labels


def permutation(cycles: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
    out = list(range(7))
    for cycle in cycles:
        for index, item in enumerate(cycle):
            out[item] = cycle[(index + 1) % len(cycle)]
    return tuple(out)


def act_on_label(perm: tuple[int, ...], label: Label) -> Label:
    missing, matching = label
    image = frozenset(frozenset(perm[x] for x in pair) for pair in matching)
    return perm[missing], image


def label_orbits(generators: list[tuple[int, ...]], universe: list[Label]) -> dict[str, Any]:
    seen: set[Label] = set()
    profile: dict[int, int] = {}
    orbit_count = 0
    for label in universe:
        if label in seen:
            continue
        component = {label}
        stack = [label]
        while stack:
            current = stack.pop()
            for generator in generators:
                image = act_on_label(generator, current)
                if image not in component:
                    component.add(image)
                    stack.append(image)
        seen |= component
        profile[len(component)] = profile.get(len(component), 0) + 1
        orbit_count += 1
    require(len(seen) == len(universe), "label orbit coverage")
    return {
        "orbits": orbit_count,
        "profile": {str(size): profile[size] for size in sorted(profile)},
        "weighted_total": sum(size * count for size, count in profile.items()),
    }


def label_orbit_census() -> dict[str, Any]:
    labels = outside_labels()
    require(len(labels) == 105 and len(set(labels)) == 105, "105-label universe")
    cases = {
        "o0b_d_sign": [permutation(((2, 3), (4, 5)))],
        "o0a_universal": [permutation(((0, 1),)), permutation(((3, 4),))],
        "o0b_identical_pair": [permutation(((2, 3),))],
        "o0b_s0_role": [permutation(((0, 1), (2, 4), (3, 5)))],
        "o0b_s0_both": [
            permutation(((0, 1), (2, 4), (3, 5))),
            permutation(((2, 3), (4, 5))),
        ],
    }
    return {name: label_orbits(generators, labels) for name, generators in cases.items()}


def split_signature_permutation_audit() -> dict[str, Any]:
    # Diagonal entries are outside half-edge counts r_i; off-diagonal entries
    # are the three pair multiplicities m_ij.
    o0a = ((0, 3, 1), (3, 0, 1), (1, 1, 2))
    o0b = ((0, 2, 2), (2, 1, 1), (2, 1, 1))
    matches = 0
    for perm in itertools.permutations(range(3)):
        image = tuple(tuple(o0b[perm[i]][perm[j]] for j in range(3)) for i in range(3))
        matches += int(image == o0a)
    return {
        "o0a_signature": [[0, 0, 2], [1, 1, 3]],
        "o0b_signature": [[0, 1, 1], [1, 2, 2]],
        "permutations_checked": 6,
        "isomorphisms": matches,
    }


def source_bindings() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path, digest in sorted(LOCAL_BINDINGS.items()):
        rows.append(
            {
                "repo": "przchojecki/rs-mca",
                "commit": PR1152_HEAD,
                "path": path,
                "sha256": digest,
                "kind": "LOCAL_BLOB_SHA256",
            }
        )
    for path, digest in sorted(PUBLIC_DAG_BINDINGS.items()):
        rows.append(
            {
                "repo": "AllenGrahamHart/rs-mca-prize-dag",
                "commit": PUBLIC_DAG_COMMIT,
                "path": path,
                "sha256": digest,
                "kind": "GIT_BLOB_CONTENT_SHA256",
            }
        )
    for path, digest in sorted(PR1155_BINDINGS.items()):
        rows.append(
            {
                "repo": "przchojecki/rs-mca",
                "commit": PR1155_HEAD,
                "path": path,
                "sha256": digest,
                "kind": "GIT_BLOB_CONTENT_SHA256",
            }
        )
    return rows


def build_certificate() -> dict[str, Any]:
    routes = derive_routes()
    remaining = [
        row["route"]
        for row in routes
        if row["status"] == "TARGET_RAW_WORKBOARD_ROUTE_NO_SLOPE_PAYMENT"
    ]
    diagonal = diagonal_involution_census()
    labels = label_orbit_census()
    split_signature = split_signature_permutation_audit()
    cert: dict[str, Any] = {
        "schema": SCHEMA,
        "status": STATUS,
        "terminal": TERMINAL,
        "theorem_kind": "MAXIMAL_ROUTE_CUT_NOT_A_K3_PAYMENT",
        "active_contract": {
            "architecture_id": ARCHITECTURE,
            "partition_sha256": PARTITION_SHA256,
            "owner": "ACTIVE_V4_BALANCED_CORE",
            "owner_priority": 2,
            "first_match": True,
            "unit": UNIT,
            "quantifier": QUANTIFIER,
            "row": {
                "base_prime": P,
                "extension_degree": 6,
                "n": N,
                "k": K,
                "agreement": AGREEMENT,
                "B_star": B_STAR,
            },
            "contract_scope": "DECLARED_TARGET_CONTRACT_WITH_STALE_TRANSITIVE_PROOF_SOURCE",
        },
        "tangent_import_source_gate": {
            "atom": "U_paid",
            "manifest_declared_value": U_PAID,
            "manifest_declared_proof_status": "PROVED_GATE_B_BANKABLE_ATOM_ROW_OPEN",
            "expected_active_v4_git_blob": EXPECTED_ACTIVE_V4_BLOB,
            "observed_pr1152_active_v4_git_blob": OBSERVED_ACTIVE_V4_BLOB,
            "source_binding_matches": False,
            "expected_steering_git_blob": EXPECTED_STEERING_BLOB,
            "observed_pr1152_steering_git_blob": OBSERVED_PR1152_STEERING_BLOB,
            "steering_binding_matches": False,
            "steering_drift_is_gating": False,
            "transitive_source_revalidated": False,
            "classification": "STALE_TRANSITIVE_SOURCE_BINDING_NOT_A_REVALIDATED_PAYMENT",
        },
        "imported_raw_dependency": {
            "route": "433-1b -> O0a",
            "public_dag_commit": RAW_DAG_COMMIT,
            "status": "PROVED_EMPTY_RAW_SYSTEMS",
            "role_cells": 15,
            "raw_labels": 1_575,
            "signed_principal_systems": 25_200,
            "surviving_raw_systems": 0,
            "ledger_movement": 0,
            "active_partition_bridge_proved": False,
        },
        "compiler_contract": {
            "domain": ACTIVE_SLICE,
            "domain_is_all_Z_BC": False,
            "slice_membership_predicate_proved": False,
            "slice_exhaustive_within_Z_BC": False,
            "requested_partition": ["source-line", "coordinate", "source-cover"],
            "inverse_must_preserve": [
                "received_line",
                "reconstructed_support",
                "affine_slope",
                "first_match_owner",
                "add_back_chronology",
            ],
            "parameter_line_is_evaluation_carrier": False,
            "single_valued_source_to_component_map_proved": False,
            "inverse_reconstruction_map_proved": False,
            "exhaustive_partition_proved": False,
        },
        "frozen_equations": {
            "active_first_match": [
                "Z_paid = Z intersect T",
                "R1 = Z setminus Z_paid",
                "Z_Q = R1 intersect Q",
                "R2 = R1 setminus Z_Q",
                "Z_BC = R2 intersect BC",
                "Z_new = R2 setminus Z_BC",
            ],
            "source_pencil": [
                "V_act in Sym^(60/m)(W)",
                "A_S in W",
                "A_R^5 in W",
            ],
            "active_slice": "Z_BC^(m=2,r=4) is the declared residual slice of Z_BC; a source-bound membership predicate and exhaustive reduction are open",
            "unproved_bridge": "every z in the declared active m=2,r=4 slice admits a total same-record selector/reconstruction into supplied actual endpoint records and actual (4,4) components, preserving every compiler field and carrying an exact projection-fiber bound; a two-sided inverse is a sufficient stronger form",
        },
        "first_failed_bridge": {
            "id": "ACTIVE_M2_R4_SLICE_TO_CARRIER_SELECTOR_RECONSTRUCTION_AND_PROJECTION",
            "status": "UNPROVEN",
            "reason": "the orientation target is scoped to a declared active m=2,r=4 residual slice, while the source-pencil theorem classifies only supplied actual endpoint records and explicitly distinguishes its parameter line from the evaluation carrier",
            "falsifier": "an ill-defined active m=2,r=4 slice, one slope in that slice with no admissible selected component, incompatible selected components without a controlled fiber, or any reconstruction changing line, support, slope, owner, or chronology",
            "effect": "raw labels/systems cannot be charged as distinct affine slopes",
        },
        "orientation_census": {
            "transverse_partitions_per_supplied_actual_record": 32_099,
            "diagonal_involutions": diagonal,
            "source_line_closed_scope": "SATURATED_c2_1_1_2_ONLY",
            "live_unrouted_source_line_rows": [[1, 0, 4], [0, 1, 4], [0, 0, 6]],
            "exceptional_source_line_orbit": "KBDM-10",
            "independent_transverse_type": {"m": 2, "r": 8, "delta": 1, "status": "OUTSIDE_THREE_ORIENTATIONS_OPEN"},
        },
        "source_cover": {
            "terminal_workboard_exists": False,
            "terminal_census": None,
            "U_sourcecover": None,
            "live_diagonal_rows": [[1, 1, 2], [1, 0, 4], [0, 1, 4], [0, 0, 6]],
            "passports_per_row": [
                {"genus": 0, "passport": ["eta", "eta_prime", "mu"]},
                {"genus": 1, "passport": ["eta", "eta", "eta_prime", "eta_prime"]},
            ],
            "unresolved_candidate_row_passport_combinations": 8,
        },
        "coordinate_workboard": {
            "route_count": len(routes),
            "routes": routes,
            "proved_raw_zero_count": len(CLOSED_ROUTES),
            "remaining_route_count": len(remaining),
            "remaining_routes": remaining,
            "U_remaining": None,
        },
        "o0b_native_route_cut": {
            "route": "433-1b -> O0b",
            "transport_scope": {
                "class_id": TRANSPORT_CLASS_ID,
                "generators": list(TRANSPORT_GENERATORS),
                "preserves": [
                    "displayed_parallel_product_equations",
                    "typed_outside_incidence_data",
                    "record_and_role_types",
                ],
                "arbitrary_algebraic_orientation_changing_maps_covered": False,
                "claim": "NO_TRANSPORT_IN_THIS_DECLARED_NATURAL_CLASS",
            },
            "residual_owner_partition": {
                "split_rank5": {"rows": 360, "raw_labels": 37_800},
                "repeated_cells_1_2": {"rows": 16, "raw_labels": 1_680},
                "repeated_cells_11_14": {"rows": 32, "raw_labels": 3_360},
                "total": {"rows": 408, "raw_labels": 42_840},
            },
            "o0a_transport_obstructions": [
                {
                    "branch": "REPEATED_BC",
                    "invariant": "parallel_product_ratio",
                    "o0b_value": 1,
                    "o0a_value_mod_p": P - 1,
                    "guard": {"characteristic_not_2": True, "bc_nonzero": True},
                    "isomorphism_exists": False,
                },
                {
                    "branch": "SPLIT_BC_FULL_SYSTEM",
                    "invariant": "outside_incidence_signature",
                    **split_signature,
                },
            ],
            "outside_label_orbits": labels,
            "split_block_candidate_orbit_audit": {
                "status": "CONDITIONAL_ABSTRACT_LABEL_ORBIT_WORKLOAD_NOT_A_CENSUS_ELIMINATION_OR_PAYMENT",
                "raw_labels": 37_800,
                "unproved_inputs": [
                    "widened-scope O0b S0 d-sign quotient",
                    "SDE-to-SDF lane transport as a banked full-system certificate",
                    "S0 role transport as a banked full-system certificate",
                ],
                "sdf_candidate_term": 0,
                "sde_candidate_term": 2 * 15 * 4 * 60,
                "s0_paired_candidate_term": 2 * 6 * 4 * 57,
                "s0_fixed_candidate_term": 2 * 3 * 4 * 57,
                "conditional_candidate_workload": 11_304,
            },
        },
        "pr1155_reconciliation": {
            "commit": PR1155_HEAD,
            "classification": "VALID_GUARD_TRANSPLANT_ROUTE_CUT_REGRESSION_DEPENDENCY",
            "status": "OPEN_GAP",
            "raw_sha256": "74c2a601542b12cf236aa60519e486a361fbe3326dca62455e460da6ce710e76",
            "mutations_rejected_by_own_verifier": 16,
            "guarded_necessary_point_survives": True,
            "witness": {
                "r": 976_487_466,
                "t": 1_814_604_652,
                "b": 1_722_399_428,
                "c": 463_843_441,
                "w0": 58_144_935,
                "w1": 1_833_131_373,
                "N0": 1_242_524_170,
                "D0": 796_444_780,
            },
            "strategic_effect": "rules out guard-only transplant; does not assign a slope payment and is not superseded by PR1152",
        },
        "exact_ledger_outputs": {
            "U_remaining": None,
            "U_positive": None,
            "U_sourcecover": None,
            "U_K3": None,
            "U_K3_allocation": None,
            "signed_slack": None,
            "inequality_evaluable": False,
            "B_star": B_STAR,
            "U_paid": U_PAID,
            "U_paid_source_status": "MANIFEST_DECLARED_TRANSITIVE_SOURCE_GATE_STALE",
            "joint_Q_BC_new_reserve": JOINT_UNPAID_RESERVE,
            "joint_reserve_status": "ARITHMETIC_FROM_MANIFEST_DECLARATION_NOT_REVALIDATED_PAYMENT",
            "joint_reserve_is_K3_allocation": False,
            "allocation_interval_only": [0, JOINT_UNPAID_RESERVE],
        },
        "conclusion": {
            "success_condition": "B",
            "verdict": "YELLOW_GLOBAL_RED_NATURAL_O0B_TO_O0A_TRANSPORT",
            "route_cut": "the active m=2,r=4 slice/source-bound selector, reconstruction, projection, and unit conversion are unproved; the proposed O0b-to-O0a transport fails within the declared natural map class; the imported tangent atom has a stale transitive source gate",
            "ledger_movement": 0,
            "K3_closed": False,
            "KoalaBear_row_closed": False,
        },
        "nonclaims": [
            "No active balanced-core bad slope is identified with a raw workboard label.",
            "The conditional 11304 abstract-orbit workload is not a census, elimination, or distinct-slope payment.",
            "The manifest-declared U_paid is not source-revalidated by this packet because its active-v4 transitive blob pin is stale.",
            "The joint Q/BC/new reserve is not U_K3_allocation.",
            "The source-cover row-passport strata are not a terminal census.",
            "PR1155 is preserved as a valid route cut, not promoted to a closure.",
            "No K3 or KoalaBear-row ledger value moves.",
        ],
        "source_bindings": source_bindings(),
    }
    return seal(cert)


def verify_certificate(cert: dict[str, Any]) -> None:
    require(cert.get("schema") == SCHEMA, "schema")
    require(cert.get("status") == STATUS, "status")
    require(cert.get("terminal") == TERMINAL, "terminal")
    require(cert.get("payload_sha256") == payload_digest(cert), "payload digest")

    active = cert["active_contract"]
    require(active["architecture_id"] == ARCHITECTURE, "architecture")
    require(active["partition_sha256"] == PARTITION_SHA256, "partition")
    require(active["unit"] == UNIT and active["quantifier"] == QUANTIFIER, "unit/quantifier")
    require(active["owner"] == "ACTIVE_V4_BALANCED_CORE" and active["owner_priority"] == 2, "owner")
    require(active["first_match"] is True, "first-match chronology")
    require(
        active["contract_scope"]
        == "DECLARED_TARGET_CONTRACT_WITH_STALE_TRANSITIVE_PROOF_SOURCE",
        "active contract source scope",
    )
    require(active["row"] == {
        "base_prime": P,
        "extension_degree": 6,
        "n": N,
        "k": K,
        "agreement": AGREEMENT,
        "B_star": B_STAR,
    }, "row")

    tangent_gate = cert["tangent_import_source_gate"]
    require(
        tangent_gate
        == {
            "atom": "U_paid",
            "manifest_declared_value": U_PAID,
            "manifest_declared_proof_status": "PROVED_GATE_B_BANKABLE_ATOM_ROW_OPEN",
            "expected_active_v4_git_blob": EXPECTED_ACTIVE_V4_BLOB,
            "observed_pr1152_active_v4_git_blob": OBSERVED_ACTIVE_V4_BLOB,
            "source_binding_matches": False,
            "expected_steering_git_blob": EXPECTED_STEERING_BLOB,
            "observed_pr1152_steering_git_blob": OBSERVED_PR1152_STEERING_BLOB,
            "steering_binding_matches": False,
            "steering_drift_is_gating": False,
            "transitive_source_revalidated": False,
            "classification": "STALE_TRANSITIVE_SOURCE_BINDING_NOT_A_REVALIDATED_PAYMENT",
        },
        "stale tangent import source gate",
    )

    raw = cert["imported_raw_dependency"]
    require(raw["public_dag_commit"] == RAW_DAG_COMMIT, "raw commit")
    require((raw["role_cells"], raw["raw_labels"], raw["signed_principal_systems"], raw["surviving_raw_systems"]) == (15, 1575, 25200, 0), "raw census")
    require(raw["ledger_movement"] == 0 and not raw["active_partition_bridge_proved"], "raw scope")

    compiler = cert["compiler_contract"]
    require(compiler["domain"] == ACTIVE_SLICE, "active residual slice")
    require(not compiler["domain_is_all_Z_BC"], "must not claim all Z_BC")
    require(
        not compiler["slice_membership_predicate_proved"]
        and not compiler["slice_exhaustive_within_Z_BC"],
        "slice membership/exhaustivity must remain open",
    )
    require(compiler["requested_partition"] == ["source-line", "coordinate", "source-cover"], "orientation partition")
    require(not compiler["parameter_line_is_evaluation_carrier"], "parameter/carrier distinction")
    require(not compiler["single_valued_source_to_component_map_proved"], "source map must remain open")
    require(not compiler["inverse_reconstruction_map_proved"], "inverse must remain open")
    require(not compiler["exhaustive_partition_proved"], "exhaustivity must remain open")
    require(
        cert["first_failed_bridge"]["id"]
        == "ACTIVE_M2_R4_SLICE_TO_CARRIER_SELECTOR_RECONSTRUCTION_AND_PROJECTION"
        and cert["first_failed_bridge"]["status"] == "UNPROVEN",
        "first bridge",
    )

    orientation = cert["orientation_census"]
    require(orientation["transverse_partitions_per_supplied_actual_record"] == 32099, "transverse per-record census")
    require(orientation["diagonal_involutions"] == diagonal_involution_census(), "diagonal census")
    require(orientation["live_unrouted_source_line_rows"] == [[1, 0, 4], [0, 1, 4], [0, 0, 6]], "unrouted source rows")
    require(orientation["independent_transverse_type"] == {"m": 2, "r": 8, "delta": 1, "status": "OUTSIDE_THREE_ORIENTATIONS_OPEN"}, "independent transverse type")

    source_cover = cert["source_cover"]
    require(
        not source_cover["terminal_workboard_exists"]
        and source_cover["terminal_census"] is None,
        "source-cover object",
    )
    require(
        source_cover["U_sourcecover"] is None
        and source_cover["unresolved_candidate_row_passport_combinations"] == 8,
        "source-cover output",
    )

    board = cert["coordinate_workboard"]
    require(board["routes"] == derive_routes(), "route derivation")
    require(board["route_count"] == 13 and board["proved_raw_zero_count"] == 2, "route counts")
    require(board["remaining_route_count"] == 11 and len(board["remaining_routes"]) == 11, "remaining route count")
    require(board["U_remaining"] is None, "U_remaining must remain undefined")
    raw_zero_rows = [row for row in board["routes"] if row["status"] == "PROVED_EMPTY_RAW_SYSTEMS"]
    open_rows = [row for row in board["routes"] if row["status"] == "TARGET_RAW_WORKBOARD_ROUTE_NO_SLOPE_PAYMENT"]
    require(
        len(raw_zero_rows) == 2
        and all(row["surviving_raw_systems"] == 0 for row in raw_zero_rows),
        "raw-zero survivor semantics",
    )
    require(
        len(open_rows) == 11
        and all(row["surviving_raw_systems"] is None for row in open_rows),
        "open raw-route semantics",
    )
    require(
        all(row["distinct_affine_slope_payment"] is None for row in board["routes"]),
        "no raw route is a slope payment",
    )

    o0b = cert["o0b_native_route_cut"]
    transport_scope = o0b["transport_scope"]
    require(
        transport_scope
        == {
            "class_id": TRANSPORT_CLASS_ID,
            "generators": list(TRANSPORT_GENERATORS),
            "preserves": [
                "displayed_parallel_product_equations",
                "typed_outside_incidence_data",
                "record_and_role_types",
            ],
            "arbitrary_algebraic_orientation_changing_maps_covered": False,
            "claim": "NO_TRANSPORT_IN_THIS_DECLARED_NATURAL_CLASS",
        },
        "declared natural transport class",
    )
    parts = o0b["residual_owner_partition"]
    require(parts["split_rank5"] == {"rows": 360, "raw_labels": 37800}, "split partition")
    require(parts["repeated_cells_1_2"] == {"rows": 16, "raw_labels": 1680}, "repeated 1/2")
    require(parts["repeated_cells_11_14"] == {"rows": 32, "raw_labels": 3360}, "repeated 11/14")
    require(parts["total"] == {"rows": 408, "raw_labels": 42840}, "O0b total")
    repeated, split = o0b["o0a_transport_obstructions"]
    require(repeated["o0b_value"] == 1 and repeated["o0a_value_mod_p"] == P - 1, "ratio obstruction")
    require(repeated["guard"] == {"characteristic_not_2": True, "bc_nonzero": True}, "ratio guard")
    require(not repeated["isomorphism_exists"], "false repeated transport")
    require(split == {"branch": "SPLIT_BC_FULL_SYSTEM", "invariant": "outside_incidence_signature", **split_signature_permutation_audit()}, "split transport obstruction")
    require(o0b["outside_label_orbits"] == label_orbit_census(), "label orbit census")
    split_audit = o0b["split_block_candidate_orbit_audit"]
    candidate_terms = (
        split_audit["sdf_candidate_term"],
        split_audit["sde_candidate_term"],
        split_audit["s0_paired_candidate_term"],
        split_audit["s0_fixed_candidate_term"],
    )
    require(
        split_audit["conditional_candidate_workload"] == 11304
        and sum(candidate_terms) == 11304,
        "conditional candidate abstract-label-orbit workload",
    )
    require(
        split_audit["status"]
        == "CONDITIONAL_ABSTRACT_LABEL_ORBIT_WORKLOAD_NOT_A_CENSUS_ELIMINATION_OR_PAYMENT"
        and len(split_audit["unproved_inputs"]) == 3,
        "candidate orbit audit scope",
    )

    guard = cert["pr1155_reconciliation"]
    require(guard["commit"] == PR1155_HEAD and guard["status"] == "OPEN_GAP", "PR1155 binding")
    require(guard["guarded_necessary_point_survives"], "PR1155 surviving point")
    require(guard["classification"] == "VALID_GUARD_TRANSPLANT_ROUTE_CUT_REGRESSION_DEPENDENCY", "PR1155 classification")

    ledger = cert["exact_ledger_outputs"]
    for name in ("U_remaining", "U_positive", "U_sourcecover", "U_K3", "U_K3_allocation", "signed_slack"):
        require(ledger[name] is None, f"{name} must remain undefined")
    require(not ledger["inequality_evaluable"], "inequality must not be evaluated")
    require(ledger["B_star"] == B_STAR and ledger["U_paid"] == U_PAID, "ledger known terms")
    require(
        ledger["U_paid_source_status"]
        == "MANIFEST_DECLARED_TRANSITIVE_SOURCE_GATE_STALE",
        "U_paid stale-source status",
    )
    require(ledger["joint_Q_BC_new_reserve"] == JOINT_UNPAID_RESERVE, "joint reserve")
    require(
        ledger["joint_reserve_status"]
        == "ARITHMETIC_FROM_MANIFEST_DECLARATION_NOT_REVALIDATED_PAYMENT",
        "joint reserve source status",
    )
    require(not ledger["joint_reserve_is_K3_allocation"], "reserve/allocation distinction")
    require(ledger["allocation_interval_only"] == [0, JOINT_UNPAID_RESERVE], "allocation interval")

    conclusion = cert["conclusion"]
    require(conclusion["success_condition"] == "B", "success condition")
    require(
        conclusion["verdict"]
        == "YELLOW_GLOBAL_RED_NATURAL_O0B_TO_O0A_TRANSPORT",
        "verdict scope",
    )
    require(conclusion["ledger_movement"] == 0, "ledger movement")
    require(not conclusion["K3_closed"] and not conclusion["KoalaBear_row_closed"], "closure flags")
    require(cert["source_bindings"] == source_bindings(), "source bindings")


def mutation_tests(cert: dict[str, Any]) -> int:
    tests: list[tuple[str, dict[str, Any], bool]] = []

    def add(name: str, mutate: Callable[[dict[str, Any]], None], reseal: bool = True) -> None:
        candidate = copy.deepcopy(cert)
        mutate(candidate)
        if reseal:
            candidate = seal(candidate)
        tests.append((name, candidate, reseal))

    add("partition", lambda x: x["active_contract"].__setitem__("partition_sha256", "0" * 64))
    add("unit", lambda x: x["active_contract"].__setitem__("unit", "RAW_LABELS"))
    add("first_match", lambda x: x["active_contract"].__setitem__("first_match", False))
    add("tangent_revalidated", lambda x: x["tangent_import_source_gate"].__setitem__("transitive_source_revalidated", True))
    add("tangent_hash_match", lambda x: x["tangent_import_source_gate"].__setitem__("source_binding_matches", True))
    add("tangent_steering_gating", lambda x: x["tangent_import_source_gate"].__setitem__("steering_drift_is_gating", True))
    add("overbroad_domain", lambda x: x["compiler_contract"].__setitem__("domain_is_all_Z_BC", True))
    add("slice_membership", lambda x: x["compiler_contract"].__setitem__("slice_membership_predicate_proved", True))
    add("slice_exhaustive", lambda x: x["compiler_contract"].__setitem__("slice_exhaustive_within_Z_BC", True))
    add("fake_bridge", lambda x: x["compiler_contract"].__setitem__("single_valued_source_to_component_map_proved", True))
    add("fake_inverse", lambda x: x["compiler_contract"].__setitem__("inverse_reconstruction_map_proved", True))
    add("fake_exhaustive", lambda x: x["compiler_contract"].__setitem__("exhaustive_partition_proved", True))
    add("source_cover_paid", lambda x: x["source_cover"].__setitem__("U_sourcecover", 0))
    add("source_cover_candidate_count", lambda x: x["source_cover"].__setitem__("unresolved_candidate_row_passport_combinations", 7))
    add("omit_281", lambda x: x["orientation_census"].__setitem__("independent_transverse_type", None))
    add("close_open_route", lambda x: x["coordinate_workboard"]["routes"][0].__setitem__("status", "PROVED_EMPTY_RAW_SYSTEMS"))
    add("raw_zero_as_slope_zero", lambda x: next(row for row in x["coordinate_workboard"]["routes"] if row["status"] == "PROVED_EMPTY_RAW_SYSTEMS").__setitem__("distinct_affine_slope_payment", 0))
    add("remaining_count", lambda x: x["coordinate_workboard"].__setitem__("remaining_route_count", 10))
    add("o0b_labels", lambda x: x["o0b_native_route_cut"]["residual_owner_partition"]["total"].__setitem__("raw_labels", 42839))
    add("transport_scope_widened", lambda x: x["o0b_native_route_cut"]["transport_scope"].__setitem__("arbitrary_algebraic_orientation_changing_maps_covered", True))
    add("ratio_transport", lambda x: x["o0b_native_route_cut"]["o0a_transport_obstructions"][0].__setitem__("isomorphism_exists", True))
    add("signature_transport", lambda x: x["o0b_native_route_cut"]["o0a_transport_obstructions"][1].__setitem__("isomorphisms", 1))
    add("candidate_workload", lambda x: x["o0b_native_route_cut"]["split_block_candidate_orbit_audit"].__setitem__("conditional_candidate_workload", 11303))
    add("candidate_promoted", lambda x: x["o0b_native_route_cut"]["split_block_candidate_orbit_audit"].__setitem__("status", "PROVED_CENSUS"))
    add("guard_promoted", lambda x: x["pr1155_reconciliation"].__setitem__("status", "CLOSED"))
    add("fake_U_K3", lambda x: x["exact_ledger_outputs"].__setitem__("U_K3", 0))
    add("reserve_as_allocation", lambda x: x["exact_ledger_outputs"].__setitem__("U_K3_allocation", JOINT_UNPAID_RESERVE))
    add("reserve_flag", lambda x: x["exact_ledger_outputs"].__setitem__("joint_reserve_is_K3_allocation", True))
    add("U_paid_revalidated", lambda x: x["exact_ledger_outputs"].__setitem__("U_paid_source_status", "SOURCE_REVALIDATED"))
    add("ledger_movement", lambda x: x["conclusion"].__setitem__("ledger_movement", 1))
    add("source_binding", lambda x: x["source_bindings"][0].__setitem__("sha256", "f" * 64))
    add("payload", lambda x: x.__setitem__("payload_sha256", "0" * 64), reseal=False)

    rejected = 0
    for name, candidate, _ in tests:
        try:
            verify_certificate(candidate)
        except (AssertionError, KeyError, TypeError):
            rejected += 1
            continue
        raise AssertionError(f"mutation survived: {name}")
    return rejected


def verify_local_sources() -> None:
    for relative, expected in LOCAL_BINDINGS.items():
        require(sha256_file(ROOT / relative) == expected, f"local source digest: {relative}")
        committed = hashlib.sha256(git_blob(ROOT, PR1152_HEAD, relative)).hexdigest()
        require(committed == expected, f"PR1152 source digest: {relative}")
    row = load_json(ROOT / ROW_REL)
    require(row["architecture_id"] == ARCHITECTURE, "row architecture")
    partition = row["partition"]
    require(partition["partition_sha256"] == PARTITION_SHA256, "row partition")
    require(partition["unit"] == UNIT and partition["quantifier"] == QUANTIFIER, "row unit/quantifier")
    require(partition["first_match"] is True and partition["first_match_disjoint"] is True, "row first-match semantics")
    require(partition["same_partition_for_all_atoms"] is True, "same partition for all atoms")
    bc_stage = next(stage for stage in partition["chronology_stages"] if stage["atom_id"] == "U_BC")
    require(
        bc_stage["owner_id"] == "ACTIVE_V4_BALANCED_CORE"
        and bc_stage["priority"] == 2
        and bc_stage["paid"] is False,
        "row U_BC owner chronology",
    )
    contract = row["row_contract"]
    require(contract["field"]["base_prime"] == P, "row base prime")
    require(contract["field"]["extension_degree"] == 6, "row extension degree")
    require(contract["domain"]["cardinality"] == N, "row domain cardinality")
    require(contract["code"]["dimension"] == K, "row code dimension")
    require(contract["agreement"] == AGREEMENT, "row agreement")
    require(contract["B_star"] == B_STAR, "row B_star")
    require(contract["projection_and_unit"] == UNIT, "row projection/unit")
    require(
        contract["received_object_quantifier"] == "FOR_EVERY_ADMISSIBLE_RECEIVED_LINE",
        "row received-line quantifier",
    )
    active_binding = next(
        binding
        for binding in row["source_bindings"]
        if binding["binding_id"] == "KB_V4_ROW::active_v4"
    )
    require(active_binding["hash"] == EXPECTED_ACTIVE_V4_BLOB, "tangent expected active-v4 blob")
    steering_binding = next(
        binding
        for binding in row["source_bindings"]
        if binding["binding_id"] == "KB_V4_ROW::workboard"
    )
    require(steering_binding["hash"] == EXPECTED_STEERING_BLOB, "tangent expected steering blob")
    require(
        git_blob_id(ROOT, PR1152_HEAD, str(ACTIVE_V4_REL))
        == OBSERVED_ACTIVE_V4_BLOB,
        "PR1152 observed active-v4 blob",
    )
    require(EXPECTED_ACTIVE_V4_BLOB != OBSERVED_ACTIVE_V4_BLOB, "stale source gate must remain explicit")
    require(
        git_blob_id(ROOT, PR1152_HEAD, "agents.md")
        == OBSERVED_PR1152_STEERING_BLOB,
        "PR1152 observed steering blob",
    )
    require(
        EXPECTED_STEERING_BLOB != OBSERVED_PR1152_STEERING_BLOB,
        "non-gating steering drift must remain explicit",
    )
    tangent = load_json(ROOT / TANGENT_REL)
    require(tangent["architecture_id"] == ARCHITECTURE, "tangent architecture")
    require(tangent["partition_sha256"] == PARTITION_SHA256, "tangent partition")
    require(tangent["proof_status"] == "PROVED_GATE_B_BANKABLE_ATOM_ROW_OPEN", "tangent declared proof status")
    require(tangent["closure_state"]["known_sum"] == U_PAID, "known U_paid")
    require(tangent["closure_state"]["remaining_budget_after_known_sum"] == JOINT_UNPAID_RESERVE, "known reserve")
    paid_atom = next(atom for atom in tangent["atoms"] if atom["atom_id"] == "U_paid")
    require(
        paid_atom["value"] == U_PAID
        and paid_atom["unit"] == UNIT
        and paid_atom["quantifier"] == QUANTIFIER
        and paid_atom["partition_sha256"] == PARTITION_SHA256,
        "manifest-declared U_paid semantics",
    )
    bc_atom = next(atom for atom in tangent["atoms"] if atom["atom_id"] == "U_BC")
    require(
        bc_atom["value"] is None
        and bc_atom["owner_ids"] == ["ACTIVE_V4_BALANCED_CORE"]
        and bc_atom["unit"] == UNIT
        and bc_atom["quantifier"] == QUANTIFIER,
        "U_BC must remain null in the same contract",
    )
    raw = load_json(ROOT / RAW_REL)
    require(raw["provenance"]["commit"] == RAW_DAG_COMMIT, "raw provenance")
    require(raw["statement"]["ledger_movement"] == 0, "raw ledger movement")
    require(
        raw["statement"]["claims"]["principal_census"]
        == "15 role cells, 1575 raw labels, 25200 signed principal systems",
        "raw census statement",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, help="rs-mca-prize-dag clone containing the pinned public-DAG commit")
    parser.add_argument("--pr1155-root", type=Path, help="rs-mca clone containing PR #1155 commit")
    parser.add_argument("--skip-mutations", action="store_true")
    parser.add_argument("--print-certificate", action="store_true")
    args = parser.parse_args()

    verify_local_sources()
    shipped = load_json(ROOT / CERT_REL)
    expected = build_certificate()
    require(shipped == expected, "shipped certificate differs from exact constructor")
    verify_certificate(shipped)

    checked = len(LOCAL_BINDINGS)
    if args.source_root is not None:
        checked += verify_blob_bindings(args.source_root, PUBLIC_DAG_COMMIT, PUBLIC_DAG_BINDINGS)
    if args.pr1155_root is not None:
        checked += verify_blob_bindings(args.pr1155_root, PR1155_HEAD, PR1155_BINDINGS)

    mutations = 0 if args.skip_mutations else mutation_tests(shipped)
    if args.print_certificate:
        print(json.dumps(shipped, indent=2, sort_keys=True))
    print(
        "K3_SOURCE_BOUND_ROUTE_CUT_PASS "
        f"routes=13 closed_raw=2 remaining=11 o0b_labels=42840 "
        f"sourcecover_candidate_combinations=8 mutations={mutations} source_hashes={checked} "
        f"terminal={TERMINAL}"
    )


if __name__ == "__main__":
    main()
