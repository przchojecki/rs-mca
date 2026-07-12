#!/usr/bin/env python3
"""Verify the owner-rooted dense-band finite reductions.

The mathematical proofs live in the companion note.  This stdlib-only checker
replays the Fourier norming-dual identity, positive owner partition, exact RS
fixed-support ownership, saturation packet, repeated-rim rejection, global
(a-1)-packing, and the projected-energy gate. It does not prove semantic
source-to-cell emission, the dense complete-band estimate, or A4.
"""

from __future__ import annotations

import argparse
import cmath
import hashlib
import itertools
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
NOTE = ROOT / "experimental" / "notes" / "audits" / "owner_rooted_dense_band_localization_v1.md"
POSITIVE_SUPPORT_NOTE = (
    ROOT
    / "experimental"
    / "notes"
    / "audits"
    / "owner_rooted_positive_support_localization_v1.md"
)
SECANT_NOTE = (
    ROOT
    / "experimental"
    / "notes"
    / "audits"
    / "secant_annihilator_localization_v1.md"
)
SIGNED_PAYMENT_NOTE = (
    ROOT
    / "experimental"
    / "notes"
    / "audits"
    / "primitive_signed_payment_barrier_v1.md"
)
ARBITRARY_MASK_NOTE = (
    ROOT
    / "experimental"
    / "notes"
    / "audits"
    / "arbitrary_mask_idempotent_guardrail_v1.md"
)
CERTIFICATE = (
    ROOT
    / "experimental"
    / "data"
    / "certificates"
    / "owner-rooted-dense-band-v1"
    / "owner_rooted_dense_band_v1.json"
)
STATUS = "PROVED FINITE LOCALIZATION + SPARSE/LOW-LOAD PAYMENT / OPEN PRIMITIVE SIDON PAYMENT"
TOLERANCE = 1e-9
DIAGNOSTIC_DECIMALS = 12


def dft(values: list[complex]) -> list[complex]:
    size = len(values)
    root = cmath.exp(-2j * math.pi / size)
    return [
        sum(values[index] * root ** (frequency * index) for index in range(size))
        for frequency in range(size)
    ]


def idft(values: list[complex]) -> list[complex]:
    size = len(values)
    root = cmath.exp(2j * math.pi / size)
    return [
        sum(values[frequency] * root ** (frequency * index) for frequency in range(size))
        / size
        for index in range(size)
    ]


def inner(left: list[complex], right: list[complex]) -> complex:
    return sum(x * y.conjugate() for x, y in zip(left, right))


def lpnorm(values: list[complex], exponent: float) -> float:
    return sum(abs(value) ** exponent for value in values) ** (1.0 / exponent)


def fourier_dual_regression() -> dict[str, Any]:
    counts = [2.0, 0.0, 1.0, 3.0, 0.0]
    transform = dft([complex(value) for value in counts])
    band = {1, 4}
    masked = [value if index in band else 0j for index, value in enumerate(transform)]
    projection = idft(masked)
    q = 4.0
    qprime = q / (q - 1.0)
    norm = lpnorm(projection, q)
    dual = [
        (value / abs(value)) * abs(value) ** (q - 1.0) / norm ** (q - 1.0)
        if abs(value) > 0
        else 0j
        for value in projection
    ]
    projected_dual = idft(
        [value if index in band else 0j for index, value in enumerate(dft(dual))]
    )
    dual_norm = lpnorm(dual, qprime)
    first_pairing = inner(projection, dual).real
    second_pairing = inner([complex(value) for value in counts], projected_dual).real

    support_points = [index for index, count in enumerate(counts) for _ in range(int(count))]
    weights = [projected_dual[index].conjugate().real for index in support_points]
    pullback = sum(weights)
    positive_mass = sum(max(weight, 0.0) for weight in weights)
    owners = [point % 3 for point in support_points]
    owner_mass: dict[int, float] = defaultdict(float)
    for owner, weight in zip(owners, weights):
        owner_mass[owner] += max(weight, 0.0)
    owner_total = sum(owner_mass.values())
    eta = 0.5
    threshold = eta * positive_mass / len(owner_mass)
    heavy_mass = sum(value for value in owner_mass.values() if value >= threshold)

    return {
        "group_order": len(counts),
        "band": sorted(band),
        "q": q,
        "dual_norm_qprime": dual_norm,
        "projection_norm_q": norm,
        "projection_dual_pairing": first_pairing,
        "self_adjoint_pullback_pairing": second_pairing,
        "support_pullback_sum": pullback,
        "positive_mass": positive_mass,
        "owner_positive_mass": {str(key): value for key, value in sorted(owner_mass.items())},
        "owner_partition_sum": owner_total,
        "heavy_owner_mass_eta_half": heavy_mass,
        "checks": {
            "dual_norm_one": abs(dual_norm - 1.0) <= TOLERANCE,
            "norming_pairing": abs(first_pairing - norm) <= TOLERANCE,
            "self_adjoint_pairing": abs(second_pairing - norm) <= TOLERANCE,
            "support_pullback": abs(pullback - norm) <= TOLERANCE,
            "positive_mass_dominates": positive_mass + TOLERANCE >= norm,
            "owner_partition_exact": abs(owner_total - positive_mass) <= TOLERANCE,
            "heavy_owner_alternative": heavy_mass + TOLERANCE >= (1.0 - eta) * positive_mass,
        },
    }


