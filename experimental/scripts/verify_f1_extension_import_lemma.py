#!/usr/bin/env python3
"""Verify the F1 extension-import arithmetic and base-rational confinement.

This is the Q2.4 / ext_import proof packet:

* a nontrivial affine linear pencil with coefficients in B has any isolated
  slope in B, even when slopes are allowed in an extension F;
* the extension-pole numerator
      N_ext(L)=ceil(L(|F|-|B|)/(|F|-|B|+kL))
  crosses a printed denominator budget at an exact list-size threshold.

Run:
    python3 experimental/scripts/verify_f1_extension_import_lemma.py --emit
    python3 experimental/scripts/verify_f1_extension_import_lemma.py
"""

from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import product
import json
from math import comb, floor, log2
from pathlib import Path
from typing import Iterable


REPO = Path(__file__).resolve().parents[2]
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "f1-extension-import"
    / "f1_extension_import_certificate.json"
)

TARGET_BITS = 128


def ceil_div(a: int, b: int) -> int:
    if b <= 0:
        raise ValueError("nonpositive denominator")
    return -(-a // b)


def extension_numerator(q: int, b: int, k: int, list_size: int) -> int:
    if not (0 < b < q):
        raise ValueError("need proper base field size 0 < b < q")
    if k <= 0 or list_size <= 0:
        raise ValueError("k and list_size must be positive")
    x = q - b
    return ceil_div(list_size * x, x + k * list_size)


def budget(q: int, bits: int = TARGET_BITS) -> int:
    return q // (2**bits)


def crossing_threshold(q: int, b: int, k: int, bits: int = TARGET_BITS) -> int | None:
    """Smallest L with N_ext(L) > floor(q/2^bits), or None if impossible."""
    x = q - b
    bstar = budget(q, bits)
    if bstar == 0:
        return 1
    denominator = x - bstar * k
    if denominator <= 0:
        return None
    # ceil(y)>B iff y>B, so solve L*x/(x+kL)>B.
    return floor(Fraction(bstar * x, denominator)) + 1


def log2_int(value: int) -> float:
    return log2(value)


class QuadraticField:
    """F_p[u]/(u^2-d), for small exhaustive confinement checks."""

    def __init__(self, p: int, d: int):
        self.p = p
        self.d = d % p
        self.zero = (0, 0)

    def add(self, left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
        return ((left[0] + right[0]) % self.p, (left[1] + right[1]) % self.p)

    def neg(self, value: tuple[int, int]) -> tuple[int, int]:
        return ((-value[0]) % self.p, (-value[1]) % self.p)

    def sub(self, left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
        return self.add(left, self.neg(right))

    def mul(self, left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
        a, b = left
        c, e = right
        return ((a * c + b * e * self.d) % self.p, (a * e + b * c) % self.p)

    def pow(self, value: tuple[int, int], exponent: int) -> tuple[int, int]:
        out = (1, 0)
        base = value
        while exponent:
            if exponent & 1:
                out = self.mul(out, base)
            base = self.mul(base, base)
            exponent >>= 1
        return out

    def inv(self, value: tuple[int, int]) -> tuple[int, int]:
        if value == self.zero:
            raise ZeroDivisionError("zero inverse")
        return self.pow(value, self.p * self.p - 2)

    def div(self, left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
        return self.mul(left, self.inv(right))

    def base(self, value: int) -> tuple[int, int]:
        return (value % self.p, 0)

    def is_base(self, value: tuple[int, int]) -> bool:
        return value[1] % self.p == 0

    def elements(self) -> Iterable[tuple[int, int]]:
        for a in range(self.p):
            for b in range(self.p):
                yield (a, b)


def solve_base_vector_pencil(
    field: QuadraticField,
    a_vec: tuple[int, ...],
    b_vec: tuple[int, ...],
) -> list[tuple[int, int]]:
    solutions: list[tuple[int, int]] = []
    for z in field.elements():
        ok = True
        for a, b in zip(a_vec, b_vec):
            if field.add(field.base(a), field.mul(z, field.base(b))) != field.zero:
                ok = False
                break
        if ok:
            solutions.append(z)
    return solutions


def check_base_rational_confinement() -> tuple[bool, list[str], dict[str, object]]:
    field = QuadraticField(5, 2)
    checked = 0
    singleton_nonbase = []
    all_extension_count = 0
    empty_count = 0
    singleton_base_count = 0
    for length in (1, 2, 3):
        for a_vec in product(range(field.p), repeat=length):
            for b_vec in product(range(field.p), repeat=length):
                checked += 1
                solutions = solve_base_vector_pencil(field, a_vec, b_vec)
                if len(solutions) == 0:
                    empty_count += 1
                elif len(solutions) == field.p * field.p:
                    all_extension_count += 1
                elif len(solutions) == 1 and field.is_base(solutions[0]):
                    singleton_base_count += 1
                else:
                    singleton_nonbase.append({
                        "a_vec": a_vec,
                        "b_vec": b_vec,
                        "solutions": solutions,
                    })
    ok = not singleton_nonbase
    payload = {
        "field": "F_25 = F_5[u]/(u^2-2)",
        "vector_lengths": [1, 2, 3],
        "checked_base_pencils": checked,
        "empty_solution_sets": empty_count,
        "all_extension_solution_sets": all_extension_count,
        "singleton_base_solution_sets": singleton_base_count,
        "non_base_singleton_or_other_counterexamples": singleton_nonbase[:5],
    }
    return ok, [
        f"checked base-rational vector pencils over F_25: {checked}",
        f"singleton base slopes: {singleton_base_count}",
        f"non-base singleton/exceptional solution sets: {len(singleton_nonbase)}",
    ], payload


def sample_row(name: str, q: int, b: int, k: int, list_size: int, bits: int = TARGET_BITS) -> dict[str, object]:
    threshold = crossing_threshold(q, b, k, bits)
    numerator = extension_numerator(q, b, k, list_size)
    bstar = budget(q, bits)
    x = q - b
    if threshold is None:
        threshold_payload: dict[str, object] = {
            "crossing_possible": False,
            "reason": "floor(q/2^bits) is at least the saturation limit (q-b)/k",
        }
    else:
        before = threshold - 1 if threshold > 1 else None
        threshold_payload = {
            "crossing_possible": True,
            "minimal_L_with_N_ext_above_budget": threshold,
            "N_ext_at_threshold_minus_1": (
                extension_numerator(q, b, k, before)
                if before is not None
                else None
            ),
            "N_ext_at_threshold": extension_numerator(q, b, k, threshold),
            "log2_threshold": log2_int(threshold),
        }
    return {
        "name": name,
        "q_line": q,
        "base_size": b,
        "extension_gap_q_minus_b": x,
        "k": k,
        "target_bits": bits,
        "budget_floor_q_over_2bits": bstar,
        "saturation_limit_floor": x // k,
        "sample_list_size": list_size,
        "sample_N_ext": numerator,
        "sample_crosses_budget": numerator > bstar,
        "sample_log2_L": log2_int(list_size),
        "sample_log2_N_ext": log2_int(numerator) if numerator > 0 else None,
        "threshold": threshold_payload,
    }


def build_samples() -> list[dict[str, object]]:
    koala_p = 2**31 - 2**24 + 1
    koala_q = koala_p**6
    koala_k = 2**20
    koala_L = ceil_div(comb(256, 130), koala_p)

    near_p = 2**64 - 59
    near_q = near_p**4
    near_k = 2**40
    near_threshold = crossing_threshold(near_q, near_p, near_k, TARGET_BITS)
    near_L = near_threshold if near_threshold is not None else 2**128

    return [
        sample_row("toy_quadratic", q=5**2, b=5, k=3, list_size=4, bits=4),
        sample_row("toy_no_crossing", q=5**2, b=5, k=30, list_size=100, bits=4),
        sample_row(
            "koalabear_sextic_slack_two_demo",
            q=koala_q,
            b=koala_p,
            k=koala_k,
            list_size=koala_L,
        ),
        sample_row(
            "near_256_bit_fourth_power_size_arithmetic",
            q=near_q,
            b=near_p,
            k=near_k,
            list_size=near_L,
        ),
    ]


def check_extension_thresholds() -> tuple[bool, list[str], dict[str, object]]:
    samples = build_samples()
    ok = True
    details = []
    for row in samples:
        threshold = row["threshold"]
        if threshold["crossing_possible"]:
            before_value = threshold["N_ext_at_threshold_minus_1"]
            ok &= (
                before_value is None
                or before_value <= row["budget_floor_q_over_2bits"]
            )
            ok &= threshold["N_ext_at_threshold"] > row["budget_floor_q_over_2bits"]
            details.append(
                "{name}: log2 L_min={log2:.6f}, sample crosses={crosses}".format(
                    name=row["name"],
                    log2=threshold["log2_threshold"],
                    crosses=row["sample_crosses_budget"],
                )
            )
        else:
            ok &= row["saturation_limit_floor"] <= row["budget_floor_q_over_2bits"]
            details.append(f"{row['name']}: crossing impossible")
    payload = {
        "formula": {
            "N_ext(L)": "ceil(L(q-b)/(q-b+kL))",
            "budget": "B*=floor(q/2^lambda)",
            "minimal_crossing_L": (
                "floor(B*(q-b)/(q-b-B*k))+1 when q-b-B*k>0; "
                "otherwise no crossing"
            ),
        },
        "samples": samples,
    }
    return ok, details, payload


def build_artifact() -> dict[str, object]:
    conf_ok, _, confinement = check_base_rational_confinement()
    ext_ok, _, extension = check_extension_thresholds()
    classification = (
        "F1_EXTENSION_IMPORT_ARITHMETIC_AND_BASE_CONFINEMENT_VERIFIED"
        if conf_ok and ext_ok
        else "F1_EXTENSION_IMPORT_CHECK_FAILED"
    )
    return {
        "schema_version": "f1-extension-import-v1",
        "status": "PROVED / ARITHMETIC",
        "dag_target": "ext_import",
        "classification": classification,
        "base_rational_confinement": confinement,
        "extension_pole_thresholds": extension,
        "nonclaims": [
            "does not prove the full F1 safe-side classification",
            "does not prove every F-valued bad slope is extension-pole or subfield-confined",
            "does not transfer base-field MCA bounds to arbitrary F-valued lines",
            "does not change Papers A-D",
        ],
    }


def write_artifact() -> None:
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(build_artifact(), indent=2, sort_keys=True) + "\n")


def check_artifact_replay() -> tuple[bool, list[str], dict[str, object]]:
    if not ARTIFACT.exists():
        return False, ["artifact missing; rerun with --emit"], {}
    actual = json.loads(ARTIFACT.read_text())
    expected = build_artifact()
    ok = actual == expected
    return ok, [
        f"artifact path: {ARTIFACT.relative_to(REPO)}",
        f"artifact matches deterministic builder: {ok}",
        f"classification: {actual.get('classification')}",
    ], {}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true", help="write the JSON certificate")
    args = parser.parse_args()
    if args.emit:
        write_artifact()

    checks = [
        ("base-rational pencil confinement", check_base_rational_confinement),
        ("extension-pole threshold arithmetic", check_extension_thresholds),
        ("artifact replay", check_artifact_replay),
    ]

    print("=" * 78)
    print("F1 extension-import lemma")
    print("=" * 78)
    passed = failed = 0
    for title, check in checks:
        ok, details, _ = check()
        passed += int(ok)
        failed += int(not ok)
        print(f"\n[{'PASS' if ok else 'FAIL':4}] {title}")
        for line in details:
            print(f"       {line}")
    print("\n" + "-" * 78)
    print(f"classification: {build_artifact()['classification']}")
    print(f"PASS: {passed}   FAIL: {failed}")
    print("-" * 78)
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
