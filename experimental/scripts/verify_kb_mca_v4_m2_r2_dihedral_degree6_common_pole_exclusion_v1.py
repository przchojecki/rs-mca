#!/usr/bin/env python3
"""Verify the KoalaBear degree-six common-pole exclusion."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable

if not __debug__:
    raise RuntimeError("verifier refuses optimized Python execution")


class VerificationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


EXPERIMENTAL = Path(__file__).resolve().parents[1]
REPO_ROOT = EXPERIMENTAL.parent
CERTIFICATE = (
    EXPERIMENTAL
    / "data/certificates/kb-mca-v4-m2-r2-dihedral-degree6-common-pole-exclusion-v1"
    / "kb_mca_v4_m2_r2_dihedral_degree6_common_pole_exclusion_v1.json"
)
TWIST_PARENT = {
    "commit": "4b722a5f3a03ea3074441553438e212b074de0db",
    "certificate_path": "experimental/data/certificates/kb-mca-v4-m2-r2-dihedral-residual-source-cover-twist-classifier-v1/kb_mca_v4_m2_r2_dihedral_residual_source_cover_twist_classifier_v1.json",
    "certificate_blob_oid": "715c980aaf20ad2e6d5075ac3cd1da2903af7e79",
    "certificate_payload_sha256": "ec4c0ff7938e4176ba8d5f2a889201b5d683635538a28bed90d86240d4e67313",
    "imported_terminal": "M2_R2_DIHEDRAL_RESIDUAL_SOURCE_COVER_TWIST_CLASSIFIER",
}
P = 2_130_706_433
T2 = Fraction(-27, 5)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def payload_hash(value: dict[str, Any]) -> str:
    unhashed = copy.deepcopy(value)
    unhashed.pop("payload_sha256", None)
    return hashlib.sha256(canonical_json(unhashed).encode()).hexdigest()


def reject_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise VerificationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def parse_json(text: str, label: str) -> dict[str, Any]:
    try:
        value = json.loads(text, object_pairs_hook=reject_duplicates)
    except (json.JSONDecodeError, VerificationError) as error:
        raise VerificationError(f"cannot parse {label}: {error}") from error
    require(isinstance(value, dict), f"{label} is not an object")
    return value


def git_output(*args: str) -> str:
    try:
        result = subprocess.run(["git", *args], cwd=REPO_ROOT, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as error:
        raise VerificationError(error.stderr.strip()) from error
    return result.stdout.strip()


def verify_parent() -> None:
    path = TWIST_PARENT["certificate_path"]
    require(git_output("rev-parse", f"{TWIST_PARENT['commit']}:{path}") == TWIST_PARENT["certificate_blob_oid"], "parent blob")
    data = parse_json(git_output("show", f"{TWIST_PARENT['commit']}:{path}"), path)
    require(data.get("payload_sha256") == TWIST_PARENT["certificate_payload_sha256"], "parent payload")
    require(payload_hash(data) == data.get("payload_sha256"), "parent seal")
    require(data.get("conclusion", {}).get("terminal") == TWIST_PARENT["imported_terminal"], "parent terminal")


@dataclass(frozen=True)
class Quad:
    a: Fraction = Fraction(0)
    b: Fraction = Fraction(0)

    def __add__(self, other: Quad) -> Quad:
        return Quad(self.a + other.a, self.b + other.b)

    def __neg__(self) -> Quad:
        return Quad(-self.a, -self.b)

    def __sub__(self, other: Quad) -> Quad:
        return self + (-other)

    def __mul__(self, other: Quad) -> Quad:
        return Quad(self.a * other.a + self.b * other.b * T2, self.a * other.b + self.b * other.a)

    def inverse(self) -> Quad:
        norm = self.a * self.a - T2 * self.b * self.b
        require(norm != 0, "quadratic inverse")
        return Quad(self.a / norm, -self.b / norm)

    def __truediv__(self, other: Quad) -> Quad:
        return self * other.inverse()


ZERO = Quad()
ONE = Quad(Fraction(1))


def determinant(matrix: list[list[Quad]]) -> Quad:
    rows = [row[:] for row in matrix]
    det = ONE
    for column in range(len(rows)):
        pivot = next((row for row in range(column, len(rows)) if rows[row][column] != ZERO), None)
        require(pivot is not None, "singular Sylvester matrix")
        if pivot != column:
            rows[column], rows[pivot] = rows[pivot], rows[column]
            det = -det
        value = rows[column][column]
        det = det * value
        for row in range(column + 1, len(rows)):
            factor = rows[row][column] / value
            for entry in range(column + 1, len(rows)):
                rows[row][entry] = rows[row][entry] - factor * rows[column][entry]
    return det


def resultant(first: list[Quad], second: list[Quad]) -> Quad:
    m = len(first) - 1
    n = len(second) - 1
    matrix = [[ZERO for _ in range(m + n)] for _ in range(m + n)]
    for row in range(n):
        matrix[row][row : row + m + 1] = list(reversed(first))
    for row in range(m):
        matrix[n + row][row : row + n + 1] = list(reversed(second))
    return determinant(matrix)


def poly_add(left, right):
    zero = left[0] - left[0] if left else right[0] - right[0]
    result = [zero] * max(len(left), len(right))
    for index, value in enumerate(left):
        result[index] = result[index] + value
    for index, value in enumerate(right):
        result[index] = result[index] + value
    return result


def poly_mul(left, right):
    zero = left[0] - left[0]
    result = [zero] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] = result[i + j] + a * b
    return result


def poly_pow(base, exponent):
    one = base[0] - base[0] + (ONE if isinstance(base[0], Quad) else Fraction(1))
    result = [one]
    for _ in range(exponent):
        result = poly_mul(result, base)
    return result


def poly_scale(poly, scalar):
    return [scalar * value for value in poly]


def exact_arithmetic() -> dict[str, Any]:
    plus = [Fraction(1), Fraction(1)]
    minus = [Fraction(-1), Fraction(1)]
    commuting_terms = [
        poly_scale(poly_pow(plus, 6), Fraction(-27, 8)),
        poly_scale(poly_mul(poly_pow(plus, 4), poly_pow(minus, 2)), Fraction(-27, 2)),
        poly_scale(poly_mul(poly_pow(plus, 2), poly_pow(minus, 4)), Fraction(-27, 2)),
        poly_scale(poly_pow(minus, 6), Fraction(-27, 8)),
    ]
    commuting = [Fraction(0)]
    for term in commuting_terms:
        commuting = poly_add(commuting, term)
    expected_commuting = poly_scale([Fraction(5), 0, 11, 0, 11, 0, 5], Fraction(-27, 4))
    require(commuting == expected_commuting, "commuting pullback")
    require(11 * 11 != 4 * 5 * 11, "commuting invariant")

    t = Quad(Fraction(0), Fraction(1))
    x_numerator = [Quad(T2), t]
    denominator = [t, Quad(Fraction(-3))]
    c = Quad(Fraction(756, 125))
    order_three_terms = [
        poly_pow(x_numerator, 6),
        poly_scale(poly_mul(poly_pow(x_numerator, 4), poly_pow(denominator, 2)), Quad(Fraction(-6))),
        poly_scale(poly_mul(poly_pow(x_numerator, 2), poly_pow(denominator, 4)), Quad(Fraction(9))),
        poly_scale(poly_pow(denominator, 6), -c),
    ]
    transformed = [ZERO]
    for term in order_three_terms:
        transformed = poly_add(transformed, term)
    standard = [-c, ZERO, Quad(Fraction(9)), ZERO, Quad(Fraction(-6)), ZERO, ONE]
    require(transformed == poly_scale(standard, transformed[6]), "order-three automorphism")

    reciprocal = resultant(
        [Quad(Fraction(-9)), Quad(Fraction(-8)), ZERO, Quad(Fraction(8))],
        [Quad(Fraction(-12)), Quad(Fraction(-12)), Quad(Fraction(-3)), ZERO, Quad(Fraction(16))],
    )
    require(reciprocal.b == 0 and abs(reciprocal.a) == 22_371_648, "reciprocal resultant")

    e = [
        Quad(Fraction(-198), Fraction(-140)),
        Quad(Fraction(-60), Fraction(-70)),
        Quad(Fraction(-45), Fraction(50)),
        Quad(Fraction(150), Fraction(25)),
    ]
    h = [
        Quad(Fraction(-2268, 5), Fraction(1296)),
        Quad(Fraction(-2592), Fraction(2088)),
        Quad(Fraction(-459), Fraction(1260)),
        Quad(Fraction(3240), Fraction(-1530)),
        Quad(Fraction(-2295), Fraction(-900)),
    ]
    order_three = resultant(e, h)
    scale = Fraction(76_527_504_000)
    expected = Quad(scale * 1_585_334_079, scale * 1_472_792_180)
    require(order_three in (expected, -expected), "order-three resultant")
    norm = 5 * 1_585_334_079**2 + 27 * 1_472_792_180**2
    require(norm == 71_132_574_457_861_006_005, "primitive norm")
    require(norm % P == 1_274_367_339, "norm residue")
    return {
        "commuting_pullback_coefficients_low_to_high": [str(value) for value in commuting],
        "commuting_invariant_comparison": "121!=220",
        "reciprocal_resultant": int(abs(reciprocal.a)),
        "reciprocal_resultant_mod_p": int(abs(reciprocal.a)) % P,
        "order_three_resultant_primitive": "1472792180*t+1585334079",
        "order_three_norm": norm,
        "order_three_norm_mod_p": norm % P,
    }


def build_certificate() -> dict[str, Any]:
    data = {
        "schema": "kb-mca-v4-m2-r2-dihedral-degree6-common-pole-exclusion-v1",
        "parent_source_cover_twist_classifier": TWIST_PARENT,
        "field": {"p": P, "excluded_small_characteristics": [2, 3, 5]},
        "pole_sextic_atlas": {
            "D6": "x^6-6*x^4+9*x^2-2",
            "fiber": "P_c=x^6-6*x^4+9*x^2-c, c not in {0,4}",
            "matching_cases": ["coincident", "V4", "S3"],
            "coincident": "ell=+/-x; exceptionally +/-3/(2x) at c=27/8",
            "V4": "c=27/8 but the fixed-point-free pullback is not a Dickson-six fiber",
            "S3": "c=756/125; ell in {+/-g_t,+/-g_t^2}, g_t=t(x+t)/(t-3x), 5t^2+27=0",
        },
        "source_twist": {
            "a": 1,
            "d_relation": "d^2=3",
            "forced_preimages": "ell^-1({2,b})=roots(z^2-b*d*z+b^2-1)",
            "normalizer_outcome": "empty",
            "order_three_outcome": "empty",
        },
        "exact_arithmetic": exact_arithmetic(),
        "conclusion": {
            "terminal": "M2_R2_DIHEDRAL_DEGREE6_COMMON_POLE_EMPTY",
            "deleted_factor_degrees": [6],
            "surviving_factor_degrees": [3],
            "next_gate": "n=3 common degree-30 function and six-pole/source-locator realization",
        },
        "nonclaims": [
            "no n=3 construction or deletion",
            "no m2 type, K3, KoalaBear, endpoint, or Prize close",
            "no owner or payment",
        ],
    }
    data["payload_sha256"] = payload_hash(data)
    return data


def verify_certificate(data: dict[str, Any], verify_parents: bool) -> None:
    require(data.get("schema") == "kb-mca-v4-m2-r2-dihedral-degree6-common-pole-exclusion-v1", "schema")
    require(data.get("payload_sha256") == payload_hash(data), "payload seal")
    require(data.get("parent_source_cover_twist_classifier") == TWIST_PARENT, "parent")
    if verify_parents:
        verify_parent()
    expected = build_certificate()
    for key in ("field", "pole_sextic_atlas", "source_twist", "exact_arithmetic", "conclusion", "nonclaims"):
        require(data.get(key) == expected[key], key)


def reseal(data: dict[str, Any]) -> None:
    data["payload_sha256"] = payload_hash(data)


def tamper_selftest(original: dict[str, Any]) -> int:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("parent", lambda row: row["parent_source_cover_twist_classifier"].__setitem__("certificate_blob_oid", "0" * 40)),
        ("field", lambda row: row["field"].__setitem__("p", 101)),
        ("D6", lambda row: row["pole_sextic_atlas"].__setitem__("D6", "x^6")),
        ("fiber", lambda row: row["pole_sextic_atlas"].__setitem__("fiber", "arbitrary")),
        ("cases", lambda row: row["pole_sextic_atlas"]["matching_cases"].pop()),
        ("coincident", lambda row: row["pole_sextic_atlas"].__setitem__("coincident", "all ell")),
        ("V4", lambda row: row["pole_sextic_atlas"].__setitem__("V4", "survives")),
        ("S3", lambda row: row["pole_sextic_atlas"].__setitem__("S3", "survives")),
        ("a", lambda row: row["source_twist"].__setitem__("a", -1)),
        ("d", lambda row: row["source_twist"].__setitem__("d_relation", "d^2=1")),
        ("preimages", lambda row: row["source_twist"].__setitem__("forced_preimages", "arbitrary")),
        ("normal", lambda row: row["source_twist"].__setitem__("normalizer_outcome", "live")),
        ("order3", lambda row: row["source_twist"].__setitem__("order_three_outcome", "live")),
        ("pullback", lambda row: row["exact_arithmetic"]["commuting_pullback_coefficients_low_to_high"].pop()),
        ("comparison", lambda row: row["exact_arithmetic"].__setitem__("commuting_invariant_comparison", "121=220")),
        ("reciprocal", lambda row: row["exact_arithmetic"].__setitem__("reciprocal_resultant", 0)),
        ("order-resultant", lambda row: row["exact_arithmetic"].__setitem__("order_three_resultant_primitive", "0")),
        ("norm", lambda row: row["exact_arithmetic"].__setitem__("order_three_norm", 0)),
        ("terminal", lambda row: row["conclusion"].__setitem__("terminal", "OPEN")),
        ("deleted", lambda row: row["conclusion"]["deleted_factor_degrees"].clear()),
        ("survivor", lambda row: row["conclusion"]["surviving_factor_degrees"].append(6)),
        ("next", lambda row: row["conclusion"].__setitem__("next_gate", "closed")),
        ("nonclaim", lambda row: row["nonclaims"].pop()),
    ]
    passed = 0
    for name, mutate in mutations:
        candidate = copy.deepcopy(original)
        mutate(candidate)
        reseal(candidate)
        try:
            verify_certificate(candidate, False)
        except VerificationError:
            passed += 1
        else:
            raise VerificationError(f"tamper survived: {name}")
    bad_hash = copy.deepcopy(original)
    bad_hash["payload_sha256"] = "0" * 64
    try:
        verify_certificate(bad_hash, False)
    except VerificationError:
        passed += 1
    else:
        raise VerificationError("tamper survived: payload")
    try:
        parse_json('{"x":1,"x":2}', "duplicate")
    except VerificationError:
        passed += 1
    else:
        raise VerificationError("duplicate key survived")
    return passed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    if not args.write and not args.check and not args.tamper_selftest:
        parser.error("at least one action is required")
    if args.write:
        verify_parent()
        data = build_certificate()
        CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
        print(f"WROTE: {CERTIFICATE.relative_to(REPO_ROOT)}")
    data = parse_json(CERTIFICATE.read_text(), str(CERTIFICATE))
    verify_certificate(data, True)
    print("PASS: residual degree-six common-pole profile is empty")
    if args.tamper_selftest:
        count = tamper_selftest(data)
        print(f"PASS: {count}/{count} tamper mutations rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
