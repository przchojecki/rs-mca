#!/usr/bin/env python3
"""Verify the primitive A4/PRE boundary audit and planted-pair regression."""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import math
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any


THEOREM_ID = "primitive-a4-pre-boundary-v1"
STATUS = "AUDIT / PROVED EQUIVALENCE / COUNTEREXAMPLE GUARDRAIL"
SEED = 20260711
SOURCE_BASE = "36de5bfc"

REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental/notes/audits/primitive_a4_pre_boundary_v1.md"
CERT = (
    REPO
    / "experimental/data/certificates/primitive-a4-pre-boundary-v1"
    / "primitive_a4_pre_boundary_v1.json"
)

REQUIRED_NOTE_MARKERS = (
    "Status: AUDIT / PROVED LOGICAL EQUIVALENCE / COUNTEREXAMPLE GUARDRAIL",
    "L^{-1}R_*^q\\le\\Gamma_q\\le R_*^{q-1}",
    "Primitive fixed-composition rectangle evasiveness (PRE)",
    "Proposition 5.1 (qualified PRE/Q/Sidon equivalence)",
    "Without those two printed hypotheses, this note claims only the definitional",
    "A4 + moment accessibility + Boolean high-energy theorem => primitive Q",
    "NOT PROVED:",
)

FORBIDDEN_NOTE_MARKERS = (
    "A4 from algebraic first-match removal is proved",
    "unconditional asymptotic profile-envelope theorem is proved",
    "PRE is proved for every source-derived primitive residual",
)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def payload_hash(payload: dict[str, Any]) -> str:
    unsigned = dict(payload)
    unsigned.pop("payload_sha256", None)
    return hashlib.sha256(canonical_bytes(unsigned)).hexdigest()


def choose_masks(n: int, weight: int) -> list[int]:
    return [sum(1 << i for i in comb) for comb in itertools.combinations(range(n), weight)]


def bit(mask: int, i: int) -> int:
    return (mask >> i) & 1


def pair_sum_key(a: int, b: int, width: int) -> tuple[int, ...]:
    return tuple(bit(a, i) + bit(b, i) for i in range(width))


def exact_middle_slice_energy(b: int) -> int:
    if b % 2:
        raise ValueError("B must be even")
    k = b // 2
    return math.comb(2 * k, k) * sum(
        math.comb(k, r) ** 2 * math.comb(2 * (k - r), k - r)
        for r in range(k + 1)
    )


