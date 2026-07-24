#!/usr/bin/env python3
"""Exact replay for the M31 quotient T16 mixing-floor counterexample.

The verifier is stdlib-only.  It reconstructs the quotient labels, the pinned
anchor, all 1,225 full-T64 triple-swap neighbors, and the eight T16-mixed
neighbors.  It checks support validity, deficiency 192, the common depth-32
locator prefix, the exact shell arithmetic, canonical JSON, artifact hashes,
and (inside a Git checkout) the read-only predecessor/source blob pins.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import math
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable, Sequence

P = 2**31 - 1
DEPTH = 32
SUPPORT_SIZE = 479
DOMAIN_SIZE = 1022
B_STAR = 16_777_215
B_VIABLE_MAX = 5_191
T32_REMOVED = (5, 21, 27, 29, 31, 39)
T32_ADDED = (13, 19, 33, 37, 43, 63)
T32_POWER_SUM = 1_122_577_494
ROOT = Path(__file__).resolve().parents[2]
CERT_PATH = (
    ROOT
    / "experimental/data/certificates/m31-quotient-t16-mixing-floor"
    / "m31_quotient_t16_mixing_floor.json"
)

INSIDE_T64 = (7, 9, 13, 19, 21, 23, 27)
OUTSIDE_T64 = (5, 11, 15, 17, 25, 29, 31)

# (removed T16 classes, added T16 classes, common first power sum)
MIXED_SPECS: tuple[tuple[tuple[int, ...], tuple[int, ...], int], ...] = (
    (
        (7, 9, 27, 37, 55, 71, 73, 77, 83, 109, 115, 119),
        (5, 11, 17, 25, 39, 47, 53, 69, 79, 93, 99, 113),
        752_337_374,
    ),
    (
        (7, 21, 27, 37, 43, 71, 77, 83, 85, 107, 109, 115),
        (5, 11, 17, 25, 39, 47, 53, 69, 79, 93, 99, 113),
        752_337_374,
    ),
    (
        (7, 23, 27, 37, 41, 71, 77, 83, 87, 105, 109, 115),
        (5, 11, 17, 25, 39, 47, 53, 69, 79, 93, 99, 113),
        752_337_374,
    ),
    (
        (9, 37, 41, 51, 55, 83, 85, 101, 105, 107, 109, 115),
        (5, 25, 31, 33, 47, 69, 75, 89, 93, 99, 111, 117),
        1_029_303_379,
    ),
    (
        (13, 19, 21, 23, 27, 43, 45, 73, 77, 87, 91, 119),
        (11, 17, 29, 35, 39, 53, 59, 81, 95, 97, 103, 123),
        1_118_180_268,
    ),
    (
        (9, 13, 19, 45, 51, 55, 57, 73, 91, 101, 119, 121),
        (15, 29, 35, 49, 59, 75, 81, 89, 103, 111, 117, 123),
        1_395_146_273,
    ),
    (
        (13, 19, 21, 43, 45, 51, 57, 85, 91, 101, 107, 121),
        (15, 29, 35, 49, 59, 75, 81, 89, 103, 111, 117, 123),
        1_395_146_273,
    ),
    (
        (13, 19, 23, 41, 45, 51, 57, 87, 91, 101, 105, 121),
        (15, 29, 35, 49, 59, 75, 81, 89, 103, 111, 117, 123),
        1_395_146_273,
    ),
)


def mul2(u: tuple[int, int], v: tuple[int, int]) -> tuple[int, int]:
    return ((u[0] * v[0] - u[1] * v[1]) % P, (u[0] * v[1] + u[1] * v[0]) % P)


def pow2(u: tuple[int, int], exponent: int) -> tuple[int, int]:
    out = (1, 0)
    while exponent:
        if exponent & 1:
            out = mul2(out, u)
        u = mul2(u, u)
        exponent >>= 1
    return out


def cheb_pow_two(x: int, log_degree: int) -> int:
    for _ in range(log_degree):
        x = (2 * x * x - 1) % P
    return x


def quotient_labels() -> dict[int, int]:
    scale = pow(2, -2047, P)
    generator = (1_717_986_917, 1_288_490_189)
    return {
        r: (scale * pow2(generator, r * 2**19)[0]) % P
        for r in range(1, 2048, 2)
    }


def block_reps(block_size: int, index: int) -> tuple[int, ...]:
    modulus = 4096 // block_size
    return tuple(
        r
        for r in range(1, 2048, 2)
        if r % modulus in (index, modulus - index)
    )


def punctured_reps() -> tuple[int, ...]:
    return tuple(r for r in range(1, 2048, 2) if r not in (1, 3))


def prefix_from_reps(reps: Iterable[int], labels: dict[int, int], depth: int) -> tuple[int, ...]:
    coeffs = [1] + [0] * depth
    for rep in reps:
        root = labels[rep]
        for j in range(depth, 0, -1):
            coeffs[j] = (coeffs[j] - root * coeffs[j - 1]) % P
    return tuple(coeffs[1:])


def full_locator(reps: Iterable[int], labels: dict[int, int]) -> tuple[int, ...]:
    """Return the complete monic locator, in ascending coefficient order."""
    poly = [1]
    for rep in reps:
        root = labels[rep]
        out = [0] * (len(poly) + 1)
        for j, coefficient in enumerate(poly):
            out[j] = (out[j] - root * coefficient) % P
            out[j + 1] = (out[j + 1] + coefficient) % P
        poly = out
    return tuple(poly)


def full_locator_prefix(reps: Iterable[int], labels: dict[int, int], depth: int) -> tuple[int, ...]:
    poly = full_locator(reps, labels)
    assert poly[-1] == 1
    return tuple(reversed(poly[:-1]))[:depth]


def support_hash(reps: Sequence[int]) -> str:
    payload = ",".join(str(x) for x in reps).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def family_hash(supports: Sequence[Sequence[int]]) -> str:
    payload = "\n".join(support_hash(s) for s in supports).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def choose_count_by_product(n: int, k: int) -> int:
    acc = 1
    for j in range(1, k + 1):
        acc = acc * (n - k + j) // j
    return acc


def binomial_by_pascal(n: int, k: int) -> int:
    row = [1]
    for _ in range(n):
        row = [1] + [row[j - 1] + row[j] for j in range(1, len(row))] + [1]
        if len(row) > k + 1:
            row = row[: k + 1]
    return row[k]


def power_by_loop(base: int, exponent: int) -> int:
    out = 1
    for _ in range(exponent):
        out *= base
    return out


def matching_prefix_length(a: Sequence[int], b: Sequence[int], labels: dict[int, int], cap: int = 64) -> int:
    pa = prefix_from_reps(a, labels, cap)
    pb = prefix_from_reps(b, labels, cap)
    for i, (x, y) in enumerate(zip(pa, pb)):
        if x != y:
            return i
    return cap


def build_core() -> dict[str, Any]:
    labels = quotient_labels()
    assert P == 2_147_483_647
    assert len(labels) == 1024 and len(set(labels.values())) == 1024
    domain = punctured_reps()
    assert len(domain) == DOMAIN_SIZE == 1024 - 2

    t64 = {a: block_reps(64, a) for a in range(1, 32, 2)}
    t16 = {a: block_reps(16, a) for a in range(1, 128, 2)}
    assert all(len(v) == 64 for v in t64.values())
    assert all(len(v) == 16 for v in t16.values())

    residual = tuple(r for r in t64[1] if r != 1)[:31]
    anchor_seed = set(residual)
    for a in INSIDE_T64:
        anchor_seed.update(t64[a])
    anchor = tuple(r for r in domain if r in anchor_seed)
    assert len(anchor) == SUPPORT_SIZE == 31 + 7 * 64
    assert len(set(anchor)) == SUPPORT_SIZE
    eta = prefix_from_reps(anchor, labels, DEPTH)
    anchor_full_prefix = full_locator_prefix(anchor, labels, 64)
    assert eta == anchor_full_prefix[:DEPTH]

    anchor_set = set(anchor)
    class_neighbors: list[tuple[int, ...]] = []
    class_specs: list[dict[str, Any]] = []
    for removed in itertools.combinations(INSIDE_T64, 3):
        remove_reps = set(itertools.chain.from_iterable(t64[a] for a in removed))
        for added in itertools.combinations(OUTSIDE_T64, 3):
            add_reps = set(itertools.chain.from_iterable(t64[a] for a in added))
            support_set = (anchor_set - remove_reps) | add_reps
            support = tuple(r for r in domain if r in support_set)
            assert len(support) == SUPPORT_SIZE
            assert len(anchor_set - support_set) == 192 == 3 * 64
            assert prefix_from_reps(support, labels, DEPTH) == eta
            class_neighbors.append(support)
            class_specs.append({"remove_t64": list(removed), "add_t64": list(added)})

    class_closed = choose_count_by_product(7, 3) ** 2
    class_enum = len(tuple(itertools.product(itertools.combinations(INSIDE_T64, 3), itertools.combinations(OUTSIDE_T64, 3))))
    assert class_closed == class_enum == len(class_neighbors) == 1225
    assert len(set(class_neighbors)) == len(class_neighbors)

    t16_rho = {
        a: cheb_pow_two((2 * labels[a]) % P, 4)
        for a in range(1, 128, 2)
    }
    mixed_neighbors: list[tuple[int, ...]] = []
    mixed_records: list[dict[str, Any]] = []
    for removed, added, key in MIXED_SPECS:
        remove_reps = set(itertools.chain.from_iterable(t16[a] for a in removed))
        add_reps = set(itertools.chain.from_iterable(t16[a] for a in added))
        assert len(remove_reps) == len(add_reps) == 192
        assert remove_reps <= anchor_set
        assert add_reps.isdisjoint(anchor_set)

        p1_remove = sum(t16_rho[a] for a in removed) % P
        p1_add = sum(t16_rho[a] for a in added) % P
        p2_remove = sum(t16_rho[a] * t16_rho[a] for a in removed) % P
        p2_add = sum(t16_rho[a] * t16_rho[a] for a in added) % P
        assert p1_remove == p1_add == key
        assert p2_remove == p2_add == 6

        support_set = (anchor_set - remove_reps) | add_reps
        support = tuple(r for r in domain if r in support_set)
        assert len(support) == SUPPORT_SIZE
        assert len(anchor_set - support_set) == 192 == 12 * 16
        assert prefix_from_reps(support, labels, DEPTH) == eta
        match = matching_prefix_length(anchor, support, labels, 64)
        assert match == 47 == SUPPORT_SIZE - (287 + 9 * 16) - 1
        full_prefix = full_locator_prefix(support, labels, 48)
        assert full_prefix[:47] == anchor_full_prefix[:47]
        assert full_prefix[47] != anchor_full_prefix[47]
        mixed_neighbors.append(support)
        mixed_records.append(
            {
                "remove_t16": list(removed),
                "add_t16": list(added),
                "power_sum_1": key,
                "power_sum_2": 6,
                "matching_nonleading_coefficients": match,
                "support_sha256": support_hash(support),
            }
        )


    # Independent secondary A1 falsifier at the T32 level.  Equal first
    # T32-fiber power sums cancel the H^5 coefficient of six-factor products.
    t32 = {a: block_reps(32, a) for a in range(1, 64, 2)}
    t32_rho = {a: cheb_pow_two((2 * labels[a]) % P, 5) for a in range(1, 64, 2)}
    t32_removed_reps = set(itertools.chain.from_iterable(t32[a] for a in T32_REMOVED))
    t32_added_reps = set(itertools.chain.from_iterable(t32[a] for a in T32_ADDED))
    assert len(t32_removed_reps) == len(t32_added_reps) == 6 * 32 == 192
    assert t32_removed_reps.isdisjoint(t32_added_reps)
    assert {1, 3}.isdisjoint(t32_removed_reps | t32_added_reps)
    assert sum(t32_rho[a] for a in T32_REMOVED) % P == T32_POWER_SUM
    assert sum(t32_rho[a] for a in T32_ADDED) % P == T32_POWER_SUM
    assert any((64 - a) not in T32_REMOVED for a in T32_REMOVED)
    assert any((64 - a) not in T32_ADDED for a in T32_ADDED)
    t32_core = tuple(r for r in domain if r not in t32_removed_reps | t32_added_reps)[:287]
    t32_anchor_set = set(t32_core) | t32_removed_reps
    t32_neighbor_set = set(t32_core) | t32_added_reps
    t32_anchor = tuple(r for r in domain if r in t32_anchor_set)
    t32_neighbor = tuple(r for r in domain if r in t32_neighbor_set)
    assert len(t32_core) == 287
    assert len(t32_anchor) == len(t32_neighbor) == SUPPORT_SIZE
    assert len(t32_anchor_set - t32_neighbor_set) == 192
    assert matching_prefix_length(t32_anchor, t32_neighbor, labels, 64) == 63
    assert full_locator_prefix(t32_anchor, labels, 64)[:63] == full_locator_prefix(t32_neighbor, labels, 64)[:63]
    assert full_locator_prefix(t32_anchor, labels, 64)[63] != full_locator_prefix(t32_neighbor, labels, 64)[63]

    assert len(mixed_neighbors) == 8
    assert len(set(mixed_neighbors)) == 8
    assert set(mixed_neighbors).isdisjoint(set(class_neighbors))

    all_neighbors = class_neighbors + mixed_neighbors
    assert len(all_neighbors) == 1233
    assert len(set(all_neighbors)) == 1233
    assert all(prefix_from_reps(s, labels, DEPTH) == eta for s in all_neighbors)
    assert all(len(anchor_set - set(s)) == 192 for s in all_neighbors)

    # Independent direct full-prefix checks at the exact differentiating depths.
    assert SUPPORT_SIZE - (287 + 2 * 64) - 1 == 63
    class_match_63 = all(prefix_from_reps(s, labels, 63) == prefix_from_reps(anchor, labels, 63) for s in class_neighbors)
    class_break_64 = all(prefix_from_reps(s, labels, 64) != prefix_from_reps(anchor, labels, 64) for s in class_neighbors)
    mixed_match_47 = all(prefix_from_reps(s, labels, 47) == prefix_from_reps(anchor, labels, 47) for s in mixed_neighbors)
    mixed_break_48 = all(prefix_from_reps(s, labels, 48) != prefix_from_reps(anchor, labels, 48) for s in mixed_neighbors)
    assert class_match_63 and class_break_64 and mixed_match_47 and mixed_break_48

    h_192_math = math.comb(479, 192) * math.comb(543, 192)
    h_192_product = choose_count_by_product(479, 192) * choose_count_by_product(543, 192)
    h_192_pascal = binomial_by_pascal(479, 192) * binomial_by_pascal(543, 192)
    assert h_192_math == h_192_product == h_192_pascal
    q_32_pow = P**32
    q_32_loop = power_by_loop(P, 32)
    assert q_32_pow == q_32_loop
    assert 4 * h_192_math < q_32_pow
    assert (4 * h_192_math) // q_32_pow == 0

    class_count_second = sum(1 for _ in class_specs)
    mixed_count_second = sum(1 for _ in MIXED_SPECS)
    total_first = class_closed + len(MIXED_SPECS)
    total_second = class_count_second + mixed_count_second
    assert total_first == total_second == 1233

    charge_mul = 1233 * 447
    charge_sum = sum(447 for _ in range(1233))
    assert charge_mul == charge_sum == 551_151
    compiled = 1 + charge_mul + 14_456_476
    compiled_second = 14_456_477 + charge_sum
    assert compiled == compiled_second == 15_007_628
    reserve = B_STAR - compiled
    reserve_second = B_STAR - 14_456_477 - charge_sum
    assert reserve == reserve_second == 1_769_587
    assert 1 + 5191 * 447 + 14_456_476 == 16_776_854
    assert 1 + 5192 * 447 + 14_456_476 == 16_777_301

    return {
        "field": {
            "p": P,
            "generator_fp2": [1_717_986_917, 1_288_490_189],
            "scale_2048": pow(2, -2047, P),
        },
        "domain": {
            "raw_labels": 1024,
            "removed_representatives": [1, 3],
            "quotient_labels": DOMAIN_SIZE,
            "support_size": SUPPORT_SIZE,
            "prefix_depth": DEPTH,
        },
        "anchor": {
            "inside_t64": list(INSIDE_T64),
            "outside_t64": list(OUTSIDE_T64),
            "residual_representatives": list(residual),
            "support_representatives": list(anchor),
            "support_sha256": support_hash(anchor),
            "eta": list(eta),
        },
        "class_swap_family": {
            "remove_classes": 3,
            "add_classes": 3,
            "closed_form": "C(7,3)^2",
            "closed_form_count": class_closed,
            "enumerated_count": class_enum,
            "matching_nonleading_coefficients": 63,
            "breaks_at_nonleading_coefficient": 64,
            "supports_sha256": family_hash(class_neighbors),
        },
        "mixed_t16_family": {
            "count": len(mixed_neighbors),
            "records": mixed_records,
            "matching_nonleading_coefficients": 47,
            "breaks_at_nonleading_coefficient": 48,
            "supports_sha256": family_hash(mixed_neighbors),
        },
        "secondary_t32_falsifier": {
            "removed_t32": list(T32_REMOVED),
            "added_t32": list(T32_ADDED),
            "common_power_sum_1": T32_POWER_SUM,
            "common_core_size": len(t32_core),
            "deficiency": 192,
            "matching_nonleading_coefficients": 63,
            "breaks_at_nonleading_coefficient": 64,
            "anchor_sha256": support_hash(t32_anchor),
            "neighbor_sha256": support_hash(t32_neighbor),
            "neither_side_is_a_union_of_full_t64_classes": True,
        },
        "witness": {
            "deficiency": 192,
            "class_swap_neighbors": len(class_neighbors),
            "non_class_neighbors": len(mixed_neighbors),
            "total_distinct_neighbors": len(all_neighbors),
            "all_supports_sha256": family_hash(all_neighbors),
            "a1_classification_refuted": True,
        },
        "shell": {
            "H_192": h_192_math,
            "p_power_32": q_32_pow,
            "four_H_192_lt_p_power_32": True,
            "floor_four_H_192_over_p_power_32": 0,
        },
        "compiler": {
            "old_floor": 6,
            "new_certified_floor": 1233,
            "largest_viable_uniform_intercept": B_VIABLE_MAX,
            "viable_window": [1233, B_VIABLE_MAX],
            "intercept_charge_1233": charge_mul,
            "compiled_bound_at_1233": compiled,
            "reserve_at_1233": reserve,
            "compiled_bound_at_5191": 16_776_854,
            "compiled_bound_at_5192": 16_777_301,
            "B_star": B_STAR,
        },
        "remaining_requirement": {
            "band": "uniform d_e(A) <= b for 33 <= e <= 213 with 1233 <= b <= 5191 remains open",
            "post_crossover": "for 214 <= e <= 479, d_e(A) <= b + floor(4 H_e / p^32) remains required",
            "B1_e64": "not certified",
            "B2_5192": "not certified",
        },
    }


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git_blob(path: Path) -> str:
    proc = subprocess.run(
        ["git", "hash-object", str(path.relative_to(ROOT))],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    return proc.stdout.strip()


def validate_against_core(data: dict[str, Any], core: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("schema_version") != 1:
        errors.append("schema_version")
    if data.get("packet") != "m31-quotient-t16-mixing-floor":
        errors.append("packet")
    if data.get("status") != "COUNTEREXAMPLE_NEW_FLOOR":
        errors.append("status")
    if data.get("computed") != core:
        errors.append("computed")
    if data.get("terminal") != "COUNTEREXAMPLE_NEW_FLOOR":
        errors.append("terminal")
    return errors


# Transport-only files: carried by the PR bundle, deliberately never imported
# upstream.  The certificate still records their hashes as provenance, so the
# recorded values are cross-checked here while their absence is not an error.
LEGACY_PACKET_FILE_SHA256 = {
    "PR_BODY.md":
        "8c4c1fa2a9f675a516cd9268f0831c759d3721b6e6a75070ef594b77460f6f89",
    "experimental/agents-log-entry-gptpro-m31-quotient-t16-mixing-floor.md":
        "4b30f9ef3fb3042069d48b5bbf338a64194faee867bf0c3fff3fd8f25be2eefe",
}


def validate_artifacts(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    manifest = data.get("artifact_sha256", {})
    for rel, expected in sorted(manifest.items()):
        legacy = LEGACY_PACKET_FILE_SHA256.get(rel)
        if legacy is not None:
            if legacy != expected:
                errors.append(f"legacy transport hash {rel}")
            continue
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"missing artifact {rel}")
        elif sha256_file(path) != expected:
            errors.append(f"artifact hash {rel}")
    return errors


def validate_source_pins(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not (ROOT / ".git").exists():
        return errors
    parent = data["provenance"]["parent_head"]
    anc = subprocess.run(
        ["git", "merge-base", "--is-ancestor", parent, "HEAD"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if anc.returncode != 0:
        errors.append("parent head is not an ancestor")
    for rel, expected in sorted(data.get("source_git_blobs", {}).items()):
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"missing source {rel}")
        elif git_blob(path) != expected:
            errors.append(f"source blob {rel}")
    return errors


def canonical_bytes(data: dict[str, Any]) -> bytes:
    return (json.dumps(data, sort_keys=True, indent=2) + "\n").encode("utf-8")


def run_check(data: dict[str, Any], *, quiet: bool = False) -> None:
    core = build_core()
    errors = validate_against_core(data, core)
    errors.extend(validate_artifacts(data))
    errors.extend(validate_source_pins(data))
    raw = CERT_PATH.read_bytes()
    if raw != canonical_bytes(data):
        errors.append("certificate is not canonical JSON")
    if errors:
        raise AssertionError("; ".join(errors))
    if not quiet:
        print("PASS m31 quotient T16 mixing floor")
        print("anchor=479, deficiency=192, class_swaps=1225, mixed=8, total=1233")
        print("floor(4*H_192/p^32)=0, intercept_floor=1233")
        print("compiled(1233)=15007628, reserve=1769587")


def run_tamper_selftest(data: dict[str, Any]) -> None:
    core = build_core()
    assert not validate_against_core(data, core)
    mutations: list[tuple[str, Any]] = []

    def add_mutation(name: str, mutate: Any) -> None:
        item = copy.deepcopy(data)
        mutate(item)
        mutations.append((name, item))

    add_mutation("neighbor count", lambda d: d["computed"]["witness"].__setitem__("total_distinct_neighbors", 1232))
    add_mutation("eta", lambda d: d["computed"]["anchor"]["eta"].__setitem__(0, 0))
    add_mutation("mixed key", lambda d: d["computed"]["mixed_t16_family"]["records"][0].__setitem__("power_sum_1", 1))
    add_mutation("class count", lambda d: d["computed"]["class_swap_family"].__setitem__("closed_form_count", 1224))
    add_mutation("intercept floor", lambda d: d["computed"]["compiler"].__setitem__("new_certified_floor", 1232))
    add_mutation("terminal", lambda d: d.__setitem__("terminal", "OPEN GAP"))

    for name, item in mutations:
        if not validate_against_core(item, core):
            raise AssertionError(f"mutation escaped: {name}")
    print(f"PASS tamper selftest ({len(mutations)} mutations rejected)")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args(argv)

    data = json.loads(CERT_PATH.read_text(encoding="utf-8"))
    if args.check:
        run_check(data)
    else:
        run_tamper_selftest(data)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, KeyError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
