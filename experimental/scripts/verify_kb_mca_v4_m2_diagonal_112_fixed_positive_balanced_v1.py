#!/usr/bin/env python3
"""Verify one fixed-moving aligned-positive balanced (1,1) representative."""

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
    "kb-mca-v4-m2-diagonal-112-fixed-positive-balanced-v1/"
    "kb_mca_v4_m2_diagonal_112_fixed_positive_balanced_v1.json"
)
SAGE_REPLAY = (
    ROOT
    / "experimental/scripts/"
    "verify_kb_mca_v4_m2_diagonal_112_fixed_positive_balanced_v1.sage"
)
SINGULAR_REPLAY = (
    ROOT
    / "experimental/scripts/"
    "verify_kb_mca_v4_m2_diagonal_112_fixed_positive_balanced_v1.sing"
)
WOLFRAM_REPLAY = (
    ROOT
    / "experimental/scripts/"
    "verify_kb_mca_v4_m2_diagonal_112_fixed_positive_balanced_v1.wl"
)

PRIME = 2130706433
EXPECTED_PAYLOAD = (
    "a9e67b5cb40c0731f504636f06e2e99c9147b76e1d27dfee2b9d6855e9dca471"
)
SAGE_OUTPUT_PAYLOAD = (
    "86b859a30fcf95b613385c7d6a705bc5c5c3ac2e2bdfcadf37e93086b8567ca4"
)
IDENTITY_PAYLOAD = (
    "ce59e2be2417dd8681bce65d7f0d838850445dfccbd82d68c137387510ea7cb5"
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
    "certificate_blob_oid": "1e083a5cac1bba0827ae2c6c9e72ffd9da03d3ba",
    "certificate_path": (
        "experimental/data/certificates/"
        "kb-mca-v4-m2-diagonal-112-fixed-positive-identity-v1/"
        "kb_mca_v4_m2_diagonal_112_fixed_positive_identity_v1.json"
    ),
    "commit": "9f5b7ffa8759f0372802792bc5baf589410cdd28",
    "note_blob_oid": "8a541e989d9882316cd25de90bebb37afec116a6",
    "note_path": (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_m2_diagonal_112_fixed_positive_identity_v1.md"
    ),
    "other_assignments_status": "OPEN_SEPARATE_EXACT_SYSTEMS",
    "payload_sha256": IDENTITY_PAYLOAD,
    "verifier_blob_oid": "45c5d583039c326705769e55dc309142f3b39813",
    "verifier_path": (
        "experimental/scripts/"
        "verify_kb_mca_v4_m2_diagonal_112_fixed_positive_identity_v1.py"
    ),
}

EXPECTED_METRICS = {
    "A": {
        "degree": 9,
        "sha256": "720eec95a329975e0df2ea1533648af0dbb2254f726b11131acc090e1386d140",
        "terms": 115,
    },
    "B": {
        "degree": 8,
        "sha256": "412b6a1290d0b0cafb5795b6591c15b94a1f7aefedd641b1fd0d6abcad7c43c6",
        "terms": 84,
    },
    "L": {
        "degree": 10,
        "sha256": "1d10dcd6da3f56234773ef8067f1471d636ed43d71dca825576554e5fe05bd8e",
        "terms": 69,
    },
    "Q": {
        "degree": 7,
        "sha256": "27345df84a941f9892be25b62fd5104a41392d14b40c003be36fab41b9f020e8",
        "terms": 43,
    },
    "eC": {
        "degree": 20,
        "sha256": "163673f99d8078515ab0b0845a2e77f617a627507e78474b70b4bb844d381367",
        "terms": 943,
    },
    "eD": {
        "degree": 20,
        "sha256": "7a219b3ebff0b4162c6533209bc2402e8f80f5f0899bcd45435c820df5f88582",
        "terms": 943,
    },
    "incidence_compact_ell": {
        "degree": 7,
        "sha256": "c245ad66f003f08ab8dd7d4ac6bf1b8ff501768dfb55954faa47180922a70388",
        "terms": 16,
    },
    "incidence_compact_qC": {
        "degree": 8,
        "sha256": "14d979e5e87e8c63e28417bef8ca2bfa5278cde9fb2004f2ca0e0d6ac87f4589",
        "terms": 32,
    },
    "incidence_compact_qD": {
        "degree": 8,
        "sha256": "dcff91b87a60d0f9ae50f39b549602cd13d7b3176b9a1a88fe1b308e2ef2dc02",
        "terms": 32,
    },
    "qC": {
        "degree": 12,
        "sha256": "89ac6b1c752f14da89fb1c9f2e3dca3a438fbd87fb7bcbc927a03c943e1a0212",
        "terms": 197,
    },
    "qD": {
        "degree": 12,
        "sha256": "bcee3e9dd49ebc1957ed817f0c16d8b302c89ed51626c9dbbbd53724efdcf7ba",
        "terms": 197,
    },
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
        predecessor_json["payload_sha256"] == IDENTITY_PAYLOAD,
        "identity predecessor payload binding",
    )
    require(
        predecessor_json["scope"]["assignment"]
        == "{{2,1/2},{2,b}}"
        and predecessor_json["scope"]["assignment_quantifier"]
        == "SINGLE_NORMALIZED_REPRESENTATIVE",
        "identity predecessor representative binding",
    )
    require(
        predecessor_json["assignment_scope"]["status"]
        == "REPRESENTATIVE_ONLY"
        and predecessor_json["assignment_scope"]["other_assignments_status"]
        == "OPEN_SEPARATE_EXACT_SYSTEMS"
        and predecessor_json["assignment_scope"]["complete_system_covariance"]
        == "NOT_CLAIMED",
        "identity predecessor scope binding",
    )
    require(
        predecessor_json["conclusion"][
            "representative_fixed_moving_identity_2_0_empty"
        ]
        is True,
        "identity predecessor conclusion binding",
    )