def brute_middle_slice_energy(b: int) -> int:
    masks = choose_masks(b, b // 2)
    reps = Counter(pair_sum_key(a, c, b) for a in masks for c in masks)
    return sum(value * value for value in reps.values())


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def next_prime(value: int) -> int:
    candidate = max(2, value)
    if candidate > 2 and candidate % 2 == 0:
        candidate += 1
    while not is_prime(candidate):
        candidate += 1 if candidate == 2 else 2
    return candidate


def planted_row(b: int, q: int = 5) -> dict[str, Any]:
    if b % 2:
        raise ValueError("B must be even")
    powers = [q ** (i + 1) for i in range(b)]
    c = 4 * sum(powers) + 1
    weights: list[int] = []
    for value in powers:
        weights.extend((value, c - value))
    if len(set(weights)) != 2 * b or min(weights) <= 0:
        raise AssertionError("weights are not distinct and nonzero")

    p = next_prime(2 * b * c + 1)
    points = list(range(1, 2 * b + 1))
    if p <= 2 * b * c or len(set(point % p for point in points)) != 2 * b:
        raise AssertionError("finite-field no-wrap or evaluation-point guard failed")
    if any(weight % p == 0 for weight in weights):
        raise AssertionError("zero finite-field column weight")

    fibers: Counter[int] = Counter()
    finite_field_fibers: Counter[int] = Counter()
    delta_fibers: dict[tuple[int, ...], int] = {}
    delta_counts: Counter[tuple[int, ...]] = Counter()
    for support in itertools.combinations(range(2 * b), b):
        mask = set(support)
        image = sum(weights[i] for i in support)
        fibers[image] += 1
        finite_field_fibers[image % p] += 1
        delta = tuple(
            int(2 * i in mask) - int(2 * i + 1 in mask) for i in range(b)
        )
        r_value = sum(int(2 * i + 1 in mask) for i in range(b))
        key = (r_value,) + delta
        delta_counts[key] += 1
        previous = delta_fibers.setdefault(key, image)
        if previous != image:
            raise AssertionError("(r,delta) does not determine image")

    m = math.comb(2 * b, b)
    expected_l = (3**b + 1) // 2
    expected_max = math.comb(b, b // 2)
    if len(fibers) != expected_l:
        raise AssertionError("image-size formula failed")
    if finite_field_fibers != fibers:
        raise AssertionError("finite-field image census differs from integer no-wrap census")
    if len(delta_fibers) != expected_l or len(set(delta_fibers.values())) != expected_l:
        raise AssertionError("(r,delta) labels are not in bijection with the image")
    if sum(fibers.values()) != m:
        raise AssertionError("full-slice size failed")
    if max(fibers.values()) != expected_max:
        raise AssertionError("maximum-fiber formula failed")
    for key, count in delta_counts.items():
        delta = key[1:]
        support_size = sum(value != 0 for value in delta)
        expected_count = math.comb(b - support_size, (b - support_size) // 2)
        if count != expected_count or fibers[delta_fibers[key]] != expected_count:
            raise AssertionError("individual fiber-size formula failed")

    formula_energy = exact_middle_slice_energy(b)
    brute_energy = brute_middle_slice_energy(b)
    if formula_energy != brute_energy:
        raise AssertionError("middle-slice energy formula failed")

    ratio = Fraction(expected_l * expected_max, m)
    delta = Fraction(formula_energy, expected_max**3)
    return {
        "B": b,
        "N": 2 * b,
        "M": m,
        "L": expected_l,
        "max_fiber": expected_max,
        "max_over_image_average": {
            "numerator": ratio.numerator,
            "denominator": ratio.denominator,
        },
        "heavy_energy": formula_energy,
        "normalized_energy": {
            "numerator": delta.numerator,
            "denominator": delta.denominator,
        },
        "log_ratio_per_B": math.log(float(ratio)) / b,
        "log_delta_per_B": math.log(float(delta)) / b,
        "finite_field_realization": {
            "p": p,
            "R": 1,
            "evaluation_points": points,
            "weights_nonzero": True,
            "one_column_minors_nonzero": 2 * b,
            "no_wrap_bound": 2 * b * c,
            "image_census_matches_integer_model": True,
        },
    }


def verify_moment_sandwich() -> list[dict[str, Any]]:
    cases = (
        ([0, 1, 3], 6),
        ([2, 2, 2, 2], 10),
        ([0, 0, 5, 1], 9),
        ([1, 4, 2, 0, 3], 12),
    )
    output = []
    for counts, full_mass in cases:
        l_value = len(counts)
        if sum(counts) > full_mass:
            raise AssertionError("residual mass exceeds full mass")
        ratios = [Fraction(value * l_value, full_mass) for value in counts]
        r_star = max(ratios)
        average = sum(ratios, Fraction()) / l_value
        for q_value in (2, 3, 5):
            gamma = sum((value**q_value for value in ratios), Fraction()) / l_value
            lower = r_star**q_value / l_value
            upper = r_star ** (q_value - 1) * average
            if not (lower <= gamma <= upper <= r_star ** (q_value - 1)):
                raise AssertionError("max-moment sandwich failed")
        output.append(
            {
                "counts": counts,
                "full_mass": full_mass,
                "residual_average_ratio": float(average),
                "max_ratio": float(r_star),
                "orders_checked": [2, 3, 5],
            }
        )
    return output


def determinant_mod(matrix: list[list[int]], p: int) -> int:
    work = [[value % p for value in row] for row in matrix]
    det = 1
    for col in range(len(work)):
        pivot = next((row for row in range(col, len(work)) if work[row][col]), None)
        if pivot is None:
            return 0
        if pivot != col:
            work[pivot], work[col] = work[col], work[pivot]
            det = -det
        pivot_value = work[col][col]
        det = det * pivot_value % p
        inverse = pow(pivot_value, -1, p)
        for row in range(col + 1, len(work)):
            factor = work[row][col] * inverse % p
            for j in range(col, len(work)):
                work[row][j] = (work[row][j] - factor * work[col][j]) % p
    return det % p


def verify_weighted_vandermonde() -> dict[str, Any]:
    p = 101
    n = 8
    rank = 3
    points = list(range(1, n + 1))
    weights = [2 * i + 1 for i in range(1, n + 1)]
    checked = 0
    for columns in itertools.combinations(range(n), rank):
        matrix = [
            [weights[j] * pow(points[j], degree, p) % p for j in columns]
            for degree in range(rank)
        ]
        if determinant_mod(matrix, p) == 0:
            raise AssertionError("weighted Vandermonde minor vanished")
        checked += 1
    return {"p": p, "N": n, "R": rank, "minors_checked": checked}


def build_payload() -> dict[str, Any]:
    rows = [planted_row(b) for b in (2, 4, 6, 8)]
    payload: dict[str, Any] = {
        "theorem_id": THEOREM_ID,
        "status": STATUS,
        "source_base_commit": SOURCE_BASE,
        "seed": SEED,
        "claims": [
            "exact finite max-moment sandwich",
            "exact planted-pair image and fiber census",
            "exact middle-slice additive-energy formula",
            "weighted-Vandermonde MDS minor check",
            "same-family finite-field weighted-Vandermonde realization",
            "qualified PRE/Q/Sidon equivalence under accessibility and Boolean high energy",
        ],
        "nonclaims": [
            "no proof of A4 from first-match removal",
            "no source-derived PRE theorem",
            "no Sidon or signed large-sieve payment",
            "no unconditional asymptotic profile-envelope theorem",
        ],
        "moment_sandwich": verify_moment_sandwich(),
        "planted_pair_rows": rows,
        "weighted_vandermonde": verify_weighted_vandermonde(),
        "asymptotic_targets": {
            "log_ratio_per_B": math.log(1.5),
            "log_normalized_energy_per_B": -math.log(4.0 / 3.0),
        },
    }
    payload["payload_sha256"] = payload_hash(payload)
    return payload


def validate_note() -> None:
    text = NOTE.read_text(encoding="utf-8")
    for marker in REQUIRED_NOTE_MARKERS:
        if marker not in text:
            raise AssertionError(f"missing note marker: {marker}")
    for marker in FORBIDDEN_NOTE_MARKERS:
        if marker in text:
            raise AssertionError(f"forbidden overclaim: {marker}")


def validate_payload(actual: dict[str, Any], expected: dict[str, Any]) -> None:
    if actual.get("payload_sha256") != payload_hash(actual):
        raise AssertionError("certificate payload hash mismatch")
    if actual != expected:
        raise AssertionError("certificate does not match deterministic recomputation")
    if actual["status"] != STATUS:
        raise AssertionError("status drift")
    if not actual["nonclaims"]:
        raise AssertionError("nonclaims missing")


def tamper_selftest(expected: dict[str, Any]) -> int:
    mutations: list[dict[str, Any]] = []
    item = copy.deepcopy(expected)
    item["status"] = "PROVED PRIMITIVE Q"
    mutations.append(item)
    item = copy.deepcopy(expected)
    item["planted_pair_rows"][1]["L"] += 1
    mutations.append(item)
    item = copy.deepcopy(expected)
    item["planted_pair_rows"][2]["heavy_energy"] += 1
    mutations.append(item)
    item = copy.deepcopy(expected)
    item["planted_pair_rows"][3]["finite_field_realization"]["p"] += 2
    mutations.append(item)
    item = copy.deepcopy(expected)
    item["nonclaims"] = []
    mutations.append(item)
    item = copy.deepcopy(expected)
    item["payload_sha256"] = "0" * 64
    mutations.append(item)

    rejected = 0
    for mutation in mutations:
        try:
            validate_payload(mutation, expected)
        except AssertionError:
            rejected += 1
    if rejected != len(mutations):
        raise AssertionError("tamper self-test did not reject every mutation")
    return rejected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write deterministic certificate")
    parser.add_argument("--check", action="store_true", help="check committed certificate and note")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    expected = build_payload()
    if args.write:
        CERT.parent.mkdir(parents=True, exist_ok=True)
        CERT.write_text(json.dumps(expected, indent=2) + "\n", encoding="utf-8")
        print(f"wrote: {CERT.relative_to(REPO)}")

    if args.check or not (args.write or args.tamper_selftest):
        validate_note()
        actual = json.loads(CERT.read_text(encoding="utf-8"))
        validate_payload(actual, expected)

    if args.tamper_selftest:
        print(f"tamper_mutations_rejected: {tamper_selftest(expected)}")

    last = expected["planted_pair_rows"][-1]
    print(f"theorem_id: {THEOREM_ID}")
    print(f"status: {STATUS}")
    print(f"finite_rows: {len(expected['planted_pair_rows'])}")
    print(
        "B=8: "
        f"M={last['M']} L={last['L']} max_fiber={last['max_fiber']} "
        f"energy={last['heavy_energy']} p={last['finite_field_realization']['p']}"
    )
    print("moment_sandwich: PASS")
    print("weighted_vandermonde: PASS")
    print("result: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
