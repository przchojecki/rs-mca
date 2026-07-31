#!/usr/bin/env python3
"""Verify the canonical moving-moving aligned-positive balanced (1,1) packet."""

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
    "kb-mca-v4-m2-diagonal-112-moving-positive-balanced-v1/"
    "kb_mca_v4_m2_diagonal_112_moving_positive_balanced_v1.json"
)
SAGE_REPLAY = (
    ROOT
    / "experimental/scripts/"
    "verify_kb_mca_v4_m2_diagonal_112_moving_positive_balanced_v1.sage"
)
SINGULAR_REPLAY = (
    ROOT
    / "experimental/scripts/"
    "verify_kb_mca_v4_m2_diagonal_112_moving_positive_balanced_v1.sing"
)
WOLFRAM_REPLAY = (
    ROOT
    / "experimental/scripts/"
    "verify_kb_mca_v4_m2_diagonal_112_moving_positive_balanced_v1.wl"
)

PRIME = 2130706433
EXPECTED_PAYLOAD = (
    "3f32af654c6527e97c036d09a07c1d5554923c484300d5c3141fd997cc3a7a05"
)
SAGE_OUTPUT_PAYLOAD = (
    "329c9b206d6f03671fd8233afe7c49a005f7e4af0f668b2d2eb97f29efb9cc76"
)
SOURCE_FACET_PAYLOAD = (
    "8f768cfded349dc3dd40cf6214ffe980c69ff18ae2d8c209e63b4307767429d2"
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
    "payload_sha256": SOURCE_FACET_PAYLOAD,
    "verifier_blob_oid": "e810f286d5b67d19660c3c382501a690e3e76fb0",
    "verifier_path": (
        "experimental/scripts/"
        "verify_kb_mca_v4_m2_u2_universal_source_facet_census_v1.py"
    ),
}

CANONICAL_PAIR = [["2", "b"], ["2", "1/b"]]
YINF_AUDIT_PAYLOAD = (
    "16cd5144eb45c930e48d02388c658c7aee19d4e60956421e83bb0a485a7e28e8"
)
W0_AUDIT_PAYLOAD = (
    "e507788efd3bd9be3bd04b14a40e70cbf34acec0eadc24044a3294d057027980"
)

EXPECTED_METRICS = {
    "factor_metrics": {
        "F11": (
            11,
            (2, 6, 6, 3),
            311,
            "d13f4d8b197a74b5c5a0d12a17a63cb14bd2954367dfed05a8d4b4e7b326c2cc",
        ),
        "F5": (
            5,
            (1, 2, 3, 1),
            32,
            "f8313e4ce2a50bd863cbf7c938f84b12608733766d6a2a484fd572e169318d88",
        ),
        "G15": (
            15,
            (9, 11, 4),
            339,
            "fc60106eafded78b78b6549ba16eb23d152f2ef9759abd6b297e993f1dea79b3",
        ),
        "G7": (
            7,
            (4, 5, 2),
            43,
            "27345df84a941f9892be25b62fd5104a41392d14b40c003be36fab41b9f020e8",
        ),
        "G9": (
            9,
            (5, 6, 3),
            94,
            "73fb7784c21706e1824cbbc52ac374f7c8341b302447e6705c216676ab0cac8e",
        ),
        "L2": (
            2,
            (1, 1, 1, 0),
            3,
            "771d6d8f80f86a15adc308b063e2aae551943d22e190ea6cb180623fa041f81b",
        ),
        "P25": (
            25,
            (6, 14, 14, 6),
            5048,
            "1a1685279f4e80a86eaf399153051a4c7f7ccc691a2d63c33791d5980174a8d3",
        ),
        "P46": (
            46,
            (5, 25, 25, 17),
            35534,
            "725c9adcb6d74e93868675be71a65b0321f79bdaf895ba3e571acdad4dac4696",
        ),
        "alpha": (
            4,
            (0, 2, 3, 1),
            16,
            "ebbefe610613c9b532eeb85ab5da9e49a7055fabde4bbed4535ed2618fbdfcbe",
        ),
        "beta": (
            4,
            (0, 2, 3, 1),
            16,
            "844b85e8a90b7a7566caf06be91a99c4f7a83862de0b47c661a11d6be070fc11",
        ),
    },
    "qslice_metrics": {
        "A0": (
            10,
            (2, 6, 6, 2),
            211,
            "80c87dadfe17314095dcac33916b12551010101861ea35231e7c3d19a48183fb",
        ),
        "A1": (
            15,
            (2, 9, 9, 4),
            780,
            "594b1e0cc8128e0189f9419ffe311d1d279a739e4238702faa92c5114f80a490",
        ),
        "B0": (
            9,
            (2, 4, 5, 2),
            134,
            "e0d4d5529c2b8e3f00ea62d2aa99e57e14309ff162f8a5876b05d60fd663b8a8",
        ),
        "B1": (
            14,
            (2, 7, 8, 4),
            581,
            "1762587b9591de809265a7d517b3aa4ad7fc4a5663393a23d0277379e45a84ad",
        ),
    },
    "remainder_metrics": {
        "P25_generic": (
            13,
            (11, 12, 9),
            368,
            "d320c59d012bb6c3d8287c7f83ec9dd3e0977faeff61528c401b316e0333a0ce",
        ),
        "P46_generic_unused": (
            13,
            (11, 12, 9),
            368,
            "a0f77109edc5d92ab670dabddfe35a6116012e65e8845fed72aadf3a43a29406",
        ),
        "P46_l2": (
            7,
            (0, 6, 1),
            12,
            "ae2e03fcbb73ab177ddf992966aab46dc1e575cb14377830b0c287831295294f",
        ),
        "l2_p_eliminant": (
            10,
            (0, 10, 0),
            9,
            "b25564c21bd8301474e7928fd11bd992475890b99233ab6718e885ecf03f7366",
        ),
    },
}

