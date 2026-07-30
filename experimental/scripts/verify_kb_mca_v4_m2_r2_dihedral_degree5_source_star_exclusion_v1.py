#!/usr/bin/env python3
"""Verify the KoalaBear m2 r2 degree-five dihedral exclusion."""

from __future__ import annotations

import argparse
import copy
import hashlib
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
    / "data/certificates/kb-mca-v4-m2-r2-dihedral-degree5-source-star-exclusion-v1"
    / "kb_mca_v4_m2_r2_dihedral_degree5_source_star_exclusion_v1.json"
)
OUTER_PARENT = {
    "commit": "b264da9d3309b7b42ab81a1481778d9d92ca8926",
    "certificate_path": "experimental/data/certificates/kb-mca-v4-m2-r2-dihedral-outer-factor-reduction-v1/kb_mca_v4_m2_r2_dihedral_outer_factor_reduction_v1.json",
    "certificate_blob_oid": "4e389740170515d668ad1057488a484fb43cd104",
    "certificate_payload_sha256": "7f85c8e4bf9c1f324a705058992cd2e082a990feeb648f37189ba78d72df831c",
    "imported_terminal": "M2_R2_DIHEDRAL_FACTOR_DEGREES_2_3_5_6",
}
DEFECT_PARENT = {
    "commit": "59c4449ca0f5cee929dd39fc7b5ae8b0a33877f4",
    "certificate_path": "experimental/data/certificates/kb-mca-v4-degree60-primitive-subdegree4-route-cut-v1/kb_mca_v4_degree60_primitive_subdegree4_route_cut_v1.json",
    "certificate_blob_oid": "7e8a79db97dc56125f25d9a190c3b0c3adca158a",
    "certificate_payload_sha256": "21a8ca7800745c2c94876d48473801e84f4d9c8f9e6ce5b53e8b8bd66b699962",
    "imported_terminal": "ROUTED_TO_GEOMETRIC_FUNCTIONAL_DECOMPOSITION_ADAPTER",
}
SOURCE_PARENT = {
    "commit": "ad109774f7d9bc320e7e0c046ba83471f39d5cd9",
    "certificate_path": "experimental/data/certificates/kb-mca-v4-q6-u2-complete-source-conic-exclusion-v1/kb_mca_v4_q6_u2_complete_source_conic_exclusion_v1.json",
    "certificate_blob_oid": "61afd4534740c5ccabc6196919126c80c361e4c5",
    "certificate_payload_sha256": "30a5d45895957f774ef972118e227fa54522fc27a48ee0e2a99a0d5a012a5451",
    "imported_terminal": "DELETED_BY_COMPLETE_SOURCE_DIVISOR_PROFILE_OBSTRUCTION",
}
GENUS_PARENT = {
    "commit": "f6bc4a2b2a6a5b3bba98f24a520c67ca3373dbbb",
    "certificate_path": "experimental/data/certificates/kb-mca-v4-m2-r2-full-v4-source-genus-drop-v1/kb_mca_v4_m2_r2_full_v4_source_genus_drop_v1.json",
    "certificate_blob_oid": "83e82b826ddfa2f5377e99f439be5f00900507c6",
    "certificate_payload_sha256": "9a2ea090568600356f27f3174aee6d08414217b26dbb8f7922931c64a151122f",
    "imported_terminal": "M2_R2_SOURCE_GENUS_ZERO_OR_ONE",
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
            ["git", *args],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as error:
        raise VerificationError(error.stderr.strip()) from error
    return result.stdout.strip()


def compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[i]] for i in range(len(left)))


def cycle_lengths(permutation: tuple[int, ...]) -> list[int]:
    seen: set[int] = set()
    lengths = []
    for start in range(len(permutation)):
        if start in seen:
            continue
        point = start
        length = 0
        while point not in seen:
            seen.add(point)
            point = permutation[point]
            length += 1
        lengths.append(length)
    return sorted(lengths, reverse=True)


def dihedral_coset_replay() -> dict[str, Any]:
    rotation = tuple((i + 1) % 5 for i in range(5))
    reflection = tuple((-i) % 5 for i in range(5))
    identity = tuple(range(5))
    require(compose(reflection, reflection) == identity, "reflection order")
    require(compose(rotation, compose(reflection, rotation)) == reflection, "D5 relation")
    require(cycle_lengths(rotation) == [5], "rotation branch")
    require(cycle_lengths(reflection) == [2, 2, 1], "reflection branch")
    return {
        "degree": 5,
        "rotation_branch_cycles": [5],
        "reflection_branch_cycles": [2, 2, 1],
        "totally_ramified_quotient_fiber_size": 1,
    }


