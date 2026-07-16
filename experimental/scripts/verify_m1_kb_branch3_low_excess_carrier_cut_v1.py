#!/usr/bin/env python3
"""Verify the KoalaBear branch-3 low-excess common-carrier route cut.

The packet proves a conditional global owner.  For one retained finite-slope
set, choose one actual noncontained exact-A witness per slope.  If the union of
the resulting actual error supports lies in one common carrier of excess at
most ten over the RS redundancy, the independent-union or
agreement-weighted transverse-secant theorem gives a budget-fitting global
cap.  Without such a single-carrier certificate, the verifier fails closed
and makes no ledger deduction.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]

SCHEMA = "rs-mca-m1-kb-branch3-low-excess-carrier-cut-v1"
ARTIFACT_KIND = "M1_KB_BRANCH3_LOW_EXCESS_COMMON_CARRIER_ROUTE_CUT"
STATUS = (
    "PROVED_CONDITIONAL_GLOBAL_CARRIER_OWNER_"
    "EXACT_EXCESS10_BUDGET_CUTOFF_FAIL_CLOSED_ROW_OPEN"
)

CERT_DIR = (
    ROOT
    / "experimental/data/certificates/"
    "m1-kb-branch3-low-excess-carrier-cut-v1"
)
CERT_PATH = CERT_DIR / "m1_kb_branch3_low_excess_carrier_cut_v1.json"
README_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-branch3-low-excess-carrier-cut-v1/README.md"
)

NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_kb_branch3_low_excess_carrier_cut_v1.md"
)
VERIFIER_REL = Path(
    "experimental/scripts/"
    "verify_m1_kb_branch3_low_excess_carrier_cut_v1.py"
)
BRANCH2_NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_branch2_rank_deep_owner_v1.md"
)
BRANCH2_CERT_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-branch2-rank-deep-owner-v1/"
    "m1_kb_branch2_rank_deep_owner_v1.json"
)
BRANCH2_VERIFIER_REL = Path(
    "experimental/scripts/verify_m1_kb_branch2_rank_deep_owner_v1.py"
)
TRANSVERSE_REL = Path(
    "experimental/notes/thresholds/"
    "agreement_weighted_transverse_secant.md"
)
TRANSVERSE_VERIFIER_REL = Path(
    "experimental/scripts/verify_agreement_weighted_transverse_secant.py"
)
THRESHOLDS_REL = Path("experimental/rs_mca_thresholds.tex")
FIRST_MATCH_NOTE_REL = Path(
    "experimental/notes/thresholds/"
    "kb_mca_1116048_first_match_ledger_v1.md"
)
POST_C5_CERT_REL = Path(
    "experimental/data/certificates/"
    "m1-fp2-post-c5-mask-incidence-v1/"
    "m1_fp2_post_c5_mask_incidence_v1.json"
)

P = 2_130_706_433
EXTENSION_DEGREE = 6
Q_LINE = P**EXTENSION_DEGREE
N = 2_097_152
K = 1_048_576
A = 1_116_048
R = N - K
J = N - A
T = A - K
DENOMINATOR = 1 << 128
B_STAR = (Q_LINE - 1) // DENOMINATOR
U_PAID_BEFORE = 2_602_220_945
B_REMAINING_BEFORE = B_STAR - U_PAID_BEFORE
K_REM = 4_807_520
LARGEST_BUDGET_FITTING_EXCESS = 10
FIRST_BUDGET_FAILING_EXCESS = 11

V2_ORDER = [
    "contained_or_noncontained_failure",
    "rank_drop_or_pivot_failure",
    "tangent_common_line_residue",
    "quotient_periodic_or_divisor_stabilized",
    "planted_prefix_structured",
    "extension_valued_slope",
    "residual_base_slope_universe",
    "sparse_sigma_or_sparse_support",
    "m1_half_turn_or_coefficient_shadow",
    "primitive_qfin_residual",
]

TOP_KEYS = {
    "schema",
    "artifact_kind",
    "status",
    "source_bindings",
    "row",
    "branch3_scope",
    "actual_witness_contract",
    "carrier_dichotomy",
    "budget_table",
    "classifier_contract",
    "charges",
    "ledger",
    "audit_sections",
    "nonclaims",
    "payload_sha256",
}

EDGE_CASES = [
    "Each selected error support is the actual nonzero support tied to a declared noncontained exact-A witness, not the padded co-support.",
    "One carrier must contain the selected actual error supports for the entire retained slope set.",
    "Several unrelated carriers cannot be charged by taking the maximum of their individual caps.",
    "The kappa=0 case uses the independent-union theorem; the transverse-secant theorem is invoked only for kappa>=1.",
    "A supplied carrier with excess above ten does not prove the minimum global excess is above ten.",
    "Failure to exhibit a valid low-excess carrier emits UNPAID_NOT_CERTIFIED_LOW_EXCESS.",
    "The low-excess theorem is monotone under arbitrary earlier first-match deletion.",
    "The packet does not identify low carrier excess with the full tangent/common-line/residue-line branch.",
    "Null ledger entries are not zero.",
]

REMAINING_RISKS = [
    "No witness-exhaustive theorem proves that every retained branch-3 family has global carrier excess at most ten.",
    "The high-excess residual has no paid owner.",
    "The frozen tangent/common-line/residue-line label still lacks an exact exhaustive row-specific projector.",
    "Branches 4 and 5, the field-full quadratic support union, U_2, U_Q, and U_A remain open.",
    "The complete KoalaBear row inequality remains undecided.",
]

NONCLAIMS = [
    "This packet does not prove the KoalaBear row safe.",
    "This packet does not close branch 3.",
    "This packet does not prove that a low-excess global carrier exists.",
    "This packet does not prove a bounded cover by several low-excess carriers.",
    "This packet does not charge the cap once per carrier, support, chart, or slope.",
    "This packet does not bank B_10 in the deployed upper ledger.",
    "This packet does not identify transverse low-excess carriers with every tangent, common-line, or residue-line component.",
    "This packet does not determine U_2, U_Q, or U_A.",
    "This packet does not begin the degree-three parameter class.",
]


class VerificationError(RuntimeError):
    """A source, arithmetic, schema, or semantic check failed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def require_int(value: Any, label: str) -> None:
    require(type(value) is int, f"{label} is not an exact JSON integer")


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise VerificationError(f"nonstandard JSON constant: {value}")


