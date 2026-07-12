#!/usr/bin/env python3
"""Finite regression for flat rooted secant-annihilator localization.

This checks the exact finite identities used in the flat rooted source inverse proof:
  * decomposition by restrictions to K=<u>;
  * one symmetric <=6-coset packet simultaneously retains q-norm,
    Fourier energy, and character cardinality;
  * the subgroup spectral projector is contractive and recovers the
    q-heavy restriction class from the combined packet;
  * the resulting Y ratio is at least d^(-(q-1));
  * the paired singleton-image family emits a fixed-radius rooted trade layer
    with the stated support/mass pigeonhole bounds.

The cyclic annihilator is universal for a nonzero secant; this checker does
not certify a semantic quotient cell or its slope payment. It is a
deterministic numerical regression, not a proof assistant.
Only the Python standard library is used.
"""
from __future__ import annotations

import argparse
import cmath
import itertools
import json
import math
import random
from dataclasses import asdict, dataclass

TOL = 2e-8


def dft(x: list[complex]) -> list[complex]:
    n = len(x)
    return [
        sum(x[t] * cmath.exp(-2j * math.pi * k * t / n) for t in range(n))
        for k in range(n)
    ]


def idft(xhat: list[complex]) -> list[complex]:
    n = len(xhat)
    return [
        sum(xhat[k] * cmath.exp(2j * math.pi * k * t / n) for k in range(n)) / n
        for t in range(n)
    ]


def lp(x: list[complex], q: int) -> float:
    return sum(abs(v) ** q for v in x) ** (1.0 / q)


def cyclic_order(u: int, h: int) -> int:
    return h // math.gcd(u % h, h)


def restriction_key(k: int, u: int, h: int) -> int:
    # gamma_k(j*u)=exp(2*pi*i*j*(k*u)/h), so k*u mod h labels gamma_k|_<u>.
    return (k * u) % h


def projection(fhat: list[complex], packet: set[int]) -> list[complex]:
    return idft([value if k in packet else 0j for k, value in enumerate(fhat)])


def energy(fhat: list[complex], packet: set[int]) -> float:
    h = len(fhat)
    return sum(abs(fhat[k]) ** 2 for k in packet) / h


def subgroup_projector(values: list[complex], u: int, key: int) -> list[complex]:
    """Q_chi h(s)=d^-1 sum_j conjugate(chi(j*u)) h(s+j*u)."""
    h = len(values)
    d = cyclic_order(u, h)
    out: list[complex] = []
    for s in range(h):
        total = 0j
        for j in range(d):
            phase = cmath.exp(-2j * math.pi * key * j / h)
            total += phase * values[(s + j * u) % h]
        out.append(total / d)
    return out


def max_abs_diff(x: list[complex], y: list[complex]) -> float:
    return max((abs(a - b) for a, b in zip(x, y)), default=0.0)


@dataclass
class TrialSummary:
    h: int
    q: int
    u: int
    d: int
    band_size: int
    packet_size: int
    packet_cosets: int
    q_ratio_scaled: float
    energy_ratio_scaled: float
    size_ratio_scaled: float
    y_ratio_scaled: float
    projector_error: float
    contraction_slack: float


def combined_localization_trial(
    b: list[float], a_band: set[int], q: int, u: int
) -> TrialSummary:
    h = len(b)
    assert a_band and 0 not in a_band
    assert all((-k) % h in a_band for k in a_band)
    assert u % h != 0

    bhat = dft([complex(v) for v in b])
    d = cyclic_order(u, h)
    bins: dict[int, set[int]] = {}
    for k in a_band:
        bins.setdefault(restriction_key(k, u, h), set()).add(k)
    assert len(bins) <= d

    h_a = projection(bhat, a_band)
    norm_a = lp(h_a, q)
    e_a = energy(bhat, a_band)
    if norm_a <= TOL or e_a <= TOL:
        raise ValueError("degenerate test trial")

    q_key = max(bins, key=lambda key: lp(projection(bhat, bins[key]), q))
    e_key = max(bins, key=lambda key: energy(bhat, bins[key]))
    m_key = max(bins, key=lambda key: len(bins[key]))

    selected_keys = {q_key, e_key, m_key}
    selected_keys |= {(-key) % h for key in tuple(selected_keys)}
    a_prime: set[int] = set()
    for key in selected_keys:
        a_prime.update(bins.get(key, set()))
    assert a_prime <= a_band
    actual_keys = {restriction_key(k, u, h) for k in a_prime}
    assert len(actual_keys) <= 6

    h_prime = projection(bhat, a_prime)
    h_q = projection(bhat, bins[q_key])
    q_projected = subgroup_projector(h_prime, u, q_key)
    projector_error = max_abs_diff(q_projected, h_q)

    norm_prime = lp(h_prime, q)
    norm_q = lp(h_q, q)
    e_prime = energy(bhat, a_prime)
    size_ratio = len(a_prime) / len(a_band)
    energy_ratio = e_prime / e_a
    q_ratio = norm_prime / norm_a
    y_ratio = energy_ratio * size_ratio ** (q - 2)

    assert projector_error <= TOL
    assert lp(q_projected, q) <= norm_prime + TOL
    assert norm_q + TOL >= norm_a / d
    assert q_ratio + TOL >= 1.0 / d
    assert energy_ratio + TOL >= 1.0 / d
    assert size_ratio + TOL >= 1.0 / d
    assert y_ratio + TOL >= d ** (-(q - 1))

    return TrialSummary(
        h=h,
        q=q,
        u=u,
        d=d,
        band_size=len(a_band),
        packet_size=len(a_prime),
        packet_cosets=len(actual_keys),
        q_ratio_scaled=q_ratio * d,
        energy_ratio_scaled=energy_ratio * d,
        size_ratio_scaled=size_ratio * d,
        y_ratio_scaled=y_ratio * d ** (q - 1),
        projector_error=projector_error,
        contraction_slack=norm_prime - lp(q_projected, q),
    )


