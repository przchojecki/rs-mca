#!/usr/bin/env python3
"""Fail-closed verifier for the aligned-positive fixed-frontier packet."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

import sympy as sp


if not __debug__:
    raise SystemExit("optimized Python execution is refused")


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE = (
    ROOT
    / "experimental/data/certificates/"
    "kb-mca-v4-m2-aligned-positive-fixed-frontier-v1/"
    "kb_mca_v4_m2_aligned_positive_fixed_frontier_v1.json"
)
NOTE = (
    ROOT
    / "experimental/notes/frontier-adjacent/"
    "kb_mca_v4_m2_aligned_positive_fixed_frontier_v1.md"
)
COMPILER = (
    ROOT
    / "experimental/scripts/"
    "compile_kb_mca_v4_m2_aligned_positive_fixed_frontier_v1.sage"
)

ASSIGNMENTS = ("F00", "F01", "F04", "F05", "F06", "F07")
TARGETS = ("R02", "R11", "R20")
ALL_CELLS = {f"{assignment}-{target}" for assignment in ASSIGNMENTS for target in TARGETS}
EMPTY = {"F00-R11", "F01-R11"}
SMALL_SURVIVORS = {"F00-R02", "F00-R20", "F01-R02", "F01-R20"}
QUADRATIC = {
    f"{assignment}-{target}"
    for assignment in ("F04", "F05", "F06", "F07")
    for target in TARGETS
}


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def payload_sha(certificate: dict) -> str:
    copied = copy.deepcopy(certificate)
    copied.pop("payload_sha256", None)
    return hashlib.sha256(canonical_json(copied).encode()).hexdigest()


def reseal(certificate: dict) -> dict:
    certificate["payload_sha256"] = payload_sha(certificate)
    return certificate


def verify_generic_identities() -> None:
    a, b, c, d, e, f, w = sp.symbols("a b c d e f w")
    p = a * w**2 + b * w + c
    q = d * w**2 + e * w + f
    u = a * f - c * d
    v = a * e - b * d
    z = b * f - c * e
    r = u**2 - v * z
    checks = (
        sp.resultant(p, q, w) - r,
        d * p - a * q + v * w + u,
        sp.together(v**2 * p.subs(w, -u / v) - a * r),
        sp.together(v**2 * q.subs(w, -u / v) - d * r),
        a * z - b * u + c * v,
    )
    assert all(sp.expand(value) == 0 for value in checks)


def validate(certificate: dict, *, check_files: bool = True) -> None:
    assert certificate["schema"] == "rs-mca-kb-v4-m2-aligned-positive-fixed-frontier-v1"
    assert certificate["payload_sha256"] == payload_sha(certificate)
    assert certificate["field"] == {
        "base_prime": 2130706433,
        "challenge_extension_degree": 6,
    }
    assert certificate["scope"]["literal_cell_count"] == 18
    assert certificate["scope"]["ledger_movement"] == 0

    full = certificate["full_localization"]
    assert set(full["empty"]) == EMPTY
    assert set(full["surviving_two_dimensional"]) == SMALL_SURVIVORS
    assert set(full["basis_fingerprints"]) == EMPTY | SMALL_SURVIVORS
    for cell_id, fingerprint in full["basis_fingerprints"].items():
        assert len(fingerprint) == 3
        assert fingerprint[0] == 2
        assert fingerprint[1] > 0
        assert len(fingerprint[2]) == 64
        if cell_id in EMPTY:
            assert fingerprint[1] == 127

    route = certificate["quadratic_route"]
    assert set(route["literal_cells"]) == QUADRATIC
    assert route["rank_drop_retained"] == "AE-BD=0"
    groups = route["literal_orbit_groups"]
    assert len(groups) == 6
    assert all(len(group) == 2 and len(set(group)) == 2 for group in groups)
    assert {cell for group in groups for cell in group} == QUADRATIC
    assert len({cell for group in groups for cell in group}) == 12
    assert set(route["group_fingerprints"]) == {"|".join(group) for group in groups}
    for group in groups:
        record = route["group_fingerprints"]["|".join(group)]
        degree, terms, digest = record["resultant"]
        assert degree in (38, 42)
        assert terms == (2464 if degree == 38 else 3679)
        assert len(digest) == 64
        assert len(record["cores_U_V_Z"]) == 3
        assert all(len(value) == 64 for value in record["cores_U_V_Z"])

    assert EMPTY | SMALL_SURVIVORS | QUADRATIC == ALL_CELLS
    assert certificate["independent_symbolic_check"]["result"] == [0, 0, 0, 0, 0]
    conclusion = certificate["conclusion"]
    assert conclusion == {
        "newly_empty_cells": 2,
        "remaining_open_cells": 16,
        "quadratic_route_cells": 12,
        "quadratic_route_orbits": 6,
        "K3_closed": False,
        "KoalaBear_row_closed": False,
    }
    assert certificate["terminal"] == "TWO_BALANCED_CELLS_EMPTY_TWELVE_QUADRATIC_ROUTES_COMPILED"

    verify_generic_identities()

    if check_files:
        parent = certificate["parent"]
        raw_parent = (ROOT / parent["path"]).read_bytes()
        assert hashlib.sha256(raw_parent).hexdigest() == parent["sha256"]
        assert hashlib.sha1(f"blob {len(raw_parent)}\0".encode() + raw_parent).hexdigest() == parent["git_blob"]
        note = NOTE.read_text()
        compiler = COMPILER.read_text()
        for text in (
            "18 open cells -> 2 empty + 16 open cells",
            "The rank-drop branch `V=0` is retained",
            "Do not retry the raw monolithic four-variable basis",
        ):
            assert text in note
        for text in (
            "QUADRATIC_W_ROUTE_CUT_RETAINS_GENERIC_AND_RANK_DROP",
            "rank_drop_retained",
            "TWO_CELLS_EMPTY_SIXTEEN_FIXED_MOVING_ROUTES_RETAINED",
        ):
            assert text in compiler


def mutation_selftest(original: dict) -> int:
    mutations = []

    def add(mutator):
        value = copy.deepcopy(original)
        mutator(value)
        mutations.append(reseal(value))

    add(lambda value: value["full_localization"]["empty"].pop())
    add(lambda value: value["full_localization"]["surviving_two_dimensional"].append("F00-R11"))
    add(lambda value: value["quadratic_route"]["literal_cells"].pop())
    add(lambda value: value["quadratic_route"]["literal_orbit_groups"][0].append("F05-R02"))
    add(lambda value: value["quadratic_route"].__setitem__("rank_drop_retained", "discarded"))
    add(lambda value: value["quadratic_route"]["group_fingerprints"]["F04-R02|F07-R02"]["resultant"].__setitem__(0, 41))
    add(lambda value: value["independent_symbolic_check"].__setitem__("result", [0, 0, 0, 0, 1]))
    add(lambda value: value["conclusion"].__setitem__("remaining_open_cells", 15))
    add(lambda value: value["conclusion"].__setitem__("K3_closed", True))
    add(lambda value: value.__setitem__("terminal", "SAFE"))

    rejected = 0
    for mutation in mutations:
        try:
            validate(mutation, check_files=False)
        except AssertionError:
            rejected += 1
    assert rejected == len(mutations)

    bad_hash = copy.deepcopy(original)
    bad_hash["payload_sha256"] = "0" * 64
    try:
        validate(bad_hash, check_files=False)
    except AssertionError:
        rejected += 1
    assert rejected == len(mutations) + 1
    return rejected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    certificate = json.loads(CERTIFICATE.read_text())
    validate(certificate)
    rejected = mutation_selftest(certificate) if args.tamper_selftest else 0
    if args.check:
        print(
            "PASS "
            f"cells={len(ALL_CELLS)} empty={len(EMPTY)} open={len(ALL_CELLS - EMPTY)} "
            f"quadratic_routes={len(QUADRATIC)} orbits=6 mutations_rejected={rejected} "
            f"payload={certificate['payload_sha256']}"
        )


if __name__ == "__main__":
    main()
