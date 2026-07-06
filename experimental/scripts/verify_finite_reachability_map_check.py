#!/usr/bin/env python3
"""Independent checker for the finite reachability map certificate.

Status: AUDIT / INDEPENDENT_RECHECK.

The checker does not import the generator. It reloads the JSON certificate,
recounts every recorded fixed-dimensional incidence row from the listed basis,
recomputes the exact first and second moments on the small rows, and confirms
that the cited theorem/problem labels exist in the current TeX files.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Iterable


THEOREM_PROBLEM_ID = "prob:band fixed-parameter reachability map independent check"
PROOF_STATUS = "AUDIT / INDEPENDENT_RECHECK"
DETERMINISM = "deterministic exhaustive recheck; no random seed"


REQUIRED_LABELS = {
    "experimental/cap25_v13_experimental.tex": [
        "thm:v13-first-moment",
        "thm:v13-second-moment",
        "lem:v13-gcd",
        "lem:v13-quot-pullback",
        "lem:v13-dim1",
        "lem:v13-concurrency",
        "thm:v13-dim2",
        "thm:v13-fixeddim",
        "rem:v13-conjf-open",
    ],
    "tex/cs25_cap_v12.tex": ["prob:band"],
}


def primitive_root(p: int) -> int:
    factors: list[int] = []
    m = p - 1
    d = 2
    while d * d <= m:
        if m % d == 0:
            factors.append(d)
            while m % d == 0:
                m //= d
        d += 1
    if m > 1:
        factors.append(m)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in factors):
            return g
    raise ValueError(f"no primitive root for F_{p}")


def subgroup(p: int, order: int) -> list[int]:
    g = primitive_root(p)
    omega = pow(g, (p - 1) // order, p)
    values = [pow(omega, i, p) for i in range(order)]
    if len(set(values)) != order:
        raise AssertionError("bad subgroup order")
    return values


def trim(poly: Iterable[int], p: int) -> tuple[int, ...]:
    out = [x % p for x in poly]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return tuple(out)


def coeff(poly: tuple[int, ...], index: int) -> int:
    return poly[index] if index < len(poly) else 0


def poly_mul(a: tuple[int, ...], b: tuple[int, ...], p: int) -> tuple[int, ...]:
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] = (out[i + j] + ai * bj) % p
    return trim(out, p)


def poly_eval(poly: tuple[int, ...], x: int, p: int) -> int:
    acc = 0
    for c in reversed(poly):
        acc = (acc * x + c) % p
    return acc


def locator(roots: tuple[int, ...], p: int) -> tuple[int, ...]:
    poly = (1,)
    for root in roots:
        poly = poly_mul(poly, ((-root) % p, 1), p)
    return poly


def rref(rows: list[list[int]], p: int) -> tuple[list[list[int]], list[int]]:
    work = [[x % p for x in row] for row in rows]
    if not work:
        return [], []
    width = len(work[0])
    rank = 0
    pivots: list[int] = []
    for col in range(width):
        pivot = None
        for row in range(rank, len(work)):
            if work[row][col]:
                pivot = row
                break
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inv = pow(work[rank][col], -1, p)
        work[rank] = [(inv * x) % p for x in work[rank]]
        for row in range(len(work)):
            if row != rank and work[row][col]:
                factor = work[row][col]
                work[row] = [
                    (work[row][i] - factor * work[rank][i]) % p
                    for i in range(width)
                ]
        pivots.append(col)
        rank += 1
        if rank == len(work):
            break
    return work[:rank], pivots


def reduce_by_rref(vector: list[int], basis_rref: list[list[int]], pivots: list[int], p: int) -> list[int]:
    out = [x % p for x in vector]
    for row, pivot in zip(basis_rref, pivots):
        if out[pivot]:
            factor = out[pivot]
            out = [(out[i] - factor * row[i]) % p for i in range(len(out))]
    return out


def vector(poly: tuple[int, ...], width: int) -> list[int]:
    return [coeff(poly, i) for i in range(width)]


def common_roots(basis: list[tuple[int, ...]], H: list[int], p: int) -> list[int]:
    return [h for h in H if all(poly_eval(poly, h, p) == 0 for poly in basis)]


def check_incidence_row(row: dict[str, object]) -> list[str]:
    field = str(row["field"])
    p = int(field.split("_", 1)[1])
    n = int(row["domain"]["n"])  # type: ignore[index]
    j = int(row["j"])
    d = int(row["projective_dimension_d"])
    H = subgroup(p, n)
    if H != list(row["domain"]["elements"]):  # type: ignore[index]
        return [f"{row['name']}: domain elements do not match subgroup reconstruction"]

    basis = [tuple(int(x) for x in poly) for poly in row["basis_locators"]]  # type: ignore[index]
    width = j + 1
    basis_rref, pivots = rref([vector(poly, width) for poly in basis], p)
    incidence = 0
    for combo in itertools.combinations(H, j):
        poly = locator(tuple(combo), p)
        remainder = reduce_by_rref(vector(poly, width), basis_rref, pivots, p)
        if all(x == 0 for x in remainder):
            incidence += 1
    issues: list[str] = []
    if incidence != int(row["census_value"]):
        issues.append(f"{row['name']}: incidence {incidence} != recorded {row['census_value']}")

    c0 = common_roots(basis, H, p)
    if c0 != list(row["common_roots"]):
        issues.append(f"{row['name']}: common roots {c0} != recorded {row['common_roots']}")
    if len(c0) != int(row["common_root_count"]):
        issues.append(f"{row['name']}: common root count mismatch")

    if row["type"] == "fixed_dimension_locator_incidence":
        bound = math.comb(n - len(c0), d)
        if bound != int(row["fixed_dim_bound"]):
            issues.append(f"{row['name']}: fixed-dimensional bound mismatch")
        if incidence > bound or not bool(row["respects_fixed_dim_bound"]):
            issues.append(f"{row['name']}: fixed-dimensional bound not respected")
        if d == 2 and row.get("dim2_bound") is not None:
            dim2 = row["dim2_bound"]  # type: ignore[assignment]
            numerator = math.comb(n, 2)
            denominator = j - 1
            if int(dim2["numerator"]) != numerator or int(dim2["denominator"]) != denominator:  # type: ignore[index]
                issues.append(f"{row['name']}: dim2 bound mismatch")
            if incidence * denominator > numerator or row["respects_dim2_bound"] is not True:
                issues.append(f"{row['name']}: dim2 bound not respected")
    else:
        bound = math.comb(n - len(c0), d)
        if bound != int(row["refined_fixed_dim_bound"]):
            issues.append(f"{row['name']}: refined bound mismatch")
        if incidence > bound or not bool(row["respects_refined_bound"]):
            issues.append(f"{row['name']}: refined fixed-dimensional bound not respected")
    return issues


def syndrome(
    word: tuple[int, ...],
    domain: list[int],
    roots: tuple[int, ...],
    t: int,
    p: int,
) -> tuple[int, ...]:
    ell = locator(roots, p)
    values: list[int] = []
    for power in range(t):
        total = 0
        for idx, x in enumerate(domain):
            total = (total + word[idx] * poly_eval(ell, x, p) * pow(x, power, p)) % p
        values.append(total)
    return tuple(values)


def is_aligned(a: tuple[int, ...], b: tuple[int, ...], p: int) -> bool:
    if all(x == 0 for x in b):
        return False
    pivot = next(i for i, x in enumerate(b) if x != 0)
    scalar = a[pivot] * pow(b[pivot], -1, p)
    return all((a[i] - scalar * b[i]) % p == 0 for i in range(len(a)))


def moment_formula(n: int, j: int, t: int, q: int) -> tuple[Fraction, Fraction]:
    first = Fraction(math.comb(n, j) * (q**t - 1) * q, q ** (2 * t))
    second = Fraction(0, 1)
    for c in range(max(0, 2 * j - n), j + 1):
        h = max(0, t - j + c)
        numerator = q * (q**h - 1) * q ** (2 * (t - h))
        numerator += q**2 * (q ** (t - h) - 1) ** 2
        denominator = q ** (4 * t - 2 * h)
        second += (
            math.comb(n, j)
            * math.comb(j, c)
            * math.comb(n - j, j - c)
            * Fraction(numerator, denominator)
        )
    return first, second


def fraction_from_record(record: dict[str, object]) -> Fraction:
    return Fraction(int(record["numerator"]), int(record["denominator"]))


def check_moment_row(row: dict[str, object]) -> list[str]:
    p = int(str(row["field"]).split("_", 1)[1])
    n = int(row["domain"]["n"])  # type: ignore[index]
    j = int(row["j"])
    t = int(row["t"])
    domain = subgroup(p, n)
    if domain != list(row["domain"]["elements"]):  # type: ignore[index]
        return [f"{row['name']}: domain reconstruction mismatch"]

    roots_list = list(itertools.combinations(domain, j))
    words = list(itertools.product(range(p), repeat=n))
    total = 0
    total_square = 0
    histogram: Counter[int] = Counter()
    syndrome_cache: dict[tuple[int, ...], list[tuple[int, ...]]] = {}
    for roots in roots_list:
        syndrome_cache[roots] = [syndrome(word, domain, roots, t, p) for word in words]
    for u_index in range(len(words)):
        for v_index in range(len(words)):
            count = 0
            for roots in roots_list:
                if is_aligned(syndrome_cache[roots][u_index], syndrome_cache[roots][v_index], p):
                    count += 1
            histogram[count] += 1
            total += count
            total_square += count * count

    denominator = len(words) * len(words)
    observed_first = Fraction(total, denominator)
    observed_second = Fraction(total_square, denominator)
    theorem_first, theorem_second = moment_formula(n, j, t, p)
    issues: list[str] = []
    if observed_first != theorem_first:
        issues.append(f"{row['name']}: first moment formula mismatch")
    if observed_second != theorem_second:
        issues.append(f"{row['name']}: second moment formula mismatch")
    if observed_first != fraction_from_record(row["observed_first_moment"]):  # type: ignore[arg-type]
        issues.append(f"{row['name']}: recorded observed first moment mismatch")
    if observed_second != fraction_from_record(row["observed_second_moment"]):  # type: ignore[arg-type]
        issues.append(f"{row['name']}: recorded observed second moment mismatch")
    if theorem_first != fraction_from_record(row["theorem_first_moment"]):  # type: ignore[arg-type]
        issues.append(f"{row['name']}: recorded theorem first moment mismatch")
    if theorem_second != fraction_from_record(row["theorem_second_moment"]):  # type: ignore[arg-type]
        issues.append(f"{row['name']}: recorded theorem second moment mismatch")
    recorded_hist = {int(k): int(v) for k, v in row["histogram_N_A"].items()}  # type: ignore[index]
    if dict(histogram) != recorded_hist:
        issues.append(f"{row['name']}: N_A histogram mismatch")
    return issues


def check_labels(repo_root: Path) -> list[str]:
    issues: list[str] = []
    for relative, labels in REQUIRED_LABELS.items():
        text = (repo_root / relative).read_text(encoding="utf-8")
        for label in labels:
            if f"\\label{{{label}}}" not in text:
                issues.append(f"missing label {label} in {relative}")
    return issues


def check_certificate(path: Path, repo_root: Path) -> list[str]:
    cert = json.loads(path.read_text(encoding="utf-8"))
    issues: list[str] = []
    if cert.get("schema") != "finite_reachability_map_v1":
        issues.append("schema mismatch")
    if cert.get("status") != "PASS":
        issues.append("certificate status is not PASS")
    if cert.get("proof_status") != "EXPERIMENTAL / SCOPE-MAP":
        issues.append("proof_status mismatch")
    if cert.get("evidence_type") != "FULL_FINITE_CENSUS":
        issues.append("evidence_type mismatch")

    boundaries = cert.get("claim_boundaries", {})
    expected_false = [
        "is_counterexample",
        "is_full_canonical_statement_not_proxy_or_toy_row",
        "resolves_or_advances_prob_band",
        "proves_prob_band_undecidable",
        "claims_no_method_can_reach",
        "beats_or_narrows_trivial_baseline",
    ]
    for key in expected_false:
        if boundaries.get(key) is not False:
            issues.append(f"claim_boundaries.{key} should be false")
    if boundaries.get("is_novel_not_confirming_a_proven_theorem") is not True:
        issues.append("scope-map novelty boundary should be true")
    if boundaries.get("independent_recheck_confirms") is not True:
        issues.append("independent_recheck_confirms should be true")
    if cert.get("is_tautology_under_preconditions") is not True:
        issues.append("is_tautology_under_preconditions should be true")
    if cert.get("beats_trivial_baseline") is not False:
        issues.append("beats_trivial_baseline should be false")

    for row in cert.get("incidence_rows", []):
        issues.extend(check_incidence_row(row))
    for row in cert.get("moment_rows", []):
        issues.extend(check_moment_row(row))
    issues.extend(check_labels(repo_root))
    return issues


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", required=True, type=Path)
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    issues = check_certificate(args.check, repo_root)
    print("=" * 72)
    print("Finite reachability map independent checker")
    print("=" * 72)
    print(f"theorem_problem_id: {THEOREM_PROBLEM_ID}")
    print(f"proof_status: {PROOF_STATUS}")
    print(f"determinism: {DETERMINISM}")
    if issues:
        for issue in issues:
            print(f"FAIL: {issue}")
        raise SystemExit(1)
    print("CHECK PASS")


if __name__ == "__main__":
    main()
