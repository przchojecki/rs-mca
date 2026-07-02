#!/usr/bin/env python3
"""E5 evidence: multiscale resonance attack on payment completeness.

This verifier is deliberately a bounded evidence packet, not a theorem about
the full MCA object.  It tests the Fable E5 question in a linear periodic
model: can phase-locked dyadic structure across many quotient scales create
extra slope rank beyond the deduped union of per-scale character payments?

Run:
    python3 experimental/scripts/verify_x1_e5_multiscale_resonance_evidence.py
    python3 experimental/scripts/verify_x1_e5_multiscale_resonance_evidence.py --emit
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Iterable


REPO = Path(__file__).resolve().parents[2]
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "x1-e5-multiscale-resonance"
    / "e5_multiscale_resonance_evidence.json"
)

PRIME = 12289
ROWS = [1024, 2048, 4096]
EXTENSION_DEGREE = 32
EXTENSION_GAMMA = 11
RANDOM_SEED = 20260702
RANDOM_TRIALS_PER_ROW_AND_CAP = 512


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


def factor_distinct(value: int) -> list[int]:
    factors: list[int] = []
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


def multiplicative_order(value: int, p: int) -> int:
    if value % p == 0:
        raise ValueError("zero has no multiplicative order")
    order = p - 1
    for factor in factor_distinct(p - 1):
        while order % factor == 0 and pow(value, order // factor, p) == 1:
            order //= factor
    return order


def binomial_irreducible(p: int, degree: int, gamma: int) -> bool:
    """Irreducibility criterion for X^degree - gamma over F_p."""
    order = multiplicative_order(gamma, p)
    radical = 1
    for factor in factor_distinct(degree):
        radical *= factor
    return (
        order % radical == 0
        and all(((p - 1) // order) % factor != 0 for factor in factor_distinct(degree))
        and (degree % 4 != 0 or p % 4 == 1)
    )


def rank_mod_p(vectors: Iterable[tuple[int, ...]], p: int) -> int:
    rows = [list(vector) for vector in vectors if any(coord % p for coord in vector)]
    if not rows:
        return 0
    ncols = len(rows[0])
    rank = 0
    for col in range(ncols):
        pivot = next((row for row in range(rank, len(rows)) if rows[row][col] % p), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = pow(rows[rank][col] % p, -1, p)
        rows[rank] = [(entry * inv) % p for entry in rows[rank]]
        for row in range(len(rows)):
            if row != rank and rows[row][col] % p:
                scale = rows[row][col] % p
                rows[row] = [
                    (rows[row][idx] - scale * rows[rank][idx]) % p
                    for idx in range(ncols)
                ]
        rank += 1
        if rank == len(rows):
            break
    return rank


def alpha_power_vector(
    exponent: int,
    degree: int,
    gamma: int = EXTENSION_GAMMA,
) -> tuple[int, ...]:
    """Vector for alpha^exponent in F_p[alpha]/(alpha^degree-gamma).

    The rank calculation only uses the fact that powers with distinct exponents
    modulo degree occupy distinct basis lines.  The scalar gamma factor records
    the wrap count so the representation is an honest binomial-extension model.
    """
    residue = exponent % degree
    wraps = exponent // degree
    vector = [0] * degree
    vector[residue] = pow(gamma, wraps, PRIME)
    return tuple(vector)


def residue_rank(residues: Iterable[int], degree: int) -> int:
    return len({residue % degree for residue in residues})


def dyadic_scales(n: int, degree: int) -> list[int]:
    scales: list[int] = []
    scale = degree
    while scale <= n:
        if n % scale == 0:
            scales.append(scale)
        scale *= 2
    return scales


def evaluate_family(
    n: int,
    degree: int,
    residues_by_scale: dict[int, list[int]],
) -> dict[str, object]:
    per_scale = {
        str(scale): residue_rank(residues, degree)
        for scale, residues in residues_by_scale.items()
    }
    all_residues = [
        residue
        for residues in residues_by_scale.values()
        for residue in residues
    ]
    deduped_union_rank = residue_rank(all_residues, degree)
    actual_rank = rank_mod_p(
        [alpha_power_vector(residue, degree) for residue in all_residues],
        PRIME,
    )
    additive_rank = sum(per_scale.values())
    max_single = max(per_scale.values()) if per_scale else 0
    hidden_excess = actual_rank - deduped_union_rank
    return {
        "n": n,
        "extension_degree": degree,
        "scales": sorted(residues_by_scale),
        "residues_by_scale": {
            str(scale): residues_by_scale[scale]
            for scale in sorted(residues_by_scale)
        },
        "per_scale_ranks": per_scale,
        "max_single_scale_rank": max_single,
        "additive_rank_without_dedup": additive_rank,
        "deduped_union_rank": deduped_union_rank,
        "actual_combined_rank": actual_rank,
        "hidden_excess_over_deduped_union": hidden_excess,
        "additive_overcount_removed_by_dedup": additive_rank - actual_rank,
        "ratio_vs_max_single_scale": (
            None if max_single == 0 else actual_rank / max_single
        ),
    }


def summarize_families(name: str, families: list[dict[str, object]]) -> dict[str, object]:
    max_rank = max(families, key=lambda row: int(row["actual_combined_rank"]))
    max_hidden = max(families, key=lambda row: int(row["hidden_excess_over_deduped_union"]))
    max_ratio = max(
        families,
        key=lambda row: float(row["ratio_vs_max_single_scale"] or 0.0),
    )
    return {
        "name": name,
        "families_checked": len(families),
        "max_combined_rank": max_rank["actual_combined_rank"],
        "max_hidden_excess_over_deduped_union": max_hidden[
            "hidden_excess_over_deduped_union"
        ],
        "max_ratio_vs_single_scale": max_ratio["ratio_vs_max_single_scale"],
        "witness_for_max_rank": max_rank,
        "witness_for_max_ratio": max_ratio,
    }


def phase_locked_families() -> list[dict[str, object]]:
    families: list[dict[str, object]] = []
    for n in ROWS:
        scales = dyadic_scales(n, EXTENSION_DEGREE)
        for cap in (2, 3):
            for phase in range(EXTENSION_DEGREE):
                residues_by_scale = {
                    scale: [(phase + slot) % scale for slot in range(cap)]
                    for scale in scales
                }
                families.append(evaluate_family(n, EXTENSION_DEGREE, residues_by_scale))
    return families


def adversarial_spread_families() -> list[dict[str, object]]:
    families: list[dict[str, object]] = []
    for n in ROWS:
        scales = dyadic_scales(n, EXTENSION_DEGREE)
        for cap in (2, 3):
            for phase in range(EXTENSION_DEGREE):
                residues_by_scale = {}
                for idx, scale in enumerate(scales):
                    residues_by_scale[scale] = [
                        (phase + cap * idx + slot) % scale
                        for slot in range(cap)
                    ]
                families.append(evaluate_family(n, EXTENSION_DEGREE, residues_by_scale))
    return families


def random_families() -> list[dict[str, object]]:
    rng = random.Random(RANDOM_SEED)
    families: list[dict[str, object]] = []
    for n in ROWS:
        scales = dyadic_scales(n, EXTENSION_DEGREE)
        for cap in (2, 3):
            for _ in range(RANDOM_TRIALS_PER_ROW_AND_CAP):
                residues_by_scale = {
                    scale: sorted(rng.sample(range(scale), cap))
                    for scale in scales
                }
                families.append(evaluate_family(n, EXTENSION_DEGREE, residues_by_scale))
    return families


def exact_small_character_rank_check() -> tuple[bool, list[str]]:
    residues_by_scale = {
        8: [0, 1],
        16: [2, 5],
        32: [3, 7],
    }
    row = evaluate_family(32, 8, residues_by_scale)
    expected = len({0, 1, 2, 5, 3, 7})
    ok = (
        row["actual_combined_rank"] == expected
        and row["deduped_union_rank"] == expected
        and row["hidden_excess_over_deduped_union"] == 0
    )
    return ok, [
        "exact full-character check: n=32, extension degree 8, scales 8/16/32",
        f"actual combined rank = {row['actual_combined_rank']}, "
        f"deduped character-union rank = {row['deduped_union_rank']}, "
        f"expected = {expected}",
        "the calculation is linear algebra over the binomial basis "
        "1, alpha, ..., alpha^7",
    ]


def build_artifact() -> dict[str, object]:
    phase = summarize_families("phase_locked_same_residue_windows", phase_locked_families())
    spread = summarize_families("adversarial_residue_spread", adversarial_spread_families())
    random_summary = summarize_families(
        "seeded_random_phase_locked_residue_sets",
        random_families(),
    )
    summaries = [phase, spread, random_summary]
    max_hidden = max(
        int(summary["max_hidden_excess_over_deduped_union"])
        for summary in summaries
    )
    classification = (
        "NO_MULTISCALE_HIDDEN_RANK_SIGNAL_IN_PRE_REGISTERED_LINEAR_PERIODIC_MODEL"
        if max_hidden == 0
        else "MULTISCALE_HIDDEN_RANK_SIGNAL_FOUND"
    )
    return {
        "schema_version": "x1-e5-multiscale-resonance-v1",
        "status": "EXPERIMENTAL/AUDIT",
        "dag_targets": ["payment_completeness", "redteam_multiscale"],
        "fable_evidence_item": "E5",
        "model": (
            "linear periodic dyadic character model; combined image rank is "
            "computed in a common binomial extension basis and compared with "
            "the deduped union of per-scale character payments"
        ),
        "pre_registered_search_space": {
            "prime": PRIME,
            "rows_n": ROWS,
            "extension_degree": EXTENSION_DEGREE,
            "extension_gamma": EXTENSION_GAMMA,
            "binomial": f"X^{EXTENSION_DEGREE}-{EXTENSION_GAMMA}",
            "binomial_irreducible_over_Fp": binomial_irreducible(
                PRIME,
                EXTENSION_DEGREE,
                EXTENSION_GAMMA,
            ),
            "dyadic_scales": {
                str(n): dyadic_scales(n, EXTENSION_DEGREE)
                for n in ROWS
            },
            "active_characters_per_scale": [2, 3],
            "phase_locked_families": "all phases modulo extension_degree",
            "adversarial_spread_families": "all phases with residues spread across scales",
            "seeded_random_trials_per_row_and_cap": RANDOM_TRIALS_PER_ROW_AND_CAP,
            "random_seed": RANDOM_SEED,
        },
        "interpretation_table": {
            "max_hidden_excess_over_deduped_union = 0": (
                "supports payment-completeness in this model; multiscale "
                "accumulation is exactly paid by the union of character lines"
            ),
            "max_hidden_excess_over_deduped_union > 0": (
                "candidate fifth mechanism; minimize the witness and add a "
                "new paid-ledger column before using payment completeness"
            ),
        },
        "summaries": summaries,
        "classification": classification,
        "nonclaims": [
            "does not prove payment_completeness",
            "does not search arbitrary received words",
            "does not model nonlinear Hankel chart interactions",
            "does not change Paper A-D statements",
        ],
    }


def write_artifact() -> None:
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(build_artifact(), indent=2, sort_keys=True) + "\n")


def check_prime_and_rows() -> tuple[bool, list[str]]:
    irreducible = binomial_irreducible(PRIME, EXTENSION_DEGREE, EXTENSION_GAMMA)
    ok = (
        is_prime(PRIME)
        and all((PRIME - 1) % n == 0 for n in ROWS)
        and irreducible
    )
    return ok, [
        f"prime p={PRIME}: {is_prime(PRIME)}",
        "row compatibility: "
        + ", ".join(f"n={n} divides p-1: {((PRIME - 1) % n) == 0}" for n in ROWS),
        f"extension model: F_p[alpha]/(alpha^{EXTENSION_DEGREE}-{EXTENSION_GAMMA})",
        f"gamma order in F_p^*: {multiplicative_order(EXTENSION_GAMMA, PRIME)}",
        f"binomial irreducible over F_p: {irreducible}",
    ]


def check_family_summary(name: str, families: list[dict[str, object]]) -> tuple[bool, list[str]]:
    summary = summarize_families(name, families)
    max_hidden = int(summary["max_hidden_excess_over_deduped_union"])
    max_rank = int(summary["max_combined_rank"])
    max_ratio = summary["max_ratio_vs_single_scale"]
    ok = max_hidden == 0 and max_rank > 0 and (max_ratio or 0) >= 1
    return ok, [
        f"families checked: {summary['families_checked']}",
        f"max combined rank: {max_rank}",
        f"max ratio versus one scale: {max_ratio}",
        f"max hidden excess over deduped union: {max_hidden}",
    ]


def check_artifact_matches_builder() -> tuple[bool, list[str]]:
    if not ARTIFACT.exists():
        return False, ["artifact missing; rerun with --emit"]
    actual = json.loads(ARTIFACT.read_text())
    expected = build_artifact()
    return actual == expected, [
        f"artifact path: {ARTIFACT.relative_to(REPO)}",
        f"artifact matches deterministic builder: {actual == expected}",
        f"classification: {actual.get('classification')}",
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true", help="write the JSON artifact")
    args = parser.parse_args()
    if args.emit:
        write_artifact()

    checks = [
        ("prime and dyadic-row compatibility", check_prime_and_rows),
        ("exact small multiscale character rank", exact_small_character_rank_check),
        (
            "phase-locked same-residue families",
            lambda: check_family_summary(
                "phase_locked_same_residue_windows",
                phase_locked_families(),
            ),
        ),
        (
            "adversarial spread families",
            lambda: check_family_summary(
                "adversarial_residue_spread",
                adversarial_spread_families(),
            ),
        ),
        (
            "seeded random families",
            lambda: check_family_summary(
                "seeded_random_phase_locked_residue_sets",
                random_families(),
            ),
        ),
        ("artifact replay", check_artifact_matches_builder),
    ]

    print("=" * 78)
    print("X1 / E5 multiscale resonance evidence")
    print("=" * 78)
    passed = failed = 0
    for title, check in checks:
        ok, details = check()
        passed += int(ok)
        failed += int(not ok)
        print(f"\n[{'PASS' if ok else 'FAIL':4}] {title}")
        for line in details:
            print(f"       {line}")
    print("\n" + "-" * 78)
    artifact = build_artifact()
    print(f"classification: {artifact['classification']}")
    print(f"PASS: {passed}   FAIL: {failed}")
    print("-" * 78)
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
