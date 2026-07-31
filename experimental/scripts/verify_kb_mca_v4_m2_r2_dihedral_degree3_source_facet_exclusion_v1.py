#!/usr/bin/env python3
"""Verify the cubic source-facet and full-V4 exclusion packet."""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import subprocess
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
    / "data/certificates/kb-mca-v4-m2-r2-dihedral-degree3-source-facet-exclusion-v1"
    / "kb_mca_v4_m2_r2_dihedral_degree3_source_facet_exclusion_v1.json"
)

SOURCE_FACET = {
    "commit": "44542e91e459364a521870ed2ebde7f6fe5055bf",
    "theorem_path": "experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/proof/pole_disjoint_conic_facet_collinearity_reduction.md",
    "theorem_blob_oid": "356ff4b47d0bb429d11ea10382762a6e95b5ce24",
    "certificate_path": "experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/pole_disjoint_conic_facet_collinearity_certificate.json",
    "certificate_blob_oid": "91643b5b9020f52764a77cfbc8aa6279ce2d5ef8",
    "certificate_payload_sha256": "396697687aa5baf19d8114b20858d4500b119c078f5f128b6c0e207ec8ff50bb",
}

PARENTS = {
    "star_graph": {
        "commit": "06a0dcb152687db4017484b215ed851bae52f1f2",
        "certificate_path": "experimental/data/certificates/kb-mca-v4-m2-r2-dihedral-residual-star-graph-rigidity-v1/kb_mca_v4_m2_r2_dihedral_residual_star_graph_rigidity_v1.json",
        "certificate_blob_oid": "c842c89b0d4978a12d4ede3d12fc040de6d11741",
        "certificate_payload_sha256": "63f6387bba81e51e0a49f409645e9493b3f128f6ab9d119be2dcc64da766b1d4",
        "terminal": "M2_R2_DIHEDRAL_RESIDUAL_STAR_GRAPH_RIGIDITY",
    },
    "outer_factor": {
        "commit": "b264da9d3309b7b42ab81a1481778d9d92ca8926",
        "certificate_path": "experimental/data/certificates/kb-mca-v4-m2-r2-dihedral-outer-factor-reduction-v1/kb_mca_v4_m2_r2_dihedral_outer_factor_reduction_v1.json",
        "certificate_blob_oid": "4e389740170515d668ad1057488a484fb43cd104",
        "certificate_payload_sha256": "7f85c8e4bf9c1f324a705058992cd2e082a990feeb648f37189ba78d72df831c",
        "terminal": "M2_R2_DIHEDRAL_FACTOR_DEGREES_2_3_5_6",
    },
    "degree2": {
        "commit": "36ed2ac28176fb583cbf15d16f8074b6e8a48de8",
        "certificate_path": "experimental/data/certificates/kb-mca-v4-m2-r2-dihedral-degree2-source-star-exclusion-v1/kb_mca_v4_m2_r2_dihedral_degree2_source_star_exclusion_v1.json",
        "certificate_blob_oid": "a6705b3507014434052c4c5e63209fae2d566038",
        "certificate_payload_sha256": "c3771a0386e955b87f6ec9f4256d9569fb5e9459036653f790691851be0f2a89",
        "terminal": "M2_R2_DIHEDRAL_DEGREE2_EMPTY",
    },
    "degree5": {
        "commit": "fe2a549c8de1de34e5ea331ff4c410145207e381",
        "certificate_path": "experimental/data/certificates/kb-mca-v4-m2-r2-dihedral-degree5-source-star-exclusion-v1/kb_mca_v4_m2_r2_dihedral_degree5_source_star_exclusion_v1.json",
        "certificate_blob_oid": "ba27da451743fd198efd4b335a0983ed030acbb5",
        "certificate_payload_sha256": "1b711c1cde8f0652ce5e713513955ecdc1789e9fd62c361bca00ae05c9b4c287",
        "terminal": "M2_R2_DIHEDRAL_DEGREE5_EMPTY",
    },
    "degree6": {
        "commit": "5bcb2b2bd0158912cb7319ef386ca2523db5436d",
        "certificate_path": "experimental/data/certificates/kb-mca-v4-m2-r2-dihedral-degree6-common-pole-exclusion-v1/kb_mca_v4_m2_r2_dihedral_degree6_common_pole_exclusion_v1.json",
        "certificate_blob_oid": "b6c821cdf89c0e82461ff53216e7a83ac8087ff5",
        "certificate_payload_sha256": "224fbbaf75c0aa830c7fab8e6024a51d3454d7ce3a6260184041983806f1e3fd",
        "terminal": "M2_R2_DIHEDRAL_DEGREE6_COMMON_POLE_EMPTY",
    },
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
    require(
        git_output(
            "rev-parse",
            f"{SOURCE_FACET['commit']}:{SOURCE_FACET['theorem_path']}",
        )
        == SOURCE_FACET["theorem_blob_oid"],
        "source-facet theorem blob",
    )
    source = load_pinned(SOURCE_FACET)
    statuses = source.get("theorem_status", {})
    require(statuses.get("q6_s6_source_label_near_coincidence_9_25") == "PROVED",
            "Corollary 9.25 status")
    require(statuses.get("q6_s6_source_facet_deck_9_27") == "PROVED",
            "Corollary 9.27 status")
    require(source.get("outgoing_conjugate_ledger", {}).get(
                "q6_s6_source_facet_common_size") == 5,
            "source-facet common size")

    loaded = {name: load_pinned(record) for name, record in PARENTS.items()}
    for name, record in PARENTS.items():
        terminal = loaded[name].get("conclusion", {}).get("terminal")
        if terminal is None:
            terminal = loaded[name].get("statement", {}).get("terminal")
        require(terminal == record["terminal"], f"parent terminal {name}")
    require(
        loaded["outer_factor"]["conclusion"]["surviving_factor_degrees"] == [2, 3, 5, 6],
        "outer factor list",
    )
    require(
        loaded["star_graph"]["source_graphs"][0]["graph_shape"] == "2 K2,2,2",
        "cubic star graph",
    )


def graph_replay() -> dict[str, Any]:
    parts = [
        [{0, 1}, {2, 3}, {4, 5}],
        [{6, 7}, {8, 9}, {10, 11}],
    ]
    edges: set[frozenset[int]] = set()
    for component in parts:
        for left_index, right_index in itertools.combinations(range(3), 2):
            for left in component[left_index]:
                for right in component[right_index]:
                    edges.add(frozenset((left, right)))
    require(len(edges) == 24, "edge count")

    maximum = 0
    independent_fives = 0
    for size in range(13):
        for subset in itertools.combinations(range(12), size):
            chosen = set(subset)
            independent = all(not edge <= chosen for edge in edges)
            if independent:
                maximum = max(maximum, size)
                if size == 5:
                    independent_fives += 1
    degrees = [
        sum(vertex in edge for edge in edges)
        for vertex in range(12)
    ]
    require(maximum == 4, "independence number")
    require(independent_fives == 0, "independent five")
    require(degrees == [4] * 12, "vertex degrees")
    return {
        "components": ["K_(2,2,2)", "K_(2,2,2)"],
        "vertices": 12,
        "edges": 24,
        "vertex_degrees": degrees,
        "independence_number": maximum,
        "five_subsets_checked": 792,
        "independent_five_subsets": independent_fives,
    }


def expected_certificate() -> dict[str, Any]:
    data = {
        "schema": "kb-mca-v4-m2-r2-dihedral-degree3-source-facet-exclusion-v1",
        "source_facet_parent": SOURCE_FACET,
        "parents": PARENTS,
        "source_facet": {
            "invariant_set_size": 6,
            "common_set_size": 5,
            "common_set_contained_in_invariant_set": True,
            "horizontal_outgoing_roots_over_common_fiber": "I^c",
        },
        "twist_safe_identification": {
            "complete_coordinate_fiber_star_endpoints": "U_k",
            "endpoint_count": 4,
            "omitted_deck_pair": "P_k",
            "omitted_pair_size": 2,
            "facet_consequence": "U_k subset I^c and k in I imply k notin U_k",
            "common_pole_consequence": "k lies in U_k disjoint_union P_k",
            "conclusion": "k in P_k and U_k=N_G(k)",
            "relative_endpoint_twist_set_to_identity": False,
        },
        "graph_replay": graph_replay(),
        "full_v4_synthesis": {
            "exhaustive_factor_degrees": [2, 3, 5, 6],
            "excluded_factor_degrees": [2, 3, 5, 6],
            "degree3_exclusion": "common-five source-facet independence contradiction",
        },
        "conclusion": {
            "degree3_deleted": True,
            "full_v4_type_deleted": True,
            "deleted_type": {"m": 2, "r": 2, "delta": 4},
            "remaining_m2_types": [
                {"r": 4, "delta": 2},
                {"r": 8, "delta": 1},
            ],
            "k3_status": "OPEN",
            "koalabear_row_status": "OPEN",
            "terminal": "M2_R2_DIHEDRAL_DEGREE3_AND_FULL_V4_EMPTY",
        },
        "nonclaims": [
            "no deletion of the order-two or trivial m2 stabilizer types",
            "no carrier, data, explaining-polynomial, or slope owner",
            "no payment, K3, KoalaBear row, endpoint, or Prize close",
        ],
    }
    data["payload_sha256"] = payload_hash(data)
    return data


def verify_data(data: dict[str, Any]) -> None:
    require(payload_hash(data) == data.get("payload_sha256"), "certificate seal")
    require(data == expected_certificate(), "certificate content")


def tamper_selftest(data: dict[str, Any]) -> int:
    mutations: list[Callable[[dict[str, Any]], None]] = [
        lambda x: x["source_facet"].__setitem__("common_set_size", 4),
        lambda x: x["source_facet"].__setitem__("invariant_set_size", 7),
        lambda x: x["twist_safe_identification"].__setitem__(
            "relative_endpoint_twist_set_to_identity", True
        ),
        lambda x: x["twist_safe_identification"].__setitem__("endpoint_count", 3),
        lambda x: x["graph_replay"].__setitem__("edges", 23),
        lambda x: x["graph_replay"].__setitem__("independence_number", 5),
        lambda x: x["graph_replay"].__setitem__("independent_five_subsets", 1),
        lambda x: x["full_v4_synthesis"].__setitem__(
            "exhaustive_factor_degrees", [2, 3, 5]
        ),
        lambda x: x["full_v4_synthesis"].__setitem__(
            "excluded_factor_degrees", [2, 3, 6]
        ),
        lambda x: x["conclusion"].__setitem__("degree3_deleted", False),
        lambda x: x["conclusion"].__setitem__("full_v4_type_deleted", False),
        lambda x: x["conclusion"].__setitem__("k3_status", "CLOSED"),
        lambda x: x["conclusion"].__setitem__("koalabear_row_status", "CLOSED"),
        lambda x: x["conclusion"].__setitem__("terminal", "M2_R2_OPEN"),
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
        "KB_MCA_V4_M2_R2_DIHEDRAL_DEGREE3_SOURCE_FACET_EXCLUSION_PASS "
        f"alpha={data['graph_replay']['independence_number']} "
        f"full_v4_deleted={data['conclusion']['full_v4_type_deleted']} "
        f"tamper_rejected={rejected}"
    )


if __name__ == "__main__":
    main()
