#!/usr/bin/env python3
"""Replay the C9 literal-interface counterexample audit packet.

This verifier checks a finite k=5 instance of the asymptotic family from
experimental/notes/audits/c9_literal_interface_counterexample_v1.md.  It does
not claim that the example survives the intended, currently informal C1--C8
first-match predicates.
"""

from __future__ import annotations

import argparse
import copy
import itertools
import json
import math
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Iterator, Sequence


REPO_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = REPO_ROOT / "experimental/data/c9_literal_interface_counterexample_v1.json"
NOTE = REPO_ROOT / "experimental/notes/audits/c9_literal_interface_counterexample_v1.md"


def balanced_words(k: int) -> Iterator[tuple[int, ...]]:
    """Yield words with exactly k/5 copies of every digit in 0,...,4."""
    if k <= 0 or k % 5:
        raise ValueError("k must be a positive multiple of 5")
    counts = [k // 5] * 5
    word = [0] * k

    def rec(pos: int) -> Iterator[tuple[int, ...]]:
        if pos == k:
            yield tuple(word)
            return
        for digit in range(5):
            if counts[digit] == 0:
                continue
            counts[digit] -= 1
            word[pos] = digit
            yield from rec(pos + 1)
            counts[digit] += 1

    yield from rec(0)


def prefix_support(c: Sequence[int]) -> int:
    """Encode the block-prefix support associated with c as an N-bit mask."""
    mask = 0
    for i, count in enumerate(c):
        for j in range(count):
            mask |= 1 << (4 * i + j)
    return mask


def heavy_support(bits: Sequence[int]) -> int:
    """Choice 0 uses local positions {0,3}; choice 1 uses {1,2}."""
    mask = 0
    for i, bit in enumerate(bits):
        local = (0, 3) if bit == 0 else (1, 2)
        for j in local:
            mask |= 1 << (4 * i + j)
    return mask


def support_sum(mask: int, points: Sequence[int]) -> int:
    return sum(point for i, point in enumerate(points) if (mask >> i) & 1)


def brute_energy(masks: Sequence[int], n: int) -> int:
    """Compute energy in Z^N by counting ordered Boolean differences."""
    full = (1 << n) - 1
    counts: Counter[tuple[int, int]] = Counter()
    for x in masks:
        for y in masks:
            counts[(x & (~y & full), y & (~x & full))] += 1
    return sum(multiplicity * multiplicity for multiplicity in counts.values())


def build_certificate(k: int, brute: bool) -> dict[str, object]:
    if k <= 0 or k % 5:
        raise ValueError("k must be a positive multiple of 5")

    n = 4 * k
    m = 2 * k
    r = 2
    qbase = 100 * k + 1
    bases = [qbase**i for i in range(k)]
    points = [base + offset for base in bases for offset in range(4)]
    total_point_sum = sum(points)

    heavy_masks = [
        heavy_support(bits) for bits in itertools.product((0, 1), repeat=k)
    ]
    heavy_images = {
        (mask.bit_count(), support_sum(mask, points)) for mask in heavy_masks
    }
    if len(heavy_images) != 1:
        raise AssertionError("heavy supports do not form one Phi-fiber")
    heavy_image = next(iter(heavy_images))

    singleton_masks: list[int] = []
    singleton_images: list[tuple[int, int]] = []
    for word in balanced_words(k):
        mask = prefix_support(word)
        singleton_masks.append(mask)
        singleton_images.append((mask.bit_count(), support_sum(mask, points)))

    expected_singletons = math.factorial(k) // (math.factorial(k // 5) ** 5)
    if len(singleton_masks) != expected_singletons:
        raise AssertionError("balanced-word count mismatch")

    heavy_size = 2**k
    image_size = expected_singletons + 1
    domain_size = expected_singletons + heavy_size
    barn = Fraction(domain_size, image_size)
    energy_formula = 6**k
    delta = Fraction(energy_formula, heavy_size**3)
    sigma = math.log(4.0 / 3.0) / 8.0
    qlog = math.ceil(math.log(max(n, 3)))
    log_lower = (
        -math.log(image_size)
        + qlog * (math.log(heavy_size) - math.log(float(barn)))
    )
    normalized_lower = log_lower / (n * qlog)

    brute_match = True
    if brute:
        if heavy_size > 4096:
            raise ValueError("brute energy requires k <= 12")
        brute_match = brute_energy(heavy_masks, n) == energy_formula

    checks = {
        "all_fixed_weight": all(
            mask.bit_count() == m for mask in heavy_masks + singleton_masks
        ),
        "heavy_same_image": len(heavy_images) == 1,
        "singleton_images_distinct": (
            len(set(singleton_images)) == len(singleton_images)
        ),
        "singleton_images_avoid_heavy": heavy_image not in set(singleton_images),
        "support_families_disjoint": (
            set(heavy_masks).isdisjoint(singleton_masks)
        ),
        "integer_no_wrap_threshold_valid": (
            max(support_sum(mask, points) for mask in heavy_masks + singleton_masks)
            <= total_point_sum
        ),
        "sidon_cut_contains_heavy_fiber": (
            float(delta) <= math.exp(-sigma * n)
        ),
        "finite_normalized_C9_lower_bound_positive": normalized_lower > 0.0,
        "brute_energy_matches_formula": brute_match,
    }
    if not all(checks.values()):
        raise AssertionError(f"certificate check failed: {checks}")

    return {
        "schema_version": 1,
        "status": "COUNTEREXAMPLE_NEW_FLOOR",
        "scope": "LITERAL_QUANTITATIVE_PRIMITIVE_LEAF_INTERFACE_ONLY",
        "proof_status": "PROVED_FAMILY_WITH_REPLAYED_K5_INSTANCE",
        "theorem_attacked": "image-normalized C9 Fourier/Sidon payment",
        "caveat": (
            "This refutes the universal statement under the displayed "
            "quantitative data in def:primitive-leaf. It does not assert that "
            "the example survives the intended informal C1--C8 atlas or "
            "belongs to an intended smooth-domain row sequence."
        ),
        "nonclaims": [
            "not a counterexample to C9 for formal smooth-domain rows",
            "not a counterexample under R asymptotic to N",
            "not a proof that the construction survives exact C1--C8 predicates",
            "not a refutation of the conditional compiler in asymptotic_rs_mca.tex",
        ],
        "source_labels": [
            "experimental/asymptotic_rs_mca.tex:def:primitive-leaf",
            "experimental/asymptotic_rs_mca.tex:def:sidon-paid",
            "experimental/asymptotic_rs_mca.tex:ass:image-normalized-sidon-input",
            "experimental/asymptotic_rs_mca.tex:thm:bsg",
            "experimental/asymptotic_rs_mca.tex:thm:quasicube",
        ],
        "parameters": {"k": k, "N": n, "m": m, "R": r, "Q": qbase},
        "field_model": {
            "integer_total_point_sum": total_point_sum,
            "choose_any_prime_strictly_greater_than": 2 * total_point_sum,
            "reason": (
                "Every subset sum lies in [0,sum(T)], so congruence modulo "
                "such a prime is equivalent to integer equality."
            ),
        },
        "sample_counts": {
            "heavy_fiber_size": heavy_size,
            "singleton_fibers": expected_singletons,
            "image_size_L": image_size,
            "domain_size_M": domain_size,
            "barN_numerator": barn.numerator,
            "barN_denominator": barn.denominator,
        },
        "energy": {
            "heavy_energy": energy_formula,
            "heavy_delta_numerator": delta.numerator,
            "heavy_delta_denominator": delta.denominator,
            "brute_energy_checked": brute,
        },
        "C9_sample": {
            "sigma": sigma,
            "logarithmic_q": qlog,
            "log_C9_lower_bound": log_lower,
            "normalized_log_C9_lower_bound": normalized_lower,
        },
        "asymptotic_family": {
            "heavy_log_rate_per_N": math.log(2.0) / 4.0,
            "filler_log_rate_per_N": math.log(5.0) / 4.0,
            "energy_decay_rate_per_N": math.log(4.0 / 3.0) / 4.0,
            "normalized_log_C9_lower_limit": math.log(2.0) / 4.0,
            "barN_limit": 1.0,
        },
        "checks": checks,
    }


def validate_note() -> list[str]:
    errors: list[str] = []
    text = NOTE.read_text(encoding="utf-8")
    required = [
        "COUNTEREXAMPLE_NEW_FLOOR",
        "literal quantitative interface",
        "SPECIFICATION_BLOCKER",
        "C9}\\iff\\text{primitive Q",
        "**not** refute",
        "zero-error two-list recovery",
        "R/N>=1/2+epsilon",
        "not asserted to be one of the",
    ]
    for needle in required:
        if needle not in text:
            errors.append(f"note missing required scope/proof marker: {needle}")
    forbidden = [
        "This is a counterexample to the intended smooth Reed--Solomon theorem",
        "C9 is false for smooth-domain rows",
        "full asymptotic theorem is disproved",
    ]
    for needle in forbidden:
        if needle in text:
            errors.append(f"note contains forbidden overclaim: {needle}")
    return errors


def compare_artifact(actual: dict[str, object], expected: dict[str, object]) -> list[str]:
    if actual == expected:
        return []
    errors: list[str] = []
    for key in sorted(set(actual) | set(expected)):
        if actual.get(key) != expected.get(key):
            errors.append(f"artifact mismatch at top-level key: {key}")
    return errors


def run_check() -> None:
    expected = build_certificate(5, brute=True)
    actual = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    errors = compare_artifact(actual, expected) + validate_note()
    if errors:
        raise SystemExit("\n".join(f"ERROR: {error}" for error in errors))
    print("C9 literal-interface artifact check passed: 2 files")
    print("STATUS: COUNTEREXAMPLE_NEW_FLOOR (literal interface only)")
    print("RESULT: PASS")


def run_tamper_selftest() -> None:
    expected = build_certificate(5, brute=True)
    mutations = [
        ("status", lambda d: d.__setitem__("status", "PROVED")),
        ("scope", lambda d: d.__setitem__("scope", "ALL_SMOOTH_ROWS")),
        (
            "heavy size",
            lambda d: d["sample_counts"].__setitem__("heavy_fiber_size", 31),
        ),
        (
            "image size",
            lambda d: d["sample_counts"].__setitem__("image_size_L", 120),
        ),
        (
            "energy",
            lambda d: d["energy"].__setitem__("heavy_energy", 7775),
        ),
        (
            "delta",
            lambda d: d["energy"].__setitem__("heavy_delta_numerator", 242),
        ),
        (
            "no-wrap threshold",
            lambda d: d["field_model"].__setitem__(
                "choose_any_prime_strictly_greater_than", 17
            ),
        ),
        (
            "normalized lower bound",
            lambda d: d["C9_sample"].__setitem__(
                "normalized_log_C9_lower_bound", 0.0
            ),
        ),
        (
            "asymptotic limit",
            lambda d: d["asymptotic_family"].__setitem__(
                "normalized_log_C9_lower_limit", 0.0
            ),
        ),
        (
            "scope caveat",
            lambda d: d.__setitem__("nonclaims", []),
        ),
    ]
    for name, mutate in mutations:
        candidate = copy.deepcopy(expected)
        mutate(candidate)
        if not compare_artifact(candidate, expected):
            raise SystemExit(f"tamper was not detected: {name}")
    print(f"tamper self-test passed: {len(mutations)} mutations rejected")
    print("RESULT: PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--k", type=int, default=5, help="positive multiple of 5")
    parser.add_argument("--brute-energy", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    modes = sum((args.check, args.write, args.tamper_selftest))
    if modes > 1:
        raise SystemExit("choose at most one of --check, --write, --tamper-selftest")
    if args.check:
        run_check()
        return
    if args.tamper_selftest:
        run_tamper_selftest()
        return

    if args.write and args.k != 5:
        raise SystemExit("--write is reserved for the canonical k=5 artifact")
    certificate = build_certificate(args.k, args.brute_energy or args.write)
    if args.write:
        ARTIFACT.write_bytes(
            (json.dumps(certificate, indent=2, sort_keys=True) + "\n").encode("utf-8")
        )
        print(f"wrote {ARTIFACT.relative_to(REPO_ROOT)}")
        return
    if args.json:
        print(json.dumps(certificate, indent=2, sort_keys=True))
        return

    counts = certificate["sample_counts"]
    c9 = certificate["C9_sample"]
    asymptotic = certificate["asymptotic_family"]
    print("C9 literal-interface counterexample replay")
    print(f"k={args.k}, N={certificate['parameters']['N']}")
    print(f"heavy_fiber_size={counts['heavy_fiber_size']}")
    print(f"singleton_fibers={counts['singleton_fibers']}")
    print(f"normalized_log_C9_lower_bound={c9['normalized_log_C9_lower_bound']}")
    print(
        "asymptotic_normalized_limit="
        f"{asymptotic['normalized_log_C9_lower_limit']}"
    )
    print("STATUS: COUNTEREXAMPLE_NEW_FLOOR (literal interface only)")
    print("RESULT: PASS")


if __name__ == "__main__":
    main()