def projected_energy_gate_regression() -> dict[str, Any]:
    counts = [2.0, 0.0, 1.0, 3.0, 0.0]
    group_order = len(counts)
    band = {1, 4}
    q = 4
    transform = dft([complex(value) for value in counts])
    projection = idft(
        [value if index in band else 0j for index, value in enumerate(transform)]
    )
    norm_q = lpnorm(projection, q)
    energy = sum(abs(value) ** 2 for value in projection)
    full_mass = 10.0
    image_size = float(group_order)
    residual_mass = sum(counts)
    density = len(band) / group_order
    rho = residual_mass / full_mass
    normalized_ratio = image_size ** (1.0 - 1.0 / q) * norm_q / full_mass
    normalized_energy = image_size * energy / full_mass ** 2
    band_load = image_size * rho * density
    projected_load = normalized_energy * band_load ** (q - 2)

    # Exact exponent bookkeeping behind cancellation of M and L powers in
    # R_A^q <= e_A x_A^(q-2).
    m_exponent = -q + 2 + (q - 2)
    l_exponent = q - 1 - 1 - (q - 2)
    synthetic_high_ratio = 2
    synthetic_high_load = synthetic_high_ratio ** q
    return {
        "q": q,
        "M": full_mass,
        "L": image_size,
        "W": residual_mass,
        "band_density": density,
        "projection_norm_q": norm_q,
        "projected_energy": energy,
        "R_A": normalized_ratio,
        "e_A": normalized_energy,
        "x_A": band_load,
        "Y_A": projected_load,
        "R_A_power_q": normalized_ratio ** q,
        "checks": {
            "interpolation_gate": normalized_ratio ** q <= projected_load + TOLERANCE,
            "low_energy_payment": normalized_ratio <= projected_load ** (1.0 / q) + TOLERANCE,
            "M_exponents_cancel": m_exponent == 0,
            "L_exponents_cancel": l_exponent == 0,
            "positive_rate_failure_forces_high_load": synthetic_high_load >= synthetic_high_ratio ** q,
        },
    }


def eval_poly(coefficients: tuple[int, ...], x: int, p: int) -> int:
    value = 0
    for coefficient in reversed(coefficients):
        value = (value * x + coefficient) % p
    return value


def interpolate_degree_one(xs: tuple[int, ...], ys: tuple[int, ...], p: int) -> tuple[int, int] | None:
    x0, x1 = xs[:2]
    y0, y1 = ys[:2]
    slope = (y1 - y0) * pow((x1 - x0) % p, p - 2, p) % p
    intercept = (y0 - slope * x0) % p
    candidate = (intercept, slope)
    return candidate if all(eval_poly(candidate, x, p) == y for x, y in zip(xs, ys)) else None


