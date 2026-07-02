#!/usr/bin/env python3
"""Verify the arithmetic lemmas in adjacency_staircase_localization.md.

The checks are exact and deliberately small.  They exercise the generic
nonincreasing staircase classification, the lower/upper corridor lemma, the
list-radius analogue, and the relative-envelope steepness compiler.  They also
replay the known F_17^32 high-agreement tangent crossing as an anchor example;
that replay is not a new row theorem.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from fractions import Fraction
from itertools import product
from pathlib import Path


@dataclass(frozen=True)
class CheckResult:
    name: str
    status: str
    details: list[str]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def is_nonincreasing(values: list[int]) -> bool:
    return all(values[i] >= values[i + 1] for i in range(len(values) - 1))


def is_nondecreasing(values: list[int]) -> bool:
    return all(values[i] <= values[i + 1] for i in range(len(values) - 1))


def classify_nonincreasing(
    agreements: list[int], values: list[int], budget: int
) -> dict[str, int | str]:
    require(len(agreements) == len(values), "agreement/value length mismatch")
    require(is_nonincreasing(values), "values are not nonincreasing")
    safe = [i for i, value in enumerate(values) if value <= budget]
    if not safe:
        return {"case": "ALL_UNSAFE"}
    if safe[0] == 0:
        return {"case": "ALL_SAFE"}
    first = safe[0]
    require(values[first - 1] > budget >= values[first], "bad adjacent crossing")
    require(all(values[i] > budget for i in range(first)), "unsafe prefix failed")
    require(all(values[i] <= budget for i in range(first, len(values))), "safe suffix failed")
    return {
        "case": "INTERIOR",
        "first_safe_agreement": agreements[first],
        "last_unsafe_agreement": agreements[first - 1],
    }


def classify_nondecreasing_radius(
    radii: list[int], values: list[int], budget: int
) -> dict[str, int | str]:
    require(len(radii) == len(values), "radius/value length mismatch")
    require(is_nondecreasing(values), "values are not nondecreasing")
    safe = [i for i, value in enumerate(values) if value <= budget]
    if not safe:
        return {"case": "ALL_UNSAFE"}
    if safe[-1] == len(values) - 1:
        return {"case": "ALL_SAFE"}
    last = safe[-1]
    require(values[last] <= budget < values[last + 1], "bad radius crossing")
    require(all(values[i] <= budget for i in range(last + 1)), "safe radius prefix failed")
    require(all(values[i] > budget for i in range(last + 1, len(values))), "unsafe radius suffix failed")
    return {
        "case": "INTERIOR",
        "largest_safe_radius": radii[last],
        "first_unsafe_radius": radii[last + 1],
    }


def corridor(
    agreements: list[int], lower: list[int], upper: list[int], budget: int
) -> tuple[int, int]:
    require(len(agreements) == len(lower) == len(upper), "corridor length mismatch")
    require(all(lo <= hi for lo, hi in zip(lower, upper)), "lower exceeds upper")
    certified_unsafe = [a for a, lo in zip(agreements, lower) if lo > budget]
    certified_safe = [a for a, hi in zip(agreements, upper) if hi <= budget]
    lo = max(certified_unsafe) + 1 if certified_unsafe else agreements[0]
    hi = min(certified_safe) if certified_safe else agreements[-1]
    return lo, hi


def integer_sequences_between(
    lower: list[int], upper: list[int], *, cap: int
) -> list[list[int]]:
    out: list[list[int]] = []
    ranges = [range(lo, hi + 1) for lo, hi in zip(lower, upper)]
    for values in product(*ranges):
        seq = list(values)
        if max(seq, default=0) <= cap and is_nonincreasing(seq):
            out.append(seq)
    return out


def check_generic_staircase() -> CheckResult:
    cases = [
        ("all safe", [4, 3, 2, 1], 4, "ALL_SAFE"),
        ("all unsafe", [9, 8, 7, 7], 6, "ALL_UNSAFE"),
        ("interior with plateau", [12, 9, 9, 6, 4, 4, 1], 5, "INTERIOR"),
        ("interior at last point", [10, 8, 6, 5], 5, "INTERIOR"),
    ]
    agreements = list(range(20, 27))
    details = []
    for label, values, budget, expected in cases:
        aa = agreements[: len(values)]
        result = classify_nonincreasing(aa, values, budget)
        require(result["case"] == expected, f"{label}: expected {expected}, got {result}")
        details.append(f"{label}: {result}")
    return CheckResult(
        "generic nonincreasing numerator staircase",
        "PASS",
        details,
    )


def check_f17_high_agreement_anchor() -> CheckResult:
    n, k = 512, 256
    q = 17**32
    budget = q // 2**128
    agreements = list(range(427, 513))
    values = [n - a + 1 for a in agreements]
    result = classify_nonincreasing(agreements, values, budget)
    require(budget == 6, "unexpected F_17^32 budget")
    require(result["case"] == "INTERIOR", "high-agreement anchor not interior")
    require(result["first_safe_agreement"] == 507, "wrong first safe agreement")
    require(result["last_unsafe_agreement"] == 506, "wrong last unsafe agreement")
    require((n - result["first_safe_agreement"], n - result["last_unsafe_agreement"]) == (5, 6), "wrong radii")
    return CheckResult(
        "F_17^32 high-agreement tangent anchor",
        "PASS",
        [
            f"floor(17^32/2^128) = {budget}",
            "LD_sw(C,a)=512-a+1 on a in [427,512]",
            f"classification: {result}",
            "largest safe radius = 5, first unsafe radius = 6",
            f"tangent exactness gate floor((n-k)/3) = {(n-k)//3}",
        ],
    )


def check_corridor_bruteforce() -> CheckResult:
    agreements = [10, 11, 12, 13, 14]
    lower = [8, 6, 3, 0, 0]
    upper = [10, 8, 5, 2, 1]
    budget = 4
    lo, hi = corridor(agreements, lower, upper, budget)
    require((lo, hi) == (12, 13), f"unexpected corridor {(lo, hi)}")

    sequences = integer_sequences_between(lower, upper, cap=12)
    interior = 0
    for seq in sequences:
        result = classify_nonincreasing(agreements, seq, budget)
        if result["case"] == "INTERIOR":
            interior += 1
            first = int(result["first_safe_agreement"])
            require(lo <= first <= hi, f"first safe {first} outside corridor {(lo, hi)} for {seq}")
    require(interior > 0, "corridor example has no interior sequence")
    return CheckResult(
        "lower/upper certificate corridor",
        "PASS",
        [
            f"bounds lower={lower}, upper={upper}, budget={budget}",
            f"corridor for first safe agreement: [{lo},{hi}]",
            f"brute-forced {len(sequences)} nonincreasing numerator staircases inside bounds",
            f"interior cases checked: {interior}",
        ],
    )


def check_list_radius_staircase() -> CheckResult:
    radii = list(range(7))
    values = [1, 1, 2, 3, 5, 9, 13]
    budget = 5
    result = classify_nondecreasing_radius(radii, values, budget)
    require(result["case"] == "INTERIOR", "list staircase should have an interior crossing")
    require(result["largest_safe_radius"] == 4, "wrong largest safe radius")
    require(result["first_unsafe_radius"] == 5, "wrong first unsafe radius")

    n = 12
    agreements = [n - r for r in radii]
    agreement_values = list(reversed(values))
    agreement_grid = list(reversed(agreements))
    agreement_result = classify_nonincreasing(agreement_grid, agreement_values, budget)
    require(agreement_result["case"] == "INTERIOR", "agreement transform failed")
    return CheckResult(
        "list-radius monotone staircase",
        "PASS",
        [
            f"radius values: {list(zip(radii, values))}",
            f"radius classification: {result}",
            f"agreement-coordinate classification: {agreement_result}",
        ],
    )


def ambiguity_interval(model_value: int, envelope: int) -> tuple[Fraction, Fraction]:
    return Fraction(model_value, envelope), Fraction(envelope * model_value, 1)


def envelope_decision(model_value: int, envelope: int, budget: Fraction) -> str:
    low, high = ambiguity_interval(model_value, envelope)
    if low > budget:
        return "UNSAFE"
    if high <= budget:
        return "SAFE"
    return "AMBIGUOUS"


def check_steepness_envelope() -> CheckResult:
    q = 17
    envelope = 4
    require(envelope * envelope < q, "chosen envelope is not below sqrt(step)")
    models = [q ** e for e in range(5, -1, -1)]
    intervals = [ambiguity_interval(m, envelope) for m in models]
    for i in range(len(intervals) - 1):
        require(intervals[i][0] > intervals[i + 1][1], "adjacent ambiguity intervals overlap")

    budgets = [Fraction(1), Fraction(20), Fraction(300), Fraction(5000), Fraction(80000)]
    max_ambiguous = 0
    rows = []
    for budget in budgets:
        decisions = [envelope_decision(m, envelope, budget) for m in models]
        ambiguous = decisions.count("AMBIGUOUS")
        max_ambiguous = max(max_ambiguous, ambiguous)
        require(ambiguous <= 1, f"budget {budget} has multiple ambiguous agreements")
        rows.append(f"B={budget}: {decisions}")
    return CheckResult(
        "relative-envelope steepness compiler",
        "PASS",
        [
            f"model ratios are exactly q={q}; envelope E={envelope}; E^2={envelope*envelope}<q",
            "adjacent ambiguity intervals are disjoint",
            f"maximum ambiguous agreements over tested budgets: {max_ambiguous}",
            *rows,
        ],
    )


CHECKS = [
    check_generic_staircase,
    check_f17_high_agreement_anchor,
    check_corridor_bruteforce,
    check_list_radius_staircase,
    check_steepness_envelope,
]


def run_checks() -> list[CheckResult]:
    results = []
    for fn in CHECKS:
        results.append(fn())
    return results


def emit_certificate(results: list[CheckResult]) -> Path:
    repo = Path(__file__).resolve().parents[2]
    out_dir = repo / "experimental" / "data" / "certificates" / "adjacency-staircase-localization"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "adjacency_staircase_localization.json"
    payload = {
        "status": "PROVED-COMPILER-ARITHMETIC",
        "note": "experimental/notes/thresholds/adjacency_staircase_localization.md",
        "script": "experimental/scripts/verify_adjacency_staircase_localization.py",
        "dag_nodes": [
            "crossing_localization",
            "staircase_steepness",
            "list_crossing_localization",
        ],
        "edge_case_correction": (
            "An interior adjacent crossing exists exactly when the tested grid "
            "contains at least one safe and one unsafe agreement; otherwise "
            "the theorem returns ALL_SAFE or ALL_UNSAFE."
        ),
        "checks": [asdict(result) for result in results],
    }
    out_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true", help="write the JSON certificate")
    args = parser.parse_args()

    print("=" * 74)
    print("VERIFY: adjacency staircase localization")
    print("=" * 74)
    failed = 0
    results: list[CheckResult] = []
    for fn in CHECKS:
        try:
            result = fn()
        except AssertionError as exc:
            failed += 1
            print(f"\n[FAIL] {fn.__name__}")
            print(f"       {exc}")
            continue
        results.append(result)
        print(f"\n[{result.status}] {result.name}")
        for line in result.details:
            print(f"       {line}")
    print("\n" + "-" * 74)
    print(f"implemented PASS: {len(results)}   FAIL: {failed}")
    if failed:
        raise SystemExit(1)
    if args.emit:
        out_path = emit_certificate(results)
        print(f"emitted: {out_path.relative_to(Path(__file__).resolve().parents[2])}")


if __name__ == "__main__":
    main()
