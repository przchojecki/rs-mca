#!/usr/bin/env python3
"""Verify the KoalaBear m4 A6/S6 genus-zero passport reduction."""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
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
CERTIFICATE = EXPERIMENTAL / "data" / "certificates" / "kb-mca-v4-m4-a6s6-genus-zero-passport-reduction-v1" / "kb_mca_v4_m4_a6s6_genus_zero_passport_reduction_v1.json"
PARENT_COMMIT = "d7232a30a5cca4a42330422415da71f06a7c5a31"
PARENT_PATH = "experimental/data/certificates/kb-mca-v4-m4-outer-a6s6-route-cut-v1/kb_mca_v4_m4_outer_a6s6_route_cut_v1.json"
PARENT_BLOB = "bb130d089d1ca7c0fcab04b65f66de773952ceb2"
PARENT_PAYLOAD = "61a8db82285f22393fc2af6c1d35224d79587fa150009270d42ac33972557485"
LETTERS = tuple(range(6))
PAIRS = tuple(itertools.combinations(LETTERS, 2))
PAIR_INDEX = {pair: index for index, pair in enumerate(PAIRS)}


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


def exact_keys(value: Any, expected: set[str], label: str) -> None:
    require(isinstance(value, dict), f"{label} is not an object")
    require(set(value) == expected, f"{label} keys differ: {sorted(set(value) ^ expected)}")


def git_output(*args: str) -> str:
    try:
        result = subprocess.run(
            ["git", *args], cwd=REPO_ROOT, check=True, capture_output=True, text=True
        )
    except subprocess.CalledProcessError as error:
        raise VerificationError(error.stderr.strip()) from error
    return result.stdout.strip()


def cycle_type(permutation: tuple[int, ...]) -> tuple[int, ...]:
    unseen = set(range(len(permutation)))
    lengths = []
    while unseen:
        start = min(unseen)
        point = start
        orbit = []
        while point not in orbit:
            orbit.append(point)
            unseen.remove(point)
            point = permutation[point]
        lengths.append(len(orbit))
    return tuple(sorted(lengths, reverse=True))


def label(cycles: tuple[int, ...]) -> str:
    return ".".join(map(str, cycles))


def on_pairs(permutation: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        PAIR_INDEX[tuple(sorted((permutation[left], permutation[right])))]
        for left, right in PAIRS
    )


def compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[point]] for point in LETTERS)


def inverse(permutation: tuple[int, ...]) -> tuple[int, ...]:
    result = [0] * 6
    for point, image in enumerate(permutation):
        result[image] = point
    return tuple(result)


def generated_order(generators: tuple[tuple[int, ...], ...]) -> int:
    steps = generators + tuple(inverse(generator) for generator in generators)
    group = {LETTERS}
    pending = [LETTERS]
    while pending:
        current = pending.pop()
        for step in steps:
            candidate = compose(current, step)
            if candidate not in group:
                group.add(candidate)
                pending.append(candidate)
    return len(group)