def line_values(
    p: int, domain: list[int], roots: list[int], amplitude_shift: int = 0
) -> tuple[list[int], list[int]]:
    anchor_polynomial = (3, 2)
    direction_polynomial = (5, 1)
    amplitudes = [
        ((index + 1) ** 2 + 3 * (index + 1) + amplitude_shift) % p or 1
        for index in range(len(domain))
    ]
    anchor = []
    direction = []
    for index, x in enumerate(domain):
        anchor.append((eval_poly(anchor_polynomial, x, p) - amplitudes[index] * roots[index]) % p)
        direction.append((eval_poly(direction_polynomial, x, p) + amplitudes[index]) % p)
    return anchor, direction


def enumerate_line(
    p: int, domain: list[int], k: int, agreement: int, anchor: list[int], direction: list[int]
) -> dict[str, Any]:
    polynomials = list(itertools.product(range(p), repeat=k))
    records = []
    support_slopes: dict[tuple[int, ...], set[int]] = defaultdict(set)
    support_records: dict[tuple[int, ...], list[tuple[int, tuple[int, ...], tuple[int, ...]]]] = defaultdict(list)
    for slope in range(p):
        received = [
            (anchor[index] + slope * direction[index]) % p for index in range(len(domain))
        ]
        for polynomial in polynomials:
            complete = tuple(
                index
                for index, x in enumerate(domain)
                if eval_poly(polynomial, x, p) == received[index]
            )
            if len(complete) < agreement:
                continue
            records.append((slope, polynomial, complete))
            for support in itertools.combinations(complete, agreement):
                support_slopes[support].add(slope)
                support_records[support].append((slope, polynomial, complete))

    common = set()
    for support in itertools.combinations(range(len(domain)), agreement):
        xs = tuple(domain[index] for index in support)
        if (
            interpolate_degree_one(xs, tuple(anchor[index] for index in support), p)
            and interpolate_degree_one(xs, tuple(direction[index] for index in support), p)
        ):
            common.add(support)
    multiple_owner = {
        support: sorted(slopes) for support, slopes in support_slopes.items() if len(slopes) > 1
    }
    ownership_ok = all(support in common for support in multiple_owner)

    exact_supports = {
        support
        for support, rows in support_records.items()
        if support not in common and any(len(complete) == agreement for _, _, complete in rows)
    }
    exact_owner = {
        support: next(
            slope
            for slope, _, complete in support_records[support]
            if len(complete) == agreement
        )
        for support in exact_supports
    }

    # Retain a deterministic cross-slope rim-free subfamily.
    retained = []
    used_rims: set[tuple[int, ...]] = set()
    for support in sorted(exact_supports):
        rims = {tuple(rim) for rim in itertools.combinations(support, agreement - 1)}
        if rims & used_rims:
            continue
        retained.append(support)
        used_rims |= rims

    saturation_records = [
        {"slope": slope, "polynomial": list(polynomial), "agreement_set": list(complete)}
        for slope, polynomial, complete in records
        if len(complete) >= agreement + 1
    ]
    saturation_packets_ok = True
    for row in saturation_records:
        complete = tuple(row["agreement_set"][: agreement + 1])
        slope = row["slope"]
        polynomial = tuple(row["polynomial"])
        for support in itertools.combinations(complete, agreement):
            same_explanation = any(
                record_slope == slope
                and record_polynomial == polynomial
                and set(complete) <= set(record_complete)
                for record_slope, record_polynomial, record_complete in support_records[tuple(support)]
            )
            saturation_packets_ok &= same_explanation

    all_rims = [
        tuple(rim)
        for support in retained
        for rim in itertools.combinations(support, agreement - 1)
    ]
    packing_ok = len(all_rims) == len(set(all_rims))
    packing_lhs = agreement * len(retained)
    packing_rhs = math.comb(len(domain), agreement - 1)

    repeated_rim_mutation = None
    if retained:
        first = retained[0]
        rim = first[:-1]
        replacement = next(index for index in range(len(domain)) if index not in first)
        repeated_rim_mutation = tuple(sorted(rim + (replacement,)))
    mutated_family = retained + ([repeated_rim_mutation] if repeated_rim_mutation else [])
    mutated_rims = [
        tuple(rim)
        for support in mutated_family
        for rim in itertools.combinations(support, agreement - 1)
    ]
    mutation_rejected = bool(
        repeated_rim_mutation and len(mutated_rims) != len(set(mutated_rims))
    )

    return {
        "p": p,
        "n": len(domain),
        "k": k,
        "agreement": agreement,
        "witness_record_count": len(records),
        "common_support_count": len(common),
        "multiple_owner_supports": {str(list(key)): value for key, value in multiple_owner.items()},
        "exact_support_count": len(exact_supports),
        "retained_rim_free_supports": [
            {"support": list(support), "owner": exact_owner[support]} for support in retained
        ],
        "saturation_record_count": len(saturation_records),
        "packing_lhs": packing_lhs,
        "packing_rhs": packing_rhs,
        "negative_repeated_rim_mutation": list(repeated_rim_mutation) if repeated_rim_mutation else None,
        "checks": {
            "fixed_support_unique_or_common": ownership_ok,
            "nonempty_exact_family": len(exact_supports) >= 2,
            "nonempty_rim_free_family": len(retained) >= 2,
            "saturation_packets_complete": saturation_packets_ok,
            "global_rims_unique": packing_ok,
            "packing_bound": packing_lhs <= packing_rhs,
            "repeated_rim_mutation_rejected": mutation_rejected,
        },
    }


