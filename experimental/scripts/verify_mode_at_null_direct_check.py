#!/usr/bin/env python3
"""Independent checker for direct mode-at-null finite certificates.

Status: AUDIT.  The checker rebuilds Phi_w fibers from raw power sums using
Newton identities, not the elementary-symmetric recurrence used by the
enumerator.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from fractions import Fraction
from math import comb
from pathlib import Path
from typing import Any


STATUS = "AUDIT"
THEOREM_PROBLEM_ID = "prob:band; Q3 mode-at-null; Phi_w prefix fibers"
SCHEMA_VERSION = "mode-at-null-direct-v2"
DEFAULT_CERT = Path(
    "experimental/data/certificates/mode-at-null-direct/mode_at_null_direct.json"
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


def signed_prefix_from_power_sums(values: tuple[int, ...], w: int, p: int) -> tuple[int, ...]:
    power_sums = [0] + [
        sum(pow(value, degree, p) for value in values) % p
        for degree in range(1, w + 1)
    ]
    elementary = [0] * (w + 1)
    elementary[0] = 1
    for degree in range(1, w + 1):
        total = 0
        for index in range(1, degree + 1):
            sign = 1 if index % 2 else -1
            total += sign * elementary[degree - index] * power_sums[index]
        elementary[degree] = (total * pow(degree, -1, p)) % p
    return tuple(((-1 if degree % 2 else 1) * elementary[degree]) % p for degree in range(1, w + 1))


def fraction_from_record(record: dict[str, Any]) -> Fraction:
    return Fraction(int(record["numerator"]), int(record["denominator"]))


def fraction_record(value: Fraction) -> dict[str, Any]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "text": f"{value.numerator}/{value.denominator}",
    }


def payload_hash(payload: dict[str, Any]) -> str:
    clone = {key: value for key, value in payload.items() if key != "payload_sha256"}
    blob = json.dumps(clone, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def check_row(row: dict[str, Any]) -> None:
    p = int(row["p"])
    n = int(row["n"])
    m = int(row["m"])
    w = int(row["w"])
    domain = subgroup(p, n)
    assert row["domain"] == list(domain)
    histogram: Counter[tuple[int, ...]] = Counter()
    for support in itertools.combinations(range(n), m):
        values = tuple(domain[index] for index in support)
        histogram[signed_prefix_from_power_sums(values, w, p)] += 1
    total = comb(n, m)
    zero = (0,) * w
    null_count = histogram.get(zero, 0)
    max_count = max(histogram.values())
    strict_margin = max_count - null_count
    argmax = sorted(prefix for prefix, count in histogram.items() if count == max_count)
    avg = Fraction(total, p**w)
    kappa_null = Fraction(null_count * p**w, total)
    kappa_max = Fraction(max_count * p**w, total)
    assert row["subsets_total"] == total
    assert row["realized_fibers"] == len(histogram)
    assert fraction_from_record(row["average_fiber_size"]) == avg
    assert row["zero_prefix"] == list(zero)
    assert row["N_w_zero"] == null_count
    assert row["z_zero_realized"] == (null_count > 0)
    assert row["argmax_count"] == max_count
    assert row["strict_margin"] == strict_margin
    assert row["argmax_prefixes"] == [list(prefix) for prefix in argmax[:12]]
    assert row["mode_at_null_holds"] == (max_count <= null_count)
    assert fraction_from_record(row["kappa_null"]) == kappa_null
    assert fraction_from_record(row["kappa_max"]) == kappa_max
    assert row["fiber_histogram"] == [
        {"z": list(prefix), "count": count}
        for prefix, count in sorted(histogram.items())
    ]
    assert row["top_fibers"] == [
        {"z": list(prefix), "count": count}
        for prefix, count in sorted(histogram.items(), key=lambda item: (-item[1], item[0]))[:12]
    ]
    if max_count > null_count and null_count > 0:
        assert row["failure_witnesses"]
        for witness in row["failure_witnesses"]:
            z = tuple(witness["z"])
            assert histogram[z] == max_count
            assert witness["N_w_z"] == max_count
            assert witness["N_w_zero"] == null_count
            assert witness["excess"] == max_count - null_count
    else:
        assert row["failure_witnesses"] == []


def check_payload(cert: dict[str, Any]) -> None:
    assert cert["schema_version"] == SCHEMA_VERSION
    assert cert["theorem_problem_id"] == THEOREM_PROBLEM_ID
    assert cert["payload_sha256"] == payload_hash(cert)
    vacuous = []
    genuine = []
    for row in cert["rows"]:
        check_row(row)
        if not row["z_zero_realized"]:
            vacuous.append(
                {
                    "row": row["label"],
                    "reason": "zero prefix is not realized",
                    "N_w_zero": row["N_w_zero"],
                    "argmax_count": row["argmax_count"],
                    "strict_margin": row["strict_margin"],
                }
            )
        elif not row["mode_at_null_holds"]:
            genuine.append(
                {
                    "row": row["label"],
                    "N_w_zero": row["N_w_zero"],
                    "argmax_count": row["argmax_count"],
                    "strict_margin": row["strict_margin"],
                    "witnesses": row["failure_witnesses"],
                }
            )
    realized = [row for row in cert["rows"] if row["z_zero_realized"]]
    assert cert["realized_null_summary"] == {
        "realized_rows": len(realized),
        "exact_mode_rows": sum(1 for row in realized if row["strict_margin"] == 0),
        "one_below_mode_rows": sum(1 for row in realized if row["strict_margin"] == 1),
        "max_strict_margin_on_realized_rows": max((row["strict_margin"] for row in realized), default=0),
    }
    assert cert["vacuous_null_rows"] == vacuous
    assert cert["genuine_strict_failures"] == genuine


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
        "vacuous_rows_checked": len(cert["vacuous_null_rows"]),
        "strict_failures_checked": len(cert["genuine_strict_failures"]),
    }
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(
            "mode_at_null_direct_check: "
            f"status={STATUS} result=PASS file={args.check.as_posix()}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
