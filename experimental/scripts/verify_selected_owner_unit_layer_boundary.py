#!/usr/bin/env python3
"""Verify finite regressions for the selected-owner unit-layer boundary.

The script checks finite identities and guardrails.  It does not prove the
asymptotic selected-owner source inverse (SULSI).
"""

from __future__ import annotations

import argparse
import cmath
import itertools
import json
import math
import random
from pathlib import Path
from typing import Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE = (
    ROOT
    / "experimental"
    / "data"
    / "certificates"
    / "selected-owner-unit-layer-boundary"
    / "selected_owner_unit_layer_boundary.json"
)
TOL = 1.0e-9


def lp(values: Iterable[complex], exponent: int) -> float:
    return sum(abs(value) ** exponent for value in values) ** (1.0 / exponent)


def dft(values: Sequence[complex]) -> list[complex]:
    size = len(values)
    return [
        sum(
            values[position]
            * cmath.exp(-2j * math.pi * frequency * position / size)
            for position in range(size)
        )
        for frequency in range(size)
    ]


def idft(values: Sequence[complex]) -> list[complex]:
    size = len(values)
    return [
        sum(
            values[frequency]
            * cmath.exp(2j * math.pi * frequency * position / size)
            for frequency in range(size)
        )
        / size
        for position in range(size)
    ]


def cyclic_project(values: Sequence[complex], band: set[int]) -> list[complex]:
    transform = dft(values)
    return idft(
        [value if frequency in band else 0j for frequency, value in enumerate(transform)]
    )


def norming_dual(projected: Sequence[complex], exponent: int) -> list[complex]:
    norm = lp(projected, exponent)
    if norm <= TOL:
        return [0j for _ in projected]
    return [
        abs(value) ** (exponent - 2) * value / norm ** (exponent - 1)
        if abs(value) > TOL
        else 0j
        for value in projected
    ]


def charge_identity_regression() -> dict[str, Any]:
    counts = [0, 3, 1, 0, 2, 0, 1, 0, 0, 2, 0, 1, 0]
    band = {1, 2, 11, 12}
    exponent = 4
    projected = cyclic_project([complex(value) for value in counts], band)
    dual = norming_dual(projected, exponent)
    projected_dual = cyclic_project(dual, band)
    weights = [max(value.conjugate().real, 0.0) for value in projected_dual]
    positive_counts = [count if weights[index] > TOL else 0 for index, count in enumerate(counts)]
    layer_count = max(positive_counts)
    layers = [
        [1 if count >= layer else 0 for count in positive_counts]
        for layer in range(1, layer_count + 1)
    ]
    charges = []
    pairing_errors = []
    norm_slacks = []
    for layer in layers:
        charge = sum(layer[index] * weights[index] for index in range(len(layer)))
        projected_layer = cyclic_project([complex(value) for value in layer], band)
        pairing = sum(
            projected_layer[index] * dual[index].conjugate()
            for index in range(len(layer))
        ).real
        charges.append(charge)
        pairing_errors.append(abs(charge - pairing))
        norm_slacks.append(lp(projected_layer, exponent) - charge)
    rooted_mass = sum(
        positive_counts[index] * weights[index] for index in range(len(counts))
    )
    reconstructed = [sum(layer[index] for layer in layers) for index in range(len(counts))]
    return {
        "group_order": len(counts),
        "band": sorted(band),
        "q": exponent,
        "layer_count": layer_count,
        "charges": charges,
        "rooted_mass": rooted_mass,
        "charge_sum": sum(charges),
        "max_pairing_error": max(pairing_errors, default=0.0),
        "min_norm_slack": min(norm_slacks, default=0.0),
        "checks": {
            "layer_reconstruction": reconstructed == positive_counts,
            "charge_sum_exact": abs(sum(charges) - rooted_mass) <= TOL,
            "charge_pairing_exact": max(pairing_errors, default=0.0) <= TOL,
            "charge_below_q_norm": min(norm_slacks, default=0.0) >= -TOL,
        },
    }