EXPECTED_RAW_HASHES = [
    "8f73e1d4bdda3fc3262e042d35cb714d541f827978638a6ecaf630b5731b93f7",
    "984a41f0ac99fda8a192fd20d0ee7f8f14be2a43b52105ec44cc80eb58c16a8f",
    "42e8416d1c217567e1a67a1a38ddc9069043d72238e997cacc4dc0a3bbcd9be0",
    "dd1b7d639bbbfe61c56db298f970cf4a3f5020c71bc6c15fda146ced5c18ea5e",
]

EXPECTED_W0_CHART = {
    "basis_sha256": (
        "cc74d01fc4c41b8ace5c23f78a26ce4991450e7c0430eaa42dea0f8bf0042dd2"
    ),
    "basis_size": 24,
    "dimension": 1,
    "generators": {
        "A0": {
            "degree": 8,
            "degrees": [2, 6, 6],
            "sha256": (
                "8defe2bf2497853b3fe0892acadba8cf4c78c5857ce62e649f0ebe6d65462dac"
            ),
            "terms": 74,
        },
        "A1": {
            "degree": 11,
            "degrees": [2, 9, 9],
            "sha256": (
                "75aaa5b5a764b87e7c290515016089f912874c95f5b9a2f0a678be55abf394df"
            ),
            "terms": 154,
        },
        "B0": {
            "degree": 7,
            "degrees": [2, 4, 5],
            "sha256": (
                "1efc4d5300563528c06cb80eb13a65e51d8373ad554bddcf6c073cba97e7448d"
            ),
            "terms": 48,
        },
        "B1": {
            "degree": 10,
            "degrees": [2, 7, 8],
            "sha256": (
                "11cf57939097174326d3a31e5c4a19ea68328988ee01bf0b9fae4f13480bdd4e"
            ),
            "terms": 119,
        },
    },
    "load_bearing": True,
    "localizer_factors": [
        "p",
        "s^2-4p",
        "p-1",
        "1-s+p",
        "1+s+p",
        "4-2s+p",
        "1-2s+4p",
        "5p-4s+5",
        "2s-4p-1",
    ],
    "localizer_nilpotence": 3,
    "localizer_remainders": [
        {
            "exponent": 1,
            "record": {
                "degree": 10,
                "degrees": [4, 8, 10],
                "sha256": (
                    "0ab4b29eb2fbcc56b9fb6a88ff17dbd147545d5e90e601373db988776df405b1"
                ),
                "terms": 151,
            },
            "zero": False,
        },
        {
            "exponent": 2,
            "record": {
                "degree": 20,
                "degrees": [4, 8, 20],
                "sha256": (
                    "c2609c094eb529764bbbd9c110a4334d5129c92c6b331dcb9bff972b642cb418"
                ),
                "terms": 221,
            },
            "zero": False,
        },
        {
            "exponent": 3,
            "record": {
                "degree": -1,
                "degrees": [-1, -1, -1],
                "sha256": (
                    "5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9"
                ),
                "terms": 0,
            },
            "zero": True,
        },
    ],
    "rabinowitsch_basis_size": 1,
    "rabinowitsch_unit_ideal": True,
    "scope": "canonical_assignment_affine_y_w_equals_zero",
    "terminal": "EMPTY_BY_QSLICE_BEFORE_PARITY",
}

