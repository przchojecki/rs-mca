#!/usr/bin/env python3
"""Verify one fixed-moving aligned-positive identity-doubled representative."""

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
    "kb-mca-v4-m2-diagonal-112-fixed-positive-identity-v1/"
    "kb_mca_v4_m2_diagonal_112_fixed_positive_identity_v1.json"
)
SAGE_REPLAY = (
    ROOT
    / "experimental/scripts/"
    "verify_kb_mca_v4_m2_diagonal_112_fixed_positive_identity_v1.sage"
)
SINGULAR_REPLAY = (
    ROOT
    / "experimental/scripts/"
    "verify_kb_mca_v4_m2_diagonal_112_fixed_positive_identity_v1.sing"
)
WOLFRAM_REPLAY = (
    ROOT
    / "experimental/scripts/"
    "verify_kb_mca_v4_m2_diagonal_112_fixed_positive_identity_v1.wl"
)
PRIME = 2130706433
SAGE_OUTPUT_PAYLOAD = (
    "47a0b79c0cc2e8c3c1ad0265c8214075e92366bb6f6d4339d8bbe07a098f4852"
)
CROSSED_PAYLOAD = (
    "ec52873035a42fec4c3f19f429913197df872487c2a6137646dd81474c6fedf7"
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
    "assignment": "{{2,1/2},{2,b}}",
    "assignment_quantifier": "SINGLE_NORMALIZED_REPRESENTATIVE",
    "certificate_blob_oid": "31cddc835ed2e896aa1d94a953ea8518362628c8",
    "certificate_path": (
        "experimental/data/certificates/"
        "kb-mca-v4-m2-diagonal-112-fixed-positive-crossed-v1/"
        "kb_mca_v4_m2_diagonal_112_fixed_positive_crossed_v1.json"
    ),
    "commit": "f0a1d20ea16721d9596a3520658406528f5ade9f",
    "note_blob_oid": "983439be8d47cd2db229c5289ca07fbcf4ea8360",
    "note_path": (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_m2_diagonal_112_fixed_positive_crossed_v1.md"
    ),
    "other_assignments_status": "OPEN_SEPARATE_EXACT_SYSTEMS",
    "payload_sha256": CROSSED_PAYLOAD,
    "verifier_blob_oid": "581d196f24836c0247c01ef09268def2f5878cae",
    "verifier_path": (
        "experimental/scripts/"
        "verify_kb_mca_v4_m2_diagonal_112_fixed_positive_crossed_v1.py"
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
    data = json.loads(raw.decode(), object_pairs_hook=reject_duplicate_keys)
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


def git_json(commit: str, path: str) -> dict[str, Any]:
    process = subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    require(process.returncode == 0, f"missing pinned JSON: {commit}:{path}")
    return json.loads(
        process.stdout, object_pairs_hook=reject_duplicate_keys
    )


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    for divisor in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
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


EXPECTED_FACTORS = {
    "c_minus_1": [-1, 1],
    "c_minus_2": [-2, 1],
    "c_plus_1": [1, 1],
    "f10": [
        36,
        -352,
        1741,
        -5266,
        9871,
        -12124,
        9871,
        -5266,
        1741,
        -352,
        36,
    ],
    "f6": [9, -82, 119, -156, 119, -82, 9],
    "f8": [324, -5328, 29617, -77552, 106134, -77552, 29617, -5328, 324],
    "two_c_minus_1": [-1, 2],
}
EXPECTED_COMPONENTS = [
    {
        "factor": "c-2",
        "multiplicity": 4,
        "terminal": "c=2 fixed-label collision",
    },
    {
        "factor": "2c-1",
        "multiplicity": 4,
        "terminal": "c=1/2 fixed-label collision",
    },
    {
        "factor": "c-1",
        "multiplicity": 10,
        "terminal": "c=1 deck fixed-point collision",
    },
    {
        "factor": "c+1",
        "multiplicity": 10,
        "terminal": "c=-1 deck fixed-point collision",
    },
    {
        "factor": "f6",
        "multiplicity": 1,
        "terminal": "cd=1 reciprocal-label and w=1 fixed-label collisions",
    },
    {
        "factor": "f8",
        "multiplicity": 1,
        "terminal": "full quotient J and I coefficient-one mismatch",
    },
    {
        "factor": "f10",
        "multiplicity": 1,
        "terminal": "d=c equal-label collision",
    },
]
EXPECTED_QUOTIENT = {
    "I": {
        "bezout_f8": [
            728891986,
            1711384843,
            1704323271,
            1339492114,
            986262926,
            227124627,
            1820761540,
        ],
        "bezout_mismatch": [
            1963273613,
            197424372,
            2109338360,
            1768858959,
            338011691,
            1809782485,
            644748967,
            880556468,
        ],
        "mismatch": [
            467867406,
            1278816008,
            1198218452,
            795930408,
            413622875,
            1507080347,
            1359907050,
            829611936,
        ],
    },
    "J": {
        "bezout_f8": [
            1050548741,
            177769301,
            1055326069,
            1301926167,
            1415812154,
            1258221600,
            1606439928,
        ],
        "bezout_mismatch": [
            162121279,
            343401622,
            1095838264,
            1916788299,
            901744177,
            1465118481,
            885094218,
            29628355,
        ],
        "mismatch": [
            482954018,
            1996723265,
            47079281,
            913730111,
            915891061,
            1812515029,
            763829210,
            9883900,
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
    predecessor_json = git_json(
        PREDECESSOR["commit"], PREDECESSOR["certificate_path"]
    )
    require(
        predecessor_json["payload_sha256"] == CROSSED_PAYLOAD,
        "crossed predecessor payload binding",
    )
    require(
        predecessor_json["scope"]["assignment"]
        == PREDECESSOR["assignment"],
        "crossed predecessor assignment binding",
    )
    require(
        predecessor_json["scope"]["assignment_quantifier"]
        == PREDECESSOR["assignment_quantifier"],
        "crossed predecessor representative quantifier binding",
    )
    require(
        predecessor_json["assignment_scope"]["status"]
        == "REPRESENTATIVE_ONLY",
        "crossed predecessor representative-only scope",
    )
    require(
        predecessor_json["assignment_scope"]["other_assignments_status"]
        == PREDECESSOR["other_assignments_status"],
        "crossed predecessor open-seven binding",
    )
    require(
        predecessor_json["assignment_scope"]["complete_system_covariance"]
        == "NOT_CLAIMED",
        "crossed predecessor covariance scope",
    )


def verify_identity_terminal(terminal: dict[str, Any], prime: int) -> None:
    require(
        terminal["c1_d0"]
        == {
            "collision": "b=1/2",
            "retained_factor": "c+d",
            "retained_factor_exponent": 2,
        },
        "c1/d0 half collision",
    )
    final = terminal["c1_d1"]
    require(final["component_partition"] == EXPECTED_COMPONENTS, "components")
    require(final["resultant_degree"] == 52, "resultant degree")
    require(final["resultant_scalar"] == 3486784401, "resultant scalar")
    require(
        final["resultant_factors_low_to_high"] == EXPECTED_FACTORS,
        "resultant factors",
    )
    require(final["full_quotient"] == EXPECTED_QUOTIENT, "quotient witnesses")

    degree = 0
    for component in EXPECTED_COMPONENTS:
        factor_name = {
            "c-2": "c_minus_2",
            "2c-1": "two_c_minus_1",
            "c-1": "c_minus_1",
            "c+1": "c_plus_1",
            "f6": "f6",
            "f8": "f8",
            "f10": "f10",
        }[component["factor"]]
        degree += (
            len(EXPECTED_FACTORS[factor_name]) - 1
        ) * component["multiplicity"]
    require(degree == final["resultant_degree"], "resultant degree sum")
    for name in ("f6", "f8", "f10"):
        require(
            EXPECTED_FACTORS[name] == list(reversed(EXPECTED_FACTORS[name])),
            f"{name} reciprocal symmetry",
        )

    modulus = EXPECTED_FACTORS["f8"]
    for side in ("I", "J"):
        record = final["full_quotient"][side]
        combination = poly_add(
            poly_multiply(record["bezout_f8"], modulus, prime),
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
            "identity_terminal",
            "nonclaims",
            "normalization",
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
        == "kb-mca-v4-m2-diagonal-112-fixed-positive-identity-v1",
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
            "root_distribution": [2, 0],
            "source_branch": "saturated source-line",
            "target": (
                "normalized fixed-moving aligned-positive "
                "identity-doubled representative"
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
                "K3_M2_DIAGONAL_112_FIXED_POSITIVE_"
                "IDENTITY_2_0_REPRESENTATIVE"
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
            "root_distribution": [2, 0],
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
            "positive_0_2_status": (
                "REPRESENTATIVE_CLOSED_BY_PREDECESSOR_ONLY_"
                "OTHER_SEVEN_OPEN"
            ),
            "positive_1_1_status": "OPEN_ALL_EIGHT_ASSIGNMENTS",
            "representative_fixed_moving_identity_2_0_empty": True,
        },
        "conclusion",
    )
    require(
        data["branch_partition"]
        == {
            "c_choice_count": 2,
            "c_choice_one": {
                "d_choice_one": "IDENTITY_TERMINAL",
                "d_choice_zero": "HALF_COLLISION",
            },
            "c_choice_zero": {
                "d_choices_deleted": 2,
                "required_nonzero_factorization": [
                    ["c", 1],
                    ["w-c", 2],
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
                    "localizer": "Hbasic; additionally c-w on c_choice=0",
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
    verify_identity_terminal(data["identity_terminal"], PRIME)
    require(
        data["nonclaims"]
        == [
            (
                "no identity (2,0) claim for the other seven "
                "fixed-moving assignments"
            ),
            (
                "no crossed (0,2) claim for the other seven "
                "fixed-moving assignments"
            ),
            "no projective covariance claim for the complete source system",
            (
                "no balanced positive (1,1) deletion for any "
                "fixed-moving assignment"
            ),
            "no moving-moving deletion",
            "no near-aligned positive deletion",
            "no exceptional unsaturated-orbit or biquadratic-source-cover deletion",
            "no complete (1,1,2) row deletion",
            "no owner, payment, K3 value, KoalaBear row bound, or Prize closure",
        ],
        "nonclaims",
    )
    verify_provenance(data["provenance"])
    require(
        data["artifacts"]
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
        lambda x: x["scope"]["root_distribution"].reverse(),
        lambda x: x["scope"].__setitem__("profile", "(2,0,1)"),
        lambda x: x["scope"].__setitem__("target", "balanced"),
        lambda x: x["scope"].__setitem__(
            "assignment", "{{2,1/2},{2,1/b}}"
        ),
        lambda x: x["scope"].__setitem__(
            "assignment_quantifier", "FULL_FIXED_MOVING_ORBIT"
        ),
        lambda x: x["assignment_scope"].__setitem__("status", "FULL_ORBIT"),
        lambda x: x["assignment_scope"].__setitem__(
            "complete_system_covariance", "PROVED"
        ),
        lambda x: x["assignment_scope"].__setitem__(
            "closed_assignment_count", 8
        ),
        lambda x: x["assignment_scope"].__setitem__(
            "open_assignment_count", 0
        ),
        lambda x: x["assignment_scope"].__setitem__(
            "other_assignments_status", "CLOSED"
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
            "representative_fixed_moving_identity_2_0_empty", False
        ),
        lambda x: x["conclusion"].__setitem__("complete_112_row_deleted", True),
        lambda x: x["conclusion"].__setitem__(
            "complete_system_covariance", "PROVED"
        ),
        lambda x: x["conclusion"].__setitem__(
            "other_fixed_moving_assignments_status", "CLOSED"
        ),
        lambda x: x["conclusion"].__setitem__(
            "other_fixed_moving_assignment_count", 0
        ),
        lambda x: x["conclusion"].__setitem__(
            "positive_0_2_status", "CLOSED_ALL_ASSIGNMENTS"
        ),
        lambda x: x["conclusion"].__setitem__("positive_1_1_status", "CLOSED"),
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
            "d_choice_zero", "IDENTITY_TERMINAL"
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
        lambda x: x["identity_terminal"]["c1_d0"].__setitem__(
            "collision", "w=c"
        ),
        lambda x: x["identity_terminal"]["c1_d0"].__setitem__(
            "retained_factor", "c-d"
        ),
        lambda x: x["identity_terminal"]["c1_d0"].__setitem__(
            "retained_factor_exponent", 1
        ),
        lambda x: x["identity_terminal"]["c1_d1"].__setitem__(
            "resultant_degree", 51
        ),
        lambda x: x["identity_terminal"]["c1_d1"].__setitem__(
            "resultant_scalar", 1
        ),
        lambda x: x["identity_terminal"]["c1_d1"][
            "component_partition"
        ][4].__setitem__("terminal", "owner"),
        lambda x: x["identity_terminal"]["c1_d1"][
            "component_partition"
        ][5].__setitem__("multiplicity", 2),
        lambda x: x["identity_terminal"]["c1_d1"][
            "resultant_factors_low_to_high"
        ]["f6"].__setitem__(1, -81),
        lambda x: x["identity_terminal"]["c1_d1"][
            "resultant_factors_low_to_high"
        ]["f8"].pop(),
        lambda x: x["identity_terminal"]["c1_d1"][
            "resultant_factors_low_to_high"
        ]["f10"].__setitem__(5, -12123),
        lambda x: x["identity_terminal"]["c1_d1"][
            "full_quotient"
        ].__setitem__("coefficient_index", 2),
        lambda x: x["identity_terminal"]["c1_d1"]["full_quotient"][
            "identities_tested"
        ].reverse(),
        lambda x: x["identity_terminal"]["c1_d1"]["full_quotient"]["J"][
            "mismatch"
        ].__setitem__(0, 0),
        lambda x: x["identity_terminal"]["c1_d1"]["full_quotient"]["I"][
            "bezout_f8"
        ].__setitem__(0, 0),
        lambda x: x["identity_terminal"]["c1_d1"]["full_quotient"]["J"][
            "bezout_mismatch"
        ].__setitem__(0, 0),
        lambda x: x["provenance"]["predecessor"].__setitem__(
            "commit", "0" * 40
        ),
        lambda x: x["provenance"]["predecessor"].__setitem__(
            "payload_sha256", "0" * 64
        ),
        lambda x: x["provenance"]["predecessor"].__setitem__(
            "certificate_blob_oid", "0" * 40
        ),
        lambda x: x["provenance"]["predecessor"].__setitem__(
            "assignment_quantifier", "FULL_FIXED_MOVING_ORBIT"
        ),
        lambda x: x["provenance"]["predecessor"].__setitem__(
            "other_assignments_status", "CLOSED"
        ),
        lambda x: x["provenance"]["predecessor"].__setitem__(
            "assignment", "{{2,1/2},{2,1/b}}"
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
        "PASS representative fixed-positive identity (2,0) "
        f"payload={data['payload_sha256']} "
        "terminal=EMPTY other_assignments=OPEN_7 covariance=NOT_CLAIMED"
    )
    if args.tamper_selftest:
        rejected = tamper_selftest(data)
        print(f"PASS tamper self-test: {rejected}/{rejected} rejected")


if __name__ == "__main__":
    main()
