#!/usr/bin/env python3
"""Verify the KoalaBear m4 rigid A6 [5,4,2] pair quotient."""

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


K = tuple[Fraction, Fraction]
Poly = tuple[K, ...]
KZERO: K = (Fraction(0), Fraction(0))
KONE: K = (Fraction(1), Fraction(0))

EXPERIMENTAL = Path(__file__).resolve().parents[1]
REPO_ROOT = EXPERIMENTAL.parent
CERTIFICATE = (
    EXPERIMENTAL
    / "data/certificates/kb-mca-v4-m4-a6-542-pair-quotient-normal-form-v1"
    / "kb_mca_v4_m4_a6_542_pair_quotient_normal_form_v1.json"
)
PARENT_COMMIT = "4e33c7be8b3b29848e0ceb8fd7f50dce45fb2eed"
PARENT_PATH = (
    "experimental/data/certificates/"
    "kb-mca-v4-m4-a6s6-genus-zero-passport-reduction-v1/"
    "kb_mca_v4_m4_a6s6_genus_zero_passport_reduction_v1.json"
)
PARENT_BLOB = "c9be4609a28f4c4b89c099e09a359f833dbf7e1b"
PARENT_PAYLOAD = "c9cfbbf394e479f93d8d8378d886331c8afbbaf338e6fc6b21f55e3e1c485fd7"


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


def k(constant: int | Fraction, nu: int | Fraction = 0) -> K:
    return Fraction(constant), Fraction(nu)


def kadd(left: K, right: K) -> K:
    return left[0] + right[0], left[1] + right[1]


def kneg(value: K) -> K:
    return -value[0], -value[1]


def kmul(left: K, right: K) -> K:
    a, b = left
    c, d = right
    return a * c - 4 * b * d, a * d + b * c + b * d


def kinv(value: K) -> K:
    a, b = value
    norm = a * a + a * b + 4 * b * b
    require(norm != 0, "field division by zero")
    return (a + b) / norm, -b / norm


def kdiv(left: K, right: K) -> K:
    return kmul(left, kinv(right))


def poly(*coefficients: K) -> Poly:
    result = tuple(coefficients)
    while len(result) > 1 and result[-1] == KZERO:
        result = result[:-1]
    return result


PZERO: Poly = poly(KZERO)
PONE: Poly = poly(KONE)


def padd(left: Poly, right: Poly) -> Poly:
    return poly(
        *(
            kadd(
                left[index] if index < len(left) else KZERO,
                right[index] if index < len(right) else KZERO,
            )
            for index in range(max(len(left), len(right)))
        )
    )


def pneg(value: Poly) -> Poly:
    return poly(*(kneg(coefficient) for coefficient in value))


def psub(left: Poly, right: Poly) -> Poly:
    return padd(left, pneg(right))


def pmul(left: Poly, right: Poly) -> Poly:
    result = [KZERO] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] = kadd(result[i + j], kmul(a, b))
    return poly(*result)


def pscale(value: Poly, scalar: K) -> Poly:
    return poly(*(kmul(coefficient, scalar) for coefficient in value))


def ppow(value: Poly, exponent: int) -> Poly:
    result = PONE
    base = value
    power = exponent
    while power:
        if power & 1:
            result = pmul(result, base)
        base = pmul(base, base)
        power //= 2
    return result


def pderivative(value: Poly) -> Poly:
    return poly(*(kmul(value[index], k(index)) for index in range(1, len(value))))


def pdivmod(numerator: Poly, denominator: Poly) -> tuple[Poly, Poly]:
    require(denominator != PZERO, "polynomial division by zero")
    quotient = [KZERO] * max(1, len(numerator) - len(denominator) + 1)
    remainder = numerator
    while remainder != PZERO and len(remainder) >= len(denominator):
        shift = len(remainder) - len(denominator)
        coefficient = kdiv(remainder[-1], denominator[-1])
        quotient[shift] = kadd(quotient[shift], coefficient)
        term = poly(*([KZERO] * shift + [coefficient]))
        remainder = psub(remainder, pmul(term, denominator))
    return poly(*quotient), remainder


