#!/usr/bin/env python3
"""Verify the KoalaBear m4 rigid S6 [6,5,2] pair quotient."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable

if not __debug__:
    raise RuntimeError("verifier refuses optimized Python execution")


class VerificationError(RuntimeError):
    pass


EXPERIMENTAL = Path(__file__).resolve().parents[1]
REPO_ROOT = EXPERIMENTAL.parent
CERTIFICATE = (
    EXPERIMENTAL
    / "data/certificates/kb-mca-v4-m4-s6-652-pair-quotient-normal-form-v1"
    / "kb_mca_v4_m4_s6_652_pair_quotient_normal_form_v1.json"
)
PARENT_COMMIT = "4e33c7be8b3b29848e0ceb8fd7f50dce45fb2eed"
PARENT_PATH = (
    "experimental/data/certificates/"
    "kb-mca-v4-m4-a6s6-genus-zero-passport-reduction-v1/"
    "kb_mca_v4_m4_a6s6_genus_zero_passport_reduction_v1.json"
)
PARENT_BLOB = "c9be4609a28f4c4b89c099e09a359f833dbf7e1b"
PARENT_PAYLOAD = "c9cfbbf394e479f93d8d8378d886331c8afbbaf338e6fc6b21f55e3e1c485fd7"

Poly = tuple[Fraction, ...]
Rat = tuple[Poly, Poly]
ZERO: Poly = (Fraction(0),)
ONE: Poly = (Fraction(1),)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


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


def exact_keys(value: Any, expected: set[str], label: str) -> None:
    require(isinstance(value, dict), f"{label} is not an object")
    require(set(value) == expected, f"{label} keys differ")


def git_output(*args: str) -> str:
    try:
        result = subprocess.run(
            ["git", *args], cwd=REPO_ROOT, check=True, capture_output=True, text=True
        )
    except subprocess.CalledProcessError as error:
        raise VerificationError(error.stderr.strip()) from error
    return result.stdout.strip()


def poly(*coefficients: int | Fraction) -> Poly:
    result = tuple(Fraction(value) for value in coefficients)
    while len(result) > 1 and result[-1] == 0:
        result = result[:-1]
    return result


def padd(left: Poly, right: Poly) -> Poly:
    length = max(len(left), len(right))
    return poly(
        *(
            (left[index] if index < len(left) else 0)
            + (right[index] if index < len(right) else 0)
            for index in range(length)
        )
    )


def pneg(value: Poly) -> Poly:
    return poly(*(-coefficient for coefficient in value))


def psub(left: Poly, right: Poly) -> Poly:
    return padd(left, pneg(right))


def pmul(left: Poly, right: Poly) -> Poly:
    result = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return poly(*result)


def pscale(value: Poly, scalar: int | Fraction) -> Poly:
    return poly(*(Fraction(scalar) * coefficient for coefficient in value))


def ppow(value: Poly, exponent: int) -> Poly:
    result = ONE
    base = value
    power = exponent
    while power:
        if power & 1:
            result = pmul(result, base)
        base = pmul(base, base)
        power //= 2
    return result


def pderivative(value: Poly) -> Poly:
    return poly(*(index * value[index] for index in range(1, len(value))))


def pdivmod(numerator: Poly, denominator: Poly) -> tuple[Poly, Poly]:
    require(denominator != ZERO, "polynomial division by zero")
    quotient = [Fraction(0)] * max(1, len(numerator) - len(denominator) + 1)
    remainder = numerator
    while remainder != ZERO and len(remainder) >= len(denominator):
        shift = len(remainder) - len(denominator)
        coefficient = remainder[-1] / denominator[-1]
        quotient[shift] += coefficient
        term = poly(*([0] * shift + [coefficient]))
        remainder = psub(remainder, pmul(term, denominator))
    return poly(*quotient), remainder


def pgcd(left: Poly, right: Poly) -> Poly:
    a, b = left, right
    while b != ZERO:
        _, remainder = pdivmod(a, b)
        a, b = b, remainder
    if a == ZERO:
        return ZERO
    return pscale(a, 1 / a[-1])


def normalize(value: Rat) -> Rat:
    numerator, denominator = value
    require(denominator != ZERO, "rational-function denominator zero")
    common = pgcd(numerator, denominator)
    if common != ONE:
        numerator, remainder_n = pdivmod(numerator, common)
        denominator, remainder_d = pdivmod(denominator, common)
        require(remainder_n == remainder_d == ZERO, "nonexact cancellation")
    if denominator[-1] < 0:
        numerator, denominator = pneg(numerator), pneg(denominator)
    return numerator, denominator


def rpoly(value: Poly) -> Rat:
    return value, ONE


def radd(left: Rat, right: Rat) -> Rat:
    return normalize(
        (padd(pmul(left[0], right[1]), pmul(right[0], left[1])), pmul(left[1], right[1]))
    )


def rneg(value: Rat) -> Rat:
    return pneg(value[0]), value[1]


def rmul(left: Rat, right: Rat) -> Rat:
    return normalize((pmul(left[0], right[0]), pmul(left[1], right[1])))


def rdiv(left: Rat, right: Rat) -> Rat:
    return normalize((pmul(left[0], right[1]), pmul(left[1], right[0])))


def rscale(value: Rat, scalar: int | Fraction) -> Rat:
    return normalize((pscale(value[0], scalar), value[1]))


def rpow(value: Rat, exponent: int) -> Rat:
    result = rpoly(ONE)
    for _ in range(exponent):
        result = rmul(result, value)
    return result


def requal(left: Rat, right: Rat) -> bool:
    return pmul(left[0], right[1]) == pmul(right[0], left[1])


def linear(constant: int) -> Poly:
    return poly(constant, 1)


def reconstruct() -> dict[str, Any]:
    e = poly(1257325157, 28623155, -425920, -9680, 55, 1)
    y = normalize(
        (
            pscale(pmul(pmul(linear(-55), linear(44)), ppow(linear(55), 2)), -192),
            e,
        )
    )
    z = normalize((pscale(pmul(ppow(linear(44), 2), linear(55)), 12288), e))
    m = normalize((pscale(linear(44), -64), pmul(linear(-55), linear(55))))
    w = normalize(
        (pscale(poly(3025, 88, 1), -32), pmul(linear(-55), linear(55)))
    )
    require(requal(rdiv(z, y), m), "projection parameter")
    conic = radd(
        radd(rscale(rpow(m, 2), -3025), rscale(m, 2816)),
        radd(rpow(w, 2), rpoly(poly(-1024))),
    )
    require(conic[0] == ZERO, "conic parametrization")

    curve_terms = (
        (-4194304, 5, 0),
        (7434240, 3, 2),
        (16777216, 3, 1),
        (6814720, 2, 3),
        (2635380, 1, 4),
        (-14868480, 1, 3),
        (-12582912, 1, 2),
        (483153, 0, 5),
        (-6814720, 0, 4),
    )
    curve = rpoly(ZERO)
    for coefficient, y_degree, z_degree in curve_terms:
        curve = radd(
            curve,
            rscale(rmul(rpow(y, y_degree), rpow(z, z_degree)), coefficient),
        )
    require(curve[0] == ZERO, "pair curve")

    projected_a = poly(-4194304, 0, 7434240, 6814720, 2635380, 483153)
    projected_b = poly(0, 16777216, 0, -14868480, -6814720)
    projected_c = poly(0, 0, -12582912)
    projected_discriminant = psub(ppow(projected_b, 2), pscale(pmul(projected_a, projected_c), 4))
    expected_discriminant = pscale(
        pmul(
            pmul(poly(0, 0, 1), ppow(linear(Fraction(16, 11)), 4)),
            poly(1024, -2816, 3025),
        ),
        1048576 * 11**4,
    )
    require(projected_discriminant == expected_discriminant, "projected discriminant")

    powers: list[tuple[Rat, Rat]] = [(rpoly(ONE), rpoly(ZERO))]
    for _ in range(6):
        constant, coefficient = powers[-1]
        powers.append((rneg(rmul(coefficient, z)), radd(constant, rmul(coefficient, y))))
    remainder_n = tuple(rscale(part, Fraction(625, 624)) for part in powers[6])
    d_coefficients = (
        Fraction(67108864, 345454395),
        Fraction(0),
        -Fraction(65536, 190333),
        -Fraction(16384, 51909),
        -Fraction(192, 1573),
        -Fraction(16, 715),
        Fraction(1),
    )
    remainder_d = [rpoly(ZERO), rpoly(ZERO)]
    for degree, coefficient in enumerate(d_coefficients):
        for part in range(2):
            remainder_d[part] = radd(
                remainder_d[part], rscale(powers[degree][part], coefficient)
            )

    quartic = poly(12576619, 660176, 14520, 176, 1)
    sextic = poly(-870224422859, -39333485730, -372423117, 3380740, 22143, -330, 1)
    quotient_n = pscale(pmul(ppow(linear(44), 6), ppow(linear(55), 3)), -9566429400000)
    quotient_d = pmul(pmul(linear(143), ppow(quartic, 2)), sextic)
    quotient = normalize((quotient_n, quotient_d))
    require(requal(rdiv(remainder_n[0], remainder_d[0]), quotient), "constant remainder quotient")
    require(requal(rdiv(remainder_n[1], remainder_d[1]), quotient), "linear remainder quotient")
    difference = pneg(pmul(ppow(linear(77), 5), ppow(poly(-4961, -44, 1), 5)))
    require(psub(quotient_n, quotient_d) == difference, "one-fiber factorization")
    factors = (linear(143), quartic, sextic)
    require(all(len(pgcd(factor, pderivative(factor))) == 1 for factor in factors), "squarefree denominator factors")
    require(
        all(len(pgcd(factors[i], factors[j])) == 1 for i in range(3) for j in range(i + 1, 3)),
        "coprime denominator factors",
    )

    profiles = [[6, 6, 3], [5, 5, 5], [2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1]]
    require(all(sum(profile) == 15 for profile in profiles), "fiber degrees")
    require(sum(value - 1 for profile in profiles for value in profile) == 28, "Riemann-Hurwitz")
    p = 2130706433
    require(all(p % prime for prime in (2, 3, 5, 11)), "bad characteristic")
    require(sum(p**index for index in range(6)) % 2 == 0, "even tower multiplier")
    require(44**2 + 4 * 4961 == 66**2 * 5, "pole discriminant")

    return {
        "statement": {
            "schema": "kb-mca-v4-m4-s6-652-pair-quotient-normal-form-v1",
            "terminal": "M4_S6_652_RIGID_PAIR_QUOTIENT_AND_POLE_DESCENT",
        },
        "parent_passport_reduction": {
            "commit": PARENT_COMMIT,
            "certificate_path": PARENT_PATH,
            "certificate_blob_oid": PARENT_BLOB,
            "certificate_payload_sha256": PARENT_PAYLOAD,
            "imported_terminal": "M4_A6S6_GEOMETRIC_FRONTIER_FOUR_PASSPORTS",
            "imported_passport": ["S6", ["5.1", "2.1.1.1.1", "6"]],
        },
        "source_companion": {
            "repository": "michaelmusty/BelyiDB",
            "commit": "7d5b899b0741ebd505363f7f811e5737e906abee",
            "path": "belyi_db/6/6T16-[6,5,2]-6-51-21111-g0.m",
            "blob_oid": "454b284b8d09d855b1fde5c86dac2c28859f0f67",
            "label": "6T16-[6,5,2]-6-51-21111-g0",
        },
        "pair_curve": {
            "equation_terms": [list(term) for term in curve_terms],
            "projection": "z=m*y",
            "projected_discriminant": "2^20*m^2*(11*m+16)^4*(3025*m^2-2816*m+1024)",
            "conic": "w^2=3025*m^2-2816*m+1024",
            "parameter": "m=-64*(u+44)/((u-55)*(u+55))",
        },
        "quotient": {
            "degree": 15,
            "numerator": "-9566429400000*(u+44)^6*(u+55)^3",
            "denominator_linear_shift": 143,
            "denominator_quartic_coefficients_ascending": [int(value) for value in quartic],
            "denominator_sextic_coefficients_ascending": [int(value) for value in sextic],
            "numerator_minus_denominator": "-(u+77)^5*(u^2-44u-4961)^5",
            "fiber_profiles": profiles,
            "total_branch_index": 28,
        },
        "challenge_field": {
            "p": p,
            "extension_degree": 6,
            "pole_points": ["-77", "22+33*sqrt(5)", "22-33*sqrt(5)"],
            "pole_quadratic_discriminant": 21780,
            "pole_fiber_splits": True,
        },
        "source_bindings": {
            "arithmetic": "exact_Fraction_polynomial_and_rational_function_replay",
            "pair_object": "unordered_quadratic_divisor_of_degree_six_fiber",
            "target_transform_for_poles": "T/(T-1)",
        },
        "conclusion": {
            "passport": ["S6", ["5.1", "2.1.1.1.1", "6"]],
            "terminal": "M4_S6_652_RIGID_PAIR_QUOTIENT_AND_POLE_DESCENT",
            "impact": "ONE_OF_THREE_RIGID_M4_PASSPORTS_EXPLICIT_POLE_DESCENT_PROVED",
        },
        "nonclaims": [
            "no completely split unramified active fiber",
            "no quartic source-star incidence",
            "no surviving m4 type deletion",
            "no owner, ledger, endpoint, or KoalaBear row closure",
        ],
    }


def expected_certificate() -> dict[str, Any]:
    data = reconstruct()
    data["payload_sha256"] = payload_hash(data)
    return data


def verify_parent(data: dict[str, Any], check_git: bool) -> None:
    parent = data["parent_passport_reduction"]
    require(parent == expected_certificate()["parent_passport_reduction"], "parent binding")
    if not check_git:
        return
    require(git_output("rev-parse", f"{PARENT_COMMIT}:{PARENT_PATH}") == PARENT_BLOB, "parent blob")
    parent_data = parse_json(git_output("show", f"{PARENT_COMMIT}:{PARENT_PATH}"), "parent certificate")
    require(payload_hash(parent_data) == parent_data["payload_sha256"] == PARENT_PAYLOAD, "parent payload")
    require(parent_data["conclusion"]["terminal"] == parent["imported_terminal"], "parent terminal")
    require(parent["imported_passport"] in parent_data["conclusion"]["retained"], "parent passport")
    tuple_rows = [
        row
        for row in parent_data["tuple_audit"]
        if row[0] == ["2.1.1.1.1", "6"] and row[1] == 720
    ]
    require(len(tuple_rows) == 1, "parent rigid tuple row")
    require(tuple_rows[0][2] == [["5A", 5, {"720": 5}, 5]], "parent generating tuples")
    require(tuple_rows[0][3] is True, "parent rigid passport retained")


def verify_certificate(data: dict[str, Any], check_git: bool = True, expected=None) -> None:
    exact_keys(
        data,
        {
            "payload_sha256",
            "statement",
            "parent_passport_reduction",
            "source_companion",
            "pair_curve",
            "quotient",
            "challenge_field",
            "source_bindings",
            "conclusion",
            "nonclaims",
        },
        "certificate",
    )
    require(payload_hash(data) == data["payload_sha256"], "payload hash")
    if expected is None:
        expected = expected_certificate()
    require(data == expected, "certificate reconstruction")
    verify_parent(data, check_git)


def reseal(data: dict[str, Any]) -> None:
    data["payload_sha256"] = payload_hash(data)


def tamper_selftest(original: dict[str, Any], expected: dict[str, Any]) -> int:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("parent", lambda row: row["parent_passport_reduction"].__setitem__("certificate_blob_oid", "0" * 40)),
        ("source", lambda row: row["source_companion"].__setitem__("blob_oid", "0" * 40)),
        ("curve", lambda row: row["pair_curve"]["equation_terms"][0].__setitem__(0, -4194303)),
        ("conic", lambda row: row["pair_curve"].__setitem__("conic", "w^2=0")),
        ("degree", lambda row: row["quotient"].__setitem__("degree", 14)),
        ("numerator", lambda row: row["quotient"].__setitem__("numerator", "0")),
        ("quartic", lambda row: row["quotient"]["denominator_quartic_coefficients_ascending"].pop()),
        ("profile", lambda row: row["quotient"]["fiber_profiles"][0].pop()),
        ("index", lambda row: row["quotient"].__setitem__("total_branch_index", 27)),
        ("field", lambda row: row["challenge_field"].__setitem__("extension_degree", 5)),
        ("split", lambda row: row["challenge_field"].__setitem__("pole_fiber_splits", False)),
        ("passport", lambda row: row["conclusion"].__setitem__("passport", ["A6", []])),
        ("nonclaim", lambda row: row["nonclaims"].pop()),
        ("extra", lambda row: row.__setitem__("extra", 1)),
    ]
    passed = 0
    for name, mutate in mutations:
        candidate = copy.deepcopy(original)
        mutate(candidate)
        reseal(candidate)
        try:
            verify_certificate(candidate, False, expected)
        except VerificationError:
            passed += 1
        else:
            raise VerificationError(f"tamper survived: {name}")
    bad_hash = copy.deepcopy(original)
    bad_hash["payload_sha256"] = "0" * 64
    try:
        verify_certificate(bad_hash, False, expected)
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
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if not args.check and not args.tamper_selftest and not args.write:
        parser.error("at least one action is required")
    expected = expected_certificate()
    if args.write:
        CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE.write_text(json.dumps(expected, indent=2, sort_keys=True) + "\n")
        print(f"WROTE: {CERTIFICATE.relative_to(REPO_ROOT)}")
    if args.check or args.tamper_selftest:
        data = parse_json(CERTIFICATE.read_text(), str(CERTIFICATE))
        verify_certificate(data, True, expected)
        print("PASS: rigid S6 [6,5,2] pair quotient and pole descent")
        if args.tamper_selftest:
            count = tamper_selftest(data, expected)
            print(f"PASS: {count}/{count} tamper mutations rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
