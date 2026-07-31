#!/usr/bin/env python3
"""Verify one fixed-moving aligned-positive crossed representative."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable

if not __debug__:
    print("REFUSE: optimized Python is unsupported", file=sys.stderr)
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE = (
    ROOT
    / "experimental/data/certificates/"
    "kb-mca-v4-m2-diagonal-112-fixed-positive-crossed-v1/"
    "kb_mca_v4_m2_diagonal_112_fixed_positive_crossed_v1.json"
)
SAGE_REPLAY = (
    ROOT
    / "experimental/scripts/"
    "verify_kb_mca_v4_m2_diagonal_112_fixed_positive_crossed_v1.sage"
)
SINGULAR_REPLAY = (
    ROOT
    / "experimental/scripts/"
    "verify_kb_mca_v4_m2_diagonal_112_fixed_positive_crossed_v1.sing"
)
WOLFRAM_REPLAY = (
    ROOT
    / "experimental/scripts/"
    "verify_kb_mca_v4_m2_diagonal_112_fixed_positive_crossed_v1.wl"
)
PRIME = 2130706433
SAGE_OUTPUT_PAYLOAD = (
    "38ee51ae4fbf76f97cbf4382b55c13c81820c2eeab45387a0cbc3942316673c6"
)

SOURCE_FACET_PARENT = {
    "certificate_blob_oid": "844b7885620bf10fe19336f3acd7866cf1d9a204",
    "certificate_path": (
        "experimental/data/certificates/"
        "kb-mca-v4-m2-u2-universal-source-facet-census-v1/"
        "kb_mca_v4_m2_u2_universal_source_facet_census_v1.json"
    ),
    "commit": "c2edcfa5cbfb8a41e7dea04ae1b34325c90ed5dc",
    "note_blob_oid": "cc315015998cf9ab0ecf2970c13f1e27f1f132d6",
    "note_path": (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_m2_u2_universal_source_facet_census_v1.md"
    ),
    "verifier_blob_oid": "e810f286d5b67d19660c3c382501a690e3e76fb0",
    "verifier_path": (
        "experimental/scripts/"
        "verify_kb_mca_v4_m2_u2_universal_source_facet_census_v1.py"
    ),
}
PREDECESSOR = {
    "certificate_blob_oid": "b585fac976632789f979773b445da5bb82438a4b",
    "certificate_path": (
        "experimental/data/certificates/"
        "kb-mca-v4-m2-diagonal-112-near-negative-qslice-v1/"
        "kb_mca_v4_m2_diagonal_112_near_negative_qslice_v1.json"
    ),
    "commit": "84d35eca57609057a7226f1054501f3885014874",
    "note_blob_oid": "d8d52aa81ffdaa6736b7f5dc16c1b3c9c4bc2a97",
    "note_path": (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_m2_diagonal_112_near_negative_qslice_v1.md"
    ),
    "verifier_blob_oid": "0aeaa65ba8097ebeaf9390bf7fa39f58f8c40180",
    "verifier_path": (
        "experimental/scripts/"
        "verify_kb_mca_v4_m2_diagonal_112_near_negative_qslice_v1.py"
    ),
}


class VerificationError(RuntimeError):
    """A deterministic certificate check failed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def canonical_bytes(data: dict[str, Any]) -> bytes:
    return (
        json.dumps(data, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    ).encode()


def load_certificate() -> dict[str, Any]:
    raw = CERTIFICATE.read_bytes()
    data = json.loads(
        raw.decode(),
        object_pairs_hook=reject_duplicate_keys,
    )
    require(raw == canonical_bytes(data), "certificate canonical formatting")
    return data


def payload_hash(data: dict[str, Any]) -> str:
    payload = copy.deepcopy(data)
    payload.pop("payload_sha256", None)
    encoded = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob(commit: str, path: str) -> str:
    process = subprocess.run(
        ["git", "rev-parse", f"{commit}:{path}"],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    require(process.returncode == 0, f"missing pinned path: {commit}:{path}")
    return process.stdout.strip()


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for divisor in small:
        if value % divisor == 0:
            return value == divisor
    odd_part = value - 1
    exponent = 0
    while odd_part % 2 == 0:
        exponent += 1
        odd_part //= 2
    for base in (2, 3, 5, 7, 11):
        residue = pow(base, odd_part, value)
        if residue in (1, value - 1):
            continue
        for _ in range(exponent - 1):
            residue = residue * residue % value
            if residue == value - 1:
                break
        else:
            return False
    return True


def poly_trim(poly: list[int], prime: int) -> list[int]:
    result = [coefficient % prime for coefficient in poly]
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result or [0]


def poly_add(left: list[int], right: list[int], prime: int) -> list[int]:
    return poly_trim(
        [
            (
                (left[index] if index < len(left) else 0)
                + (right[index] if index < len(right) else 0)
            )
            % prime
            for index in range(max(len(left), len(right)))
        ],
        prime,
    )


def poly_scale(poly: list[int], scalar: int, prime: int) -> list[int]:
    return poly_trim([scalar * coefficient for coefficient in poly], prime)


def poly_multiply(
    left: list[int], right: list[int], prime: int
) -> list[int]:
    result = [0] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            result[left_index + right_index] = (
                result[left_index + right_index] + left_value * right_value
            ) % prime
    return poly_trim(result, prime)


def poly_remainder(
    dividend: list[int], divisor: list[int], prime: int
) -> list[int]:
    work = poly_trim(dividend, prime)
    divisor = poly_trim(divisor, prime)
    require(divisor != [0], "polynomial division by zero")
    inverse_lead = pow(divisor[-1], -1, prime)
    while work != [0] and len(work) >= len(divisor):
        shift = len(work) - len(divisor)
        coefficient = work[-1] * inverse_lead % prime
        for index, value in enumerate(divisor):
            work[index + shift] = (
                work[index + shift] - coefficient * value
            ) % prime
        work = poly_trim(work, prime)
    return work


def poly_multiply_mod(
    left: list[int],
    right: list[int],
    modulus: list[int],
    prime: int,
) -> list[int]:
    return poly_remainder(poly_multiply(left, right, prime), modulus, prime)


def poly_power_mod(
    base: list[int], exponent: int, modulus: list[int], prime: int
) -> list[int]:
    result = [1]
    base = poly_remainder(base, modulus, prime)
    while exponent:
        if exponent & 1:
            result = poly_multiply_mod(result, base, modulus, prime)
        base = poly_multiply_mod(base, base, modulus, prime)
        exponent >>= 1
    return result


def substitute_d_mod_component(
    terms: list[list[int]],
    d_polynomial: list[int],
    modulus: list[int],
    prime: int,
) -> list[int]:
    result = [0]
    for d_exponent, c_exponent, coefficient in terms:
        term = poly_multiply_mod(
            poly_power_mod(d_polynomial, d_exponent, modulus, prime),
            poly_power_mod([0, 1], c_exponent, modulus, prime),
            modulus,
            prime,
        )
        result = poly_remainder(
            poly_add(result, poly_scale(term, coefficient, prime), prime),
            modulus,
            prime,
        )
    return result


EXPECTED_E0 = [
    [4, 2, 4],
    [3, 2, -120],
    [4, 1, 8],
    [2, 2, 193],
    [3, 1, 120],
    [4, 0, 4],
    [1, 2, -84],
    [2, 1, -262],
    [3, 0, -84],
    [0, 2, 4],
    [1, 1, 120],
    [2, 0, 193],
    [0, 1, 8],
    [1, 0, -120],
    [0, 0, 4],
]
EXPECTED_E1 = [
    [2, 4, 4],
    [1, 4, 8],
    [2, 3, -120],
    [0, 4, 4],
    [1, 3, 120],
    [2, 2, 193],
    [0, 3, -84],
    [1, 2, -262],
    [2, 1, -84],
    [0, 2, 193],
    [1, 1, 120],
    [2, 0, 4],
    [0, 1, -120],
    [1, 0, 8],
    [0, 0, 4],
]
EXPECTED_FACTORS = {
    "c_minus_2": [-2, 1],
    "h": [100, -504, 817, -504, 100],
    "q2": [1, -14, 1],
    "q6": [4, -112, 317, -430, 317, -112, 4],
    "two_c_minus_1": [-1, 2],
}
EXPECTED_COMPONENTS = [
    {
        "factor": "2c-1",
        "multiplicity": 3,
        "terminal": "c=1/2 fixed-label collision",
    },
    {
        "factor": "c-2",
        "multiplicity": 3,
        "terminal": "c=2 fixed-label collision",
    },
    {
        "factor": "q2",
        "multiplicity": 1,
        "terminal": "cd=1 reciprocal-label collision",
    },
    {
        "factor": "q6",
        "multiplicity": 1,
        "terminal": "d=c equal-label collision",
    },
    {
        "factor": "h",
        "multiplicity": 1,
        "terminal": "full quotient J and I coefficient-one mismatch",
    },
]
EXPECTED_QUOTIENT = {
    "I": {
        "bezout_h": [450536384, 1582407299, 134274715],
        "bezout_mismatch": [
            1149576513,
            264697898,
            1366419164,
            1452206296,
        ],
        "mismatch": [
            1474202438,
            1474392606,
            1373289511,
            1777964224,
        ],
    },
    "J": {
        "bezout_h": [1378984398, 161871344, 481856514],
        "bezout_mismatch": [
            1355798505,
            577218842,
            1092963338,
            2108730127,
        ],
        "mismatch": [
            1265012543,
            2079603121,
            44715398,
            1153095255,
        ],
    },
    "coefficient_index": 1,
    "identities_tested": [
        "Q_J proportional to K_5^2 chi_Omega",
        "chi_Omega Q_I proportional to R_7^2",
    ],
}


def verify_provenance(provenance: dict[str, Any]) -> None:
    require(
        provenance
        == {
            "predecessor": PREDECESSOR,
            "source_facet_parent": SOURCE_FACET_PARENT,
        },
        "exact provenance",
    )
    for parent_name, parent in provenance.items():
        for kind in ("certificate", "note", "verifier"):
            require(
                git_blob(parent["commit"], parent[f"{kind}_path"])
                == parent[f"{kind}_blob_oid"],
                f"{parent_name} {kind} blob binding",
            )


def verify_h9(h9: dict[str, Any], prime: int) -> None:
    require(h9["component_partition"] == EXPECTED_COMPONENTS, "H9 components")
    require(h9["e0_terms_d_c_coefficient"] == EXPECTED_E0, "H9 e0")
    require(h9["e1_terms_d_c_coefficient"] == EXPECTED_E1, "H9 e1")
    require(h9["eliminant_degree"] == 18, "H9 eliminant degree")
    require(
        h9["eliminant_factors_low_to_high"] == EXPECTED_FACTORS,
        "H9 eliminant factors",
    )
    require(h9["groebner_basis_size"] == 3, "H9 Groebner basis size")
    require(
        h9["h_d_relation_low_to_high"] == [-1400, 7241, -6664, 1600],
        "H9 h-component relation",
    )
    require(h9["full_quotient"] == EXPECTED_QUOTIENT, "H9 quotient witnesses")
    require(
        h9["h_factorization_mod_p"]
        == {
            "factor_one": [1210481498, 272520209, 1],
            "factor_two": [1516822740, 1602501447, 1],
            "scalar": 100,
        },
        "H9 quartic factorization record",
    )

    factors = h9["eliminant_factors_low_to_high"]
    eliminant = [1]
    for name, multiplicity in (
        ("two_c_minus_1", 3),
        ("c_minus_2", 3),
        ("q2", 1),
        ("q6", 1),
        ("h", 1),
    ):
        for _ in range(multiplicity):
            eliminant = poly_multiply(eliminant, factors[name], prime)
    require(len(eliminant) - 1 == h9["eliminant_degree"], "factor degree sum")

    h = factors["h"]
    factorization = h9["h_factorization_mod_p"]
    reconstructed_h = poly_scale(
        poly_multiply(
            factorization["factor_one"],
            factorization["factor_two"],
            prime,
        ),
        factorization["scalar"],
        prime,
    )
    require(
        reconstructed_h == poly_trim(h, prime),
        "native characteristic h factorization",
    )

    component_data = (
        ("q2", [14, -1]),
        ("q6", [0, 1]),
        (
            "h",
            [
                coefficient * pow(375, -1, prime) % prime
                for coefficient in h9["h_d_relation_low_to_high"]
            ],
        ),
    )
    for component_name, d_polynomial in component_data:
        modulus = factors[component_name]
        for equation_name in (
            "e0_terms_d_c_coefficient",
            "e1_terms_d_c_coefficient",
        ):
            require(
                substitute_d_mod_component(
                    h9[equation_name],
                    d_polynomial,
                    modulus,
                    prime,
                )
                == [0],
                f"{component_name} satisfies {equation_name[:2]}",
            )

    for side in ("I", "J"):
        record = h9["full_quotient"][side]
        combination = poly_add(
            poly_multiply(record["bezout_h"], h, prime),
            poly_multiply(
                record["bezout_mismatch"], record["mismatch"], prime
            ),
            prime,
        )
        require(combination == [1], f"{side} full-quotient Bezout identity")


def verify_data(data: dict[str, Any]) -> None:
    require(
        set(data)
        == {
            "artifacts",
            "assignment_scope",
            "branch_partition",
            "conclusion",
            "field",
            "h8",
            "h9",
            "normalization",
            "nonclaims",
            "payload_sha256",
            "provenance",
            "schema",
            "scope",
            "workboard",
        },
        "top-level fields",
    )
    require(
        data["schema"]
        == "kb-mca-v4-m2-diagonal-112-fixed-positive-crossed-v1",
        "schema",
    )
    require(data["payload_sha256"] == payload_hash(data), "payload hash")
    require(
        data["scope"]
        == {
            "assignment": "{{2,1/2},{2,b}}",
            "assignment_quantifier": "SINGLE_NORMALIZED_REPRESENTATIVE",
            "ledger_movement": 0,
            "profile": "(a,b,c)=(1,1,2)",
            "root_distribution": [0, 2],
            "source_branch": "saturated source-line",
            "target": (
                "normalized fixed-moving aligned-positive crossed "
                "representative"
            ),
        },
        "scope",
    )
    require(
        data["assignment_scope"]
        == {
            "closed_assignment_count": 1,
            "complete_system_covariance": "NOT_CLAIMED",
            "covariance_mismatch": {
                "diagonal_W_transport": (
                    "preserves aligned target but not observed "
                    "residual/source W divisor"
                ),
                "endpoint_only_normalizer": (
                    "preserves observed residual side but not aligned target"
                ),
            },
            "fixed_moving_assignment_count": 8,
            "open_assignment_count": 7,
            "other_assignments_status": "OPEN_SEPARATE_EXACT_SYSTEMS",
            "status": "REPRESENTATIVE_ONLY",
        },
        "assignment scope",
    )
    require(
        data["workboard"]
        == {
            "B_star": 274980728111395087,
            "agreement": 1116048,
            "architecture": None,
            "atom_or_cell": (
                "K3_M2_DIAGONAL_112_FIXED_POSITIVE_CROSSED_0_2_"
                "REPRESENTATIVE"
            ),
            "impact": "ROUTE_CUT_LOCAL_ONLY",
            "object": "MCA",
            "row": "KoalaBear MCA at 2^-128",
            "target_epsilon": "2^-128",
            "workboard_item": "K3",
        },
        "workboard",
    )
    require(
        data["field"]
        == {
            "challenge_extension_degree": 6,
            "prime": PRIME,
            "prime_avoids": [2, 3, 5],
        },
        "field",
    )
    require(is_prime(data["field"]["prime"]), "deployed characteristic prime")
    require(
        data["normalization"]
        == {
            "J0": ["2", "1/2", "b", "1/b"],
            "J1": ["c", "d"],
            "deck": "tau(x)=1/x",
            "fixed_moving_edges": [["2", "1/2"], ["2", "b"]],
            "root_distribution": [0, 2],
        },
        "normalization",
    )
    require(
        data["conclusion"]
        == {
            "complete_112_row_deleted": False,
            "complete_system_covariance": "NOT_CLAIMED",
            "k3_status": "OPEN",
            "koalabear_row_status": "OPEN",
            "ledger_movement": 0,
            "moving_moving_status": "OPEN",
            "other_fixed_moving_assignment_count": 7,
            "other_fixed_moving_assignments_status": (
                "OPEN_SEPARATE_EXACT_SYSTEMS"
            ),
            "positive_1_1_status": "OPEN",
            "positive_2_0_status": "OPEN",
            "representative_fixed_moving_crossed_0_2_empty": True,
        },
        "conclusion",
    )
    require(
        data["branch_partition"]
        == {
            "c_choice_count": 2,
            "c_choice_one": {
                "d_choice_one": "H9",
                "d_choice_zero": "H8",
            },
            "c_choice_zero": {
                "d_choices_deleted": 2,
                "required_nonzero_factorization": [
                    ["d", 1],
                    ["w-d", 2],
                    ["w-1", 2],
                    ["w+1", 2],
                    ["d-2", 2],
                    ["2d-1", 2],
                    ["c-1", 2],
                    ["c+1", 2],
                    ["A", 2],
                    ["cd-1", 4],
                ],
            },
            "d_choice_count_per_c_choice": 2,
            "degenerate_linear_splits": {
                "initial_b_coefficient_and_constant_zero": {
                    "charts": [[0, 0], [0, 1], [1, 0], [1, 1]],
                    "localized_groebner_bases": ["1", "1", "1", "1"],
                    "localizer": (
                        "Hbasic; additionally d-w on c_choice=0"
                    ),
                },
                "later_w_coefficient_and_constant_zero": {
                    "charts": [0, 1],
                    "localized_groebner_bases": ["1", "1"],
                    "localizer": (
                        "substituted Hbasic times the nonzero b coefficient "
                        "and all introduced denominators"
                    ),
                },
                "rabinowitsch_equation": "t*H-1",
            },
            "normal_branch_count": 4,
        },
        "branch partition",
    )
    require(
        data["h8"]
        == {
            "collision": "w=c",
            "retained_factor": "c+d",
            "retained_factor_exponent": 2,
            "w_denominator_on_d_minus_c_coefficients": [0, -10, 10],
            "w_numerator_minus_c_denominator_on_d_minus_c_coefficients": [0],
            "w_numerator_on_d_minus_c_coefficients": [0, 0, -10, 10],
        },
        "H8 record",
    )
    h8 = data["h8"]
    require(
        poly_add(
            h8["w_numerator_on_d_minus_c_coefficients"],
            poly_scale(
                poly_multiply(
                    [0, 1],
                    h8["w_denominator_on_d_minus_c_coefficients"],
                    PRIME,
                ),
                -1,
                PRIME,
            ),
            PRIME,
        )
        == [0],
        "H8 w=c identity",
    )
    verify_h9(data["h9"], PRIME)
    require(
        data["nonclaims"]
        == [
            "no claim for the other seven fixed-moving assignments",
            "no projective covariance claim for the complete source system",
            "no claim for the separately derived positive root distribution (2,0)",
            "no balanced positive (1,1) deletion",
            "no moving-moving deletion",
            "no near-aligned positive deletion",
            "no exceptional unsaturated-orbit or biquadratic-source-cover deletion",
            "no complete (1,1,2) row deletion",
            "no owner, payment, K3 value, KoalaBear row bound, or Prize closure",
        ],
        "nonclaims",
    )
    verify_provenance(data["provenance"])
    artifacts = data["artifacts"]
    require(
        artifacts
        == {
            "sage_output_payload_sha256": SAGE_OUTPUT_PAYLOAD,
            "sage_sha256": file_hash(SAGE_REPLAY),
            "singular_sha256": file_hash(SINGULAR_REPLAY),
            "wolfram_sha256": file_hash(WOLFRAM_REPLAY),
        },
        "artifact bindings",
    )


def tamper_selftest(data: dict[str, Any]) -> int:
    mutations: list[Callable[[dict[str, Any]], None]] = [
        lambda x: x.__setitem__("schema", "wrong"),
        lambda x: x.__setitem__("payload_sha256", "0" * 64),
        lambda x: x["scope"].__setitem__("ledger_movement", 1),
        lambda x: x["scope"].__setitem__("profile", "(2,0,1)"),
        lambda x: x["scope"]["root_distribution"].reverse(),
        lambda x: x["scope"].__setitem__("source_branch", "biquadratic"),
        lambda x: x["scope"].__setitem__("target", "wrong"),
        lambda x: x["scope"].__setitem__(
            "assignment_quantifier", "FULL_ORBIT"
        ),
        lambda x: x["scope"].__setitem__(
            "assignment", "{{2,1/2},{1/2,b}}"
        ),
        lambda x: x["assignment_scope"].__setitem__("status", "FULL_ORBIT"),
        lambda x: x["assignment_scope"].__setitem__(
            "complete_system_covariance", "PROVED"
        ),
        lambda x: x["assignment_scope"].__setitem__(
            "other_assignments_status", "CLOSED"
        ),
        lambda x: x["assignment_scope"].__setitem__(
            "closed_assignment_count", 8
        ),
        lambda x: x["assignment_scope"].__setitem__(
            "fixed_moving_assignment_count", 1
        ),
        lambda x: x["assignment_scope"].__setitem__(
            "open_assignment_count", 0
        ),
        lambda x: x["assignment_scope"]["covariance_mismatch"].__setitem__(
            "endpoint_only_normalizer", "preserves complete system"
        ),
        lambda x: x["workboard"].__setitem__("agreement", 1116047),
        lambda x: x["workboard"].__setitem__("B_star", 0),
        lambda x: x["workboard"].__setitem__("atom_or_cell", "wrong"),
        lambda x: x["workboard"].__setitem__("impact", "PAYMENT"),
        lambda x: x["field"].__setitem__("prime", 43),
        lambda x: x["field"].__setitem__("challenge_extension_degree", 1),
        lambda x: x["field"]["prime_avoids"].pop(),
        lambda x: x["normalization"]["J0"].reverse(),
        lambda x: x["normalization"]["J1"].reverse(),
        lambda x: x["normalization"].__setitem__("deck", "tau(x)=x"),
        lambda x: x["normalization"]["fixed_moving_edges"][1].reverse(),
        lambda x: x["normalization"]["root_distribution"].reverse(),
        lambda x: x["conclusion"].__setitem__(
            "representative_fixed_moving_crossed_0_2_empty", False
        ),
        lambda x: x["conclusion"].__setitem__(
            "complete_system_covariance", "PROVED"
        ),
        lambda x: x["conclusion"].__setitem__(
            "other_fixed_moving_assignments_status", "CLOSED"
        ),
        lambda x: x["conclusion"].__setitem__(
            "other_fixed_moving_assignment_count", 0
        ),
        lambda x: x["conclusion"].__setitem__("complete_112_row_deleted", True),
        lambda x: x["conclusion"].__setitem__("positive_1_1_status", "CLOSED"),
        lambda x: x["conclusion"].__setitem__("positive_2_0_status", "CLOSED"),
        lambda x: x["conclusion"].__setitem__("moving_moving_status", "CLOSED"),
        lambda x: x["conclusion"].__setitem__("ledger_movement", 1),
        lambda x: x["branch_partition"].__setitem__("c_choice_count", 1),
        lambda x: x["branch_partition"].__setitem__("normal_branch_count", 3),
        lambda x: x["branch_partition"]["c_choice_zero"].__setitem__(
            "d_choices_deleted", 1
        ),
        lambda x: x["branch_partition"]["c_choice_zero"][
            "required_nonzero_factorization"
        ].pop(),
        lambda x: x["branch_partition"]["c_choice_one"].__setitem__(
            "d_choice_zero", "H9"
        ),
        lambda x: x["branch_partition"]["degenerate_linear_splits"][
            "initial_b_coefficient_and_constant_zero"
        ]["charts"].pop(),
        lambda x: x["branch_partition"]["degenerate_linear_splits"][
            "initial_b_coefficient_and_constant_zero"
        ]["localized_groebner_bases"].__setitem__(0, "nonunit"),
        lambda x: x["branch_partition"]["degenerate_linear_splits"][
            "later_w_coefficient_and_constant_zero"
        ]["charts"].pop(),
        lambda x: x["branch_partition"]["degenerate_linear_splits"].__setitem__(
            "rabinowitsch_equation", "t*H"
        ),
        lambda x: x["h8"].__setitem__("collision", "d=c"),
        lambda x: x["h8"].__setitem__("retained_factor", "c-d"),
        lambda x: x["h8"].__setitem__("retained_factor_exponent", 1),
        lambda x: x["h8"]["w_numerator_on_d_minus_c_coefficients"].__setitem__(
            2, -9
        ),
        lambda x: x[
            "h8"
        ]["w_denominator_on_d_minus_c_coefficients"].__setitem__(1, -9),
        lambda x: x["h9"]["component_partition"][2].__setitem__(
            "terminal", "owner"
        ),
        lambda x: x["h9"]["component_partition"][4].__setitem__(
            "multiplicity", 2
        ),
        lambda x: x["h9"]["e0_terms_d_c_coefficient"][0].__setitem__(2, 5),
        lambda x: x["h9"]["e1_terms_d_c_coefficient"][1].__setitem__(2, 9),
        lambda x: x["h9"].__setitem__("eliminant_degree", 17),
        lambda x: x["h9"]["eliminant_factors_low_to_high"]["q2"].__setitem__(
            1, -13
        ),
        lambda x: x["h9"]["eliminant_factors_low_to_high"]["q6"].pop(),
        lambda x: x["h9"]["eliminant_factors_low_to_high"]["h"].__setitem__(
            2, 818
        ),
        lambda x: x["h9"].__setitem__("groebner_basis_size", 2),
        lambda x: x["h9"]["h_d_relation_low_to_high"].__setitem__(0, -1399),
        lambda x: x["h9"]["h_factorization_mod_p"].__setitem__("scalar", 99),
        lambda x: x["h9"]["h_factorization_mod_p"]["factor_one"].__setitem__(
            0, 0
        ),
        lambda x: x["h9"]["full_quotient"].__setitem__(
            "coefficient_index", 2
        ),
        lambda x: x["h9"]["full_quotient"]["identities_tested"].reverse(),
        lambda x: x["h9"]["full_quotient"]["J"]["mismatch"].__setitem__(0, 0),
        lambda x: x["h9"]["full_quotient"]["I"]["bezout_h"].__setitem__(0, 0),
        lambda x: x["h9"]["full_quotient"]["J"][
            "bezout_mismatch"
        ].__setitem__(0, 0),
        lambda x: x["provenance"]["predecessor"].__setitem__(
            "commit", "0" * 40
        ),
        lambda x: x["provenance"]["predecessor"].__setitem__(
            "note_blob_oid", "0" * 40
        ),
        lambda x: x["provenance"]["source_facet_parent"].__setitem__(
            "verifier_blob_oid", "0" * 40
        ),
        lambda x: x["artifacts"].__setitem__("sage_sha256", "0" * 64),
        lambda x: x["artifacts"].__setitem__("singular_sha256", "0" * 64),
        lambda x: x["artifacts"].__setitem__("wolfram_sha256", "0" * 64),
        lambda x: x["artifacts"].__setitem__(
            "sage_output_payload_sha256", "0" * 64
        ),
        lambda x: x["nonclaims"].pop(),
    ]
    rejected = 0
    accepted: list[int] = []
    payload_only_mutation = 1
    for mutation_index, mutation in enumerate(mutations):
        candidate = copy.deepcopy(data)
        mutation(candidate)
        if mutation_index != payload_only_mutation:
            candidate["payload_sha256"] = payload_hash(candidate)
        try:
            verify_data(candidate)
        except (
            VerificationError,
            IndexError,
            KeyError,
            TypeError,
            ValueError,
            ZeroDivisionError,
        ):
            rejected += 1
        else:
            accepted.append(mutation_index)
    require(
        rejected == len(mutations),
        f"tamper rejection count; accepted={accepted}",
    )
    return rejected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    require(args.check or args.tamper_selftest, "select a verifier mode")
    data = load_certificate()
    verify_data(data)
    print(
        "PASS representative fixed-positive crossed (0,2) "
        f"payload={data['payload_sha256']} "
        "terminal=EMPTY other_assignments=OPEN_7 covariance=NOT_CLAIMED"
    )
    if args.tamper_selftest:
        rejected = tamper_selftest(data)
        print(f"PASS tamper self-test: {rejected}/{rejected} rejected")


if __name__ == "__main__":
    main()
