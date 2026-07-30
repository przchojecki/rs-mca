#!/usr/bin/env python3
"""Verify the KoalaBear m3 primitive-outer degree-two router."""

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
    / "data/certificates/kb-mca-v4-m3-primitive-outer-degree2-router-v1"
    / "kb_mca_v4_m3_primitive_outer_degree2_router_v1.json"
)
FRONTIER_PARENT = {
    "commit": "b60dcda4bc84453aa72c4185c72b351fa345ea40",
    "certificate_path": "experimental/data/certificates/kb-mca-v4-m4-adjacency-genus-exclusion-v1/kb_mca_v4_m4_adjacency_genus_exclusion_v1.json",
    "certificate_blob_oid": "a0b2c8ec260da35ffdefa5a29c7aa5496af5cc79",
    "certificate_payload_sha256": "a0bc909a9e05c097440d318f5fe7aed052387507723fc1f3337172d3e5db7428",
    "imported_terminal": "M4_TRANSVERSE_ROW_EMPTY_BY_ADJACENCY_GENUS",
}
SOURCE_PROFILE_PARENT = {
    "commit": "59c4449ca0f5cee929dd39fc7b5ae8b0a33877f4",
    "certificate_path": "experimental/data/certificates/kb-mca-v4-degree60-primitive-subdegree4-route-cut-v1/kb_mca_v4_degree60_primitive_subdegree4_route_cut_v1.json",
    "certificate_blob_oid": "7e8a79db97dc56125f25d9a190c3b0c3adca158a",
    "certificate_payload_sha256": "21a8ca7800745c2c94876d48473801e84f4d9c8f9e6ce5b53e8b8bd66b699962",
    "imported_excluded_inner_degree": 15,
}
SOURCE_FIBER_PARENT = {
    "commit": "a14a05d9ba80068133e93e2fa77d6d1dc8828829",
    "certificate_path": "experimental/data/certificates/kb-mca-v4-degree60-decomposition-source-fiber-adapter-v1/kb_mca_v4_degree60_decomposition_source_fiber_adapter_v1.json",
    "certificate_blob_oid": "911bac3c1c5d1b4cd9822c59939d60e832b7ef23",
    "certificate_payload_sha256": "638190df24415e5609fa9c2f50dde8fd22bd150f60e7bef5cd1496cb22d75b4e",
    "imported_refinement": {"from": 30, "to": 6},
}
M6_PARENT = {
    "commit": "30be68b9",
    "certificate_path": "experimental/data/certificates/kb-mca-v4-m6-scott-cartesian-degree2-router-v1/kb_mca_v4_m6_scott_cartesian_degree2_router_v1.json",
    "certificate_blob_oid": "af5fd87a5c28f3b021fc05971a665e6d92f978af",
    "certificate_payload_sha256": "b34e096730f3d93644c283f95d65f622100d6868e9882ed2b901fa109b3d6116",
    "imported_terminal": "M6_NO_TERMINAL_PRODUCER_ROUTES_TO_M2_OR_EXCLUDED_M5",
}
M12_PARENT = {
    "commit": "c23eb801",
    "certificate_path": "experimental/data/certificates/kb-mca-v4-m12-diagonal-socle-degree5-close-v1/kb_mca_v4_m12_diagonal_socle_degree5_close_v1.json",
    "certificate_blob_oid": "9e1bd3d89dac6409f148dc134fda46d3bf644c11",
    "certificate_payload_sha256": "456b51c78e837c8a27ffda0b43409c63c88128b254be320723728868db096e6f",
    "imported_terminal": "M12_DECOMPOSITION_ROW_EMPTY",
}
P = 19
INFINITY = P
IDENTITY = tuple(range(P + 1))
M3_ROWS = ((2, 6), (3, 4), (4, 3), (6, 2), (12, 1))
CATALOGUE = (
    ("PSL(2,19)", 3420, (1, 19)),
    ("PGL(2,19)", 6840, (1, 19)),
    ("A20", math.factorial(20) // 2, (1, 19)),
    ("S20", math.factorial(20), (1, 19)),
)
ROUTES = (
    (2, 6, "M6_TO_M2_OR_EMPTY"),
    (4, 12, "M12_EMPTY"),
    (5, 15, "SOURCE_PROFILE_EMPTY"),
    (10, 30, "M30_TO_M6_TO_M2_OR_EMPTY"),
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


def cycle_type(value: tuple[int, ...]) -> list[int]:
    unseen = set(range(P + 1))
    lengths = []
    while unseen:
        point = min(unseen)
        length = 0
        while point in unseen:
            unseen.remove(point)
            point = value[point]
            length += 1
        lengths.append(length)
    return sorted(lengths, reverse=True)


def projective_rows() -> dict[str, Any]:
    translation = mobius(1, 1, 0, 1)
    inversion = mobius(0, -1, 1, 0)
    nonsquare_scaling = mobius(2, 0, 0, 1)
    require(pow(2, (P - 1) // 2, P) == P - 1, "2 is not nonsquare")
    psl = generated_group((translation, inversion))
    pgl = generated_group((translation, inversion, nonsquare_scaling))
    require(len(psl) == 3420 and len(pgl) == 6840, "projective group orders")
    require(psl < pgl, "projective group containment")
    require(subdegrees(psl) == subdegrees(pgl) == [1, 19], "projective subdegrees")
    require(any(cycle_type(value) == [5, 5, 5, 5] for value in psl), "pole cycle")
    return {
        "PSL(2,19)": {"reconstructed_order": len(psl), "subdegrees": [1, 19]},
        "PGL(2,19)": {"reconstructed_order": len(pgl), "subdegrees": [1, 19]},
        "mandatory_pole_cycle_present_in_PSL": [5, 5, 5, 5],
    }


def build_certificate() -> dict[str, Any]:
    require(all(r * delta == 12 for r, delta in M3_ROWS), "m3 row identity")
    live_r = {r for r, _ in M3_ROWS}
    require(
        all(not live_r.intersection(subdegrees) for _, _, subdegrees in CATALOGUE),
        "primitive catalogue supports a live subdegree",
    )
    proper_factors = tuple(value for value in range(2, 20) if 20 % value == 0)
    require(proper_factors == tuple(row[0] for row in ROUTES), "factor degrees")
    require(tuple(3 * value for value in proper_factors) == tuple(row[1] for row in ROUTES), "destination degrees")
    data = {
        "schema": "kb-mca-v4-m3-primitive-outer-degree2-router-v1",
        "payload_sha256": "",
        "statement": {
            "workboard_item": "K3",
            "row": "KoalaBear MCA at 2^-128",
            "terminal": "M3_NO_INDEPENDENT_PRODUCER_ROUTES_TO_M2",
            "ledger_movement": 0,
        },
        "parent_frontier": copy.deepcopy(FRONTIER_PARENT),
        "parent_source_profile": copy.deepcopy(SOURCE_PROFILE_PARENT),
        "parent_source_fiber": copy.deepcopy(SOURCE_FIBER_PARENT),
        "parent_m6_router": copy.deepcopy(M6_PARENT),
        "parent_m12_close": copy.deepcopy(M12_PARENT),
        "classification_source": {
            "repository": "gap-packages/primgrp",
            "commit": "5612e113d50ac23a7d10945383936e20440b4e14",
            "path": "data/gps1.g",
            "entry": "PRIMGRP[20]",
            "extracted_bytes": 342,
            "entry_sha256": "cbc9ca7fda9b0de36a4034a4d59e24bb6c07aff0e54458604990919583007133",
            "catalogue_completeness": "imported",
        },
        "input": {
            "inner_degree": 3,
            "outer_degree": 20,
            "transverse_rows": [list(row) for row in M3_ROWS],
            "required_subdegrees": sorted(live_r),
            "mandatory_outer_pole_cycle": [5, 5, 5, 5],
        },
        "primitive_catalogue": [
            {"name": name, "order": order, "subdegrees": list(subdegree_row)}
            for name, order, subdegree_row in CATALOGUE
        ],
        "projective_action_replay": projective_rows(),
        "proper_factor_routes": [
            {"right_factor_degree": factor, "new_inner_degree": inner, "terminal": terminal}
            for factor, inner, terminal in ROUTES
        ],
        "conclusion": {
            "primitive_outer_producer_count": 0,
            "m3_independent_type_count": 0,
            "m3_nonexistence_claimed": False,
            "independent_frontier_before": 8,
            "independent_frontier_after": 3,
            "remaining_inner_degrees": [2],
            "remaining_m2_rows": [[2, 4], [4, 2], [8, 1]],
            "terminal": "M3_NO_INDEPENDENT_PRODUCER_ROUTES_TO_M2",
        },
        "source_bindings": {
            "classification": "complete GAP PrimGrp degree-20 entry",
            "local_replay": "exact projective-line PSL(2,19),PGL(2,19) actions",
            "decomposition_dictionary": "primitive outer monodromy iff no proper rational right factor",
            "destination_routes": "exact parent terminals pinned by Git blob and payload",
        },
        "nonclaims": [
            "no nonexistence of every inner-degree-three decomposition",
            "no deletion or payment of an inner-degree-two type",
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
    require(git_output("rev-parse", f"{commit}:{path}") == binding["certificate_blob_oid"], f"{label} blob")
    parent = parse_json(git_output("show", f"{commit}:{path}"), label)
    require(payload_hash(parent) == parent["payload_sha256"] == binding["certificate_payload_sha256"], f"{label} payload")
    return parent


def verify_parents() -> None:
    frontier = load_parent(FRONTIER_PARENT, "frontier parent")
    require(frontier["conclusion"]["terminal"] == FRONTIER_PARENT["imported_terminal"], "frontier terminal")
    require(frontier["conclusion"]["remaining_type_counts"] == {"m2": 3, "m3": 5}, "frontier counts")

    profile = load_parent(SOURCE_PROFILE_PARENT, "source profile parent")
    require(15 in profile["excluded_inner_degrees"], "m15 exclusion")

    fiber = load_parent(SOURCE_FIBER_PARENT, "source fiber parent")
    require(SOURCE_FIBER_PARENT["imported_refinement"] in fiber["conclusion"]["refined_to_earlier_inner_degree"], "m30 refinement")

    m6 = load_parent(M6_PARENT, "m6 parent")
    require(m6["conclusion"]["terminal"] == M6_PARENT["imported_terminal"], "m6 terminal")
    require(m6["conclusion"]["degree_two_closed"] is False, "m6 scope")

    m12 = load_parent(M12_PARENT, "m12 parent")
    require(m12["conclusion"]["terminal"] == M12_PARENT["imported_terminal"], "m12 terminal")
    require(m12["conclusion"]["remaining_degree_twelve_type_count"] == 0, "m12 close")


def verify_certificate(data: dict[str, Any], check_git: bool = True) -> None:
    require(payload_hash(data) == data.get("payload_sha256"), "payload hash")
    require(data == build_certificate(), "certificate differs from exact reconstruction")
    if check_git:
        verify_parents()


def reseal(data: dict[str, Any]) -> None:
    data["payload_sha256"] = payload_hash(data)


def tamper_selftest(original: dict[str, Any]) -> int:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("frontier-parent", lambda row: row["parent_frontier"].__setitem__("certificate_blob_oid", "0" * 40)),
        ("profile-parent", lambda row: row["parent_source_profile"].__setitem__("imported_excluded_inner_degree", 14)),
        ("fiber-parent", lambda row: row["parent_source_fiber"]["imported_refinement"].__setitem__("to", 5)),
        ("m6-parent", lambda row: row["parent_m6_router"].__setitem__("imported_terminal", "EMPTY")),
        ("m12-parent", lambda row: row["parent_m12_close"].__setitem__("certificate_payload_sha256", "0" * 64)),
        ("source-hash", lambda row: row["classification_source"].__setitem__("entry_sha256", "0" * 64)),
        ("drop-row", lambda row: row["input"]["transverse_rows"].pop()),
        ("required-r", lambda row: row["input"]["required_subdegrees"].append(19)),
        ("catalogue-order", lambda row: row["primitive_catalogue"][0].__setitem__("order", 3419)),
        ("catalogue-subdegree", lambda row: row["primitive_catalogue"][1]["subdegrees"].__setitem__(1, 12)),
        ("replay", lambda row: row["projective_action_replay"]["PSL(2,19)"].__setitem__("reconstructed_order", 3421)),
        ("factor", lambda row: row["proper_factor_routes"][0].__setitem__("right_factor_degree", 3)),
        ("destination", lambda row: row["proper_factor_routes"][3].__setitem__("new_inner_degree", 20)),
        ("nonexistence", lambda row: row["conclusion"].__setitem__("m3_nonexistence_claimed", True)),
        ("frontier", lambda row: row["conclusion"].__setitem__("independent_frontier_after", 8)),
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
    print("PASS: every m3 producer routes to m2 or contradiction")
    if args.tamper_selftest:
        count = tamper_selftest(data)
        print(f"PASS: {count}/{count} tamper mutations rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
