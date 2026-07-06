#!/usr/bin/env python3
"""Independent checker for the annulus MCA-from-CA finite certificate.

Proof status: AUDIT. This checker replays the certificate with a different
restricted-code predicate from the generator: it interpolates on each support
and verifies the high-support values directly. No GPU, numpy, or floats are
used.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
from typing import Any


STATUS = "AUDIT"
THEOREM_PROBLEM_ID = "Task A.3 annulus MCA-from-CA finite verification"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def inv(value: int, p: int) -> int:
    value %= p
    if value == 0:
        raise ZeroDivisionError("zero has no inverse")
    return pow(value, p - 2, p)


def poly_trim(coeffs: list[int]) -> list[int]:
    out = [value for value in coeffs]
    while out and out[-1] == 0:
        out.pop()
    return out


def poly_add(a: list[int], b: list[int], p: int) -> list[int]:
    out = [0] * max(len(a), len(b))
    for idx in range(len(out)):
        out[idx] = ((a[idx] if idx < len(a) else 0) + (b[idx] if idx < len(b) else 0)) % p
    return poly_trim(out)


def poly_mul(a: list[int], b: list[int], p: int) -> list[int]:
    if not a or not b:
        return []
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] = (out[i + j] + ai * bj) % p
    return poly_trim(out)


def poly_eval(coeffs: tuple[int, ...] | list[int], x: int, p: int) -> int:
    total = 0
    for coeff in reversed(coeffs):
        total = (total * x + coeff) % p
    return total


def coeff_key(coeffs: tuple[int, ...] | list[int], k: int, p: int) -> tuple[int, ...]:
    out = [value % p for value in coeffs[:k]]
    out.extend([0] * (k - len(out)))
    return tuple(out)


def interpolate_coeffs(p: int, xs: tuple[int, ...], ys: tuple[int, ...], k: int) -> tuple[int, ...]:
    require(len(xs) >= k and len(ys) >= k, "need at least k interpolation points")
    result: list[int] = []
    for i in range(k):
        xi = xs[i]
        yi = ys[i]
        basis = [1]
        denominator = 1
        for j in range(k):
            if i == j:
                continue
            xj = xs[j]
            basis = poly_mul(basis, [(-xj) % p, 1], p)
            denominator = (denominator * ((xi - xj) % p)) % p
        scale = yi * inv(denominator, p)
        term = [(scale * coeff) % p for coeff in basis]
        result = poly_add(result, term, p)
    return coeff_key(tuple(result), k, p)


class InterpolationReplay:
    def __init__(self, p: int, n: int, k: int, r: int, domain: tuple[int, ...]):
        self.p = p
        self.n = n
        self.k = k
        self.r = r
        self.a = n - r
        self.domain = domain
        self.supports_ge_a = [
            tuple(support)
            for size in range(self.a, self.n + 1)
            for support in combinations(range(self.n), size)
        ]
        self.supports_eq_a = [
            tuple(support) for support in combinations(range(self.n), self.a)
        ]

    def fits(self, word: tuple[int, ...], support: tuple[int, ...]) -> bool:
        if len(support) <= self.k:
            return True
        xs = tuple(self.domain[index] for index in support)
        ys = tuple(word[index] for index in support)
        coeffs = interpolate_coeffs(self.p, xs, ys, self.k)
        return all(poly_eval(coeffs, x, self.p) == y for x, y in zip(xs, ys))

    def pair_fits(self, f1: tuple[int, ...], f2: tuple[int, ...], support: tuple[int, ...]) -> bool:
        return self.fits(f1, support) and self.fits(f2, support)

    def add_scaled(self, f1: tuple[int, ...], gamma: int, f2: tuple[int, ...]) -> tuple[int, ...]:
        return tuple((x + gamma * y) % self.p for x, y in zip(f1, f2))

    def close_slopes(self, f1: tuple[int, ...], f2: tuple[int, ...]) -> tuple[int, ...]:
        close = []
        for gamma in range(self.p):
            point = self.add_scaled(f1, gamma, f2)
            if any(self.fits(point, support) for support in self.supports_ge_a):
                close.append(gamma)
        return tuple(close)

    def mca_bad_slopes(self, f1: tuple[int, ...], f2: tuple[int, ...]) -> tuple[int, ...]:
        bad = []
        for gamma in range(self.p):
            point = self.add_scaled(f1, gamma, f2)
            for support in self.supports_ge_a:
                if self.fits(point, support) and not self.pair_fits(f1, f2, support):
                    bad.append(gamma)
                    break
        return tuple(bad)

    def cluster(self, f1: tuple[int, ...], f2: tuple[int, ...]) -> list[dict[str, Any]]:
        by_key: dict[tuple[tuple[int, ...], tuple[int, ...]], dict[str, Any]] = {}
        for support in self.supports_eq_a:
            if not self.pair_fits(f1, f2, support):
                continue
            xs = tuple(self.domain[index] for index in support)
            p1 = interpolate_coeffs(
                self.p, xs, tuple(f1[index] for index in support), self.k
            )
            p2 = interpolate_coeffs(
                self.p, xs, tuple(f2[index] for index in support), self.k
            )
            key = (p1, p2)
            if key in by_key:
                by_key[key]["support_count_at_threshold"] += 1
                continue
            full_support = tuple(
                idx
                for idx, (x1, x2) in enumerate(zip(f1, f2))
                if poly_eval(p1, self.domain[idx], self.p) == x1
                and poly_eval(p2, self.domain[idx], self.p) == x2
            )
            by_key[key] = {
                "p1_coefficients": list(p1),
                "p2_coefficients": list(p2),
                "agreement_support": list(full_support),
                "agreement_size": len(full_support),
                "support_count_at_threshold": 1,
            }
        return [by_key[key] for key in sorted(by_key)]

    def ca_bad_slopes(
        self, f1: tuple[int, ...], f2: tuple[int, ...], cluster: list[dict[str, Any]]
    ) -> tuple[int, ...]:
        if cluster:
            return ()
        return self.close_slopes(f1, f2)


def johnson_bound(n: int, k: int, agreement: int) -> Fraction:
    denominator = agreement * agreement - (k - 1) * n
    require(denominator > 0, "Johnson bound denominator is not positive")
    return Fraction(n * (agreement - k + 1), denominator)


def fraction_from_record(record: dict[str, Any]) -> Fraction:
    return Fraction(record["numerator"], record["denominator"])


def check_pair(replay: InterpolationReplay, pair: dict[str, Any]) -> None:
    f1 = tuple(pair["f1"])
    f2 = tuple(pair["f2"])
    cluster = replay.cluster(f1, f2)
    mca = replay.mca_bad_slopes(f1, f2)
    ca = replay.ca_bad_slopes(f1, f2, cluster)
    bound = johnson_bound(replay.n, replay.k, replay.a)
    require(list(mca) == pair["mca_bad_slopes"], f"MCA slopes mismatch for {pair['pair_id']}")
    require(list(ca) == pair["ca_bad_slopes"], f"CA slopes mismatch for {pair['pair_id']}")
    require(len(cluster) == pair["explanation_cluster_size"], f"cluster size mismatch for {pair['pair_id']}")
    require(bound == fraction_from_record(pair["johnson_bound"]), f"Johnson bound mismatch for {pair['pair_id']}")
    require((Fraction(len(cluster), 1) <= bound) == pair["cluster_le_johnson"], f"Johnson boolean mismatch for {pair['pair_id']}")
    require(len(mca) == pair["epsilon_mca_times_q"], f"MCA count mismatch for {pair['pair_id']}")
    require(len(ca) == pair["epsilon_ca_times_q"], f"CA count mismatch for {pair['pair_id']}")
    shape_holds = len(mca) <= len(ca) + len(cluster) * replay.r
    require(shape_holds == pair["shape_holds"], f"shape boolean mismatch for {pair['pair_id']}")


def check_oracle_exhaustive(row: dict[str, Any]) -> None:
    params = row["row"]
    p = params["q"]
    n = params["n"]
    k = params["k"]
    r = params["r"]
    if k == 1:
        check_oracle_exhaustive_constant_row(row)
        return
    replay = InterpolationReplay(p, n, k, r, tuple(row["domain"]))
    max_mca = -1
    max_ca = -1
    for values in product(range(p), repeat=2 * n):
        f1 = tuple(values[:n])
        f2 = tuple(values[n:])
        cluster = replay.cluster(f1, f2)
        max_mca = max(max_mca, len(replay.mca_bad_slopes(f1, f2)))
        max_ca = max(max_ca, len(replay.ca_bad_slopes(f1, f2, cluster)))
    require(max_mca == row["max_mca_bad_slopes"], "exhaustive oracle max MCA mismatch")
    require(max_ca == row["max_ca_bad_slopes"], "exhaustive oracle max CA mismatch")
    require(max_mca <= row["expected_r_plus_1"], "exhaustive MCA exceeds oracle bound")
    require(max_ca <= row["expected_r_plus_1"], "exhaustive CA exceeds oracle bound")


def check_oracle_exhaustive_constant_row(row: dict[str, Any]) -> None:
    params = row["row"]
    p = params["q"]
    n = params["n"]
    r = params["r"]
    agreement = n - r
    supports_ge_a = [
        tuple(support)
        for size in range(agreement, n + 1)
        for support in combinations(range(n), size)
    ]
    supports_eq_a = [tuple(support) for support in combinations(range(n), agreement)]

    def constant_on(word: tuple[int, ...], support: tuple[int, ...]) -> bool:
        first = word[support[0]]
        return all(word[index] == first for index in support)

    def pair_constant_on(
        f1: tuple[int, ...], f2: tuple[int, ...], support: tuple[int, ...]
    ) -> bool:
        return constant_on(f1, support) and constant_on(f2, support)

    def cluster_exists(f1: tuple[int, ...], f2: tuple[int, ...]) -> bool:
        return any(pair_constant_on(f1, f2, support) for support in supports_eq_a)

    def close_slopes(f1: tuple[int, ...], f2: tuple[int, ...]) -> tuple[int, ...]:
        close = []
        for gamma in range(p):
            point = tuple((x + gamma * y) % p for x, y in zip(f1, f2))
            if any(constant_on(point, support) for support in supports_ge_a):
                close.append(gamma)
        return tuple(close)

    def mca_bad_slopes(f1: tuple[int, ...], f2: tuple[int, ...]) -> tuple[int, ...]:
        bad = []
        for gamma in range(p):
            point = tuple((x + gamma * y) % p for x, y in zip(f1, f2))
            for support in supports_ge_a:
                if constant_on(point, support) and not pair_constant_on(f1, f2, support):
                    bad.append(gamma)
                    break
        return tuple(bad)

    max_mca = -1
    max_ca = -1
    words = list(product(range(p), repeat=n))
    for f1 in words:
        for f2 in words:
            cluster = cluster_exists(f1, f2)
            max_mca = max(max_mca, len(mca_bad_slopes(f1, f2)))
            max_ca = max(max_ca, 0 if cluster else len(close_slopes(f1, f2)))
    require(max_mca == row["max_mca_bad_slopes"], "exhaustive oracle max MCA mismatch")
    require(max_ca == row["max_ca_bad_slopes"], "exhaustive oracle max CA mismatch")
    require(max_mca <= row["expected_r_plus_1"], "exhaustive MCA exceeds oracle bound")
    require(max_ca <= row["expected_r_plus_1"], "exhaustive CA exceeds oracle bound")


def check_certificate(cert: dict[str, Any]) -> None:
    require(cert["theorem_problem_id"] == THEOREM_PROBLEM_ID, "theorem/problem id mismatch")
    check_oracle_exhaustive(cert["oracle_gate"]["exhaustive_deep_row"])
    tangent = cert["oracle_gate"]["f13_tangent_cell"]
    row = tangent["row"]
    replay = InterpolationReplay(row["q"], row["n"], row["k"], row["r"], tuple(tangent["domain"]))
    check_pair(replay, tangent["pair"])
    require(tangent["mca_attains_r_plus_1"], "tangent MCA oracle did not attain r+1")
    require(tangent["ca_attains_r_plus_1"], "tangent CA oracle did not attain r+1")

    violations = []
    for annulus in cert["annulus_rows"]:
        row = annulus["row"]
        replay = InterpolationReplay(row["q"], row["n"], row["k"], row["r"], tuple(annulus["domain"]))
        for pair in annulus["pairs"]:
            check_pair(replay, pair)
            if not pair["shape_holds"] or not pair["cluster_le_johnson"]:
                violations.append((row["q"], row["n"], row["k"], row["r"], pair["pair_id"]))
        require(
            annulus["all_cluster_johnson_checks_hold"]
            == all(pair["cluster_le_johnson"] for pair in annulus["pairs"]),
            "row Johnson summary mismatch",
        )
        require(
            annulus["all_shape_checks_hold"]
            == all(pair["shape_holds"] for pair in annulus["pairs"]),
            "row shape summary mismatch",
        )

    require(
        cert["overall"]["all_annulus_shape_checks_hold"]
        == all(row["all_shape_checks_hold"] for row in cert["annulus_rows"]),
        "overall shape summary mismatch",
    )
    require(
        cert["overall"]["all_annulus_cluster_johnson_checks_hold"]
        == all(row["all_cluster_johnson_checks_hold"] for row in cert["annulus_rows"]),
        "overall Johnson summary mismatch",
    )
    require(len(violations) == len(cert["overall"]["violations"]), "violation count mismatch")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path, required=True, help="certificate JSON to replay")
    args = parser.parse_args()
    cert = json.loads(args.check.read_text(encoding="utf-8"))
    check_certificate(cert)
    print(f"annulus_mca_from_ca_check: status={STATUS} result=PASS file={args.check.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
