#!/usr/bin/env python3
"""Verify the KoalaBear residual n=3,6 source-star graph rigidity."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
from collections import Counter
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
    / "data/certificates/kb-mca-v4-m2-r2-dihedral-residual-star-graph-rigidity-v1"
    / "kb_mca_v4_m2_r2_dihedral_residual_star_graph_rigidity_v1.json"
)
DEGREE2_PARENT = {
    "commit": "36ed2ac28176fb583cbf15d16f8074b6e8a48de8",
    "certificate_path": "experimental/data/certificates/kb-mca-v4-m2-r2-dihedral-degree2-source-star-exclusion-v1/kb_mca_v4_m2_r2_dihedral_degree2_source_star_exclusion_v1.json",
    "certificate_blob_oid": "a6705b3507014434052c4c5e63209fae2d566038",
    "certificate_payload_sha256": "c3771a0386e955b87f6ec9f4256d9569fb5e9459036653f790691851be0f2a89",
    "imported_terminal": "M2_R2_DIHEDRAL_DEGREE2_EMPTY",
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


def verify_parent(parent: dict[str, str]) -> None:
    path = parent["certificate_path"]
    blob = git_output("rev-parse", f"{parent['commit']}:{path}")
    require(blob == parent["certificate_blob_oid"], f"parent blob mismatch: {path}")
    data = parse_json(git_output("show", f"{parent['commit']}:{path}"), path)
    require(data.get("payload_sha256") == parent["certificate_payload_sha256"], f"parent payload mismatch: {path}")
    require(payload_hash(data) == data.get("payload_sha256"), f"parent payload seal mismatch: {path}")
    require(data.get("conclusion", {}).get("terminal") == parent["imported_terminal"], f"parent terminal mismatch: {path}")


def canonical_pair(left: tuple, right: tuple) -> tuple[tuple, tuple]:
    return tuple(sorted((left, right)))


def dihedral_incidence(n: int) -> dict[str, Any]:
    points = [(i, bit) for i in range(n) for bit in (0, 1)]

    def u(point):
        i, bit = point
        return ((-i) % n, 1 - bit)

    def v(point):
        i, bit = point
        return ((1 - i) % n, 1 - bit)

    def block(point, involution):
        return frozenset((point, involution(point)))

    y_blocks = sorted({block(point, u) for point in points}, key=repr)
    z_blocks = sorted({block(point, v) for point in points}, key=repr)
    y_index = {fiber: index for index, fiber in enumerate(y_blocks)}
    neighborhoods = []
    for z_block in z_blocks:
        pair = sorted({y_index[block(point, u)] for point in z_block})
        require(len(pair) == 2, "Z quotient fiber is not adjacent to two Y fibers")
        neighborhoods.append(tuple(pair))
    require(len(set(neighborhoods)) == n, "dihedral neighborhoods repeat")
    degrees = Counter(vertex for pair in neighborhoods for vertex in pair)
    require(set(degrees.values()) == {2}, "quotient incidence is not a cycle")
    return {
        "n": n,
        "regular_orbit_size": 2 * n,
        "incidence_graph": f"C{2*n}",
        "z_neighborhoods": [list(pair) for pair in neighborhoods],
    }


def source_graph(n: int) -> dict[str, Any]:
    pole_count = 6 // n
    stars: Counter = Counter()
    label_degrees: Counter = Counter()
    for pole in range(pole_count):
        incidence = dihedral_incidence(n)
        for left, right in incidence["z_neighborhoods"]:
            left_labels = [(pole, left, sign) for sign in (0, 1)]
            right_labels = [(pole, right, sign) for sign in (0, 1)]
            edges = [
                canonical_pair(left_labels[0], right_labels[0]),
                canonical_pair(left_labels[1], right_labels[1]),
                canonical_pair(left_labels[0], right_labels[1]),
                canonical_pair(left_labels[1], right_labels[0]),
            ]
            for edge in edges:
                stars[edge] += 1
                label_degrees.update(edge)
    defect = sum(weight * (weight - 1) // 2 for weight in stars.values())
    require(sum(stars.values()) == 24, "source mass is not 24")
    require(len(stars) == 24, "source stars repeat")
    require(set(stars.values()) == {1}, "source weights are not all one")
    require(len(label_degrees) == 12, "source-label count is not twelve")
    require(set(label_degrees.values()) == {4}, "source rows are not quartic")
    require(defect == 0, "source defect is not zero")
    return {
        "n": n,
        "generic_outer_poles": pole_count,
        "graph_shape": "2 K2,2,2" if n == 3 else "2-point blow-up of C6",
        "source_labels": len(label_degrees),
        "source_star_units": sum(stars.values()),
        "distinct_star_vertices": len(stars),
        "star_weight_multiset": sorted(stars.values()),
        "source_label_degree_multiset": sorted(label_degrees.values()),
        "defect": defect,
    }


def build_certificate() -> dict[str, Any]:
    data = {
        "schema": "kb-mca-v4-m2-r2-dihedral-residual-star-graph-rigidity-v1",
        "parent_degree2_exclusion": DEGREE2_PARENT,
        "parent_source_genus": GENUS_PARENT,
        "source_orientation_law": {
            "preserving_lift": "(tau,b)",
            "conjugation": "c eta c^-1=eta*a",
            "first_endpoint_edges": [["t", "s"], ["tau(t)", "tau(s)"]],
            "second_endpoint_edges": [["t", "tau(s)"], ["tau(t)", "s"]],
            "combined_graph": "K2,2 exactly once",
        },
        "dihedral_incidence": [dihedral_incidence(n) for n in (3, 6)],
        "source_graphs": [source_graph(n) for n in (3, 6)],
        "conclusion": {
            "terminal": "M2_R2_DIHEDRAL_RESIDUAL_STAR_GRAPH_RIGIDITY",
            "surviving_factor_degrees": [3, 6],
            "profiles_deleted": [],
            "full_v4_type_deleted": False,
            "next_gate": "birational quartic coefficient realization plus V4 branch passport",
        },
        "nonclaims": [
            "no n=3 or n=6 existence or deletion",
            "no m2 type deletion or payment",
            "no K3, KoalaBear, endpoint, or Prize close",
        ],
    }
    data["payload_sha256"] = payload_hash(data)
    return data


def verify_certificate(data: dict[str, Any], verify_parents: bool) -> None:
    require(data.get("schema") == "kb-mca-v4-m2-r2-dihedral-residual-star-graph-rigidity-v1", "schema")
    require(data.get("payload_sha256") == payload_hash(data), "payload seal")
    require(data.get("parent_degree2_exclusion") == DEGREE2_PARENT, "degree2 parent")
    require(data.get("parent_source_genus") == GENUS_PARENT, "genus parent")
    if verify_parents:
        verify_parent(DEGREE2_PARENT)
        verify_parent(GENUS_PARENT)
    require(data.get("source_orientation_law") == build_certificate()["source_orientation_law"], "orientation law")
    require(data.get("dihedral_incidence") == [dihedral_incidence(n) for n in (3, 6)], "dihedral replay")
    require(data.get("source_graphs") == [source_graph(n) for n in (3, 6)], "source replay")
    conclusion = data.get("conclusion", {})
    require(conclusion.get("terminal") == "M2_R2_DIHEDRAL_RESIDUAL_STAR_GRAPH_RIGIDITY", "terminal")
    require(conclusion.get("surviving_factor_degrees") == [3, 6], "survivors")
    require(conclusion.get("profiles_deleted") == [], "profile overclaim")
    require(conclusion.get("full_v4_type_deleted") is False, "type overclaim")
    require(len(data.get("nonclaims", [])) == 3, "nonclaims")


def reseal(data: dict[str, Any]) -> None:
    data["payload_sha256"] = payload_hash(data)


def tamper_selftest(original: dict[str, Any]) -> int:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("degree2-parent", lambda row: row["parent_degree2_exclusion"].__setitem__("certificate_blob_oid", "0" * 40)),
        ("genus-parent", lambda row: row["parent_source_genus"].__setitem__("certificate_payload_sha256", "0" * 64)),
        ("lift", lambda row: row["source_orientation_law"].__setitem__("preserving_lift", "(tau,1)")),
        ("conjugation", lambda row: row["source_orientation_law"].__setitem__("conjugation", "c eta c^-1=eta")),
        ("orientation", lambda row: row["source_orientation_law"]["second_endpoint_edges"].pop()),
        ("incidence-n", lambda row: row["dihedral_incidence"][0].__setitem__("n", 4)),
        ("incidence-graph", lambda row: row["dihedral_incidence"][1].__setitem__("incidence_graph", "K6,6")),
        ("neighborhood", lambda row: row["dihedral_incidence"][0]["z_neighborhoods"].pop()),
        ("pole-count", lambda row: row["source_graphs"][0].__setitem__("generic_outer_poles", 1)),
        ("shape3", lambda row: row["source_graphs"][0].__setitem__("graph_shape", "C6")),
        ("shape6", lambda row: row["source_graphs"][1].__setitem__("graph_shape", "K2,2,2")),
        ("mass", lambda row: row["source_graphs"][1].__setitem__("source_star_units", 23)),
        ("vertices", lambda row: row["source_graphs"][0].__setitem__("distinct_star_vertices", 23)),
        ("weights", lambda row: row["source_graphs"][1]["star_weight_multiset"].append(2)),
        ("degrees", lambda row: row["source_graphs"][0]["source_label_degree_multiset"].__setitem__(0, 3)),
        ("defect", lambda row: row["source_graphs"][0].__setitem__("defect", 1)),
        ("survivors", lambda row: row["conclusion"]["surviving_factor_degrees"].append(2)),
        ("delete", lambda row: row["conclusion"].__setitem__("full_v4_type_deleted", True)),
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
        verify_parent(DEGREE2_PARENT)
        verify_parent(GENUS_PARENT)
        data = build_certificate()
        CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
        print(f"WROTE: {CERTIFICATE.relative_to(REPO_ROOT)}")
    data = parse_json(CERTIFICATE.read_text(), str(CERTIFICATE))
    verify_certificate(data, True)
    print("PASS: residual n=3,6 source-star graphs are exact and defect zero")
    if args.tamper_selftest:
        count = tamper_selftest(data)
        print(f"PASS: {count}/{count} tamper mutations rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
