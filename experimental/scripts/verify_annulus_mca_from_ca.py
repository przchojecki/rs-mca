#!/usr/bin/env python3
"""Finite annulus MCA-from-CA verification for small Reed-Solomon rows.

Status: EXPERIMENTAL. This script records exact finite evidence for the
annulus MCA-from-CA shape. It is not a proof of the annulus theorem and does
not resolve prob:band.

The default packet first runs an oracle gate in the proved deep regime, then
tests constructed and deterministic sampled annulus pairs. All arithmetic is
exact over prime fields; rational quantities use fractions.Fraction.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
from collections import Counter
from fractions import Fraction
from math import comb
from pathlib import Path
from typing import Any


STATUS = "EXPERIMENTAL"
THEOREM_PROBLEM_ID = "Task A.3 annulus MCA-from-CA finite verification"
SCHEMA_VERSION = "annulus-mca-from-ca-v1"
DEFAULT_OUTPUT = Path(
    "experimental/data/certificates/annulus-mca-from-ca/annulus_mca_from_ca.json"
)

ORACLE_EXHAUSTIVE_ROW = (5, 4, 1, 1)
ORACLE_TANGENT_ROW = (13, 12, 6, 2)
ANNULUS_ROWS = (
    (11, 10, 3, 4),
    (13, 12, 5, 4),
    (17, 16, 7, 5),
    (31, 10, 3, 4),
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def inv(value: int, p: int) -> int:
    value %= p
    if value == 0:
        raise ZeroDivisionError("zero has no inverse")
    return pow(value, p - 2, p)


def fraction_record(value: Fraction) -> dict[str, int | str]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "text": f"{value.numerator}/{value.denominator}",
    }


def poly_trim(coeffs: list[int]) -> list[int]:
    out = [value for value in coeffs]
    while out and out[-1] == 0:
        out.pop()
    return out


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


def poly_from_roots(roots: list[int], p: int) -> tuple[int, ...]:
    coeffs = [1]
    for root in roots:
        coeffs = poly_mul(coeffs, [(-root) % p, 1], p)
    return tuple(coeffs)


def coeff_key(coeffs: tuple[int, ...] | list[int], k: int, p: int) -> tuple[int, ...]:
    out = [value % p for value in coeffs[:k]]
    out.extend([0] * (k - len(out)))
    return tuple(out)


def word_from_coeffs(coeffs: tuple[int, ...], domain: tuple[int, ...], p: int) -> tuple[int, ...]:
    return tuple(poly_eval(coeffs, x, p) for x in domain)


def factorize(value: int) -> list[int]:
    factors: list[int] = []
    d = 2
    while d * d <= value:
        if value % d == 0:
            factors.append(d)
            while value % d == 0:
                value //= d
        d += 1 if d == 2 else 2
    if value > 1:
        factors.append(value)
    return factors


def primitive_root(p: int) -> int:
    factors = factorize(p - 1)
    for candidate in range(2, p):
        if all(pow(candidate, (p - 1) // factor, p) != 1 for factor in factors):
            return candidate
    raise ValueError(f"no primitive root for F_{p}")


def subgroup(p: int, n: int) -> tuple[int, ...]:
    require((p - 1) % n == 0, "domain order must divide p-1")
    gen = pow(primitive_root(p), (p - 1) // n, p)
    values: list[int] = []
    x = 1
    for _ in range(n):
        values.append(x)
        x = (x * gen) % p
    require(x == 1 and len(set(values)) == n, "bad subgroup generator")
    return tuple(values)


def rref_modp(matrix: list[list[int]], p: int) -> tuple[list[list[int]], list[int]]:
    rows = [[value % p for value in row] for row in matrix]
    if not rows:
        return rows, []
    row_count = len(rows)
    col_count = len(rows[0])
    pivots: list[int] = []
    pivot_row = 0
    for col in range(col_count):
        pivot = None
        for row in range(pivot_row, row_count):
            if rows[row][col] % p:
                pivot = row
                break
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        scale = inv(rows[pivot_row][col], p)
        rows[pivot_row] = [(value * scale) % p for value in rows[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or rows[row][col] % p == 0:
                continue
            factor = rows[row][col] % p
            rows[row] = [
                (rows[row][idx] - factor * rows[pivot_row][idx]) % p
                for idx in range(col_count)
            ]
        pivots.append(col)
        pivot_row += 1
        if pivot_row == row_count:
            break
    return rows, pivots


def nullspace_modp(matrix: list[list[int]], p: int) -> list[list[int]]:
    if not matrix:
        return []
    rref, pivots = rref_modp(matrix, p)
    col_count = len(rref[0])
    pivot_set = set(pivots)
    free_cols = [col for col in range(col_count) if col not in pivot_set]
    basis: list[list[int]] = []
    for free_col in free_cols:
        vector = [0] * col_count
        vector[free_col] = 1
        for row, pivot_col in enumerate(pivots):
            vector[pivot_col] = (-rref[row][free_col]) % p
        basis.append(vector)
    return basis


def parity_checks_for_support(
    p: int, domain: tuple[int, ...], k: int, support: tuple[int, ...]
) -> tuple[tuple[tuple[int, int], ...], ...]:
    if len(support) <= k:
        return ()
    matrix = [[pow(domain[index], degree, p) for index in support] for degree in range(k)]
    checks = []
    for vector in nullspace_modp(matrix, p):
        sparse = tuple(
            (support[pos], coeff % p)
            for pos, coeff in enumerate(vector)
            if coeff % p
        )
        checks.append(sparse)
    return tuple(checks)


def fit_by_checks(
    word: tuple[int, ...], checks: tuple[tuple[tuple[int, int], ...], ...], p: int
) -> bool:
    return all(sum(coeff * word[index] for index, coeff in row) % p == 0 for row in checks)


def interpolate_coeffs(
    p: int, xs: tuple[int, ...], ys: tuple[int, ...], k: int
) -> tuple[int, ...]:
    require(len(xs) >= k and len(ys) >= k, "need at least k interpolation points")
    points = list(zip(xs[:k], ys[:k]))
    result: list[int] = []
    for i, (xi, yi) in enumerate(points):
        basis = [1]
        denom = 1
        for j, (xj, _yj) in enumerate(points):
            if i == j:
                continue
            basis = poly_mul(basis, [(-xj) % p, 1], p)
            denom = (denom * ((xi - xj) % p)) % p
        scale = yi * inv(denom, p)
        if len(result) < len(basis):
            result.extend([0] * (len(basis) - len(result)))
        for idx, coeff in enumerate(basis):
            result[idx] = (result[idx] + scale * coeff) % p
    return coeff_key(tuple(result), k, p)


class RSAnalyzer:
    def __init__(self, p: int, n: int, k: int, r: int):
        self.p = p
        self.n = n
        self.k = k
        self.r = r
        self.a = n - r
        self.domain = subgroup(p, n)
        self._checks: dict[tuple[int, ...], tuple[tuple[tuple[int, int], ...], ...]] = {}
        self.supports_ge_a = [
            tuple(support)
            for size in range(self.a, self.n + 1)
            for support in itertools.combinations(range(self.n), size)
        ]
        self.supports_eq_a = [
            tuple(support) for support in itertools.combinations(range(self.n), self.a)
        ]

    def checks(self, support: tuple[int, ...]) -> tuple[tuple[tuple[int, int], ...], ...]:
        if support not in self._checks:
            self._checks[support] = parity_checks_for_support(
                self.p, self.domain, self.k, support
            )
        return self._checks[support]

    def fits(self, word: tuple[int, ...], support: tuple[int, ...]) -> bool:
        return fit_by_checks(word, self.checks(support), self.p)

    def pair_fits(
        self, f1: tuple[int, ...], f2: tuple[int, ...], support: tuple[int, ...]
    ) -> bool:
        return self.fits(f1, support) and self.fits(f2, support)

    def add_scaled(
        self, f1: tuple[int, ...], gamma: int, f2: tuple[int, ...]
    ) -> tuple[int, ...]:
        return tuple((x + gamma * y) % self.p for x, y in zip(f1, f2))

    def close_slopes(self, f1: tuple[int, ...], f2: tuple[int, ...]) -> tuple[int, ...]:
        close: list[int] = []
        for gamma in range(self.p):
            point = self.add_scaled(f1, gamma, f2)
            if any(self.fits(point, support) for support in self.supports_ge_a):
                close.append(gamma)
        return tuple(close)

    def mca_bad_slopes(self, f1: tuple[int, ...], f2: tuple[int, ...]) -> tuple[int, ...]:
        bad: list[int] = []
        for gamma in range(self.p):
            point = self.add_scaled(f1, gamma, f2)
            for support in self.supports_ge_a:
                if self.fits(point, support) and not self.pair_fits(f1, f2, support):
                    bad.append(gamma)
                    break
        return tuple(bad)

    def explanation_cluster(
        self, f1: tuple[int, ...], f2: tuple[int, ...]
    ) -> list[dict[str, Any]]:
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
            word1 = word_from_coeffs(p1, self.domain, self.p)
            word2 = word_from_coeffs(p2, self.domain, self.p)
            full_support = tuple(
                idx
                for idx, (x1, x2, y1, y2) in enumerate(zip(f1, f2, word1, word2))
                if x1 == y1 and x2 == y2
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

    def analyze_pair(self, pair: dict[str, Any]) -> dict[str, Any]:
        f1 = tuple(pair["f1"])
        f2 = tuple(pair["f2"])
        cluster = self.explanation_cluster(f1, f2)
        close = self.close_slopes(f1, f2)
        mca = self.mca_bad_slopes(f1, f2)
        ca = self.ca_bad_slopes(f1, f2, cluster)
        johnson = johnson_bound(self.n, self.k, self.a)
        shape_left = len(mca)
        shape_right = len(ca) + len(cluster) * self.r
        return {
            "pair_id": pair["pair_id"],
            "construction": pair["construction"],
            "f1": list(f1),
            "f2": list(f2),
            "close_slopes": list(close),
            "mca_bad_slopes": list(mca),
            "ca_bad_slopes": list(ca),
            "epsilon_mca_times_q": len(mca),
            "epsilon_ca_times_q": len(ca),
            "explanation_cluster_size": len(cluster),
            "explanation_cluster_examples": cluster[:6],
            "johnson_agreement": self.a,
            "johnson_bound": fraction_record(johnson),
            "cluster_le_johnson": Fraction(len(cluster), 1) <= johnson,
            "shape_lhs_count": shape_left,
            "shape_rhs_count": shape_right,
            "shape_holds": shape_left <= shape_right,
        }


def johnson_bound(n: int, k: int, agreement: int) -> Fraction:
    denominator = agreement * agreement - (k - 1) * n
    require(denominator > 0, "Johnson denominator must be positive")
    return Fraction(n * (agreement - k + 1), denominator)


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


def tangent_pair(analyzer: RSAnalyzer, pair_id: str, construction: str) -> dict[str, Any]:
    support = list(range(analyzer.r + 1))
    f1 = [0] * analyzer.n
    f2 = [0] * analyzer.n
    for offset, index in enumerate(support):
        gamma = offset % analyzer.p
        f1[index] = (-gamma) % analyzer.p
        f2[index] = 1
    return {
        "pair_id": pair_id,
        "construction": construction,
        "tangent_support": support,
        "f1": f1,
        "f2": f2,
    }


def clustered_pair(analyzer: RSAnalyzer, pair_id: str) -> dict[str, Any]:
    h = analyzer.k - 1
    unique = analyzer.a - h
    require(h >= 0 and unique > 0, "bad cluster dimensions")
    require(h + 2 * unique <= analyzer.n, "row does not fit two planted supports")
    overlap = list(range(h))
    block0 = list(range(h, h + unique))
    block1 = list(range(h + unique, h + 2 * unique))
    roots = [analyzer.domain[index] for index in overlap]
    base_poly = coeff_key(poly_from_roots(roots, analyzer.p), analyzer.k, analyzer.p)
    p1_coeffs = base_poly
    p2_coeffs = tuple((2 * coeff) % analyzer.p for coeff in base_poly)
    word1 = word_from_coeffs(p1_coeffs, analyzer.domain, analyzer.p)
    word2 = word_from_coeffs(p2_coeffs, analyzer.domain, analyzer.p)
    f1 = [0] * analyzer.n
    f2 = [0] * analyzer.n
    for index in block1:
        f1[index] = word1[index]
        f2[index] = word2[index]
    # Any leftover coordinates get a deterministic non-codeword-looking fill.
    used = set(overlap + block0 + block1)
    for index in range(analyzer.n):
        if index not in used:
            f1[index] = (index * index + 3) % analyzer.p
            f2[index] = (index + 5) % analyzer.p
    return {
        "pair_id": pair_id,
        "construction": "two planted incomparable explanations with overlap k-1",
        "planted_supports": [overlap + block0, overlap + block1],
        "planted_overlap": overlap,
        "f1": f1,
        "f2": f2,
    }


def sampled_close_pair(analyzer: RSAnalyzer, pair_id: str, seed: int) -> dict[str, Any]:
    rng = random.Random(seed)
    support = sorted(rng.sample(range(analyzer.n), analyzer.a))
    coeffs1 = tuple(rng.randrange(analyzer.p) for _ in range(analyzer.k))
    coeffs2 = tuple(rng.randrange(analyzer.p) for _ in range(analyzer.k))
    word1 = word_from_coeffs(coeffs1, analyzer.domain, analyzer.p)
    word2 = word_from_coeffs(coeffs2, analyzer.domain, analyzer.p)
    f1 = [(7 * index + 3) % analyzer.p for index in range(analyzer.n)]
    f2 = [(5 * index + 1) % analyzer.p for index in range(analyzer.n)]
    for index in support:
        f1[index] = word1[index]
        f2[index] = word2[index]
    return {
        "pair_id": pair_id,
        "construction": "deterministic seeded close sample",
        "seed": seed,
        "planted_supports": [support],
        "f1": f1,
        "f2": f2,
    }


def exhaustive_deep_oracle() -> dict[str, Any]:
    p, n, k, r = ORACLE_EXHAUSTIVE_ROW
    analyzer = RSAnalyzer(p, n, k, r)
    max_mca = -1
    max_ca = -1
    max_mca_example: dict[str, Any] | None = None
    max_ca_example: dict[str, Any] | None = None
    for values in itertools.product(range(p), repeat=2 * n):
        f1 = tuple(values[:n])
        f2 = tuple(values[n:])
        cluster = analyzer.explanation_cluster(f1, f2)
        mca = analyzer.mca_bad_slopes(f1, f2)
        ca = analyzer.ca_bad_slopes(f1, f2, cluster)
        if len(mca) > max_mca:
            max_mca = len(mca)
            max_mca_example = {
                "f1": list(f1),
                "f2": list(f2),
                "mca_bad_slopes": list(mca),
            }
        if len(ca) > max_ca:
            max_ca = len(ca)
            max_ca_example = {
                "f1": list(f1),
                "f2": list(f2),
                "ca_bad_slopes": list(ca),
            }
    expected = r + 1
    return {
        "row": row_conditions(p, n, k, r),
        "domain": list(analyzer.domain),
        "all_pairs_examined": p ** (2 * n),
        "expected_r_plus_1": expected,
        "max_mca_bad_slopes": max_mca,
        "max_ca_bad_slopes": max_ca,
        "max_mca_le_r_plus_1": max_mca <= expected,
        "max_ca_le_r_plus_1": max_ca <= expected,
        "max_mca_attains_r_plus_1": max_mca == expected,
        "max_ca_attains_r_plus_1": max_ca == expected,
        "max_mca_example": max_mca_example,
        "max_ca_example": max_ca_example,
    }


def tangent_oracle() -> dict[str, Any]:
    p, n, k, r = ORACLE_TANGENT_ROW
    analyzer = RSAnalyzer(p, n, k, r)
    pair = tangent_pair(analyzer, "f13_tangent_cell", "prop:v13-tangent construction")
    row = analyzer.analyze_pair(pair)
    expected = r + 1
    return {
        "row": row_conditions(p, n, k, r),
        "domain": list(analyzer.domain),
        "expected_r_plus_1": expected,
        "pair": row,
        "mca_attains_r_plus_1": row["epsilon_mca_times_q"] == expected,
        "ca_attains_r_plus_1": row["epsilon_ca_times_q"] == expected,
    }


def annulus_row(p: int, n: int, k: int, r: int) -> dict[str, Any]:
    analyzer = RSAnalyzer(p, n, k, r)
    conditions = row_conditions(p, n, k, r)
    require(conditions["annulus_below_half_distance"], "row must be in strict annulus")
    require(conditions["agreement_above_sqrt_kn"], "agreement must exceed sqrt(kn)")
    require(
        conditions["agreement_below_half_distance_boundary"],
        "agreement must be below (n+k)/2",
    )
    require(
        conditions["johnson_for_explanation_agreement"],
        "Johnson bound at explanation agreement must apply",
    )
    pairs = [
        clustered_pair(analyzer, "cluster_two_explanations"),
        tangent_pair(analyzer, "annulus_tangent_like", "tangent-cell construction outside deep range"),
        sampled_close_pair(analyzer, "seeded_close_sample", seed=1000 + p * 100 + n * 10 + k),
    ]
    analyzed = [analyzer.analyze_pair(pair) for pair in pairs]
    return {
        "row": conditions,
        "domain": list(analyzer.domain),
        "support_counts": {
            "supports_at_agreement": len(analyzer.supports_eq_a),
            "supports_at_or_above_agreement": len(analyzer.supports_ge_a),
        },
        "pairs": analyzed,
        "all_cluster_johnson_checks_hold": all(pair["cluster_le_johnson"] for pair in analyzed),
        "all_shape_checks_hold": all(pair["shape_holds"] for pair in analyzed),
    }


def attach_payload_hash(payload: dict[str, Any]) -> dict[str, Any]:
    clone = json.loads(json.dumps(payload, sort_keys=True))
    clone.pop("payload_sha256", None)
    rendered = json.dumps(clone, sort_keys=True, separators=(",", ":"))
    clone["payload_sha256"] = hashlib.sha256(rendered.encode("utf-8")).hexdigest()
    return clone


def build_certificate() -> dict[str, Any]:
    annulus_rows = [annulus_row(*row) for row in ANNULUS_ROWS]
    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "proof_status": STATUS,
        "theorem_problem_id": THEOREM_PROBLEM_ID,
        "claim": (
            "Finite oracle-gated study of the annulus MCA-from-CA shape: the A.3 "
            "cluster condition n-2r>sqrt((k-1)n) is unsatisfiable in the annulus; "
            "under the natural a=n-r reading, the pair-explanation cluster does not "
            "bound MCA-bad slopes on all recorded rows."
        ),
        "recorded_findings": [
            {
                "finding": "a3_cluster_condition_unsatisfiable_in_strict_annulus",
                "status": "EXPERIMENTAL / AUDIT",
                "proof": (
                    "If 2r>n-k then n-2r<=k-1, while sqrt((k-1)n)>k-1 for k<n; "
                    "therefore n-2r>sqrt((k-1)n) has no strict-annulus instance."
                ),
            },
            {
                "finding": "naive_cluster_correction_insufficient_under_a_equals_n_minus_r_reading",
                "status": "EXPERIMENTAL",
                "witness_row": {"q": 13, "n": 12, "k": 5, "r": 4, "a": 8},
                "witness_pair_id": "seeded_close_sample",
                "summary": "MCA count 5, CA count 0, cluster size 1, right side 4.",
            },
        ],
        "non_claims": [
            "This is not a proof of the annulus MCA-from-CA theorem.",
            "This is not a prob:band resolution.",
            "The strict-annulus condition 2r>n-k is incompatible with n-2r>sqrt((k-1)n); the packet records the A=n-r Johnson check instead.",
        ],
        "definition_sources": {
            "tex/cs25_cap_v12.tex:131": "def:ca defines CA-bad slopes and eca normalization.",
            "tex/cs25_cap_v12.tex:139": "def:mca defines support-wise MCA-bad slopes and emca normalization.",
            "tex/cs25_cap_v12.tex:4504": "thm:deep-mca gives the r+1 oracle upper bound in 3r<=n-k.",
            "tex/cs25_cap_v12.tex:4627": "thm:johnson-list gives the interleaved Johnson list bound.",
            "tex/cs25_cap_v12.tex:4939": "thm:mca-from-ca gives the half-distance MCA-from-CA reduction.",
            "tex/cs25_cap_v12.tex:4970": "rem:half-scope identifies multiple explanations below half distance.",
            "tex/cs25_cap_v12.tex:4974": "cor:band-reduction records the support-mismatch reduction below half distance.",
            "experimental/cap25_v13_experimental.tex:171": "prop:v13-tangent gives the exact r+1 tangent cell used as an oracle witness.",
        },
        "oracle_gate": {
            "exhaustive_deep_row": exhaustive_deep_oracle(),
            "f13_tangent_cell": tangent_oracle(),
        },
        "annulus_rows": annulus_rows,
        "overall": {
            "oracle_gate_passed": True,
            "all_annulus_cluster_johnson_checks_hold": all(
                row["all_cluster_johnson_checks_hold"] for row in annulus_rows
            ),
            "all_annulus_shape_checks_hold": all(
                row["all_shape_checks_hold"] for row in annulus_rows
            ),
            "violations": [
                {
                    "row": row["row"],
                    "pair": pair,
                }
                for row in annulus_rows
                for pair in row["pairs"]
                if not pair["cluster_le_johnson"] or not pair["shape_holds"]
            ],
        },
    }
    payload["overall"]["oracle_gate_passed"] = (
        payload["oracle_gate"]["exhaustive_deep_row"]["max_mca_le_r_plus_1"]
        and payload["oracle_gate"]["exhaustive_deep_row"]["max_ca_le_r_plus_1"]
        and payload["oracle_gate"]["f13_tangent_cell"]["mca_attains_r_plus_1"]
        and payload["oracle_gate"]["f13_tangent_cell"]["ca_attains_r_plus_1"]
    )
    return attach_payload_hash(payload)


def render_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit-defaults", action="store_true", help="write the default certificate")
    parser.add_argument("--check", type=Path, help="compare a certificate to a fresh run")
    args = parser.parse_args()

    cert = build_certificate()
    rendered = render_json(cert)

    if args.emit_defaults:
        DEFAULT_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        DEFAULT_OUTPUT.write_text(rendered, encoding="utf-8")
        print(
            "annulus_mca_from_ca: "
            f"status={STATUS} result=PASS "
            f"oracle={cert['overall']['oracle_gate_passed']} "
            f"rows={len(cert['annulus_rows'])} "
            f"shape={cert['overall']['all_annulus_shape_checks_hold']}"
        )
        print(DEFAULT_OUTPUT.as_posix())
    elif args.check:
        existing = args.check.read_text(encoding="utf-8")
        require(existing == rendered, f"certificate mismatch: {args.check}")
        print(f"annulus_mca_from_ca: status={STATUS} result=PASS file={args.check.as_posix()}")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
