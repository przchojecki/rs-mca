#!/usr/bin/env python3
"""Independent checker for the finite mu_2 fold-defect injection census.

Status: AUDIT.  The checker recomputes the fold map, child support, complete
signed defect certificate, and multiplicity histograms from raw set arithmetic.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter, defaultdict
from fractions import Fraction
from math import comb
from pathlib import Path
from typing import Any


STATUS = "AUDIT"
THEOREM_PROBLEM_ID = "thm:fiber-descent; lem:v13-quot-pullback; Route-gamma fold-defect injection"
SCHEMA_VERSION = "gamma-fold-defect-injection-v2"
DEFAULT_CERT = Path(
    "experimental/data/certificates/gamma-fold-defect/gamma_fold_defect_injection.json"
)


def primitive_root(p: int) -> int:
    factors: list[int] = []
    value = p - 1
    d = 2
    while d * d <= value:
        if value % d == 0:
            factors.append(d)
            while value % d == 0:
                value //= d
        d += 1 if d == 2 else 2
    if value > 1:
        factors.append(value)
    for candidate in range(2, p):
        if all(pow(candidate, (p - 1) // factor, p) != 1 for factor in factors):
            return candidate
    raise ValueError(f"no primitive root for F_{p}")


def subgroup(p: int, n: int) -> tuple[int, ...]:
    omega = pow(primitive_root(p), (p - 1) // n, p)
    values = tuple(pow(omega, index, p) for index in range(n))
    assert len(set(values)) == n
    return values


def locator(domain: tuple[int, ...], support: tuple[int, ...], p: int) -> tuple[int, ...]:
    coeffs = [1]
    for index in support:
        root = domain[index]
        nxt = [0] * (len(coeffs) + 1)
        for i, coeff in enumerate(coeffs):
            nxt[i] = (nxt[i] - coeff * root) % p
            nxt[i + 1] = (nxt[i + 1] + coeff) % p
        coeffs = nxt
    return tuple(coeffs)


def stabilizer_size(support: tuple[int, ...], n: int) -> int:
    support_set = set(support)
    return sum(1 for shift in range(n) if {(index + shift) % n for index in support_set} == support_set)


def fold_parts_raw(support: tuple[int, ...], n: int) -> tuple[tuple[int, ...], tuple[tuple[int, int], ...]]:
    support_set = set(support)
    child = []
    signed_singletons = []
    for folded_index in range(n // 2):
        low = folded_index in support_set
        high = (folded_index + n // 2) in support_set
        if low and high:
            child.append(folded_index)
        elif low:
            signed_singletons.append((folded_index, 0))
        elif high:
            signed_singletons.append((folded_index, 1))
    return tuple(child), tuple(signed_singletons)


def folded_counts_raw(support: tuple[int, ...], n: int) -> tuple[int, ...]:
    child, signed_singletons = fold_parts_raw(support, n)
    counts = [0] * (n // 2)
    for index in child:
        counts[index] = 2
    for index, _sign in signed_singletons:
        counts[index] = 1
    return tuple(counts)


def fraction_record(value: Fraction) -> dict[str, int | str]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "text": f"{value.numerator}/{value.denominator}",
    }


def child_record(child: tuple[int, ...], child_domain: tuple[int, ...], p: int) -> dict[str, Any]:
    return {
        "support": list(child),
        "size": len(child),
        "periodicity_scale": stabilizer_size(child, len(child_domain)) if child else 0,
        "locator_coefficients": list(locator(child_domain, child, p)),
        "locator_roots": [child_domain[index] for index in child],
        "wellformed_support": len(set(child)) == len(child)
        and all(0 <= index < len(child_domain) for index in child),
    }


def complete_defect_record(signed_singletons: tuple[tuple[int, int], ...]) -> dict[str, Any]:
    return {
        "singleton_count": len(signed_singletons),
        "signed_singletons": [
            {
                "folded_index": index,
                "sign": sign,
                "parent_index": index if sign == 0 else None,
                "opposite_parent_index_offset": sign,
            }
            for index, sign in signed_singletons
        ],
    }


def parent_record(support: tuple[int, ...], child_domain: tuple[int, ...], p: int, n: int) -> dict[str, Any]:
    child, signed_singletons = fold_parts_raw(support, n)
    return {
        "support": list(support),
        "periodicity_scale": stabilizer_size(support, n),
        "folded_counts": list(folded_counts_raw(support, n)),
        "child": child_record(child, child_domain, p),
        "complete_defect": complete_defect_record(signed_singletons),
        "destroyed": bool(signed_singletons),
    }


def payload_hash(payload: dict[str, Any]) -> str:
    clone = {key: value for key, value in payload.items() if key != "payload_sha256"}
    blob = json.dumps(clone, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def row_replay(row: dict[str, Any]) -> dict[str, Any]:
    p = int(row["p"])
    n = int(row["n"])
    j = int(row["j"])
    domain = subgroup(p, n)
    assert row["domain"] == list(domain)
    child_domain = tuple((value * value) % p for value in domain[: n // 2])
    assert row["folded_domain"] == list(child_domain)
    complete_groups: dict[tuple[tuple[int, ...], tuple[tuple[int, int], ...]], list[tuple[int, ...]]] = defaultdict(list)
    count_only_groups: dict[tuple[int, ...], list[tuple[int, ...]]] = defaultdict(list)
    singleton_histogram: Counter[int] = Counter()
    child_size_histogram: Counter[int] = Counter()
    child_periodicity_histogram: Counter[int] = Counter()
    child_wellformed = 0
    child_malformed = 0
    aperiodic_total = 0
    surviving_aperiodic = 0
    periodic_total = 0
    for support in itertools.combinations(range(n), j):
        if stabilizer_size(support, n) != 1:
            periodic_total += 1
            continue
        aperiodic_total += 1
        child, signed_singletons = fold_parts_raw(support, n)
        if not signed_singletons:
            surviving_aperiodic += 1
            continue
        complete_groups[(child, signed_singletons)].append(support)
        count_only_groups[folded_counts_raw(support, n)].append(support)
        singleton_histogram[len(signed_singletons)] += 1
        child_size_histogram[len(child)] += 1
        child_periodicity_histogram[stabilizer_size(child, n // 2) if child else 0] += 1
        if child_record(child, child_domain, p)["wellformed_support"]:
            child_wellformed += 1
        else:
            child_malformed += 1
    complete_histogram = Counter(len(parents) for parents in complete_groups.values())
    count_only_histogram = Counter(len(parents) for parents in count_only_groups.values())
    max_complete = max(complete_histogram) if complete_histogram else 0
    examples = []
    for key, parents in sorted(
        complete_groups.items(),
        key=lambda item: (-len(item[0][1]), item[0][0], item[0][1]),
    )[:12]:
        child, signed_singletons = key
        examples.append(
            {
                "child": child_record(child, child_domain, p),
                "complete_defect": complete_defect_record(signed_singletons),
                "multiplicity": len(parents),
                "representative_parent": parent_record(parents[0], child_domain, p, n),
            }
        )
    destroyed_count = sum(len(parents) for parents in complete_groups.values())
    return {
        "total_j_subsets": comb(n, j),
        "aperiodic_j_subsets": aperiodic_total,
        "periodic_j_subsets": periodic_total,
        "destroyed_aperiodic_count": destroyed_count,
        "surviving_aperiodic_count": surviving_aperiodic,
        "complete_defect_bucket_count": len(complete_groups),
        "complete_defect_multiplicity_histogram": [
            {"multiplicity": multiplicity, "bucket_count": count}
            for multiplicity, count in sorted(complete_histogram.items())
        ],
        "max_complete_defect_multiplicity": max_complete,
        "defect_complexity_histogram": [
            {"singleton_count": singleton_count, "parent_count": count}
            for singleton_count, count in sorted(singleton_histogram.items())
        ],
        "child_size_histogram": [
            {"child_size": size, "parent_count": count}
            for size, count in sorted(child_size_histogram.items())
        ],
        "child_periodicity_histogram": [
            {"periodicity_scale": scale, "parent_count": count}
            for scale, count in sorted(child_periodicity_histogram.items())
        ],
        "child_wellformedness": {
            "description": (
                "structural sanity check that the doubleton child is a set of "
                "distinct in-range indices; NOT a rung-(n/2) split-witness validity claim"
            ),
            "wellformed_support_count": child_wellformed,
            "malformed_support_count": child_malformed,
            "wellformed_support_fraction": fraction_record(
                Fraction(child_wellformed, destroyed_count) if destroyed_count else Fraction(1, 1)
            ),
        },
        "count_only_key_diagnostic": {
            "description": "folded count vector without singleton signs; records sign-choice degeneracy only",
            "multiplicity_histogram": [
                {"multiplicity": multiplicity, "bucket_count": count}
                for multiplicity, count in sorted(count_only_histogram.items())
            ],
            "max_multiplicity": max(count_only_histogram) if count_only_histogram else 0,
        },
        "examples": examples,
    }


def check_payload(cert: dict[str, Any]) -> None:
    assert cert["schema_version"] == SCHEMA_VERSION
    assert cert["theorem_problem_id"] == THEOREM_PROBLEM_ID
    assert cert["payload_sha256"] == payload_hash(cert)
    max_values = []
    for row in cert["rows"]:
        actual = row_replay(row)
        for key, value in actual.items():
            assert row[key] == value, (row["label"], key)
        assert row["max_complete_defect_multiplicity"] == 1
        assert row["child_wellformedness"]["malformed_support_count"] == 0
        max_values.append(row["max_complete_defect_multiplicity"])
    assert cert["max_complete_defect_multiplicity_sequence"] == max_values
    assert cert["complete_defect_injective_on_recorded_rows"] == all(value == 1 for value in max_values)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path, default=DEFAULT_CERT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    cert = json.loads(args.check.read_text(encoding="utf-8"))
    check_payload(cert)
    result = {
        "status": STATUS,
        "result": "PASS",
        "certificate": args.check.as_posix(),
        "theorem_problem_id": THEOREM_PROBLEM_ID,
        "rows_checked": len(cert["rows"]),
    }
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(
            "gamma_fold_defect_injection_check: "
            f"status={STATUS} result=PASS file={args.check.as_posix()}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