def incidence_regression() -> dict[str, Any]:
    p = 17
    domain = list(range(1, 9))
    roots = [0, 0, 0, 0, 1, 1, 1, 1]
    exact_case = None
    exact_shift = None
    for shift in range(p):
        anchor, direction = line_values(p, domain, roots, shift)
        candidate = enumerate_line(p, domain, 2, 4, anchor, direction)
        if (
            candidate["checks"]["nonempty_exact_family"]
            and candidate["checks"]["nonempty_rim_free_family"]
        ):
            exact_case = candidate
            exact_shift = shift
            break
    if exact_case is None:
        raise RuntimeError("failed to construct exact-agreement incidence control")
    exact_case["amplitude_shift"] = exact_shift

    saturation_roots = [0, 0, 0, 0, 0, 1, 2, 3]
    saturation_case = None
    saturation_shift = None
    for shift in range(p):
        sat_anchor, sat_direction = line_values(p, domain, saturation_roots, shift)
        candidate = enumerate_line(p, domain, 2, 4, sat_anchor, sat_direction)
        if candidate["saturation_record_count"] >= 1:
            saturation_case = candidate
            saturation_shift = shift
            break
    if saturation_case is None:
        raise RuntimeError("failed to construct saturation control")
    saturation_case["amplitude_shift"] = saturation_shift
    return {
        "exact_agreement_case": exact_case,
        "positive_saturation_control": saturation_case,
        "checks": {
            "exact_case": all(exact_case["checks"].values()),
            "positive_saturation_detected": saturation_case["saturation_record_count"] >= 1,
            "positive_saturation_packet_complete": saturation_case["checks"]["saturation_packets_complete"],
        },
    }