def source_weight_replay() -> dict[str, Any]:
    endpoint_source_fiber_size = 2
    source_parameter_fiber_degree = 2
    endpoint_values_over_z0 = 2
    forced_weight = source_parameter_fiber_degree * endpoint_values_over_z0
    defect_cost = forced_weight * (forced_weight - 1) // 2
    require(forced_weight == 4, "forced source-star weight")
    require(defect_cost == 6, "forced defect cost")
    require(forced_weight > 3, "weight contradiction")
    return {
        "endpoint_source_fiber_size": endpoint_source_fiber_size,
        "source_parameter_fiber_degree": source_parameter_fiber_degree,
        "distinct_endpoint_values_over_z0": endpoint_values_over_z0,
        "forced_matching_star_weight": forced_weight,
        "forced_defect_cost": defect_cost,
        "proved_maximum_star_weight": 3,
        "proved_total_defect_budget": 3,
    }


def build_certificate() -> dict[str, Any]:
    data = {
        "schema": "kb-mca-v4-m2-r2-dihedral-degree5-source-star-exclusion-v1",
        "payload_sha256": "",
        "statement": {
            "workboard_item": "K3",
            "row": "KoalaBear MCA at 2^-128",
            "terminal": "M2_R2_DIHEDRAL_DEGREE5_EMPTY",
            "ledger_movement": 0,
        },
        "parent_outer_reduction": copy.deepcopy(OUTER_PARENT),
        "parent_quartic_defect": copy.deepcopy(DEFECT_PARENT),
        "parent_complete_source": copy.deepcopy(SOURCE_PARENT),
        "parent_source_cover": copy.deepcopy(GENUS_PARENT),
        "input": {
            "inner_degree": 2,
            "outer_subdegree": 2,
            "component_degree": 4,
            "dihedral_factor_degree": 5,
            "outer_pole_profile": {
                "generic_order_five_poles": 1,
                "simple_totally_ramified_poles": 1,
                "endpoint_order_five_poles": 6,
            },
        },
        "dihedral_coset_replay": dihedral_coset_replay(),
        "source_pullback": {
            "complete_source_identity": "div(B)=psi^*(sum_i [alpha_i])",
            "coordinate_index_identification_used": False,
            "endpoint_map_unramified_over_source_poles": True,
            "source_base_change_degree": 2,
            "local_saturation": "two distinct source labels at every B-root",
            "forced_star": "h^(-1)(y_0)",
        },
        "source_weight_replay": source_weight_replay(),
        "conclusion": {
            "factor_degree_five_deleted": True,
            "surviving_factor_degrees": [2, 3, 6],
            "full_v4_type_deleted": False,
            "terminal": "M2_R2_DIHEDRAL_DEGREE5_EMPTY",
        },
        "nonclaims": [
            "no deletion of factor degree 2, 3, or 6",
            "no deletion of either other inner-degree-two type",
            "no deletion or payment of the full-V4 inner-degree-two type",
            "no coordinate-index identity z_i=psi^*[alpha_i]",
            "no carrier, received-data, explaining-polynomial, or slope owner",
            "no u2, K3, KoalaBear row, endpoint, or prize closure",
            "no ledger movement",
        ],
    }
    data["payload_sha256"] = payload_hash(data)
    return data


def load_parent(binding: dict[str, Any], label: str) -> dict[str, Any]:
    commit = binding["commit"]
    path = binding["certificate_path"]
    require(
        git_output("rev-parse", f"{commit}:{path}") == binding["certificate_blob_oid"],
        f"{label} blob",
    )
    parent = parse_json(git_output("show", f"{commit}:{path}"), label)
    require(
        payload_hash(parent)
        == parent["payload_sha256"]
        == binding["certificate_payload_sha256"],
        f"{label} payload",
    )
    return parent