def reconstruct() -> tuple[list, list, list]:
    classes: dict[tuple[int, ...], list[tuple[int, ...]]] = {}
    pair_types: dict[tuple[int, ...], tuple[int, ...]] = {}
    for permutation in itertools.permutations(LETTERS):
        kind = cycle_type(permutation)
        pair_kind = cycle_type(on_pairs(permutation))
        classes.setdefault(kind, []).append(permutation)
        pair_types.setdefault(kind, pair_kind)
        require(pair_types[kind] == pair_kind, "pair type varies inside a class")
    require(len(classes) == 11 and sum(map(len, classes.values())) == 720, "class coverage")

    class_rows = []
    class_index = {}
    class_parity = {}
    for kind in sorted(classes):
        index = 15 - len(pair_types[kind])
        parity = (6 - len(kind)) % 2
        class_index[kind] = index
        class_parity[kind] = parity
        class_rows.append(
            [label(kind), len(classes[kind]), "odd" if parity else "even", label(pair_types[kind]), index]
        )

    nonidentity = [kind for kind in sorted(classes) if class_index[kind] > 0]
    candidates = []
    for length in range(2, 5):
        for kinds in itertools.combinations_with_replacement(nonidentity, length):
            if sum(class_index[kind] for kind in kinds) != 16:
                continue
            odd_count = sum(class_parity[kind] for kind in kinds)
            if odd_count % 2 == 0:
                ambient = "A6" if odd_count == 0 else "S6"
                candidates.append((kinds, ambient, odd_count))
    require(len(candidates) == 9, "necessary passport count")
    candidates.sort(key=lambda row: row[0])
    necessary = [
        [ambient, [label(kind) for kind in kinds], [class_index[kind] for kind in kinds], odd_count]
        for kinds, ambient, odd_count in candidates
    ]

    pole_5a = (1, 2, 3, 4, 0, 5)
    pole_5b = compose(pole_5a, pole_5a)
    tuple_rows = []
    for kinds, ambient, _ in candidates:
        target = 360 if ambient == "A6" else 720
        poles = [("5A", pole_5a), ("5B", pole_5b)] if target == 360 else [("5A", pole_5a)]
        pole_rows = []
        for pole_name, pole in poles:
            orders: Counter[int] = Counter()
            for prefix in itertools.product(*(classes[kind] for kind in kinds[:-1])):
                running = pole
                for branch_cycle in prefix:
                    running = compose(running, branch_cycle)
                final = inverse(running)
                if cycle_type(final) != kinds[-1]:
                    continue
                orders[generated_order((pole,) + prefix + (final,))] += 1
            product_one_count = sum(orders.values())
            pole_rows.append(
                [pole_name, product_one_count, {str(order): count for order, count in sorted(orders.items())}, orders[target]]
            )
        realized = any(row[3] > 0 for row in pole_rows)
        tuple_rows.append([[label(kind) for kind in kinds], target, pole_rows, realized])
    return class_rows, necessary, tuple_rows


def verify_schema(data: dict[str, Any]) -> None:
    exact_keys(data, {"payload_sha256", "statement", "parent_route_cut", "input", "class_rows", "necessary_passports", "tuple_audit", "conclusion", "source_bindings", "nonclaims"}, "certificate")
    exact_keys(data["statement"], {"schema", "terminal"}, "statement")
    exact_keys(data["parent_route_cut"], {"commit", "certificate_path", "certificate_blob_oid", "certificate_payload_sha256", "imported_terminal", "imported_survivor", "mandatory_pair_cycle_type"}, "parent")
    exact_keys(data["input"], {"degree", "genus_zero_total_index", "mandatory_letter_class", "mandatory_pair_cycle_type", "mandatory_index", "residual_index_budget"}, "input")
    exact_keys(data["conclusion"], {"necessary_passport_count", "realized_passport_count", "retained", "three_point_count", "four_point_count", "terminal"}, "conclusion")
    exact_keys(data["source_bindings"], {"enumerated_group", "group_order", "action", "largest_prefix_count", "arithmetic"}, "source bindings")


def verify_parent(data: dict[str, Any], check_git: bool) -> None:
    expected = {"commit": PARENT_COMMIT, "certificate_path": PARENT_PATH, "certificate_blob_oid": PARENT_BLOB, "certificate_payload_sha256": PARENT_PAYLOAD, "imported_terminal": "M4_ONLY_R8_DELTA2_A6S6_OUTER_SURVIVES", "imported_survivor": [8, 2, "A6_or_S6_two_subsets"], "mandatory_pair_cycle_type": [5, 5, 5]}
    require(data["parent_route_cut"] == expected, "parent binding")
    if not check_git:
        return
    require(git_output("rev-parse", f"{PARENT_COMMIT}:{PARENT_PATH}") == PARENT_BLOB, "parent blob")
    parent = parse_json(git_output("show", f"{PARENT_COMMIT}:{PARENT_PATH}"), "parent certificate")
    require(payload_hash(parent) == parent["payload_sha256"] == PARENT_PAYLOAD, "parent payload")
    require(parent["conclusion"]["terminal"] == expected["imported_terminal"], "parent terminal")
    require(parent["conclusion"]["surviving_m4_rows"] == [[8, 2]], "parent survivor")
    require(parent["survivor"]["pole_cycle_type"] == [5, 5, 5], "parent pole")


