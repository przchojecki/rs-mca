#!/usr/bin/env python3
"""Replay the mask-aware signed-spectrum census and its guardrails.

This is an experiment, not a proof of the mask-aware band restriction (MBR)
payment.  It computes complete fixed-weight Fourier coefficients, secant
kernels, signed contributions, threshold sweeps, character-triple moments,
and conservative structural proxies on finite source-like toys.  The artifact
is designed to reject sign-blind or mask-blind promotions.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE = (
    ROOT
    / "experimental"
    / "data"
    / "certificates"
    / "mask-aware-band-restriction-v1"
    / "mask_aware_band_restriction_v1.json"
)
NOTE = ROOT / "experimental" / "notes" / "audits" / "mask_aware_band_restriction_v1.md"
EXPERIMENT_ID = "mask-aware-band-restriction-v1"
SOURCE_BASE = "36de5bfcc7d6e0ca44806112acec2f4a1b4a7532"


def prime_factors(value: int) -> list[int]:
    factors = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        factors.append(value)
    return factors


def primitive_root(p: int) -> int:
    factors = prime_factors(p - 1)
    for candidate in range(2, p):
        if all(pow(candidate, (p - 1) // factor, p) != 1 for factor in factors):
            return candidate
    raise ValueError(f"no primitive root for p={p}")


def subgroup(p: int, n: int) -> list[int]:
    if (p - 1) % n:
        raise ValueError("n must divide p-1")
    generator = pow(primitive_root(p), (p - 1) // n, p)
    return [pow(generator, index, p) for index in range(n)]


def frequency_grid(p: int, rank: int) -> np.ndarray:
    grids = np.meshgrid(*([np.arange(p, dtype=np.int64)] * rank), indexing="ij")
    return np.stack([grid.ravel() for grid in grids], axis=1)


def flatten_coordinates(coords: np.ndarray, p: int) -> np.ndarray:
    index = np.zeros(len(coords), dtype=np.int64)
    for column in range(coords.shape[1]):
        index = index * p + coords[:, column]
    return index


def fixed_weight_fourier(phases: np.ndarray, m: int) -> np.ndarray:
    """Coefficient [t^m] prod_i (1+t*phase_i), vectorized by frequency."""
    count = phases.shape[0]
    coeffs = [np.ones(count, dtype=np.complex128)] + [
        np.zeros(count, dtype=np.complex128) for _ in range(m)
    ]
    for column in range(phases.shape[1]):
        value = phases[:, column]
        for weight in range(min(m, column + 1), 0, -1):
            coeffs[weight] += coeffs[weight - 1] * value
    return coeffs[m]


def exact_fibers(columns: list[tuple[int, ...]], p: int, m: int) -> Counter[tuple[int, ...]]:
    total = math.comb(len(columns), m)
    if total > 200_000:
        rank = len(columns[0])
        shape = (p,) * rank
        layers = [np.zeros(shape, dtype=np.int64) for _ in range(m + 1)]
        layers[0][(0,) * rank] = 1
        for column_index, column in enumerate(columns):
            for weight in range(min(m, column_index + 1), 0, -1):
                shifted = layers[weight - 1]
                for axis, value in enumerate(column):
                    shifted = np.roll(shifted, int(value), axis=axis)
                layers[weight] += shifted
        flat = layers[m].ravel()
        return Counter({(int(index),): int(value) for index, value in enumerate(flat) if value})
    output: Counter[tuple[int, ...]] = Counter()
    rank = len(columns[0])
    for support in itertools.combinations(range(len(columns)), m):
        image = tuple(sum(columns[i][j] for i in support) % p for j in range(rank))
        output[image] += 1
    return output


def phase_statistics(residues: np.ndarray, p: int) -> dict[str, Any]:
    distances = np.minimum(residues, p - residues) / p
    return {
        "phase_image_size": int(len(set(int(value) for value in residues))),
        "bohr_fraction_005": float(np.mean(distances <= 0.05)),
        "bohr_fraction_010": float(np.mean(distances <= 0.10)),
        "bohr_fraction_020": float(np.mean(distances <= 0.20)),
    }


def classify_frequency(
    profile: dict[str, Any], coords: np.ndarray, residues: np.ndarray, tau_abs: float
) -> tuple[str, dict[str, Any]]:
    p = profile["p"]
    n = profile["n"]
    if np.all(coords == 0):
        return "zero", phase_statistics(residues, p)
    stats = phase_statistics(residues, p)
    if profile.get("planted_pair"):
        return "planted_pair_relation", stats
    if tau_abs >= n - 1e-8:
        return "exact_phase_collapse", stats
    # Coordinates are moments j=1,...,R.  Vanishing odd coordinates is the
    # first dyadic-conductor proxy; this is not asserted to be an atlas proof.
    odd_positions = np.arange(profile["rank"]) % 2 == 0
    if np.all(coords[odd_positions] == 0):
        return "dyadic_even_frequency_proxy", stats
    nonzero = np.flatnonzero(coords)
    if len(nonzero) and nonzero[-1] == 0:
        return "low_degree_phase_proxy", stats
    if stats["phase_image_size"] <= max(2, n // 2):
        return "small_phase_image_proxy", stats
    if stats["bohr_fraction_010"] >= 0.75:
        return "quadratic_bohr_proxy", stats
    return "unclassified", stats


def make_subgroup_profile(name: str, p: int, n: int, rank: int, m: int) -> dict[str, Any]:
    domain = subgroup(p, n)
    columns = [tuple(pow(value, degree, p) for degree in range(1, rank + 1)) for value in domain]
    return {
        "name": name,
        "kind": "source_like_subgroup_identity",
        "p": p,
        "n": n,
        "rank": rank,
        "m": m,
        "domain": domain,
        "columns": columns,
        "planted_pair": False,
    }


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def next_prime(value: int) -> int:
    candidate = value if value % 2 else value + 1
    while not is_prime(candidate):
        candidate += 2
    return candidate


def make_planted_profile(b: int = 4, q: int = 5) -> dict[str, Any]:
    powers = [q ** (i + 1) for i in range(b)]
    c_value = 4 * sum(powers) + 1
    weights = []
    for value in powers:
        weights.extend((value, c_value - value))
    p = next_prime(2 * b * c_value + 1)
    return {
        "name": f"planted_pair_B{b}",
        "kind": "arbitrary_weight_regression",
        "p": p,
        "n": 2 * b,
        "rank": 1,
        "m": b,
        "domain": list(range(1, 2 * b + 1)),
        "columns": [(value % p,) for value in weights],
        "planted_pair": True,
        "pair_sum": c_value,
        "source_scope": "not_source_derived",
    }


def threshold_sweep(
    profile: dict[str, Any], tau_abs: np.ndarray, contribution: np.ndarray, zero_index: int
) -> list[dict[str, Any]]:
    mask = np.ones(len(tau_abs), dtype=bool)
    mask[zero_index] = False
    values = tau_abs[mask]
    real = contribution.real
    total_positive = float(np.maximum(real[mask], 0).sum())
    total_abs = float(np.abs(contribution[mask]).sum())
    mu = math.comb(profile["n"], profile["m"]) / (profile["p"] ** profile["rank"])
    secant_scale = profile["n"] ** 2 * mu
    rows = []
    for quantile in (0.50, 0.75, 0.90, 0.95, 0.99):
        threshold = float(np.quantile(values, quantile))
        exceptional = mask & (tau_abs >= threshold - 1e-12)
        bulk = mask & ~exceptional
        rows.append(
            {
                "quantile": quantile,
                "threshold": threshold,
                "exceptional_count": int(exceptional.sum()),
                "exceptional_fraction": float(exceptional.sum() / mask.sum()),
                "bulk_signed": float(real[bulk].sum()),
                "bulk_signed_over_n2mu": float(real[bulk].sum() / secant_scale),
                "bulk_positive": float(np.maximum(real[bulk], 0).sum()),
                "bulk_positive_over_n2mu": float(
                    np.maximum(real[bulk], 0).sum() / secant_scale
                ),
                "bulk_absolute": float(np.abs(contribution[bulk]).sum()),
                "exceptional_signed": float(real[exceptional].sum()),
                "exceptional_positive": float(np.maximum(real[exceptional], 0).sum()),
                "exceptional_absolute": float(np.abs(contribution[exceptional]).sum()),
                "exceptional_positive_share": (
                    float(np.maximum(real[exceptional], 0).sum() / total_positive)
                    if total_positive
                    else 0.0
                ),
                "exceptional_absolute_share": (
                    float(np.abs(contribution[exceptional]).sum() / total_abs)
                    if total_abs
                    else 0.0
                ),
            }
        )
    return rows


def square_root_threshold_sweep(
    profile: dict[str, Any], tau_abs: np.ndarray, contribution: np.ndarray, zero_index: int
) -> list[dict[str, Any]]:
    mask = np.ones(len(tau_abs), dtype=bool)
    mask[zero_index] = False
    real = contribution.real
    total_positive = float(np.maximum(real[mask], 0).sum())
    total_abs = float(np.abs(contribution[mask]).sum())
    mu = math.comb(profile["n"], profile["m"]) / (profile["p"] ** profile["rank"])
    secant_scale = profile["n"] ** 2 * mu
    rows = []
    for multiplier in (1.0, 1.25, 1.5, 1.75, 2.0):
        threshold = multiplier * math.sqrt(profile["n"])
        exceptional = mask & (tau_abs >= threshold - 1e-12)
        bulk = mask & ~exceptional
        rows.append(
            {
                "sqrt_n_multiplier": multiplier,
                "threshold": threshold,
                "exceptional_count": int(exceptional.sum()),
                "exceptional_fraction": float(exceptional.sum() / mask.sum()),
                "exceptional_positive_share": (
                    float(np.maximum(real[exceptional], 0).sum() / total_positive)
                    if total_positive
                    else 0.0
                ),
                "exceptional_absolute_share": (
                    float(np.abs(contribution[exceptional]).sum() / total_abs)
                    if total_abs
                    else 0.0
                ),
                "bulk_signed_over_n2mu": float(real[bulk].sum() / secant_scale),
                "bulk_positive_over_n2mu": float(
                    np.maximum(real[bulk], 0).sum() / secant_scale
                ),
            }
        )
    return rows


def semantic_proxy_census(
    profile: dict[str, Any],
    coords: np.ndarray,
    residues: np.ndarray,
    tau_abs: np.ndarray,
    contribution: np.ndarray,
) -> dict[str, Any]:
    nonzero_tau = tau_abs[1:]
    threshold = float(np.quantile(nonzero_tau, 0.95))
    indices = np.flatnonzero((tau_abs >= threshold - 1e-12) & (np.arange(len(tau_abs)) != 0))
    counts: Counter[str] = Counter()
    positive_mass: Counter[str] = Counter()
    absolute_mass: Counter[str] = Counter()
    bohr_stats: dict[str, list[float]] = {
        "bohr_fraction_005": [],
        "bohr_fraction_010": [],
        "bohr_fraction_020": [],
    }
    for index in indices:
        label, stats = classify_frequency(profile, coords[index], residues[index], float(tau_abs[index]))
        counts[label] += 1
        positive_mass[label] += max(float(contribution[index].real), 0.0)
        absolute_mass[label] += float(abs(contribution[index]))
        for key in bohr_stats:
            bohr_stats[key].append(stats[key])
    total_positive = sum(positive_mass.values())
    total_absolute = sum(absolute_mass.values())
    return {
        "threshold_quantile": 0.95,
        "threshold": threshold,
        "exceptional_count": len(indices),
        "class_counts": dict(sorted(counts.items())),
        "class_positive_mass": dict(sorted(positive_mass.items())),
        "class_absolute_mass": dict(sorted(absolute_mass.items())),
        "classified_fraction": (
            1.0 - counts.get("unclassified", 0) / len(indices) if len(indices) else 1.0
        ),
        "classified_positive_mass_fraction": (
            1.0 - positive_mass.get("unclassified", 0.0) / total_positive
            if total_positive
            else 1.0
        ),
        "classified_absolute_mass_fraction": (
            1.0 - absolute_mass.get("unclassified", 0.0) / total_absolute
            if total_absolute
            else 1.0
        ),
        "mean_bohr_fractions": {
            key: float(np.mean(values)) if values else 0.0 for key, values in bohr_stats.items()
        },
        "warning": "labels are conservative structural proxies, not semantic atlas certificates",
    }


def band_payment_census(
    profile: dict[str, Any],
    coords: np.ndarray,
    tau_abs: np.ndarray,
    image_size: int,
) -> dict[str, Any]:
    """Finite diagnostics for the proved sparse-pattern bound.

    The thresholds 1, N, and N^2 are declared review proxies for exp(o(N));
    they are not asymptotic theorem statuses.
    """
    p = profile["p"]
    rank = profile["rank"]
    n = profile["n"]
    group_size = len(coords)
    nonzero = np.arange(group_size) != 0
    bands = []
    assignments = np.full(group_size, -2, dtype=np.int64)
    assignments[nonzero & (tau_abs < 1.0)] = -1
    for index in np.flatnonzero(nonzero & (tau_abs >= 1.0)):
        assignments[index] = int(math.floor(math.log2(float(tau_abs[index])) + 1e-12))

    low_mask = assignments == -1
    if np.any(low_mask):
        bands.append(
            {
                "label": "lt1",
                "dyadic_index": None,
                "mask": low_mask,
                "moment_density_upper": 1.0,
            }
        )
    for band_index in range(math.ceil(math.log2(n)) + 1):
        mask = assignments == band_index
        if not np.any(mask):
            continue
        moment_upper = min(
            [1.0]
            + [
                math.factorial(order)
                * n**order
                / 2 ** (2 * order * band_index)
                for order in range(1, rank + 1)
            ]
        )
        bands.append(
            {
                "label": f"k{band_index}",
                "dyadic_index": band_index,
                "mask": mask,
                "moment_density_upper": moment_upper,
            }
        )

    shape = (p,) * rank
    negative_index = flatten_coordinates((-coords) % p, p)
    indicator_arrays = [band["mask"].astype(np.float64).reshape(shape) for band in bands]
    transforms = [np.fft.fftn(array) for array in indicator_arrays]
    pair_convolutions: dict[tuple[int, int], np.ndarray] = {}
    for first in range(len(bands)):
        for second in range(len(bands)):
            pair_convolutions[(first, second)] = np.rint(
                np.fft.ifftn(transforms[first] * transforms[second]).real
            ).astype(np.int64).ravel()

    patterns = []
    rho = 1.0
    budgets = {"one": 1.0, "N": float(n), "N2": float(n**2)}
    counts = {
        "nonempty": 0,
        "exact": {key: 0 for key in budgets},
        "moment_certified": {key: 0 for key in budgets},
    }
    for pattern in itertools.product(range(len(bands)), repeat=3):
        third_mask = bands[pattern[2]]["mask"]
        tuple_count = int(
            np.dot(
                pair_convolutions[(pattern[0], pattern[1])][negative_index],
                third_mask.astype(np.int64),
            )
        )
        if tuple_count == 0:
            continue
        exact_densities = [float(np.mean(bands[index]["mask"])) for index in pattern]
        certified_densities = [
            bands[index]["moment_density_upper"] for index in pattern
        ]
        exact_geometric = math.prod(exact_densities) ** (1 / 3)
        certified_geometric = math.prod(certified_densities) ** (1 / 3)
        exact_load = image_size * rho * exact_geometric
        certified_load = image_size * rho * certified_geometric
        row = {
            "labels": [bands[index]["label"] for index in pattern],
            "tuple_count": tuple_count,
            "tuple_density": tuple_count / group_size**2,
            "exact_D": exact_geometric,
            "moment_certified_D_upper": certified_geometric,
            "exact_L_rho_D": exact_load,
            "moment_certified_L_rho_D_upper": certified_load,
            "exact_positive_log_rate": math.log(max(1.0, exact_load)) / n,
            "moment_certified_positive_log_rate": math.log(
                max(1.0, certified_load)
            )
            / n,
        }
        patterns.append(row)
        counts["nonempty"] += 1
        for key, budget in budgets.items():
            counts["exact"][key] += int(exact_load <= budget + 1e-12)
            counts["moment_certified"][key] += int(
                certified_load <= budget + 1e-12
            )

    patterns.sort(
        key=lambda row: (
            row["moment_certified_L_rho_D_upper"],
            row["exact_L_rho_D"],
        ),
        reverse=True,
    )
    nonempty_count = counts["nonempty"]
    dense_patterns = [
        row
        for row in patterns
        if row["moment_certified_L_rho_D_upper"] > n**2 + 1e-12
    ]
    return {
        "scope": "full-slice finite diagnostic with rho=1",
        "order": 3,
        "band_count": len(bands),
        "partitioned_nonzero_frequency_count": int(
            sum(np.sum(band["mask"]) for band in bands)
        ),
        "bands": [
            {
                "label": band["label"],
                "dyadic_index": band["dyadic_index"],
                "size": int(np.sum(band["mask"])),
                "exact_density": float(np.mean(band["mask"])),
                "moment_density_upper": band["moment_density_upper"],
                "repeated_exact_L_rho_D": image_size
                * float(np.mean(band["mask"])),
                "repeated_moment_certified_L_rho_D_upper": image_size
                * band["moment_density_upper"],
            }
            for band in bands
        ],
        "nonempty_complete_patterns": nonempty_count,
        "proxy_budgets": budgets,
        "fractions_at_proxy_budget": {
            "exact": {
                key: counts["exact"][key] / nonempty_count if nonempty_count else 1.0
                for key in budgets
            },
            "moment_certified": {
                key: counts["moment_certified"][key] / nonempty_count
                if nonempty_count
                else 1.0
                for key in budgets
            },
        },
        "dense_diagnostic_residual_count_at_N2": len(dense_patterns),
        "dense_diagnostic_residual_at_N2": dense_patterns[:3],
        "largest_patterns": patterns[:3],
        "warning": (
            "proxy budgets are finite diagnostics for exp(o(N)); "
            "they do not classify an asymptotic pattern as proved or open"
        ),
    }


def analyze_profile(profile: dict[str, Any], do_triples: bool) -> tuple[dict[str, Any], dict[str, Any]]:
    p = profile["p"]
    rank = profile["rank"]
    columns = np.asarray(profile["columns"], dtype=np.int64)
    coords = frequency_grid(p, rank)
    residues = (coords @ columns.T) % p
    phases = np.exp(2j * np.pi * residues / p)
    tau = phases.sum(axis=1)
    tau_abs = np.abs(tau)
    nuhat = fixed_weight_fourier(phases, profile["m"])
    kernel = tau_abs**2 - profile["n"]
    contribution = nuhat * kernel / (p**rank)
    fibers = exact_fibers(profile["columns"], p, profile["m"])
    full_mass = math.comb(profile["n"], profile["m"])
    image_size = len(fibers)
    average = full_mass / image_size
    maximum = max(fibers.values())
    zero_index = 0
    nonzero = np.arange(len(tau_abs)) != zero_index
    signed_total = float(contribution[nonzero].real.sum())
    absolute_total = float(np.abs(contribution[nonzero]).sum())
    positive_total = float(np.maximum(contribution[nonzero].real, 0).sum())

    result = {
        "name": profile["name"],
        "kind": profile["kind"],
        "parameters": {
            "p": p,
            "n": profile["n"],
            "rank": rank,
            "m": profile["m"],
            "frequency_count": len(coords),
        },
        "fiber": {
            "full_mass": full_mass,
            "image_size": image_size,
            "image_average": average,
            "max_fiber": maximum,
            "max_over_average": maximum / average,
        },
        "sign_ablation": {
            "signed_nonzero_sum": signed_total,
            "positive_part_sum": positive_total,
            "absolute_sum": absolute_total,
            "absolute_over_signed": absolute_total / max(abs(signed_total), 1e-15),
            "positive_over_signed": positive_total / max(abs(signed_total), 1e-15),
        },
        "threshold_sweep": threshold_sweep(profile, tau_abs, contribution, zero_index),
        "sqrt_n_threshold_sweep": square_root_threshold_sweep(
            profile, tau_abs, contribution, zero_index
        ),
        "semantic_proxy": semantic_proxy_census(profile, coords, residues, tau_abs, contribution),
        "band_payment_census": band_payment_census(
            profile, coords, tau_abs, image_size
        ),
    }
    if profile.get("source_scope"):
        result["source_scope"] = profile["source_scope"]

    state = {
        "coords": coords,
        "tau_abs": tau_abs,
        "nuhat": nuhat,
    }
    if do_triples:
        result["triple_census"] = triple_census(profile, state)
    return result, state


def triple_census(profile: dict[str, Any], state: dict[str, Any]) -> dict[str, Any]:
    p = profile["p"]
    rank = profile["rank"]
    coords = state["coords"]
    tau_abs = state["tau_abs"]
    nuhat = state["nuhat"]
    q_count = len(coords)
    if q_count * q_count > 1_000_000:
        return {"skipped": True, "reason": "frequency-pair count exceeds 1e6"}
    threshold = float(np.quantile(tau_abs[1:], 0.90))
    total_positive = 0.0
    total_absolute = 0.0
    any_high_positive = 0.0
    any_high_absolute = 0.0
    any_high_count = 0
    product_scores = []
    positive_values = []
    absolute_values = []
    nonzero_indices = np.arange(q_count) != 0
    high_frequency = tau_abs >= threshold - 1e-12
    high_frequency[0] = False
    for index in range(1, q_count):
        third_coords = (-coords[index] - coords) % p
        third_index = flatten_coordinates(third_coords, p)
        terms = nuhat[index] * nuhat * nuhat[third_index] / (p ** (2 * rank))
        real = terms.real
        absolute = np.abs(terms)
        positive = np.maximum(real, 0)
        valid = nonzero_indices & (third_index != 0)
        high = valid & (
            high_frequency[index] | high_frequency | high_frequency[third_index]
        )
        positive[~valid] = 0.0
        absolute[~valid] = 0.0
        total_positive += float(positive.sum())
        total_absolute += float(absolute.sum())
        any_high_positive += float(positive[high].sum())
        any_high_absolute += float(absolute[high].sum())
        any_high_count += int(high.sum())
        product_scores.extend((tau_abs[index] * tau_abs[valid] * tau_abs[third_index[valid]]).tolist())
        positive_values.extend(positive[valid].tolist())
        absolute_values.extend(absolute[valid].tolist())

    scores = np.asarray(product_scores)
    positives = np.asarray(positive_values)
    absolutes = np.asarray(absolute_values)
    tuple_total = len(scores)
    selected_fraction = any_high_count / tuple_total
    product_threshold = float(np.quantile(scores, 1.0 - selected_fraction))
    product_high = scores >= product_threshold - 1e-12
    geometric_mean = np.cbrt(np.maximum(scores, 0.0))
    fixed_geometric_sweep = []
    for multiplier in (1.0, 1.25, 1.5, 1.75, 2.0):
        threshold_fixed = multiplier * math.sqrt(profile["n"])
        selected = geometric_mean >= threshold_fixed - 1e-12
        fixed_geometric_sweep.append(
            {
                "sqrt_n_multiplier": multiplier,
                "tuple_fraction": float(selected.mean()),
                "positive_share": (
                    float(positives[selected].sum() / total_positive) if total_positive else 0.0
                ),
                "absolute_share": (
                    float(absolutes[selected].sum() / total_absolute) if total_absolute else 0.0
                ),
            }
        )
    return {
        "skipped": False,
        "order": 3,
        "single_frequency_threshold_quantile": 0.90,
        "single_frequency_threshold": threshold,
        "any_high_tuple_fraction": selected_fraction,
        "any_high_positive_share": any_high_positive / total_positive if total_positive else 0.0,
        "any_high_absolute_share": any_high_absolute / total_absolute if total_absolute else 0.0,
        "product_score_threshold_same_fraction": product_threshold,
        "product_high_positive_share": (
            float(positives[product_high].sum() / total_positive) if total_positive else 0.0
        ),
        "product_high_absolute_share": (
            float(absolutes[product_high].sum() / total_absolute) if total_absolute else 0.0
        ),
        "fixed_geometric_mean_sweep": fixed_geometric_sweep,
        "interpretation": "compares any-large-single-frequency against tuple-product selection at matched density",
    }


def external_regressions() -> dict[str, Any]:
    return {
        "chg_signed_witness": {
            "source": "PR #662 committed census",
            "p": 11,
            "c": 2,
            "z": [1, 7],
            "P": [10, 3, 6],
            "termwise_absolute": 374.0,
            "signed_magnitude": 31.3093,
            "toy_n_cubed": 125.0,
            "sign_blind_fails_while_signed_passes": True,
        },
        "balanced_zero_twist": {
            "source": "PR #662 full-rank bridge",
            "parameters": [7, 6, 1, 3],
            "statement": "v=0 complementary twist is zero when m=n/2",
            "role": "guard against assuming a nonzero endpoint exceptional phase",
        },
    }


def exact_reduction_regressions() -> dict[str, Any]:
    """Finite checks of the exact peeling, pattern, tail, and diagonal identities."""
    group_size = 11
    residual = np.asarray([3.0, 1.0, 4.0, 0.0, 2.0, 1.0, 0.0, 5.0, 2.0, 0.0, 1.0])
    fhat = np.fft.fft(residual)
    mass = float(residual.sum())
    peeling_errors = []
    for order in range(2, 6):
        nonzero_sector = 0.0j
        for prefix in itertools.product(range(1, group_size), repeat=order - 1):
            last = (-sum(prefix)) % group_size
            if last:
                term = fhat[last]
                for gamma in prefix:
                    term *= fhat[gamma]
                nonzero_sector += term
        rhs = mass**order
        for nonzero_count in range(2, order + 1):
            sector = 0.0j
            for prefix in itertools.product(
                range(1, group_size), repeat=nonzero_count - 1
            ):
                last = (-sum(prefix)) % group_size
                if last:
                    term = fhat[last]
                    for gamma in prefix:
                        term *= fhat[gamma]
                    sector += term
            rhs += math.comb(order, nonzero_count) * mass ** (
                order - nonzero_count
            ) * sector
        lhs = group_size ** (order - 1) * float(np.sum(residual**order))
        peeling_errors.append(float(abs(lhs - rhs)))

    roots = np.exp(2j * np.pi * np.arange(group_size) / group_size)
    columns = (0, 1, 2, 3)
    tau = np.asarray(
        [sum(roots[(gamma * column) % group_size] for column in columns) for gamma in range(group_size)]
    )
    bands: list[list[int]] = []
    low = [gamma for gamma in range(1, group_size) if abs(tau[gamma]) < 1.0]
    if low:
        bands.append(low)
    for band_index in range(math.ceil(math.log2(len(columns))) + 1):
        band = [
            gamma
            for gamma in range(1, group_size)
            if 2**band_index <= abs(tau[gamma]) < 2 ** (band_index + 1)
        ]
        if band:
            bands.append(band)

    characters = np.exp(
        2j
        * np.pi
        * np.outer(np.arange(group_size), np.arange(group_size))
        / group_size
    )
    projections = [
        sum(fhat[gamma] * characters[gamma] for gamma in band) / group_size
        for band in bands
    ]
    pattern_errors = []
    sparse_pattern_ratios = []
    for pattern in itertools.product(range(len(bands)), repeat=3):
        tuple_sum = 0.0j
        for first in bands[pattern[0]]:
            for second in bands[pattern[1]]:
                third = (-first - second) % group_size
                if third in bands[pattern[2]]:
                    tuple_sum += fhat[first] * fhat[second] * fhat[third]
        physical = group_size**2 * np.sum(
            projections[pattern[0]]
            * projections[pattern[1]]
            * projections[pattern[2]]
        )
        pattern_errors.append(float(abs(tuple_sum - physical)))
        densities = [len(bands[index]) / group_size for index in pattern]
        geometric_density = math.prod(densities) ** (1 / 3)
        sparse_bound = mass**3 * geometric_density**2
        sparse_pattern_ratios.append(
            float(abs(np.sum(projections[pattern[0]] * projections[pattern[1]] * projections[pattern[2]])) / sparse_bound)
            if sparse_bound
            else 0.0
        )

    band_density_ratios = []
    interpolation_ratios = []
    top_order = 5
    for band, projection in zip(bands, projections):
        density = len(band) / group_size
        for order in range(2, top_order + 1):
            lhs = float(np.linalg.norm(projection, ord=order))
            rhs = mass * density ** (1 - 1 / order)
            band_density_ratios.append(lhs / rhs if rhs else 0.0)
            theta_order = 2 * (top_order - order) / (order * (top_order - 2))
            interpolated = float(np.linalg.norm(projection, ord=2)) ** theta_order * float(
                np.linalg.norm(projection, ord=top_order)
            ) ** (1 - theta_order)
            interpolation_ratios.append(lhs / interpolated if interpolated else 0.0)

    repeated_endpoint_rhs = mass / group_size + sum(
        float(np.linalg.norm(projection, ord=top_order)) for projection in projections
    )
    repeated_endpoint_ratio = float(np.max(residual) / repeated_endpoint_rhs)

    dual_projection = np.real_if_close(projections[0]).real
    dual_order = 3
    dual_norm = float(np.linalg.norm(dual_projection, ord=dual_order))
    dual_function = (
        np.sign(dual_projection)
        * np.abs(dual_projection) ** (dual_order - 1)
        / dual_norm ** (dual_order - 1)
    )
    projected_dual = np.real_if_close(
        sum(
            np.fft.fft(dual_function)[gamma] * characters[gamma]
            for gamma in bands[0]
        )
        / group_size
    ).real
    dual_pairing = float(np.dot(residual, projected_dual))
    order_two_localization_ratio = float(
        np.linalg.norm(dual_projection, ord=2) ** 2
        / (float(np.max(residual)) * mass)
    )

    exponent_checks = 0
    for compiler_order in range(3, 13):
        for lower_order in range(2, compiler_order + 1):
            theta_exact = Fraction(
                2 * (compiler_order - lower_order),
                lower_order * (compiler_order - 2),
            )
            exponent = Fraction(lower_order - 1, 1) - lower_order * (
                1 - theta_exact
            ) * (1 - Fraction(1, compiler_order))
            expected_exponent = Fraction(
                compiler_order - lower_order, compiler_order - 2
            )
            if exponent != expected_exponent:
                raise AssertionError("top-order compiler exponent identity failed")
            exponent_checks += 1

    point_mass = np.zeros(group_size)
    point_mass[2] = 5.0
    point_hat = np.fft.fft(point_mass)
    point_mass_band_errors = []
    for band in bands:
        point_projection = sum(
            point_hat[gamma] * characters[gamma] for gamma in band
        ) / group_size
        point_mass_band_errors.append(
            float(abs(point_projection[2] - 5.0 * len(band) / group_size))
        )
    diagonal_errors = []
    for first in range(group_size):
        for second in range(group_size):
            third = (-first - second) % group_size
            diagonal_errors.append(
                float(abs(point_hat[first] * point_hat[second] * point_hat[third] - 125.0))
            )

    theta = 2.0
    order = 3
    exceptional_count = 0
    for first in range(1, group_size):
        for second in range(1, group_size):
            third = (-first - second) % group_size
            if third == 0:
                continue
            score = (abs(tau[first]) * abs(tau[second]) * abs(tau[third])) ** (1 / order)
            exceptional_count += int(score >= theta)
    one_coordinate_bound = order * len(columns) / theta**2
    return {
        "group": "Z/11Z",
        "orders_checked": [2, 3, 4, 5],
        "max_zero_peeling_error": max(peeling_errors),
        "band_count": len(bands),
        "complete_patterns_checked": len(bands) ** 3,
        "max_complete_pattern_identity_error": max(pattern_errors),
        "max_universal_band_density_ratio": max(band_density_ratios),
        "max_sparse_triple_pattern_ratio": max(sparse_pattern_ratios),
        "max_top_order_interpolation_ratio": max(interpolation_ratios),
        "exact_top_order_exponent_checks": exponent_checks,
        "repeated_pattern_endpoint_ratio": repeated_endpoint_ratio,
        "dual_witness_pairing_error": abs(dual_pairing - dual_norm),
        "order_two_localization_ratio": order_two_localization_ratio,
        "point_mass_zero_sum_triples_checked": group_size**2,
        "max_diagonal_identity_error": max(diagonal_errors),
        "max_point_mass_band_value_error": max(point_mass_band_errors),
        "tail_check": {
            "order": order,
            "theta": theta,
            "actual_density": exceptional_count / group_size ** (order - 1),
            "one_coordinate_h1_bound": one_coordinate_bound,
            "passes": exceptional_count / group_size ** (order - 1)
            <= one_coordinate_bound + 1e-12,
        },
    }


def build_report(results: list[dict[str, Any]]) -> str:
    lines = [
        "# Signed exceptional-spectrum census v1",
        "",
        "```text",
        "Status: EXPERIMENTAL / NOT A PROOF",
        "Purpose: determine viable statements for signed bulk and exceptional inverse lemmas",
        "```",
        "",
        "## Profile summary",
        "",
        "| profile | p | n | R | m | max/avg | abs/signed | q90 exceptional positive share | proxy positive-mass covered |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in results:
        q90 = next(item for item in row["threshold_sweep"] if item["quantile"] == 0.90)
        lines.append(
            f"| {row['name']} | {row['parameters']['p']} | {row['parameters']['n']} | "
            f"{row['parameters']['rank']} | {row['parameters']['m']} | "
            f"{row['fiber']['max_over_average']:.4g} | "
            f"{row['sign_ablation']['absolute_over_signed']:.4g} | "
            f"{q90['exceptional_positive_share']:.3f} | "
            f"{row['semantic_proxy']['classified_positive_mass_fraction']:.3f} |"
        )
    lines.extend(["", "## Character-triple comparison", ""])
    for row in results:
        triple = row.get("triple_census")
        if not triple or triple.get("skipped"):
            continue
        lines.append(
            f"- `{row['name']}`: any-high positive share "
            f"`{triple['any_high_positive_share']:.3f}`, matched-density product-high "
            f"positive share `{triple['product_high_positive_share']:.3f}`; "
            f"geometric `1.5 sqrt(n)` share "
            f"`{next(item for item in triple['fixed_geometric_mean_sweep'] if item['sqrt_n_multiplier'] == 1.5)['positive_share']:.3f}`."
        )
    lines.extend(["", "## Fixed square-root threshold (1.5 sqrt(n))", ""])
    for row in results:
        fixed = next(
            item
            for item in row["sqrt_n_threshold_sweep"]
            if item["sqrt_n_multiplier"] == 1.5
        )
        lines.append(
            f"- `{row['name']}`: exceptional fraction `{fixed['exceptional_fraction']:.3f}`, "
            f"positive share `{fixed['exceptional_positive_share']:.3f}`, "
            f"bulk signed / `n^2 mu` `{fixed['bulk_signed_over_n2mu']:.4g}`."
        )
    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- Structural labels are proxies, not semantic atlas certificates.",
            "- The planted-pair row is intentionally not source-derived.",
            "- Finite toys can falsify a decomposition but cannot prove uniform asymptotics.",
            "- Signed and absolute totals are both printed; no absolute-value payment is promoted.",
            "",
        ]
    )
    return "\n".join(lines)


def payload_digest(payload: dict[str, Any]) -> str:
    unsigned = dict(payload)
    unsigned.pop("payload_sha256", None)
    encoded = json.dumps(
        unsigned, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")
    return hashlib.sha256(encoded).hexdigest()


def build_payload(*, verbose: bool = False) -> dict[str, Any]:
    profiles = [
        make_subgroup_profile("sg17_n8_w2_m4", 17, 8, 2, 4),
        make_subgroup_profile("sg13_n12_w2_m6", 13, 12, 2, 6),
        make_subgroup_profile("sg17_n16_w2_m8", 17, 16, 2, 8),
        make_subgroup_profile("sg19_n18_w2_m9", 19, 18, 2, 9),
        make_subgroup_profile("sg41_n8_w2_m4", 41, 8, 2, 4),
        make_subgroup_profile("sg17_n8_w3_m4", 17, 8, 3, 4),
        make_subgroup_profile("sg17_n16_w3_m8", 17, 16, 3, 8),
        make_subgroup_profile("sg73_n24_w2_m12", 73, 24, 2, 12),
        make_subgroup_profile("sg97_n16_w2_m8", 97, 16, 2, 8),
        make_subgroup_profile("sg193_n24_w2_m12", 193, 24, 2, 12),
        make_planted_profile(4),
    ]
    triple_names = {"sg17_n8_w2_m4", "sg13_n12_w2_m6", "sg17_n16_w2_m8"}
    results = []
    for profile in profiles:
        if verbose:
            print(f"analyzing {profile['name']} ...", flush=True)
        result, _ = analyze_profile(profile, profile["name"] in triple_names)
        results.append(result)
    payload = {
        "status": "EXPERIMENTAL / PROVED FINITE REDUCTIONS / OPEN ROOTED DENSE-BAND BCI",
        "experiment_id": EXPERIMENT_ID,
        "source_base": SOURCE_BASE,
        "claim_boundary": {
            "proved_in_note": [
                "exact zero-character peeling identity",
                "one-coordinate tuple-tail certificate",
                "tensor-Holder tuple-tail certificate",
                "diagonal point-mass obstruction",
                "complete-band-pattern Fourier identity",
                "universal mask-aware band-density restriction",
                "sparse-pattern absolute payment criterion",
                "top-order BR implies all lower bulk sectors",
                "repeated-pattern endpoint guardrail",
                "per-band point-mass low-spectrum guardrail",
                "order-two BCI localization to the PRE/Q endpoint",
                "exact dual witness for every MBR violation",
            ],
            "experimental_only": [
                "finite threshold census",
                "tuple-product versus any-large-coordinate comparison",
                "structural proxy coverage",
                "finite paid-versus-dense proxy census",
            ],
            "not_proved": [
                "dense low-tau top-order band restriction payment",
                "rooted band-to-cell inverse theorem",
                "full source-specific mask-aware multilinear band restriction payment",
                "exceptional-spectrum inverse compiler",
                "A4 payment",
                "primitive Q",
                "Proximity Prize theorem",
            ],
        },
        "exact_reduction_regressions": exact_reduction_regressions(),
        "profiles": results,
        "external_regressions": external_regressions(),
    }
    payload["payload_sha256"] = payload_digest(payload)
    return payload


def profile_by_name(payload: dict[str, Any], name: str) -> dict[str, Any]:
    return next(row for row in payload["profiles"] if row["name"] == name)


def validate_payload(payload: dict[str, Any]) -> None:
    if payload.get("experiment_id") != EXPERIMENT_ID:
        raise AssertionError("wrong experiment id")
    if payload.get("status") != "EXPERIMENTAL / PROVED FINITE REDUCTIONS / OPEN ROOTED DENSE-BAND BCI":
        raise AssertionError("status boundary was weakened")
    if payload.get("payload_sha256") != payload_digest(payload):
        raise AssertionError("payload hash mismatch")
    if len(payload.get("profiles", [])) != 11:
        raise AssertionError("expected ten source-like toys and one planted regression")
    reductions = payload.get("exact_reduction_regressions", {})
    if reductions.get("max_zero_peeling_error", 1.0) > 1e-6:
        raise AssertionError("zero-character peeling regression failed")
    if reductions.get("max_complete_pattern_identity_error", 1.0) > 1e-8:
        raise AssertionError("complete-band-pattern identity regression failed")
    if reductions.get("max_diagonal_identity_error", 1.0) > 1e-8:
        raise AssertionError("diagonal point-mass identity regression failed")
    if reductions.get("max_universal_band_density_ratio", 2.0) > 1 + 1e-9:
        raise AssertionError("universal band-density restriction regression failed")
    if reductions.get("max_sparse_triple_pattern_ratio", 2.0) > 1 + 1e-9:
        raise AssertionError("sparse complete-pattern payment regression failed")
    if reductions.get("max_top_order_interpolation_ratio", 2.0) > 1 + 1e-9:
        raise AssertionError("top-order interpolation regression failed")
    if reductions.get("exact_top_order_exponent_checks") != 65:
        raise AssertionError("top-order exponent identity regression failed")
    if reductions.get("repeated_pattern_endpoint_ratio", 2.0) > 1 + 1e-9:
        raise AssertionError("repeated-pattern endpoint regression failed")
    if reductions.get("dual_witness_pairing_error", 1.0) > 1e-8:
        raise AssertionError("dual MBR witness regression failed")
    if reductions.get("order_two_localization_ratio", 2.0) > 1 + 1e-9:
        raise AssertionError("order-two PRE/Q localization regression failed")
    if reductions.get("max_point_mass_band_value_error", 1.0) > 1e-8:
        raise AssertionError("point-mass per-band guardrail regression failed")
    if not reductions.get("tail_check", {}).get("passes"):
        raise AssertionError("one-coordinate tuple-tail regression failed")
    source_like = [row for row in payload["profiles"] if row["kind"] == "source_like_subgroup_identity"]
    if len(source_like) != 10:
        raise AssertionError("source-like profile census changed")
    for row in payload["profiles"]:
        census = row.get("band_payment_census", {})
        if census.get("partitioned_nonzero_frequency_count") != row["parameters"][
            "frequency_count"
        ] - 1:
            raise AssertionError(f"band partition is incomplete for {row['name']}")
        if census.get("nonempty_complete_patterns", 0) <= 0:
            raise AssertionError(f"no complete band patterns for {row['name']}")
        for band in census.get("bands", []):
            if band["exact_density"] > band["moment_density_upper"] + 1e-10:
                raise AssertionError(f"moment band-density certificate failed for {row['name']}")
        for kind in ("exact", "moment_certified"):
            fractions = census["fractions_at_proxy_budget"][kind]
            if not all(0.0 <= value <= 1.0 for value in fractions.values()):
                raise AssertionError(f"invalid paid-pattern fraction for {row['name']}")
    source_exact_n2 = [
        row["band_payment_census"]["fractions_at_proxy_budget"]["exact"]["N2"]
        for row in source_like
    ]
    source_certified_n2 = [
        row["band_payment_census"]["fractions_at_proxy_budget"][
            "moment_certified"
        ]["N2"]
        for row in source_like
    ]
    if not (min(source_exact_n2) == 0.0 and max(source_exact_n2) == 1.0):
        raise AssertionError("exact N^2 band-payment diagnostic lost its range")
    if not (min(source_certified_n2) == 0.0 and max(source_certified_n2) > 0.5):
        raise AssertionError("moment-certified N^2 diagnostic lost its range")
    planted = profile_by_name(payload, "planted_pair_B4")
    if planted.get("source_scope") != "not_source_derived":
        raise AssertionError("planted regression lost its source-scope warning")
    if planted["sign_ablation"]["absolute_over_signed"] <= 500:
        raise AssertionError("planted sign-ablation regression was not reproduced")

    q90_shares = []
    for row in source_like:
        q90 = next(item for item in row["threshold_sweep"] if item["quantile"] == 0.90)
        q90_shares.append(q90["exceptional_positive_share"])
    if min(q90_shares) > 0.01 or max(q90_shares) < 0.95:
        raise AssertionError("single-frequency q90 threshold no longer shows nonuniform behavior")

    triple_rows = [row for row in source_like if "triple_census" in row]
    if len(triple_rows) != 3:
        raise AssertionError("expected three complete character-triple censuses")
    if not all(
        row["triple_census"]["product_high_positive_share"]
        > row["triple_census"]["any_high_positive_share"]
        for row in triple_rows
    ):
        raise AssertionError("matched-density tuple-product regression failed")
    rank_three = profile_by_name(payload, "sg17_n16_w3_m8")
    if rank_three["sign_ablation"]["absolute_over_signed"] <= 100:
        raise AssertionError("source-like sign-cancellation regression failed")

    for forbidden in (
        "dense low-tau top-order band restriction payment",
        "rooted band-to-cell inverse theorem",
        "primitive Q",
    ):
        if forbidden not in payload["claim_boundary"]["not_proved"]:
            raise AssertionError(f"missing nonclaim: {forbidden}")


def compare_payload(actual: Any, expected: Any, path: str = "payload") -> None:
    if isinstance(expected, dict):
        if not isinstance(actual, dict) or set(actual) != set(expected):
            raise AssertionError(f"mapping mismatch at {path}")
        for key in expected:
            if key == "payload_sha256":
                continue
            compare_payload(actual[key], expected[key], f"{path}.{key}")
        return
    if isinstance(expected, list):
        if not isinstance(actual, list) or len(actual) != len(expected):
            raise AssertionError(f"list mismatch at {path}")
        for index, (left, right) in enumerate(zip(actual, expected)):
            compare_payload(left, right, f"{path}[{index}]")
        return
    if isinstance(expected, float):
        if not isinstance(actual, (int, float)) or not math.isclose(
            float(actual), expected, rel_tol=2e-10, abs_tol=2e-10
        ):
            raise AssertionError(f"float mismatch at {path}: {actual!r} != {expected!r}")
        return
    if actual != expected:
        raise AssertionError(f"value mismatch at {path}: {actual!r} != {expected!r}")


def validate_note() -> None:
    text = NOTE.read_text(encoding="utf-8")
    required = [
        "Status: AUDIT / PROVED SPARSE-PATTERN AND TOP-ORDER REDUCTIONS / OPEN ROOTED DENSE-BAND BCI",
        "band-density restriction",
        "top-order restriction compiler",
        "Rooted band-to-cell inverse theorem (BCI)",
        "order-two dual witness localizes exactly to the PRE/Q endpoint",
        "per-band point-mass guardrail",
        "complete band patterns",
        "Theorem dependency table",
        "Paid-versus-dense pattern census",
        "The finite budgets `1`, `N`, and",
        "`N^2` are review diagnostics",
        "does not prove dense-band `(q-BR)`/rooted `(BCI)`",
        "PR #674",
    ]
    for marker in required:
        if marker not in text:
            raise AssertionError(f"note is missing required marker: {marker}")
    forbidden = [
        "MBR is proved",
        "primitive Q is proved by this note",
        "A4 is closed by this note",
    ]
    for marker in forbidden:
        if marker in text:
            raise AssertionError(f"note contains forbidden promotion: {marker}")


def print_summary(payload: dict[str, Any]) -> None:
    source_like = [row for row in payload["profiles"] if row["kind"] == "source_like_subgroup_identity"]
    q90 = [
        next(item for item in row["threshold_sweep"] if item["quantile"] == 0.90)[
            "exceptional_positive_share"
        ]
        for row in source_like
    ]
    triples = [row["triple_census"] for row in source_like if "triple_census" in row]
    exact_n2 = [
        row["band_payment_census"]["fractions_at_proxy_budget"]["exact"]["N2"]
        for row in source_like
    ]
    certified_n2 = [
        row["band_payment_census"]["fractions_at_proxy_budget"][
            "moment_certified"
        ]["N2"]
        for row in source_like
    ]
    print(f"profiles: {len(payload['profiles'])} (source-like: {len(source_like)}, planted: 1)")
    print(f"q90 positive-share range: {min(q90):.6f} .. {max(q90):.6f}")
    print(
        "matched-density tuple-product wins: "
        f"{sum(row['product_high_positive_share'] > row['any_high_positive_share'] for row in triples)}"
        f"/{len(triples)}"
    )
    print(
        "rank-3 absolute/signed ratio: "
        f"{profile_by_name(payload, 'sg17_n16_w3_m8')['sign_ablation']['absolute_over_signed']:.3f}"
    )
    print(
        "source-like N^2 proxy paid fraction (exact density): "
        f"{min(exact_n2):.3f} .. {max(exact_n2):.3f}"
    )
    print(
        "source-like N^2 proxy paid fraction (moment-certified): "
        f"{min(certified_n2):.3f} .. {max(certified_n2):.3f}"
    )
    print(f"payload_sha256: {payload['payload_sha256']}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="regenerate the JSON certificate")
    parser.add_argument("--check", action="store_true", help="recompute and compare the certificate")
    parser.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    expected = build_payload(verbose=args.verbose)
    validate_payload(expected)
    if args.write:
        CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE.write_text(json.dumps(expected, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {CERTIFICATE.relative_to(ROOT)}")
    if args.check:
        actual = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
        validate_payload(actual)
        compare_payload(actual, expected)
        validate_note()
        print("artifact replay: PASS")
    if args.tamper_selftest:
        tampered = json.loads(json.dumps(expected))
        profile_by_name(tampered, "sg17_n16_w3_m8")["sign_ablation"][
            "absolute_over_signed"
        ] = 1.0
        tampered["payload_sha256"] = payload_digest(tampered)
        try:
            validate_payload(tampered)
        except AssertionError:
            print("tamper self-test: PASS (sign-ablation mutation rejected)")
        else:
            raise AssertionError("tamper self-test failed")
    print_summary(expected)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