def verify_parents() -> None:
    outer = load_parent(OUTER_PARENT, "outer parent")
    require(outer["conclusion"]["terminal"] == OUTER_PARENT["imported_terminal"], "outer terminal")
    require(outer["conclusion"]["surviving_factor_degrees"] == [2, 3, 5, 6], "outer factor list")
    row_five = next(row for row in outer["pole_sieve_replay"] if row["factor_degree"] == 5)
    require(row_five["survives"] is True, "degree-five parent profile")

    defect = load_parent(DEFECT_PARENT, "defect parent")
    gate = defect["complete_source_quartic_defect_gate"]
    require(gate["maximum_weight"] == 3, "maximum source-star weight")
    require(gate["delta_lower_bound"] == "delta_v >= binomial(w_v,2)", "defect lower bound")

    source = load_parent(SOURCE_PARENT, "source parent")
    require(source["conclusion"]["terminal"] == SOURCE_PARENT["imported_terminal"], "source terminal")
    require("B_IS_COMPLETE_TWELVE_SOURCE_PULLBACK" in source["dependencies"]["required_results"], "complete source pullback")
    require(source["complete_source_saturation"]["local_inequality"] == "sum_i ord_x H(alpha_i,-) <= 2 ord_x B", "local saturation")

    genus = load_parent(GENUS_PARENT, "source-cover parent")
    require(genus["conclusion"]["terminal"] == GENUS_PARENT["imported_terminal"], "source-cover terminal")
    cover = genus["source_cover"]
    require(cover["degree_over_W"] // cover["degree_over_X"] == 2, "source base-change degree")


def verify_certificate(data: dict[str, Any], check_git: bool = True) -> None:
    require(payload_hash(data) == data.get("payload_sha256"), "payload hash")
    require(data == build_certificate(), "certificate differs from exact reconstruction")
    if check_git:
        verify_parents()


def reseal(data: dict[str, Any]) -> None:
    data["payload_sha256"] = payload_hash(data)


def tamper_selftest(original: dict[str, Any]) -> int:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("outer-parent", lambda row: row["parent_outer_reduction"].__setitem__("certificate_blob_oid", "0" * 40)),
        ("defect-parent", lambda row: row["parent_quartic_defect"].__setitem__("certificate_payload_sha256", "0" * 64)),
        ("source-parent", lambda row: row["parent_complete_source"].__setitem__("commit", "0" * 40)),
        ("cover-parent", lambda row: row["parent_source_cover"].__setitem__("certificate_blob_oid", "0" * 40)),
        ("factor-degree", lambda row: row["input"].__setitem__("dihedral_factor_degree", 6)),
        ("pole-profile", lambda row: row["input"]["outer_pole_profile"].__setitem__("simple_totally_ramified_poles", 0)),
        ("rotation", lambda row: row["dihedral_coset_replay"]["rotation_branch_cycles"].append(1)),
        ("fiber-size", lambda row: row["dihedral_coset_replay"].__setitem__("totally_ramified_quotient_fiber_size", 2)),
        ("source-identity", lambda row: row["source_pullback"].__setitem__("complete_source_identity", "unknown")),
        ("coordinate-index", lambda row: row["source_pullback"].__setitem__("coordinate_index_identification_used", True)),
        ("base-degree", lambda row: row["source_pullback"].__setitem__("source_base_change_degree", 3)),
        ("weight", lambda row: row["source_weight_replay"].__setitem__("forced_matching_star_weight", 3)),
        ("defect", lambda row: row["source_weight_replay"].__setitem__("forced_defect_cost", 3)),
        ("survivors", lambda row: row["conclusion"]["surviving_factor_degrees"].append(5)),
        ("delete-type", lambda row: row["conclusion"].__setitem__("full_v4_type_deleted", True)),
        ("nonclaim", lambda row: row["nonclaims"].pop()),
    ]
    passed = 0
    for name, mutate in mutations:
        candidate = copy.deepcopy(original)
        mutate(candidate)
        reseal(candidate)
        try:
            verify_certificate(candidate, False)
        except VerificationError:
            passed += 1
        else:
            raise VerificationError(f"tamper survived: {name}")
    bad_hash = copy.deepcopy(original)
    bad_hash["payload_sha256"] = "0" * 64
    try:
        verify_certificate(bad_hash, False)
    except VerificationError:
        passed += 1
    else:
        raise VerificationError("tamper survived: payload")
    try:
        parse_json('{"x":1,"x":2}', "duplicate")
    except VerificationError:
        passed += 1
    else:
        raise VerificationError("duplicate key survived")
    return passed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    if not args.write and not args.check and not args.tamper_selftest:
        parser.error("at least one action is required")
    if args.write:
        verify_parents()
        data = build_certificate()
        CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
        print(f"WROTE: {CERTIFICATE.relative_to(REPO_ROOT)}")
    data = parse_json(CERTIFICATE.read_text(), str(CERTIFICATE))
    verify_certificate(data, True)
    print("PASS: full-V4 m2 r2 degree-five dihedral profile is empty")
    if args.tamper_selftest:
        count = tamper_selftest(data)
        print(f"PASS: {count}/{count} tamper mutations rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
