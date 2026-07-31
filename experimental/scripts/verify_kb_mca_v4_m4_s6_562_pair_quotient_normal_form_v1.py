#!/usr/bin/env python3
"""Verify the KoalaBear m4 rigid S6 [5,6,2] pair quotient."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable

import verify_kb_mca_v4_m4_s6_652_pair_quotient_normal_form_v1 as algebra

if not __debug__:
    raise RuntimeError("verifier refuses optimized Python execution")


class VerificationError(RuntimeError):
    pass


EXPERIMENTAL = Path(__file__).resolve().parents[1]
REPO_ROOT = EXPERIMENTAL.parent
CERTIFICATE = (
    EXPERIMENTAL
    / "data/certificates/kb-mca-v4-m4-s6-562-pair-quotient-normal-form-v1"
    / "kb_mca_v4_m4_s6_562_pair_quotient_normal_form_v1.json"
)
PARENT_COMMIT = "4e33c7be8b3b29848e0ceb8fd7f50dce45fb2eed"
PARENT_PATH = (
    "experimental/data/certificates/"
    "kb-mca-v4-m4-a6s6-genus-zero-passport-reduction-v1/"
    "kb_mca_v4_m4_a6s6_genus_zero_passport_reduction_v1.json"
)
PARENT_BLOB = "c9be4609a28f4c4b89c099e09a359f833dbf7e1b"
PARENT_PAYLOAD = "c9cfbbf394e479f93d8d8378d886331c8afbbaf338e6fc6b21f55e3e1c485fd7"
HELPER_COMMIT = "0d2d1a9811b9b540619f5746acd7107a1c31204e"
HELPER_PATH = "experimental/scripts/verify_kb_mca_v4_m4_s6_652_pair_quotient_normal_form_v1.py"
HELPER_BLOB = "0fd60889fe3aac71170ae74113b91166d917baec"


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


def reconstruct() -> dict[str, Any]:
    a2 = algebra.poly(15129, -50922, 25444)
    y_cubic = algebra.poly(-414973341, 608911992, -276920478, 36517864)
    e5 = algebra.poly(
        2391178738527,
        -4974655751100,
        3171741595920,
        -97900305120,
        -559791696960,
        144800664832,
    )
    y_numerator = algebra.pmul(a2, y_cubic)
    z_linear = algebra.poly(-287, 188)
    z_numerator = algebra.pscale(algebra.pmul(z_linear, algebra.ppow(a2, 2)), -41)

    curve_terms = (
        (-2780548824, 5, 0),
        (1627638336, 4, 1),
        (4750104241, 4, 0),
        (1389447360, 3, 2),
        (8341646472, 3, 1),
        (-819790080, 2, 3),
        (-7256554248, 2, 2),
        (-14250312723, 2, 1),
        (-137681280, 1, 4),
        (-1378420000, 1, 3),
        (-2780548824, 1, 2),
        (82396160, 0, 5),
        (1054995600, 0, 4),
        (4001277576, 0, 3),
        (4750104241, 0, 2),
    )
    curve_numerator = algebra.ZERO
    for coefficient, y_degree, z_degree in curve_terms:
        total_degree = y_degree + z_degree
        scalar = Fraction(12**5, 3**y_degree * 4**z_degree)
        term = algebra.pmul(
            algebra.pmul(
                algebra.ppow(y_numerator, y_degree),
                algebra.ppow(z_numerator, z_degree),
            ),
            algebra.ppow(e5, 5 - total_degree),
        )
        curve_numerator = algebra.padd(
            curve_numerator, algebra.pscale(term, coefficient * scalar)
        )
    require(curve_numerator == algebra.ZERO, "pair-curve parametrization")

    def mscale(expression, scalar):
        return {
            monomial: coefficient * scalar
            for monomial, coefficient in expression.items()
            if coefficient * scalar
        }

    def madd(left, right):
        result = dict(left)
        for monomial, coefficient in right.items():
            result[monomial] = result.get(monomial, Fraction(0)) + coefficient
            if result[monomial] == 0:
                del result[monomial]
        return result

    def shift(expression, dy, dz):
        return {(a + dy, b + dz): coefficient for (a, b), coefficient in expression.items()}

    powers = [({(0, 0): Fraction(1)}, {})]
    for _ in range(6):
        constant, coefficient = powers[-1]
        powers.append((mscale(shift(coefficient, 0, 1), -1), madd(constant, shift(coefficient, 1, 0))))
    n_coefficients = (
        Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(0),
        -Fraction(59778, 17689), Fraction(34992, 17689),
    )
    d_coefficients = (
        Fraction(4750104241, 18113536),
        -Fraction(347568603, 2264192),
        -Fraction(42386415, 323456),
        Fraction(43764835, 566048),
        Fraction(14700345, 1132096),
        -Fraction(5043, 532),
        Fraction(1),
    )
    remainder_n = [{}, {}]
    remainder_d = [{}, {}]
    for degree in range(7):
        for part in range(2):
            remainder_n[part] = madd(
                remainder_n[part], mscale(powers[degree][part], n_coefficients[degree])
            )
            remainder_d[part] = madd(
                remainder_d[part], mscale(powers[degree][part], d_coefficients[degree])
            )

    def clear_denominator(expression, degree=6):
        result = algebra.ZERO
        for (y_degree, z_degree), coefficient in expression.items():
            scalar = coefficient * Fraction(12**degree, 3**y_degree * 4**z_degree)
            term = algebra.pmul(
                algebra.pmul(
                    algebra.ppow(y_numerator, y_degree),
                    algebra.ppow(z_numerator, z_degree),
                ),
                algebra.ppow(e5, degree - y_degree - z_degree),
            )
            result = algebra.padd(result, algebra.pscale(term, scalar))
        return result

    cubic = algebra.poly(33495606, -8441982, -31403007, 14658356)
    sextic = algebra.poly(
        -119893424310248247,
        379227334439635443,
        -474965645409866205,
        290661295480797960,
        -83250949083482880,
        6554290056691968,
        915512069923328,
    )
    quotient_n = algebra.pscale(
        algebra.pmul(algebra.ppow(z_linear, 5), algebra.ppow(a2, 5)), 177147
    )
    quotient_d = algebra.pmul(cubic, algebra.ppow(sextic, 2))
    for part in range(2):
        cleared_n = clear_denominator(remainder_n[part])
        cleared_d = clear_denominator(remainder_d[part])
        require(
            algebra.pmul(cleared_n, quotient_d)
            == algebra.pmul(cleared_d, quotient_n),
            f"remainder quotient part {part}",
        )

    difference = algebra.pscale(
        algebra.pmul(
            algebra.pmul(
                algebra.ppow(algebra.poly(123, 88), 2),
                algebra.ppow(algebra.poly(-123, 89), 3),
            ),
            algebra.pmul(
                algebra.ppow(algebra.poly(-369, 208), 6),
                algebra.pmul(
                    algebra.ppow(algebra.poly(-1107, 683), 3),
                    algebra.poly(-1599, 980),
                ),
            ),
        ),
        3125,
    )
    require(algebra.psub(quotient_n, quotient_d) == difference, "one-fiber factorization")
    require(len(algebra.pgcd(cubic, algebra.pderivative(cubic))) == 1, "cubic squarefree")
    require(len(algebra.pgcd(sextic, algebra.pderivative(sextic))) == 1, "sextic squarefree")
    require(len(algebra.pgcd(cubic, sextic)) == 1, "denominator coprime")
    require(len(algebra.pgcd(z_linear, a2)) == 1, "zero factors coprime")
    require(len(algebra.pgcd(a2, algebra.pderivative(a2))) == 1, "quadratic squarefree")

    profiles = [[5, 5, 5], [6, 3, 3, 2, 1], [2, 2, 2, 2, 2, 2, 1, 1, 1]]
    require(all(sum(profile) == 15 for profile in profiles), "fiber degrees")
    require(sum(value - 1 for profile in profiles for value in profile) == 28, "Riemann-Hurwitz")
    require(50922**2 - 4 * 25444 * 15129 == 14514**2 * 5, "pole discriminant")
    p = 2130706433
    require(all(p % prime for prime in (2, 3, 5, 41, 59)), "bad characteristic")
    require(sum(p**index for index in range(6)) % 2 == 0, "even tower multiplier")

    return {
        "statement": {
            "schema": "kb-mca-v4-m4-s6-562-pair-quotient-normal-form-v1",
            "terminal": "M4_S6_562_RIGID_PAIR_QUOTIENT_AND_POLE_DESCENT",
        },
        "parent_passport_reduction": {
            "commit": PARENT_COMMIT,
            "certificate_path": PARENT_PATH,
            "certificate_blob_oid": PARENT_BLOB,
            "certificate_payload_sha256": PARENT_PAYLOAD,
            "imported_terminal": "M4_A6S6_GEOMETRIC_FRONTIER_FOUR_PASSPORTS",
            "imported_passport": ["S6", ["5.1", "2.2.2", "3.2.1"]],
        },
        "arithmetic_helper": {
            "commit": HELPER_COMMIT,
            "path": HELPER_PATH,
            "blob_oid": HELPER_BLOB,
            "role": "exact Fraction polynomial primitives only",
        },
        "source_companion": {
            "repository": "michaelmusty/BelyiDB",
            "commit": "7d5b899b0741ebd505363f7f811e5737e906abee",
            "path": "belyi_db/6/6T16-[5,6,2]-51-321-222-g0.m",
            "blob_oid": "94cff64a36672ba6bde9e6cbc1fa251230aa8001",
            "label": "6T16-[5,6,2]-51-321-222-g0",
        },
        "pair_model": {
            "construction": "cubic_adjoint_normalization_of_unordered_pair_quintic",
            "curve_terms": [list(term) for term in curve_terms],
            "y_numerator_coefficients_ascending": [int(value) for value in y_numerator],
            "z_numerator_coefficients_ascending": [int(value) for value in z_numerator],
            "common_denominator_coefficients_ascending": [int(value) for value in e5],
            "y_denominator_scalar": 3,
            "z_denominator_scalar": 4,
        },
        "quotient": {
            "degree": 15,
            "numerator": "177147*(188u-287)^5*(25444u^2-50922u+15129)^5",
            "denominator_cubic_coefficients_ascending": [int(value) for value in cubic],
            "denominator_sextic_coefficients_ascending": [int(value) for value in sextic],
            "numerator_minus_denominator": "3125*(88u+123)^2*(89u-123)^3*(208u-369)^6*(683u-1107)^3*(980u-1599)",
            "fiber_profiles": profiles,
            "total_branch_index": 28,
        },
        "challenge_field": {
            "p": p,
            "extension_degree": 6,
            "pole_points": [
                "287/188",
                "(25461+7257*sqrt(5))/25444",
                "(25461-7257*sqrt(5))/25444",
            ],
            "pole_quadratic_discriminant": 1053280980,
            "pole_fiber_splits": True,
        },
        "conclusion": {
            "passport": ["S6", ["5.1", "2.2.2", "3.2.1"]],
            "terminal": "M4_S6_562_RIGID_PAIR_QUOTIENT_AND_POLE_DESCENT",
            "impact": "SECOND_OF_THREE_RIGID_M4_PASSPORTS_EXPLICIT_POLE_DESCENT_PROVED",
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


def verify_bindings(data: dict[str, Any], check_git: bool) -> None:
    if not check_git:
        return
    require(git_output("rev-parse", f"{PARENT_COMMIT}:{PARENT_PATH}") == PARENT_BLOB, "parent blob")
    parent = parse_json(git_output("show", f"{PARENT_COMMIT}:{PARENT_PATH}"), "parent certificate")
    require(payload_hash(parent) == parent["payload_sha256"] == PARENT_PAYLOAD, "parent payload")
    require(data["parent_passport_reduction"]["imported_passport"] in parent["conclusion"]["retained"], "parent passport")
    require(git_output("rev-parse", f"{HELPER_COMMIT}:{HELPER_PATH}") == HELPER_BLOB, "helper blob")


def verify_certificate(data: dict[str, Any], check_git: bool = True, expected=None) -> None:
    exact_keys(
        data,
        {
            "payload_sha256", "statement", "parent_passport_reduction",
            "arithmetic_helper", "source_companion", "pair_model", "quotient",
            "challenge_field", "conclusion", "nonclaims",
        },
        "certificate",
    )
    require(payload_hash(data) == data["payload_sha256"], "payload hash")
    if expected is None:
        expected = expected_certificate()
    require(data == expected, "certificate reconstruction")
    verify_bindings(data, check_git)


def reseal(data: dict[str, Any]) -> None:
    data["payload_sha256"] = payload_hash(data)


def tamper_selftest(original: dict[str, Any], expected: dict[str, Any]) -> int:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("parent", lambda row: row["parent_passport_reduction"].__setitem__("certificate_blob_oid", "0" * 40)),
        ("helper", lambda row: row["arithmetic_helper"].__setitem__("blob_oid", "0" * 40)),
        ("source", lambda row: row["source_companion"].__setitem__("blob_oid", "0" * 40)),
        ("curve", lambda row: row["pair_model"]["curve_terms"][0].__setitem__(0, -1)),
        ("parameter", lambda row: row["pair_model"]["y_numerator_coefficients_ascending"].pop()),
        ("degree", lambda row: row["quotient"].__setitem__("degree", 14)),
        ("cubic", lambda row: row["quotient"]["denominator_cubic_coefficients_ascending"].pop()),
        ("profile", lambda row: row["quotient"]["fiber_profiles"][1].pop()),
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
        print("PASS: rigid S6 [5,6,2] pair quotient and pole descent")
        if args.tamper_selftest:
            count = tamper_selftest(data, expected)
            print(f"PASS: {count}/{count} tamper mutations rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
