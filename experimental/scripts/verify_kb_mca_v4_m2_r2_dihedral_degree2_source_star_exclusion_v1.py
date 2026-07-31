#!/usr/bin/env python3
"""Verify the KoalaBear m2 r2 degree-two dihedral exclusion."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
from itertools import product
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
    / "data/certificates/kb-mca-v4-m2-r2-dihedral-degree2-source-star-exclusion-v1"
    / "kb_mca_v4_m2_r2_dihedral_degree2_source_star_exclusion_v1.json"
)
DEGREE5_PARENT = {
    "commit": "fe2a549c8de1de34e5ea331ff4c410145207e381",
    "certificate_path": "experimental/data/certificates/kb-mca-v4-m2-r2-dihedral-degree5-source-star-exclusion-v1/kb_mca_v4_m2_r2_dihedral_degree5_source_star_exclusion_v1.json",
    "certificate_blob_oid": "ba27da451743fd198efd4b335a0983ed030acbb5",
    "certificate_payload_sha256": "1b711c1cde8f0652ce5e713513955ecdc1789e9fd62c361bca00ae05c9b4c287",
    "imported_terminal": "M2_R2_DIHEDRAL_DEGREE5_EMPTY",
}
M2_PARENT = {
    "commit": "d4063dcd9c56835c3916ef792e263ea720a4d397",
    "certificate_path": "experimental/data/certificates/kb-mca-v4-m2-v4-outer-recurrence-router-v1/kb_mca_v4_m2_v4_outer_recurrence_router_v1.json",
    "certificate_blob_oid": "50d17f218bfa7d3acb211c946db0c025b9a98944",
    "certificate_payload_sha256": "fe8141810501fd7b3762a378210609177185972ec706bf9ac943fa398bd82d39",
    "imported_terminal": "M2_V4_STABILIZERS_OUTER_RECURRENCE_AND_SOURCE_PARITY",
}
DEFECT_PARENT = {
    "commit": "59c4449ca0f5cee929dd39fc7b5ae8b0a33877f4",
    "certificate_path": "experimental/data/certificates/kb-mca-v4-degree60-primitive-subdegree4-route-cut-v1/kb_mca_v4_degree60_primitive_subdegree4_route_cut_v1.json",
    "certificate_blob_oid": "7e8a79db97dc56125f25d9a190c3b0c3adca158a",
    "certificate_payload_sha256": "21a8ca7800745c2c94876d48473801e84f4d9c8f9e6ce5b53e8b8bd66b699962",
    "imported_terminal": "ROUTED_TO_GEOMETRIC_FUNCTIONAL_DECOMPOSITION_ADAPTER",
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


def orbits(permutation: tuple[int, ...]) -> list[frozenset[int]]:
    unseen = set(range(len(permutation)))
    result = []
    while unseen:
        start = min(unseen)
        orbit = frozenset({start, permutation[start]})
        result.append(orbit)
        unseen -= orbit
    return result


def d2_incidence_replay() -> dict[str, Any]:
    u = (1, 0, 3, 2)
    v = (2, 3, 0, 1)
    y_orbits = orbits(u)
    z_orbits = orbits(v)
    incidence = sorted(
        {
            (
                next(i for i, block in enumerate(y_orbits) if point in block),
                next(i for i, block in enumerate(z_orbits) if point in block),
            )
            for point in range(4)
        }
    )
    require(incidence == list(product(range(2), repeat=2)), "K2,2 incidence")
    return {
        "group": "D2=V4",
        "regular_orbit_size": 4,
        "y_quotient_size": 2,
        "z_quotient_size": 2,
        "incidence": [list(edge) for edge in incidence],
        "incidence_graph": "K2,2",
    }


def defect_floor_replay() -> dict[str, Any]:
    profiles = [row for row in product(range(9), repeat=4) if sum(row) == 8]
    costs = [sum(weight * (weight - 1) // 2 for weight in row) for row in profiles]
    minimum = min(costs)
    minimizers = [list(profiles[i]) for i, cost in enumerate(costs) if cost == minimum]
    require(minimum == 4, "defect floor")
    require(minimizers == [[2, 2, 2, 2]], "defect minimizer")
    return {
        "source_units": 8,
        "available_cross_vertices": 4,
        "profile_count_checked": len(profiles),
        "minimum_defect": minimum,
        "minimizers": minimizers,
        "proved_defect_budget": 3,
    }


def build_certificate() -> dict[str, Any]:
    data = {
        "schema": "kb-mca-v4-m2-r2-dihedral-degree2-source-star-exclusion-v1",
        "payload_sha256": "",
        "statement": {
            "workboard_item": "K3",
            "row": "KoalaBear MCA at 2^-128",
            "terminal": "M2_R2_DIHEDRAL_DEGREE2_EMPTY",
            "ledger_movement": 0,
        },
        "parent_degree5_exclusion": copy.deepcopy(DEGREE5_PARENT),
        "parent_m2_router": copy.deepcopy(M2_PARENT),
        "parent_quartic_defect": copy.deepcopy(DEFECT_PARENT),
        "parent_source_cover": copy.deepcopy(GENUS_PARENT),
        "input": {
            "inner_degree": 2,
            "outer_subdegree": 2,
            "component_degree": 4,
            "dihedral_factor_degree": 2,
            "outer_generic_order_five_poles": 3,
        },
        "d2_incidence_replay": d2_incidence_replay(),
        "source_cross_edge": {
            "z_values_per_generic_pole": 2,
            "endpoint_lifts_per_z": 2,
            "source_units_per_endpoint_lift": 2,
            "normalized_W_fiber_size": 4,
            "roots_per_y_value": 2,
            "roots_per_source_sheet_per_y_value": 1,
            "preserving_lift": "(T,X)->(tau(T),b(X))",
            "available_cross_vertices": 4,
        },
        "defect_floor_replay": defect_floor_replay(),
        "conclusion": {
            "factor_degree_two_deleted": True,
            "surviving_factor_degrees": [3, 6],
            "full_v4_type_deleted": False,
            "terminal": "M2_R2_DIHEDRAL_DEGREE2_EMPTY",
        },
        "nonclaims": [
            "no deletion of factor degree 3 or 6",
            "no deletion of either other inner-degree-two type",
            "no deletion or payment of the full-V4 inner-degree-two type",
            "no coordinate-index identity for complete source divisors",
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
    degree5 = load_parent(DEGREE5_PARENT, "degree-five parent")
    require(degree5["conclusion"]["terminal"] == DEGREE5_PARENT["imported_terminal"], "degree-five terminal")
    require(degree5["conclusion"]["surviving_factor_degrees"] == [2, 3, 6], "incoming factor list")
    require(degree5["source_pullback"]["source_base_change_degree"] == 2, "source base degree")

    m2 = load_parent(M2_PARENT, "m2 parent")
    require(m2["conclusion"]["terminal"] == M2_PARENT["imported_terminal"], "m2 terminal")
    require(m2["coordinate_stabilized_source"]["star_equivariance"] == "star(b*x)=tau(star(x))", "source lift equivariance")

    defect = load_parent(DEFECT_PARENT, "defect parent")
    gate = defect["complete_source_quartic_defect_gate"]
    require(gate["maximum_weight"] == 3, "maximum source-star weight")
    require(gate["delta_lower_bound"] == "delta_v >= binomial(w_v,2)", "defect lower bound")

    genus = load_parent(GENUS_PARENT, "source-cover parent")
    require(genus["conclusion"]["terminal"] == GENUS_PARENT["imported_terminal"], "source-cover terminal")
    require(genus["input"]["component_stabilizer"] == "full_V4", "full V4 source cover")
    cover = genus["source_cover"]
    require(cover["degree_over_W"] == 4 and cover["degree_over_X"] == 2, "source-cover degrees")


def verify_certificate(data: dict[str, Any], check_git: bool = True) -> None:
    require(payload_hash(data) == data.get("payload_sha256"), "payload hash")
    require(data == build_certificate(), "certificate differs from exact reconstruction")
    if check_git:
        verify_parents()


def reseal(data: dict[str, Any]) -> None:
    data["payload_sha256"] = payload_hash(data)


def tamper_selftest(original: dict[str, Any]) -> int:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("degree5-parent", lambda row: row["parent_degree5_exclusion"].__setitem__("certificate_blob_oid", "0" * 40)),
        ("m2-parent", lambda row: row["parent_m2_router"].__setitem__("certificate_payload_sha256", "0" * 64)),
        ("defect-parent", lambda row: row["parent_quartic_defect"].__setitem__("commit", "0" * 40)),
        ("cover-parent", lambda row: row["parent_source_cover"].__setitem__("certificate_blob_oid", "0" * 40)),
        ("factor-degree", lambda row: row["input"].__setitem__("dihedral_factor_degree", 3)),
        ("pole-count", lambda row: row["input"].__setitem__("outer_generic_order_five_poles", 2)),
        ("incidence", lambda row: row["d2_incidence_replay"]["incidence"].pop()),
        ("graph", lambda row: row["d2_incidence_replay"].__setitem__("incidence_graph", "C4 proper")),
        ("z-values", lambda row: row["source_cross_edge"].__setitem__("z_values_per_generic_pole", 1)),
        ("source-units", lambda row: row["source_cross_edge"].__setitem__("source_units_per_endpoint_lift", 1)),
        ("cross-roots", lambda row: row["source_cross_edge"].__setitem__("roots_per_source_sheet_per_y_value", 0)),
        ("lift", lambda row: row["source_cross_edge"].__setitem__("preserving_lift", "(tau,1)")),
        ("weight", lambda row: row["defect_floor_replay"].__setitem__("source_units", 7)),
        ("floor", lambda row: row["defect_floor_replay"].__setitem__("minimum_defect", 3)),
        ("survivors", lambda row: row["conclusion"]["surviving_factor_degrees"].append(2)),
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
    print("PASS: full-V4 m2 r2 degree-two dihedral profile is empty")
    if args.tamper_selftest:
        count = tamper_selftest(data)
        print(f"PASS: {count}/{count} tamper mutations rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
