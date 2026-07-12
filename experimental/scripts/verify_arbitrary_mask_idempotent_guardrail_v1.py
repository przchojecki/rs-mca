#!/usr/bin/env python3
"""Finite regression for the abstract owner-rooted idempotent-mask guardrail.

This checks dense scalar-orbit Fourier amplification and prints why the finite
state is not a source-semantic witness. It does not falsify weighted-
Vandermonde, tau-band, or one-received-line primitive signed-payment boundary.
"""

from __future__ import annotations

import argparse
import cmath
import itertools
import math


# The original deterministic 40-sample search selected this witness. Keeping
# the winning orbit indices makes ordinary certificate replay substantially
# faster while preserving the exact regression state.
WITNESS_ORBIT_INDICES = (
    2, 6, 9, 10, 12, 16, 18, 19, 20, 21, 23, 24, 26, 28, 32, 35, 36, 38,
    40, 42, 43, 44, 45, 46, 49, 52, 53, 54, 58, 59, 62, 64, 65, 66, 69, 70,
    71, 73, 75, 76, 78, 79, 83, 84, 86, 89, 90, 92, 95, 96, 98, 100, 101,
    105, 109, 110, 111, 112, 113, 116, 117, 118, 119, 121, 125, 126, 130,
    131, 132, 133, 134, 135, 136, 138, 139, 142, 144, 147, 148, 149, 152,
    155, 157, 159, 161, 162, 165, 168, 169, 170, 172, 174, 175, 179, 184,
    187, 188, 194, 199, 200, 201, 202, 203, 206, 209, 213, 217, 219, 222,
    223, 226, 228, 229, 231, 232, 233, 234, 235, 236, 238, 239, 242, 243,
    245, 252, 254, 255, 256, 257, 260, 263, 265, 266, 268, 270, 272, 275,
    276, 279, 280, 283, 285, 287, 288, 289, 291, 292, 294, 296, 297, 299,
    300, 301, 305, 308, 312, 313, 314, 315, 317, 318, 321, 324, 328, 330,
    332, 334, 336, 338, 340, 342, 343, 347, 349, 351, 352, 353, 355, 356,
    357, 358, 362,
)


def dot(x: tuple[int, ...], y: tuple[int, ...], p: int) -> int:
    return sum(a * b for a, b in zip(x, y)) % p


def add(x: tuple[int, ...], y: tuple[int, ...], p: int) -> tuple[int, ...]:
    return tuple((a + b) % p for a, b in zip(x, y))


def neg(x: tuple[int, ...], p: int) -> tuple[int, ...]:
    return tuple((-a) % p for a in x)


def scalar(c: int, x: tuple[int, ...], p: int) -> tuple[int, ...]:
    return tuple(c * a % p for a in x)


def character(xi: tuple[int, ...], x: tuple[int, ...], p: int) -> complex:
    return cmath.exp(2j * math.pi * dot(xi, x, p) / p)


def scalar_orbits(
    group: list[tuple[int, ...]], p: int
) -> list[frozenset[tuple[int, ...]]]:
    unseen = set(group)
    unseen.remove(tuple(0 for _ in group[0]))
    result: list[frozenset[tuple[int, ...]]] = []
    while unseen:
        root = min(unseen)
        orbit = frozenset(scalar(c, root, p) for c in range(1, p))
        result.append(orbit)
        unseen -= orbit
    return result


def kernel(
    group: list[tuple[int, ...]],
    band: set[tuple[int, ...]],
    p: int,
) -> dict[tuple[int, ...], complex]:
    order = len(group)
    return {
        x: sum(character(xi, x, p) for xi in band) / order
        for x in group
    }


def convolution(
    group: list[tuple[int, ...]],
    k: dict[tuple[int, ...], complex],
    values: dict[tuple[int, ...], float],
    p: int,
) -> dict[tuple[int, ...], complex]:
    return {
        x: sum(k[add(x, neg(y, p), p)] * values[y] for y in group)
        for x in group
    }


def dyadic_label(value: float) -> str:
    if value < 1.0:
        return "<1"
    return str(math.floor(math.log2(value)))


def is_weighted_moment_column(column: tuple[int, ...], p: int) -> bool:
    rho = column[0] % p
    if rho == 0:
        return False
    t = column[1] * pow(rho, p - 2, p) % p
    return all(column[j] % p == rho * pow(t, j, p) % p for j in range(len(column)))


def collinear(words: list[tuple[int, ...]], p: int) -> bool:
    base = words[0]
    d1 = tuple((a - b) % p for a, b in zip(words[1], base))
    d2 = tuple((a - b) % p for a, b in zip(words[2], base))
    return any(d2 == scalar(c, d1, p) for c in range(p))


def run() -> dict[str, object]:
    p = 3
    rank = 6
    group = list(itertools.product(range(p), repeat=rank))
    orbits = scalar_orbits(group, p)
    chosen = [orbits[index] for index in WITNESS_ORBIT_INDICES]
    best_band = set().union(*chosen)
    best_kernel = kernel(group, best_band, p)
    best_l1 = sum(abs(value) for value in best_kernel.values())

    zero = (0,) * rank
    sign_mask = {
        y: 1.0 if best_kernel[neg(y, p)].real >= 0 else 0.0 for y in group
    }
    projected = convolution(group, best_kernel, sign_mask, p)
    q = 4
    q_norm = sum(abs(value) ** q for value in projected.values()) ** (1 / q)
    point_identity_error = abs(projected[zero].real - best_l1 / 2)
    abstract_gain = q_norm / len(group) ** (1 / q)

    columns = [group[index] for index in (1, 5, 11, 19, 28, 37, 53, 68)]
    tau_labels = set()
    for xi in best_band:
        tau = sum(character(xi, column, p) for column in columns)
        tau_labels.add(dyadic_label(abs(tau)))
    moment_violations = sum(not is_weighted_moment_column(column, p) for column in columns)

    owner_words = [
        (1, 0, 0, 0, 0, 0),
        (0, 1, 0, 0, 0, 0),
        (0, 0, 1, 0, 0, 0),
    ]
    owner_collinear = collinear(owner_words, 7)

    checks = {
        "dense_band": 0.35 <= len(best_band) / len(group) <= 0.65,
        "scalar_complete_and_symmetric": all(
            scalar(c, xi, p) in best_band
            for xi in best_band
            for c in range(1, p)
        ),
        "large_kernel_l1": best_l1 >= 0.30 * math.sqrt(len(group)),
        "kernel_sign_identity": point_identity_error <= 1e-9,
        "q_greater_than_2_gain": abstract_gain > 1.0,
        "not_one_tau_band": len(tau_labels) >= 2,
        "not_weighted_vandermonde": moment_violations >= 1,
        "owner_words_not_one_affine_line": not owner_collinear,
    }
    assert all(checks.values()), checks
    return {
        "group": f"F_{p}^{rank}",
        "group_order": len(group),
        "scalar_orbits": len(orbits),
        "band_size": len(best_band),
        "band_density": len(best_band) / len(group),
        "kernel_l1": best_l1,
        "kernel_l1_over_sqrt_group": best_l1 / math.sqrt(len(group)),
        "q": q,
        "normalized_q_gain": abstract_gain,
        "tau_band_labels_met": sorted(tau_labels),
        "weighted_vandermonde_violations": moment_violations,
        "owner_words_collinear": owner_collinear,
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="run the regression")
    parser.parse_args()
    result = run()
    print("ABSTRACT IDEMPOTENT-MASK GUARDRAIL")
    for key, value in result.items():
        print(f"{key:38s} = {value}")
    print("RESULT = PASS")


if __name__ == "__main__":
    main()