EXPECTED_YINF_CHART = {
    "basis_sha256": (
        "988d28d187d8668c9a14bfef2368e195ec443fe8d98cc449752ce9399be07289"
    ),
    "basis_size": 23,
    "dimension": 1,
    "generators": {
        "A0_y2": {
            "degree": 8,
            "degrees": [4, 6, 2],
            "sha256": (
                "eaa8ecedd16472ef17d2650fa933ec4932ddc2c8c70b1eaf63fbfc889a487d2d"
            ),
            "terms": 72,
        },
        "A1_y2": {
            "degree": 13,
            "degrees": [7, 9, 4],
            "sha256": (
                "f36fffc6bc4151ecf3603a04932130eae311d3499c835f6e50f8956ad1d76877"
            ),
            "terms": 252,
        },
        "B0_y2": {
            "degree": 7,
            "degrees": [3, 5, 2],
            "sha256": (
                "57a370968b5e5da315ee12dbfb7179913eb7a9e61da62af67235de12fb0cd502"
            ),
            "terms": 44,
        },
        "B1_y2": {
            "degree": 12,
            "degrees": [6, 8, 4],
            "sha256": (
                "eb9ff31d007f782587f59aa6c7dd21074b608cbc91fed83926e997c38a90a7a0"
            ),
            "terms": 182,
        },
    },
    "load_bearing": False,
    "localizer_factors": [
        "p",
        "s^2-4p",
        "p-1",
        "1-s+p",
        "1+s+p",
        "4-2s+p",
        "1-2s+4p",
        "w^2-1",
        "w^2-sw+p",
        "1-sw+pw^2",
        "5p-4s+5",
        "-2sw+pw+2s-4p+4w-1",
    ],
    "localizer_nilpotence": 2,
    "localizer_remainders": [
        {
            "exponent": 1,
            "record": {
                "degree": 12,
                "degrees": [7, 11, 7],
                "sha256": (
                    "62d9e0da9c13fb9c83cb9080463b1228a5da51c8045286be8fca7bf18fb51c0b"
                ),
                "terms": 214,
            },
            "zero": False,
        },
        {
            "exponent": 2,
            "record": {
                "degree": -1,
                "degrees": [-1, -1, -1],
                "sha256": (
                    "5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9"
                ),
                "terms": 0,
            },
            "zero": True,
        },
    ],
    "rabinowitsch_basis_size": 1,
    "rabinowitsch_unit_ideal": True,
    "role": "NON_LOAD_BEARING_PROJECTIVE_COMPACTIFICATION_CONTROL",
    "terminal": "CONTROL_EMPTY_BY_QSLICE",
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


def verify_provenance(provenance: dict[str, Any]) -> None:
    require(
        provenance
        == {"source_facet_parent": SOURCE_FACET_PARENT},
        "exact provenance",
    )
    for parent_name, parent in provenance.items():
        for kind in ("certificate", "note", "verifier"):
            require(
                git_blob(parent["commit"], parent[f"{kind}_path"])
                == parent[f"{kind}_blob_oid"],
                f"{parent_name} {kind} blob binding",
            )
        parent_json = git_json(parent["commit"], parent["certificate_path"])
        require(
            parent_json["payload_sha256"] == parent["payload_sha256"],
            f"{parent_name} payload binding",
        )


def verify_normalization(record: dict[str, Any]) -> None:
    require(
        record
        == {
            "J0": ["2", "1/2", "b", "1/b"],
            "J1": ["c", "d"],
            "assignment_scope": {
                "canonical_only": True,
                "canonical_unordered_source_star_pair": CANONICAL_PAIR,
                "covariance_used": False,
                "other_three_moving_moving_assignments": (
                    "OPEN_SEPARATE_EXACT_SYSTEMS"
                ),
            },
            "covariance_audit": {
                "diagonal_W_action": (
                    "PRESERVES_ALIGNED_TARGET_NOT_OBSERVED_RESIDUALS"
                ),
                "endpoint_only_action": (
                    "PRESERVES_OBSERVED_RESIDUALS_NOT_ALIGNED_TARGET"
                ),
                "transport_claim": False,
            },
            "deck": "tau(x)=1/x",
            "finite_parameter": {
                "b_finite": True,
                "b_nonzero": True,
                "y": "b+1/b",
                "y_affine_finite": True,
            },
            "moving_moving_edges": CANONICAL_PAIR,
            "root_distribution": [1, 1],
            "target_quadratic": "(W-1/c)(W-1/d)",
        },
        "canonical-only normalization",
    )


def verify_metrics(polynomial_metrics: dict[str, Any]) -> None:
    require(
        set(polynomial_metrics)
        == {
            "factor_metrics",
            "qslice_metrics",
            "raw_projective_hashes",
            "remainder_metrics",
        },
        "polynomial metric sections",
    )
    for section, expected_records in EXPECTED_METRICS.items():
        actual_records = polynomial_metrics[section]
        require(set(actual_records) == set(expected_records), f"{section} keys")
        for name, expected in expected_records.items():
            actual = actual_records[name]
            require(
                (
                    actual["degree"],
                    tuple(actual["degrees"]),
                    actual["terms"],
                    actual["sha256"],
                )
                == expected,
                f"{section} {name}",
            )
    require(
        polynomial_metrics["raw_projective_hashes"] == EXPECTED_RAW_HASHES,
        "raw projective hashes",
    )


def verify_partition(partition: dict[str, Any]) -> None:
    require(
        set(partition)
        == {
            "charts",
            "equations",
            "existing_six_chart_scope",
            "first_match_order",
            "selector_definitions",
        },
        "partition fields",
    )
    require(
        partition["existing_six_chart_scope"]
        == "canonical_assignment_finite_y_w_nonzero",
        "existing six-chart scope",
    )
    require(
        partition["first_match_order"]
        == [
            "finite_y,w=0",
            "finite_y,w!=0,L2=0",
            "finite_y,w!=0,L2!=0,F5=0,alpha=0",
            "finite_y,w!=0,L2!=0,F5=0,alpha!=0,D=0,R=0",
            "finite_y,w!=0,L2!=0,F5=0,alpha!=0,D=0,R!=0,G9=0",
            "finite_y,w!=0,L2!=0,F5=0,alpha!=0,D!=0,R=0",
            "finite_y,w!=0,L2!=0,F5=0,alpha!=0,D!=0,R!=0,G9=0",
        ],
        "exhaustive first-match order",
    )
    require(
        partition["selector_definitions"]
        == {
            "D": "-2sw+4pw+2s-p+w-4",
            "E": "-2sw+pw+2s-4p+4w-1",
            "L2": "y(p+1)-2s",
            "R": "-5s+4p+4",
        },
        "selector definitions",
    )
    require(
        partition["equations"]
        == {
            "f5_substitution": "y=-beta/alpha",
            "factorization": [
                "B0=-A(w-1)L2 F5",
                "B1=-A(w-1)(p-1)F11",
                "F5=alpha*y+beta",
                "A0|F5 ~ G7",
                "A1|F5 ~ G15",
                "F11|F5 ~ R*G9",
            ],
            "parity": [
                "Parity_J ~ w^2 D L2 E^6 P25",
                "Parity_I ~ E^3 P46",
            ],
            "qslice": ["A0=0", "B0=0", "A1=0", "B1=0"],
        },
        "exact equation record",
    )
    require(
        partition["charts"]
        == {
            "finite_y_w_zero": EXPECTED_W0_CHART,
            "f5_alpha_zero": {
                "basis_size": 24,
                "dimension": 2,
                "localizer_nilpotence": 1,
                "terminal": "PARENT_BOUNDARY_OR_EARLIER_L2",
            },
            "f5_d0_g9": {
                "basis_size": 9,
                "dimension": 1,
                "localizer_nilpotence": 1,
                "terminal": "PARENT_BOUNDARY_OR_EARLIER_FIRST_MATCH",
            },
            "f5_d0_r0": {
                "basis_size": 4,
                "dimension": 0,
                "localizer_nilpotence": 1,
                "terminal": "PARENT_BOUNDARY_OR_EARLIER_FIRST_MATCH",
            },
            "f5_generic_p25": {
                "basis_size_after_p25": 35,
                "dimension": 1,
                "localizer": "H=H_parent*alpha*L2*D*R",
                "localizer_nonzero_before_square": True,
                "localizer_square_zero": True,
                "p46_used": False,
                "parity_equation": "P25",
                "qslice_basis_size": 38,
                "terminal": "EMPTY_AFTER_LOCALIZATION",
            },
            "f5_r0_dnz": {
                "basis_size": 2,
                "dimension": 1,
                "localizer_nilpotence": 1,
                "terminal": "PARENT_BOUNDARY_OR_EARLIER_FIRST_MATCH",
            },
            "l2": {
                "basis_size_after_p46": 3,
                "coefficient_zero_terminal": (
                    "PARENT_COLLISION_q_equals_T2_minus_1"
                ),
                "dimension": 0,
                "eliminant_factorization": (
                    "p^2(p+1)^4(p-1)^2(p-4)(p-1/4)"
                ),
                "localizer_nilpotence": 1,
                "parity_equation": "P46",
                "terminal": "EMPTY_AFTER_LOCALIZATION",
            },
            "projective_y_infinity_control": EXPECTED_YINF_CHART,
        },
        "complete chart records",
    )


def verify_normalization_audit(audit: dict[str, Any]) -> None:
    require(
        audit
        == {
            "coefficientwise_normalization_used": False,
            "dropped_qslice_parent_factors": [
                "(p-1)E^2",
                "1",
                "(p-1)E^2",
                "1",
            ],
            "eliminant_normalization": (
                "one_nonzero_deployed_field_scalar"
            ),
            "parity_clear_scalars": [
                "2/16423203268260658146231467800709255289",
                "1/17455927136175424851782794958953454680082898",
            ],
            "parity_denominator_patterns": [
                "core2^3 corehalf^3 (p-1)^3 (w-1)^4 A^5 (w+1)^5",
                (
                    "w^2 p^2 (p-1)^3 A^5 core2^5 corehalf^5 "
                    "(w-1)^5 (w+1)^5 D^2"
                ),
            ],
            "parity_line_scaling": (
                "one_common_nonzero_QQ_scalar_per_cleared_line"
            ),
            "projective_y_chart": {
                "affine_coordinate": "y=Y/Z",
                "homogeneous_coordinates": "[Y:Z]",
                "infinity_value": "coefficient_of_y^2",
                "load_bearing": False,
                "role": "non_load_bearing_compactification_control",
            },
            "projective_target_pivot": "monic_W^2_coefficient_1",
            "raw_clear_scalars": [
                "1/79766443076872509863361",
                "-1/282429536481",
                "1/79766443076872509863361",
                "-1/282429536481",
            ],
            "raw_denominator_patterns": [
                (
                    "cd(w-1)^2(w+1)^2(d-2)^2(2d-1)^2"
                    "(b-1)^2(b+1)^2A^2"
                ),
                (
                    "cd(w-1)^2(w+1)^2(c-2)^2(2c-1)^2"
                    "(b-1)^2(b+1)^2A^2"
                ),
            ],
            "raw_line_scaling": (
                "one_common_nonzero_QQ_scalar_per_cleared_line"
            ),
            "residual_divisor": "monic_(W-w)^2",
            "root_reduction_divisor": "monic_X^2-sX+p",
            "source_determinant_denominator": "E^6",
            "source_determinant_numerator_factors": [
                "(d-2)^2",
                "(2d-1)^2",
                "(c-2)^2",
                "(2c-1)^2",
                "(w-1)^5",
                "(w+1)^5",
                "A",
                "(p-1)^2",
            ],
            "substitution_clearances": {
                "F5": "alpha^degree_y",
                "L2": "(p+1)^degree_y",
            },
        },
        "normalization and sign audit",
    )


def verify_data(data: dict[str, Any]) -> None:
    require(
        set(data)
        == {
            "artifacts",
            "branch_partition",
            "conclusion",
            "field",
            "nonclaims",
            "normalization",
            "normalization_audit",
            "parity_usage",
            "payload_sha256",
            "polynomial_metrics",
            "proof_status",
            "provenance",
            "repair_audit_inputs",
            "review_status",
            "schema",
            "scope",
            "source_incidence",
            "workboard",
        },
        "top-level fields",
    )
    require(
        data["schema"]
        == "kb-mca-v4-m2-diagonal-112-moving-positive-balanced-v1",
        "schema",
    )
    require(data["payload_sha256"] == EXPECTED_PAYLOAD, "expected payload")
    require(data["payload_sha256"] == payload_hash(data), "payload hash")
    require(
        data["scope"]
        == {
            "assignment_count": 1,
            "ledger_movement": 0,
            "profile": "(a,b,c)=(1,1,2)",
            "root_distribution": [1, 1],
            "source_branch": "saturated source-line",
            "target": (
                "canonical moving-moving aligned-positive balanced pattern"
            ),
        },
        "scope",
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
    verify_normalization(data["normalization"])
    verify_normalization_audit(data["normalization_audit"])
    verify_partition(data["branch_partition"])
    verify_metrics(data["polynomial_metrics"])
    verify_provenance(data["provenance"])
    require(
        data["parity_usage"]
        == {
            "f5_boundaries": "q-slice only",
            "f5_generic": "P25",
            "l2": "P46",
            "low_squared_quotient_used": False,
            "scope": "canonical_assignment_finite_y_w_nonzero",
            "w_nonzero_source": (
                "complement_of_first_match_finite_y_w_zero_chart"
            ),
        },
        "parity usage",
    )
    require(
        data["workboard"]
        == {
            "B_star": 274980728111395087,
            "agreement": 1116048,
            "architecture": None,
            "atom_or_cell": (
                "K3_M2_DIAGONAL_112_MOVING_POSITIVE_BALANCED_1_1"
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
        data["conclusion"]
        == {
            "canonical_source_star_pair_aligned_positive_balanced_1_1_empty": (
                True
            ),
            "complete_112_row_deleted": False,
            "k3_status": "OPEN",
            "koalabear_row_status": "OPEN",
            "ledger_movement": 0,
            "moving_moving_doubled_root_distributions_status": "OPEN",
            "near_aligned_and_exceptional_status": "OPEN",
            "other_three_moving_moving_assignments_status": (
                "OPEN_SEPARATE_EXACT_SYSTEMS"
            ),
        },
        "conclusion",
    )
    require(
        data["nonclaims"]
        == [
            (
                "no covariance or orbit transport from the canonical "
                "source-star pair"
            ),
            "no deletion of the other three moving-moving assignment systems",
            "no moving-moving doubled-root deletion",
            "no near-aligned positive or exceptional-branch deletion",
            "no complete (1,1,2) row deletion",
            "no owner, payment, K3 value, KoalaBear row bound, or Prize closure",
            "no theorem over arbitrary characteristics",
            "no use of the lower squared-quotient coefficients",
        ],
        "nonclaims",
    )
    require(
        data["repair_audit_inputs"]
        == {
            "finite_y_w_zero_payload_sha256": W0_AUDIT_PAYLOAD,
            "projective_y_infinity_payload_sha256": YINF_AUDIT_PAYLOAD,
            "status": "independently_rederived_in_packet",
        },
        "repair audit inputs",
    )
    require(
        data["source_incidence"]
        == {
            "identity": "z=-D/E",
            "parent_nonzero": ["E", "A", "D"],
            "rationale": {
                "A": "source_reconstruction_determinant",
                "D": "z_nonzero_and_E_nonzero",
                "E": "source_incidence_denominator",
            },
        },
        "source incidence and imported units",
    )
    require(
        data["proof_status"]
        == (
            "PROVED_CANONICAL_MOVING_MOVING_ALIGNED_POSITIVE_"
            "BALANCED_1_1_EMPTY"
        ),
        "proof status",
    )
    require(
        data["review_status"]
        == {
            "fresh_independent_review": True,
            "result": "NO_ISSUE",
            "verdict": "GREEN",
        },
        "fresh independent review status",
    )
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
        lambda x: x.__setitem__("extra", True),
        lambda x: x.__setitem__("proof_status", "CANDIDATE"),
        lambda x: x["review_status"].__setitem__("verdict", "YELLOW"),
        lambda x: x["scope"].__setitem__("assignment_count", 4),
        lambda x: x["scope"].__setitem__("ledger_movement", 1),
        lambda x: x["scope"]["root_distribution"].__setitem__(0, 2),
        lambda x: x["scope"].__setitem__("source_branch", "exceptional"),
        lambda x: x["scope"].__setitem__("target", "fixed-moving"),
        lambda x: x["workboard"].__setitem__("agreement", 1116047),
        lambda x: x["workboard"].__setitem__("atom_or_cell", "wrong"),
        lambda x: x["workboard"].__setitem__("impact", "PAYMENT"),
        lambda x: x["field"].__setitem__("prime", 43),
        lambda x: x["field"].__setitem__("challenge_extension_degree", 1),
        lambda x: x["field"]["prime_avoids"].pop(),
        lambda x: x["normalization"]["J0"].reverse(),
        lambda x: x["normalization"]["J1"].reverse(),
        lambda x: x["normalization"].__setitem__("deck", "tau(x)=x"),
        lambda x: x["normalization"]["moving_moving_edges"][1].reverse(),
        lambda x: x["normalization"]["root_distribution"].__setitem__(1, 2),
        lambda x: x["normalization"].__setitem__(
            "target_quadratic", "(W-1/c)^2"
        ),
        lambda x: x["normalization"]["assignment_scope"].__setitem__(
            "canonical_only", False
        ),
        lambda x: x["normalization"]["assignment_scope"].__setitem__(
            "covariance_used", True
        ),
        lambda x: x["normalization"]["assignment_scope"].__setitem__(
            "other_three_moving_moving_assignments", "CLOSED_BY_ORBIT"
        ),
        lambda x: x["normalization"]["assignment_scope"][
            "canonical_unordered_source_star_pair"
        ].append([["1/2", "b"], ["1/2", "1/b"]]),
        lambda x: x["normalization"]["covariance_audit"].__setitem__(
            "transport_claim", True
        ),
        lambda x: x["normalization"]["finite_parameter"].__setitem__(
            "b_nonzero", False
        ),
        lambda x: x["normalization"]["finite_parameter"].__setitem__(
            "y_affine_finite", False
        ),
        lambda x: x["normalization_audit"].__setitem__(
            "coefficientwise_normalization_used", True
        ),
        lambda x: x["normalization_audit"].__setitem__(
            "raw_line_scaling", "coefficientwise"
        ),
        lambda x: x["normalization_audit"]["raw_clear_scalars"].__setitem__(
            1, "1/282429536481"
        ),
        lambda x: x["normalization_audit"][
            "raw_denominator_patterns"
        ].pop(),
        lambda x: x["normalization_audit"].__setitem__(
            "source_determinant_denominator", "E^5"
        ),
        lambda x: x["normalization_audit"][
            "source_determinant_numerator_factors"
        ].pop(),
        lambda x: x["normalization_audit"][
            "dropped_qslice_parent_factors"
        ].__setitem__(0, "(p-1)E"),
        lambda x: x["normalization_audit"].__setitem__(
            "residual_divisor", "(W-w)^2"
        ),
        lambda x: x["normalization_audit"].__setitem__(
            "root_reduction_divisor", "X^2-sX+p"
        ),
        lambda x: x["normalization_audit"][
            "parity_clear_scalars"
        ].reverse(),
        lambda x: x["normalization_audit"][
            "parity_denominator_patterns"
        ].pop(),
        lambda x: x["normalization_audit"]["projective_y_chart"].__setitem__(
            "load_bearing", True
        ),
        lambda x: x["branch_partition"]["first_match_order"].reverse(),
        lambda x: x["branch_partition"]["first_match_order"].pop(),
        lambda x: x["branch_partition"].__setitem__(
            "existing_six_chart_scope", "all_assignments"
        ),
        lambda x: x["branch_partition"]["selector_definitions"].__setitem__(
            "D", "wrong"
        ),
        lambda x: x["branch_partition"]["equations"]["qslice"].pop(),
        lambda x: x["branch_partition"]["equations"]["parity"].reverse(),
        lambda x: x["branch_partition"]["equations"][
            "factorization"
        ].__setitem__(0, "B0=L2 F5"),
        lambda x: x["branch_partition"]["charts"]["l2"].__setitem__(
            "basis_size_after_p46", 2
        ),
        lambda x: x["branch_partition"]["charts"]["l2"].__setitem__(
            "localizer_nilpotence", 2
        ),
        lambda x: x["branch_partition"]["charts"].pop("finite_y_w_zero"),
        lambda x: x["branch_partition"]["charts"]["finite_y_w_zero"].__setitem__(
            "basis_size", 23
        ),
        lambda x: x["branch_partition"]["charts"]["finite_y_w_zero"].__setitem__(
            "localizer_nilpotence", 2
        ),
        lambda x: x["branch_partition"]["charts"]["finite_y_w_zero"][
            "localizer_remainders"
        ].__setitem__(1, copy.deepcopy(
            x["branch_partition"]["charts"]["finite_y_w_zero"][
                "localizer_remainders"
            ][2]
        )),
        lambda x: x["branch_partition"]["charts"]["finite_y_w_zero"][
            "generators"
        ]["A0"].__setitem__("sha256", "0" * 64),
        lambda x: x["branch_partition"]["charts"][
            "finite_y_w_zero"
        ].__setitem__("rabinowitsch_unit_ideal", False),
        lambda x: x["branch_partition"]["charts"].pop(
            "projective_y_infinity_control"
        ),
        lambda x: x["branch_partition"]["charts"][
            "projective_y_infinity_control"
        ].__setitem__("load_bearing", True),
        lambda x: x["branch_partition"]["charts"][
            "projective_y_infinity_control"
        ].__setitem__("basis_sha256", "0" * 64),
        lambda x: x["branch_partition"]["charts"][
            "projective_y_infinity_control"
        ]["generators"]["A0_y2"].__setitem__("terms", 71),
        lambda x: x["branch_partition"]["charts"][
            "projective_y_infinity_control"
        ].__setitem__("localizer_nilpotence", 3),
        lambda x: x["branch_partition"]["charts"][
            "projective_y_infinity_control"
        ]["localizer_factors"].pop(),
        lambda x: x["branch_partition"]["charts"][
            "projective_y_infinity_control"
        ].__setitem__("rabinowitsch_unit_ideal", False),
        lambda x: x["branch_partition"]["charts"]["f5_alpha_zero"].__setitem__(
            "dimension", 1
        ),
        lambda x: x["branch_partition"]["charts"]["f5_d0_r0"].__setitem__(
            "basis_size", 3
        ),
        lambda x: x["branch_partition"]["charts"]["f5_d0_g9"].__setitem__(
            "terminal", "UNPAID_PRIMITIVE"
        ),
        lambda x: x["branch_partition"]["charts"]["f5_r0_dnz"].__setitem__(
            "localizer_nilpotence", 2
        ),
        lambda x: x["branch_partition"]["charts"][
            "f5_generic_p25"
        ].__setitem__("localizer_nonzero_before_square", False),
        lambda x: x["branch_partition"]["charts"][
            "f5_generic_p25"
        ].__setitem__("localizer_square_zero", False),
        lambda x: x["branch_partition"]["charts"][
            "f5_generic_p25"
        ].__setitem__("p46_used", True),
        lambda x: x["parity_usage"].__setitem__(
            "low_squared_quotient_used", True
        ),
        lambda x: x["parity_usage"].__setitem__("f5_generic", "P46"),
        lambda x: x["parity_usage"].__setitem__(
            "scope", "canonical_assignment_all_w"
        ),
        lambda x: x["parity_usage"].__setitem__(
            "w_nonzero_source", "parent_unit"
        ),
        lambda x: x["source_incidence"].__setitem__("identity", "z=D/E"),
        lambda x: x["source_incidence"]["parent_nonzero"].remove("D"),
        lambda x: x["source_incidence"]["parent_nonzero"].append("w"),
        lambda x: x["repair_audit_inputs"].__setitem__(
            "finite_y_w_zero_payload_sha256", "0" * 64
        ),
        lambda x: x["repair_audit_inputs"].__setitem__(
            "projective_y_infinity_payload_sha256", "0" * 64
        ),
        lambda x: x["polynomial_metrics"]["factor_metrics"]["P25"].__setitem__(
            "terms", 5047
        ),
        lambda x: x["polynomial_metrics"]["factor_metrics"]["P46"].__setitem__(
            "sha256", "0" * 64
        ),
        lambda x: x["polynomial_metrics"]["qslice_metrics"]["B0"].__setitem__(
            "degree", 8
        ),
        lambda x: x["polynomial_metrics"][
            "raw_projective_hashes"
        ].__setitem__(0, "0" * 64),
        lambda x: x["polynomial_metrics"]["remainder_metrics"][
            "P25_generic"
        ].__setitem__("terms", 367),
        lambda x: x["provenance"]["source_facet_parent"].__setitem__(
            "commit", "0" * 40
        ),
        lambda x: x["provenance"]["source_facet_parent"].__setitem__(
            "payload_sha256", "0" * 64
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
        lambda x: x["conclusion"].__setitem__(
            "canonical_source_star_pair_aligned_positive_balanced_1_1_empty",
            False,
        ),
        lambda x: x["conclusion"].__setitem__(
            "other_three_moving_moving_assignments_status", "CLOSED"
        ),
        lambda x: x["conclusion"].__setitem__(
            "moving_moving_doubled_root_distributions_status", "CLOSED"
        ),
        lambda x: x["conclusion"].__setitem__("complete_112_row_deleted", True),
        lambda x: x["conclusion"].__setitem__("k3_status", "CLOSED"),
        lambda x: x["conclusion"].__setitem__("ledger_movement", 1),
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

    duplicate_rejected = 0
    try:
        json.loads(
            '{"payload_sha256":"a","payload_sha256":"b"}',
            object_pairs_hook=reject_duplicate_keys,
        )
    except VerificationError:
        duplicate_rejected = 1
    require(duplicate_rejected == 1, "duplicate-key rejection")
    return rejected + duplicate_rejected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    require(args.check or args.tamper_selftest, "select a verifier mode")
    data = load_certificate()
    verify_data(data)
    print(
        "PASS canonical moving-positive balanced (1,1) "
        f"payload={data['payload_sha256']} terminal=EMPTY review=GREEN"
    )
    if args.tamper_selftest:
        rejected = tamper_selftest(data)
        print(f"PASS tamper self-test: {rejected}/{rejected} rejected")


if __name__ == "__main__":
    main()
