#!/usr/bin/env python3
"""Deterministic point-mask and secant guardrails for the owner-rooted audit.

The point-mass check concerns a hereditary source-fiber submask. The secant
check rules out automatic coordinate folding and proper-field descent; neither
regression certifies the signed nonstructure payment or a semantic atlas cell.
"""

from __future__ import annotations

import argparse
import cmath
import math
from collections import defaultdict
from itertools import combinations


def dft(f: list[complex]) -> list[complex]:
    h = len(f)
    return [
        sum(f[x] * cmath.exp(-2j * math.pi * k * x / h) for x in range(h))
        for k in range(h)
    ]


def project_band(f: list[complex], band: list[int]) -> list[complex]:
    h = len(f)
    fh = dft(f)
    return [
        sum(fh[k] * cmath.exp(2j * math.pi * k * x / h) for k in band) / h
        for x in range(h)
    ]


def lq_norm(v: list[complex], q: int) -> float:
    return sum(abs(z) ** q for z in v) ** (1.0 / q)


def norming_dual(hv: list[complex], q: int) -> list[complex]:
    norm = lq_norm(hv, q)
    if norm == 0:
        raise AssertionError("zero projected function")
    return [
        (abs(z) ** (q - 2) * z / norm ** (q - 1)) if z else 0j
        for z in hv
    ]


def make_tau_bands(columns: list[int], h: int) -> dict[str, list[int]]:
    n = len(columns)
    bands: dict[str, list[int]] = defaultdict(list)
    for k in range(1, h):
        tau = sum(cmath.exp(2j * math.pi * k * v / h) for v in columns)
        mag = abs(tau)
        if mag < 1.0:
            key = "<1"
        else:
            j = int(math.floor(math.log(mag, 2)))
            key = f"{j}"
        bands[key].append(k)
    assert len(bands) <= 2 + math.ceil(math.log2(n))
    assert sum(map(len, bands.values())) == h - 1
    return dict(bands)


def check_point_mass_reduction() -> dict[str, float | int | str]:
    h = 17
    n = 12
    q = 8
    columns = [0, 1, 1, 2, 3, 5, 7, 8, 10, 11, 13, 16]
    bands = make_tau_bands(columns, h)
    band_name, band = max(bands.items(), key=lambda kv: len(kv[1]))

    s0 = 6
    w = 137
    f = [0j] * h
    f[s0] = complex(w)

    pf = project_band(f, band)
    delta = len(band) / h
    expected = w * delta
    assert abs(pf[s0].real - expected) < 1e-10
    assert abs(pf[s0].imag) < 1e-10

    norm = lq_norm(pf, q)
    assert norm + 1e-12 >= expected

    g = norming_dual(pf, q)
    qprime = q / (q - 1)
    dual_norm = sum(abs(z) ** qprime for z in g) ** (1.0 / qprime)
    assert abs(dual_norm - 1.0) < 1e-10

    pag = project_band(g, band)
    root_weight = pag[s0].conjugate().real
    assert root_weight > 0
    assert abs(w * root_weight - norm) < 1e-9

    return {
        "group_order": h,
        "coordinate_count": n,
        "band_count": len(bands),
        "selected_band": band_name,
        "selected_band_size": len(band),
        "band_density": delta,
        "point_value": pf[s0].real,
        "q_norm": norm,
        "dual_norm": dual_norm,
        "root_weight": root_weight,
        "rooted_mass": w * root_weight,
    }


def vec(t: int, p: int = 7) -> tuple[int, int, int]:
    return (t % p, t * t % p, t * t * t % p)


def add_vec(a: tuple[int, ...], b: tuple[int, ...], p: int) -> tuple[int, ...]:
    return tuple((x + y) % p for x, y in zip(a, b))


def sub_vec(a: tuple[int, ...], b: tuple[int, ...], p: int) -> tuple[int, ...]:
    return tuple((x - y) % p for x, y in zip(a, b))


def smul(c: int, a: tuple[int, ...], p: int) -> tuple[int, ...]:
    return tuple(c * x % p for x in a)


def check_secant_no_folding() -> dict[str, object]:
    p = 7
    s0 = add_vec(vec(0), vec(1), p)
    s1 = add_vec(vec(2), vec(3), p)
    u = sub_vec(s0, s1, p)
    assert u == (3, 2, 1)

    collisions: list[tuple[int, int, int]] = []
    for x, y in combinations(range(p), 2):
        diff = sub_vec(vec(x), vec(y), p)
        for c in range(p):
            if diff == smul(c, u, p):
                collisions.append((x, y, c))
    assert collisions == []

    # The annihilator of one nonzero vector in F_p^3 has p^2 elements.
    annihilator = []
    for a in range(p):
        for b in range(p):
            for c in range(p):
                if (a * u[0] + b * u[1] + c * u[2]) % p == 0:
                    annihilator.append((a, b, c))
    assert len(annihilator) == p * p

    return {
        "field": "F_7",
        "root_support_0": [0, 1],
        "root_support_1": [2, 3],
        "rooted_secant": list(u),
        "annihilator_size": len(annihilator),
        "column_collisions_mod_secant": len(collisions),
        "proper_subfields": 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="run the regression")
    parser.parse_args()

    point = check_point_mass_reduction()
    secant = check_secant_no_folding()
    print("POINT-MASS REDUCTION")
    for key, value in point.items():
        print(f"{key:34s} = {value}")
    print()
    print("SECANT-TO-FOLDING GUARDRAIL")
    for key, value in secant.items():
        print(f"{key:34s} = {value}")
    print()
    print("RESULT = PASS")


if __name__ == "__main__":
    main()
