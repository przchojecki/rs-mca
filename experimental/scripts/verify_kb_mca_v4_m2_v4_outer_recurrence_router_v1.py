#!/usr/bin/env python3
"""Verify the KoalaBear m2 V4 outer-recurrence router."""

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
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


EXPERIMENTAL = Path(__file__).resolve().parents[1]
REPO_ROOT = EXPERIMENTAL.parent
CERTIFICATE = (
    EXPERIMENTAL
    / "data/certificates/kb-mca-v4-m2-v4-outer-recurrence-router-v1"
    / "kb_mca_v4_m2_v4_outer_recurrence_router_v1.json"
)
M3_FRONTIER_PARENT = {
    "commit": "bf173815d0a51d880c94c833be125769715f2c49",
    "certificate_path": "experimental/data/certificates/kb-mca-v4-m3-primitive-outer-degree2-router-v1/kb_mca_v4_m3_primitive_outer_degree2_router_v1.json",
    "certificate_blob_oid": "24f406d8bdb72d8562c91b28890eae59befd6d91",
    "certificate_payload_sha256": "0f7c0134c723875d66dd19d96f9c68c7299079b5560e63780910afc6d86f21d4",
    "imported_terminal": "M3_NO_INDEPENDENT_PRODUCER_ROUTES_TO_M2",
}
COMPILER_PARENT = {
    "commit": "e287c54252c7872e1745c7594cfef62b74a65cf5",
    "certificate_path": "experimental/data/certificates/kb-mca-v4-degree60-source-pencil-rank-compiler-v1/kb_mca_v4_degree60_source_pencil_rank_compiler_v1.json",
    "certificate_blob_oid": "5c16c7884b349d7e474b8dfc1267ab357ef0d477",
    "certificate_payload_sha256": "6d4bc83e40e491f02f7d265b021628ffb7d52b1978c0655f83e5a9d3e0a9f4bb",
    "imported_terminal": "TRANSVERSE_OUTER_CORRESPONDENCE_UNPAID",
}
PRIMITIVE_PARENT = {
    "commit": "59c4449ca0f5cee929dd39fc7b5ae8b0a33877f4",
    "certificate_path": "experimental/data/certificates/kb-mca-v4-degree60-primitive-subdegree4-route-cut-v1/kb_mca_v4_degree60_primitive_subdegree4_route_cut_v1.json",
    "certificate_blob_oid": "7e8a79db97dc56125f25d9a190c3b0c3adca158a",
    "certificate_payload_sha256": "21a8ca7800745c2c94876d48473801e84f4d9c8f9e6ce5b53e8b8bd66b699962",
    "imported_terminal": "ROUTED_TO_GEOMETRIC_FUNCTIONAL_DECOMPOSITION_ADAPTER",
}
M10_PARENT = {
    "commit": "412bc68f1dcb6ac3924d6445146417f3c713ef89",
    "certificate_path": "experimental/data/certificates/kb-mca-v4-m10-scott-strip-lower-degree-router-v1/kb_mca_v4_m10_scott_strip_lower_degree_router_v1.json",
    "certificate_blob_oid": "6e49093fdb9d9e55b45c55265eb3cc0c0e65e8c9",
    "certificate_payload_sha256": "66117d7ba207a66606fc4ae4770a2b314b3510066be7af734b4e579d028ce1d1",
    "imported_terminal": "M10_NO_TERMINAL_PRODUCER_ROUTES_TO_M2_M3_M6",
}
P = 29
INFINITY = P
IDENTITY = tuple(range(P + 1))
ROWS = ((2, 4), (4, 2), (8, 1))
CATALOGUE = (
    ("PSL(2,29)", 12180, (1, 29)),
    ("PGL(2,29)", 24360, (1, 29)),
    ("A30", math.factorial(30) // 2, (1, 29)),
    ("S30", math.factorial(30), (1, 29)),
)
ROUTES = (
    (2, 4, "M4_EMPTY"),
    (3, 6, "M6_TO_M2_OR_EMPTY"),
    (5, 10, "M10_TO_M2_M3_M6"),
    (6, 12, "M12_EMPTY"),
    (10, 20, "SOURCE_PROFILE_EMPTY"),
    (15, 30, "M30_TO_M6_TO_M2_OR_EMPTY"),
)


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


def mobius(a: int, b: int, c: int, d: int) -> tuple[int, ...]:
    require((a * d - b * c) % P != 0, "singular Mobius matrix")
    result = []
    for value in range(P):
        denominator = (c * value + d) % P
        if denominator == 0:
            result.append(INFINITY)
        else:
            result.append(((a * value + b) * pow(denominator, -1, P)) % P)
    result.append(INFINITY if c == 0 else (a * pow(c, -1, P)) % P)
    require(len(set(result)) == P + 1, "Mobius action is not a permutation")
    return tuple(result)


def compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[value]] for value in range(P + 1))