def verify_partition(partition: dict[str, Any]) -> None:
    require(partition["equation_count"] == 4, "four q-slice equations")
    split = partition["leading_coefficient_split"]
    require(split["coefficient"] == "L=coeff_b^2(qC)", "L definition")
    require(split["exhaustive_charts"] == ["L=0", "L!=0"], "L split")
    zero = split["leading_zero"]
    require(
        zero["generators"]
        == ["L", "qC", "qD", "eC", "eD", "t*Hbasic-1"],
        "leading-zero generators",
    )
    require(
        zero["localized_dimension"] == -1
        and zero["localized_groebner_basis"] == "1"
        and zero["linear_coefficient_zero_subchart_unit"] is True,
        "leading-zero unit ideal",
    )

    quadratic = partition["quadratic_chart"]
    expected_factors = [
        (2, "w-1", "DECLARED_PARENT_UNIT"),
        (1, "w^2-cd", "SEPARATE_INCIDENCE_CHART"),
        (1, "cd-1", "DECLARED_PARENT_UNIT"),
        (2, "5cd-4c-4d+5", "DECLARED_RECONSTRUCTION_UNIT"),
        (1, "q_essential", "SYMMETRIC_PIVOT_PARTITION"),
    ]
    actual_factors = [
        (row["exponent"], row["factor"], row["terminal"])
        for row in quadratic["complete_terminal_factorization"]
    ]
    require(actual_factors == expected_factors, "complete terminal factors")
    require(len({factor for _, factor, _ in actual_factors}) == 5, "unique factors")
    require(quadratic["factor_unit"] == -1, "factorization unit")

    incidence = quadratic["incidence_cd_eq_w2"]
    require(incidence["compact_substitution"] == "d=w^2/c", "incidence substitution")
    require(incidence["essential_equation_degrees"] == [8, 8], "incidence degrees")
    require(
        incidence["localized_dimension"] == -1
        and incidence["localized_groebner_basis"] == "1",
        "incidence unit ideal",
    )
    require(
        incidence["generators"]
        == [
            "qC",
            "qD",
            "eC",
            "eD",
            "cd-w^2",
            "t*Hbasic*L*Hfixed-1",
        ],
        "incidence generators",
    )

    retained = quadratic["q_essential"]
    require(
        retained["symmetric_equations"]
        == ["Q(s,p,w)=0", "A(s,p,w)=0", "B(s,p,w)=0"],
        "symmetric equations",
    )
    require(
        retained["support_dimension"] == 1
        and retained["support_pointwise_equations"]
        == ["p=-w", "5s+4w-4=0"],
        "support curve",
    )
    for key in (
        "first_pivot_ordinary_localized_groebner_basis",
        "second_pivot_coefficient_zero_localized_groebner_basis",
        "second_pivot_ordinary_localized_groebner_basis",
    ):
        require(retained[key] == "1", f"{key} unit")
    for key in (
        "first_pivot_ordinary_localized_dimension",
        "second_pivot_coefficient_zero_localized_dimension",
        "second_pivot_ordinary_localized_dimension",
    ):
        require(retained[key] == -1, f"{key} empty")
    require(
        retained["first_pivot_support_status"]
        == "coefficient and constant vanish",
        "first pivot support",
    )
    require(partition["rabinowitsch_equation"] == "t*H-1", "Rabinowitsch")


