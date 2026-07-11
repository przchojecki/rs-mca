#!/usr/bin/env python3
"""CHG-linked toy census for the B2 twisted Hankel transform.

The census has two deliberately separate layers:

1. exact ordinary-Hankel transform diagnostics at the same (p,c=w+1) as
   integrated CHG toys, measuring termwise absolute mass versus signed value;
2. reconstruction of the original A_lambda Gaussian completion vector l/2 in
   those CHG toys.

It does not identify the latter vector directly with the complementary-Hankel
twist in the transform theorem.  The companion bridge now supplies the exact
change of coordinates; the signed estimate remains open.

Status: EXPERIMENTAL CENSUS / BRIDGE PROVED / SIGNED ESTIMATE OPEN.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import math
import random
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Sequence

import verify_b2_twisted_hankel_transform_v1 as core


THEOREM_ID = "b2-twisted-hankel-cancellation-census-v1"
STATUS = "EXPERIMENTAL CENSUS / BRIDGE PROVED / SIGNED ESTIMATE OPEN"
SEED = 20260711
CERT = Path(
    "experimental/data/certificates/b2-twisted-hankel-transform-v1/"
    "b2_twisted_hankel_cancellation_v1.json"
)
NOTE = Path("experimental/notes/roadmaps/b2_twisted_hankel_transform_v1.md")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def normalize(value: Any) -> Any:
    if isinstance(value, float):
        if math.isinf(value):
            return "infinity"
        return round(value, 12)
    if isinstance(value, dict):
        return {key: normalize(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [normalize(item) for item in value]
    return value


def payload_hash(payload: dict[str, Any]) -> str:
    clean = copy.deepcopy(payload)
    clean.pop("payload_sha256", None)
    return hashlib.sha256(
        json.dumps(clean, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def transform_masses(
    p: int, c: int, z: Sequence[int], P: Sequence[int]
) -> dict[str, Any]:
    dimension = 2 * c - 1
    impulse_mass = 0
    divisor_mass = 0
    for x in core.vectors(p, c):
        y = core.fixed_add(P, core.square_coefficients(x, p), dimension, p)
        impulse_mass += p**dimension * int(not core.trim(y, p))
        divisor_mass += p ** (c - 1) * abs(
            core.omega(y, c - 1, p, dimension - 1)
            - core.omega(y, c - 2, p, dimension - 1)
        )

    direct = core.twisted_transform_direct_cyclotomic(p, c, z, P)
    numerator = core.twisted_transform_numerator_cyclotomic(p, c, z, P)
    scaled_direct = core.cyc_mul(core.cyc_pow(core.gauss_cyclotomic(p), c), direct)
    if not core.cyc_equal(scaled_direct, numerator):
        raise AssertionError("exact twisted-transform identity failed in census")

    signed_transform = abs(core.cyc_complex(direct))
    signed_numerator = abs(core.cyc_complex(numerator))
    triangle_transform = (impulse_mass + divisor_mass) / (p ** (c / 2))
    cancellation_ratio = (
        math.inf if signed_transform < 1.0e-12 and triangle_transform else
        triangle_transform / max(signed_transform, 1.0e-300)
    )
    return {
        "z": list(z),
        "P": list(P),
        "impulse_absolute_mass": impulse_mass,
        "divisor_absolute_mass": divisor_mass,
        "triangle_transform_bound": triangle_transform,
        "signed_numerator_abs": signed_numerator,
        "signed_transform_abs": signed_transform,
        "absolute_over_signed": cancellation_ratio,
    }


def ordinary_hankel_census(
    *,
    p: int,
    c: int,
    source_toy: dict[str, int],
    sample_count: int | None,
    rng: random.Random,
) -> dict[str, Any]:
    all_pairs: Iterable[tuple[tuple[int, ...], tuple[int, ...]]] = itertools.product(
        core.vectors(p, c), core.vectors(p, 2 * c - 1)
    )
    total_pairs = p ** (3 * c - 1)
    if sample_count is None:
        pairs = list(all_pairs)
        sampling = "exhaustive"
    else:
        population = list(all_pairs)
        pairs = rng.sample(population, min(sample_count, len(population)))
        sampling = "deterministic sample"

    best_cancellation: dict[str, Any] | None = None
    best_finite_cancellation: dict[str, Any] | None = None
    threshold_witness: dict[str, Any] | None = None
    zero_signed = 0
    endpoint_rows = 0
    maximum_triangle_bound = 0.0
    maximum_signed_transform = 0.0
    for z, P in pairs:
        row = transform_masses(p, c, z, P)
        maximum_triangle_bound = max(maximum_triangle_bound, row["triangle_transform_bound"])
        maximum_signed_transform = max(maximum_signed_transform, row["signed_transform_abs"])
        if all(value == 0 for value in z[1:]) and z[0] != 0:
            endpoint_rows += 1
        if row["signed_transform_abs"] < 1.0e-12:
            zero_signed += 1
        if best_cancellation is None or float(row["absolute_over_signed"]) > float(
            best_cancellation["absolute_over_signed"]
        ):
            best_cancellation = row
        if not math.isinf(float(row["absolute_over_signed"])) and (
            best_finite_cancellation is None
            or row["absolute_over_signed"] > best_finite_cancellation["absolute_over_signed"]
        ):
            best_finite_cancellation = row
        toy_target = source_toy["n"] ** 3
        if (
            row["triangle_transform_bound"] > toy_target
            and row["signed_transform_abs"] < toy_target
        ):
            if threshold_witness is None or row["triangle_transform_bound"] > threshold_witness[
                "triangle_transform_bound"
            ]:
                threshold_witness = row

    assert best_cancellation is not None
    return {
        "p": p,
        "c": c,
        "source_toy": source_toy,
        "bridge_scope": (
            "same ordinary-Hankel order as the integrated toy; (P,z) are target-space "
            "census points, not asserted CHG images"
        ),
        "sampling": sampling,
        "population_pair_count": total_pairs,
        "checked_pair_count": len(pairs),
        "endpoint_pair_count": endpoint_rows,
        "zero_signed_count": zero_signed,
        "maximum_triangle_transform_bound": maximum_triangle_bound,
        "maximum_signed_transform_abs": maximum_signed_transform,
        "largest_absolute_over_signed": best_cancellation,
        "largest_finite_absolute_over_signed": best_finite_cancellation,
        "toy_n_cubed_separation_witness": threshold_witness,
        "exact_transform_mismatch_count": 0,
    }


def original_gauss_twist_census(p: int, n: int, w: int, m: int) -> dict[str, Any]:
    if w != 1:
        raise ValueError("this finite census currently prints the integrated w=1 toys")
    c = w + 1
    d = n - c
    H = core.roots_of_unity(p, n)
    inverse_n = pow(n, -1, p)
    inverse_two = pow(2, -1, p)
    free_exponents = tuple(range(1, d + 1))
    evaluation = tuple(
        tuple(pow(point, exponent, p) for exponent in free_exponents) for point in H
    )
    lambdas = list(core.vectors(p, n))

    full_rank = []
    for lam in lambdas:
        matrix = tuple(
            tuple(
                sum(
                    lam[index] * evaluation[index][i] * evaluation[index][j]
                    for index in range(n)
                )
                % p
                for j in range(d)
            )
            for i in range(d)
        )
        if core.matrix_det(matrix, p):
            full_rank.append(lam)

    syndrome_rows = []
    for v in range(p):
        fixed_values = tuple(
            (m * inverse_n + v * inverse_n * pow(point, n - 1, p)) % p
            for point in H
        )
        twist_counts: Counter[tuple[int, ...]] = Counter()
        for lam in full_rank:
            linear = tuple(
                sum(
                    lam[index]
                    * evaluation[index][coordinate]
                    * (2 * fixed_values[index] - 1)
                    for index in range(n)
                )
                % p
                for coordinate in range(d)
            )
            z_a = tuple(inverse_two * value % p for value in linear)
            twist_counts[z_a] += 1

        axis_count = sum(
            count
            for z_a, count in twist_counts.items()
            if z_a[0] != 0 and all(value == 0 for value in z_a[1:])
        )
        zero_count = twist_counts.get((0,) * d, 0)
        syndrome_rows.append(
            {
                "v": v,
                "unique_original_twists": len(twist_counts),
                "zero_twist_lambda_count": zero_count,
                "first_axis_twist_lambda_count": axis_count,
                "most_common_twist_count": max(twist_counts.values(), default=0),
            }
        )

    return {
        "parameters": {"p": p, "n": n, "w": w, "m": m, "c": c, "d": d},
        "lambda_count": len(lambdas),
        "full_rank_lambda_count": len(full_rank),
        "coordinate_warning": (
            "z_A=l/2 is the completion vector in the original free-coefficient "
            "Hankel A_lambda; it is not the complementary-Hankel z of Theorem 4.1"
        ),
        "syndromes": syndrome_rows,
    }


def polar_census(p: int, k: int, rng: random.Random, sample_count: int) -> dict[str, Any]:
    rows = []
    for _ in range(sample_count):
        P = tuple(rng.randrange(p) for _ in range(2 * k + 1))
        z = tuple(rng.randrange(p) for _ in range(k + 1))
        raw_incidence = 0
        filtered_incidence = 0
        for Q in core.projective_polynomials(p, k):
            for x in core.vectors(p, k + 1):
                y = core.fixed_add(P, core.square_coefficients(x, p), 2 * k + 1, p)
                if core.homogeneous_divides(Q, k, y, 2 * k, p):
                    raw_incidence += 1
                    if core.polar_condition_degree_k(z, Q, p):
                        filtered_incidence += 1
        for Q in core.projective_polynomials(p, k - 1):
            for x in core.vectors(p, k + 1):
                y = core.fixed_add(P, core.square_coefficients(x, p), 2 * k + 1, p)
                if core.homogeneous_divides(Q, k - 1, y, 2 * k, p):
                    raw_incidence += 1
                    if core.polar_condition_degree_k_minus_one(z, Q, p):
                        filtered_incidence += 1
        original = core.polar_original(p, k, z, P)
        filtered = core.polar_filtered(p, k, z, P)
        if not core.cyc_equal(original, filtered):
            raise AssertionError("polar census identity mismatch")
        rows.append(
            {
                "raw_incidence": raw_incidence,
                "filtered_incidence": filtered_incidence,
                "retained_fraction": filtered_incidence / raw_incidence if raw_incidence else 0.0,
                "signed_abs": abs(core.cyc_complex(original)),
            }
        )
    return {
        "p": p,
        "k": k,
        "sample_count": sample_count,
        "mean_retained_fraction": sum(row["retained_fraction"] for row in rows) / len(rows),
        "minimum_retained_fraction": min(row["retained_fraction"] for row in rows),
        "maximum_retained_fraction": max(row["retained_fraction"] for row in rows),
        "exact_polar_mismatch_count": 0,
    }


def note_contract(root: Path) -> dict[str, bool]:
    note = (root / NOTE).read_text(encoding="utf-8")
    checks = {
        "census_section": "CHG-linked toy cancellation census" in note,
        "absolute_separation": "termwise absolute transformed bound" in note,
        "original_coordinate_warning": "original-coordinate Gaussian twist" in note,
        "coordinate_distinction": "does not identify" in note and "complementary-Hankel" in note,
        "proof_code_map": "Proof-to-code correspondence" in note,
        "elkies_specialization": "Elkies Theorem 1 specialization" in note,
        "exact_cyclotomic": "exact cyclotomic arithmetic" in note,
    }
    if not all(checks.values()):
        raise AssertionError({key: value for key, value in checks.items() if not value})
    return checks


def build_payload(root: Path) -> dict[str, Any]:
    rng = random.Random(SEED)
    ordinary = [
        ordinary_hankel_census(
            p=7,
            c=2,
            source_toy={"p": 7, "n": 6, "w": 1, "m": 3},
            sample_count=None,
            rng=rng,
        ),
        ordinary_hankel_census(
            p=11,
            c=2,
            source_toy={"p": 11, "n": 5, "w": 1, "m": 2},
            sample_count=500,
            rng=rng,
        ),
    ]
    payload: dict[str, Any] = {
        "theorem_id": THEOREM_ID,
        "status": STATUS,
        "seed": SEED,
        "ordinary_hankel": ordinary,
        "original_gauss_twists": [
            original_gauss_twist_census(7, 6, 1, 3),
            original_gauss_twist_census(11, 5, 1, 2),
        ],
        "polar": polar_census(3, 2, rng, 40),
        "note_contract": note_contract(root),
        "nonclaims": [
            "asymptotic cancellation estimate",
            "lower-rank pseudodeterminant strata",
            "N(0) <= n^3 or max_v N(v) <= n^3",
        ],
    }
    payload = normalize(payload)
    payload["payload_sha256"] = payload_hash(payload)
    return payload


def validate(actual: dict[str, Any], expected: dict[str, Any]) -> None:
    if actual.get("payload_sha256") != payload_hash(actual):
        raise AssertionError("payload hash mismatch")
    if normalize(actual) != normalize(expected):
        raise AssertionError("certificate does not match recomputed census")


def write_payload(root: Path, payload: dict[str, Any]) -> None:
    path = root / CERT
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def tamper_selftest(root: Path, expected: dict[str, Any]) -> int:
    source = json.loads((root / CERT).read_text(encoding="utf-8"))
    mutations = []
    changed = copy.deepcopy(source)
    changed["status"] = "PROVED CHG"
    mutations.append(changed)
    changed = copy.deepcopy(source)
    changed["ordinary_hankel"][0]["exact_transform_mismatch_count"] = 1
    mutations.append(changed)
    changed = copy.deepcopy(source)
    changed["nonclaims"] = []
    mutations.append(changed)
    changed = copy.deepcopy(source)
    changed["payload_sha256"] = "0" * 64
    mutations.append(changed)

    rejected = 0
    with tempfile.TemporaryDirectory() as directory:
        for index, mutation in enumerate(mutations):
            path = Path(directory) / f"mutation_{index}.json"
            path.write_text(json.dumps(mutation), encoding="utf-8")
            try:
                validate(json.loads(path.read_text(encoding="utf-8")), expected)
            except AssertionError:
                rejected += 1
    if rejected != len(mutations):
        raise AssertionError("tamper self-test failed")
    return rejected


def print_summary(payload: dict[str, Any]) -> None:
    print(f"theorem_id: {payload['theorem_id']}")
    print(f"status: {payload['status']}")
    for row in payload["ordinary_hankel"]:
        witness = row["toy_n_cubed_separation_witness"]
        print(
            "ordinary_hankel: "
            f"p={row['p']} c={row['c']} checked={row['checked_pair_count']} "
            f"zero_signed={row['zero_signed_count']} "
            f"n^3_separation={'YES' if witness else 'NO'}"
        )
        if witness:
            print(
                "  witness: "
                f"triangle={witness['triangle_transform_bound']:.6g} "
                f"signed={witness['signed_transform_abs']:.6g}"
            )
    for row in payload["original_gauss_twists"]:
        zero = row["syndromes"][0]
        print(
            "original_twist: "
            f"p={row['parameters']['p']} full_rank={row['full_rank_lambda_count']} "
            f"v0_unique={zero['unique_original_twists']} "
            f"v0_first_axis={zero['first_axis_twist_lambda_count']}"
        )
    print("result: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument(
        "--artifact-check",
        action="store_true",
        help="fast hash/status/note-contract check without recomputing the census",
    )
    args = parser.parse_args()
    if not (args.write or args.check or args.tamper_selftest or args.artifact_check):
        args.artifact_check = True

    root = repo_root()
    if args.artifact_check and not (args.write or args.check or args.tamper_selftest):
        actual = json.loads((root / CERT).read_text(encoding="utf-8"))
        if actual.get("payload_sha256") != payload_hash(actual):
            raise AssertionError("payload hash mismatch")
        note_contract(root)
        print("artifact_check: PASS")
        print_summary(actual)
        return 0

    expected = build_payload(root)
    if args.write:
        write_payload(root, expected)
        print(f"wrote: {CERT.as_posix()}")
    if args.check:
        actual = json.loads((root / CERT).read_text(encoding="utf-8"))
        validate(actual, expected)
    if args.tamper_selftest:
        print(f"tamper_mutations_rejected: {tamper_selftest(root, expected)}")
    print_summary(expected)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
