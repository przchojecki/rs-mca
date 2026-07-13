#!/usr/bin/env python3
"""Census slope-faithful multiplicity layers on finite RS received lines.

This is an experiment, not a proof of the dense-band payment.  It compares
the actual whole-slope witness residual with the unit-multiplicity
lexicographic surrogate.  The census keeps the received line, exact
agreement polynomial, support, and unique owner slope attached to every
retained record.

For each complete dyadic |tau|-band it computes:

* the image-normalized q-restriction load R_A;
* the exact norming dual and its positive-support packet;
* the projected-energy load;
* the owner-labelled unit-layer decomposition of the positive packet;
* the universal unit-mask bound for each layer; and
* rooted same-syndrome trades carried by multiplicity greater than one.

The output is deterministic.  The checked-in certificate retains aggregates,
per-regime extrema, and quantized SHA-256 commitments to every omitted line,
analysis, and control row.  ``--check`` recomputes the full census.  Floating-
point values are diagnostics only; semantic checks use exact finite-field and
integer data.
"""

from __future__ import annotations

import argparse
import cmath
import hashlib
import itertools
import json
import math
import random
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = (
    ROOT
    / "experimental"
    / "data"
    / "certificates"
    / "slope-faithful-multiplicity-census-v1"
    / "slope_faithful_multiplicity_census_v1.json"
)
TOL = 1.0e-9
FLOAT_DIGITS = 12