def universal_bound_regression() -> dict[str, Any]:
    order = 7
    symmetric_pairs = ((1, 6), (2, 5), (3, 4))
    bands = []
    for selector in range(1, 1 << len(symmetric_pairs)):
        bands.append(
            {
                character
                for index, pair in enumerate(symmetric_pairs)
                if selector & (1 << index)
                for character in pair
            }
        )
    maximum_ratio = 0.0
    checks = 0
    for band in bands:
        density = len(band) / order
        for mask_bits in range(1 << order):
            mask = [complex((mask_bits >> index) & 1) for index in range(order)]
            support_size = sum(int(value.real) for value in mask)
            for exponent in (2, 3, 4, 6):
                projected = cyclic_project(mask, band)
                lhs = order ** (-1.0 / exponent) * lp(projected, exponent)
                rhs = (order * density) ** (0.5 - 1.0 / exponent)
                maximum_ratio = max(maximum_ratio, lhs / max(rhs, TOL))
                if lhs > rhs + TOL:
                    raise AssertionError("universal unit-mask estimate failed")
                if support_size <= order and lp(projected, 2) > math.sqrt(order) + TOL:
                    raise AssertionError("projection contraction failed")
                checks += 1
    return {
        "group_order": order,
        "bands": len(bands),
        "masks": 1 << order,
        "q_values": [2, 3, 4, 6],
        "checks_run": checks,
        "maximum_ratio_to_bound": maximum_ratio,
        "checks": {"universal_bound": maximum_ratio <= 1.0 + TOL},
    }


def vector_elements(prime: int, dimension: int) -> list[tuple[int, ...]]:
    return list(itertools.product(range(prime), repeat=dimension))


def vector_character(
    frequency: tuple[int, ...], value: tuple[int, ...], prime: int
) -> complex:
    dot = sum(left * right for left, right in zip(frequency, value)) % prime
    return cmath.exp(2j * math.pi * dot / prime)


def vector_project(
    values: Sequence[complex],
    band_indices: set[int],
    elements: Sequence[tuple[int, ...]],
    prime: int,
) -> list[complex]:
    size = len(elements)
    hats = {}
    for frequency_index in band_indices:
        frequency = elements[frequency_index]
        hats[frequency_index] = sum(
            values[position] * vector_character(frequency, value, prime).conjugate()
            for position, value in enumerate(elements)
        )
    return [
        sum(
            hats[frequency_index]
            * vector_character(elements[frequency_index], value, prime)
            for frequency_index in band_indices
        )
        / size
        for value in elements
    ]


def scalar_orbits(
    elements: Sequence[tuple[int, ...]], prime: int
) -> list[tuple[int, ...]]:
    index = {value: position for position, value in enumerate(elements)}
    unseen = set(range(1, len(elements)))
    result = []
    while unseen:
        representative = elements[min(unseen)]
        orbit = tuple(
            sorted(
                index[tuple((scalar * coordinate) % prime for coordinate in representative)]
                for scalar in range(1, prime)
            )
        )
        result.append(orbit)
        unseen.difference_update(orbit)
    return result


