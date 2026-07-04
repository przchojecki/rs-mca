#!/usr/bin/env python3
"""Exact toy-row verifier for the sparse sigma_C MCA layer.

This is intentionally a small CPU certificate path. It brute-forces tiny
prime-field rows and checks the sparse mutual layer from `towards-prize.tex`
using the maximal witness set

    S_z = {i in D : eps1_i + gamma eps2_i = z_i}

for each close codeword z. Finite slopes only are counted. The verifier does
not quotient by projective/Mobius symmetries; future optimized searches should
only use slope-preserving upper-triangular reductions before returning to this
exact checker.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


SCHEMA_VERSION = "sigma-c-sparse-census-v1"
SCHEMA_VERSION_V2 = "sigma-c-sparse-census-v2"
HANKEL_SCAN_SCHEMA_VERSION = "sigma-c-sparse-census-hankel-scan-v1"
DEFAULT_ROWS = (
    {"q": 5, "n": 4, "k": 2, "r": 1, "expected_sigma_c": 1},
    {"q": 7, "n": 6, "k": 3, "r": 1, "expected_sigma_c": 1},
    {"q": 5, "n": 4, "k": 2, "r": 2, "expected_sigma_c": None},
)


@dataclass(frozen=True)
class Row:
    q: int
    n: int
    k: int
    r: int
    expected_sigma_c: int | None = None


def render(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def inv(value: int, p: int) -> int:
    value %= p
    require(value != 0, "division by zero")
    return pow(value, p - 2, p)


def prime_factors(value: int) -> list[int]:
    out: list[int] = []
    d = 2
    while d * d <= value:
        if value % d == 0:
            out.append(d)
            while value % d == 0:
                value //= d
        d += 1
    if value > 1:
        out.append(value)
    return out


def primitive_root(p: int) -> int:
    require(p >= 3, "q must be an odd prime in this toy verifier")
    factors = prime_factors(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // factor, p) != 1 for factor in factors):
            return g
    raise ValueError(f"no primitive root found for F_{p}")


def subgroup_domain(q: int, n: int) -> tuple[int, ...]:
    require((q - 1) % n == 0, "n must divide q-1")
    gen = primitive_root(q)
    step = pow(gen, (q - 1) // n, q)
    values: list[int] = []
    x = 1
    for _ in range(n):
        values.append(x)
        x = (x * step) % q
    require(x == 1 and len(set(values)) == n, "domain generator has wrong order")
    return tuple(values)


def poly_eval(coeffs: tuple[int, ...], x: int, q: int) -> int:
    acc = 0
    power = 1
    for coeff in coeffs:
        acc = (acc + coeff * power) % q
        power = (power * x) % q
    return acc


def poly_add(left: list[int], right: list[int], q: int) -> list[int]:
    size = max(len(left), len(right))
    out = [0] * size
    for index in range(size):
        out[index] = ((left[index] if index < len(left) else 0) + (right[index] if index < len(right) else 0)) % q
    return out


def poly_mul_linear(poly: list[int], root: int, q: int) -> list[int]:
    out = [0] * (len(poly) + 1)
    for index, coeff in enumerate(poly):
        out[index] = (out[index] - coeff * root) % q
        out[index + 1] = (out[index + 1] + coeff) % q
    return out


def interpolate_coefficients(points: list[tuple[int, int]], q: int) -> tuple[int, ...]:
    require(points, "cannot interpolate an empty point set")
    coeffs = [0]
    for i, (xi, yi) in enumerate(points):
        basis = [1]
        denom = 1
        for j, (xj, _yj) in enumerate(points):
            if i == j:
                continue
            basis = poly_mul_linear(basis, xj, q)
            denom = (denom * (xi - xj)) % q
        scale = yi * inv(denom, q)
        coeffs = poly_add(coeffs, [(scale * coeff) % q for coeff in basis], q)
    while len(coeffs) > 1 and coeffs[-1] == 0:
        coeffs.pop()
    return tuple(coeffs)


def restriction_coefficients(
    values: tuple[int, ...],
    support: tuple[int, ...],
    domain: tuple[int, ...],
    k: int,
    q: int,
) -> tuple[int, ...] | None:
    if len(support) <= k:
        points = [(domain[index], values[index]) for index in support]
        if not points:
            return (0,)
        return interpolate_coefficients(points, q)
    base = support[:k]
    coeffs = interpolate_coefficients([(domain[index], values[index]) for index in base], q)
    if all(poly_eval(coeffs, domain[index], q) == values[index] for index in support):
        return coeffs
    return None


def all_codewords(q: int, domain: tuple[int, ...], k: int) -> tuple[tuple[int, ...], ...]:
    words: list[tuple[int, ...]] = []
    for coeffs in itertools.product(range(q), repeat=k):
        words.append(tuple(poly_eval(coeffs, x, q) for x in domain))
    return tuple(words)


def support_restricts_to_code(
    eps2: tuple[int, ...],
    support: tuple[int, ...],
    codewords: tuple[tuple[int, ...], ...],
    k: int,
) -> bool:
    # Any assignment on at most k distinct RS domain points interpolates.
    if len(support) <= k:
        return True
    for codeword in codewords:
        if all(codeword[i] == eps2[i] for i in support):
            return True
    return False


def hamming_distance(a: tuple[int, ...], b: tuple[int, ...]) -> int:
    return sum(x != y for x, y in zip(a, b, strict=True))


def enumerate_error_pairs(q: int, n: int, r: int) -> Iterable[tuple[tuple[int, ...], tuple[int, ...]]]:
    value_pairs = [(a, b) for a in range(q) for b in range(q) if a != 0 or b != 0]
    zero = (0,) * n
    yield zero, zero
    for size in range(1, r + 1):
        for support in itertools.combinations(range(n), size):
            for values in itertools.product(value_pairs, repeat=size):
                eps1 = [0] * n
                eps2 = [0] * n
                for index, (a, b) in zip(support, values, strict=True):
                    eps1[index] = a
                    eps2[index] = b
                yield tuple(eps1), tuple(eps2)


def bad_slope_witnesses(
    eps1: tuple[int, ...],
    eps2: tuple[int, ...],
    q: int,
    r: int,
    codewords: tuple[tuple[int, ...], ...],
    k: int,
) -> list[dict[str, Any]]:
    witnesses: list[dict[str, Any]] = []
    n = len(eps1)
    for gamma in range(q):
        word = tuple((eps1[i] + gamma * eps2[i]) % q for i in range(n))
        found: dict[str, Any] | None = None
        for codeword_index, codeword in enumerate(codewords):
            distance = hamming_distance(word, codeword)
            if distance > r:
                continue
            maximal_support = tuple(i for i, (wi, zi) in enumerate(zip(word, codeword, strict=True)) if wi == zi)
            if not support_restricts_to_code(eps2, maximal_support, codewords, k):
                found = {
                    "gamma": gamma,
                    "codeword_index": codeword_index,
                    "distance": distance,
                    "maximal_witness_set": list(maximal_support),
                    "agreement": len(maximal_support),
                }
                break
        if found is not None:
            witnesses.append(found)
    return witnesses


def sparse_union_size(eps1: tuple[int, ...], eps2: tuple[int, ...]) -> int:
    return sum(a != 0 or b != 0 for a, b in zip(eps1, eps2, strict=True))


def lagrange_weights(domain: tuple[int, ...], q: int) -> tuple[int, ...]:
    weights: list[int] = []
    for i, x in enumerate(domain):
        denom = 1
        for j, y in enumerate(domain):
            if i != j:
                denom = (denom * (x - y)) % q
        weights.append(inv(denom, q))
    return tuple(weights)


def syndrome(
    word: tuple[int, ...],
    domain: tuple[int, ...],
    weights: tuple[int, ...],
    q: int,
    m: int,
) -> tuple[int, ...]:
    return tuple(
        sum(weight * pow(x, a, q) * value for weight, x, value in zip(weights, domain, word, strict=True)) % q
        for a in range(m)
    )


def hankel_window(syn: tuple[int, ...], m: int, r: int) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(syn[a + b] for b in range(r + 1)) for a in range(m - r))


def locator_coefficients(domain: tuple[int, ...], disagreement_set: tuple[int, ...], q: int) -> tuple[int, ...]:
    coeffs = [1]
    for index in disagreement_set:
        x = domain[index]
        next_coeffs = [0] * (len(coeffs) + 1)
        for power, coeff in enumerate(coeffs):
            next_coeffs[power] = (next_coeffs[power] - coeff * x) % q
            next_coeffs[power + 1] = (next_coeffs[power + 1] + coeff) % q
        coeffs = next_coeffs
    return tuple(coeffs)


def mat_vec(matrix: tuple[tuple[int, ...], ...], vector: tuple[int, ...], q: int) -> tuple[int, ...]:
    return tuple(sum(row[col] * vector[col] for col in range(len(vector))) % q for row in matrix)


def candidate_gamma_for_shape(h1_ell: tuple[int, ...], h2_ell: tuple[int, ...], q: int) -> int | None:
    """Solve h1_ell + gamma*h2_ell = 0 for one finite gamma, if consistent."""

    require(len(h1_ell) == len(h2_ell), "shape functional vectors have different lengths")
    gamma: int | None = None
    for left, right in zip(h1_ell, h2_ell, strict=True):
        left %= q
        right %= q
        if right == 0:
            if left != 0:
                return None
            continue
        local_gamma = (-left * inv(right, q)) % q
        if gamma is None:
            gamma = local_gamma
        elif gamma != local_gamma:
            return None
    return gamma


def bad_slope_witnesses_hankel(
    eps1: tuple[int, ...],
    eps2: tuple[int, ...],
    q: int,
    n: int,
    k: int,
    r: int,
) -> list[dict[str, Any]]:
    """Pair-level verifier using the closed-ball Pade-Hankel formulation.

    This avoids materializing the full `q^k` codeword table.  For sub-capacity
    Reed-Solomon rows (`r <= m-1`, `m=n-k`), a finite slope is sparse-MCA-bad
    exactly when some size-`r` closed-ball disagreement set `T` has

        (H_1 + gamma H_2) ell_T = 0,    H_2 ell_T != 0.

    The second condition is the same-support noncontainment gate.
    """

    m = n - k
    require(0 <= r <= m - 1, "Pade-Hankel witness path expects sub-capacity r <= n-k-1")
    require(len(eps1) == n and len(eps2) == n, "sparse pair has wrong length")
    require(sparse_union_size(eps1, eps2) <= r, "sparse pair support exceeds r")
    domain = subgroup_domain(q, n)
    weights = lagrange_weights(domain, q)
    h1 = hankel_window(syndrome(eps1, domain, weights, q, m), m, r)
    h2 = hankel_window(syndrome(eps2, domain, weights, q, m), m, r)
    locators = [
        (disagreement_set, locator_coefficients(domain, disagreement_set, q))
        for disagreement_set in itertools.combinations(range(n), r)
    ]
    shape_products = [(disagreement_set, ell, mat_vec(h1, ell, q), mat_vec(h2, ell, q)) for disagreement_set, ell in locators]

    by_gamma: dict[int, dict[str, Any]] = {}
    for disagreement_set, ell, h1_ell, h2_ell in shape_products:
        if not any(h2_ell):
            continue
        gamma = candidate_gamma_for_shape(h1_ell, h2_ell, q)
        if gamma is None or gamma in by_gamma:
            continue
        direct = direct_maximal_witness_from_disagreement(
            eps1,
            eps2,
            q,
            n,
            k,
            r,
            gamma,
            disagreement_set,
        )
        by_gamma[gamma] = {
            "gamma": gamma,
            "agreement": direct["agreement"],
            "distance": direct["distance"],
            "disagreement_set": list(disagreement_set),
            "closed_ball_witness_set": direct["closed_ball_witness_set"],
            "maximal_witness_set": direct["maximal_witness_set"],
            "codeword_coefficients": direct["codeword_coefficients"],
            "locator_coefficients": list(ell),
            "noncontainment_vector": list(h2_ell),
        }
    return [by_gamma[gamma] for gamma in sorted(by_gamma)]


def direct_maximal_witness_from_disagreement(
    eps1: tuple[int, ...],
    eps2: tuple[int, ...],
    q: int,
    n: int,
    k: int,
    r: int,
    gamma: int,
    disagreement_set: tuple[int, ...],
) -> dict[str, Any]:
    """Reconstruct the close codeword and recheck the maximal witness set.

    The Pade-Hankel check supplies a closed-ball disagreement set `T` of size
    `r`.  This routine interpolates the unique degree-`<k` codeword from
    `S=D\\T`, evaluates it on all of `D`, then checks the maximal agreement set
    `S_z={i: eps1_i+gamma eps2_i=z_i}` for same-support noncontainment.
    """

    domain = subgroup_domain(q, n)
    word = tuple((eps1[index] + gamma * eps2[index]) % q for index in range(n))
    witness_set = tuple(index for index in range(n) if index not in disagreement_set)
    require(len(witness_set) >= k, "closed-ball witness set is too small to interpolate")
    codeword_coeffs = restriction_coefficients(word, witness_set, domain, k, q)
    require(codeword_coeffs is not None, "closed-ball witness does not interpolate to a codeword")
    codeword = tuple(poly_eval(codeword_coeffs, x, q) for x in domain)
    maximal_support = tuple(index for index, (left, right) in enumerate(zip(word, codeword, strict=True)) if left == right)
    distance = n - len(maximal_support)
    require(distance <= r, "reconstructed codeword is outside the radius")
    eps2_coeffs = restriction_coefficients(eps2, maximal_support, domain, k, q)
    require(eps2_coeffs is None, "maximal witness set mutually extends")
    return {
        "gamma": gamma,
        "distance": distance,
        "agreement": len(maximal_support),
        "disagreement_set": list(disagreement_set),
        "closed_ball_witness_set": list(witness_set),
        "maximal_witness_set": list(maximal_support),
        "codeword_coefficients": list(codeword_coeffs),
    }


def verify_row(row: Row) -> dict[str, Any]:
    q, n, k, r = row.q, row.n, row.k, row.r
    require(0 < k < n, "expected 0 < k < n")
    require(0 <= r <= n - k, "this census records the sparse layer r <= n-k")
    domain = subgroup_domain(q, n)
    codewords = all_codewords(q, domain, k)
    sigma_c = -1
    max_pairs: list[dict[str, Any]] = []
    pair_count = 0
    bad_pair_count = 0

    for eps1, eps2 in enumerate_error_pairs(q, n, r):
        pair_count += 1
        require(sparse_union_size(eps1, eps2) <= r, "enumerator emitted an oversized sparse pair")
        witnesses = bad_slope_witnesses(eps1, eps2, q, r, codewords, k)
        count = len(witnesses)
        if count:
            bad_pair_count += 1
        if count > sigma_c:
            sigma_c = count
            max_pairs = [
                {
                    "eps1": list(eps1),
                    "eps2": list(eps2),
                    "bad_slope_count": count,
                    "bad_slopes": witnesses,
                }
            ]
        elif count == sigma_c and count > 0 and len(max_pairs) < 3:
            max_pairs.append(
                {
                    "eps1": list(eps1),
                    "eps2": list(eps2),
                    "bad_slope_count": count,
                    "bad_slopes": witnesses,
                }
            )

    require(sigma_c >= 0, "sigma_c was not computed")
    if row.expected_sigma_c is not None:
        require(
            sigma_c == row.expected_sigma_c,
            f"expected sigma_C={row.expected_sigma_c} for {(q, n, k, r)}, got {sigma_c}",
        )
    if 2 * r <= n - k:
        require(sigma_c == r, f"trivial-regime check sigma_C=r failed for {(q, n, k, r)}")

    return {
        "q_line": q,
        "q_gen": q,
        "q_chal": None,
        "n": n,
        "k": k,
        "rho": f"{k}/{n}",
        "r": r,
        "delta_floor_convention": "r=floor(delta*n)",
        "domain": list(domain),
        "codeword_count": len(codewords),
        "sparse_pair_count": pair_count,
        "bad_pair_count": bad_pair_count,
        "sigma_c": sigma_c,
        "expected_sigma_c": row.expected_sigma_c,
        "trivial_regime_2r_le_n_minus_k": 2 * r <= n - k,
        "max_pairs_sample": max_pairs,
    }


def total_sparse_pair_count(q: int, n: int, r: int) -> int:
    value_pairs = q * q - 1
    return sum(math.comb(n, size) * (value_pairs**size) for size in range(r + 1))


def write_scan_checkpoint(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render(payload), encoding="utf-8")


def verify_row_hankel_scan(
    row: Row,
    *,
    checkpoint: Path | None = None,
    checkpoint_interval_s: float = 600.0,
    max_pairs_to_scan: int | None = None,
    stop_at_saturation: bool = False,
) -> dict[str, Any]:
    """Enumerate sparse pairs with the Pade-Hankel witness equations.

    This is the stdlib, no-codeword-materialization scan rung.  It is intended
    for small exact rows and for partial/checkpointed long-row runs whose output
    remains explicitly EXPERIMENTAL unless the scan completes or hits finite
    slope saturation.
    """

    q, n, k, r = row.q, row.n, row.k, row.r
    require(0 < k < n, "expected 0 < k < n")
    require(0 <= r <= n - k - 1, "Hankel scan requires sub-capacity r <= n-k-1")
    domain = subgroup_domain(q, n)
    expected_pairs = total_sparse_pair_count(q, n, r)
    sigma_c = -1
    max_pair_records: list[dict[str, Any]] = []
    pair_count = 0
    bad_pair_count = 0
    completed = True
    early_stop_reason: str | None = None
    started = time.perf_counter()
    next_checkpoint = started + max(checkpoint_interval_s, 0.0)

    for eps1, eps2 in enumerate_error_pairs(q, n, r):
        pair_count += 1
        witnesses = bad_slope_witnesses_hankel(eps1, eps2, q, n, k, r)
        count = len(witnesses)
        if count:
            bad_pair_count += 1
        if count > sigma_c:
            sigma_c = count
            max_pair_records = [
                {
                    "eps1": list(eps1),
                    "eps2": list(eps2),
                    "bad_slope_count": count,
                    "bad_slopes": witnesses,
                }
            ]
        elif count == sigma_c and count > 0 and len(max_pair_records) < 3:
            max_pair_records.append(
                {
                    "eps1": list(eps1),
                    "eps2": list(eps2),
                    "bad_slope_count": count,
                    "bad_slopes": witnesses,
                }
            )

        if stop_at_saturation and sigma_c == q:
            completed = False
            early_stop_reason = "finite_slope_saturation"
            break
        if max_pairs_to_scan is not None and pair_count >= max_pairs_to_scan:
            completed = False
            early_stop_reason = "max_pairs_to_scan"
            break
        if checkpoint is not None and time.perf_counter() >= next_checkpoint:
            write_scan_checkpoint(
                checkpoint,
                {
                    "schema_version": HANKEL_SCAN_SCHEMA_VERSION,
                    "status": "EXPERIMENTAL partial checkpoint",
                    "q_line": q,
                    "q_gen": q,
                    "q_chal": None,
                    "n": n,
                    "k": k,
                    "m": n - k,
                    "r": r,
                    "pairs_scanned": pair_count,
                    "pairs_total": expected_pairs,
                    "bad_pair_count": bad_pair_count,
                    "sigma_c_lower_bound": max(sigma_c, 0),
                    "elapsed_s": round(time.perf_counter() - started, 3),
                    "codeword_materialization": False,
                    "max_pairs_sample": max_pair_records,
                },
            )
            next_checkpoint = time.perf_counter() + max(checkpoint_interval_s, 0.0)

    require(sigma_c >= 0, "sigma_c was not computed")
    if completed:
        require(pair_count == expected_pairs, "completed scan did not visit the expected sparse-pair count")
        status = "PROVED-by-enumeration via Pade-Hankel full sparse-pair scan"
        census_coverage = "full_hankel_scan"
        sigma_exact: int | None = sigma_c
        sigma_lower_bound = sigma_c
    elif early_stop_reason == "finite_slope_saturation":
        status = "PROVED exact by finite-slope saturation during Pade-Hankel scan"
        census_coverage = "exact_by_finite_slope_saturation"
        sigma_exact = q
        sigma_lower_bound = q
    else:
        status = "EXPERIMENTAL partial Pade-Hankel sparse-pair scan"
        census_coverage = "partial_hankel_scan"
        sigma_exact = None
        sigma_lower_bound = sigma_c

    if row.expected_sigma_c is not None and sigma_exact is not None:
        require(
            sigma_exact == row.expected_sigma_c,
            f"expected sigma_C={row.expected_sigma_c} for {(q, n, k, r)}, got {sigma_exact}",
        )

    return {
        "q_line": q,
        "q_gen": q,
        "q_chal": None,
        "n": n,
        "k": k,
        "m": n - k,
        "rho": f"{k}/{n}",
        "r": r,
        "delta_floor_convention": "r=floor(delta*n)",
        "domain": list(domain),
        "codeword_materialization": False,
        "pairs_scanned": pair_count,
        "pairs_total": expected_pairs,
        "bad_pair_count": bad_pair_count,
        "sigma_c": sigma_exact,
        "sigma_c_lower_bound": sigma_lower_bound,
        "expected_sigma_c": row.expected_sigma_c,
        "census_coverage": census_coverage,
        "early_stop_reason": early_stop_reason,
        "elapsed_s": round(time.perf_counter() - started, 3),
        "max_pairs_sample": max_pair_records,
    }


def build_certificate(rows: Iterable[Row]) -> dict[str, Any]:
    checked_rows = [verify_row(row) for row in rows]
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "EXPERIMENTAL / PROVED-by-enumeration for the finite rows listed",
        "theorem_or_problem_id": "towards-prize prob:mutual; thm:sparsify sparse mutual layer",
        "object": "sigma_C(r)=max sparse-pair count of finite MCA-bad slopes",
        "conventions": {
            "finite_slopes_only": True,
            "slope_denominator": "q_line",
            "witness_set": "maximal S_z={i: eps1_i + gamma eps2_i equals close codeword z_i}",
            "symmetry_policy": "no symmetry quotient is used here; optimized searches must not use full Mobius reductions because they can send finite slopes to infinity",
            "field_ledger": "toy prime-field rows use q_gen=q_line; no q_chal soundness division is claimed",
        },
        "rows": checked_rows,
        "non_claims": [
            "No asymptotic bound is claimed.",
            "No prize-band deployed-row claim is made.",
            "No GPU search result is included in this certificate.",
        ],
    }


def build_hankel_scan_certificate(
    rows: Iterable[Row],
    *,
    checkpoint: Path | None = None,
    checkpoint_interval_s: float = 600.0,
    max_pairs_to_scan: int | None = None,
    stop_at_saturation: bool = False,
) -> dict[str, Any]:
    checked_rows = [
        verify_row_hankel_scan(
            row,
            checkpoint=checkpoint,
            checkpoint_interval_s=checkpoint_interval_s,
            max_pairs_to_scan=max_pairs_to_scan,
            stop_at_saturation=stop_at_saturation,
        )
        for row in rows
    ]
    return {
        "schema_version": HANKEL_SCAN_SCHEMA_VERSION,
        "status": "AUDIT / Pade-Hankel sparse-pair scan certificate",
        "theorem_or_problem_id": "towards-prize prob:mutual; thm:sparsify sparse mutual layer",
        "object": "sigma_C(r)=max sparse-pair count of finite MCA-bad slopes",
        "conventions": {
            "finite_slopes_only": True,
            "slope_denominator": "q_line",
            "delta_floor": "r=floor(delta*n)",
            "witness_set": "Pade-Hankel closed-ball shape T, followed by exact maximal S_z reconstruction",
            "symmetry_policy": "no Mobius/projective quotient",
            "field_ledger": "toy prime-field rows use q_gen=q_line; no q_chal soundness division is claimed",
        },
        "rows": checked_rows,
        "non_claims": [
            "Partial scans are EXPERIMENTAL lower bounds unless finite-slope saturation is reached.",
            "No deployed/prize-band row is claimed.",
            "The stdlib scan path is a correctness rung, not the optimized GPU implementation.",
        ],
    }


def require_v2_row_common(row: dict[str, Any]) -> tuple[int, int, int, int]:
    q = int(row["q_line"])
    require(int(row["q_gen"]) == q, "v2 toy rows expect q_gen=q_line")
    require(row.get("q_chal") is None, "v2 toy rows do not use q_chal")
    n = int(row["n"])
    k = int(row["k"])
    r = int(row["r"])
    require(0 < k < n, "expected 0 < k < n")
    require(0 <= r <= n - k - 1, "v2 rows are sub-capacity")
    require(row.get("m") == n - k, "bad m=n-k field")
    require(row.get("delta_floor_convention") == "r=floor(delta*n)", "missing endpoint convention")
    return q, n, k, r


def check_v2_trivial_row(row: dict[str, Any]) -> dict[str, Any]:
    q, n, k, r = require_v2_row_common(row)
    m = n - k
    require(row.get("exact_path") == "trivial-regime-theorem", "bad trivial exact_path")
    require(2 * r <= m, "trivial row must satisfy 2r <= n-k")
    require(row.get("sigma_c") == r, "trivial row must record sigma_C=r")
    require(row.get("saturates") is False, "trivial row should not saturate q")
    require(row.get("census_coverage") == "theorem_guard", "bad trivial census_coverage")
    require(row.get("pairs_total") is None, "trivial theorem row should not claim pair enumeration")
    return {"row": f"q{q}_n{n}_k{k}_r{r}", "status": "EXACT_TRIVIAL_PASS", "sigma_c": r}


def check_v2_pair_row(row: dict[str, Any]) -> dict[str, Any]:
    q, n, k, r = require_v2_row_common(row)
    exact_path = row.get("exact_path")
    require(
        exact_path in {"pade-hankel-saturation-witness", "pade-hankel-lower-bound-witness"},
        "bad pair exact_path",
    )
    pair = row["witness_pair"]
    eps1 = tuple(int(value) for value in pair["eps1"])
    eps2 = tuple(int(value) for value in pair["eps2"])
    witnesses = bad_slope_witnesses_hankel(eps1, eps2, q, n, k, r)
    gammas = [int(witness["gamma"]) for witness in witnesses]
    recorded = [int(witness["gamma"]) for witness in pair["bad_slopes"]]
    require(gammas == recorded, f"bad slope list mismatch for {(q, n, k, r)}: {gammas} != {recorded}")
    require(pair["bad_slopes"] == witnesses, f"bad slope witness records mismatch for {(q, n, k, r)}")
    if exact_path == "pade-hankel-saturation-witness":
        require(gammas == list(range(q)), f"saturation row did not cover all finite slopes: {gammas}")
        require(row.get("sigma_c") == q, "saturation row must record sigma_C=q")
        require(row.get("saturates") is True, "saturation row must set saturates=true")
        require(row.get("census_coverage") == "exact_by_finite_slope_saturation", "bad saturation coverage")
        status = "EXACT_SATURATION_PASS"
        sigma = q
    else:
        require(row.get("sigma_c") is None, "lower-bound rows must not record an exact sigma_C")
        require(row.get("saturates") is False, "lower-bound rows must not set saturates=true")
        require(row.get("census_coverage") == "partial_lower_bound_witness", "bad lower-bound coverage")
        require(row.get("sigma_c_lower_bound") == len(gammas), "bad lower-bound count")
        status = "LOWER_BOUND_WITNESS_PASS"
        sigma = len(gammas)
    require(pair.get("bad_slope_count") == len(gammas), "bad_slope_count mismatch")
    require(row.get("single_exact_path") is True, "v2 pair rows should disclose single exact path")
    require(row.get("pairs_total") is None, "v2 witness rows should not claim pair enumeration")
    return {"row": f"q{q}_n{n}_k{k}_r{r}", "status": status, "count": sigma}


def check_v2_certificate(certificate: dict[str, Any]) -> list[dict[str, Any]]:
    require(certificate.get("schema_version") == SCHEMA_VERSION_V2, "not a v2 sigma_C certificate")
    require(certificate.get("status"), "missing status")
    require(certificate.get("family_signals") is not None, "missing family_signals")
    require(certificate.get("conventions", {}).get("finite_slopes_only") is True, "missing finite-slope convention")
    checked: list[dict[str, Any]] = []
    for row in certificate["rows"]:
        if row.get("exact_path") == "trivial-regime-theorem":
            checked.append(check_v2_trivial_row(row))
        else:
            checked.append(check_v2_pair_row(row))
    return checked


def check_hankel_scan_certificate(certificate: dict[str, Any]) -> list[dict[str, Any]]:
    require(certificate.get("schema_version") == HANKEL_SCAN_SCHEMA_VERSION, "not a Hankel scan certificate")
    require(certificate.get("status"), "missing status")
    require(certificate.get("conventions", {}).get("finite_slopes_only") is True, "missing finite-slope convention")
    checked: list[dict[str, Any]] = []
    for row in certificate["rows"]:
        q = int(row["q_line"])
        require(int(row["q_gen"]) == q, "Hankel scan rows expect q_gen=q_line")
        require(row.get("q_chal") is None, "Hankel scan rows do not use q_chal")
        n = int(row["n"])
        k = int(row["k"])
        r = int(row["r"])
        require(row.get("m") == n - k, "bad m=n-k field")
        require(row.get("delta_floor_convention") == "r=floor(delta*n)", "missing endpoint convention")
        require(row.get("codeword_materialization") is False, "Hankel scan must not materialize codewords")
        expected_pairs = total_sparse_pair_count(q, n, r)
        require(row.get("pairs_total") == expected_pairs, "bad pairs_total")
        pairs_scanned = int(row["pairs_scanned"])
        require(0 < pairs_scanned <= expected_pairs, "bad pairs_scanned")
        coverage = row.get("census_coverage")
        sigma = row.get("sigma_c")
        sigma_lower = int(row["sigma_c_lower_bound"])
        if coverage == "full_hankel_scan":
            require(pairs_scanned == expected_pairs, "full scan must cover every sparse pair")
            require(row.get("early_stop_reason") is None, "full scan cannot have early_stop_reason")
            require(sigma == sigma_lower, "full scan must record exact sigma_C")
        elif coverage == "exact_by_finite_slope_saturation":
            require(row.get("early_stop_reason") == "finite_slope_saturation", "bad saturation stop reason")
            require(sigma == q and sigma_lower == q, "saturation scan must record sigma_C=q_line")
        elif coverage == "partial_hankel_scan":
            require(sigma is None, "partial scan must not record exact sigma_C")
            require(pairs_scanned < expected_pairs, "partial scan should not claim full coverage")
        else:
            raise AssertionError(f"bad census_coverage: {coverage}")
        for pair in row.get("max_pairs_sample", []):
            eps1 = tuple(int(value) for value in pair["eps1"])
            eps2 = tuple(int(value) for value in pair["eps2"])
            witnesses = bad_slope_witnesses_hankel(eps1, eps2, q, n, k, r)
            require(pair.get("bad_slope_count") == len(witnesses), "bad_slope_count mismatch")
            require(pair.get("bad_slopes") == witnesses, "bad slope witness records mismatch")
        checked.append(
            {
                "row": f"q{q}_n{n}_k{k}_r{r}",
                "status": str(coverage).upper(),
                "pairs_scanned": pairs_scanned,
                "pairs_total": expected_pairs,
            }
        )
    return checked


def rows_from_args(args: argparse.Namespace) -> list[Row]:
    if not args.row:
        return [Row(**row) for row in DEFAULT_ROWS]
    rows: list[Row] = []
    for spec in args.row:
        # PowerShell passes an unquoted comma-separated native argument as a
        # single whitespace-separated string, so accept both shell spellings.
        parts = [int(part) for part in spec.replace(",", " ").split()]
        require(len(parts) in {4, 5}, "--row expects q,n,k,r[,expected_sigma_c]")
        expected = parts[4] if len(parts) == 5 else None
        rows.append(Row(parts[0], parts[1], parts[2], parts[3], expected))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--row", action="append", help="row q,n,k,r[,expected_sigma_c]; may be repeated")
    parser.add_argument(
        "--verify-mode",
        choices=("full-cpu", "witness-sample", "extremal-only"),
        default="full-cpu",
        help="full-cpu regenerates v1 rows; extremal-only checks v2 theorem/witness rows",
    )
    parser.add_argument("--write", type=Path, help="write certificate JSON")
    parser.add_argument("--check", type=Path, help="check certificate JSON exactly")
    parser.add_argument("--checkpoint", type=Path, help="write periodic Hankel-scan checkpoint JSON")
    parser.add_argument("--checkpoint-interval-s", type=float, default=600.0)
    parser.add_argument("--max-pairs-to-scan", type=int, help="stop a Hankel scan after this many sparse pairs")
    parser.add_argument("--stop-at-saturation", action="store_true", help="stop Hankel scan once sigma_C reaches q_line")
    args = parser.parse_args()

    if args.check:
        expected = json.loads(args.check.read_text(encoding="utf-8"))
        if expected.get("schema_version") == SCHEMA_VERSION_V2:
            checked_rows = check_v2_certificate(expected)
            print("sigma_C sparse census verifier")
            print("  object: sparse support-wise MCA bad-slope count")
            print("  theorem/problem: towards-prize prob:mutual / thm:sparsify")
            print("  status: AUDIT; v2 rows exact by theorem guards or Pade-Hankel witnesses")
            print("  conventions: finite slopes only; sub-capacity closed-ball witnesses; no Mobius quotient")
            for checked in checked_rows:
                print(f"  row {checked['row']}: {checked['status']}")
            print("RESULT: PASS")
            return 0
        if expected.get("schema_version") == HANKEL_SCAN_SCHEMA_VERSION:
            checked_rows = check_hankel_scan_certificate(expected)
            print("sigma_C sparse census verifier")
            print("  object: sparse support-wise MCA bad-slope count")
            print("  theorem/problem: towards-prize prob:mutual / thm:sparsify")
            print("  status: AUDIT; Hankel scan artifact invariants replayed")
            print("  conventions: finite slopes only; Pade-Hankel closed-ball shapes; no codeword table")
            for checked in checked_rows:
                print(
                    "  row {row}: {status} pairs_scanned={pairs_scanned}/{pairs_total}".format(
                        **checked
                    )
                )
            print("RESULT: PASS")
            return 0

    if args.verify_mode == "witness-sample" and not args.check:
        certificate = build_hankel_scan_certificate(
            rows_from_args(args),
            checkpoint=args.checkpoint,
            checkpoint_interval_s=args.checkpoint_interval_s,
            max_pairs_to_scan=args.max_pairs_to_scan,
            stop_at_saturation=args.stop_at_saturation,
        )
    else:
        certificate = build_certificate(rows_from_args(args))
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(render(certificate), encoding="utf-8")
    if args.check:
        expected = json.loads(args.check.read_text(encoding="utf-8"))
        require(certificate == expected, f"sigma_C sparse census mismatch: {args.check}")

    print("sigma_C sparse census verifier")
    print("  object: sparse support-wise MCA bad-slope count")
    print("  theorem/problem: towards-prize prob:mutual / thm:sparsify")
    if certificate["schema_version"] == HANKEL_SCAN_SCHEMA_VERSION:
        print("  status: AUDIT; Hankel scan rows report PROVED or EXPERIMENTAL coverage per row")
        print("  conventions: finite slopes only; Pade-Hankel closed-ball shapes; no codeword table")
    else:
        print("  status: AUDIT; finite rows PROVED-by-enumeration")
        print("  conventions: finite slopes only; maximal S_z failure check; no Mobius quotient")
    for row in certificate["rows"]:
        if certificate["schema_version"] == HANKEL_SCAN_SCHEMA_VERSION:
            print(
                "  row q={q_line} n={n} k={k} r={r}: sigma_C={sigma_c} "
                "lower_bound={sigma_c_lower_bound} pairs_scanned={pairs_scanned}/{pairs_total} "
                "coverage={census_coverage}".format(**row)
            )
        else:
            print(
                "  row q={q_line} n={n} k={k} r={r}: sigma_C={sigma_c} "
                "pairs={sparse_pair_count} bad_pairs={bad_pair_count}".format(**row)
            )
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