def stable_value(value):
    """Quantize diagnostics before hashing or writing portable JSON."""
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("non-finite diagnostic")
        return float(format(value, f".{FLOAT_DIGITS}g"))
    if isinstance(value, dict):
        return {str(key): stable_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [stable_value(item) for item in value]
    return value


def update_digest(digest, value) -> None:
    encoded = json.dumps(
        stable_value(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("ascii")
    digest.update(encoded)
    digest.update(b"\n")


def digest_values(values: Iterable[dict]) -> str:
    digest = hashlib.sha256()
    for value in values:
        update_digest(digest, value)
    return digest.hexdigest()


@dataclass(frozen=True)
class LineConfig:
    label: str
    prime: int
    domain: tuple[int, ...]
    dimension: int
    agreement: int
    samples: int


@dataclass(frozen=True)
class Witness:
    support: tuple[int, ...]
    owner: int
    polynomial: tuple[int, ...]


def eval_poly(coefficients: Sequence[int], x: int, prime: int) -> int:
    value = 0
    for coefficient in reversed(coefficients):
        value = (value * x + coefficient) % prime
    return value


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


def project(values: Sequence[complex], band: set[int]) -> list[complex]:
    transform = dft(values)
    return idft(
        [value if frequency in band else 0j for frequency, value in enumerate(transform)]
    )


def norming_dual(projected: Sequence[complex], exponent: int) -> list[complex]:
    norm = lp(projected, exponent)
    if norm <= TOL:
        return [0j for _ in projected]
    return [
        (abs(value) ** (exponent - 2) * value) / (norm ** (exponent - 1))
        if abs(value) > TOL
        else 0j
        for value in projected
    ]


def enumerate_line(
    prime: int,
    domain: Sequence[int],
    dimension: int,
    agreement: int,
    anchor: Sequence[int],
    direction: Sequence[int],
) -> dict:
    """Enumerate exact witnesses and apply whole-slope saturation deletion."""

    polynomials = tuple(itertools.product(range(prime), repeat=dimension))
    exact_rows: list[Witness] = []
    saturated_slopes: set[int] = set()

    for owner in range(prime):
        received = [
            (anchor[index] + owner * direction[index]) % prime
            for index in range(len(domain))
        ]
        owner_rows: list[Witness] = []
        for polynomial in polynomials:
            complete = tuple(
                index
                for index, point in enumerate(domain)
                if eval_poly(polynomial, point, prime) == received[index]
            )
            if len(complete) > agreement:
                saturated_slopes.add(owner)
            elif len(complete) == agreement:
                owner_rows.append(Witness(complete, owner, tuple(polynomial)))
        exact_rows.extend(owner_rows)

    # Saturation is a whole-slope first-match cell: every exact witness at an
    # owner with a higher-agreement explanation is deleted.
    after_saturation = [row for row in exact_rows if row.owner not in saturated_slopes]
    support_owners: dict[tuple[int, ...], set[int]] = defaultdict(set)
    for row in after_saturation:
        support_owners[row.support].add(row.owner)
    common_supports = {
        support for support, owners in support_owners.items() if len(owners) > 1
    }

    retained_by_support: dict[tuple[int, ...], Witness] = {}
    for row in after_saturation:
        if row.support in common_supports:
            continue
        previous = retained_by_support.get(row.support)
        if previous is None:
            retained_by_support[row.support] = row
        elif previous.owner != row.owner:
            raise AssertionError("noncommon support acquired two owners")

    retained = tuple(sorted(retained_by_support.values(), key=lambda row: row.support))
    return {
        "retained": retained,
        "exact_before_first_match": len(exact_rows),
        "saturated_slopes": tuple(sorted(saturated_slopes)),
        "common_supports": tuple(sorted(common_supports)),
    }


def full_slice_data(
    prime: int, domain: Sequence[int], agreement: int, columns: Sequence[int]
) -> tuple[int, int, tuple[int, ...]]:
    supports = tuple(itertools.combinations(range(len(domain)), agreement))
    images = tuple(sum(columns[index] for index in support) % prime for support in supports)
    return len(supports), len(set(images)), images


def arbitrary_kernel_sign_control(
    images: Sequence[int],
    prime: int,
    band: set[int],
    exponent: int,
    ambient_mass: int,
    image_size: int,
) -> dict:
    """Apply the dense-idempotent sign mask to the actual full-slice fibers."""

    full_counts = Counter(images)
    kernel = idft([complex(1 if frequency in band else 0) for frequency in range(prime)])
    normalization = image_size ** (1.0 - 1.0 / exponent) / ambient_mass
    candidates = []
    for orientation in (1, -1):
        selected = [
            complex(
                full_counts.get(value, 0)
                if orientation * kernel[(-value) % prime].real > TOL
                else 0
            )
            for value in range(prime)
        ]
        projected = project(selected, band)
        candidates.append(
            (normalization * lp(projected, exponent), orientation, selected)
        )
    restriction, orientation, selected = max(candidates, key=lambda row: row[0])
    selected_counts = [int(value.real) for value in selected]
    unit_mask = [complex(1 if value > 0 else 0) for value in selected_counts]
    unit_transfer = lp(project(unit_mask, band), exponent) / (
        image_size ** (1.0 / exponent)
    )
    return {
        "band_size": len(band),
        "q": exponent,
        "R": restriction,
        "orientation": orientation,
        "selected_mass": sum(selected_counts),
        "selected_images": sum(value > 0 for value in selected_counts),
        "max_normalized_fiber": (
            max(selected_counts, default=0) * image_size / ambient_mass
        ),
        "kernel_l1": sum(abs(value) for value in kernel),
        "unit_mask_transfer_over_L_over_M": unit_transfer,
    }


def tau_bands(prime: int, columns: Sequence[int]) -> tuple[dict, ...]:
    buckets: dict[str, list[int]] = defaultdict(list)
    magnitudes: dict[int, float] = {}
    for character in range(1, prime):
        value = sum(
            cmath.exp(2j * math.pi * character * column / prime) for column in columns
        )
        magnitudes[character] = abs(value)

    # Assign conjugate pairs together.  Their magnitudes are mathematically
    # equal, but independent floating evaluations can straddle a dyadic
    # boundary in the last bit.
    assigned: set[int] = set()
    for character in range(1, prime):
        if character in assigned:
            continue
        conjugate = (prime - character) % prime
        pair = (character, conjugate) if conjugate != character else (character,)
        magnitude = sum(magnitudes[member] for member in pair) / len(pair)
        if magnitude < TOL:
            label = "tau=0"
        elif magnitude < 1.0:
            label = "tau<1"
        else:
            label = f"2^{math.floor(math.log2(magnitude))}"
        buckets[label].extend(pair)
        assigned.update(pair)

    result = []
    for label, members in sorted(buckets.items()):
        band = set(members)
        if any((prime - character) % prime not in band for character in band):
            raise AssertionError("dyadic |tau| band is not symmetric")
        result.append(
            {
                "label": label,
                "members": tuple(members),
                "density": len(members) / prime,
                "tau_min": min(magnitudes[member] for member in members),
                "tau_max": max(magnitudes[member] for member in members),
            }
        )
    if sorted(member for band in result for member in band["members"]) != list(
        range(1, prime)
    ):
        raise AssertionError("bands do not partition the nonzero dual")
    return tuple(result)


def support_image(witness: Witness, columns: Sequence[int], prime: int) -> int:
    return sum(columns[index] for index in witness.support) % prime


def planted_pair_score(columns: Sequence[int], prime: int) -> dict:
    best_constant = None
    best_pairs: tuple[tuple[int, int], ...] = ()
    for constant in range(prime):
        used: set[int] = set()
        pairs = []
        for left in range(len(columns)):
            if left in used:
                continue
            for right in range(left + 1, len(columns)):
                if right in used:
                    continue
                if (columns[left] + columns[right]) % prime == constant:
                    pairs.append((left, right))
                    used.add(left)
                    used.add(right)
                    break
        if len(pairs) > len(best_pairs):
            best_constant = constant
            best_pairs = tuple(pairs)
    return {
        "constant": best_constant,
        "pair_count": len(best_pairs),
        "coverage": 2 * len(best_pairs) / len(columns),
        "pairs": [list(pair) for pair in best_pairs],
    }


def domain_quotients(columns: Sequence[int], prime: int) -> list[int]:
    column_set = set(columns)
    return [
        shift
        for shift in range(1, prime)
        if {(column + shift) % prime for column in columns} == column_set
    ]


def rim_collisions(witnesses: Sequence[Witness], agreement: int) -> dict:
    rims: dict[tuple[int, ...], list[int]] = defaultdict(list)
    for witness in witnesses:
        for rim in itertools.combinations(witness.support, agreement - 1):
            rims[tuple(rim)].append(witness.owner)
    repeated = {rim: owners for rim, owners in rims.items() if len(set(owners)) > 1}
    return {
        "count": len(repeated),
        "examples": [
            {"rim": list(rim), "owners": sorted(set(owners))}
            for rim, owners in list(sorted(repeated.items()))[:5]
        ],
    }


def trade_census(
    positive: Sequence[Witness], columns: Sequence[int], prime: int
) -> dict:
    by_image: dict[int, list[Witness]] = defaultdict(list)
    for witness in positive:
        by_image[support_image(witness, columns, prime)].append(witness)
    radius_counts: Counter[int] = Counter()
    owner_pair_counts: Counter[tuple[int, int]] = Counter()
    examples = []
    total = 0
    for image, rows in by_image.items():
        for left, right in itertools.combinations(rows, 2):
            left_only = tuple(sorted(set(left.support) - set(right.support)))
            right_only = tuple(sorted(set(right.support) - set(left.support)))
            if sum(columns[index] for index in left_only) % prime != sum(
                columns[index] for index in right_only
            ) % prime:
                raise AssertionError("same-syndrome pair failed exact trade identity")
            total += 1
            radius_counts[len(left_only)] += 1
            owner_pair_counts[tuple(sorted((left.owner, right.owner)))] += 1
            if len(examples) < 5:
                examples.append(
                    {
                        "image": image,
                        "left_support": list(left.support),
                        "right_support": list(right.support),
                        "owners": [left.owner, right.owner],
                        "radius": len(left_only),
                    }
                )
    return {
        "pair_count": total,
        "radius_counts": {str(key): value for key, value in sorted(radius_counts.items())},
        "distinct_owner_pairs": len(owner_pair_counts),
        "max_owner_pair_multiplicity": max(owner_pair_counts.values(), default=0),
        "examples": examples,
    }


def analyze_band(
    witnesses: Sequence[Witness],
    columns: Sequence[int],
    prime: int,
    ambient_mass: int,
    image_size: int,
    band_record: dict,
    exponent: int,
) -> dict | None:
    if not witnesses:
        return None
    band = set(band_record["members"])
    actual_counts = Counter(support_image(row, columns, prime) for row in witnesses)
    actual = [complex(actual_counts.get(value, 0)) for value in range(prime)]
    lex = [complex(1 if actual_counts.get(value, 0) else 0) for value in range(prime)]
    projected = project(actual, band)
    projected_lex = project(lex, band)
    norm = lp(projected, exponent)
    norm_lex = lp(projected_lex, exponent)
    normalization = image_size ** (1.0 - 1.0 / exponent) / ambient_mass
    restriction = normalization * norm
    lex_restriction = normalization * norm_lex

    dual = norming_dual(projected, exponent)
    projected_dual = project(dual, band)
    weights = [max(projected_dual[value].conjugate().real, 0.0) for value in range(prime)]
    positive = tuple(
        row
        for row in witnesses
        if weights[support_image(row, columns, prime)] > TOL
    )
    positive_counts = Counter(support_image(row, columns, prime) for row in positive)
    rooted_mass = sum(positive_counts[value] * weights[value] for value in range(prime))
    positive_vector = [complex(positive_counts.get(value, 0)) for value in range(prime)]
    projected_positive = project(positive_vector, band)
    positive_restriction = normalization * lp(projected_positive, exponent)

    layer_count = max(positive_counts.values(), default=0)
    layer_norms = []
    layer_charges = []
    owner_layers = []
    by_image: dict[int, list[Witness]] = defaultdict(list)
    for row in positive:
        by_image[support_image(row, columns, prime)].append(row)
    for rows in by_image.values():
        rows.sort(key=lambda row: (row.owner, row.support))
    for layer in range(1, layer_count + 1):
        mask = [complex(1 if positive_counts.get(value, 0) >= layer else 0) for value in range(prime)]
        layer_norms.append(lp(project(mask, band), exponent))
        layer_charges.append(
            sum(weights[value] for value in range(prime) if positive_counts.get(value, 0) >= layer)
        )
        owner_layers.append(
            [
                {
                    "image": image,
                    "support": list(rows[layer - 1].support),
                    "owner": rows[layer - 1].owner,
                }
                for image, rows in sorted(by_image.items())
                if len(rows) >= layer
            ]
        )

    density = len(band) / prime
    unit_bound = (image_size / ambient_mass) * (
        image_size * density
    ) ** (0.5 - 1.0 / exponent)
    layer_bound = layer_count * unit_bound
    layer_restrictions = [normalization * value for value in layer_norms]
    layer_sum = sum(layer_restrictions)
    unit_image_scale = image_size / ambient_mass
    max_layer_transfer = (
        max(layer_restrictions, default=0.0) / unit_image_scale
        if unit_image_scale > 0
        else 0.0
    )

    energy = lp(projected_positive, 2) ** 2
    residual_ratio = len(positive) / ambient_mass
    normalized_energy = image_size * energy / (ambient_mass**2)
    band_load = image_size * residual_ratio * density
    projected_load = normalized_energy * band_load ** (exponent - 2)

    # Exact checks are tolerant only where a finite Fourier calculation uses
    # floating arithmetic.
    if rooted_mass + 1.0e-7 < norm:
        raise AssertionError("positive rooting lost norming-dual mass")
    if positive_restriction + 1.0e-7 < restriction:
        raise AssertionError("positive packet lost normalized q-load")
    if abs(sum(layer_charges) - rooted_mass) > 1.0e-7:
        raise AssertionError("owner-labelled layers do not partition positive charge")
    if layer_sum + 1.0e-7 < positive_restriction:
        raise AssertionError("layer triangle bound failed")
    if positive_restriction > layer_bound + 1.0e-6:
        raise AssertionError("unit-layer universal bound failed")

    trades = trade_census(positive, columns, prime)
    return {
        "band": band_record["label"],
        "band_size": len(band),
        "band_density": density,
        "q": exponent,
        "actual_R": restriction,
        "lex_R": lex_restriction,
        "actual_to_lex_R": restriction / max(lex_restriction, TOL),
        "positive_R": positive_restriction,
        "positive_supports": len(positive),
        "positive_images": len(positive_counts),
        "rooted_mass": rooted_mass,
        "layer_count": layer_count,
        "layer_charge_sum": sum(layer_charges),
        "layer_triangle_R": layer_sum,
        "max_unit_layer_R": max(layer_restrictions, default=0.0),
        "max_unit_layer_transfer_over_L_over_M": max_layer_transfer,
        "unit_bound_per_layer": unit_bound,
        "unit_layer_bound_R": layer_bound,
        "unit_bound_slack": layer_bound / max(positive_restriction, TOL),
        "projected_energy": energy,
        "projected_load_Y": projected_load,
        "max_positive_fiber": max(positive_counts.values(), default=0),
        "trades": trades,
        "owner_layers": owner_layers,
    }


def analyze_line(
    label: str,
    prime: int,
    domain: Sequence[int],
    dimension: int,
    agreement: int,
    anchor: Sequence[int],
    direction: Sequence[int],
    exponents: Sequence[int],
    random_columns: Sequence[int] | None = None,
) -> dict:
    enumerated = enumerate_line(prime, domain, dimension, agreement, anchor, direction)
    witnesses: tuple[Witness, ...] = enumerated["retained"]
    column_models = [("moment", tuple(point % prime for point in domain))]
    if random_columns is not None:
        column_models.append(("permuted-control", tuple(random_columns)))

    analyses = []
    models = []
    for model, columns in column_models:
        ambient_mass, image_size, full_images = full_slice_data(
            prime, domain, agreement, columns
        )
        bands = tau_bands(prime, columns)
        model_rows = []
        arbitrary_controls = []
        for band in bands:
            for exponent in exponents:
                row = analyze_band(
                    witnesses,
                    columns,
                    prime,
                    ambient_mass,
                    image_size,
                    band,
                    exponent,
                )
                if row is not None:
                    row["model"] = model
                    model_rows.append(row)
                    analyses.append(row)
                control = arbitrary_kernel_sign_control(
                    full_images,
                    prime,
                    set(band["members"]),
                    exponent,
                    ambient_mass,
                    image_size,
                )
                control["band"] = band["label"]
                arbitrary_controls.append(control)
        models.append(
            {
                "model": model,
                "columns": list(columns),
                "M": ambient_mass,
                "L": image_size,
                "average_fiber": ambient_mass / image_size,
                "band_count": len(bands),
                "planted_pair": planted_pair_score(columns, prime),
                "domain_quotient_shifts": domain_quotients(columns, prime),
                "arbitrary_kernel_sign_controls": arbitrary_controls,
            }
        )

    return {
        "label": label,
        "prime": prime,
        "domain": list(domain),
        "dimension": dimension,
        "agreement": agreement,
        "anchor": list(anchor),
        "direction": list(direction),
        "exact_before_first_match": enumerated["exact_before_first_match"],
        "saturated_slopes": list(enumerated["saturated_slopes"]),
        "common_supports": [list(support) for support in enumerated["common_supports"]],
        "retained_supports": [
            {
                "support": list(row.support),
                "owner": row.owner,
                "polynomial": list(row.polynomial),
            }
            for row in witnesses
        ],
        "retained_count": len(witnesses),
        "retained_owner_count": len({row.owner for row in witnesses}),
        "rim_collisions": rim_collisions(witnesses, agreement),
        "models": models,
        "analyses": analyses,
    }


def known_regression(exponents: Sequence[int]) -> dict:
    # Review regression: two actual slopes survive at one moment syndrome,
    # whereas lexicographic unit-multiplicity deletion keeps only one support.
    return analyze_line(
        "known-F17-whole-slope-regression",
        17,
        (1, 2, 5, 8, 9),
        1,
        3,
        (15, 2, 15, 3, 15),
        (14, 15, 2, 14, 3),
        exponents,
        random_columns=(1, 4, 6, 10, 15),
    )


def constructed_regression(exponents: Sequence[int]) -> dict:
    prime = 17
    domain = tuple(range(1, 9))
    roots = (0, 0, 0, 0, 1, 1, 1, 1)
    anchor_polynomial = (3, 2)
    direction_polynomial = (5, 1)
    amplitudes = [((index + 1) ** 2 + 3 * (index + 1)) % prime or 1 for index in range(8)]
    anchor = tuple(
        (eval_poly(anchor_polynomial, point, prime) - amplitudes[index] * roots[index])
        % prime
        for index, point in enumerate(domain)
    )
    direction = tuple(
        (eval_poly(direction_polynomial, point, prime) + amplitudes[index]) % prime
        for index, point in enumerate(domain)
    )
    return analyze_line(
        "constructed-F17-two-root-line",
        prime,
        domain,
        2,
        4,
        anchor,
        direction,
        exponents,
        random_columns=(1, 2, 4, 7, 8, 11, 13, 16),
    )


def search_random_lines(configs: Sequence[LineConfig], seed: int, exponents: Sequence[int]) -> dict:
    rng = random.Random(seed)
    aggregate = {
        "lines": 0,
        "nonempty_lines": 0,
        "multi_owner_lines": 0,
        "analysis_rows": 0,
        "max_actual_R": 0.0,
        "max_actual_to_lex_R": 0.0,
        "max_layer_count": 0,
        "max_unit_bound_slack": 0.0,
        "rows_with_multiplicity": 0,
        "multiplicity_rows_with_rooted_trade": 0,
        "rows_with_rim_collision": 0,
        "rows_with_R_above_one": 0,
        "rows_with_R_above_half": 0,
        "min_unit_bound_slack": None,
        "max_layer_triangle_ratio": 0.0,
        "max_unit_layer_transfer_over_L_over_M": 0.0,
        "max_arbitrary_kernel_sign_R": 0.0,
        "max_arbitrary_unit_mask_transfer_over_L_over_M": 0.0,
    }
    grouped: dict[str, dict] = {}
    line_digest = hashlib.sha256()
    analysis_digest = hashlib.sha256()
    control_digest = hashlib.sha256()
    control_rows = 0

    for config in configs:
        for sample in range(config.samples):
            anchor = tuple(rng.randrange(config.prime) for _ in config.domain)
            direction = tuple(rng.randrange(config.prime) for _ in config.domain)
            random_columns = tuple(rng.sample(range(1, config.prime), len(config.domain)))
            line = analyze_line(
                f"{config.label}-{sample:05d}",
                config.prime,
                config.domain,
                config.dimension,
                config.agreement,
                anchor,
                direction,
                exponents,
                random_columns=random_columns,
            )
            aggregate["lines"] += 1
            update_digest(
                line_digest,
                {
                    "label": line["label"],
                    "prime": line["prime"],
                    "dimension": line["dimension"],
                    "agreement": line["agreement"],
                    "anchor": line["anchor"],
                    "direction": line["direction"],
                    "retained_count": line["retained_count"],
                    "retained_owner_count": line["retained_owner_count"],
                    "rim_collision_count": line["rim_collisions"]["count"],
                },
            )
            if not line["retained_count"]:
                continue
            aggregate["nonempty_lines"] += 1
            if line["retained_owner_count"] > 1:
                aggregate["multi_owner_lines"] += 1
            if line["rim_collisions"]["count"]:
                aggregate["rows_with_rim_collision"] += 1
            aggregate["max_arbitrary_kernel_sign_R"] = max(
                aggregate["max_arbitrary_kernel_sign_R"],
                max(
                    control["R"]
                    for model in line["models"]
                    for control in model["arbitrary_kernel_sign_controls"]
                ),
            )
            aggregate["max_arbitrary_unit_mask_transfer_over_L_over_M"] = max(
                aggregate["max_arbitrary_unit_mask_transfer_over_L_over_M"],
                max(
                    control["unit_mask_transfer_over_L_over_M"]
                    for model in line["models"]
                    for control in model["arbitrary_kernel_sign_controls"]
                ),
            )
            for model in line["models"]:
                for control in model["arbitrary_kernel_sign_controls"]:
                    control_rows += 1
                    update_digest(
                        control_digest,
                        {
                            "line": line["label"],
                            "config": config.label,
                            "model": model["model"],
                            **control,
                        },
                    )
            for row in line["analyses"]:
                aggregate["analysis_rows"] += 1
                aggregate["max_actual_R"] = max(aggregate["max_actual_R"], row["actual_R"])
                aggregate["max_actual_to_lex_R"] = max(
                    aggregate["max_actual_to_lex_R"], row["actual_to_lex_R"]
                )
                aggregate["max_layer_count"] = max(
                    aggregate["max_layer_count"], row["layer_count"]
                )
                aggregate["max_unit_bound_slack"] = max(
                    aggregate["max_unit_bound_slack"], row["unit_bound_slack"]
                )
                aggregate["min_unit_bound_slack"] = (
                    row["unit_bound_slack"]
                    if aggregate["min_unit_bound_slack"] is None
                    else min(aggregate["min_unit_bound_slack"], row["unit_bound_slack"])
                )
                aggregate["max_layer_triangle_ratio"] = max(
                    aggregate["max_layer_triangle_ratio"],
                    row["layer_triangle_R"] / max(row["positive_R"], TOL),
                )
                aggregate["max_unit_layer_transfer_over_L_over_M"] = max(
                    aggregate["max_unit_layer_transfer_over_L_over_M"],
                    row["max_unit_layer_transfer_over_L_over_M"],
                )
                aggregate["rows_with_R_above_one"] += int(row["actual_R"] > 1.0)
                aggregate["rows_with_R_above_half"] += int(row["actual_R"] > 0.5)
                if row["layer_count"] > 1:
                    aggregate["rows_with_multiplicity"] += 1
                    if row["trades"]["pair_count"]:
                        aggregate["multiplicity_rows_with_rooted_trade"] += 1
                group_key = f"{config.label}|{row['model']}|q={row['q']}"
                group = grouped.setdefault(
                    group_key,
                    {
                        "config": config.label,
                        "model": row["model"],
                        "q": row["q"],
                        "rows": 0,
                        "multiplicity_rows": 0,
                        "max_actual_R": 0.0,
                        "max_actual_to_lex_R": 0.0,
                        "max_layer_count": 0,
                        "min_unit_bound_slack": None,
                        "max_unit_bound_slack": 0.0,
                        "max_unit_layer_transfer_over_L_over_M": 0.0,
                    },
                )
                group["rows"] += 1
                group["multiplicity_rows"] += int(row["layer_count"] > 1)
                group["max_actual_R"] = max(group["max_actual_R"], row["actual_R"])
                group["max_actual_to_lex_R"] = max(
                    group["max_actual_to_lex_R"], row["actual_to_lex_R"]
                )
                group["max_layer_count"] = max(group["max_layer_count"], row["layer_count"])
                group["min_unit_bound_slack"] = (
                    row["unit_bound_slack"]
                    if group["min_unit_bound_slack"] is None
                    else min(group["min_unit_bound_slack"], row["unit_bound_slack"])
                )
                group["max_unit_bound_slack"] = max(
                    group["max_unit_bound_slack"], row["unit_bound_slack"]
                )
                group["max_unit_layer_transfer_over_L_over_M"] = max(
                    group["max_unit_layer_transfer_over_L_over_M"],
                    row["max_unit_layer_transfer_over_L_over_M"],
                )
                update_digest(
                    analysis_digest,
                    {
                        "line": line["label"],
                        "prime": line["prime"],
                        "dimension": line["dimension"],
                        "agreement": line["agreement"],
                        "retained_count": line["retained_count"],
                        "owner_count": line["retained_owner_count"],
                        "rim_collision_count": line["rim_collisions"]["count"],
                        **{key: value for key, value in row.items() if key != "owner_layers"},
                    },
                )
    return {
        "seed": seed,
        "configs": [asdict(config) for config in configs],
        "aggregate": aggregate,
        "grouped": [grouped[key] for key in sorted(grouped)],
        "row_streams": {
            "float_significant_digits": FLOAT_DIGITS,
            "line_rows": aggregate["lines"],
            "line_sha256": line_digest.hexdigest(),
            "analysis_rows": aggregate["analysis_rows"],
            "analysis_sha256": analysis_digest.hexdigest(),
            "arbitrary_control_rows": control_rows,
            "arbitrary_control_sha256": control_digest.hexdigest(),
        },
    }


def compact_control(line: dict) -> dict:
    moment_rows = [row for row in line["analyses"] if row["model"] == "moment"]
    return {
        "label": line["label"],
        "prime": line["prime"],
        "dimension": line["dimension"],
        "agreement": line["agreement"],
        "domain_size": len(line["domain"]),
        "exact_before_first_match": line["exact_before_first_match"],
        "saturated_slope_count": len(line["saturated_slopes"]),
        "common_support_count": len(line["common_supports"]),
        "retained_count": line["retained_count"],
        "retained_owner_count": line["retained_owner_count"],
        "rim_collision_count": line["rim_collisions"]["count"],
        "analysis_rows": len(line["analyses"]),
        "analysis_sha256": digest_values(line["analyses"]),
        "max_moment_layer_count": max(row["layer_count"] for row in moment_rows),
        "max_moment_actual_to_lex_R": max(
            row["actual_to_lex_R"] for row in moment_rows
        ),
        "max_moment_actual_R": max(row["actual_R"] for row in moment_rows),
    }


def build_payload(samples_scale: float) -> dict:
    exponents = (3, 4, 6)
    configs = (
        LineConfig("F7-k1-a3", 7, tuple(range(6)), 1, 3, max(1, int(2500 * samples_scale))),
        LineConfig("F11-k2-a4", 11, tuple(range(1, 8)), 2, 4, max(1, int(1800 * samples_scale))),
        LineConfig("F13-k2-a4", 13, tuple(range(1, 9)), 2, 4, max(1, int(1200 * samples_scale))),
        LineConfig("F11-H5-k1-a3", 11, (1, 3, 4, 5, 9), 1, 3, max(1, int(1600 * samples_scale))),
        LineConfig("F13-H6-k1-a3", 13, (1, 3, 4, 9, 10, 12), 1, 3, max(1, int(1400 * samples_scale))),
        LineConfig("F17-H8-k2-a4", 17, (1, 2, 4, 8, 9, 13, 15, 16), 2, 4, max(1, int(800 * samples_scale))),
        LineConfig("F19-H9-k2-a4", 19, (1, 4, 5, 6, 7, 9, 11, 16, 17), 2, 4, max(1, int(500 * samples_scale))),
    )
    full_controls = [known_regression(exponents), constructed_regression(exponents)]
    search = search_random_lines(configs, seed=20260713, exponents=exponents)

    known = full_controls[0]
    known_moment_rows = [row for row in known["analyses"] if row["model"] == "moment"]
    if known["retained_owner_count"] < 2:
        raise AssertionError("known whole-slope control lost an owner")
    if not any(row["layer_count"] >= 2 for row in known_moment_rows):
        raise AssertionError("known whole-slope control did not retain multiplicity")
    if not any(row["actual_to_lex_R"] > 1.0 + TOL for row in known_moment_rows):
        raise AssertionError("known whole-slope control did not separate from lex deletion")

    aggregate = search["aggregate"]
    if aggregate["rows_with_multiplicity"] != aggregate["multiplicity_rows_with_rooted_trade"]:
        raise AssertionError("a multiplicity layer failed to emit a rooted exact trade")

    payload = {
        "certificate_id": "slope-faithful-multiplicity-census-v1",
        "schema_version": 2,
        "status": "EXPERIMENTAL_CENSUS_NOT_A_PROOF",
        "source_revision": "9262f63cf093a7510a2df435f220390f59e2bcd5",
        "samples_scale": samples_scale,
        "retention": (
            "aggregate and per-regime summaries; omitted deterministic rows are "
            "committed by quantized SHA-256 streams"
        ),
        "semantics": {
            "residual": "exact agreement after whole-slope saturation deletion and common-support removal",
            "owner": "actual affine-line slope attached to the exact explaining polynomial",
            "profile": "unweighted depth-one Vandermonde moment sum on the full fixed-weight slice",
            "lex_control": "one support per realized residual syndrome; diagnostic only",
            "layering": "owner-labelled unit masks 1_{b(s)>=j} of the exact positive packet",
        },
        "controls": [compact_control(line) for line in full_controls],
        "random_search": search,
        "checks": {
            "known_control_retains_two_owners": known["retained_owner_count"] >= 2,
            "known_control_has_true_multiplicity": any(
                row["layer_count"] >= 2 for row in known_moment_rows
            ),
            "known_control_separates_from_lex": any(
                row["actual_to_lex_R"] > 1.0 + TOL for row in known_moment_rows
            ),
            "all_multiplicity_rows_emit_rooted_trade": (
                aggregate["rows_with_multiplicity"]
                == aggregate["multiplicity_rows_with_rooted_trade"]
            ),
        },
    }
    return stable_value(payload)


def print_summary(payload: dict) -> None:
    known = payload["controls"][0]
    search = payload["random_search"]["aggregate"]
    print("SLOPE-FAITHFUL MULTIPLICITY CENSUS")
    print(f"source revision                  = {payload['source_revision'][:12]}")
    print(f"known retained supports          = {known['retained_count']}")
    print(f"known retained owners            = {known['retained_owner_count']}")
    print(f"known maximum multiplicity       = {known['max_moment_layer_count']}")
    print(
        "known max actual/lex R ratio  = "
        f"{known['max_moment_actual_to_lex_R']:.6f}"
    )
    print(f"random lines                     = {search['lines']}")
    print(f"nonempty actual residuals        = {search['nonempty_lines']}")
    print(f"multi-owner residuals            = {search['multi_owner_lines']}")
    print(f"band/q rows                      = {search['analysis_rows']}")
    print(f"maximum actual R                = {search['max_actual_R']:.6f}")
    print(
        "maximum arbitrary-mask R        = "
        f"{search['max_arbitrary_kernel_sign_R']:.6f}"
    )
    print(
        "maximum arbitrary unit transfer = "
        f"{search['max_arbitrary_unit_mask_transfer_over_L_over_M']:.6f}"
    )
    print(f"maximum actual/lex R ratio      = {search['max_actual_to_lex_R']:.6f}")
    print(f"maximum positive multiplicity   = {search['max_layer_count']}")
    print(f"multiplicity rows               = {search['rows_with_multiplicity']}")
    print(
        "multiplicity rows with trade = "
        f"{search['multiplicity_rows_with_rooted_trade']}"
    )
    print(f"RESULT                           = PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--check",
        action="store_true",
        help="recompute the full census and compare its compact certificate",
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="run ten percent of the deterministic random census",
    )
    args = parser.parse_args()
    if args.check:
        payload = json.loads(args.output.read_text(encoding="utf-8"))
        expected = build_payload(float(payload.get("samples_scale", 1.0)))
        if payload != expected:
            raise SystemExit("certificate replay mismatch")
        if not all(payload.get("checks", {}).values()):
            raise SystemExit("certificate check failed")
        aggregate = payload["random_search"]["aggregate"]
        if (
            aggregate["rows_with_multiplicity"]
            != aggregate["multiplicity_rows_with_rooted_trade"]
        ):
            raise SystemExit("certificate multiplicity/trade check failed")
        print_summary(payload)
        print(f"certificate                       = {args.output}")
        return 0
    payload = build_payload(0.1 if args.quick else 1.0)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print_summary(payload)
    print(f"certificate                       = {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