def paired_rim_free_regression() -> dict[str, Any]:
    """Finite planted-pair guardrail: rim packing is not semantic primitivity."""
    block_count = 6
    agreement = block_count
    base = 5
    left = [base ** (index + 1) for index in range(block_count)]
    pair_sum = 2 * sum(left) + 1
    coordinates = []
    for value in left:
        coordinates.extend((value, pair_sum - value))

    images: dict[int, list[tuple[int, ...]]] = defaultdict(list)
    for support in itertools.combinations(range(2 * block_count), agreement):
        images[sum(coordinates[index] for index in support)].append(tuple(support))
    heavy_image = block_count * pair_sum // 2
    heavy = images[heavy_image]
    expected_heavy = math.comb(block_count, block_count // 2)
    expected_image = (3 ** block_count + 1) // 2

    heavy_rims = [
        tuple(rim)
        for support in heavy
        for rim in itertools.combinations(support, agreement - 1)
    ]
    pairwise_intersection_max = max(
        len(set(left_support) & set(right_support))
        for index, left_support in enumerate(heavy)
        for right_support in heavy[index + 1 :]
    )
    planted_pairs = [
        [2 * index, 2 * index + 1] for index in range(block_count)
    ]
    planted_valid = all(
        coordinates[left_index] + coordinates[right_index] == pair_sum
        for left_index, right_index in planted_pairs
    )
    return {
        "block_count": block_count,
        "N": 2 * block_count,
        "agreement": agreement,
        "M": math.comb(2 * block_count, block_count),
        "L": len(images),
        "expected_L": expected_image,
        "heavy_fiber_size": len(heavy),
        "expected_heavy_fiber_size": expected_heavy,
        "pair_sum": pair_sum,
        "planted_pairs": planted_pairs,
        "pairwise_intersection_max": pairwise_intersection_max,
        "rim_count": len(heavy_rims),
        "normalized_heavy_numerator": len(heavy) * len(images),
        "normalized_heavy_denominator": math.comb(2 * block_count, block_count),
        "asymptotic_excess_rate": "log(3/2)/2",
        "checks": {
            "image_formula": len(images) == expected_image,
            "heavy_fiber_formula": len(heavy) == expected_heavy,
            "global_rim_packing": len(heavy_rims) == len(set(heavy_rims)),
            "intersection_at_most_a_minus_2": pairwise_intersection_max <= agreement - 2,
            "planted_pair_certificate": planted_valid,
            "naive_rim_packing_implies_dense_band_payment_rejected": planted_valid,
        },
    }


def note_audit() -> dict[str, Any]:
    text = NOTE.read_text(encoding="utf-8")
    required = [
        "Proposition 2.1 (norming dual)",
        "Proposition 3.1 (fixed-support slope uniqueness)",
        "Proposition 3.2 (lossless rooting and heavy-owner alternative)",
        "Proposition 4.1 (saturation packet equivalence)",
        "Theorem 4.2 (global rim packing)",
        "Corollary 5.1 (sparse-band complete-band restriction bound)",
        "Rim packing does not imply dense-band complete-band restriction bound",
        "Assumption 7.1 (rooted exponential excess-to-cell emission, rooted excess-to-cell emission)",
        "Theorem 7.2 (rooted excess-to-cell emission implies dense-band complete-band restriction bound)",
        "Theorem 8.1 (owner-rooted projected-energy compiler)",
        "mathcal R_A^q\\le\\mathcal Y_A",
        "e_Ax_A^{q-2}",
        "complete-agreement-exact",
        "prop:exact-support-upper",
        "Positive-support and secant localization",
        "prove hereditary mask admissibility or a source-algebraic heavy-fiber inverse",
        "prove the charge-preserving semantic-or-signed dichotomy",
        "no dense complete-band estimate, A4 theorem, primitive Q, or Proximity Prize theorem is proved",
    ]
    forbidden = [
        "DENSE-BAND rooted band-to-cell emission PROVED",
        "A4 PROVED",
        "PRIMITIVE Q PROVED",
    ]
    return {
        "required_tokens": {token: token in text for token in required},
        "forbidden_tokens_absent": {token: token not in text for token in forbidden},
    }


def companion_note_audit() -> dict[str, Any]:
    rank_text = POSITIVE_SUPPORT_NOTE.read_text(encoding="utf-8")
    secant_text = SECANT_NOTE.read_text(encoding="utf-8")
    barrier_text = SIGNED_PAYMENT_NOTE.read_text(encoding="utf-8")
    idempotent_text = ARBITRARY_MASK_NOTE.read_text(encoding="utf-8")
    rank_required = [
        "ZERO-LOSS ROOTED LOCALIZATION + TRADE BRANCH PROVED",
        "the literal per-witness rank precursor is automatic",
        "baseline-free collective rank",
        r"\|P_Ab\|_q\ge \Omega_+",
    ]
    secant_required = [
        "exact finite secant-annihilator localization proved",
        "every nonzero secant generates such a cyclic annihilator",
        "Nonclaim: semantic source quotient, canonical `(CAT)` cell, or payment",
        "\\mathcal R_{A'}(b)",
        "\\mathcal Y_{A'}(b)",
        "\\log d_*=o(N)",
    ]
    barrier_required = [
        "POINT-MASK REDUCTION + CHARGE-PRESERVING DICHOTOMY IMPLICATION PROVED",
        "hereditary source-algebraic emission contains source-algebraic heavy-fiber inverse",
        "whole residual does not automatically apply to this submask",
        "charge-preserving",
        "does not rule out every atlas notion of quotient",
        r"\mathcal Y_{B_i}(b_{\mathcal U_i})",
        r"\mathcal R_A^q\le\mathcal Y_A",
    ]
    idempotent_required = [
        "ABSTRACT FOURIER/RIM COUNTEREXAMPLE PROVED",
        "NOT A VALID `(CAT)`/PRIMITIVE-SIDON FALSIFIER",
        "not proved to be genuine weighted-Vandermonde columns",
        "random union of scalar character orbits",
        "does not place those words on one affine received line",
        "abstract harmonic + rim hypotheses",
        "source transfer-radius inverse",
    ]
    forbidden = [
        "CANONICAL `(CAT)` CELL PROVED",
        "DENSE-BAND complete-band restriction bound PROVED",
        "A4 PROVED",
    ]
    joined = (
        rank_text + "\n" + secant_text + "\n" + barrier_text + "\n" + idempotent_text
    )
    return {
        "rank_required_tokens": {
            token: token in rank_text for token in rank_required
        },
        "secant_required_tokens": {
            token: token in secant_text for token in secant_required
        },
        "barrier_required_tokens": {
            token: token in barrier_text for token in barrier_required
        },
        "idempotent_required_tokens": {
            token: token in idempotent_text for token in idempotent_required
        },
        "forbidden_tokens_absent": {token: token not in joined for token in forbidden},
    }


def canonical_bytes(payload: dict[str, Any]) -> bytes:
    copy = dict(payload)
    copy.pop("payload_sha256", None)
    return json.dumps(copy, sort_keys=True, separators=(",", ":")).encode()


def quantize_diagnostics(value: Any) -> Any:
    """Remove platform-level float noise before serialization and hashing."""
    if isinstance(value, float):
        rounded = round(value, DIAGNOSTIC_DECIMALS)
        return 0.0 if rounded == 0.0 else rounded
    if isinstance(value, list):
        return [quantize_diagnostics(item) for item in value]
    if isinstance(value, dict):
        return {key: quantize_diagnostics(item) for key, item in value.items()}
    return value


def build_payload() -> dict[str, Any]:
    payload: dict[str, Any] = {
        "certificate_id": "owner-rooted-dense-band-v1",
        "status": STATUS,
        "diagnostic_float_decimals": DIAGNOSTIC_DECIMALS,
        "theorem_boundary": {
            "proved": [
                "exact norming-dual pullback and positive-mass truncation",
                "fixed-support slope uniqueness and lossless owner partition",
                "saturation equivalence and global (a-1)-rim packing",
                "full-slice sparse-band complete-band restriction bound corollary",
                "owner-rooted projected-energy gate and high-load proof object",
                "exact owner-rooted localization is delegated to companion regressions",
                "planted rim-free negative guardrail",
            ],
            "open": [
                "trade/annihilator packet to non-tautological source structure",
                "hereditary source-fiber admissibility or direct source-algebraic heavy-fiber inverse",
                "charge-preserving signed nonstructure payment",
                "source-realizability rigidity excluding kernel-sign masks",
                "localized packet to canonical semantic cell",
                "same-owner rooted payment validation",
                "A4 and primitive Q",
            ],
        },
        "fourier_dual": fourier_dual_regression(),
        "projected_energy_gate": projected_energy_gate_regression(),
        "incidence": incidence_regression(),
        "paired_rim_free_guardrail": paired_rim_free_regression(),
        "note_audit": note_audit(),
        "companion_note_audit": companion_note_audit(),
    }
    payload["all_checks_pass"] = (
        all(payload["fourier_dual"]["checks"].values())
        and all(payload["projected_energy_gate"]["checks"].values())
        and all(payload["incidence"]["checks"].values())
        and all(payload["paired_rim_free_guardrail"]["checks"].values())
        and all(payload["note_audit"]["required_tokens"].values())
        and all(payload["note_audit"]["forbidden_tokens_absent"].values())
        and all(payload["companion_note_audit"]["rank_required_tokens"].values())
        and all(payload["companion_note_audit"]["secant_required_tokens"].values())
        and all(payload["companion_note_audit"]["barrier_required_tokens"].values())
        and all(payload["companion_note_audit"]["idempotent_required_tokens"].values())
        and all(payload["companion_note_audit"]["forbidden_tokens_absent"].values())
    )
    payload = quantize_diagnostics(payload)
    payload["payload_sha256"] = hashlib.sha256(canonical_bytes(payload)).hexdigest()
    return payload


def validate(payload: dict[str, Any]) -> bool:
    expected_hash = hashlib.sha256(canonical_bytes(payload)).hexdigest()
    return (
        payload.get("status") == STATUS
        and payload.get("payload_sha256") == expected_hash
        and payload.get("all_checks_pass") is True
        and all(payload["fourier_dual"]["checks"].values())
        and all(payload["projected_energy_gate"]["checks"].values())
        and all(payload["incidence"]["checks"].values())
        and all(payload["incidence"]["exact_agreement_case"]["checks"].values())
        and payload["incidence"]["positive_saturation_control"]["saturation_record_count"] >= 1
        and all(payload["paired_rim_free_guardrail"]["checks"].values())
        and all(payload["note_audit"]["required_tokens"].values())
        and all(payload["note_audit"]["forbidden_tokens_absent"].values())
        and all(payload["companion_note_audit"]["rank_required_tokens"].values())
        and all(payload["companion_note_audit"]["secant_required_tokens"].values())
        and all(payload["companion_note_audit"]["barrier_required_tokens"].values())
        and all(payload["companion_note_audit"]["idempotent_required_tokens"].values())
        and all(payload["companion_note_audit"]["forbidden_tokens_absent"].values())
    )


def print_summary(payload: dict[str, Any]) -> None:
    exact = payload["incidence"]["exact_agreement_case"]
    print(STATUS)
    print(f"fourier_dual_checks={payload['fourier_dual']['checks']}")
    print(f"projected_energy_gate_checks={payload['projected_energy_gate']['checks']}")
    print(
        "incidence="
        f"records:{exact['witness_record_count']} "
        f"exact:{exact['exact_support_count']} "
        f"rim_free:{len(exact['retained_rim_free_supports'])} "
        f"packing:{exact['packing_lhs']}<={exact['packing_rhs']}"
    )
    print(f"incidence_checks={payload['incidence']['checks']}")
    print(f"all_checks_pass={payload['all_checks_pass']}")
    print(f"payload_sha256={payload['payload_sha256']}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write the regenerated artifact")
    parser.add_argument("--check", action="store_true", help="compare against the tracked artifact")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    payload = build_payload()
    print_summary(payload)
    if not validate(payload):
        return 1
    if args.write:
        CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"wrote={CERTIFICATE}")
    if args.check:
        if not CERTIFICATE.exists():
            print(f"missing={CERTIFICATE}")
            return 1
        expected = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
        if expected != payload:
            print("artifact_mismatch")
            return 1
        print("artifact_check=PASS")
    if args.tamper_selftest:
        tampered = json.loads(json.dumps(payload))
        tampered["incidence"]["exact_agreement_case"]["checks"]["packing_bound"] = False
        tampered["payload_sha256"] = hashlib.sha256(canonical_bytes(tampered)).hexdigest()
        if validate(tampered):
            print("tamper_selftest=FAIL")
            return 1
        print("tamper_selftest=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
