#!/usr/bin/env python3
"""Exact toy sweeps for F1 extension-line MCA bad slopes.

Proof status: EXPERIMENTAL / AUDIT.

This script works in quadratic extensions F = F_p[u]/(u^2 - d), where d is
the least nonsquare modulo p.  Let B = F_p and H <= B^* have size n.  For every
beta in F minus B, it studies the denominator family

    f_beta(x) = 1 / (x - beta),      g(x) = x^k.

For each support S subset H of size k+1, the leading interpolation coefficient
of f_beta + z g on S is L_S(f_beta) + z.  Thus exactly one slope
z = -L_S(f_beta) makes the restriction agree with a degree < k word on S.
The sweep counts the unique such slopes and separates base-field slopes from
genuinely extension-valued slopes.

The output is finite-field evidence about the F1 extension-line MCA mechanism.
It is not a proof of the corrected MCA conjecture and does not assert a
large-support counterexample.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from collections import Counter
from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Tuple

Element = Tuple[int, int]
SupportData = Tuple[Tuple[int, ...], Tuple[int, ...]]

DEFAULT_CASES = ((5, 4, 2), (7, 6, 3), (17, 8, 4))


@dataclass(frozen=True)
class QuadraticField:
    """Arithmetic in F_p[u]/(u^2 - d), with elements encoded as (a, b)."""

    p: int
    d: int

    def element(self, a: int, b: int = 0) -> Element:
        return (a % self.p, b % self.p)

    def zero(self) -> Element:
        return (0, 0)

    def add(self, x: Element, y: Element) -> Element:
        return ((x[0] + y[0]) % self.p, (x[1] + y[1]) % self.p)

    def sub(self, x: Element, y: Element) -> Element:
        return ((x[0] - y[0]) % self.p, (x[1] - y[1]) % self.p)

    def neg(self, x: Element) -> Element:
        return ((-x[0]) % self.p, (-x[1]) % self.p)

    def mul(self, x: Element, y: Element) -> Element:
        a = x[0] * y[0] + self.d * x[1] * y[1]
        b = x[0] * y[1] + x[1] * y[0]
        return (a % self.p, b % self.p)

    def scalar_mul(self, c: int, x: Element) -> Element:
        return ((c * x[0]) % self.p, (c * x[1]) % self.p)

    def inv(self, x: Element) -> Element:
        norm = (x[0] * x[0] - self.d * x[1] * x[1]) % self.p
        if norm == 0:
            raise ZeroDivisionError(f"nonzero element has zero norm: {x}")
        inv_norm = pow(norm, -1, self.p)
        return ((x[0] * inv_norm) % self.p, (-x[1] * inv_norm) % self.p)

    def is_base(self, x: Element) -> bool:
        return x[1] == 0

    def to_json(self, x: Element) -> Dict[str, int]:
        return {"a": x[0], "b": x[1]}

    def format(self, x: Element) -> str:
        a, b = x
        if b == 0:
            return str(a)
        if a == 0:
            return "u" if b == 1 else f"{b}u"
        suffix = "u" if b == 1 else f"{b}u"
        return f"{a}+{suffix}"


def prime_factors(value: int) -> List[int]:
    factors = []
    trial = 2
    remaining = value
    while trial * trial <= remaining:
        if remaining % trial == 0:
            factors.append(trial)
            while remaining % trial == 0:
                remaining //= trial
        trial += 1 if trial == 2 else 2
    if remaining > 1:
        factors.append(remaining)
    return factors


def primitive_root(p: int) -> int:
    factors = prime_factors(p - 1)
    for candidate in range(2, p):
        if all(pow(candidate, (p - 1) // factor, p) != 1 for factor in factors):
            return candidate
    raise ValueError(f"could not find a primitive root modulo {p}")


def least_nonsquare(p: int) -> int:
    for candidate in range(2, p):
        if pow(candidate, (p - 1) // 2, p) == p - 1:
            return candidate
    raise ValueError(f"could not find a nonsquare modulo {p}")


def subgroup_points(p: int, n: int) -> Tuple[int, ...]:
    if (p - 1) % n != 0:
        raise ValueError(f"n={n} must divide p-1={p - 1}")
    generator = primitive_root(p)
    subgroup_generator = pow(generator, (p - 1) // n, p)
    points = tuple(pow(subgroup_generator, i, p) for i in range(n))
    if len(set(points)) != n:
        raise ValueError(f"subgroup generator produced {len(set(points))} points")
    return points


def support_data(points: Sequence[int], p: int, size: int) -> List[SupportData]:
    data = []
    for indices in itertools.combinations(range(len(points)), size):
        weights = []
        for i in indices:
            denominator = 1
            xi = points[i]
            for j in indices:
                if i == j:
                    continue
                denominator = (denominator * (xi - points[j])) % p
            weights.append(pow(denominator, -1, p))
        data.append((indices, tuple(weights)))
    return data


def slope_for_support(
    field: QuadraticField,
    inverse_values: Sequence[Element],
    data: SupportData,
) -> Element:
    indices, weights = data
    leading_coefficient = field.zero()
    for index, weight in zip(indices, weights):
        leading_coefficient = field.add(
            leading_coefficient,
            field.scalar_mul(weight, inverse_values[index]),
        )
    return field.neg(leading_coefficient)


def all_extension_betas(p: int) -> Iterable[Element]:
    for a in range(p):
        for b in range(1, p):
            yield (a, b)


def summarize_records(records: Sequence[Dict[str, object]], key: str) -> Dict[str, float]:
    values = [int(record[key]) for record in records]
    return {
        "min": min(values),
        "max": max(values),
        "mean": sum(values) / len(values),
    }


def histogram(records: Sequence[Dict[str, object]], key: str) -> Dict[str, int]:
    counts = Counter(int(record[key]) for record in records)
    return {str(value): counts[value] for value in sorted(counts)}


def sweep_case(p: int, n: int, k: int, sample_limit: int) -> Dict[str, object]:
    d = least_nonsquare(p)
    field = QuadraticField(p, d)
    points = subgroup_points(p, n)
    supports = support_data(points, p, k + 1)
    beta_records: List[Dict[str, object]] = []

    for beta in all_extension_betas(p):
        inverse_values = [
            field.inv(field.sub(field.element(point), beta)) for point in points
        ]
        slopes = {
            slope_for_support(field, inverse_values, data) for data in supports
        }
        base_slopes = sorted(slope for slope in slopes if field.is_base(slope))
        extension_slopes = sorted(slope for slope in slopes if not field.is_base(slope))
        beta_records.append(
            {
                "beta": beta,
                "unique_slopes": len(slopes),
                "base_slopes": len(base_slopes),
                "extension_slopes": len(extension_slopes),
                "sample_base_slopes": base_slopes[:sample_limit],
                "sample_extension_slopes": extension_slopes[:sample_limit],
            }
        )

    beta_records.sort(
        key=lambda record: (
            -int(record["extension_slopes"]),
            -int(record["unique_slopes"]),
            record["beta"],
        )
    )
    best = beta_records[0]

    return {
        "proof_status": "EXPERIMENTAL / AUDIT",
        "theorem_problem_id": "F1-extension-line-MCA-slope-sweep",
        "determinism": "deterministic exhaustive finite-field sweep; no random seed",
        "object_checked": "f_beta(x)=1/(x-beta), g(x)=x^k, |S|=k+1",
        "field": {
            "base": f"F_{p}",
            "extension": f"F_{p}[u]/(u^2-{d})",
            "p": p,
            "d": d,
        },
        "parameters": {
            "n": n,
            "k": k,
            "support_size": k + 1,
            "subgroup_points": list(points),
            "support_count": math.comb(n, k + 1),
            "beta_count": p * (p - 1),
        },
        "statistics": {
            "unique_slopes": summarize_records(beta_records, "unique_slopes"),
            "base_slopes": summarize_records(beta_records, "base_slopes"),
            "extension_slopes": summarize_records(beta_records, "extension_slopes"),
            "extension_slope_histogram": histogram(beta_records, "extension_slopes"),
            "base_slope_histogram": histogram(beta_records, "base_slopes"),
        },
        "best_extension_beta": {
            "beta": field.to_json(best["beta"]),
            "unique_slopes": best["unique_slopes"],
            "base_slopes": best["base_slopes"],
            "extension_slopes": best["extension_slopes"],
            "sample_base_slopes": [
                field.to_json(slope) for slope in best["sample_base_slopes"]
            ],
            "sample_extension_slopes": [
                field.to_json(slope) for slope in best["sample_extension_slopes"]
            ],
            "display": {
                "beta": field.format(best["beta"]),
                "sample_base_slopes": [
                    field.format(slope) for slope in best["sample_base_slopes"]
                ],
                "sample_extension_slopes": [
                    field.format(slope) for slope in best["sample_extension_slopes"]
                ],
            },
        },
    }


def parse_case(raw: str) -> Tuple[int, int, int]:
    try:
        p_raw, n_raw, k_raw = raw.split(":")
        return (int(p_raw), int(n_raw), int(k_raw))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("cases must have form p:n:k") from exc


def dedupe_cases(cases: Iterable[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
    seen = set()
    result = []
    for case in cases:
        if case in seen:
            continue
        seen.add(case)
        result.append(case)
    return result


def json_ready(result: Dict[str, object]) -> Dict[str, object]:
    """Convert any remaining tuple field elements into JSON lists."""

    return json.loads(json.dumps(result))


def print_text(results: Sequence[Dict[str, object]]) -> None:
    print("F1 extension-line slope sweep")
    print("proof_status: EXPERIMENTAL / AUDIT")
    print("object: f_beta(x)=1/(x-beta), g(x)=x^k, supports |S|=k+1")
    print()

    for result in results:
        field = result["field"]
        parameters = result["parameters"]
        statistics = result["statistics"]
        best = result["best_extension_beta"]
        n = parameters["n"]
        k = parameters["k"]
        p = field["p"]
        d = field["d"]
        print(f"case p={p}, d={d}, n={n}, k={k}")
        print(
            "  supports={support_count}, betas={beta_count}, subgroup={subgroup}".format(
                support_count=parameters["support_count"],
                beta_count=parameters["beta_count"],
                subgroup=parameters["subgroup_points"],
            )
        )
        for key in ("unique_slopes", "base_slopes", "extension_slopes"):
            stats = statistics[key]
            print(
                f"  {key}: min={stats['min']}, max={stats['max']}, "
                f"mean={stats['mean']:.3f}"
            )
        print(
            "  extension_slope_histogram: "
            + ", ".join(
                f"{count}->{freq}"
                for count, freq in statistics["extension_slope_histogram"].items()
            )
        )
        display = best["display"]
        print(
            "  best_beta={beta}: unique={unique}, base={base}, extension={ext}".format(
                beta=display["beta"],
                unique=best["unique_slopes"],
                base=best["base_slopes"],
                ext=best["extension_slopes"],
            )
        )
        print(
            "  sample_extension_slopes: "
            + ", ".join(display["sample_extension_slopes"])
        )
        print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Exhaustively count same-support bad slopes for an F1 quadratic "
            "extension denominator family."
        )
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="output format",
    )
    parser.add_argument(
        "--case",
        action="append",
        default=[],
        type=parse_case,
        metavar="P:N:K",
        help="add an exact sweep case; defaults remain enabled",
    )
    parser.add_argument(
        "--include-n16",
        action="store_true",
        help="also run the slower p=17,n=16,k=8 case",
    )
    parser.add_argument(
        "--sample-limit",
        type=int,
        default=8,
        help="number of slope examples to retain per best beta",
    )
    args = parser.parse_args()

    if args.sample_limit < 0:
        raise SystemExit("--sample-limit must be nonnegative")

    cases = list(DEFAULT_CASES)
    if args.include_n16:
        cases.append((17, 16, 8))
    cases.extend(args.case)
    results = [
        sweep_case(p, n, k, sample_limit=args.sample_limit)
        for p, n, k in dedupe_cases(cases)
    ]

    if args.format == "json":
        print(json.dumps(json_ready({"cases": results}), indent=2, sort_keys=True))
    else:
        print_text(results)


if __name__ == "__main__":
    main()