def positive_rooted_obstruction_regression() -> dict[str, Any]:
    prime = 3
    dimension = 2
    elements = vector_elements(prime, dimension)
    orbits = scalar_orbits(elements, prime)
    exponent = 4
    best: dict[str, Any] | None = None
    for orbit_bits in range(1, 1 << len(orbits)):
        selected_orbits = [
            orbit for index, orbit in enumerate(orbits) if orbit_bits & (1 << index)
        ]
        band = {frequency for orbit in selected_orbits for frequency in orbit}
        density = len(band) / len(elements)
        if not 0.2 <= density <= 0.8:
            continue
        maximum = -1.0
        maximizing_mask = None
        maximizing_projection = None
        for mask_bits in range(1 << len(elements)):
            mask = [complex((mask_bits >> index) & 1) for index in range(len(elements))]
            projected = vector_project(mask, band, elements, prime)
            norm = lp(projected, exponent)
            if norm > maximum + TOL:
                maximum = norm
                maximizing_mask = mask
                maximizing_projection = projected
        assert maximizing_mask is not None and maximizing_projection is not None
        dual = norming_dual(maximizing_projection, exponent)
        projected_dual = vector_project(dual, band, elements, prime)
        positive_mask = [
            complex(1 if maximizing_mask[index].real and projected_dual[index].conjugate().real > TOL else 0)
            for index in range(len(elements))
        ]
        positive_projection = vector_project(positive_mask, band, elements, prime)
        positive_norm = lp(positive_projection, exponent)
        normalized = len(elements) ** (-1.0 / exponent) * positive_norm
        candidate = {
            "band": sorted(band),
            "density": density,
            "maximizing_support": [
                index for index, value in enumerate(maximizing_mask) if value.real
            ],
            "positive_support": [
                index for index, value in enumerate(positive_mask) if value.real
            ],
            "maximizer_norm": maximum,
            "positive_norm": positive_norm,
            "normalized_positive_load": normalized,
            "positive_packet_retains_norm": positive_norm + TOL >= maximum,
        }
        if best is None or candidate["normalized_positive_load"] > best["normalized_positive_load"]:
            best = candidate
    assert best is not None
    return {
        "group": "F_3^2",
        "group_order": len(elements),
        "scalar_orbits": [list(orbit) for orbit in orbits],
        "q": exponent,
        **best,
        "checks": {
            "dense_scalar_complete_band": 0.2 <= best["density"] <= 0.8,
            "positive_packet_is_unit_mask": True,
            "positive_packet_retains_norm": best["positive_packet_retains_norm"],
        },
    }


def lagrange_value(
    xs: Sequence[int], ys: Sequence[int], target: int, prime: int
) -> int:
    total = 0
    for index, x_value in enumerate(xs):
        numerator = 1
        denominator = 1
        for other_index, other_x in enumerate(xs):
            if other_index == index:
                continue
            numerator = numerator * (target - other_x) % prime
            denominator = denominator * (x_value - other_x) % prime
        total += ys[index] * numerator * pow(denominator % prime, prime - 2, prime)
    return total % prime


def leading_functional(
    domain: Sequence[int], support: Sequence[int], word: Sequence[int], prime: int
) -> int:
    total = 0
    for position in support:
        derivative = 1
        for other in support:
            if other != position:
                derivative = derivative * (domain[position] - domain[other]) % prime
        total += word[position] * pow(derivative, prime - 2, prime)
    return total % prime


def generic_line_decoration_regression() -> dict[str, Any]:
    prime = 101
    domain = (0, 1, 2, 3, 4, 5)
    supports = ((0, 1, 2), (0, 3, 4), (1, 3, 5), (2, 4, 5))
    rng = random.Random(20260713)
    selected = None
    for trial in range(1, 200_001):
        anchor = tuple(rng.randrange(prime) for _ in domain)
        direction = tuple(rng.randrange(prime) for _ in domain)
        records = []
        slopes = set()
        valid = True
        for support in supports:
            denominator = leading_functional(domain, support, direction, prime)
            if denominator == 0:
                valid = False
                break
            slope = -leading_functional(domain, support, anchor, prime) * pow(
                denominator, prime - 2, prime
            ) % prime
            if slope in slopes:
                valid = False
                break
            slopes.add(slope)
            received = tuple(
                (anchor[index] + slope * direction[index]) % prime
                for index in range(len(domain))
            )
            xs = tuple(domain[index] for index in support[:-1])
            ys = tuple(received[index] for index in support[:-1])
            agreement = tuple(
                index
                for index, point in enumerate(domain)
                if lagrange_value(xs, ys, point, prime) == received[index]
            )
            if agreement != support:
                valid = False
                break
            records.append({"support": list(support), "slope": slope})
        if valid:
            selected = {
                "trial": trial,
                "field": f"F_{prime}",
                "domain": list(domain),
                "anchor": list(anchor),
                "direction": list(direction),
                "records": records,
            }
            break
    if selected is None:
        raise AssertionError("failed to find generic line decoration regression")
    return {
        **selected,
        "claim_scope": "exact decorated witnesses with distinct owners; not semantic survival",
        "checks": {
            "all_supports_decorated": len(selected["records"]) == len(supports),
            "owners_distinct": len({record["slope"] for record in selected["records"]})
            == len(supports),
        },
    }