def parse_json(text: str, label: str) -> dict[str, Any]:
    value = json.loads(
        text,
        object_pairs_hook=reject_duplicate_keys,
        parse_constant=reject_constant,
    )
    require(type(value) is dict, f"top-level JSON is not an object: {label}")
    return value


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"missing JSON: {path}")
    return parse_json(path.read_text(encoding="utf-8"), str(path))


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def canonical_hash(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def payload_hash(value: dict[str, Any]) -> str:
    clean = copy.deepcopy(value)
    clean.pop("payload_sha256", None)
    return canonical_hash(clean)


def file_hash(relative: Path) -> str:
    path = ROOT / relative
    require(path.is_file(), f"missing source binding: {relative}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def binding(binding_id: str, relative: Path, role: str) -> dict[str, str]:
    return {
        "binding_id": binding_id,
        "path": relative.as_posix(),
        "sha256": file_hash(relative),
        "role": role,
    }


def expected_source_bindings() -> list[dict[str, str]]:
    return [
        binding("packet-note", NOTE_REL, "human-readable proof and audit"),
        binding(
            "certificate-readme",
            README_REL,
            "replay commands and machine-readable scope summary",
        ),
        binding(
            "python-verifier",
            VERIFIER_REL,
            "exact arithmetic, schema, and mutation replay",
        ),
        binding(
            "branch2-note",
            BRANCH2_NOTE_REL,
            "full-row-rank branch-2 complement and actual-support bridge",
        ),
        binding(
            "branch2-certificate",
            BRANCH2_CERT_REL,
            "machine-readable predecessor ledger and branch order",
        ),
        binding(
            "branch2-verifier",
            BRANCH2_VERIFIER_REL,
            "predecessor semantic and mutation replay",
        ),
        binding(
            "transverse-secant-owner",
            TRANSVERSE_REL,
            "agreement-weighted one-global-carrier theorem",
        ),
        binding(
            "transverse-secant-verifier",
            TRANSVERSE_VERIFIER_REL,
            "deterministic finite-field stress replay for the imported owner",
        ),
        binding(
            "exact-thresholds",
            THRESHOLDS_REL,
            "exact-support reduction and independent-union ray theorem",
        ),
        binding(
            "first-match-note",
            FIRST_MATCH_NOTE_REL,
            "frozen KoalaBear branch labels",
        ),
        binding(
            "post-c5-certificate",
            POST_C5_CERT_REL,
            "machine-readable open branch-3 source status",
        ),
    ]


def carrier_cap(excess: int) -> int:
    require_int(excess, "excess")
    require(excess >= 0, "negative carrier excess")
    if excess == 0:
        return J + 1
    numerator = math.comb(R + excess, excess + 1)
    denominator = math.comb(R + excess - J - 1, excess)
    require(denominator > 0, "nonpositive transverse-secant denominator")
    return numerator // denominator


def monotonicity_margin(excess: int) -> int:
    """Numerator minus denominator in B_(k+1)^raw / B_k^raw - 1."""
    require_int(excess, "monotonicity excess")
    require(excess >= 1, "monotonicity formula starts at excess one")
    return J * (excess + 2) - R + 1


def classify_supplied_carrier(
    excess: int,
    *,
    actual_noncontained_witnesses: bool,
    actual_error_supports: bool,
    one_global_carrier: bool,
    all_supports_contained: bool,
    transversality: bool,
) -> dict[str, Any]:
    require_int(excess, "classifier excess")
    require(excess >= 0, "classifier excess is negative")
    contract_holds = (
        actual_noncontained_witnesses
        and actual_error_supports
        and one_global_carrier
        and all_supports_contained
        and transversality
    )
    if contract_holds and excess <= LARGEST_BUDGET_FITTING_EXCESS:
        return {
            "terminal": "CERTIFIED_LOW_EXCESS_COMMON_CARRIER",
            "paid_owner": (
                "INDEPENDENT_UNION_RAYS"
                if excess == 0
                else "AGREEMENT_WEIGHTED_TRANSVERSE_SECANT"
            ),
            "certified_excess": excess,
            "global_distinct_slope_cap": str(carrier_cap(excess)),
            "budget_fits": True,
            "ledger_charge_banked": False,
        }
    return {
        "terminal": "UNPAID_NOT_CERTIFIED_LOW_EXCESS",
        "paid_owner": None,
        "certified_excess": None,
        "global_distinct_slope_cap": None,
        "budget_fits": None,
        "ledger_charge_banked": False,
    }


def expected_row() -> dict[str, Any]:
    return {
        "row_id": "koalabear-mca-A1116048",
        "p": P,
        "ambient_extension_degree": EXTENSION_DEGREE,
        "q_line": str(Q_LINE),
        "n": N,
        "k": K,
        "agreement_A": A,
        "redundancy_R": R,
        "error_cap_j": J,
        "full_row_rank_threshold_t": T,
        "R_minus_j": R - J,
        "B_star": str(B_STAR),
        "U_paid_before": str(U_PAID_BEFORE),
        "B_remaining_before": str(B_REMAINING_BEFORE),
        "challenge_scope": "distinct finite slopes in F_(p^6)",
    }


def expected_branch3_scope() -> dict[str, Any]:
    return {
        "v2_order": V2_ORDER,
        "branch_index_one_based": 3,
        "frozen_branch_label": "tangent_common_line_residue",
        "predecessor_branch": "rank_drop_or_pivot_failure",
        "predecessor_branch_closed": True,
        "safe_full_row_rank_envelope": (
            "Z_3_pre(f,g)=Bad_A(f,g)_MINUS_Z_2_env(f,g)"
        ),
        "literal_first_match_branch3_subset_of_safe_envelope": True,
        "safe_envelope_may_retain_earlier_branch1_slopes": True,
        "monotone_under_earlier_first_match_deletion": True,
        "carrier_scope": "ONE_RECEIVED_PAIR_AT_A_TIME",
        "full_row_rank_required": True,
        "branch3_projector_claimed_complete": False,
        "low_excess_synonymous_with_frozen_branch_label": False,
        "scope_status": "BRANCH3_ENVELOPE_OWNER_NOT_EXHAUSTIVE_PROJECTOR",
    }


def expected_actual_witness_contract() -> dict[str, Any]:
    return {
        "one_witness_per_retained_slope": True,
        "witness": "(gamma,S_gamma,c_gamma)",
        "exact_support_size": A,
        "line_word": "y_gamma=f+gamma*g",
        "actual_error": "e_gamma=y_gamma-c_gamma",
        "actual_error_support": "E_gamma=supp(e_gamma)",
        "actual_support_not_padded_co_support": True,
        "actual_support_subset_of_D_minus_S_gamma": True,
        "actual_error_weight_lower_bound_on_branch2_complement": T,
        "actual_error_weight_upper_bound": J,
        "syndrome_equation": "H*e_gamma=s(f)+gamma*s(g)",
        "transversality": (
            "{s(f),s(g)}_NOT_SUBSET_V_(E_gamma)"
        ),
        "transversality_reason": (
            "IF_BOTH_SYNDROMES_LAY_IN_V_E_THEN_THE_PAIR_WOULD_BE_"
            "SIMULTANEOUSLY_EXPLAINED_ON_D_MINUS_E_SUPERSET_S_gamma"
        ),
        "arbitrary_explaining_codeword_without_declared_bad_witness_allowed": False,
        "finite_slopes_only": True,
    }


def expected_carrier_dichotomy() -> dict[str, Any]:
    return {
        "selected_global_union": "U_sel=UNION_(gamma in Z) E_gamma",
        "minimum_global_excess": (
            "kappa_star(Z)=MIN_over_one_valid_witness_selection_per_slope_"
            "MAX(0,|U_sel|-R)"
        ),
        "mathematical_minimum_defined": True,
        "empty_slope_set_minimum_excess": 0,
        "minimum_computed_by_this_packet": False,
        "single_global_carrier_required": True,
        "multiple_carriers_combine_by": "SUM_REQUIRED_NOT_MAXIMUM",
        "kappa_zero_owner": "INDEPENDENT_UNION_RAYS",
        "kappa_zero_cap_formula": "j+1",
        "positive_kappa_owner": "AGREEMENT_WEIGHTED_TRANSVERSE_SECANT",
        "positive_kappa_cap_formula": (
            "floor(C(R+kappa,kappa+1)/"
            "C(R+kappa-j-1,kappa))"
        ),
        "positive_kappa_carrier_size_identity": "|U_sel|=R+kappa",
        "pair_level_low_excess_alternative": "kappa_star<=10",
        "pair_level_high_excess_alternative": "kappa_star>=11",
        "pair_level_dichotomy_exhaustive": True,
        "high_excess_owner": None,
        "executable_default_terminal": "UNPAID_NOT_CERTIFIED_LOW_EXCESS",
        "default_terminal_does_not_assert_kappa_star_ge_11": True,
    }


def expected_budget_table() -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    for excess in range(FIRST_BUDGET_FAILING_EXCESS + 1):
        cap = carrier_cap(excess)
        records.append(
            {
                "excess": excess,
                "owner": (
                    "INDEPENDENT_UNION_RAYS"
                    if excess == 0
                    else "AGREEMENT_WEIGHTED_TRANSVERSE_SECANT"
                ),
                "cap": str(cap),
                "budget_fits": cap <= B_REMAINING_BEFORE,
                "remaining_if_used": str(B_REMAINING_BEFORE - cap),
            }
        )
    margins = [
        {
            "from_excess": excess,
            "to_excess": excess + 1,
            "raw_ratio_numerator_minus_denominator": monotonicity_margin(
                excess
            ),
            "strictly_positive": monotonicity_margin(excess) > 0,
        }
        for excess in range(1, FIRST_BUDGET_FAILING_EXCESS)
    ]
    return {
        "records": records,
        "record_count": len(records),
        "largest_budget_fitting_excess": LARGEST_BUDGET_FITTING_EXCESS,
        "first_budget_failing_excess": FIRST_BUDGET_FAILING_EXCESS,
        "B_10": str(carrier_cap(10)),
        "B_11": str(carrier_cap(11)),
        "B_10_fits": carrier_cap(10) <= B_REMAINING_BEFORE,
        "B_11_fits": carrier_cap(11) <= B_REMAINING_BEFORE,
        "B_10_remaining": str(B_REMAINING_BEFORE - carrier_cap(10)),
        "B_11_shortfall": str(carrier_cap(11) - B_REMAINING_BEFORE),
        "raw_cap_monotonicity_ratio": (
            "((R+kappa+1)*(kappa+1))/"
            "((kappa+2)*(R+kappa-j))"
        ),
        "raw_ratio_difference": "j*(kappa+2)-R+1",
        "monotonicity_checks": margins,
        "exact_integer_arithmetic": True,
    }


def expected_classifier_contract() -> dict[str, Any]:
    valid_flags = {
        "actual_noncontained_witnesses": True,
        "actual_error_supports": True,
        "one_global_carrier": True,
        "all_supports_contained": True,
        "transversality": True,
    }
    return {
        "required_inputs": [
            "ONE_DECLARED_NONCONTAINED_EXACT_A_WITNESS_PER_SLOPE",
            "ACTUAL_NONZERO_ERROR_SUPPORT_FOR_EACH_WITNESS",
            "ONE_GLOBAL_CARRIER_FOR_THE_ENTIRE_RETAINED_SET",
            "ALL_SELECTED_SUPPORTS_CONTAINED_IN_THAT_CARRIER",
            "TRANSVERSALITY_FOR_EVERY_SELECTED_WITNESS",
            "CERTIFIED_CARRIER_EXCESS",
        ],
        "certified_low_excess_terminal": (
            "CERTIFIED_LOW_EXCESS_COMMON_CARRIER"
        ),
        "fail_closed_terminal": "UNPAID_NOT_CERTIFIED_LOW_EXCESS",
        "symbolic_controls": {
            "excess_zero": classify_supplied_carrier(0, **valid_flags),
            "excess_ten": classify_supplied_carrier(10, **valid_flags),
            "excess_eleven": classify_supplied_carrier(11, **valid_flags),
            "missing_transversality": classify_supplied_carrier(
                2,
                **{**valid_flags, "transversality": False},
            ),
            "multiple_carriers": classify_supplied_carrier(
                2,
                **{**valid_flags, "one_global_carrier": False},
            ),
            "padded_supports": classify_supplied_carrier(
                2,
                **{**valid_flags, "actual_error_supports": False},
            ),
            "missing_noncontained_witness": classify_supplied_carrier(
                2,
                **{
                    **valid_flags,
                    "actual_noncontained_witnesses": False,
                },
            ),
            "support_outside_carrier": classify_supplied_carrier(
                2,
                **{**valid_flags, "all_supports_contained": False},
            ),
        },
        "controls_are_semantic_unit_cases_not_deployed_witnesses": True,
        "deployed_low_excess_certificate_present": False,
        "deployed_terminal": "UNPAID_NOT_CERTIFIED_LOW_EXCESS",
    }


def expected_ledger() -> dict[str, Any]:
    return {
        "U_paid_before": str(U_PAID_BEFORE),
        "B_remaining_before": str(B_REMAINING_BEFORE),
        "conditional_max_low_excess_cap": str(carrier_cap(10)),
        "conditional_U_paid_if_global_low_excess_exhaustive": str(
            U_PAID_BEFORE + carrier_cap(10)
        ),
        "conditional_B_remaining_if_global_low_excess_exhaustive": str(
            B_REMAINING_BEFORE - carrier_cap(10)
        ),
        "actual_charge_banked": None,
        "packet_banked_charge": "0",
        "branch3_charge": None,
        "U_paid_after": str(U_PAID_BEFORE),
        "B_remaining_after": str(B_REMAINING_BEFORE),
        "K_rem": K_REM,
        "local_owner_contract_proved": True,
        "global_low_excess_exhaustiveness_proved": False,
        "high_excess_owner_proved": False,
        "branch3_closed": False,
        "ledger_consequence": False,
        "U_2": None,
        "U_Q": None,
        "U_A": None,
        "lhs": None,
        "row_complete": False,
        "inequality_status": "UNDECIDED_OPEN_COMPONENTS",
        "next_attack": "UNPAID_NOT_CERTIFIED_LOW_EXCESS",
    }


def expected_audit_sections() -> dict[str, Any]:
    return {
        "parameter_dependence": (
            "GENERAL_OWNER_DEPENDS_ON_R_J_KAPPA_"
            "BUDGET_CUTOFF_KOALABEAR_SPECIFIC"
        ),
        "layer_cake_dyadic_summability": "NOT_APPLICABLE",
        "moment_markov_chebyshev": "NOT_APPLICABLE",
        "numerical_evidence": (
            "EXACT_BIG_INTEGER_REPLAY_ONLY_NO_ASYMPTOTIC_EXTRAPOLATION"
        ),
        "edge_cases": EDGE_CASES,
        "remaining_risks": REMAINING_RISKS,
        "verdict": (
            "GREEN_LOCAL_OWNER_ROUTE_CUT_"
            "YELLOW_BRANCH3_AND_ROW"
        ),
    }


def validate_sources() -> None:
    thresholds = (ROOT / THRESHOLDS_REL).read_text(encoding="utf-8")
    for anchor in (
        r"\label{lem:exact-agreement-reduction}",
        r"\label{prop:syndrome-line-normal-form}",
        r"\label{lem:independent-union-rays}",
        r"\abs Z\le t+1",
    ):
        require(anchor in thresholds, f"exact-threshold anchor missing: {anchor}")

    transverse = (ROOT / TRANSVERSE_REL).read_text(encoding="utf-8")
    for anchor in (
        "Agreement-weighted transverse-secant payment",
        "sum_{gamma in Z} binom(|A_gamma|-1,kappa)",
        "binom(R+kappa-t-1,kappa)",
        "The result is monotone under arbitrary earlier first-match deletion.",
        "No such atlas or cover is inferred here.",
    ):
        require(anchor in transverse, f"transverse-secant anchor missing: {anchor}")

    branch2 = load_json(ROOT / BRANCH2_CERT_REL)
    require(
        branch2["row"]["n"] == N
        and branch2["row"]["k"] == K
        and branch2["row"]["agreement_A"] == A
        and branch2["row"]["redundancy_R"] == R
        and branch2["row"]["co_support_size_j"] == J
        and branch2["row"]["hankel_depth_t"] == T,
        "branch-2 row parameters drift",
    )
    require(
        branch2["branch2_first_match"]["v2_order"] == V2_ORDER
        and branch2["branch2_first_match"]["branch2_local_policy_complete"]
        is True
        and branch2["branch2_first_match"][
            "full_row_rank_pivot_success_survives_to_branch"
        ]
        == 3,
        "branch-2 successor interface drift",
    )
    require(
        int(branch2["ledger"]["U_paid_after"]) == U_PAID_BEFORE
        and int(branch2["ledger"]["B_remaining_after"])
        == B_REMAINING_BEFORE
        and branch2["ledger"]["K_rem"] == K_REM
        and branch2["ledger"]["branch2_closed"] is True,
        "branch-2 ledger drift",
    )

    post_c5 = load_json(ROOT / POST_C5_CERT_REL)
    branch3 = post_c5["mask_inventory"]["records"][2]
    require(
        branch3["order"] == 3
        and branch3["branch"] == "tangent_common_line_residue"
        and branch3["actual_slope_projector_complete"] is False,
        "post-C5 branch-3 open status drift",
    )

    require(R - J == T, "R-j=t arithmetic drift")
    require(
        R + LARGEST_BUDGET_FITTING_EXCESS <= N,
        "carrier padding no longer fits inside the domain",
    )
    require(
        carrier_cap(10) <= B_REMAINING_BEFORE < carrier_cap(11),
        "budget cutoff is no longer 10/11",
    )
    require(
        all(
            monotonicity_margin(excess) > 0
            for excess in range(1, FIRST_BUDGET_FAILING_EXCESS)
        ),
        "raw cap monotonicity failed before the cutoff",
    )


def build_certificate() -> dict[str, Any]:
    validate_sources()
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "artifact_kind": ARTIFACT_KIND,
        "status": STATUS,
        "source_bindings": expected_source_bindings(),
        "row": expected_row(),
        "branch3_scope": expected_branch3_scope(),
        "actual_witness_contract": expected_actual_witness_contract(),
        "carrier_dichotomy": expected_carrier_dichotomy(),
        "budget_table": expected_budget_table(),
        "classifier_contract": expected_classifier_contract(),
        "charges": [],
        "ledger": expected_ledger(),
        "audit_sections": expected_audit_sections(),
        "nonclaims": NONCLAIMS,
        "payload_sha256": "",
    }
    artifact["payload_sha256"] = payload_hash(artifact)
    return artifact


def require_exact_keys(
    value: dict[str, Any], expected: set[str], label: str
) -> None:
    require(set(value) == expected, f"{label} keys drift")


def validate_source_bindings(bindings: Any) -> None:
    require(type(bindings) is list, "source_bindings is not a list")
    require(
        canonical_bytes(bindings)
        == canonical_bytes(expected_source_bindings()),
        "source binding path/hash/role drift",
    )
    seen: set[str] = set()
    for source in bindings:
        require(type(source) is dict, "source binding is not an object")
        require_exact_keys(
            source,
            {"binding_id", "path", "sha256", "role"},
            "source binding",
        )
        require(
            all(
                type(source[key]) is str
                for key in ("binding_id", "path", "sha256", "role")
            ),
            "source binding type drift",
        )
        source_id = source["binding_id"]
        require(source_id not in seen, "duplicate source binding id")
        seen.add(source_id)
        path = Path(source["path"])
        require(
            not path.is_absolute() and ".." not in path.parts,
            "unsafe source path",
        )
        require(
            source["sha256"] == file_hash(path),
            f"source hash drift: {path}",
        )


def validate_certificate(
    artifact: dict[str, Any], *, exact_rebuild: bool = False
) -> None:
    require_exact_keys(artifact, TOP_KEYS, "top-level")
    require(artifact["schema"] == SCHEMA, "schema drift")
    require(artifact["artifact_kind"] == ARTIFACT_KIND, "artifact kind drift")
    require(artifact["status"] == STATUS, "status drift")
    require(
        artifact["payload_sha256"] == payload_hash(artifact),
        "payload hash drift",
    )
    validate_source_bindings(artifact["source_bindings"])

    expected_sections = {
        "row": expected_row(),
        "branch3_scope": expected_branch3_scope(),
        "actual_witness_contract": expected_actual_witness_contract(),
        "carrier_dichotomy": expected_carrier_dichotomy(),
        "budget_table": expected_budget_table(),
        "classifier_contract": expected_classifier_contract(),
        "ledger": expected_ledger(),
        "audit_sections": expected_audit_sections(),
    }
    for label, expected in expected_sections.items():
        require(type(artifact[label]) is dict, f"{label} is not an object")
        require(
            canonical_bytes(artifact[label]) == canonical_bytes(expected),
            f"{label} payload or JSON type drift",
        )
    require(
        artifact["nonclaims"] == NONCLAIMS,
        "nonclaim list drift",
    )
    require(artifact["charges"] == [], "unexpected banked charge record")

    row = artifact["row"]
    for key in (
        "p",
        "ambient_extension_degree",
        "n",
        "k",
        "agreement_A",
        "redundancy_R",
        "error_cap_j",
        "full_row_rank_threshold_t",
        "R_minus_j",
    ):
        require_int(row[key], f"row.{key}")
    require(
        row["R_minus_j"] == row["full_row_rank_threshold_t"],
        "row R-j=t identity drift",
    )

    scope = artifact["branch3_scope"]
    require_int(
        scope["branch_index_one_based"],
        "branch3_scope.branch_index_one_based",
    )
    require(
        scope["branch_index_one_based"] == 3
        and scope["predecessor_branch_closed"] is True
        and scope["literal_first_match_branch3_subset_of_safe_envelope"]
        is True
        and scope["monotone_under_earlier_first_match_deletion"] is True
        and scope["branch3_projector_claimed_complete"] is False
        and scope["low_excess_synonymous_with_frozen_branch_label"] is False,
        "branch-3 scope drift",
    )

    witness = artifact["actual_witness_contract"]
    for key in (
        "exact_support_size",
        "actual_error_weight_lower_bound_on_branch2_complement",
        "actual_error_weight_upper_bound",
    ):
        require_int(witness[key], f"actual_witness_contract.{key}")
    require(
        witness["actual_support_not_padded_co_support"] is True
        and witness["actual_support_subset_of_D_minus_S_gamma"] is True
        and witness[
            "arbitrary_explaining_codeword_without_declared_bad_witness_allowed"
        ]
        is False
        and witness["finite_slopes_only"] is True,
        "actual-witness semantics drift",
    )

    dichotomy = artifact["carrier_dichotomy"]
    require(
        dichotomy["single_global_carrier_required"] is True
        and dichotomy["multiple_carriers_combine_by"]
        == "SUM_REQUIRED_NOT_MAXIMUM"
        and dichotomy["empty_slope_set_minimum_excess"] == 0
        and dichotomy["minimum_computed_by_this_packet"] is False
        and dichotomy["high_excess_owner"] is None
        and dichotomy["default_terminal_does_not_assert_kappa_star_ge_11"]
        is True,
        "carrier dichotomy scope drift",
    )

    table = artifact["budget_table"]
    require_int(table["record_count"], "budget_table.record_count")
    require_int(
        table["largest_budget_fitting_excess"],
        "budget_table.largest_budget_fitting_excess",
    )
    require_int(
        table["first_budget_failing_excess"],
        "budget_table.first_budget_failing_excess",
    )
    require(
        table["record_count"] == 12
        and table["largest_budget_fitting_excess"] == 10
        and table["first_budget_failing_excess"] == 11
        and table["B_10_fits"] is True
        and table["B_11_fits"] is False
        and table["exact_integer_arithmetic"] is True,
        "budget cutoff drift",
    )
    for index, record in enumerate(table["records"]):
        require_int(record["excess"], f"budget_table.records[{index}].excess")
        require(
            record["excess"] == index
            and int(record["cap"]) == carrier_cap(index)
            and record["budget_fits"]
            is (carrier_cap(index) <= B_REMAINING_BEFORE),
            f"budget record drift at excess {index}",
        )

    classifier = artifact["classifier_contract"]
    require(
        classifier["controls_are_semantic_unit_cases_not_deployed_witnesses"]
        is True
        and classifier["deployed_low_excess_certificate_present"] is False
        and classifier["deployed_terminal"]
        == "UNPAID_NOT_CERTIFIED_LOW_EXCESS",
        "classifier deployment status drift",
    )
    controls = classifier["symbolic_controls"]
    require(
        controls["excess_zero"]["paid_owner"] == "INDEPENDENT_UNION_RAYS"
        and controls["excess_ten"]["global_distinct_slope_cap"]
        == str(carrier_cap(10))
        and controls["excess_eleven"]["paid_owner"] is None
        and controls["missing_transversality"]["paid_owner"] is None
        and controls["multiple_carriers"]["paid_owner"] is None
        and controls["padded_supports"]["paid_owner"] is None
        and controls["missing_noncontained_witness"]["paid_owner"] is None
        and controls["support_outside_carrier"]["paid_owner"] is None,
        "fail-closed classifier drift",
    )

    ledger = artifact["ledger"]
    require_int(ledger["K_rem"], "ledger.K_rem")
    require(
        ledger["actual_charge_banked"] is None
        and ledger["packet_banked_charge"] == "0"
        and ledger["branch3_charge"] is None
        and int(ledger["U_paid_after"]) == U_PAID_BEFORE
        and int(ledger["B_remaining_after"]) == B_REMAINING_BEFORE
        and ledger["global_low_excess_exhaustiveness_proved"] is False
        and ledger["high_excess_owner_proved"] is False
        and ledger["branch3_closed"] is False
        and ledger["ledger_consequence"] is False
        and ledger["U_2"] is None
        and ledger["U_Q"] is None
        and ledger["U_A"] is None
        and ledger["lhs"] is None
        and ledger["row_complete"] is False,
        "no-bank ledger boundary drift",
    )

    if exact_rebuild:
        require(
            canonical_bytes(artifact) == canonical_bytes(build_certificate()),
            "certificate differs from exact rebuild",
        )


def set_path(value: Any, path: tuple[Any, ...], replacement: Any) -> None:
    current = value
    for token in path[:-1]:
        current = current[token]
    current[path[-1]] = replacement


def run_tamper_selftest(artifact: dict[str, Any]) -> int:
    rejected = 0

    def mutate(name: str, path: tuple[Any, ...], replacement: Any) -> None:
        nonlocal rejected
        candidate = copy.deepcopy(artifact)
        set_path(candidate, path, replacement)
        candidate["payload_sha256"] = payload_hash(candidate)
        try:
            validate_certificate(candidate)
        except VerificationError:
            rejected += 1
            return
        raise VerificationError(f"tamper accepted: {name}")

    mutate("schema", ("schema",), SCHEMA + "-drift")
    mutate("artifact-kind", ("artifact_kind",), "WRONG_KIND")
    mutate("status", ("status",), "ROW_CLOSED")
    mutate("row-n", ("row", "n"), N - 1)
    mutate("row-k", ("row", "k"), K - 1)
    mutate("row-A", ("row", "agreement_A"), A - 1)
    mutate("row-R", ("row", "redundancy_R"), R - 1)
    mutate("row-j", ("row", "error_cap_j"), J - 1)
    mutate("row-t", ("row", "full_row_rank_threshold_t"), T - 1)
    mutate("row-R-minus-j", ("row", "R_minus_j"), T - 1)
    mutate("row-q", ("row", "q_line"), str(Q_LINE - 1))
    mutate("row-budget", ("row", "B_star"), str(B_STAR - 1))
    mutate(
        "row-B-remaining",
        ("row", "B_remaining_before"),
        str(B_REMAINING_BEFORE - 1),
    )
    mutate("bool-as-int", ("row", "n"), True)
    mutate(
        "negative-bigint",
        ("row", "B_remaining_before"),
        "-1",
    )
    mutate(
        "branch-order",
        ("branch3_scope", "v2_order", 2),
        "quotient_periodic_or_divisor_stabilized",
    )
    mutate(
        "branch-index",
        ("branch3_scope", "branch_index_one_based"),
        4,
    )
    mutate(
        "predecessor-open",
        ("branch3_scope", "predecessor_branch_closed"),
        False,
    )
    mutate(
        "literal-not-subset",
        (
            "branch3_scope",
            "literal_first_match_branch3_subset_of_safe_envelope",
        ),
        False,
    )
    mutate(
        "monotonicity-false",
        ("branch3_scope", "monotone_under_earlier_first_match_deletion"),
        False,
    )
    mutate(
        "projector-invented",
        ("branch3_scope", "branch3_projector_claimed_complete"),
        True,
    )
    mutate(
        "label-alias",
        ("branch3_scope", "low_excess_synonymous_with_frozen_branch_label"),
        True,
    )
    mutate(
        "padded-support",
        ("actual_witness_contract", "actual_support_not_padded_co_support"),
        False,
    )
    mutate(
        "support-not-subset",
        (
            "actual_witness_contract",
            "actual_support_subset_of_D_minus_S_gamma",
        ),
        False,
    )
    mutate(
        "lower-weight-off-by-one",
        (
            "actual_witness_contract",
            "actual_error_weight_lower_bound_on_branch2_complement",
        ),
        T - 1,
    )
    mutate(
        "upper-weight-off-by-one",
        ("actual_witness_contract", "actual_error_weight_upper_bound"),
        J + 1,
    )
    mutate(
        "arbitrary-codeword",
        (
            "actual_witness_contract",
            "arbitrary_explaining_codeword_without_declared_bad_witness_allowed",
        ),
        True,
    )
    mutate(
        "include-infinity",
        ("actual_witness_contract", "finite_slopes_only"),
        False,
    )
    mutate(
        "minimum-falsely-computed",
        ("carrier_dichotomy", "minimum_computed_by_this_packet"),
        True,
    )
    mutate(
        "empty-set-excess",
        ("carrier_dichotomy", "empty_slope_set_minimum_excess"),
        1,
    )
    mutate(
        "global-carrier-not-required",
        ("carrier_dichotomy", "single_global_carrier_required"),
        False,
    )
    mutate(
        "multiple-carriers-max",
        ("carrier_dichotomy", "multiple_carriers_combine_by"),
        "MAXIMUM",
    )
    mutate(
        "kappa-zero-owner",
        ("carrier_dichotomy", "kappa_zero_owner"),
        "AGREEMENT_WEIGHTED_TRANSVERSE_SECANT",
    )
    mutate(
        "denominator-off-by-one",
        ("carrier_dichotomy", "positive_kappa_cap_formula"),
        "floor(C(R+kappa,kappa+1)/C(R+kappa-j,kappa))",
    )
    mutate(
        "false-high-owner",
        ("carrier_dichotomy", "high_excess_owner"),
        "EXISTING_OWNER",
    )
    mutate(
        "fallback-asserts-minimum",
        (
            "carrier_dichotomy",
            "default_terminal_does_not_assert_kappa_star_ge_11",
        ),
        False,
    )
    for excess in range(12):
        mutate(
            f"cap-{excess}",
            ("budget_table", "records", excess, "cap"),
            str(carrier_cap(excess) + 1),
        )
        mutate(
            f"fit-{excess}",
            ("budget_table", "records", excess, "budget_fits"),
            not (carrier_cap(excess) <= B_REMAINING_BEFORE),
        )
    mutate(
        "cutoff-ten",
        ("budget_table", "largest_budget_fitting_excess"),
        11,
    )
    mutate(
        "cutoff-eleven",
        ("budget_table", "first_budget_failing_excess"),
        12,
    )
    mutate("B10", ("budget_table", "B_10"), str(carrier_cap(10) + 1))
    mutate("B11", ("budget_table", "B_11"), str(carrier_cap(11) - 1))
    mutate("B10-fits", ("budget_table", "B_10_fits"), False)
    mutate("B11-fits", ("budget_table", "B_11_fits"), True)
    mutate(
        "ratio-formula",
        ("budget_table", "raw_cap_monotonicity_ratio"),
        "WRONG_RATIO",
    )
    mutate(
        "ratio-margin",
        (
            "budget_table",
            "monotonicity_checks",
            0,
            "raw_ratio_numerator_minus_denominator",
        ),
        monotonicity_margin(1) - 1,
    )
    mutate(
        "deployed-certificate-invented",
        (
            "classifier_contract",
            "deployed_low_excess_certificate_present",
        ),
        True,
    )
    mutate(
        "deployed-terminal-paid",
        ("classifier_contract", "deployed_terminal"),
        "CERTIFIED_LOW_EXCESS_COMMON_CARRIER",
    )
    mutate(
        "excess11-paid",
        (
            "classifier_contract",
            "symbolic_controls",
            "excess_eleven",
            "paid_owner",
        ),
        "AGREEMENT_WEIGHTED_TRANSVERSE_SECANT",
    )
    mutate(
        "missing-transversality-paid",
        (
            "classifier_contract",
            "symbolic_controls",
            "missing_transversality",
            "paid_owner",
        ),
        "AGREEMENT_WEIGHTED_TRANSVERSE_SECANT",
    )
    mutate(
        "multiple-carriers-paid",
        (
            "classifier_contract",
            "symbolic_controls",
            "multiple_carriers",
            "paid_owner",
        ),
        "AGREEMENT_WEIGHTED_TRANSVERSE_SECANT",
    )
    mutate(
        "padded-supports-paid",
        (
            "classifier_contract",
            "symbolic_controls",
            "padded_supports",
            "paid_owner",
        ),
        "AGREEMENT_WEIGHTED_TRANSVERSE_SECANT",
    )
    mutate(
        "missing-noncontained-witness-paid",
        (
            "classifier_contract",
            "symbolic_controls",
            "missing_noncontained_witness",
            "paid_owner",
        ),
        "AGREEMENT_WEIGHTED_TRANSVERSE_SECANT",
    )
    mutate(
        "support-outside-carrier-paid",
        (
            "classifier_contract",
            "symbolic_controls",
            "support_outside_carrier",
            "paid_owner",
        ),
        "AGREEMENT_WEIGHTED_TRANSVERSE_SECANT",
    )
    mutate(
        "charges-nonempty",
        ("charges",),
        [{"owner": "AGREEMENT_WEIGHTED_TRANSVERSE_SECANT", "amount": "1"}],
    )
    mutate(
        "bank-charge-zero",
        ("ledger", "actual_charge_banked"),
        "0",
    )
    mutate(
        "packet-charge",
        ("ledger", "packet_banked_charge"),
        str(carrier_cap(10)),
    )
    mutate(
        "branch3-charge-zero",
        ("ledger", "branch3_charge"),
        "0",
    )
    mutate(
        "bank-B10",
        ("ledger", "actual_charge_banked"),
        str(carrier_cap(10)),
    )
    mutate(
        "U-paid-after",
        ("ledger", "U_paid_after"),
        str(U_PAID_BEFORE + carrier_cap(10)),
    )
    mutate(
        "B-remaining-after",
        ("ledger", "B_remaining_after"),
        str(B_REMAINING_BEFORE - carrier_cap(10)),
    )
    mutate(
        "exhaustiveness-invented",
        ("ledger", "global_low_excess_exhaustiveness_proved"),
        True,
    )
    mutate(
        "high-excess-owner-invented",
        ("ledger", "high_excess_owner_proved"),
        True,
    )
    mutate("branch3-closed", ("ledger", "branch3_closed"), True)
    mutate("ledger-consequence", ("ledger", "ledger_consequence"), True)
    mutate("U2-null-to-zero", ("ledger", "U_2"), 0)
    mutate("UQ-null-to-zero", ("ledger", "U_Q"), 0)
    mutate("UA-null-to-zero", ("ledger", "U_A"), 0)
    mutate("lhs-null-to-zero", ("ledger", "lhs"), "0")
    mutate("row-complete", ("ledger", "row_complete"), True)
    mutate(
        "inequality-decided",
        ("ledger", "inequality_status"),
        "PROVED_SAFE",
    )
    mutate(
        "next-attack-overclaims-high-excess",
        ("ledger", "next_attack"),
        "UNPAID_HIGH_EXCESS_COMMON_CARRIER_RESIDUAL",
    )
    mutate(
        "source-hash",
        ("source_bindings", 0, "sha256"),
        "0" * 64,
    )
    mutate(
        "source-path",
        ("source_bindings", 0, "path"),
        "../unsafe",
    )
    mutate(
        "source-role",
        ("source_bindings", 0, "role"),
        "wrong role",
    )
    mutate(
        "duplicate-binding-id",
        ("source_bindings", 1, "binding_id"),
        artifact["source_bindings"][0]["binding_id"],
    )
    mutate(
        "nonclaim-deleted",
        ("nonclaims", 0),
        "This packet proves the row safe.",
    )

    candidate = copy.deepcopy(artifact)
    candidate["unexpected_top_level"] = True
    candidate["payload_sha256"] = payload_hash(candidate)
    try:
        validate_certificate(candidate)
    except VerificationError:
        rejected += 1
    else:
        raise VerificationError("tamper accepted: unknown top-level key")

    candidate = copy.deepcopy(artifact)
    candidate["ledger"]["unexpected_nested"] = True
    candidate["payload_sha256"] = payload_hash(candidate)
    try:
        validate_certificate(candidate)
    except VerificationError:
        rejected += 1
    else:
        raise VerificationError("tamper accepted: unknown nested key")

    bad_payload = copy.deepcopy(artifact)
    bad_payload["payload_sha256"] = "0" * 64
    try:
        validate_certificate(bad_payload)
    except VerificationError:
        rejected += 1
    else:
        raise VerificationError("tamper accepted: payload hash")

    try:
        parse_json('{"a":1,"a":2}', "duplicate-key-control")
    except VerificationError:
        rejected += 1
    else:
        raise VerificationError("tamper accepted: duplicate JSON key")

    try:
        parse_json('{"a":NaN}', "nonstandard-constant-control")
    except VerificationError:
        rejected += 1
    else:
        raise VerificationError("tamper accepted: NaN")

    return rejected


def write_certificate(artifact: dict[str, Any]) -> None:
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    CERT_PATH.write_text(
        json.dumps(artifact, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    group.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    artifact = build_certificate()

    if args.write:
        validate_certificate(artifact, exact_rebuild=True)
        write_certificate(artifact)
        print(f"WROTE {CERT_PATH.relative_to(ROOT)}")
        return 0

    if args.check:
        loaded = load_json(CERT_PATH)
        validate_certificate(loaded, exact_rebuild=True)
        print("PASS m1-kb-branch3-low-excess-carrier-cut-v1")
        print(
            "cutoff: B_10=%d <= %d < B_11=%d"
            % (
                carrier_cap(10),
                B_REMAINING_BEFORE,
                carrier_cap(11),
            )
        )
        print(
            "ledger: no charge banked; U_paid=%d; B_remaining=%d"
            % (U_PAID_BEFORE, B_REMAINING_BEFORE)
        )
        return 0

    rejected = run_tamper_selftest(artifact)
    print(f"PASS tamper-selftest: {rejected}/{rejected} mutations rejected")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VerificationError as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