def symmetric_bands(h: int) -> list[set[int]]:
    orbits: list[tuple[int, ...]] = []
    used = {0}
    for k in range(1, h):
        if k in used:
            continue
        orbit = tuple(sorted({k, (-k) % h}))
        orbits.append(orbit)
        used.update(orbit)
    result: list[set[int]] = []
    for mask in range(1, 1 << len(orbits)):
        band: set[int] = set()
        for i, orbit in enumerate(orbits):
            if (mask >> i) & 1:
                band.update(orbit)
        result.append(band)
    return result


def run_localization_regression() -> dict[str, float | int]:
    rng = random.Random(20260712)
    trials: list[TrialSummary] = []
    for h in (7, 8, 9, 11, 12):
        bands = symmetric_bands(h)
        rng.shuffle(bands)
        bands = bands[: min(12, len(bands))]
        for _ in range(4):
            b = [float(rng.randrange(0, 5)) for _ in range(h)]
            if not any(b):
                b[0] = 1.0
            for band in bands:
                bhat = dft([complex(v) for v in b])
                if energy(bhat, band) <= TOL or lp(projection(bhat, band), 4) <= TOL:
                    continue
                for u in range(1, h):
                    for q in (4, 6):
                        trials.append(combined_localization_trial(b, band, q, u))

    assert trials
    return {
        "finite_trials": len(trials),
        "max_packet_cosets": max(t.packet_cosets for t in trials),
        "min_q_ratio_times_d": min(t.q_ratio_scaled for t in trials),
        "min_energy_ratio_times_d": min(t.energy_ratio_scaled for t in trials),
        "min_size_ratio_times_d": min(t.size_ratio_scaled for t in trials),
        "min_Y_ratio_times_d^(q-1)": min(t.y_ratio_scaled for t in trials),
        "max_projector_error": max(t.projector_error for t in trials),
        "min_contraction_slack": min(t.contraction_slack for t in trials),
    }


def paired_planted_regression(b_pairs: int = 8) -> dict[str, float | int | bool]:
    assert b_pairs % 2 == 0
    # Exact integer pair sums: v_(i,0)=Q^i, v_(i,1)=C-Q^i.
    qbase = 7
    left = [qbase ** (i + 1) for i in range(b_pairs)]
    c = 3 * sum(left) + 1
    values = [value for x in left for value in (x, c - x)]

    supports: list[frozenset[int]] = []
    for chosen in itertools.combinations(range(b_pairs), b_pairs // 2):
        supports.append(
            frozenset(2 * i + side for i in chosen for side in (0, 1))
        )
    n = len(supports)
    a = b_pairs
    sums = [sum(values[t] for t in support) for support in supports]
    assert len(set(sums)) == 1
    assert all(
        len(s & t) <= a - 2
        for i, s in enumerate(supports)
        for t in supports[i + 1 :]
    )

    root = supports[0]
    layers: dict[int, list[frozenset[int]]] = {}
    for support in supports[1:]:
        r = len(root - support)
        layers.setdefault(r, []).append(support)
    r, layer = max(layers.items(), key=lambda item: len(item[1]))

    trade_checks = 0
    for support in layer:
        i_set = root - support
        j_set = support - root
        assert len(i_set) == len(j_set) == r
        assert r >= 2
        assert sum(values[t] for t in i_set) == sum(values[t] for t in j_set)
        trade_checks += 1

    # Uniform positive weight c_w=1/sqrt(n) lies in the flat branch:
    # Omega^2=n<2n.  The layer mass fraction equals its support fraction.
    weight = 1.0 / math.sqrt(n)
    omega = n * weight
    layer_mass = len(layer) * weight
    assert omega * omega < 2 * n
    assert len(layer) + TOL >= (n - 1) / (a - 1)
    assert layer_mass + TOL >= omega / (2 * (2 * b_pairs))

    return {
        "pair_count": b_pairs,
        "active_coordinates": 2 * b_pairs,
        "positive_supports": n,
        "fixed_trade_radius": r,
        "rooted_trade_incidences": trade_checks,
        "required_incidence_floor": (n - 1) / (a - 1),
        "positive_mass_fraction": layer_mass / omega,
        "required_mass_fraction_floor": 1.0 / (4 * b_pairs),
        "flat_branch": omega * omega < 2 * n,
        "all_checks": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="run deterministic checks")
    parser.add_argument("--json", action="store_true", help="print JSON only")
    args = parser.parse_args()

    localization = run_localization_regression()
    planted = paired_planted_regression()
    result = {
        "theorem": "source-secant-annihilator-localization-v1",
        "localization": localization,
        "planted_control": planted,
        "all_checks_pass": True,
    }

    # Final assertions with a little numerical room.
    assert localization["max_packet_cosets"] <= 6
    assert localization["min_q_ratio_times_d"] + TOL >= 1.0
    assert localization["min_energy_ratio_times_d"] + TOL >= 1.0
    assert localization["min_size_ratio_times_d"] + TOL >= 1.0
    assert localization["min_Y_ratio_times_d^(q-1)"] + TOL >= 1.0
    assert localization["max_projector_error"] <= TOL

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("SOURCE-SECANT ANNIHILATOR LOCALIZATION REGRESSION")
        print(json.dumps(result, indent=2, sort_keys=True))
        print("RESULT: PASS")


if __name__ == "__main__":
    main()