def verify_data(data: dict[str, Any]) -> None:
    require(
        set(data)
        == {
            "assignment_scope",
            "artifacts",
            "branch_partition",
            "conclusion",
            "field",
            "nonclaims",
            "normalization",
            "payload_sha256",
            "polynomial_metrics",
            "provenance",
            "schema",
            "scope",
            "workboard",
        },
        "top-level fields",
    )
    require(
        data["schema"]
        == "kb-mca-v4-m2-diagonal-112-fixed-positive-balanced-v1",
        "schema",
    )
    require(data["payload_sha256"] == EXPECTED_PAYLOAD, "expected payload")
    require(data["payload_sha256"] == payload_hash(data), "payload hash")
    require(
        data["scope"]
        == {
            "assignment": "{{2,1/2},{2,b}}",
            "assignment_quantifier": "SINGLE_NORMALIZED_REPRESENTATIVE",
            "ledger_movement": 0,
            "profile": "(a,b,c)=(1,1,2)",
            "root_distribution": [1, 1],
            "source_branch": "saturated source-line",
            "target": (
                "normalized fixed-moving aligned-positive "
                "balanced representative"
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
            "root_distribution": [1, 1],
            "target_quadratic": "(W-1/c)(W-1/d)",
        },
        "normalization",
    )
    require(
        data["workboard"]
        == {
            "B_star": 274980728111395087,
            "agreement": 1116048,
            "architecture": None,
            "atom_or_cell": (
                "K3_M2_DIAGONAL_112_FIXED_POSITIVE_"
                "BALANCED_1_1_REPRESENTATIVE"
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
            "representative_all_three_root_distributions_empty": True,
            "representative_balanced_1_1_empty": True,
            "representative_crossed_0_2_status": (
                "CLOSED_BY_STACKED_PREDECESSOR_SAME_REPRESENTATIVE"
            ),
            "representative_identity_2_0_status": (
                "CLOSED_BY_IMMEDIATE_PREDECESSOR_SAME_REPRESENTATIVE"
            ),
        },
        "conclusion",
    )
    require(data["polynomial_metrics"] == EXPECTED_METRICS, "polynomial metrics")
    verify_partition(data["branch_partition"])
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
    require(
        data["nonclaims"]
        == [
            "no balanced (1,1) claim for the other seven fixed-moving assignments",
            (
                "no crossed (0,2) or identity (2,0) claim for the other "
                "seven fixed-moving assignments"
            ),
            "no projective covariance claim for the complete source system",
            "no moving-moving deletion",
            "no near-aligned positive deletion",
            "no exceptional unsaturated-orbit or biquadratic-source-cover deletion",
            "no complete (1,1,2) row deletion",
            "no owner, payment, K3 value, KoalaBear row bound, or Prize closure",
            "no use of full quotient or endpoint H-product identities",
        ],
        "nonclaims",
    )


def tamper_selftest(data: dict[str, Any]) -> int:
    mutations: list[Callable[[dict[str, Any]], None]] = [
        lambda x: x.__setitem__("schema", "wrong"),
        lambda x: x.__setitem__("payload_sha256", "0" * 64),
        lambda x: x["scope"].__setitem__("ledger_movement", 1),
        lambda x: x["scope"].__setitem__("profile", "(2,0,1)"),
        lambda x: x["scope"]["root_distribution"].__setitem__(0, 2),
        lambda x: x["scope"].__setitem__("source_branch", "exceptional"),
        lambda x: x["scope"].__setitem__("target", "moving-moving"),
        lambda x: x["scope"].__setitem__(
            "assignment", "{{2,1/2},{2,1/b}}"
        ),
        lambda x: x["scope"].__setitem__(
            "assignment_quantifier", "FULL_FIXED_MOVING_ORBIT"
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
        lambda x: x["normalization"]["root_distribution"].__setitem__(1, 2),
        lambda x: x["normalization"].__setitem__("target_quadratic", "(W-1/c)^2"),
        lambda x: x["assignment_scope"].__setitem__("status", "FULL_ORBIT"),
        lambda x: x["assignment_scope"].__setitem__(
            "complete_system_covariance", "PROVED"
        ),
        lambda x: x["assignment_scope"].__setitem__(
            "closed_assignment_count", 8
        ),
        lambda x: x["assignment_scope"].__setitem__("open_assignment_count", 0),
        lambda x: x["assignment_scope"].__setitem__(
            "other_assignments_status", "CLOSED"
        ),
        lambda x: x["assignment_scope"]["covariance_mismatch"].__setitem__(
            "endpoint_only_normalizer", "preserves complete system"
        ),
        lambda x: x["conclusion"].__setitem__(
            "representative_balanced_1_1_empty", False
        ),
        lambda x: x["conclusion"].__setitem__(
            "representative_all_three_root_distributions_empty", False
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
            "representative_crossed_0_2_status", "CLOSED_ALL_ASSIGNMENTS"
        ),
        lambda x: x["conclusion"].__setitem__(
            "representative_identity_2_0_status", "CLOSED_ALL_ASSIGNMENTS"
        ),
        lambda x: x["conclusion"].__setitem__("moving_moving_status", "CLOSED"),
        lambda x: x["conclusion"].__setitem__("k3_status", "CLOSED"),
        lambda x: x["conclusion"].__setitem__("ledger_movement", 1),
        lambda x: x["branch_partition"].__setitem__("equation_count", 3),
        lambda x: x["branch_partition"]["leading_coefficient_split"][
            "exhaustive_charts"
        ].pop(),
        lambda x: x["branch_partition"]["leading_coefficient_split"][
            "leading_zero"
        ]["generators"].pop(),
        lambda x: x["branch_partition"]["leading_coefficient_split"][
            "leading_zero"
        ].__setitem__("localized_dimension", 0),
        lambda x: x["branch_partition"]["leading_coefficient_split"][
            "leading_zero"
        ].__setitem__("localized_groebner_basis", "nonunit"),
        lambda x: x["branch_partition"]["quadratic_chart"][
            "complete_terminal_factorization"
        ].pop(1),
        lambda x: x["branch_partition"]["quadratic_chart"][
            "complete_terminal_factorization"
        ][1].__setitem__("terminal", "DECLARED_PARENT_UNIT"),
        lambda x: x["branch_partition"]["quadratic_chart"][
            "complete_terminal_factorization"
        ][1].__setitem__("factor", "cd-w^2"),
        lambda x: x["branch_partition"]["quadratic_chart"].__setitem__(
            "factor_unit", 1
        ),
        lambda x: x["branch_partition"]["quadratic_chart"][
            "incidence_cd_eq_w2"
        ].__setitem__("localized_dimension", 1),
        lambda x: x["branch_partition"]["quadratic_chart"][
            "incidence_cd_eq_w2"
        ].__setitem__("localized_groebner_basis", "nonunit"),
        lambda x: x["branch_partition"]["quadratic_chart"][
            "incidence_cd_eq_w2"
        ]["generators"].pop(),
        lambda x: x["branch_partition"]["quadratic_chart"][
            "incidence_cd_eq_w2"
        ]["essential_equation_degrees"].__setitem__(0, 7),
        lambda x: x["branch_partition"]["quadratic_chart"]["q_essential"][
            "symmetric_equations"
        ].pop(),
        lambda x: x["branch_partition"]["quadratic_chart"]["q_essential"][
            "support_pointwise_equations"
        ].pop(),
        lambda x: x["branch_partition"]["quadratic_chart"]["q_essential"].__setitem__(
            "support_dimension", 0
        ),
        lambda x: x["branch_partition"]["quadratic_chart"]["q_essential"].__setitem__(
            "first_pivot_ordinary_localized_dimension", 1
        ),
        lambda x: x["branch_partition"]["quadratic_chart"]["q_essential"].__setitem__(
            "second_pivot_coefficient_zero_localized_groebner_basis", "nonunit"
        ),
        lambda x: x["branch_partition"]["quadratic_chart"]["q_essential"].__setitem__(
            "second_pivot_ordinary_localized_dimension", 1
        ),
        lambda x: x["branch_partition"].__setitem__("rabinowitsch_equation", "t*H"),
        lambda x: x["polynomial_metrics"]["qC"].__setitem__("terms", 196),
        lambda x: x["polynomial_metrics"]["qD"].__setitem__("sha256", "0" * 64),
        lambda x: x["polynomial_metrics"]["L"].__setitem__("degree", 9),
        lambda x: x["polynomial_metrics"]["Q"].__setitem__("terms", 42),
        lambda x: x["polynomial_metrics"]["A"].__setitem__("sha256", "0" * 64),
        lambda x: x["polynomial_metrics"]["B"].__setitem__("degree", 7),
        lambda x: x["polynomial_metrics"]["incidence_compact_qC"].__setitem__(
            "terms", 31
        ),
        lambda x: x["polynomial_metrics"]["incidence_compact_ell"].__setitem__(
            "sha256", "0" * 64
        ),
        lambda x: x["provenance"]["predecessor"].__setitem__("commit", "0" * 40),
        lambda x: x["provenance"]["predecessor"].__setitem__(
            "payload_sha256", "0" * 64
        ),
        lambda x: x["provenance"]["predecessor"].__setitem__(
            "certificate_blob_oid", "0" * 40
        ),
        lambda x: x["provenance"]["predecessor"].__setitem__(
            "assignment_quantifier", "FULL_FIXED_MOVING_ORBIT"
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
        "PASS representative fixed-positive balanced (1,1) "
        f"payload={data['payload_sha256']} terminal=EMPTY"
    )
    if args.tamper_selftest:
        rejected = tamper_selftest(data)
        print(f"PASS tamper self-test: {rejected}/{rejected} rejected")


if __name__ == "__main__":
    main()
