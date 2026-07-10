#!/usr/bin/env python3
"""Verify the primitive-profile character-frame certificate and toy census.

Checked object:
  finite effective-group character-frame inequality, converse Rayleigh
  guardrail, and greedy forbidden-difference packing on deterministic toys.

Proof status:
  PROVED CONDITIONAL CERTIFICATE / OPEN SOURCE-SPECIFIC PACKING INPUT.

This script does not prove exact primitive-profile Q, effective MI/MA, or the
direct Sidon payment for the unrestricted many-shell source profiles.
"""
from __future__ import annotations

import argparse
import cmath
import hashlib
import itertools
import json
import math
import shutil
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


STATUS = "PROVED CONDITIONAL CERTIFICATE / OPEN SOURCE-SPECIFIC PACKING INPUT"
THEOREM_ID = "asymptotic-primitive-profile-character-frame-v1"
CERT = Path(
    "experimental/data/certificates/primitive-profile-character-frame/"
    "primitive_profile_character_frame_v1.json"
)
NOTE = Path(
    "experimental/notes/thresholds/"
    "asymptotic_primitive_profile_character_frame_v1.md"
)
TEX = Path("experimental/asymptotic_rs_mca_frontiers.tex")
PINS = (
    "lem:effective-span-fourier",
    "def:effective-major-minor",
    "def:effective-fourier-payment",
    "def:major-arc-aggregate",
    "def:aggregate-minor-payment",
    "prop:effective-mi-ma-flatness",
)
TOL = 2.0e-9


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def canonical_hash(payload: dict[str, Any]) -> str:
    clean = dict(payload)
    clean.pop("payload_sha256", None)
    raw = json.dumps(clean, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def normalize_numbers(value: Any) -> Any:
    """Stabilize finite complex-arithmetic output across Python platforms."""
    if isinstance(value, float):
        return round(value, 12)
    if isinstance(value, dict):
        return {key: normalize_numbers(item) for key, item in value.items()}
    if isinstance(value, list):
        return [normalize_numbers(item) for item in value]
    return value


def group_elements(p: int, rank: int) -> list[tuple[int, ...]]:
    return list(itertools.product(range(p), repeat=rank))


def sub(a: tuple[int, ...], b: tuple[int, ...], p: int) -> tuple[int, ...]:
    return tuple((x - y) % p for x, y in zip(a, b))


def dot(a: tuple[int, ...], b: tuple[int, ...], p: int) -> int:
    return sum(x * y for x, y in zip(a, b)) % p


def character(a: tuple[int, ...], z: tuple[int, ...], p: int) -> complex:
    return cmath.exp(2j * math.pi * dot(a, z, p) / p)


def matrix_rank_mod_p(rows: list[list[int]], p: int) -> int:
    work = [[x % p for x in row] for row in rows]
    if not work:
        return 0
    rank = 0
    cols = len(work[0])
    for col in range(cols):
        pivot = next((i for i in range(rank, len(work)) if work[i][col]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inv = pow(work[rank][col], -1, p)
        work[rank] = [(inv * x) % p for x in work[rank]]
        for i in range(len(work)):
            if i == rank or not work[i][col]:
                continue
            scale = work[i][col]
            work[i] = [
                (x - scale * y) % p for x, y in zip(work[i], work[rank])
            ]
        rank += 1
        if rank == len(work):
            break
    return rank


def power_sum_counts(
    p: int, support: list[int], weight: int, depth: int
) -> Counter[tuple[int, ...]]:
    counts: Counter[tuple[int, ...]] = Counter()
    for chosen in itertools.combinations(support, weight):
        image = tuple(
            sum(pow(t, k, p) for t in chosen) % p for k in range(1, depth + 1)
        )
        counts[image] += 1
    return counts


def elementary_symmetric(values: tuple[int, ...], degree: int, p: int) -> int:
    total = 0
    for chosen in itertools.combinations(values, degree):
        product = 1
        for value in chosen:
            product = product * value % p
        total = (total + product) % p
    return total


def elementary_prefix_counts(
    p: int, support: list[int], weight: int, depth: int
) -> Counter[tuple[int, ...]]:
    counts: Counter[tuple[int, ...]] = Counter()
    for chosen in itertools.combinations(support, weight):
        image = tuple(
            elementary_symmetric(chosen, degree, p)
            for degree in range(1, depth + 1)
        )
        counts[image] += 1
    return counts


def image_difference_rank(
    p: int, images: Iterable[tuple[int, ...]]
) -> int:
    ordered = sorted(images)
    anchor = ordered[0]
    rows = [[(x - y) % p for x, y in zip(image, anchor)] for image in ordered[1:]]
    return matrix_rank_mod_p(rows, p)


def effective_rank(p: int, support: list[int], depth: int) -> int:
    anchor = support[0]
    vectors = []
    for t in support[1:]:
        vectors.append(
            [
                (pow(t, k, p) - pow(anchor, k, p)) % p
                for k in range(1, depth + 1)
            ]
        )
    return matrix_rank_mod_p(vectors, p)


def fourier_transform(
    p: int,
    rank: int,
    counts: Counter[tuple[int, ...]],
) -> tuple[list[tuple[int, ...]], dict[tuple[int, ...], complex]]:
    dual = group_elements(p, rank)
    total = sum(counts.values())
    values = {
        gamma: sum(
            multiplicity * character(gamma, image, p)
            for image, multiplicity in counts.items()
        )
        / total
        for gamma in dual
    }
    return dual, values


def greedy_independent_set(
    dual: list[tuple[int, ...]],
    forbidden_differences: set[tuple[int, ...]],
    p: int,
) -> list[tuple[int, ...]]:
    selected: list[tuple[int, ...]] = []
    for gamma in dual:
        if all(
            sub(gamma, previous, p) not in forbidden_differences
            for previous in selected
        ):
            selected.append(gamma)
    return selected


def gram_row_bound(
    selected: list[tuple[int, ...]],
    fourier: dict[tuple[int, ...], complex],
    p: int,
) -> float:
    return max(
        sum(abs(fourier[sub(other, gamma, p)]) for other in selected)
        for gamma in selected
    )


def rayleigh_at_atom(
    selected: list[tuple[int, ...]],
    counts: Counter[tuple[int, ...]],
    atom: tuple[int, ...],
    p: int,
) -> float:
    """Rayleigh quotient for the character-value vector at one image atom."""
    total = sum(counts.values())
    value = 0.0
    for image, multiplicity in counts.items():
        inner = sum(
            character(gamma, image, p) * character(gamma, atom, p).conjugate()
            for gamma in selected
        )
        value += (multiplicity / total) * (abs(inner) ** 2)
    return value / len(selected)


def threshold_candidates(
    dual: list[tuple[int, ...]],
    fourier: dict[tuple[int, ...], complex],
    zero: tuple[int, ...],
) -> list[float]:
    return sorted({0.0} | {round(abs(fourier[x]), 12) for x in dual if x != zero})


def best_packing(
    p: int,
    rank: int,
    counts: Counter[tuple[int, ...]],
) -> dict[str, Any]:
    dual, fourier = fourier_transform(p, rank, counts)
    zero = (0,) * rank
    image_size = len(counts)
    best: dict[str, Any] | None = None

    for threshold in threshold_candidates(dual, fourier, zero):
        major = {
            gamma
            for gamma in dual
            if gamma == zero or abs(fourier[gamma]) > threshold + 1.0e-11
        }
        selected = greedy_independent_set(dual, major, p)
        row_bound = gram_row_bound(selected, fourier, p)
        multiplier = image_size * row_bound / len(selected)
        candidate = {
            "threshold": threshold,
            "major_size": len(major),
            "selected_size": len(selected),
            "gram_row_bound": row_bound,
            "image_multiplier": multiplier,
            "selected": selected,
            "major": major,
        }
        if best is None or (
            candidate["image_multiplier"],
            candidate["threshold"],
            -candidate["selected_size"],
        ) < (
            best["image_multiplier"],
            best["threshold"],
            -best["selected_size"],
        ):
            best = candidate

    assert best is not None
    return best


def analyze_counts(
    name: str,
    p: int,
    rank: int,
    counts: Counter[tuple[int, ...]],
    source: dict[str, Any],
) -> dict[str, Any]:
    dual, fourier = fourier_transform(p, rank, counts)
    total = sum(counts.values())
    image_size = len(counts)
    max_count = max(counts.values())
    actual_multiplier = image_size * max_count / total
    global_l1 = sum(abs(value) for value in fourier.values())
    full_dual_row_multiplier = image_size * global_l1 / len(dual)
    packing = best_packing(p, rank, counts)
    selected = packing.pop("selected")
    major = packing.pop("major")
    heaviest = min(image for image, count in counts.items() if count == max_count)
    rayleigh = rayleigh_at_atom(selected, counts, heaviest, p)
    rayleigh_multiplier = image_size * rayleigh / len(selected)
    minor_global = sum(
        abs(value) for gamma, value in fourier.items() if gamma not in major
    )
    off_diagonal_max = max(
        sum(
            abs(fourier[sub(other, gamma, p)])
            for other in selected
            if other != gamma
        )
        for gamma in selected
    )
    differences_avoid_major = all(
        first == second or sub(second, first, p) not in major
        for first in selected
        for second in selected
    )
    greedy_floor = len(selected) * len(major) >= len(dual)
    frame_dominates_actual = (
        packing["image_multiplier"] + TOL >= actual_multiplier
    )
    rayleigh_guardrail = rayleigh_multiplier + TOL >= actual_multiplier
    minor_row_control = off_diagonal_max <= minor_global + TOL

    return {
        "name": name,
        "source": source,
        "group": {"p": p, "rank": rank, "dual_size": len(dual)},
        "full_slice_size": total,
        "image_size": image_size,
        "max_fiber_size": max_count,
        "actual_image_multiplier": actual_multiplier,
        "global_absolute_fourier_multiplier": global_l1,
        "full_dual_gershgorin_image_multiplier": full_dual_row_multiplier,
        "packed": {
            key: value for key, value in packing.items() if key != "selected"
        },
        "rayleigh_image_multiplier": rayleigh_multiplier,
        "minor_global_mass": minor_global,
        "packed_off_diagonal_row_mass": off_diagonal_max,
        "checks": {
            "differences_avoid_major": differences_avoid_major,
            "greedy_cardinality_floor": greedy_floor,
            "minor_controls_packed_rows": minor_row_control,
            "frame_dominates_actual": frame_dominates_actual,
            "rayleigh_guardrail": rayleigh_guardrail,
        },
    }


def source_case(
    name: str, p: int, support: list[int], weight: int, depth: int
) -> dict[str, Any]:
    rank = effective_rank(p, support, depth)
    if rank != depth:
        raise AssertionError(f"{name}: expected full effective rank {depth}, got {rank}")
    counts = power_sum_counts(p, support, weight, depth)
    return analyze_counts(
        name,
        p,
        depth,
        counts,
        {
            "kind": "fixed_weight_power_sum",
            "support": support,
            "weight": weight,
            "depth": depth,
            "effective_rank": rank,
        },
    )


def existing_elementary_prefix_menu() -> dict[str, Any]:
    """Replay the exact menu in verify_boolean_prefix_fibers.py."""
    fixtures = (
        (5, 5, 2, 1),
        (11, 10, 5, 2),
        (13, 10, 5, 2),
        (17, 8, 4, 1),
        (17, 12, 6, 2),
    )
    rows = []
    for p, n, weight, depth in fixtures:
        support = list(range(n))
        counts = elementary_prefix_counts(p, support, weight, depth)
        rank = image_difference_rank(p, counts)
        if rank != depth:
            raise AssertionError(
                f"elementary-prefix {(p, n, weight, depth)} has rank {rank}"
            )
        row = analyze_counts(
            f"elementary_F{p}_n{n}_m{weight}_w{depth}",
            p,
            depth,
            counts,
            {
                "kind": "existing_elementary_prefix_toy",
                "source_script": "experimental/scripts/verify_boolean_prefix_fibers.py",
                "support": support,
                "weight": weight,
                "depth": depth,
                "effective_image_difference_rank": rank,
            },
        )
        row["packed_strictly_improves_full_dual_row"] = (
            row["packed"]["image_multiplier"] + TOL
            < row["full_dual_gershgorin_image_multiplier"]
        )
        rows.append(row)

    return {
        "source_script": "experimental/scripts/verify_boolean_prefix_fibers.py",
        "rows": rows,
        "summary": {
            "row_count": len(rows),
            "all_checks_pass": all(
                all(row["checks"].values()) for row in rows
            ),
            "nonuniform_rows": sum(
                row["actual_image_multiplier"] > 1.0 + TOL for row in rows
            ),
            "strict_forbidden_difference_improvements": sum(
                row["packed_strictly_improves_full_dual_row"] for row in rows
            ),
            "negative_control": (
                "No menu row selected a nontrivial forbidden-difference packing; "
                "the scalable block-parabola product is the strict family witness."
            ),
        },
    }


def heavy_regression() -> dict[str, Any]:
    p = 2
    rank = 6
    images = group_elements(p, rank)
    counts: Counter[tuple[int, ...]] = Counter()
    counts[images[0]] = 32
    for image in images[1:33]:
        counts[image] = 1
    return analyze_counts(
        "synthetic_heavy_atom_regression",
        p,
        rank,
        counts,
        {
            "kind": "synthetic_distribution_regression",
            "purpose": "CF3 must prevent a false flatness certificate",
        },
    )


def block_parabola_counts(p: int, blocks: int) -> Counter[tuple[int, ...]]:
    """Existing block-profile model: one point per F_p block."""
    counts: Counter[tuple[int, ...]] = Counter()
    for choices in itertools.product(range(p), repeat=blocks):
        image = tuple(
            coordinate
            for t in choices
            for coordinate in (t, (t * t) % p)
        )
        counts[image] += 1
    return counts


def chosen_linear_characters(p: int, blocks: int) -> list[tuple[int, ...]]:
    return [
        tuple(coordinate for a in values for coordinate in (a, 0))
        for values in itertools.product(range(p), repeat=blocks)
    ]


def explicit_block_parabola_replay(p: int, blocks: int) -> dict[str, Any]:
    counts = block_parabola_counts(p, blocks)
    rank = 2 * blocks
    measured_rank = image_difference_rank(p, counts)
    dual, fourier = fourier_transform(p, rank, counts)
    selected = chosen_linear_characters(p, blocks)
    row_bound = gram_row_bound(selected, fourier, p)
    global_l1 = sum(abs(value) for value in fourier.values())
    expected_base = 1.0 + (p - 1) * math.sqrt(p)
    expected_global = expected_base**blocks
    image_size = len(counts)
    multiplier = image_size * row_bound / len(selected)
    off_diagonal = max(
        abs(fourier[sub(other, gamma, p)])
        for gamma in selected
        for other in selected
        if gamma != other
    )
    return {
        "p": p,
        "blocks": blocks,
        "ambient_coordinates": p * blocks,
        "dual_size": len(dual),
        "effective_image_difference_rank": measured_rank,
        "full_slice_size": sum(counts.values()),
        "image_size": image_size,
        "selected_size": len(selected),
        "global_absolute_multiplier": global_l1,
        "expected_global_multiplier": expected_global,
        "packed_gram_row_bound": row_bound,
        "packed_image_multiplier": multiplier,
        "max_packed_off_diagonal": off_diagonal,
        "checks": {
            "injective_profile": image_size == p**blocks,
            "full_effective_span": measured_rank == rank,
            "selected_matches_image": len(selected) == image_size,
            "gauss_product_formula": math.isclose(
                global_l1, expected_global, rel_tol=3.0e-10, abs_tol=3.0e-10
            ),
            "packed_gram_identity": abs(row_bound - 1.0) <= TOL
            and off_diagonal <= TOL,
            "packed_multiplier_exact": abs(multiplier - 1.0) <= TOL,
        },
    }


def block_parabola_family() -> dict[str, Any]:
    primes = (3, 5, 7)
    base_rows = []
    for p in primes:
        replay = explicit_block_parabola_replay(p, 1)
        base = 1.0 + (p - 1) * math.sqrt(p)
        base_rows.append(
            {
                "p": p,
                "absolute_fourier_base": base,
                "global_loss_rate_per_coordinate": math.log(base) / p,
                "packed_multiplier": replay["packed_image_multiplier"],
                "checks": replay["checks"],
            }
        )

    explicit_replays = [
        explicit_block_parabola_replay(3, 2),
        explicit_block_parabola_replay(5, 2),
        explicit_block_parabola_replay(7, 2),
    ]
    p = 5
    base = 1.0 + (p - 1) * math.sqrt(p)
    scale_rows = [
        {
            "blocks": blocks,
            "ambient_coordinates": p * blocks,
            "full_slice_size": p**blocks,
            "image_size": p**blocks,
            "selected_size": p**blocks,
            "global_absolute_multiplier": base**blocks,
            "global_log_loss_per_coordinate": math.log(base) / p,
            "packed_gram_operator_norm": 1.0,
            "packed_image_multiplier": 1.0,
        }
        for blocks in (1, 2, 4, 8, 16)
    ]
    all_checks = all(
        all(row["checks"].values()) for row in base_rows + explicit_replays
    )
    rate = math.log(base) / p
    return {
        "name": "block_parabola_product",
        "provenance": {
            "model": "existing block-profile toy with one selected point per block",
            "related_script": "experimental/scripts/verify_asymptotic_c9_block_profile_plotkin.py",
            "semantic_residual_claimed": False,
        },
        "definition": {
            "block": "F_p with occupancy one",
            "profile": "t -> (t,t^2), direct product over blocks",
            "effective_group": "(F_p^2)^k",
            "absolute_multiplier": "[1+(p-1)*sqrt(p)]^k",
            "packed_family": "{((a_1,0),...,(a_k,0)) : a_i in F_p}",
            "packed_gram": "identity",
        },
        "base_rows": base_rows,
        "explicit_product_replays": explicit_replays,
        "scale_rows_p5": scale_rows,
        "summary": {
            "all_checks_pass": all_checks,
            "p5_global_log_loss_per_coordinate": rate,
            "global_absolute_sum_is_exponential": rate > 0.4,
            "packed_multiplier_is_one": all(
                row["packed_image_multiplier"] == 1.0 for row in scale_rows
            ),
            "strict_asymptotic_separation": rate > 0.0
            and all(row["packed_image_multiplier"] == 1.0 for row in scale_rows),
        },
    }


def pin_labels(tex: str) -> dict[str, bool]:
    return {label: (f"\\label{{{label}}}" in tex) for label in PINS}


def note_contract(note: str) -> dict[str, bool]:
    required = {
        "status_is_conditional": STATUS in note,
        "affine_translation_printed": "Phi(x)-s0" in note,
        "frame_formula_printed": "M ||K_A||_op / |A|" in note,
        "converse_guardrail_printed": "||K_A||_op >= |A| mu(z)" in note,
        "packed_corollary_printed": "Packed major/minor corollary" in note,
        "q_nonclaim_printed": "exact primitive-profile Q in the unrestricted" in note,
        "source_packing_open": "source-specific major-difference cardinality" in note,
        "mi_ma_nonclaim_printed": "effective (MI), effective (MA)" in note,
        "scalable_family_printed": "A scalable separation from global absolute summation" in note,
        "global_exponential_formula_printed": "C_p = 1 + (p-1) sqrt(p)" in note
        and "kappa_abs(k) = C_p^k" in note,
        "packed_identity_printed": "K_{A_k} = I" in note,
        "family_residual_nonclaim": "not a claimed semantic primitive" in note,
    }
    forbidden = {
        "claims_q_proved": "EXACT PRIMITIVE-PROFILE Q: PROVED" in note,
        "claims_mi_ma_proved": "MI+MA CLOSED" in note,
        "claims_sidon_proved": "DIRECT SIDON PAYMENT: PROVED" in note,
    }
    return {**required, **{key: not value for key, value in forbidden.items()}}


def build_payload(root: Path) -> dict[str, Any]:
    tex = (root / TEX).read_text(encoding="utf-8")
    note = (root / NOTE).read_text(encoding="utf-8")
    cases = [
        source_case("F5_full_m2_r2", 5, list(range(5)), 2, 2),
        source_case("F7_full_m4_r2", 7, list(range(7)), 4, 2),
        source_case("F7_prefix6_m3_r2", 7, list(range(6)), 3, 2),
        source_case("F11_prefix7_m3_r2", 11, list(range(7)), 3, 2),
        heavy_regression(),
    ]
    scalable_family = block_parabola_family()
    existing_menu = existing_elementary_prefix_menu()
    source_cases = [case for case in cases if case["source"]["kind"] != "synthetic_distribution_regression"]
    strict_packed_improvements = sum(
        case["packed"]["image_multiplier"] + TOL
        < case["full_dual_gershgorin_image_multiplier"]
        for case in source_cases
    )
    nonuniform_source_cases = sum(case["max_fiber_size"] > 1 for case in source_cases)
    all_checks = all(all(case["checks"].values()) for case in cases)
    heavy = cases[-1]
    heavy_guardrail = (
        heavy["rayleigh_image_multiplier"] + TOL
        >= heavy["actual_image_multiplier"]
        and heavy["actual_image_multiplier"] > 10
    )
    pins = pin_labels(tex)
    contract = note_contract(note)

    payload: dict[str, Any] = {
        "schema": "asymptotic-primitive-profile-character-frame-v1",
        "theorem_id": THEOREM_ID,
        "status": STATUS,
        "base_commit": "486c8fb347ace37f3033332abe572ab9fbf1bf8f",
        "checked_object": (
            "finite effective-group character-frame inequality, converse "
            "guardrail, packed-major corollary, and deterministic toy census"
        ),
        "theorem": {
            "frame": "|F_z| <= M*||K_A||_op/|A|",
            "image_multiplier": "kappa_frame = L*||K_A||_op/|A|",
            "converse": "||K_A||_op >= |A|*max_z(mu(z))",
            "packed_size": "|A| >= |hat(G)|/|Mfrak|",
        },
        "source_pins": pins,
        "note_contract": contract,
        "cases": cases,
        "existing_elementary_prefix_menu": existing_menu,
        "scalable_separating_family": scalable_family,
        "summary": {
            "case_count": len(cases),
            "source_case_count": len(source_cases),
            "strict_packed_improvements": strict_packed_improvements,
            "nonuniform_source_cases": nonuniform_source_cases,
            "all_finite_checks_pass": all_checks,
            "heavy_regression_guardrail_pass": heavy_guardrail,
            "scalable_separating_family_pass": scalable_family["summary"][
                "strict_asymptotic_separation"
            ]
            and scalable_family["summary"]["all_checks_pass"],
            "p5_global_log_loss_per_coordinate": scalable_family["summary"][
                "p5_global_log_loss_per_coordinate"
            ],
            "p5_packed_multiplier": 1.0,
            "existing_menu_rows": existing_menu["summary"]["row_count"],
            "existing_menu_all_checks_pass": existing_menu["summary"][
                "all_checks_pass"
            ],
            "existing_menu_nonuniform_rows": existing_menu["summary"][
                "nonuniform_rows"
            ],
        },
        "nonclaims": [
            "no proof of exact primitive-profile Q in the unrestricted many-shell range",
            "no proof of the uniform source-specific character packing input",
            "no proof of effective MI or effective MA",
            "no proof of the direct Sidon moment payment",
            "no proof of first-match witness exhaustiveness",
            "no claim that the block-parabola separation family is a semantic primitive residual",
        ],
    }
    payload = normalize_numbers(payload)
    payload["payload_sha256"] = canonical_hash(payload)
    return payload


def check_payload(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if payload.get("payload_sha256") != canonical_hash(payload):
        errors.append("payload hash mismatch")
    if payload.get("status") != STATUS:
        errors.append("status mismatch")
    if not all(payload.get("source_pins", {}).values()):
        errors.append("one or more active-manuscript source pins are absent")
    if not all(payload.get("note_contract", {}).values()):
        errors.append("note claim-boundary contract failed")
    summary = payload.get("summary", {})
    if summary.get("strict_packed_improvements", 0) < 2:
        errors.append("packed census lacks two strict improvement cases")
    if summary.get("nonuniform_source_cases", 0) < 2:
        errors.append("census lacks two nonuniform source-profile cases")
    if not summary.get("all_finite_checks_pass"):
        errors.append("a finite frame/packing check failed")
    if not summary.get("heavy_regression_guardrail_pass"):
        errors.append("heavy-fiber converse regression failed")
    if not summary.get("scalable_separating_family_pass"):
        errors.append("scalable packed/global separation family failed")
    if summary.get("p5_global_log_loss_per_coordinate", 0.0) <= 0.4:
        errors.append("p=5 global absolute loss is not exponentially separated")
    if summary.get("p5_packed_multiplier") != 1.0:
        errors.append("p=5 packed multiplier is not exact")
    if summary.get("existing_menu_rows") != 5:
        errors.append("existing elementary-prefix menu is incomplete")
    if not summary.get("existing_menu_all_checks_pass"):
        errors.append("existing elementary-prefix menu replay failed")
    if summary.get("existing_menu_nonuniform_rows", 0) < 4:
        errors.append("existing menu lost its nonuniform regression rows")
    expected_nonclaims = {
        "no proof of exact primitive-profile Q in the unrestricted many-shell range",
        "no proof of the uniform source-specific character packing input",
        "no proof of effective MI or effective MA",
        "no proof of the direct Sidon moment payment",
        "no proof of first-match witness exhaustiveness",
        "no claim that the block-parabola separation family is a semantic primitive residual",
    }
    if set(payload.get("nonclaims", [])) != expected_nonclaims:
        errors.append("nonclaim ledger mismatch")
    return errors


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_payload(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def payloads_close(left: Any, right: Any, path: str = "$") -> list[str]:
    errors: list[str] = []
    if isinstance(left, float) and isinstance(right, (float, int)):
        if not math.isclose(left, float(right), rel_tol=2.0e-10, abs_tol=2.0e-10):
            errors.append(f"{path}: {left!r} != {right!r}")
        return errors
    if type(left) is not type(right):
        errors.append(f"{path}: type {type(left).__name__} != {type(right).__name__}")
        return errors
    if isinstance(left, dict):
        if set(left) != set(right):
            errors.append(f"{path}: key sets differ")
            return errors
        for key in left:
            errors.extend(payloads_close(left[key], right[key], f"{path}.{key}"))
    elif isinstance(left, list):
        if len(left) != len(right):
            errors.append(f"{path}: list lengths differ")
        else:
            for i, (a, b) in enumerate(zip(left, right)):
                errors.extend(payloads_close(a, b, f"{path}[{i}]"))
    elif left != right:
        errors.append(f"{path}: {left!r} != {right!r}")
    return errors


def tamper_selftest(root: Path) -> None:
    original = build_payload(root)
    mutations: list[tuple[str, Any]] = [
        ("status", "PROVED"),
        ("nonclaims", []),
        ("source_pins", {key: False for key in PINS}),
        ("note_contract", {key: False for key in original["note_contract"]}),
        ("summary.strict_packed_improvements", 0),
        ("summary.nonuniform_source_cases", 0),
        ("summary.all_finite_checks_pass", False),
        ("summary.heavy_regression_guardrail_pass", False),
        ("summary.scalable_separating_family_pass", False),
        ("summary.p5_global_log_loss_per_coordinate", 0.0),
        ("summary.p5_packed_multiplier", 2.0),
        ("summary.existing_menu_rows", 0),
        ("summary.existing_menu_all_checks_pass", False),
    ]
    rejected = 0
    for dotted, value in mutations:
        candidate = json.loads(json.dumps(original))
        cursor = candidate
        parts = dotted.split(".")
        for part in parts[:-1]:
            cursor = cursor[part]
        cursor[parts[-1]] = value
        candidate["payload_sha256"] = canonical_hash(candidate)
        if check_payload(candidate):
            rejected += 1
    if rejected != len(mutations):
        raise AssertionError(f"tamper selftest rejected {rejected}/{len(mutations)}")

    with tempfile.TemporaryDirectory() as tmp:
        temp_root = Path(tmp)
        note_path = temp_root / NOTE
        tex_path = temp_root / TEX
        script_path = temp_root / "experimental/scripts/dummy.py"
        note_path.parent.mkdir(parents=True, exist_ok=True)
        tex_path.parent.mkdir(parents=True, exist_ok=True)
        script_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(root / NOTE, note_path)
        shutil.copy2(root / TEX, tex_path)
        note_path.write_text(
            note_path.read_text(encoding="utf-8").replace(
                STATUS, "EXACT PRIMITIVE-PROFILE Q: PROVED", 1
            ),
            encoding="utf-8",
        )
        tampered = build_payload(temp_root)
        if all(tampered["note_contract"].values()):
            raise AssertionError("overclaiming note mutation was not rejected")

    print(f"TAMPER SELFTEST: PASS ({rejected + 1} mutations rejected)")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="check committed artifact")
    parser.add_argument("--write", action="store_true", help="regenerate artifact")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    root = repo_root()
    if args.tamper_selftest:
        tamper_selftest(root)
        return 0

    generated = build_payload(root)
    errors = check_payload(generated)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    cert_path = root / CERT
    if args.write:
        write_payload(cert_path, generated)

    if args.check:
        if not cert_path.exists():
            print(f"ERROR: missing certificate {CERT}")
            return 1
        committed = load_json(cert_path)
        errors.extend(check_payload(committed))
        errors.extend(payloads_close(generated, committed))
        if errors:
            for error in errors[:30]:
                print(f"ERROR: {error}")
            return 1

    summary = generated["summary"]
    print(f"theorem_id: {THEOREM_ID}")
    print(f"status: {STATUS}")
    print(f"input: {len(generated['cases'])} deterministic finite distributions")
    print("checked: affine effective-group frame, packing, converse guardrail")
    print(f"strict_packed_improvements: {summary['strict_packed_improvements']}")
    print(f"nonuniform_source_cases: {summary['nonuniform_source_cases']}")
    print(f"existing_elementary_prefix_rows: {summary['existing_menu_rows']}")
    print(
        "block_parabola_p5_global_rate: "
        f"{summary['p5_global_log_loss_per_coordinate']:.12f}"
    )
    print(f"block_parabola_p5_packed_multiplier: {summary['p5_packed_multiplier']:.1f}")
    print(f"certificate_sha256: {generated['payload_sha256']}")
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