def generated_group(generators: tuple[tuple[int, ...], ...]) -> set[tuple[int, ...]]:
    group = {IDENTITY}
    pending = [IDENTITY]
    while pending:
        current = pending.pop()
        for generator in generators:
            candidate = compose(generator, current)
            if candidate not in group:
                group.add(candidate)
                pending.append(candidate)
    return group


def subdegrees(group: set[tuple[int, ...]]) -> list[int]:
    stabilizer = [value for value in group if value[INFINITY] == INFINITY]
    unseen = set(range(P + 1))
    lengths = []
    while unseen:
        seed = min(unseen)
        orbit = {value[seed] for value in stabilizer}
        lengths.append(len(orbit))
        unseen -= orbit
    return sorted(lengths)


def projective_rows() -> dict[str, Any]:
    translation = mobius(1, 1, 0, 1)
    inversion = mobius(0, -1, 1, 0)
    nonsquare_scaling = mobius(2, 0, 0, 1)
    require(pow(2, (P - 1) // 2, P) == P - 1, "2 is not nonsquare")
    psl = generated_group((translation, inversion))
    pgl = generated_group((translation, inversion, nonsquare_scaling))
    require(len(psl) == 12180 and len(pgl) == 24360, "projective orders")
    require(psl < pgl, "projective containment")
    require(subdegrees(psl) == subdegrees(pgl) == [1, 29], "subdegrees")
    return {
        "PSL(2,29)": {"reconstructed_order": len(psl), "subdegrees": [1, 29]},
        "PGL(2,29)": {"reconstructed_order": len(pgl), "subdegrees": [1, 29]},
    }


def v4_rows() -> dict[str, Any]:
    identity = (0, 0)
    v4 = {identity, (1, 0), (0, 1), (1, 1)}
    subgroups = [
        {identity},
        {identity, (1, 0)},
        {identity, (0, 1)},
        {identity, (1, 1)},
        v4,
    ]
    require(sorted(map(len, subgroups)) == [1, 2, 2, 2, 4], "V4 subgroups")
    require(all(r * delta == 8 for r, delta in ROWS), "row identity")
    return {
        "group_order": 4,
        "subgroup_order_multiset": [1, 2, 2, 2, 4],
        "rows": [
            {"r": 2, "delta": 4, "stabilizer": "V4"},
            {"r": 4, "delta": 2, "stabilizer": "one_of_three_C2"},
            {"r": 8, "delta": 1, "stabilizer": "trivial"},
        ],
    }


def source_defect_rows() -> dict[str, Any]:
    imported = [
        {"weight_two_vertices": value, "weight_three_vertices": 0, "defect_cost": value}
        for value in (1, 2, 3)
    ] + [{"weight_two_vertices": 0, "weight_three_vertices": 1, "defect_cost": 3}]
    refined = []
    for doubles in range(4):
        fixed = [value for value in range(doubles + 1) if (doubles - value) % 2 == 0]
        refined.append(
            {
                "weight_two_vertices": doubles,
                "weight_three_vertices": 0,
                "fixed_matching_vertex_counts": fixed,
            }
        )
    return {
        "imported_nonsimple_profiles": imported,
        "coordinate_stabilized_profiles": refined,
        "weight_three_excluded": True,
        "paired_locator_avoidance": "div(q_i)<=div(B/(z_i*z_bar_i))",
        "star_equivariance": "star(b*x)=tau(star(x))",
    }


def build_certificate() -> dict[str, Any]:
    live_r = {r for r, _ in ROWS}
    require(all(not live_r.intersection(row) for _, _, row in CATALOGUE), "primitive row")
    factors = tuple(value for value in range(2, 30) if 30 % value == 0)
    require(factors == tuple(row[0] for row in ROUTES), "factor ledger")
    require(tuple(2 * value for value in factors) == tuple(row[1] for row in ROUTES), "destinations")
    data = {
        "schema": "kb-mca-v4-m2-v4-outer-recurrence-router-v1",
        "payload_sha256": "",
        "statement": {
            "workboard_item": "K3",
            "row": "KoalaBear MCA at 2^-128",
            "terminal": "M2_V4_STABILIZERS_OUTER_RECURRENCE_AND_SOURCE_PARITY",
            "ledger_movement": 0,
        },
        "parent_m3_frontier": copy.deepcopy(M3_FRONTIER_PARENT),
        "parent_compiler": copy.deepcopy(COMPILER_PARENT),
        "parent_primitive_route": copy.deepcopy(PRIMITIVE_PARENT),
        "parent_m10_router": copy.deepcopy(M10_PARENT),
        "classification_source": {
            "repository": "gap-packages/primgrp",
            "commit": "5612e113d50ac23a7d10945383936e20440b4e14",
            "path": "data/gps1.g",
            "entry": "PRIMGRP[30]",
            "extracted_bytes": 344,
            "entry_sha256": "1a923cc8f4428ec22864109cdc60d0c87326e8939cc1d72d217d22df2a4b8da0",
            "catalogue_completeness": "imported",
        },
        "input": {
            "inner_degree": 2,
            "outer_degree": 30,
            "transverse_rows": [list(row) for row in ROWS],
            "actual_component_bidegree": [4, 4],
        },
        "v4_stabilizer_replay": v4_rows(),
        "primitive_catalogue": [
            {"name": name, "order": order, "subdegrees": list(row)}
            for name, order, row in CATALOGUE
        ],
        "projective_action_replay": projective_rows(),
        "proper_factor_routes": [
            {"right_factor_degree": factor, "new_inner_degree": inner, "terminal": terminal}
            for factor, inner, terminal in ROUTES
        ],
        "coordinate_stabilized_source": source_defect_rows(),
        "conclusion": {
            "primitive_outer_producer_count": 0,
            "outer_recurrence_classified": True,
            "m2_type_count_before": 3,
            "m2_type_count_after": 3,
            "m2_nonexistence_claimed": False,
            "coordinate_stabilized_weight_three_present": False,
            "terminal": "M2_V4_STABILIZERS_OUTER_RECURRENCE_AND_SOURCE_PARITY",
        },
        "nonclaims": [
            "no deletion or payment of an inner-degree-two type",
            "no preferred orientation in the order-two stabilizer row",
            "no source refinement without tau x 1 in the stabilizer",
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
    frontier = load_parent(M3_FRONTIER_PARENT, "m3 frontier parent")
    require(frontier["conclusion"]["terminal"] == M3_FRONTIER_PARENT["imported_terminal"], "frontier terminal")
    require(frontier["conclusion"]["remaining_m2_rows"] == [[2, 4], [4, 2], [8, 1]], "m2 frontier")

    compiler = load_parent(COMPILER_PARENT, "compiler parent")
    require(compiler["conclusion"]["terminal"] == COMPILER_PARENT["imported_terminal"], "compiler terminal")
    m2_rows = next(row for row in compiler["transverse_outer_terminal"]["rows"] if row["m"] == 2)
    require(m2_rows["r_delta"] == [[2, 4], [4, 2], [8, 1]], "compiler rows")

    primitive = load_parent(PRIMITIVE_PARENT, "primitive parent")
    require(primitive["conclusion"]["terminal"] == PRIMITIVE_PARENT["imported_terminal"], "primitive terminal")
    require(primitive["statement"]["downstairs_component_bidegree"] == [4, 4], "component bidegree")
    require(20 in primitive["excluded_inner_degrees"], "m20 exclusion")
    require(
        primitive["complete_source_quartic_defect_gate"]["allowed_nonsimple_weight_histograms"]
        == source_defect_rows()["imported_nonsimple_profiles"],
        "defect profiles",
    )

    m10 = load_parent(M10_PARENT, "m10 parent")
    require(m10["conclusion"]["terminal"] == M10_PARENT["imported_terminal"], "m10 terminal")
    require(m10["conclusion"]["m10_terminal_type_count"] == 0, "m10 route")


def verify_certificate(data: dict[str, Any], check_git: bool = True) -> None:
    require(payload_hash(data) == data.get("payload_sha256"), "payload hash")
    require(data == build_certificate(), "certificate differs from exact reconstruction")
    if check_git:
        verify_parents()


def reseal(data: dict[str, Any]) -> None:
    data["payload_sha256"] = payload_hash(data)


def tamper_selftest(original: dict[str, Any]) -> int:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("frontier-parent", lambda row: row["parent_m3_frontier"].__setitem__("certificate_blob_oid", "0" * 40)),
        ("compiler-parent", lambda row: row["parent_compiler"].__setitem__("imported_terminal", "EMPTY")),
        ("primitive-parent", lambda row: row["parent_primitive_route"].__setitem__("certificate_payload_sha256", "0" * 64)),
        ("m10-parent", lambda row: row["parent_m10_router"].__setitem__("commit", "0" * 40)),
        ("source-hash", lambda row: row["classification_source"].__setitem__("entry_sha256", "0" * 64)),
        ("drop-row", lambda row: row["input"]["transverse_rows"].pop()),
        ("bidegree", lambda row: row["input"]["actual_component_bidegree"].__setitem__(0, 3)),
        ("v4-order", lambda row: row["v4_stabilizer_replay"].__setitem__("group_order", 8)),
        ("stabilizer", lambda row: row["v4_stabilizer_replay"]["rows"][0].__setitem__("stabilizer", "C2")),
        ("catalogue-order", lambda row: row["primitive_catalogue"][0].__setitem__("order", 12179)),
        ("catalogue-subdegree", lambda row: row["primitive_catalogue"][1]["subdegrees"].__setitem__(1, 8)),
        ("replay", lambda row: row["projective_action_replay"]["PSL(2,29)"].__setitem__("reconstructed_order", 12181)),
        ("factor", lambda row: row["proper_factor_routes"][0].__setitem__("right_factor_degree", 3)),
        ("destination", lambda row: row["proper_factor_routes"][4].__setitem__("new_inner_degree", 18)),
        ("triple", lambda row: row["coordinate_stabilized_source"].__setitem__("weight_three_excluded", False)),
        ("locator", lambda row: row["coordinate_stabilized_source"].__setitem__("paired_locator_avoidance", "none")),
        ("type-count", lambda row: row["conclusion"].__setitem__("m2_type_count_after", 0)),
        ("nonexistence", lambda row: row["conclusion"].__setitem__("m2_nonexistence_claimed", True)),
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
    print("PASS: m2 V4 stabilizers, outer recurrence, and source parity")
    if args.tamper_selftest:
        count = tamper_selftest(data)
        print(f"PASS: {count}/{count} tamper mutations rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
