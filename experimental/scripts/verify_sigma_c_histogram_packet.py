#!/usr/bin/env python3
"""Check internal consistency of the sigma_C histogram packet.

This verifier is intentionally not a from-scratch rescan of the large rows.
It checks the recorded histogram arithmetic and replays the recorded extremal
witness pairs with exact integer arithmetic. The scan-wide histogram maxima
come from the offline full sparse-pair scan recorded in the packet.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PACKET = (
    REPO_ROOT
    / "experimental"
    / "data"
    / "certificates"
    / "sigma-c-sparse-census"
    / "sigma_c_sparse_census_gpu_histograms_k2_rows.json"
)
SCHEMA_VERSION = "sigma-c-sparse-census-hankel-scan-v1"


def render(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


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
        left_value = left[index] if index < len(left) else 0
        right_value = right[index] if index < len(right) else 0
        out[index] = (left_value + right_value) % q
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
    domain = subgroup_domain(q, n)
    word = tuple((eps1[index] + gamma * eps2[index]) % q for index in range(n))
    witness_set = tuple(index for index in range(n) if index not in disagreement_set)
    require(len(witness_set) >= k, "closed-ball witness set is too small")
    codeword_coeffs = restriction_coefficients(word, witness_set, domain, k, q)
    require(codeword_coeffs is not None, "closed-ball witness does not interpolate")
    codeword = tuple(poly_eval(codeword_coeffs, x, q) for x in domain)
    maximal_support = tuple(index for index, pair in enumerate(zip(word, codeword, strict=True)) if pair[0] == pair[1])
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


def bad_slope_witnesses_hankel(
    eps1: tuple[int, ...],
    eps2: tuple[int, ...],
    q: int,
    n: int,
    k: int,
    r: int,
) -> list[dict[str, Any]]:
    m = n - k
    require(0 <= r <= m - 1, "Pade-Hankel path expects sub-capacity r <= n-k-1")
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
    shape_products = [
        (disagreement_set, ell, mat_vec(h1, ell, q), mat_vec(h2, ell, q))
        for disagreement_set, ell in locators
    ]

    by_gamma: dict[int, dict[str, Any]] = {}
    for disagreement_set, ell, h1_ell, h2_ell in shape_products:
        if not any(h2_ell):
            continue
        gamma = candidate_gamma_for_shape(h1_ell, h2_ell, q)
        if gamma is None or gamma in by_gamma:
            continue
        direct = direct_maximal_witness_from_disagreement(eps1, eps2, q, n, k, r, gamma, disagreement_set)
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


def total_sparse_pair_count(q: int, n: int, r: int) -> int:
    value_pairs = q * q - 1
    return sum(math.comb(n, size) * (value_pairs**size) for size in range(r + 1))


def check_payload(payload: dict[str, Any]) -> list[dict[str, Any]]:
    require(payload.get("schema_version") == SCHEMA_VERSION, "unexpected schema_version")
    require(payload.get("conventions", {}).get("finite_slopes_only") is True, "missing finite-slope convention")
    if "payload_sha256" in payload:
        expected = payload["payload_sha256"]
        actual = sha256_text(render({key: value for key, value in payload.items() if key != "payload_sha256"}))
        require(actual == expected, "payload_sha256 mismatch")

    checked: list[dict[str, Any]] = []
    for row in payload.get("rows", []):
        q = int(row["q_line"])
        n = int(row["n"])
        k = int(row["k"])
        r = int(row["r"])
        require(row.get("q_gen") == q, "q_gen must equal q_line for this packet")
        require(row.get("q_chal") is None, "q_chal must be unused for this packet")
        require(row.get("m") == n - k, "bad m=n-k field")
        require(row.get("census_coverage") == "full_hankel_scan", "this checker expects full Hankel rows")
        pairs_total = total_sparse_pair_count(q, n, r)
        require(row.get("pairs_total") == pairs_total, "bad pairs_total")
        require(row.get("pairs_scanned") == pairs_total, "pairs_scanned must equal pairs_total")

        histogram = {int(key): int(value) for key, value in row.get("bad_slope_count_histogram", {}).items()}
        require(sum(histogram.values()) == pairs_total, "histogram bins do not sum to pairs_total")
        bad_pair_count = sum(value for key, value in histogram.items() if key > 0)
        require(row.get("bad_pair_count") == bad_pair_count, "bad_pair_count does not match histogram")
        max_nonzero = max((key for key, value in histogram.items() if value > 0), default=0)
        require(row.get("sigma_c") == max_nonzero, "sigma_c does not match histogram maximum")

        for pair in row.get("max_pairs_sample", []):
            eps1 = tuple(int(value) for value in pair["eps1"])
            eps2 = tuple(int(value) for value in pair["eps2"])
            witnesses = bad_slope_witnesses_hankel(eps1, eps2, q, n, k, r)
            require(pair.get("bad_slope_count") == len(witnesses), "bad_slope_count mismatch")
            require(pair.get("bad_slopes") == witnesses, "recorded bad slope witnesses mismatch")

        checked.append(
            {
                "row": f"q{q}_n{n}_k{k}_r{r}",
                "sigma_c": int(row["sigma_c"]),
                "pairs_total": pairs_total,
                "max_pairs_replayed": len(row.get("max_pairs_sample", [])),
            }
        )
    require(checked, "no rows checked")
    return checked


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path, default=DEFAULT_PACKET, help="histogram packet JSON to check")
    args = parser.parse_args()

    payload = json.loads(args.check.read_text(encoding="utf-8"))
    checked_rows = check_payload(payload)
    print("sigma_C histogram packet verifier")
    print("  object: recorded sparse-pair bad-slope histogram packet")
    print("  theorem/problem: towards-prize prob:mutual / thm:sparsify")
    print("  status: AUDIT; internal histogram consistency and exact recorded witness replay")
    print("  scope: not a from-scratch rescan of the large offline GPU rows")
    for row in checked_rows:
        print(
            f"  row {row['row']}: sigma_C={row['sigma_c']} "
            f"pairs_total={row['pairs_total']} witnesses_replayed={row['max_pairs_replayed']}"
        )
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
