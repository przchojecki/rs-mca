#!/usr/bin/env python3
"""Independent checker for the annulus bounded-cluster finite certificate.

Proof status: AUDIT. This checker replays the certificate with a different
restricted-code predicate from the generator: it interpolates on each support
and verifies the high-support values directly. No GPU, numpy, or floats are
used.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
from typing import Any


STATUS = "AUDIT"
THEOREM_PROBLEM_ID = "Task A.3 annulus bounded-cluster finite insufficiency search"
SCHEMA_VERSION = "annulus-corrected-cluster-v2"
CANDIDATE_ORDER = ("C0", "C1", "C2", "C3")
EXAMPLE_LIMIT = 2
REGENERATION_COMMAND = (
    "py -3.13 experimental/scripts/verify_annulus_corrected_cluster.py --emit-defaults"
)
PARENT_C0_BASELINE = {
    (11, 10, 3, 4, "cluster_two_explanations"): 2,
    (11, 10, 3, 4, "annulus_tangent_like"): 0,
    (11, 10, 3, 4, "seeded_close_sample"): 1,
    (13, 12, 5, 4, "cluster_two_explanations"): 2,
    (13, 12, 5, 4, "annulus_tangent_like"): 0,
    (13, 12, 5, 4, "seeded_close_sample"): 1,
    (17, 16, 7, 5, "cluster_two_explanations"): 2,
    (17, 16, 7, 5, "annulus_tangent_like"): 0,
    (17, 16, 7, 5, "seeded_close_sample"): 1,
    (31, 10, 3, 4, "cluster_two_explanations"): 2,
    (31, 10, 3, 4, "annulus_tangent_like"): 0,
    (31, 10, 3, 4, "seeded_close_sample"): 1,
}


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


def word_from_coeffs(coeffs: tuple[int, ...], domain: tuple[int, ...], p: int) -> tuple[int, ...]:
    return tuple(poly_eval(coeffs, x, p) for x in domain)


def first_or_empty(values: list[Any]) -> Any:
    return values[0] if values else []


def slim_record(candidate: str, record: dict[str, Any]) -> dict[str, Any]:
    if candidate == "C1":
        return {
            "codeword_coefficients": record["codeword_coefficients"],
            "slopes": record["slopes"],
            "example_full_agreement_support": first_or_empty(record["full_agreement_supports"]),
            "threshold_support_count": record["threshold_support_count"],
        }
    if candidate == "C2":
        return {
            "threshold_support": record["threshold_support"],
            "support_size": record["support_size"],
            "slopes": record["slopes"],
            "example_codeword_coefficients": first_or_empty(record["codeword_coefficients"]),
            "example_full_agreement_support": first_or_empty(record["full_agreement_supports"]),
        }
    if candidate == "C3":
        return {
            "codeword_coefficients": record["codeword_coefficients"],
            "sides": record["sides"],
            "example_full_agreement_supports_by_side": {
                side: first_or_empty(supports)
                for side, supports in record["full_agreement_supports_by_side"].items()
            },
            "threshold_support_count_by_side": record["threshold_support_count_by_side"],
        }
    raise ValueError(f"unsupported slim candidate {candidate}")


def slim_candidate_payload(
    candidate: str, records: list[dict[str, Any]], descriptions: dict[str, str]
) -> dict[str, Any]:
    return {
        "description": descriptions[candidate],
        "count": len(records),
        "records_truncated": len(records) > EXAMPLE_LIMIT,
        "example_limit": EXAMPLE_LIMIT,
        "example_records": [slim_record(candidate, record) for record in records[:EXAMPLE_LIMIT]],
        "regeneration_command": REGENERATION_COMMAND,
    }


def slim_witness_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "count": len(records),
        "records_truncated": len(records) > EXAMPLE_LIMIT,
        "example_limit": EXAMPLE_LIMIT,
        "example_records": records[:EXAMPLE_LIMIT],
        "regeneration_command": REGENERATION_COMMAND,
    }


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

    def interpolation_on_support(
        self, word: tuple[int, ...], support: tuple[int, ...]
    ) -> tuple[int, ...]:
        xs = tuple(self.domain[index] for index in support)
        ys = tuple(word[index] for index in support)
        return interpolate_coeffs(self.p, xs, ys, self.k)

    def full_agreement_support(
        self, word: tuple[int, ...], coeffs: tuple[int, ...]
    ) -> tuple[int, ...]:
        codeword = word_from_coeffs(coeffs, self.domain, self.p)
        return tuple(index for index, (x, y) in enumerate(zip(word, codeword)) if x == y)

    def mca_witness_provenance(
        self, f1: tuple[int, ...], f2: tuple[int, ...]
    ) -> dict[str, Any]:
        codewords: dict[tuple[int, ...], dict[str, Any]] = {}
        supports: dict[tuple[int, ...], dict[str, Any]] = {}
        witness_records: list[dict[str, Any]] = []
        for gamma in range(self.p):
            point = self.add_scaled(f1, gamma, f2)
            for support in self.supports_ge_a:
                if not self.fits(point, support) or self.pair_fits(f1, f2, support):
                    continue
                coeffs = self.interpolation_on_support(point, support)
                full_support = self.full_agreement_support(point, coeffs)
                code_record = codewords.setdefault(
                    coeffs,
                    {
                        "codeword_coefficients": list(coeffs),
                        "slopes": set(),
                        "full_agreement_supports": set(),
                        "threshold_support_count": 0,
                    },
                )
                code_record["slopes"].add(gamma)
                code_record["full_agreement_supports"].add(full_support)
                code_record["threshold_support_count"] += 1
                support_record = supports.setdefault(
                    support,
                    {
                        "threshold_support": list(support),
                        "support_size": len(support),
                        "slopes": set(),
                        "codeword_coefficients": set(),
                        "full_agreement_supports": set(),
                    },
                )
                support_record["slopes"].add(gamma)
                support_record["codeword_coefficients"].add(coeffs)
                support_record["full_agreement_supports"].add(full_support)
                witness_records.append(
                    {
                        "slope": gamma,
                        "threshold_support": list(support),
                        "codeword_coefficients": list(coeffs),
                        "full_agreement_support": list(full_support),
                    }
                )
        return {
            "witness_records": witness_records,
            "witness_codewords": [
                {
                    "codeword_coefficients": record["codeword_coefficients"],
                    "slopes": sorted(record["slopes"]),
                    "full_agreement_supports": [
                        list(support) for support in sorted(record["full_agreement_supports"])
                    ],
                    "threshold_support_count": record["threshold_support_count"],
                }
                for _coeffs, record in sorted(codewords.items())
            ],
            "witness_supports": [
                {
                    "threshold_support": record["threshold_support"],
                    "support_size": record["support_size"],
                    "slopes": sorted(record["slopes"]),
                    "codeword_coefficients": [
                        list(coeffs) for coeffs in sorted(record["codeword_coefficients"])
                    ],
                    "full_agreement_supports": [
                        list(support) for support in sorted(record["full_agreement_supports"])
                    ],
                }
                for _support, record in sorted(supports.items())
            ],
        }

    def half_explanation_provenance(
        self, f1: tuple[int, ...], f2: tuple[int, ...]
    ) -> list[dict[str, Any]]:
        records: dict[tuple[int, ...], dict[str, Any]] = {}
        for side, word in (("f1", f1), ("f2", f2)):
            for support in self.supports_ge_a:
                if not self.fits(word, support):
                    continue
                coeffs = self.interpolation_on_support(word, support)
                full_support = self.full_agreement_support(word, coeffs)
                record = records.setdefault(
                    coeffs,
                    {
                        "codeword_coefficients": list(coeffs),
                        "sides": set(),
                        "full_agreement_supports_by_side": {},
                        "threshold_support_count_by_side": {},
                    },
                )
                record["sides"].add(side)
                record["full_agreement_supports_by_side"].setdefault(side, set()).add(full_support)
                record["threshold_support_count_by_side"][side] = (
                    record["threshold_support_count_by_side"].get(side, 0) + 1
                )
        return [
            {
                "codeword_coefficients": record["codeword_coefficients"],
                "sides": sorted(record["sides"]),
                "full_agreement_supports_by_side": {
                    side: [list(support) for support in sorted(supports)]
                    for side, supports in sorted(record["full_agreement_supports_by_side"].items())
                },
                "threshold_support_count_by_side": dict(
                    sorted(record["threshold_support_count_by_side"].items())
                ),
            }
            for _coeffs, record in sorted(records.items())
        ]

    def candidate_clusters(
        self, f1: tuple[int, ...], f2: tuple[int, ...], cluster: list[dict[str, Any]]
    ) -> dict[str, Any]:
        mca_provenance = self.mca_witness_provenance(f1, f2)
        half_records = self.half_explanation_provenance(f1, f2)
        return {
            "C0": {"count": len(cluster), "records": cluster},
            "C1": {"count": len(mca_provenance["witness_codewords"]), "records": mca_provenance["witness_codewords"]},
            "C2": {"count": len(mca_provenance["witness_supports"]), "records": mca_provenance["witness_supports"]},
            "C3": {"count": len(half_records), "records": half_records},
            "mca_witness_records": mca_provenance["witness_records"],
        }

    def shape_tests(
        self, mca_count: int, ca_count: int, candidate_clusters: dict[str, Any]
    ) -> dict[str, Any]:
        bound = johnson_bound(self.n, self.k, self.a)
        tests = {}
        for candidate in CANDIDATE_ORDER:
            count = candidate_clusters[candidate]["count"]
            rhs = ca_count + count * self.r
            tests[candidate] = {
                "candidate_count": count,
                "lhs_mca_count": mca_count,
                "rhs_count": rhs,
                "shape_holds": mca_count <= rhs,
                "johnson_bound": {
                    "numerator": bound.numerator,
                    "denominator": bound.denominator,
                    "text": f"{bound.numerator}/{bound.denominator}",
                },
                "candidate_le_johnson": Fraction(count, 1) <= bound,
            }
        return tests


def johnson_bound(n: int, k: int, agreement: int) -> Fraction:
    denominator = agreement * agreement - (k - 1) * n
    require(denominator > 0, "Johnson bound denominator is not positive")
    return Fraction(n * (agreement - k + 1), denominator)


def fraction_from_record(record: dict[str, Any]) -> Fraction:
    return Fraction(record["numerator"], record["denominator"])


def row_conditions(p: int, n: int, k: int, r: int) -> dict[str, Any]:
    agreement = n - r
    difference_agreement = n - 2 * r
    return {
        "q": p,
        "n": n,
        "k": k,
        "r": r,
        "agreement_a": agreement,
        "rs_minimum_weight": n - k + 1,
        "annulus_below_half_distance": 2 * r > n - k,
        "half_distance_condition": 2 * r <= n - k,
        "agreement_above_sqrt_kn": agreement * agreement > k * n,
        "agreement_below_half_distance_boundary": 2 * agreement < n + k,
        "johnson_for_explanation_agreement": agreement * agreement > (k - 1) * n,
        "difference_agreement_n_minus_2r": difference_agreement,
        "strategy_difference_johnson_condition": difference_agreement * difference_agreement
        > (k - 1) * n,
        "strategy_difference_condition_impossible_in_strict_annulus": True,
        "strategy_difference_impossibility_reason": (
            "If 2r > n-k, then n-2r <= k-1, while sqrt((k-1)n) > k-1 "
            "for every k<n. Thus n-2r > sqrt((k-1)n) cannot hold in the strict annulus."
        ),
    }


def payload_hash(cert: dict[str, Any]) -> str:
    clone = json.loads(json.dumps(cert, sort_keys=True))
    recorded = clone.pop("payload_sha256", None)
    require(recorded is not None, "missing payload hash")
    rendered = json.dumps(clone, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(rendered.encode("utf-8")).hexdigest()


def check_pair(
    replay: InterpolationReplay, pair: dict[str, Any], descriptions: dict[str, str]
) -> None:
    f1 = tuple(pair["f1"])
    f2 = tuple(pair["f2"])
    cluster = replay.cluster(f1, f2)
    close = replay.close_slopes(f1, f2)
    mca = replay.mca_bad_slopes(f1, f2)
    ca = replay.ca_bad_slopes(f1, f2, cluster)
    bound = johnson_bound(replay.n, replay.k, replay.a)
    require(list(close) == pair["close_slopes"], f"close slopes mismatch for {pair['pair_id']}")
    require(list(mca) == pair["mca_bad_slopes"], f"MCA slopes mismatch for {pair['pair_id']}")
    require(list(ca) == pair["ca_bad_slopes"], f"CA slopes mismatch for {pair['pair_id']}")
    require(len(cluster) == pair["explanation_cluster_size"], f"cluster size mismatch for {pair['pair_id']}")
    require(
        cluster[:6] == pair["explanation_cluster_examples"],
        f"cluster examples mismatch for {pair['pair_id']}",
    )
    require(bound == fraction_from_record(pair["johnson_bound"]), f"Johnson bound mismatch for {pair['pair_id']}")
    require((Fraction(len(cluster), 1) <= bound) == pair["cluster_le_johnson"], f"Johnson boolean mismatch for {pair['pair_id']}")
    require(len(mca) == pair["epsilon_mca_times_q"], f"MCA count mismatch for {pair['pair_id']}")
    require(len(ca) == pair["epsilon_ca_times_q"], f"CA count mismatch for {pair['pair_id']}")
    shape_holds = len(mca) <= len(ca) + len(cluster) * replay.r
    require(shape_holds == pair["shape_holds"], f"shape boolean mismatch for {pair['pair_id']}")
    candidates = replay.candidate_clusters(f1, f2, cluster)
    for candidate in CANDIDATE_ORDER:
        recorded = pair["candidate_clusters"][candidate]
        require(
            candidates[candidate]["count"] == recorded["count"],
            f"{candidate} count mismatch for {pair['pair_id']}",
        )
        if candidate == "C0":
            require(
                candidates[candidate]["records"] == recorded["records"],
                f"{candidate} records mismatch for {pair['pair_id']}",
            )
        else:
            require(
                slim_candidate_payload(candidate, candidates[candidate]["records"], descriptions)
                == recorded,
                f"{candidate} slim payload mismatch for {pair['pair_id']}",
            )
    require(
        slim_witness_records(candidates["mca_witness_records"])
        == pair["candidate_clusters"]["mca_witness_records"],
        f"MCA witness provenance mismatch for {pair['pair_id']}",
    )
    tests = replay.shape_tests(len(mca), len(ca), candidates)
    require(tests == pair["candidate_shape_tests"], f"candidate shape tests mismatch for {pair['pair_id']}")
    require(
        pair["parent_c0_cross_check"]["observed_c0_count"] == candidates["C0"]["count"],
        f"parent C0 observed count mismatch for {pair['pair_id']}",
    )
    baseline_key = (replay.p, replay.n, replay.k, replay.r, pair["pair_id"])
    expected_c0 = PARENT_C0_BASELINE.get(baseline_key)
    require(
        pair["parent_c0_cross_check"]["parent_row"] == (expected_c0 is not None),
        f"parent C0 row marker mismatch for {pair['pair_id']}",
    )
    require(
        pair["parent_c0_cross_check"]["expected_c0_count"] == expected_c0,
        f"parent C0 expected count mismatch for {pair['pair_id']}",
    )
    require(
        pair["parent_c0_cross_check"]["matches_parent"]
        == (expected_c0 is None or candidates["C0"]["count"] == expected_c0),
        f"parent C0 match marker mismatch for {pair['pair_id']}",
    )


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


def candidate_summary_for_pairs(
    pairs: list[dict[str, Any]], descriptions: dict[str, str]
) -> dict[str, Any]:
    candidate_summary = {}
    for candidate in CANDIDATE_ORDER:
        tests = [pair["candidate_shape_tests"][candidate] for pair in pairs]
        candidate_summary[candidate] = {
            "description": descriptions[candidate],
            "all_shape_checks_hold": all(test["shape_holds"] for test in tests),
            "all_candidate_johnson_checks_hold": all(
                test["candidate_le_johnson"] for test in tests
            ),
            "max_candidate_count": max(test["candidate_count"] for test in tests),
            "total_candidate_count": sum(test["candidate_count"] for test in tests),
            "failing_pair_ids": [
                pair["pair_id"]
                for pair in pairs
                if not pair["candidate_shape_tests"][candidate]["shape_holds"]
            ],
        }
    return candidate_summary


def summarize_candidates(
    rows: list[dict[str, Any]], descriptions: dict[str, str]
) -> dict[str, Any]:
    summary = {}
    for candidate in CANDIDATE_ORDER:
        row_summaries = [row["candidate_summary"][candidate] for row in rows]
        summary[candidate] = {
            "description": descriptions[candidate],
            "universal_shape_hold": all(row["all_shape_checks_hold"] for row in row_summaries),
            "universal_johnson_hold": all(
                row["all_candidate_johnson_checks_hold"] for row in row_summaries
            ),
            "max_candidate_count": max(row["max_candidate_count"] for row in row_summaries),
            "total_candidate_count": sum(row["total_candidate_count"] for row in row_summaries),
            "failing_rows": [
                {
                    "row": row["row"],
                    "failing_pair_ids": row["candidate_summary"][candidate]["failing_pair_ids"],
                }
                for row in rows
                if not row["candidate_summary"][candidate]["all_shape_checks_hold"]
            ],
        }
    universal = [
        candidate for candidate in CANDIDATE_ORDER if summary[candidate]["universal_shape_hold"]
    ]
    universal_but_unbounded = [
        candidate for candidate in universal if not summary[candidate]["universal_johnson_hold"]
    ]
    bounded_candidates = [
        candidate for candidate in CANDIDATE_ORDER if summary[candidate]["universal_johnson_hold"]
    ]
    johnson_bounded_universal = [
        candidate for candidate in universal if summary[candidate]["universal_johnson_hold"]
    ]
    smallest_unbounded = None
    if universal_but_unbounded:
        smallest_unbounded = min(
            universal_but_unbounded,
            key=lambda candidate: (
                summary[candidate]["max_candidate_count"],
                summary[candidate]["total_candidate_count"],
                CANDIDATE_ORDER.index(candidate),
            ),
        )
    return {
        "candidates": summary,
        "universal_candidates": universal,
        "johnson_bounded_candidates": bounded_candidates,
        "johnson_bounded_universal_candidates": johnson_bounded_universal,
        "universal_but_unbounded_candidates": universal_but_unbounded,
        "principled_unbounded_candidate": "C1" if "C1" in universal_but_unbounded else None,
        "smallest_universal_but_unbounded_candidate": smallest_unbounded,
        "smallest_universal_but_unbounded_candidate_description": (
            descriptions[smallest_unbounded] if smallest_unbounded else None
        ),
        "unbounded_selection_rule": (
            "Among candidates passing every recorded pair but failing the Johnson size "
            "check, record the one with smallest maximum per-pair count, then smallest "
            "total count, then C0/C1/C2/C3 order. This is not a bounded correction."
        ),
        "negative_finding": (
            "No Johnson-bounded candidate among C0-C3 restores the shape on every "
            "recorded row. C0 is Johnson-bounded but fails; C1, C2, and C3 restore "
            "the shape only while failing the Johnson size check."
        ),
    }


def check_certificate(cert: dict[str, Any]) -> None:
    require(cert["schema_version"] == SCHEMA_VERSION, "schema version mismatch")
    require(cert["proof_status"] == "EXPERIMENTAL", "proof status mismatch")
    require(cert["theorem_problem_id"] == THEOREM_PROBLEM_ID, "theorem/problem id mismatch")
    require(payload_hash(cert) == cert["payload_sha256"], "payload hash mismatch")
    descriptions = cert["candidate_descriptions"]
    require(tuple(descriptions.keys()) == CANDIDATE_ORDER, "candidate description key mismatch")
    check_oracle_exhaustive(cert["oracle_gate"]["exhaustive_deep_row"])
    tangent = cert["oracle_gate"]["f13_tangent_cell"]
    row = tangent["row"]
    replay = InterpolationReplay(row["q"], row["n"], row["k"], row["r"], tuple(tangent["domain"]))
    check_pair(replay, tangent["pair"], descriptions)
    require(tangent["mca_attains_r_plus_1"], "tangent MCA oracle did not attain r+1")
    require(tangent["ca_attains_r_plus_1"], "tangent CA oracle did not attain r+1")

    violations = []
    for annulus in cert["annulus_rows"]:
        row = annulus["row"]
        require(
            row == row_conditions(row["q"], row["n"], row["k"], row["r"]),
            "row-condition record mismatch",
        )
        replay = InterpolationReplay(row["q"], row["n"], row["k"], row["r"], tuple(annulus["domain"]))
        require(
            annulus["support_counts"] == {
                "supports_at_agreement": len(replay.supports_eq_a),
                "supports_at_or_above_agreement": len(replay.supports_ge_a),
            },
            "support-count record mismatch",
        )
        for pair in annulus["pairs"]:
            check_pair(replay, pair, descriptions)
            if not pair["shape_holds"] or not pair["cluster_le_johnson"]:
                violations.append({"row": row, "pair": pair})
        require(
            annulus["candidate_summary"]
            == candidate_summary_for_pairs(annulus["pairs"], descriptions),
            "row candidate summary mismatch",
        )
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
            annulus["parent_c0_cross_check_passed"]
            == all(
                pair["parent_c0_cross_check"]["matches_parent"]
                for pair in annulus["pairs"]
                if pair["parent_c0_cross_check"]["parent_row"]
            ),
            "row parent C0 cross-check summary mismatch",
        )

    candidate_overall = summarize_candidates(cert["annulus_rows"], descriptions)
    require(cert["candidate_overall"] == candidate_overall, "overall candidate summary mismatch")
    oracle_passed = (
        cert["oracle_gate"]["exhaustive_deep_row"]["max_mca_le_r_plus_1"]
        and cert["oracle_gate"]["exhaustive_deep_row"]["max_ca_le_r_plus_1"]
        and cert["oracle_gate"]["f13_tangent_cell"]["mca_attains_r_plus_1"]
        and cert["oracle_gate"]["f13_tangent_cell"]["ca_attains_r_plus_1"]
    )
    require(cert["overall"]["oracle_gate_passed"] == oracle_passed, "oracle summary mismatch")
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
    require(
        cert["overall"]["parent_c0_cross_check_passed"]
        == all(row["parent_c0_cross_check_passed"] for row in cert["annulus_rows"]),
        "overall parent C0 cross-check mismatch",
    )
    require(
        cert["overall"]["no_johnson_bounded_cluster_correction"]
        == (candidate_overall["johnson_bounded_universal_candidates"] == []),
        "bounded correction summary mismatch",
    )
    require(
        cert["overall"]["smallest_universal_but_unbounded_candidate"]
        == candidate_overall["smallest_universal_but_unbounded_candidate"],
        "smallest unbounded candidate mismatch",
    )
    require(
        cert["overall"]["principled_unbounded_candidate"]
        == candidate_overall["principled_unbounded_candidate"],
        "principled unbounded candidate mismatch",
    )
    require(violations == cert["overall"]["violations"], "violation records mismatch")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path, required=True, help="certificate JSON to replay")
    args = parser.parse_args()
    cert = json.loads(args.check.read_text(encoding="utf-8"))
    check_certificate(cert)
    print(f"annulus_corrected_cluster_check: status={STATUS} result=PASS file={args.check.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