def owner_order_regression() -> dict[str, Any]:
    records = {
        2: [("S20", 3), ("S21", 8)],
        5: [("S50", 1)],
    }
    forward_layers = [
        [(syndrome, rows[layer]) for syndrome, rows in records.items() if len(rows) > layer]
        for layer in range(2)
    ]
    reversed_records = {syndrome: list(reversed(rows)) for syndrome, rows in records.items()}
    reverse_layers = [
        [
            (syndrome, rows[layer])
            for syndrome, rows in reversed_records.items()
            if len(rows) > layer
        ]
        for layer in range(2)
    ]
    forward_masks = [sorted(syndrome for syndrome, _ in layer) for layer in forward_layers]
    reverse_masks = [sorted(syndrome for syndrome, _ in layer) for layer in reverse_layers]
    return {
        "forward_layers": forward_layers,
        "reverse_layers": reverse_layers,
        "forward_masks": forward_masks,
        "reverse_masks": reverse_masks,
        "checks": {
            "syndrome_masks_invariant": forward_masks == reverse_masks,
            "attached_owners_change": forward_layers != reverse_layers,
        },
    }


def quantize(value: Any) -> Any:
    if isinstance(value, float):
        return round(value, 12)
    if isinstance(value, dict):
        return {key: quantize(item) for key, item in value.items()}
    if isinstance(value, list):
        return [quantize(item) for item in value]
    if isinstance(value, tuple):
        return [quantize(item) for item in value]
    return value


def build_payload() -> dict[str, Any]:
    payload = {
        "certificate_id": "selected-owner-unit-layer-boundary-v1",
        "source_revision": "9262f63cf093a7510a2df435f220390f59e2bcd5",
        "status": "PROVED_FINITE_IDENTITIES_AND_SOURCE_FREE_GUARDRAIL__SULSI_OPEN",
        "charge_identity": charge_identity_regression(),
        "universal_bound": universal_bound_regression(),
        "positive_rooted_obstruction": positive_rooted_obstruction_regression(),
        "generic_line_decoration": generic_line_decoration_regression(),
        "owner_order": owner_order_regression(),
        "nonclaims": [
            "no dense-band selected-owner source inverse is proved",
            "generic line decoration does not imply semantic first-match survival",
            "finite regressions do not prove an asymptotic Fourier estimate",
        ],
    }
    return quantize(payload)


def validate(payload: dict[str, Any]) -> bool:
    blocks = (
        "charge_identity",
        "universal_bound",
        "positive_rooted_obstruction",
        "generic_line_decoration",
        "owner_order",
    )
    return all(all(payload[block]["checks"].values()) for block in blocks)


def print_summary(payload: dict[str, Any]) -> None:
    print("SELECTED-OWNER UNIT-LAYER BOUNDARY")
    print(f"status                         = {payload['status']}")
    print(
        "charge max pairing error       = "
        f"{payload['charge_identity']['max_pairing_error']:.3e}"
    )
    print(
        "universal checks               = "
        f"{payload['universal_bound']['checks_run']}"
    )
    print(
        "finite rooted normalized load  = "
        f"{payload['positive_rooted_obstruction']['normalized_positive_load']:.6f}"
    )
    print(
        "generic decoration trial       = "
        f"{payload['generic_line_decoration']['trial']}"
    )
    print(f"RESULT                         = {'PASS' if validate(payload) else 'FAIL'}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    expected = build_payload()
    if args.tamper_selftest:
        tampered = json.loads(json.dumps(expected))
        tampered["owner_order"]["checks"]["attached_owners_change"] = False
        if validate(tampered):
            raise SystemExit("tamper self-test failed")
        print("TAMPER SELF-TEST: PASS")
        return 0
    if args.write:
        CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE.write_text(
            json.dumps(expected, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    if args.check:
        actual = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
        if actual != expected:
            raise SystemExit("certificate mismatch")
    print_summary(expected)
    if not validate(expected):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