def verify_certificate(data: dict[str, Any], check_git: bool = True, expected=None) -> None:
    verify_schema(data)
    require(payload_hash(data) == data["payload_sha256"], "payload hash")
    verify_parent(data, check_git)
    require(data["statement"] == {"schema": "kb-mca-v4-m4-a6s6-genus-zero-passport-reduction-v1", "terminal": "M4_A6S6_GEOMETRIC_FRONTIER_FOUR_PASSPORTS"}, "statement")
    require(data["input"] == {"degree": 15, "genus_zero_total_index": 28, "mandatory_letter_class": "5.1", "mandatory_pair_cycle_type": "5.5.5", "mandatory_index": 12, "residual_index_budget": 16}, "input")
    if expected is None:
        expected = reconstruct()
    require(data["class_rows"] == expected[0], "class rows")
    require(data["necessary_passports"] == expected[1], "necessary passports")
    require(data["tuple_audit"] == expected[2], "tuple audit")
    require(data["conclusion"] == {"necessary_passport_count": 9, "realized_passport_count": 4, "retained": [["A6", ["5.1", "2.2.1.1", "4.2"]], ["S6", ["5.1", "2.1.1.1.1", "2.2.1.1", "2.2.2"]], ["S6", ["5.1", "2.1.1.1.1", "6"]], ["S6", ["5.1", "2.2.2", "3.2.1"]]], "three_point_count": 3, "four_point_count": 1, "terminal": "M4_A6S6_GEOMETRIC_FRONTIER_FOUR_PASSPORTS"}, "conclusion")
    require(data["source_bindings"] == {"enumerated_group": "S6", "group_order": 720, "action": "two_subsets_of_six_letters", "largest_prefix_count": 3375, "arithmetic": "exact_integer_permutation_composition"}, "source bindings")
    require(data["nonclaims"] == ["no challenge-field descent", "no split-zero or split-pole payment", "no quartic source-star incidence", "no surviving m4 type deletion", "no KoalaBear row or ledger closure"], "nonclaims")


def reseal(data: dict[str, Any]) -> None:
    data["payload_sha256"] = payload_hash(data)


def tamper_selftest(original: dict[str, Any], expected) -> int:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("budget", lambda row: row["input"].__setitem__("residual_index_budget", 15)),
        ("class-index", lambda row: row["class_rows"][1].__setitem__(4, 5)),
        ("class-type", lambda row: row["class_rows"][9].__setitem__(3, "5.5.1.1.1.1.1")),
        ("drop-budget", lambda row: row["necessary_passports"].pop()),
        ("short-budget", lambda row: row["necessary_passports"][0][1].pop()),
        ("generate-deleted", lambda row: row["tuple_audit"][0][2][0].__setitem__(3, 1)),
        ("delete-retained", lambda row: row["tuple_audit"][2].__setitem__(3, False)),
        ("drop-5B", lambda row: row["tuple_audit"][5][2].pop()),
        ("count", lambda row: row["conclusion"].__setitem__("realized_passport_count", 5)),
        ("retained", lambda row: row["conclusion"]["retained"].pop()),
        ("parent", lambda row: row["parent_route_cut"].__setitem__("certificate_blob_oid", "0" * 40)),
        ("nonclaim", lambda row: row["nonclaims"].pop()),
        ("extra", lambda row: row.__setitem__("extra", 1)),
    ]
    passed = 0
    for name, mutate in mutations:
        candidate = copy.deepcopy(original)
        mutate(candidate)
        reseal(candidate)
        try:
            verify_certificate(candidate, False, expected)
        except VerificationError:
            passed += 1
        else:
            raise VerificationError(f"tamper survived: {name}")
    bad_hash = copy.deepcopy(original)
    bad_hash["payload_sha256"] = "0" * 64
    try:
        verify_certificate(bad_hash, False, expected)
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
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    if not args.check and not args.tamper_selftest:
        parser.error("at least one action is required")
    data = parse_json(CERTIFICATE.read_text(), str(CERTIFICATE))
    expected = reconstruct()
    verify_certificate(data, True, expected)
    print("PASS: m4 A6/S6 geometric frontier has four passports")
    if args.tamper_selftest:
        count = tamper_selftest(data, expected)
        print(f"PASS: {count}/{count} tamper mutations rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