def pmonic(value: Poly) -> Poly:
    if value == PZERO:
        return PZERO
    return pscale(value, kinv(value[-1]))


def pgcd(left: Poly, right: Poly) -> Poly:
    a, b = left, right
    while b != PZERO:
        _, remainder = pdivmod(a, b)
        a, b = b, remainder
    return pmonic(a)


def encode_fraction(value: Fraction) -> list[int]:
    return [value.numerator, value.denominator]


def encode_k(value: K) -> list[list[int]]:
    return [encode_fraction(value[0]), encode_fraction(value[1])]


def encode_poly(value: Poly) -> list[list[list[int]]]:
    return [encode_k(coefficient) for coefficient in value]


def reconstruct() -> dict[str, Any]:
    zero_quadratic_monic = poly(
        k(
            Fraction(245313368811, 63975032888671),
            Fraction(2125523128760, 63975032888671),
        ),
        k(Fraction(-6015606986, 466971042983), Fraction(57336230440, 466971042983)),
        KONE,
    )
    y_cubic_monic = poly(
        k(
            Fraction(3470914422396071467, 246003008801584998484),
            Fraction(3524734958495214933, 246003008801584998484),
        ),
        k(
            Fraction(-41132016151102425, 897821200005784666),
            Fraction(-102197528668958349, 897821200005784666),
        ),
        k(
            Fraction(-7375440697652349, 13106878832201236),
            Fraction(5470553333510037, 13106878832201236),
        ),
        KONE,
    )
    zero_linear_monic = poly(
        k(Fraction(-7525603, 26828299), Fraction(3231308, 26828299)), KONE
    )
    common_denominator = poly(
        k(
            Fraction(
                115199196955188692732612390958141, 59550847529704598006265593404203587
            ),
            Fraction(
                -21191636945819867052568561572396, 59550847529704598006265593404203587
            ),
        ),
        k(
            Fraction(
                -7256998572641831201916840261321, 434677719194924073038434988351851
            ),
            Fraction(
                -2830458164407443580475664525648, 434677719194924073038434988351851
            ),
        ),
        k(
            Fraction(5786107670318005115319956322, 3172830067116234109769598455123),
            Fraction(156907531659855194532377896056, 3172830067116234109769598455123),
        ),
        k(
            Fraction(1107758998128604547852149806, 23159343555592949706347433979),
            Fraction(-3726769707713614340327541072, 23159343555592949706347433979),
        ),
        k(
            Fraction(-117466603467185355100327567, 169046303325495983258010467),
            Fraction(71155876092714139509324884, 169046303325495983258010467),
        ),
        KONE,
    )
    y_scalar = k(
        Fraction(163527897805116516195004856, 985897783628257595789418709),
        Fraction(-33187595386683500765127582, 985897783628257595789418709),
    )
    z_scalar = k(
        Fraction(1461814824033427547866298780, 46337195830528107002102679323),
        Fraction(-3351575570589461905345986720, 46337195830528107002102679323),
    )
    y_numerator = pscale(pmul(zero_quadratic_monic, y_cubic_monic), y_scalar)
    z_numerator = pscale(
        pmul(zero_linear_monic, ppow(zero_quadratic_monic, 2)), z_scalar
    )

    def mscale(expression, scalar):
        return {
            monomial: kmul(coefficient, scalar)
            for monomial, coefficient in expression.items()
            if kmul(coefficient, scalar) != KZERO
        }

    def madd(left, right):
        result = dict(left)
        for monomial, coefficient in right.items():
            result[monomial] = kadd(result.get(monomial, KZERO), coefficient)
            if result[monomial] == KZERO:
                del result[monomial]
        return result

    def shift(expression, dy, dz):
        return {
            (a + dy, b + dz): coefficient for (a, b), coefficient in expression.items()
        }

    powers = [({(0, 0): KONE}, {})]
    for _ in range(6):
        constant, coefficient = powers[-1]
        powers.append(
            (
                mscale(shift(coefficient, 0, 1), k(-1)),
                madd(constant, shift(coefficient, 1, 0)),
            )
        )
    n_coefficients = (
        KZERO,
        KZERO,
        KZERO,
        KZERO,
        KZERO,
        k(Fraction(-589286016, 648626449), Fraction(-350695008, 648626449)),
        k(Fraction(1902382848, 648626449), Fraction(67262400, 648626449)),
    )
    d_coefficients = (
        k(Fraction(-43658000, 648626449), Fraction(19666500, 648626449)),
        k(Fraction(31384800, 648626449), Fraction(-49794600, 648626449)),
        k(Fraction(-327741000, 648626449), Fraction(-75218250, 648626449)),
        k(Fraction(949516600, 648626449), Fraction(-142471950, 648626449)),
        k(Fraction(57591900, 2594505796), Fraction(-1006504575, 2594505796)),
        k(Fraction(1416912, 3074059), Fraction(2550981, 3074059)),
        KONE,
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
        result = PZERO
        for (y_degree, z_degree), coefficient in expression.items():
            term = pscale(
                pmul(
                    pmul(ppow(y_numerator, y_degree), ppow(z_numerator, z_degree)),
                    ppow(common_denominator, degree - y_degree - z_degree),
                ),
                coefficient,
            )
            result = padd(result, term)
        return result

    linear_zero = poly(k(-7525603, 3231308), k(26828299))
    quadratic_zero = poly(
        k(245313368811, 2125523128760),
        k(-824138157082, 7855063570280),
        k(63975032888671),
    )
    pole_linear = poly(k(-315829, -714826), k(9994287))
    pole_simple_quadratic = poly(
        k(132674139060063, 26804277479260),
        k(-417059633688806, -83725261001260),
        k(1991382275400503),
    )
    pole_double_quadratic = poly(
        k(12231162711693, -32963869775350),
        k(-462396480179036, 244927114639150),
        k(1132252914780903),
    )
    pole_double_quartic = poly(
        k(-1822586629728176676821274861, 1518418512706836664928299688),
        k(29110362047987136464064202740, 305715256120089609322000856),
        k(-11490078199717284397847774254, -48409713450897291507014287016),
        k(-126036323962081416795984038348, 58730298647562103476728792872),
        k(89003185037860639199185563123),
    )
    one_simple = poly(k(-15954935, 15312886), k(80312277))
    one_double = poly(k(-7890011, 5302214), k(33120709))
    one_four_linear = poly(k(-133093, 97604), k(875841))
    one_four_quadratic = poly(
        k(41237398279331, -13362808229176),
        k(-142615106443814, 55888632283576),
        k(360429781037043),
    )
    scalar_denominator = (
        38291961532478173866738244146012452994162275508013680941480795766620042899277
    )
    scalar = k(
        -Fraction(
            303676164503275686857828761462277732742134748079423674177208826215100553982356192,
            scalar_denominator,
        ),
        -Fraction(
            74513842597659582802909998886996270271709813890474407398463247982555397872842400,
            scalar_denominator,
        ),
    )
    quotient_n = pscale(pmul(ppow(linear_zero, 5), ppow(quadratic_zero, 5)), scalar)
    quotient_d = pmul(
        pmul(pole_linear, pole_simple_quadratic),
        pmul(ppow(pole_double_quadratic, 2), ppow(pole_double_quartic, 2)),
    )
    for part in range(2):
        cleared_n = clear_denominator(remainder_n[part])
        cleared_d = clear_denominator(remainder_d[part])
        require(
            pmul(cleared_n, quotient_d) == pmul(cleared_d, quotient_n),
            f"source remainder quotient part {part}",
        )

    difference = psub(quotient_n, quotient_d)
    expected_difference = pmul(
        pmul(one_simple, ppow(one_double, 2)),
        pmul(ppow(one_four_linear, 4), ppow(one_four_quadratic, 4)),
    )
    require(
        pmonic(difference) == pmonic(expected_difference), "one-fiber factorization"
    )

    fibers = (
        ((linear_zero, 5), (quadratic_zero, 5)),
        (
            (one_simple, 1),
            (one_double, 2),
            (one_four_linear, 4),
            (one_four_quadratic, 4),
        ),
        (
            (pole_linear, 1),
            (pole_simple_quadratic, 1),
            (pole_double_quadratic, 2),
            (pole_double_quartic, 2),
        ),
    )
    profiles = []
    for fiber in fibers:
        profile = sorted(
            (exponent for factor, exponent in fiber for _ in range(len(factor) - 1)),
            reverse=True,
        )
        profiles.append(profile)
        factors = [factor for factor, _ in fiber]
        for index, factor in enumerate(factors):
            require(
                pgcd(factor, pderivative(factor)) == PONE, "fiber factor squarefree"
            )
            for other in factors[index + 1 :]:
                require(pgcd(factor, other) == PONE, "fiber factors coprime")
    require(
        profiles == [[5, 5, 5], [4, 4, 4, 2, 1], [2, 2, 2, 2, 2, 2, 1, 1, 1]],
        "profiles",
    )
    require(pgcd(quotient_n, quotient_d) == PONE, "quotient coprime")
    require(
        sum(value - 1 for profile in profiles for value in profile) == 28,
        "Riemann-Hurwitz",
    )

    p = 2130706433
    nu_residues = [463918232, 1666788202]
    require(
        all((value * value - value + 4) % p == 0 for value in nu_residues),
        "coefficient embeddings",
    )

    def mod_field(value: K, nu_residue: int) -> int:
        return (
            int(value[0].numerator) * pow(int(value[0].denominator), -1, p)
            + int(value[1].numerator)
            * pow(int(value[1].denominator), -1, p)
            * nu_residue
        ) % p

    discriminants = []
    separations = []
    for nu_residue in nu_residues:
        a, b, c = (mod_field(value, nu_residue) for value in quadratic_zero[::-1])
        inverse_a = pow(a, -1, p)
        b = b * inverse_a % p
        c = c * inverse_a % p
        discriminants.append((b * b - 4 * c) % p)
        l0, l1 = (mod_field(value, nu_residue) for value in linear_zero)
        root = -l0 * pow(l1, -1, p) % p
        separations.append((root * root + b * root + c) % p)
        require(mod_field(scalar, nu_residue) != 0, "quotient scalar reduction")
    require(discriminants == [149224915, 1898905147], "zero discriminants")
    require(separations == [1501399179, 1964168949], "zero separations")

    def factor_packet(fiber):
        return [
            {"coefficients_ascending": encode_poly(factor), "exponent": exponent}
            for factor, exponent in fiber
        ]

    return {
        "statement": {
            "schema": "kb-mca-v4-m4-a6-542-pair-quotient-normal-form-v1",
            "terminal": "M4_A6_542_RIGID_PAIR_QUOTIENT_AND_POLE_DESCENT",
        },
        "parent_passport_reduction": {
            "commit": PARENT_COMMIT,
            "certificate_path": PARENT_PATH,
            "certificate_blob_oid": PARENT_BLOB,
            "certificate_payload_sha256": PARENT_PAYLOAD,
            "imported_terminal": "M4_A6S6_GEOMETRIC_FRONTIER_FOUR_PASSPORTS",
            "imported_passport": ["A6", ["5.1", "2.2.1.1", "4.2"]],
        },
        "source_companion": {
            "repository": "michaelmusty/BelyiDB",
            "commit": "7d5b899b0741ebd505363f7f811e5737e906abee",
            "path": "belyi_db/6/6T15-[5,4,2]-51-42-2211-g0.m",
            "blob_oid": "55e23bc1ef1d939329a5a6b377d03c07f0ac9f2d",
            "label": "6T15-[5,4,2]-51-42-2211-g0",
        },
        "coefficient_field": {
            "minimal_polynomial": "nu^2-nu+4",
            "discriminant": -15,
        },
        "pair_model": {
            "construction": "rank_eight_cubic_adjoint_normalization_of_unordered_pair_quintic",
            "zero_quadratic_monic": encode_poly(zero_quadratic_monic),
            "y_cubic_monic": encode_poly(y_cubic_monic),
            "zero_linear_monic": encode_poly(zero_linear_monic),
            "common_denominator_monic": encode_poly(common_denominator),
            "y_scalar": encode_k(y_scalar),
            "z_scalar": encode_k(z_scalar),
        },
        "quotient": {
            "degree": 15,
            "scalar": encode_k(scalar),
            "zero_factors": factor_packet(fibers[0]),
            "one_factors": factor_packet(fibers[1]),
            "pole_factors": factor_packet(fibers[2]),
            "fiber_profiles": profiles,
            "total_branch_index": 28,
        },
        "challenge_field": {
            "p": p,
            "extension_degree": 6,
            "nu_residues": nu_residues,
            "zero_quadratic_discriminants": discriminants,
            "zero_linear_quadratic_separations": separations,
            "pole_fiber_splits": True,
        },
        "conclusion": {
            "passport": ["A6", ["5.1", "2.2.1.1", "4.2"]],
            "terminal": "M4_A6_542_RIGID_PAIR_QUOTIENT_AND_POLE_DESCENT",
            "impact": "THIRD_OF_THREE_RIGID_M4_PASSPORTS_EXPLICIT_POLE_DESCENT_PROVED",
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
    require(
        git_output("rev-parse", f"{PARENT_COMMIT}:{PARENT_PATH}") == PARENT_BLOB,
        "parent blob",
    )
    parent = parse_json(
        git_output("show", f"{PARENT_COMMIT}:{PARENT_PATH}"), "parent certificate"
    )
    require(
        payload_hash(parent) == parent["payload_sha256"] == PARENT_PAYLOAD,
        "parent payload",
    )
    require(
        data["parent_passport_reduction"]["imported_passport"]
        in parent["conclusion"]["retained"],
        "parent passport",
    )


def verify_certificate(
    data: dict[str, Any], check_git: bool = True, expected=None
) -> None:
    exact_keys(
        data,
        {
            "payload_sha256",
            "statement",
            "parent_passport_reduction",
            "source_companion",
            "coefficient_field",
            "pair_model",
            "quotient",
            "challenge_field",
            "conclusion",
            "nonclaims",
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
        (
            "parent",
            lambda row: row["parent_passport_reduction"].__setitem__(
                "certificate_blob_oid", "0" * 40
            ),
        ),
        (
            "source",
            lambda row: row["source_companion"].__setitem__("blob_oid", "0" * 40),
        ),
        ("field", lambda row: row["coefficient_field"].__setitem__("discriminant", -7)),
        ("parameter", lambda row: row["pair_model"]["common_denominator_monic"].pop()),
        ("degree", lambda row: row["quotient"].__setitem__("degree", 14)),
        ("scalar", lambda row: row["quotient"]["scalar"].pop()),
        (
            "zero",
            lambda row: row["quotient"]["zero_factors"][0].__setitem__("exponent", 4),
        ),
        ("one", lambda row: row["quotient"]["one_factors"].pop()),
        ("pole", lambda row: row["quotient"]["pole_factors"].pop()),
        ("profile", lambda row: row["quotient"]["fiber_profiles"][1].pop()),
        ("index", lambda row: row["quotient"].__setitem__("total_branch_index", 27)),
        ("embedding", lambda row: row["challenge_field"]["nu_residues"].pop()),
        (
            "split",
            lambda row: row["challenge_field"].__setitem__("pole_fiber_splits", False),
        ),
        ("passport", lambda row: row["conclusion"].__setitem__("passport", ["S6", []])),
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
        print("PASS: rigid A6 [5,4,2] pair quotient and pole descent")
        if args.tamper_selftest:
            count = tamper_selftest(data, expected)
            print(f"PASS: {count}/{count} tamper mutations rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
